"""
Visualize labeled CelebA samples to verify K-Means clustering quality.

Shows a grid of sample faces grouped by predicted label (Pinkish/Brownish/Dark).

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

    fig, axes = plt.subplots(len(labels), n, figsize=(n * 2.5, len(labels) * 2.5))

    for row, label in enumerate(labels):
        pool = by_label.get(label, [])
        chosen = random.sample(pool, min(n, len(pool)))
        for col in range(n):
            ax = axes[row, col]
            if col < len(chosen):
                img = cv2.imread(chosen[col]["path"])
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    ax.imshow(img_rgb)
                lm = chosen[col].get("lab_mean", [0, 0, 0])
                ax.set_title(f"L={lm[0]:.0f} a={lm[1]:.0f} b={lm[2]:.0f}", fontsize=7)
            ax.axis("off")
            if col == 0:
                ax.set_ylabel(label, fontsize=10, color=colors[label], fontweight="bold")

    plt.tight_layout()
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
