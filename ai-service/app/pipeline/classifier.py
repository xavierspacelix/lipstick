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

    savedmodel_path = os.path.join(MODEL_DIR, "mobilenetv2_lip")
    if os.path.isdir(savedmodel_path):
        try:
            import tensorflow as tf
            reloaded = tf.saved_model.load(savedmodel_path)
            _model = reloaded.signatures["serving_default"]
            print("[classifier] TF SavedModel loaded", flush=True)
            return
        except Exception as e:
            print(f"[classifier] SavedModel load failed: {e}", flush=True)

    print("[classifier] no model loaded, using rule-based fallback", flush=True)


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image = image.resize(MODEL_INPUT_SIZE)
    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    if _model is not None:
        import tensorflow as tf
        inp = tf.constant(image_array, dtype=tf.float32)
        out = _model(inp)
        predictions = list(out.values())[0].numpy()
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
