"""
Batch test Hybrid Recommendation System.
Outputs Tabel 4.18 and Tabel 4.19 for skripsi Bab IV.

Usage:
    python test_recommendation.py --input ./data/primer --output ./test_results
    python test_recommendation.py --input ./data/celeba_processed/crops --output ./test_results --limit 30
"""
import argparse
import csv
import json
import os
import pickle
import sys
import time
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.pipeline.face_detection import detect_face
from app.pipeline.lip_segmentation import segment_lips
from app.pipeline.classifier import load_model as load_classifier, classify_lip_type
from app.pipeline.recommender import get_top3

IMG_SIZE = (224, 224)
MAX_RGB_DIST = 441.67


def load_image_rgb(path: str) -> np.ndarray:
    img = cv2.imread(str(path))
    if img is None:
        return None
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def process_image(image_path: str) -> dict:
    image_rgb = load_image_rgb(image_path)
    if image_rgb is None:
        return None

    face_result = detect_face(cv2.imencode(".jpg", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))[1].tobytes())
    if not face_result["face_detected"]:
        return None

    lip_result = segment_lips(
        cv2.imencode(".jpg", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))[1].tobytes(),
        face_result["landmarks"],
    )
    if lip_result["status"] != "success":
        return None

    rgb = lip_result["mean_rgb"]
    cropped_bytes = lip_result["cropped_bytes"]

    classification = classify_lip_type(list(cropped_bytes))
    lip_type = classification["label"]
    confidence = classification["confidence"]

    recommendations = get_top3(lip_type, (rgb["r"], rgb["g"], rgb["b"]))

    return {
        "rgb": rgb,
        "lip_type": lip_type,
        "confidence": confidence,
        "recommendations": recommendations,
    }


def save_table_png(rows_418: list, summary: dict, output_dir: str):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Tabel 4.18
        if rows_418:
            n = len(rows_418)
            fig, ax = plt.subplots(figsize=(14, 0.5 * n + 1.5))
            ax.axis("off")
            col_labels = ["No", "RGB User", "Tipe", "Rekomendasi", "RGB Lipstik", "Distance", "Similarity"]
            cell_text = [
                [r["no"], r["rgb_user"], r["lip_type"], r["rekomendasi"], r["rgb_lipstick"], f"{r['distance']:.2f}", f"{r['similarity']:.1f}%"]
                for r in rows_418
            ]
            table = ax.table(cellText=cell_text, colLabels=col_labels, loc="center")
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.3)
            ax.set_title("Tabel 4.18 Hasil Pengujian Hybrid Recommendation System", fontsize=10, fontweight="bold")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "tabel_418.png"), dpi=200, bbox_inches="tight")
            plt.close()

        # Tabel 4.19
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.axis("off")
        sum_cells = [[k, v] for k, v in summary.items()]
        table = ax.table(cellText=sum_cells, colLabels=["Parameter", "Nilai"], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        ax.set_title("Tabel 4.19 Rekapitulasi Similarity", fontsize=10, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "tabel_419.png"), dpi=200, bbox_inches="tight")
        plt.close()

        print(f"Tabel PNG disimpan ke {output_dir}/tabel_418.png, tabel_419.png")
    except ImportError:
        print("matplotlib not installed — skip tabel PNG")
    except Exception as e:
        print(f"Warning: tabel PNG gagal: {e}")


