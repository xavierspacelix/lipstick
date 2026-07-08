import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    original_image_url: Mapped[str] = mapped_column(Text, nullable=False)
    cropped_lip_image_url: Mapped[str] = mapped_column(Text, nullable=False)
    brushed_lip_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rgb_r: Mapped[int] = mapped_column(Integer, nullable=False)
    rgb_g: Mapped[int] = mapped_column(Integer, nullable=False)
    rgb_b: Mapped[int] = mapped_column(Integer, nullable=False)
    lip_type: Mapped[str] = mapped_column(String(20), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    recommendations: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="completed")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
