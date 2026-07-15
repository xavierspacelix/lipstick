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
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tqdm import tqdm


IMG_SIZE = (224, 224)
LABEL_MAP = {"Pinkish": 0, "Brownish": 1, "Dark": 2}
INPUT_SIZES = {"mobilenetv2": 224, "inceptionv3": 299, "resnet50": 224}


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


def augment_image(img: np.ndarray) -> np.ndarray:
    img = img.copy()
    brightness = random.uniform(0.7, 1.3)
    img = np.clip(img * brightness, 0, 1)
    if random.random() > 0.5:
        hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
        hsv[:, :, 0] = (hsv[:, :, 0].astype(int) + random.randint(-10, 10)) % 180
        img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255.0
    if random.random() > 0.5:
        h, w = img.shape[:2]
        scale = random.uniform(0.9, 1.1)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), random.uniform(-5, 5), scale)
        img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    return img


def data_generator(samples, batch_size: int, class_weights: dict = None, augment: bool = False):
    """Yield batches. If class_weights given, oversample minority classes."""
    while True:
        if class_weights:
            batch = random.choices(samples, weights=[class_weights.get(l, 1.0) for _, l in samples], k=batch_size)
        else:
            batch = random.sample(samples, min(batch_size, len(samples)))
        images, labels = [], []
        for path, label in batch:
            img = load_image(path)
            if img is not None:
                if augment:
                    img = augment_image(img)
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
    img_size: int = 224,
):
    global IMG_SIZE
    IMG_SIZE = (img_size, img_size)
    print(f"Loading dataset from {metadata_path}...")
    samples = load_samples(metadata_path, balance)
    print(f"Total samples: {len(samples)}")

    # Split into train/val by index
    split_idx = int(len(samples) * (1 - val_split))
    train_samples = samples[:split_idx]
    val_samples = samples[split_idx:]
    print(f"Train: {len(train_samples)}, Val: {len(val_samples)}")

    # Compute class weights from train labels (for oversampling)
    train_labels = [label for _, label in train_samples]
    unique, counts = np.unique(train_labels, return_counts=True)
    # Higher weight = more samples drawn for that class
    max_count = float(max(counts))
    oversample_weights = {c: max_count / cnt for c, cnt in zip(unique, counts)}
    print(f"Class distribution: {dict(zip(unique, counts))}")
    print(f"Oversample weights: {oversample_weights}")

    model, base = build_model()
    print(model.summary())

    train_gen = data_generator(train_samples, batch_size, class_weights=oversample_weights, augment=True)
    val_gen = data_generator(val_samples, batch_size, augment=False)
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
            callbacks=callbacks,
            verbose=1,
        )

    # --- Phase 3: Pseudo-labeling (self-training) ---
    print("\n--- Phase 3: Pseudo-labeling ---")
    print("Predicting on training set to find high-confidence samples...")
    pseudo_samples = []
    for i in range(0, len(train_samples), batch_size):
        batch_paths = train_samples[i:i + batch_size]
        images = []
        for path, _ in batch_paths:
            img = load_image(path)
            if img is not None:
                images.append(img)
        if not images:
            continue
        images = np.array(images)
        preds = model.predict(images, verbose=0)
        max_probs = np.max(preds, axis=1)
        pred_labels = np.argmax(preds, axis=1)
        for j, (path, _) in enumerate(batch_paths):
            if max_probs[j] >= 0.9:
                pseudo_samples.append((path, int(pred_labels[j])))

    print(f"Found {len(pseudo_samples)} high-confidence pseudo-labels (threshold=0.9)")
    if len(pseudo_samples) > len(train_samples) * 0.3:
        pseudo_steps = max(1, len(pseudo_samples) // (batch_size // 2))
        pseudo_gen = data_generator(pseudo_samples, batch_size // 2, augment=True)
        model.compile(
            optimizer=optimizers.Adam(learning_rate=5e-6),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        history = model.fit(
            pseudo_gen,
            validation_data=val_gen,
            steps_per_epoch=pseudo_steps,
            validation_steps=validation_steps,
            epochs=5,
            callbacks=[EarlyStopping(patience=3, restore_best_weights=True, monitor="val_accuracy")],
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
    import shutil
    if os.path.exists(savedmodel_dir):
        shutil.rmtree(savedmodel_dir)
    model.export(savedmodel_dir)
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

    # Free some memory before confusion matrix
    import gc
    del train_gen, val_gen
    gc.collect()

    # Confusion matrix (small subset to avoid OOM)
    val_images, val_labels = [], []
    for path, label in val_samples[:50]:
        img = load_image(path)
        if img is not None:
            val_images.append(img)
            val_labels.append(label)
    if val_images:
        val_images = np.array(val_images)
        val_labels = np.array(val_labels)
        # Predict in small batches to save memory
        y_pred = []
        for i in range(0, len(val_images), 16):
            batch = val_images[i:i+16]
            preds = model.predict(batch, verbose=0)
            y_pred.extend(np.argmax(preds, axis=1))
        y_pred = np.array(y_pred)
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

        # Classification report
        report = classification_report(val_labels, y_pred, target_names=LABELS_LIST, digits=4)
        print("\nClassification Report:")
        print(report)

        # Save report as TXT
        with open(os.path.join(plot_dir, "classification_report.txt"), "w") as f:
            f.write(report)
        print(f"Classification report saved to {plot_dir}/classification_report.txt")

        # Save report as PNG table (with error handling)
        try:
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.axis("off")
            cell_text = []
            rows = []
            for line in report.split("\n"):
                stripped = line.strip()
                if not stripped:
                    continue
                parts = stripped.split()
                if len(parts) < 4:
                    continue
                if parts[0] in LABELS_LIST:
                    rows.append(parts[0])
                    cell_text.append(parts[1:5])
                elif parts[0] == "accuracy":
                    rows.append("accuracy")
                    cell_text.append(["-", "-"] + parts[1:3])
            col_labels = ["precision", "recall", "f1-score", "support"]
            table = ax.table(cellText=cell_text, rowLabels=rows, colLabels=col_labels, loc="center")
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            plt.tight_layout()
            plt.savefig(os.path.join(plot_dir, "classification_report.png"), dpi=200, bbox_inches="tight")
            plt.close()
            print(f"Classification report saved to {plot_dir}/classification_report.png")
        except Exception as e:
            print(f"Warning: Could not save classification report PNG: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="./data/processed/metadata.pkl")
    parser.add_argument("--output", default="app/models/mobilenetv2_lip.h5")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--val-split", type=float, default=0.15)
    parser.add_argument("--fine-tune", action="store_true", default=True, help="Enable fine-tuning phase")
    parser.add_argument("--balance", type=int, default=5000, help="Max samples per class (0=unlimited)")
    parser.add_argument("--img-size", type=int, default=224, choices=[224, 299], help="Input image size (224=MobileNetV2, 299=InceptionV3)")
    args = parser.parse_args()
    train(args.data, args.output, args.epochs, args.batch_size, args.val_split, args.fine_tune, args.balance, args.img_size)
