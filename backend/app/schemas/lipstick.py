from pydantic import BaseModel

from app.schemas.analysis import LipRGB


class LipstickResponse(BaseModel):
    id: str
    shade_name: str
    category: str
    rgb: LipRGB
    lip_type_tag: str
