"""Rebuild model architecture manually and load weights from .h5.

Usage:
    python scripts/rebuild_model.py
"""
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import h5py
import numpy as np
import tensorflow as tf

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "models")
H5_PATH = os.path.join(MODEL_DIR, "mobilenetv2_lip.h5")
OUTPUT_DIR = os.path.join(MODEL_DIR, "mobilenetv2_lip")

print("[rebuild] creating model architecture...", flush=True)

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

model(tf.zeros((1, 224, 224, 3)))
print(f"[rebuild] built model: {model.count_params()} params", flush=True)

# Load weights matching by variable name (not by position)
print("[rebuild] loading weights...", flush=True)
with h5py.File(H5_PATH, "r") as f:
    h5_weights = f["model_weights"]

    for layer_name in h5_weights:
        if layer_name.startswith("_"):
            continue

        try:
            layer = model.get_layer(layer_name)
        except ValueError:
            print(f"  skipping unknown layer '{layer_name}'", flush=True)
            continue

        grp = h5_weights[layer_name]
        raw_names = grp.attrs.get("weight_names", [])
        h5_w_names = [n.decode() if isinstance(n, bytes) else n for n in raw_names]

        # Build a dict: h5 weight name → numpy array
        h5_w_dict = {}
        for wn in h5_w_names:
            dataset = grp[wn]
            h5_w_dict[wn] = np.array(dataset)

        # Get layer weights — they come as list-of-variables
        layer_vars = layer.weights
        new_weights = []
        for var in layer_vars:
            var_name = var.name
            # Match: var name like "mobilenetv2_1.00_224/Conv1/kernel:0"
            # H5 name like "Conv1/kernel:0"
            # Strip the layer prefix from var_name
            short_name = var_name.split("/", 1)[1] if "/" in var_name else var_name
            if short_name in h5_w_dict:
                new_weights.append(h5_w_dict[short_name])
                print(f"  ✓ {layer_name}/{short_name}: {h5_w_dict[short_name].shape}", flush=True)
            else:
                print(f"  ✗ {layer_name}/{short_name} not found in h5", flush=True)

        if new_weights:
            layer.set_weights(new_weights)

print("[rebuild] all weights loaded", flush=True)

import shutil
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
model.save(OUTPUT_DIR)
print(f"[rebuild] saved to {OUTPUT_DIR}", flush=True)
