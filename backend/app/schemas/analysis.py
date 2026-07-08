from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LipRGB(BaseModel):
    r: int
    g: int
    b: int


class Recommendation(BaseModel):
    shade_name: str
    category: str
    score: float
    rgb: LipRGB


class AnalysisResponse(BaseModel):
    id: str
    user_id: str
    original_image_url: str
    cropped_lip_image_url: str
    brushed_lip_image_url: Optional[str] = None
    rgb: LipRGB
    lip_type: str
    confidence: float
    recommendations: list[Recommendation]
    status: str
    created_at: datetime


class AnalysisSummary(BaseModel):
    id: str
    lip_type: str
    confidence: float
    top_recommendation: Optional[str]
    created_at: datetime
