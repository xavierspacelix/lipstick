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
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tqdm import tqdm


IMG_SIZE = (224, 224)
LABEL_MAP = {"Pinkish": 0, "Brownish": 1, "Dark": 2}


def load_data(metadata_path: str, balance: int = 0):
    with open(metadata_path, "rb") as f:
        samples = pickle.load(f)

    # Group by label
    by_label: dict[str, list] = {}
    for s in samples:
        if s["label"] not in LABEL_MAP:
            continue
        by_label.setdefault(s["label"], []).append(s)

    print(f"Available samples per class: { {k: len(v) for k, v in by_label.items()} }")

    # Balance: take at most `balance` per class
    if balance > 0:
        for k in by_label:
            random.shuffle(by_label[k])
            by_label[k] = by_label[k][:balance]
        print(f"After balancing: { {k: len(v) for k, v in by_label.items()} }")

    images = []
    labels = []

    for label, ss in by_label.items():
        for s in tqdm(ss, desc=f"Loading {label}"):
            img = cv2.imread(s["path"])
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            img = img.astype(np.float32) / 255.0
            images.append(img)
            labels.append(LABEL_MAP[label])

    if len(images) == 0:
        print("No valid images found!")
        sys.exit(1)

    return np.array(images), np.array(labels)


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
    images, labels = load_data(metadata_path, balance)
    print(f"Loaded {len(images)} images")

    X_train, X_val, y_train, y_val = train_test_split(
        images, labels, test_size=val_split, stratify=labels, random_state=42
    )
    print(f"Train: {len(X_train)}, Val: {len(X_val)}")

    class_weights = compute_class_weight(
        "balanced", classes=np.unique(y_train), y=y_train
    )
    class_weight_dict = dict(enumerate(class_weights))
    print(f"Class weights: {class_weight_dict}")

    model, base = build_model()
    print(model.summary())

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
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
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
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs // 2,
            batch_size=batch_size,
            class_weight=class_weight_dict,
            callbacks=callbacks,
            verbose=1,
        )

    # Save final model
    final_path = output_path.replace(".h5", "_best.h5") if os.path.exists(output_path.replace(".h5", "_best.h5")) else output_path
    print(f"\nBest model saved to {final_path}")

    # Evaluate
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
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
