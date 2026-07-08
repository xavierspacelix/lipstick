from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.lipstick import Lipstick
from app.schemas.lipstick import LipstickResponse
from app.schemas.analysis import LipRGB

router = APIRouter()


@router.get("/lipsticks", response_model=list[LipstickResponse])
async def list_lipsticks(
    lip_type: Optional[str] = Query(None, description="Filter by lip type tag"),
    category: Optional[str] = Query(None, description="Filter by category"),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Lipstick)
    if lip_type:
        query = query.filter(Lipstick.lip_type_tag == lip_type)
    if category:
        query = query.filter(Lipstick.category == category)
    lipsticks = query.order_by(Lipstick.category, Lipstick.shade_name).all()
    return [
        LipstickResponse(
            id=l.id,
            shade_name=l.shade_name,
            category=l.category,
            rgb=LipRGB(r=l.rgb_r, g=l.rgb_g, b=l.rgb_b),
            lip_type_tag=l.lip_type_tag,
        )
        for l in lipsticks
    ]
