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
from typing import Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm


# MediaPipe face mesh lip contour (outer + inner, excludes nose bridge)
LIP_LANDMARKS = [17, 61, 78, 80, 81, 82, 84, 87, 88, 91, 95, 146, 178, 181, 185, 191, 291, 308, 310, 311, 312, 314, 317, 318, 321, 324, 375, 402, 405, 409, 415]
LABEL_NAMES = ["Pinkish", "Brownish", "Dark"]


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
    image_paths = sorted(
        list(Path(image_dir).glob("*.jpg")) +
        list(Path(image_dir).glob("*.jpeg")) +
        list(Path(image_dir).glob("*.png"))
    )

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
    all_features = []
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

        # Extract rich color features
        lab = cv2.cvtColor(lip_crop, cv2.COLOR_RGB2LAB)
        lab_mean = np.mean(lab, axis=(0, 1))
        rgb_mean = np.mean(lip_crop, axis=(0, 1))
        hsv = cv2.cvtColor(lip_crop, cv2.COLOR_RGB2HSV)
        hsv_mean = np.mean(hsv, axis=(0, 1))
        rgb_std = np.std(lip_crop, axis=(0, 1))
        hsv_std = np.std(hsv, axis=(0, 1))

        # Color histogram (8 bins per channel, RGB)
        hist_feats = []
        for c in range(3):
            hist = cv2.calcHist([lip_crop], [c], None, [8], [0, 256])
            hist = hist.flatten() / max(hist.sum(), 1e-8)
            hist_feats.extend(hist)

        features = np.concatenate([lab_mean, rgb_mean, hsv_mean, rgb_std, hsv_std, hist_feats])
        all_features.append(features)

        # Save lip crop thumbnail
        crop_dir = os.path.join(output_dir, "crops")
        os.makedirs(crop_dir, exist_ok=True)
        crop_path = os.path.join(os.path.abspath(crop_dir), img_path.name)
        cv2.imwrite(crop_path, cv2.cvtColor(lip_crop, cv2.COLOR_RGB2BGR))

        samples.append({
            "path": str(img_path),
            "crop_path": crop_path,
            "features": features.tolist(),
        })

    # K-Means clustering on rich color features (k=3: Pinkish, Brownish, Dark)
    if not all_features:
        print("Error: No images with detectable faces/lips. Skipping K-Means.", flush=True)
        print(f"  Processed {len(samples)} samples, skipped {skipped}", flush=True)
        return samples

    print("\nRunning K-Means clustering...", flush=True)
    X_raw = np.array(all_features)
    scaler = StandardScaler()
    X = scaler.fit_transform(X_raw)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto").fit(X)

    # Sort clusters by L (brightness): brightest = Pinkish, middle = Brownish, darkest = Dark
    centroids_raw = kmeans.cluster_centers_  # scaled centroids
    # Find which cluster has highest LAB-L (index 0 in original space)
    centroids_lab_l = []
    for c in range(3):
        mask = kmeans.labels_ == c
        centroids_lab_l.append(X_raw[mask, 0].mean())  # LAB-L is index 0
    cluster_order = np.argsort(centroids_lab_l)[::-1]
    cluster_to_label = {cluster_order[0]: "Pinkish", cluster_order[1]: "Brownish", cluster_order[2]: "Dark"}

    for i, s in enumerate(samples):
        cluster = int(kmeans.labels_[i])
        s["label"] = cluster_to_label[cluster]
        s["confidence"] = round(0.75 + 0.15 * (1 - kmeans.inertia_ / (3 * X.var())), 2)

    print(f"Cluster centroids (LAB-L):")
    for c in range(3):
        label = cluster_to_label[c]
        print(f"  {label:10s}  mean_L={centroids_lab_l[c]:.1f}")

    # Visualize clustering (use first 3 features for 2D projection)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from sklearn.decomposition import PCA
        colors_map = {"Pinkish": "#e74c8b", "Brownish": "#8b5e3c", "Dark": "#4a1942"}
        labels_arr = [cluster_to_label[c] for c in kmeans.labels_]
        # PCA to 2D for visualization
        pca = PCA(n_components=2, random_state=42)
        X_2d = pca.fit_transform(X)
        fig, ax = plt.subplots(figsize=(8, 6))
        for cls in ["Pinkish", "Brownish", "Dark"]:
            mask = [l == cls for l in labels_arr]
            ax.scatter(X_2d[mask, 0], X_2d[mask, 1], c=colors_map[cls], label=cls, alpha=0.3, s=2)
        centroids_2d = pca.transform(kmeans.cluster_centers_)
        ax.scatter(centroids_2d[:, 0], centroids_2d[:, 1], c="black", marker="X", s=100, label="Centroid")
        ax.set_xlabel("PC1"), ax.set_ylabel("PC2")
        ax.legend()
        ax.set_title("K-Means Clustering (PCA projection)")
        plt.tight_layout()
        plot_path = os.path.join(output_dir, "clustering.png")
        plt.savefig(plot_path, dpi=150)
        plt.close()
        print(f"Clustering plot saved to {plot_path}", flush=True)
    except ImportError:
        print("matplotlib not installed — skipping clustering plot", flush=True)

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
