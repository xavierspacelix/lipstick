import io
import os

import numpy as np
from PIL import Image

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
LIP_TYPE_LABELS = ["Pinkish", "Brownish", "Dark"]

_model = None


def load_model():
    global _model
    savedmodel_path = os.path.join(MODEL_DIR, "mobilenetv2_lip")
    if os.path.isdir(savedmodel_path):
        try:
            import tensorflow as tf
            reloaded = tf.saved_model.load(savedmodel_path)
            _model = reloaded.signatures["serving_default"]
            print("[classifier] TF SavedModel loaded", flush=True)
        except Exception as e:
            print(f"[classifier] SavedModel load failed: {e}", flush=True)
    else:
        print("[classifier] no SavedModel found, using rule-based", flush=True)


def _rule_based(image_array: np.ndarray) -> dict:
    r = float(np.mean(image_array[:, :, 0]))
    g = float(np.mean(image_array[:, :, 1]))
    b = float(np.mean(image_array[:, :, 2]))
    brightness = (r + g + b) / 3.0

    if brightness < 0.3:
        label = "Dark"
        confidence = round(0.7 + brightness * 0.5, 2)
    elif r > 0.45 and g > 0.3 and b > 0.25:
        label = "Pinkish"
        confidence = round(0.7 + (r - g) * 0.5, 2)
    else:
        label = "Brownish"
        confidence = round(0.7 + (0.4 - brightness) * 0.5, 2)

    confidence = max(0.5, min(0.98, confidence))
    return {"label": label, "confidence": confidence}


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image_array = np.array(image, dtype=np.float32) / 255.0

    if _model is not None:
        try:
            import tensorflow as tf
            inp = tf.constant(image_array[np.newaxis, ...], dtype=tf.float32)
            out = _model(inp)
            predictions = list(out.values())[0].numpy()[0]
            probs = tf.nn.softmax(predictions).numpy()
            if float(np.max(probs)) > 0.85:
                label_idx = int(np.argmax(probs))
                return {
                    "label": LIP_TYPE_LABELS[label_idx],
                    "confidence": round(float(np.max(probs)), 2),
                }
        except Exception as e:
            print(f"[classifier] TF inference failed: {e}", flush=True)

    return _rule_based(image_array)
