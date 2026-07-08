"""
Auto-label CelebA images by extracting lip regions and classifying by color.

Usage:
    python prepare_dataset.py [--input ./data/celeba/img_align_celeba] [--output ./data/processed] [--limit 50000]
"""

import argparse
import csv
import os
import sys
import pickle
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from tqdm import tqdm


LIP_LANDMARKS = list(range(61, 68)) + list(range(48, 61))


def classify_lip_color(lab_mean: np.ndarray) -> str:
    l, a, b = lab_mean
    if l < 40:
        return "Dark", 0.90
    elif a > 12 and l > 50:
        return "Pinkish", 0.85
    elif a <= 12 and l >= 40:
        return "Brownish", 0.85
    else:
        return "Dark", 0.80


def extract_lip_crop(image: np.ndarray, landmarks) -> np.ndarray | None:
    h, w, _ = image.shape
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in LIP_LANDMARKS]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x_min, x_max = max(0, min(xs) - 10), min(w, max(xs) + 10)
    y_min, y_max = max(0, min(ys) - 10), min(h, max(ys) + 10)
    if x_max - x_min < 20 or y_max - y_min < 10:
        return None
    crop = image[y_min:y_max, x_min:x_max]
    if crop.size == 0:
        return None
    return cv2.resize(crop, (128, 64))


def process_dataset(input_dir: str, output_dir: str, limit: int | None = None):
    os.makedirs(output_dir, exist_ok=True)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    image_dir = input_dir
    image_paths = sorted(Path(image_dir).glob("*.jpg"))

    if limit:
        image_paths = image_paths[:limit]

    samples = []
    skipped = 0

    for img_path in tqdm(image_paths, desc="Processing images"):
        image = cv2.imread(str(img_path))
        if image is None:
            skipped += 1
            continue
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            skipped += 1
            continue

        landmarks = results.multi_face_landmarks[0].landmark
        lip_crop = extract_lip_crop(image_rgb, landmarks)
        if lip_crop is None:
            skipped += 1
            continue

        lab = cv2.cvtColor(lip_crop, cv2.COLOR_RGB2LAB)
        lab_mean = np.mean(lab, axis=(0, 1))
        label, confidence = classify_lip_color(lab_mean)

        samples.append({
            "path": str(img_path),
            "label": label,
            "confidence": confidence,
            "lab_mean": lab_mean.tolist(),
        })

    label_counts = {}
    for s in samples:
        label_counts[s["label"]] = label_counts.get(s["label"], 0) + 1

    print(f"\nProcessed: {len(samples)} images")
    print(f"Skipped: {skipped}")
    print(f"Labels: {label_counts}")

    # Save metadata
    meta_path = os.path.join(output_dir, "metadata.pkl")
    with open(meta_path, "wb") as f:
        pickle.dump(samples, f)
    print(f"Metadata saved to {meta_path}")

    # Save label map for training
    with open(os.path.join(output_dir, "labels.txt"), "w") as f:
        for label in sorted(set(s["label"] for s in samples)):
            f.write(f"{label}\n")
    print(f"Labels saved to {output_dir}/labels.txt")

    face_mesh.close()
    return samples


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="./data/celeba/img_align_celeba")
    parser.add_argument("--output", default="./data/processed")
    parser.add_argument("--limit", type=int, default=None, help="Max images to process")
    args = parser.parse_args()
    process_dataset(args.input, args.output, args.limit)
