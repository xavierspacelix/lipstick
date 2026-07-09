"""Convert Keras 2 .h5 model to SavedModel for Keras 3 compatibility.

Usage:
    python scripts/convert_model.py <input.h5> <output_dir>
"""
import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import keras.src.backend.common.variables as variables

_orig = variables.standardize_shape


def _patched(shape):
    if isinstance(shape, (tuple, list)) and len(shape) == 2 and isinstance(shape[0], (tuple, list)):
        return _orig(shape[0])
    return _orig(shape)


variables.standardize_shape = _patched

from tensorflow.keras.models import load_model

input_path = sys.argv[1]
output_path = sys.argv[2]

print(f"[convert] loading {input_path} ...", flush=True)
model = load_model(input_path, compile=False, safe_mode=False)
print(f"[convert] saving to {output_path} ...", flush=True)
model.save(output_path)
print(f"[convert] done", flush=True)
