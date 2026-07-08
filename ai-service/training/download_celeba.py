"""
Download CelebA dataset via Kaggle.

Requires a Kaggle API token (~/.kaggle/kaggle.json).
See: https://www.kaggle.com/docs/api#authentication

Usage:
    python download_celeba.py [--output ./data/celeba]
"""

import argparse
import os
import sys
import zipfile


def download_celeba(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    try:
        import kagglehub
    except ImportError:
        print("Install kagglehub: pip install kagglehub")
        sys.exit(1)

    print("Downloading CelebA dataset via KaggleHub...")
    path = kagglehub.dataset_download("jessicali9530/celeba-dataset")

    print(f"Downloaded to cache: {path}")

    # Extract img_align_celeba.zip
    zip_path = os.path.join(path, "img_align_celeba.zip")
    if os.path.exists(zip_path):
        print(f"Extracting {zip_path} to {output_dir}...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(output_dir)
        print(f"Extracted to {output_dir}/img_align_celeba/")

    # Copy list_attr_celeba.csv for labeling
    csv_src = os.path.join(path, "list_attr_celeba.csv")
    csv_dst = os.path.join(output_dir, "list_attr_celeba.csv")
    if os.path.exists(csv_src) and not os.path.exists(csv_dst):
        import shutil
        shutil.copy2(csv_src, csv_dst)
        print(f"Copied attributes to {csv_dst}")

    print(f"\nDone. Images at: {output_dir}/img_align_celeba/")
    print(f"Attributes at: {output_dir}/list_attr_celeba.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="./data/celeba")
    args = parser.parse_args()
    download_celeba(args.output)
