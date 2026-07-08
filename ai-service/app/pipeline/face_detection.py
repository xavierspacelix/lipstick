import io

import mediapipe as mp
import numpy as np
from PIL import Image

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)


def detect_face(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)
    rgb_image = image_array[:, :, :3]

    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        return {"face_detected": False}

    landmarks = results.multi_face_landmarks[0]
    return {"face_detected": True, "landmarks": landmarks}
