"""
Merge multiple metadata.pkl files into one combined dataset.

Usage:
    python merge_metadata.py \
        data/celeba_processed/metadata.pkl \
        data/primer_processed/metadata.pkl \
        --output data/merged/metadata.pkl
"""
import argparse
import pickle
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", help="metadata.pkl files to merge")
    parser.add_argument("--output", default="data/merged/metadata.pkl")
    args = parser.parse_args()

    merged = []
    for path in args.inputs:
        with open(path, "rb") as f:
            samples = pickle.load(f)
            print(f"{path}: {len(samples)} samples")
            merged.extend(samples)

    random.shuffle(merged)
    print(f"\nTotal merged: {len(merged)} samples")

    import os
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "wb") as f:
        pickle.dump(merged, f)
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
