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
from typing import Optional

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


def extract_lip_crop(image: np.ndarray, landmarks) -> Optional[np.ndarray]:
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


def load_gender_filter(attr_path: str) -> set[str]:
    female_ids: set[str] = set()
    with open(attr_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Male") == "-1":
                female_ids.add(row["image_id"])
    print(f"Gender filter: {len(female_ids)} female images found")
    return female_ids


def process_dataset(input_dir: str, output_dir: str, limit: Optional[int] = None, female_only: bool = False, balance: int = 0):
    os.makedirs(output_dir, exist_ok=True)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    image_dir = input_dir
    image_paths = sorted(Path(image_dir).glob("*.jpg"))

    if limit:
        image_paths = image_paths[:limit]

    female_ids: Optional[set[str]] = None
    if female_only:
        attr_path = os.path.join(os.path.dirname(input_dir.rstrip("/")), "list_attr_celeba.csv")
        if os.path.exists(attr_path):
            female_ids = load_gender_filter(attr_path)
            print(f"Filtering to {len(female_ids)} female images")
        else:
            print(f"Warning: {attr_path} not found — skipping gender filter")

    samples = []
    skipped = 0

    for img_path in tqdm(image_paths, desc="Processing images"):
        if female_ids is not None and img_path.name not in female_ids:
            skipped += 1
            continue
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

    # Balance per class if requested
    if balance > 0:
        by_label: dict[str, list] = {}
        for s in samples:
            by_label.setdefault(s["label"], []).append(s)
        samples = []
        import random
        for label in by_label:
            random.shuffle(by_label[label])
            samples.extend(by_label[label][:balance])
        print(f"Balanced to max {balance} per class: {len(samples)} total")

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
    parser.add_argument("--female-only", action="store_true", help="Only use female images (requires list_attr_celeba.csv)")
    parser.add_argument("--balance", type=int, default=0, help="Max samples per class (0=unlimited)")
    args = parser.parse_args()
    process_dataset(args.input, args.output, args.limit, args.female_only, args.balance)
