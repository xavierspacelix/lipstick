"""
Prepare your own dataset for training.

Two modes:
  1. Pre-labeled folder structure:
       dataset/
         pinkish/   img1.jpg  img2.jpg  ...
         brownish/  img1.jpg  img2.jpg  ...
         dark/      img1.jpg  img2.jpg  ...

  2. Face images (auto-label via lip color):
       dataset/  img1.jpg  img2.jpg  ...

Usage:
  # Pre-labeled
  python prepare_custom.py --input ./my_dataset --labeled

  # Auto-label face images
  python prepare_custom.py --input ./my_face_photos

  # Output metadata.pkl goes to --output (default: ./data/processed/)
"""

import argparse
import os
import pickle
import sys
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from tqdm import tqdm


LIP_LANDMARKS = list(range(61, 68)) + list(range(48, 61))
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

LABEL_MAP_FOLDER = {
    "pinkish": "Pinkish",
    "brownish": "Brownish",
    "dark": "Dark",
    "pink": "Pinkish",
    "brown": "Brownish",
}


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


def process_folder_structure(input_dir: str, output_dir: str):
    """Mode 1: dataset/pinkish/*.jpg, dataset/brownish/*.jpg, etc."""
    samples = []

    for folder_name, label in LABEL_MAP_FOLDER.items():
        folder = Path(input_dir) / folder_name
        if not folder.exists():
            continue

        image_paths = [
            p for p in folder.iterdir()
            if p.suffix.lower() in IMG_EXTENSIONS
        ]

        for img_path in tqdm(image_paths, desc=f"Loading {label}"):
            samples.append({
                "path": str(img_path),
                "label": label,
                "confidence": 1.0,
            })

    if not samples:
        print(f"No labeled folders found in {input_dir}")
        print(f"Expected one of: {list(LABEL_MAP_FOLDER.keys())}")
        sys.exit(1)

    save_samples(samples, output_dir)


def process_face_images(input_dir: str, output_dir: str):
    """Mode 2: folder of face images, auto-label by lip color."""
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5
    )

    image_paths = [
        p for p in Path(input_dir).iterdir()
        if p.suffix.lower() in IMG_EXTENSIONS
    ]

    if not image_paths:
        print(f"No images found in {input_dir}")
        sys.exit(1)

    samples = []
    skipped = 0

    for img_path in tqdm(image_paths, desc="Auto-labeling"):
        image = cv2.imread(str(img_path))
        if image is None:
            skipped += 1
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            skipped += 1
            continue

        lip_crop = extract_lip_crop(image_rgb, results.multi_face_landmarks[0].landmark)
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
        })

    face_mesh.close()

    if not samples:
        print("No faces detected in any image.")
        sys.exit(1)

    print(f"\nProcessed: {len(samples)}, Skipped: {skipped}")
    label_counts = {}
    for s in samples:
        label_counts[s["label"]] = label_counts.get(s["label"], 0) + 1
    print(f"Labels: {label_counts}")

    save_samples(samples, output_dir)


def save_samples(samples: list, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    meta_path = os.path.join(output_dir, "metadata.pkl")
    with open(meta_path, "wb") as f:
        pickle.dump(samples, f)
    print(f"\nSaved {len(samples)} samples to {meta_path}")

    labels = sorted(set(s["label"] for s in samples))
    with open(os.path.join(output_dir, "labels.txt"), "w") as f:
        for label in labels:
            f.write(f"{label}\n")
    print(f"Labels: {labels}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="./data/processed")
    parser.add_argument(
        "--labeled",
        action="store_true",
        help="Images are in labeled subfolders (pinkish/, brownish/, dark/)",
    )
    args = parser.parse_args()

    if args.labeled:
        process_folder_structure(args.input, args.output)
    else:
        process_face_images(args.input, args.output)
