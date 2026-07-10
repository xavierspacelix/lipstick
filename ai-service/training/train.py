"""
Train MobileNetV2 lip classifier from auto-labeled dataset.

Usage:
    python train.py [--data ./data/processed/metadata.pkl] [--output ./app/models/mobilenetv2_lip.h5] [--epochs 20]
"""

import argparse
import os
import pickle
import sys
import random

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tqdm import tqdm


IMG_SIZE = (224, 224)
LABEL_MAP = {"Pinkish": 0, "Brownish": 1, "Dark": 2}


def load_samples(metadata_path: str, balance: int = 0):
    with open(metadata_path, "rb") as f:
        samples = pickle.load(f)

    by_label: dict[str, list] = {}
    for s in samples:
        if s["label"] not in LABEL_MAP:
            continue
        by_label.setdefault(s["label"], []).append(s)

    print(f"Available samples per class: { {k: len(v) for k, v in by_label.items()} }")

    if balance > 0:
        for k in by_label:
            random.shuffle(by_label[k])
            by_label[k] = by_label[k][:balance]
        print(f"After balancing: { {k: len(v) for k, v in by_label.items()} }")

    flat = []
    for label, ss in by_label.items():
        for s in ss:
            flat.append((s["path"], LABEL_MAP[label]))
    random.shuffle(flat)
    return flat


def load_image(path: str) -> np.ndarray:
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    return img.astype(np.float32) / 255.0


def data_generator(samples, batch_size: int):
    while True:
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            images, labels = [], []
            for path, label in batch:
                img = load_image(path)
                if img is not None:
                    images.append(img)
                    labels.append(label)
            if images:
                yield np.array(images), np.array(labels)


def build_model(num_classes: int = 3):
    base = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(*IMG_SIZE, 3),
        pooling="avg",
    )
    base.trainable = False

    model = models.Sequential([
        base,
        layers.Dropout(0.3),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model, base


def train(
    metadata_path: str,
    output_path: str,
    epochs: int,
    batch_size: int,
    val_split: float,
    fine_tune: bool,
    balance: int = 0,
):
    print(f"Loading dataset from {metadata_path}...")
    samples = load_samples(metadata_path, balance)
    print(f"Total samples: {len(samples)}")

    # Split into train/val by index
    split_idx = int(len(samples) * (1 - val_split))
    train_samples = samples[:split_idx]
    val_samples = samples[split_idx:]
    print(f"Train: {len(train_samples)}, Val: {len(val_samples)}")

    # Compute class weights from train labels
    train_labels = [label for _, label in train_samples]
    unique, counts = np.unique(train_labels, return_counts=True)
    class_weight_dict = {c: len(train_samples) / (len(unique) * cnt) for c, cnt in zip(unique, counts)}
    print(f"Class distribution: {dict(zip(unique, counts))}")
    print(f"Class weights: {class_weight_dict}")

    model, base = build_model()
    print(model.summary())

    train_gen = data_generator(train_samples, batch_size)
    val_gen = data_generator(val_samples, batch_size)
    steps_per_epoch = max(1, len(train_samples) // batch_size)
    validation_steps = max(1, len(val_samples) // batch_size)

    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, monitor="val_accuracy"),
        ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-6, monitor="val_loss"),
        ModelCheckpoint(
            output_path.replace(".h5", "_best.h5"),
            save_best_only=True,
            monitor="val_accuracy",
        ),
    ]

    print("\n--- Phase 1: Train top layers ---")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        epochs=epochs,
        class_weight=class_weight_dict,
        callbacks=callbacks,
        verbose=1,
    )

    if fine_tune:
        print("\n--- Phase 2: Fine-tune entire model ---")
        base.trainable = True
        for layer in base.layers[:100]:
            layer.trainable = False

        model.compile(
            optimizer=optimizers.Adam(learning_rate=1e-5),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        history = model.fit(
            train_gen,
            validation_data=val_gen,
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            epochs=epochs // 2,
            class_weight=class_weight_dict,
            callbacks=callbacks,
            verbose=1,
        )

    # Save final model
    final_path = output_path.replace(".h5", "_best.h5") if os.path.exists(output_path.replace(".h5", "_best.h5")) else output_path
    print(f"\nBest model saved to {final_path}")

    # Evaluate on validation set
    val_loss, val_acc = model.evaluate(val_gen, steps=validation_steps, verbose=0)
    print(f"Validation accuracy: {val_acc:.4f} ({val_acc * 100:.1f}%)")
    print(f"Validation loss: {val_loss:.4f}")

    # Convert to SavedModel for inference
    savedmodel_dir = final_path.replace(".h5", "")
    print(f"\nConverting to SavedModel at {savedmodel_dir}...")
    import shutil
    if os.path.exists(savedmodel_dir):
        shutil.rmtree(savedmodel_dir)
    model.save(savedmodel_dir)
    print(f"SavedModel saved to {savedmodel_dir}")

    # Plot training history
    plot_dir = os.path.join(os.path.dirname(final_path), "training_plots")
    os.makedirs(plot_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    if "accuracy" in history.history:
        ax1.plot(history.history["accuracy"], label="Train")
        ax1.plot(history.history["val_accuracy"], label="Val")
        ax1.set_title("Accuracy")
        ax1.set_xlabel("Epoch")
        ax1.legend()
    ax2.plot(history.history["loss"], label="Train")
    ax2.plot(history.history["val_loss"], label="Val")
    ax2.set_title("Loss")
    ax2.set_xlabel("Epoch")
    ax2.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "history.png"))
    plt.close()
    print(f"Training plots saved to {plot_dir}/history.png")

    # Confusion matrix (load a subset of val for prediction)
    val_images, val_labels = [], []
    for path, label in val_samples[:2000]:
        img = load_image(path)
        if img is not None:
            val_images.append(img)
            val_labels.append(label)
    if val_images:
        val_images = np.array(val_images)
        val_labels = np.array(val_labels)
        y_pred = np.argmax(model.predict(val_images, verbose=0, batch_size=batch_size), axis=1)
        cm = confusion_matrix(val_labels, y_pred)
        LABELS_LIST = ["Pinkish", "Brownish", "Dark"]
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS_LIST)
        fig, ax = plt.subplots(figsize=(6, 5))
        disp.plot(ax=ax, cmap="Blues", values_format="d")
        ax.set_title("Confusion Matrix (Validation)")
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, "confusion_matrix.png"))
        plt.close()
        print(f"Confusion matrix saved to {plot_dir}/confusion_matrix.png")
        print(f"\nConfusion Matrix:\n{LABELS_LIST}")
        print(cm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="./data/processed/metadata.pkl")
    parser.add_argument("--output", default="app/models/mobilenetv2_lip.h5")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--val-split", type=float, default=0.15)
    parser.add_argument("--fine-tune", action="store_true", default=True, help="Enable fine-tuning phase")
    parser.add_argument("--balance", type=int, default=5000, help="Max samples per class (0=unlimited)")
    args = parser.parse_args()
    train(args.data, args.output, args.epochs, args.batch_size, args.val_split, args.fine_tune)
