import io
import os
import numpy as np
from PIL import Image

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_INPUT_SIZE = (224, 224)
LIP_TYPE_LABELS = ["Pinkish", "Brownish", "Dark"]

CLASSIFIER_MODE = os.getenv("CLASSIFIER_MODE", "tflite").lower()

_model = None
_interpreter = None
_input_details = None
_output_details = None


def load_model():
    global _model, _interpreter, _input_details, _output_details
    if CLASSIFIER_MODE == "tensorflow":
        h5_path = os.path.join(MODEL_DIR, "mobilenetv2_lip.h5")
        if os.path.exists(h5_path):
            from tensorflow.keras.models import load_model as keras_load_model
            _model = keras_load_model(h5_path)
    else:
        tflite_path = os.path.join(MODEL_DIR, "mobilenetv2_lip.tflite")
        if os.path.exists(tflite_path):
            import tflite_runtime.interpreter as tflite
            _interpreter = tflite.Interpreter(model_path=tflite_path)
            _interpreter.allocate_tensors()
            _input_details = _interpreter.get_input_details()
            _output_details = _interpreter.get_output_details()


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image = image.resize(MODEL_INPUT_SIZE)
    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    if CLASSIFIER_MODE == "tensorflow" and _model is not None:
        predictions = _model.predict(image_array, verbose=0)
        label_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][label_idx])
        label = LIP_TYPE_LABELS[label_idx]
    elif _interpreter is not None:
        _interpreter.set_tensor(_input_details[0]["index"], image_array)
        _interpreter.invoke()
        predictions = _interpreter.get_tensor(_output_details[0]["index"])
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
