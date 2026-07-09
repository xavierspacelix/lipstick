"""Rebuild model architecture manually and load weights from .h5.

Usage:
    python scripts/rebuild_model.py
"""
import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "models")
H5_PATH = os.path.join(MODEL_DIR, "mobilenetv2_lip.h5")
OUTPUT_DIR = os.path.join(MODEL_DIR, "mobilenetv2_lip")

print("[rebuild] creating model architecture...", flush=True)

# Rebuild the same architecture as the saved model
base = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights=None,
    pooling="avg"
)

model = tf.keras.Sequential([
    base,
    tf.keras.layers.Dropout(0.3, name="dropout"),
    tf.keras.layers.Dense(128, activation="relu", name="dense"),
    tf.keras.layers.Dropout(0.2, name="dropout_1"),
    tf.keras.layers.Dense(3, activation="softmax", name="dense_1"),
], name="sequential")

# Build by calling on dummy input so all weight shapes are known
model(tf.zeros((1, 224, 224, 3)))
print(f"[rebuild] built model: {model.count_params()} params", flush=True)

print("[rebuild] loading weights...", flush=True)
model.load_weights(H5_PATH)
print("[rebuild] weights loaded successfully", flush=True)

# Save as SavedModel
import shutil
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
model.save(OUTPUT_DIR)
print(f"[rebuild] saved to {OUTPUT_DIR}", flush=True)
