"""Rebuild model architecture and load weights from training .h5.

Usage:
    python scripts/rebuild_model.py
"""
import os
import shutil

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import h5py
import numpy as np
import tensorflow as tf

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "models")
H5_PATH = os.path.join(MODEL_DIR, "mobilenetv2_lip_best.h5")
OUTPUT_DIR = os.path.join(MODEL_DIR, "mobilenetv2_lip")

print("[rebuild] building model architecture...", flush=True)
base = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet",
    pooling="avg",
)
model = tf.keras.Sequential([
    base,
    tf.keras.layers.Dropout(0.3, name="dropout"),
    tf.keras.layers.Dense(128, activation="relu", name="dense"),
    tf.keras.layers.Dropout(0.2, name="dropout_1"),
    tf.keras.layers.Dense(3, activation="softmax", name="dense_1"),
], name="sequential")
model(tf.zeros((1, 224, 224, 3)))
total = model.count_params()
print(f"[rebuild] built model: {total} params", flush=True)

print("[rebuild] loading weights from h5...", flush=True)
matched = 0
total_vars = 0
with h5py.File(H5_PATH, "r") as f:
    h5_weights = f["model_weights"]

    for layer_name in h5_weights:
        if layer_name.startswith("_"):
            continue

        try:
            layer = model.get_layer(layer_name)
        except ValueError:
            print(f"  skip  {layer_name}: not in model", flush=True)
            continue

        grp = h5_weights[layer_name]
        raw_names = grp.attrs.get("weight_names", [])
        h5_w_names = [n.decode() if isinstance(n, bytes) else n for n in raw_names]

        h5_w_dict = {}
        for wn in h5_w_names:
            h5_w_dict[wn] = np.array(grp[wn])
            # Index without "sequential/" prefix (from Sequential wrapper)
            if wn.startswith("sequential/"):
                h5_w_dict[wn[len("sequential/"):]] = h5_w_dict[wn]

        layer_vars = layer.weights
        total_vars += len(layer_vars)
        new_weights = []
        for var in layer_vars:
            key = var.name.rstrip(":0")
            if key in h5_w_dict:
                new_weights.append(h5_w_dict[key])
                matched += 1
            elif key.endswith("/depthwise_kernel") and key.replace("/depthwise_kernel", "/kernel") in h5_w_dict:
                alt = key.replace("/depthwise_kernel", "/kernel")
                new_weights.append(h5_w_dict[alt])
                matched += 1
            else:
                print(f"  MISS  {key}", flush=True)

        if new_weights:
            layer.set_weights(new_weights)

print(f"[rebuild] weights loaded: {matched}/{total_vars} vars matched", flush=True)

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
model.save(OUTPUT_DIR)
print(f"[rebuild] saved SavedModel to {OUTPUT_DIR}", flush=True)
