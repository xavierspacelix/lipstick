from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.pipeline.face_detection import detect_face
from app.pipeline.lip_segmentation import apply_tryon, segment_lips
from app.pipeline.rgb_extraction import extract_rgb
from app.pipeline.classifier import classify_lip_type
from app.pipeline.recommender import get_top3


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Lipstick AI Service", lifespan=lifespan)


@app.post("/pipeline/analyze")
async def analyze(image: UploadFile = File(...)):
    image_bytes = await image.read()

    face_result = detect_face(image_bytes)
    if not face_result["face_detected"]:
        return {"face_detected": False}

    lip_result = segment_lips(image_bytes, face_result["landmarks"])
    if not lip_result["success"]:
        raise HTTPException(status_code=422, detail="Lip segmentation failed")

    rgb = extract_rgb(lip_result["cropped_lip"])

    classification = classify_lip_type(lip_result["cropped_lip"])

    recommendations = get_top3(classification["label"], (rgb["r"], rgb["g"], rgb["b"]))

    # Generate try-on with top recommendation color
    print("[pipeline] generating try-on...", flush=True)
    try:
        top_rgb = recommendations[0]["rgb"]
        brushed_lip = apply_tryon(
            lip_result["cropped_lip"],
            lip_result["mask"],
            top_rgb["r"],
            top_rgb["g"],
            top_rgb["b"],
        )
        print(f"[pipeline] try-on generated, size={len(brushed_lip)}", flush=True)
    except Exception as e:
        print(f"[pipeline] try-on failed: {e}", flush=True)
        brushed_lip = None

    result = {
        "face_detected": True,
        "cropped_lip": lip_result["cropped_lip"],
        "rgb": rgb,
        "lip_type": classification["label"],
        "confidence": classification["confidence"],
        "recommendations": recommendations,
    }

    if brushed_lip is not None:
        result["brushed_lip"] = brushed_lip

    return result
