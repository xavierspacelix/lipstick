import uuid
from collections import Counter
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, LipRGB, Recommendation
from app.services.recommendation_service import get_top3
from app.services.storage_service import upload_file


class AnalysisError(Exception):
    pass


async def _process_one(client: httpx.AsyncClient, image_bytes: bytes, filename: str) -> dict:
    try:
        response = await client.post(
            f"{settings.ai_service_url}/pipeline/analyze",
            files={"image": (filename, image_bytes, "image/jpeg")},
        )
        response.raise_for_status()
        result = response.json()
        print(f"[analysis_service] ai-response keys: {list(result.keys())}", flush=True)
    except httpx.RequestError as e:
        raise AnalysisError(f"AI service unavailable: {str(e)}")
    if result.get("face_detected") is False:
        raise AnalysisError("No face detected in one of the photos — try a clearer, front-facing photo")
    return result


async def run_analysis(
    db: Session, user_id: str, images: list[tuple[bytes, str]]
) -> AnalysisResponse:
    analysis_id = str(uuid.uuid4())

    if not images:
        raise AnalysisError("At least one image is required")

    # Upload first original image
    first_bytes, first_filename = images[0]
    original_key = f"{user_id}/{analysis_id}.jpg"
    original_url = await upload_file(
        bucket="original-images",
        path=original_key,
        data=first_bytes,
    )

    # Process all images through AI service
    async with httpx.AsyncClient(timeout=10) as client:
        results = []
        for i, (img_bytes, filename) in enumerate(images):
            result = await _process_one(client, img_bytes, filename)
            results.append(result)

    # Use first result for cropped/brushed images
    first_result = results[0]
    cropped_lip_bytes = first_result.get("cropped_lip")
    if cropped_lip_bytes:
        cropped_lip_data = bytes(cropped_lip_bytes) if isinstance(cropped_lip_bytes, list) else cropped_lip_bytes.encode()
    else:
        cropped_lip_data = first_bytes
    cropped_key = f"{user_id}/{analysis_id}.jpg"
    cropped_url = await upload_file(bucket="cropped-lips", path=cropped_key, data=cropped_lip_data)

    brushed_url = None
    brushed_data = first_result.get("brushed_lip")
    if brushed_data:
        brushed_bytes = bytes(brushed_data) if isinstance(brushed_data, list) else brushed_data.encode()
        brushed_url = await upload_file(bucket="brushed-lips", path=f"{user_id}/{analysis_id}.jpg", data=brushed_bytes)

    # Average RGB
    avg_r = sum(r["rgb"]["r"] for r in results) // len(results)
    avg_g = sum(r["rgb"]["g"] for r in results) // len(results)
    avg_b = sum(r["rgb"]["b"] for r in results) // len(results)

    # Vote lip type (majority), fallback to first if tie
    type_counts = Counter(r["lip_type"] for r in results)
    lip_type = type_counts.most_common(1)[0][0]

    # Average confidence
    avg_confidence = round(sum(r["confidence"] for r in results) / len(results), 3)

    # Run recommendation on averaged RGB
    recommendations_data = get_top3(lip_type, (avg_r, avg_g, avg_b))

    analysis = Analysis(
        id=analysis_id,
        user_id=user_id,
        original_image_url=original_url,
        cropped_lip_image_url=cropped_url,
        brushed_lip_image_url=brushed_url,
        rgb_r=avg_r,
        rgb_g=avg_g,
        rgb_b=avg_b,
        lip_type=lip_type,
        confidence=avg_confidence,
        recommendations=recommendations_data,
        status="completed",
        created_at=datetime.now(timezone.utc),
    )
    db.add(analysis)
    db.flush()

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.total_analyses = db.query(Analysis).filter(Analysis.user_id == user_id).count()

    db.commit()
    db.refresh(analysis)

    return AnalysisResponse(
        id=analysis.id,
        user_id=analysis.user_id,
        original_image_url=analysis.original_image_url,
        cropped_lip_image_url=analysis.cropped_lip_image_url,
        brushed_lip_image_url=analysis.brushed_lip_image_url,
        rgb=LipRGB(r=analysis.rgb_r, g=analysis.rgb_g, b=analysis.rgb_b),
        lip_type=analysis.lip_type,
        confidence=analysis.confidence,
        recommendations=[Recommendation(**r) for r in analysis.recommendations],
        status=analysis.status,
        created_at=analysis.created_at,
    )
