import uuid
from typing import Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Lipstick(Base):
    __tablename__ = "lipsticks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    shade_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    rgb_r: Mapped[int] = mapped_column(Integer, nullable=False)
    rgb_g: Mapped[int] = mapped_column(Integer, nullable=False)
    rgb_b: Mapped[int] = mapped_column(Integer, nullable=False)
    lip_type_tag: Mapped[str] = mapped_column(String(20), nullable=False)
    extra_data: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, nullable=True)
