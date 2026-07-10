import io
import numpy as np
from PIL import Image


def load_model():
    pass


def classify_lip_type(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image_array = np.array(image, dtype=np.float32) / 255.0

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
