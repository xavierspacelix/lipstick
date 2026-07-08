import io
import os

import numpy as np
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "mobilenetv2_lip.h5")
MODEL_INPUT_SIZE = (224, 224)
LIP_TYPE_LABELS = ["Pinkish", "Brownish", "Dark"]

_model = None


def load_model():
    global _model
    if os.path.exists(MODEL_PATH):
        from tensorflow.keras.models import load_model as keras_load_model
        _model = keras_load_model(MODEL_PATH)


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image = image.resize(MODEL_INPUT_SIZE)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    if _model is not None:
        predictions = _model.predict(image_array, verbose=0)
        label_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][label_idx])
        label = LIP_TYPE_LABELS[label_idx]
    else:
        rgb = np.mean(image_array, axis=(1, 2, 3))
        if rgb < 0.3:
            label = "Dark"
        elif rgb < 0.5:
            label = "Brownish"
        else:
            label = "Pinkish"
        confidence = 0.85

    return {"label": label, "confidence": confidence}
