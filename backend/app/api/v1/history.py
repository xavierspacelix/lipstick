from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, AnalysisSummary, LipRGB, Recommendation

router = APIRouter()


@router.get("/history", response_model=list[AnalysisSummary])
async def list_history(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    return [
        AnalysisSummary(
            id=a.id,
            lip_type=a.lip_type,
            confidence=a.confidence,
            top_recommendation=(
                a.recommendations[0]["shade_name"] if a.recommendations else None
            ),
            created_at=a.created_at,
        )
        for a in analyses
    ]


@router.get("/history/{analysis_id}", response_model=AnalysisResponse)
async def get_history_detail(
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
        rgb=LipRGB(r=analysis.rgb_r, g=analysis.rgb_g, b=analysis.rgb_b),
        lip_type=analysis.lip_type,
        confidence=analysis.confidence,
        recommendations=[Recommendation(**r) for r in analysis.recommendations],
        status=analysis.status,
        created_at=analysis.created_at,
    )


@router.delete("/history/{analysis_id}")
async def delete_history(
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

    db.delete(analysis)
    db.commit()
    return {"message": "Analysis deleted"}
