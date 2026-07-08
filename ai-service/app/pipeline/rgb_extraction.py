import io

import numpy as np
from PIL import Image


def extract_rgb(cropped_lip_bytes: list[int]) -> dict:
    image = Image.open(io.BytesIO(bytes(cropped_lip_bytes)))
    image_array = np.array(image)

    r = int(np.mean(image_array[:, :, 0]))
    g = int(np.mean(image_array[:, :, 1]))
    b = int(np.mean(image_array[:, :, 2]))

    return {"r": r, "g": g, "b": b}
