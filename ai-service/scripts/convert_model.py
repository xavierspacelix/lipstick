"""Inspect & convert Keras 2 .h5 model for Keras 3 compatibility.

Usage:
    python scripts/convert_model.py inspect <input.h5>          # dump model config
    python scripts/convert_model.py convert <input.h5> <output_dir>  # convert to SavedModel
"""
import json
import os
import sys

import h5py
import numpy as np


def cmd_inspect(input_path):
    print(f"[inspect] reading {input_path} ...", flush=True)
    with h5py.File(input_path, "r") as f:
        raw_config = json.loads(f.attrs["model_config"])
        print(json.dumps(raw_config, indent=2), flush=True)

        print("\n[inspect] weight groups:", flush=True)
        weight_group = f.get("model_weights")
        if weight_group:
            for layer_name in weight_group:
                g = weight_group[layer_name]
                w_names = g.attrs.get("weight_names", [])
                for wn in w_names:
                    wn = wn.decode() if isinstance(wn, bytes) else wn
                    data = np.array(g[wn])
                    print(f"  {layer_name}/{wn}: {data.shape}", flush=True)


def cmd_convert(input_path, output_path):
    print(f"[convert] reading config from {input_path} ...", flush=True)
    with h5py.File(input_path, "r") as f:
        raw_config = json.loads(f.attrs["model_config"])

    # Walk config and fix shape-related fields
    SHAPE_KEYS = {
        "batch_shape", "batch_input_shape", "batch_output_shape",
        "target_shape", "input_shape", "output_shape",
    }

    def fix_node(node):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                v = fix_node(v)
                if k in SHAPE_KEYS and isinstance(v, (list, tuple)):
                    # Flatten nested tuples: [[null, 1280], 128] → [null, 1280]
                    while len(v) == 2 and isinstance(v[0], (list, tuple)):
                        v = v[0]
                out[k] = v
            return out
        elif isinstance(node, list):
            return [fix_node(item) for item in node]
        return node

    fixed_config = fix_node(raw_config)
    print("[convert] config fixed", flush=True)

    import keras
    from keras.src.legacy.saving import serialization

    import keras.src.backend.common.variables as variables
    _orig = variables.standardize_shape

    def _patched(shape):
        if isinstance(shape, (tuple, list)) and len(shape) == 2 and isinstance(shape[0], (tuple, list)):
            shape = shape[0]
        return _orig(shape)

    variables.standardize_shape = _patched

    try:
        model = serialization.deserialize_keras_object(fixed_config)
    except Exception as e:
        print(f"[convert] config-based rebuild failed: {e}", flush=True)
        # Fallback: try loading via legacy h5 format with monkey-patches
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        from tensorflow.keras.models import load_model
        model = load_model(input_path, compile=False, safe_mode=False)

    print(f"[convert] model loaded: {model.count_params()} params", flush=True)

    if os.path.exists(output_path):
        import shutil
        shutil.rmtree(output_path)

    model.save(output_path)
    print(f"[convert] saved to {output_path}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "inspect":
        cmd_inspect(sys.argv[2])
    elif cmd == "convert":
        cmd_convert(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
