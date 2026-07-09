import io
import os
import numpy as np
from PIL import Image

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_INPUT_SIZE = (224, 224)
LIP_TYPE_LABELS = ["Pinkish", "Brownish", "Dark"]

_model = None


def load_model():
    global _model

    # 1) Try pre-converted SavedModel (TF2 native format)
    savedmodel_path = os.path.join(MODEL_DIR, "mobilenetv2_lip")
    if os.path.isdir(savedmodel_path):
        try:
            import tensorflow as tf
            _model = tf.saved_model.load(savedmodel_path)
            _model = _model.signatures["serving_default"]
            print("[classifier] TF SavedModel loaded", flush=True)
            return
        except Exception as e:
            print(f"[classifier] SavedModel load failed: {e}", flush=True)

    # 2) Try .h5 (Keras 2 format) with safe_mode=False
    h5_path = os.path.join(MODEL_DIR, "mobilenetv2_lip.h5")
    if os.path.exists(h5_path):
        try:
            from tensorflow.keras.models import load_model as keras_load_model
            _model = keras_load_model(h5_path, compile=False, safe_mode=False)
            print("[classifier] .h5 model loaded (safe_mode=False)", flush=True)
            return
        except Exception as e:
            print(f"[classifier] .h5 load failed: {e}", flush=True)

    # 3) Try .h5 with Keras 3 compat monkey-patch (fixes nested tuple shapes)
    if os.path.exists(h5_path):
        try:
            import keras.src.backend.common.variables as variables

            _orig = variables.standardize_shape

            def _patch(shape):
                if isinstance(shape, (tuple, list)) and len(shape) == 2 and isinstance(shape[0], (tuple, list)):
                    return _orig(shape[0])
                return _orig(shape)

            variables.standardize_shape = _patch

            from tensorflow.keras.models import load_model as keras_load_model2
            _model = keras_load_model2(h5_path, compile=False, safe_mode=False)
            print("[classifier] .h5 model loaded (patched)", flush=True)
            return
        except Exception as e:
            print(f"[classifier] .h5 patched load failed: {e}", flush=True)

    print("[classifier] no model loaded, using rule-based fallback", flush=True)


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image = image.resize(MODEL_INPUT_SIZE)
    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    if _model is not None:
        if hasattr(_model, "predict"):
            predictions = _model.predict(image_array, verbose=0)
        else:
            import tensorflow as tf
            inp = tf.constant(image_array)
            out = _model(inp)
            predictions = list(out.values())[0].numpy() if isinstance(out, dict) else out.numpy()
        label_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][label_idx])
        label = LIP_TYPE_LABELS[label_idx]
    else:
        rgb = np.mean(image_array)
        if rgb < 0.3:
            label = "Dark"
        elif rgb < 0.5:
            label = "Brownish"
        else:
            label = "Pinkish"
        confidence = 0.85

    return {"label": label, "confidence": confidence}
