from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, LipRGB, Recommendation
from app.services.analysis_service import AnalysisError, run_analysis
from app.utils.validators import validate_image

router = APIRouter()


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == user_id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

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


@router.post("/analysis", response_model=AnalysisResponse)
async def create_analysis(
    images: list[UploadFile] = File(..., description="Up to 3 images"),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if len(images) > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 images allowed")
    if not images:
        raise HTTPException(status_code=400, detail="At least one image is required")
    try:
        for img in images:
            validate_image(img)
        image_data = [(await img.read(), img.filename or f"image_{i}.jpg") for i, img in enumerate(images)]
        result = await run_analysis(db, user_id, image_data)
        return result
    except AnalysisError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[analysis] {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
