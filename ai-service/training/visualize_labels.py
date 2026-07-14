"""
Visualize labeled CelebA samples to verify K-Means clustering quality.

Layout:
    [Pinkish]  [Brownish]  [Dark]
    img         img         img
    img         img         img
    ...

Usage:
    python training/visualize_labels.py
"""

import argparse
import os
import pickle
import random

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def visualize(metadata_path: str, output_path: str, samples_per_class: int = 9):
    with open(metadata_path, "rb") as f:
        samples = pickle.load(f)

    by_label: dict[str, list] = {}
    for s in samples:
        by_label.setdefault(s["label"], []).append(s)

    labels = ["Pinkish", "Brownish", "Dark"]
    colors = {"Pinkish": "#e74c8b", "Brownish": "#8b5e3c", "Dark": "#4a1942"}
    n = samples_per_class
    ncols = len(labels)

    fig, axes = plt.subplots(n, ncols, figsize=(ncols * 2.5, n * 2.5))
    fig.suptitle("K-Means Clustering Results — CelebA Lip Colors", fontsize=14, fontweight="bold")

    for col, label in enumerate(labels):
        pool = by_label.get(label, [])
        chosen = random.sample(pool, min(n, len(pool)))
        for row in range(n):
            ax = axes[row, col]
            if row < len(chosen):
                crop_path = chosen[row].get("crop_path") or chosen[row]["path"]
                img = cv2.imread(crop_path)
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    ax.imshow(img_rgb)
                lm = chosen[row].get("lab_mean", [0, 0, 0])
                ax.set_xlabel(f"L={lm[0]:.0f} a={lm[1]:.0f} b={lm[2]:.0f}", fontsize=6)
            ax.set_xticks([])
            ax.set_yticks([])
            if row == 0:
                ax.set_title(label, fontsize=12, color=colors[label], fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Label check saved to {output_path}")

    for label in labels:
        count = len(by_label.get(label, []))
        print(f"  {label}: {count} samples")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="./data/processed/metadata.pkl")
    parser.add_argument("--output", default="./data/processed/label_check.png")
    parser.add_argument("--samples", type=int, default=9, help="Samples per class")
    args = parser.parse_args()
    visualize(args.data, args.output, args.samples)
