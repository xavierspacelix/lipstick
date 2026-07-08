import io

import numpy as np
from PIL import Image, ImageDraw


def segment_lips(image_bytes: bytes, landmarks) -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)
    h, w = image_array.shape[:2]

    lip_indices = [
        61, 146, 91, 181, 84, 17, 314, 405, 321, 375,
        291, 409, 270, 269, 267, 0, 37, 39, 40, 185,
    ]

    lip_points = []
    for i in lip_indices:
        x = int(landmarks.landmark[i].x * w)
        y = int(landmarks.landmark[i].y * h)
        lip_points.append([x, y])

    lip_points = np.array(lip_points)
    x_min, y_min = lip_points.min(axis=0)
    x_max, y_max = lip_points.max(axis=0)

    padding = 20
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max = min(w, x_max + padding)
    y_max = min(h, y_max + padding)

    cropped = image_array[y_min:y_max, x_min:x_max]
    cropped_h, cropped_w = cropped.shape[:2]

    # Create lip mask in cropped coordinates
    mask = Image.new("L", (cropped_w, cropped_h), 0)
    draw = ImageDraw.Draw(mask)
    adjusted = [(x - x_min, y - y_min) for x, y in lip_points]
    draw.polygon(adjusted, fill=255)
    mask_array = np.array(mask)

    # Save cropped image
    pil_image = Image.fromarray(cropped)
    buf = io.BytesIO()
    pil_image.save(buf, format="JPEG")
    cropped_bytes = buf.getvalue()

    # Save mask as PNG (lossless — preserves exact binary 0/255)
    mask_buf = io.BytesIO()
    Image.fromarray(mask_array).save(mask_buf, format="PNG")
    mask_bytes = mask_buf.getvalue()

    return {
        "success": True,
        "cropped_lip": list(cropped_bytes),
        "mask": list(mask_bytes),
        "image": pil_image,
    }


def apply_tryon(cropped_lip_bytes: list[int], mask_bytes: list[int], r: int, g: int, b: int) -> list[int]:
    cropped = Image.open(io.BytesIO(bytes(cropped_lip_bytes))).convert("RGBA")
    mask = Image.open(io.BytesIO(bytes(mask_bytes))).convert("L")

    # Soften mask edges
    from PIL import ImageFilter
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))

    # Create solid color overlay
    overlay = Image.new("RGBA", cropped.size, (r, g, b, 255))

    # Composite using mask
    composite = Image.composite(overlay, cropped, mask)

    # Convert back to RGB JPEG
    composite_rgb = composite.convert("RGB")
    buf = io.BytesIO()
    composite_rgb.save(buf, format="JPEG")
    return list(buf.getvalue())