def format_table(results: list, output_dir: str):
    # Tabel 4.18 — Sample results
    rows_418 = []
    for i, r in enumerate(results[:10]):
        recs = r["recommendations"]
        for j, rec in enumerate(recs):
            rows_418.append({
                "no": i + 1 if j == 0 else "",
                "rgb_user": f"({r['rgb']['r']}, {r['rgb']['g']}, {r['rgb']['b']})",
                "lip_type": r["lip_type"] if j == 0 else '" "',
                "rekomendasi": rec["shade_name"],
                "rgb_lipstick": f"({rec['rgb']['r']}, {rec['rgb']['g']}, {rec['rgb']['b']})",
                "distance": rec["distance"],
                "similarity": rec["similarity"],
            })

    with open(os.path.join(output_dir, "tabel_418.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["no", "rgb_user", "lip_type", "rekomendasi", "rgb_lipstick", "distance", "similarity"])
        w.writeheader()
        w.writerows(rows_418)

    # Tabel 4.19 — Summary
    top1_sim = [r["recommendations"][0]["similarity"] for r in results]
    top2_sim = [r["recommendations"][1]["similarity"] for r in results]
    top3_sim = [r["recommendations"][2]["similarity"] for r in results]

    summary = {
        "Jumlah data uji": len(results),
        "Rata-rata Similarity Top-1": f"{np.mean(top1_sim):.2f}%",
        "Rata-rata Similarity Top-2": f"{np.mean(top2_sim):.2f}%",
        "Rata-rata Similarity Top-3": f"{np.mean(top3_sim):.2f}%",
        "Similarity tertinggi": f"{max(top1_sim):.2f}%",
        "Similarity terendah": f"{min(top3_sim):.2f}%",
    }

    with open(os.path.join(output_dir, "tabel_419.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Print to console
    print("\n" + "=" * 70)
    print("Tabel 4.18 — Hasil Pengujian Hybrid Recommendation System")
    print("=" * 70)
    print(f"{'No':<4} {'RGB User':<20} {'Tipe':<12} {'Rekomendasi':<18} {'RGB Lipstik':<20} {'Dist':<8} {'Sim':<6}")
    print("-" * 108)
    for row in rows_418:
        print(f"{row['no']:<4} {row['rgb_user']:<20} {row['lip_type']:<12} {row['rekomendasi']:<18} {row['rgb_lipstick']:<20} {row['distance']:<8.2f} {row['similarity']:<6.1f}")

    print("\n" + "=" * 50)
    print("Tabel 4.19 — Rekapitulasi Similarity")
    print("=" * 50)
    for k, v in summary.items():
        print(f"{k:<35} {v}")

    print(f"\nHasil disimpan ke {output_dir}/")

    # Save PNG tables
    save_table_png(rows_418, summary, output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Folder berisi gambar uji")
    parser.add_argument("--metadata", help="Path ke metadata.pkl (merged dataset)")
    parser.add_argument("--output", default="./test_results", help="Folder output")
    parser.add_argument("--limit", type=int, default=30, help="Max gambar yang diproses")
    args = parser.parse_args()

    if not args.input and not args.metadata:
        parser.error("Harap isi --input atau --metadata")

    os.makedirs(args.output, exist_ok=True)

    print("Loading classifier model...", flush=True)
    load_classifier()

    if args.metadata:
        with open(args.metadata, "rb") as f:
            samples = pickle.load(f)
        image_paths = [s["path"] for s in samples]
        if args.limit:
            image_paths = image_paths[:args.limit]
        print(f"Menggunakan metadata: {args.metadata} ({len(image_paths)} gambar)", flush=True)
    else:
        image_exts = ("*.jpg", "*.jpeg", "*.png")
        image_paths = []
        for ext in image_exts:
            from pathlib import Path
            image_paths.extend(sorted(Path(args.input).glob(ext)))
        if args.limit:
            image_paths = image_paths[:args.limit]
        print(f"Menggunakan folder: {args.input} ({len(image_paths)} gambar)", flush=True)

    print(f"Memproses {len(image_paths)} gambar...", flush=True)
    results = []
    for path in image_paths:
        result = process_image(str(path))
        if result:
            results.append(result)
            print(f"  ✓ {Path(path).name} → {result['lip_type']} (conf={result['confidence']:.2f})", flush=True)
        else:
            print(f"  ✗ {Path(path).name} → gagal (wajah/bibir tidak terdeteksi)", flush=True)

    print(f"\nBerhasil: {len(results)}/{len(image_paths)} gambar", flush=True)

    if not results:
        print("Tidak ada hasil, selesai.", flush=True)
        return

    format_table(results, args.output)


if __name__ == "__main__":
    main()
