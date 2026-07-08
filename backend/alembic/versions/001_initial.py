"""initial

Revision ID: 001
Revises:
Create Date: 2026-07-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("total_analyses", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "analyses",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("original_image_url", sa.Text(), nullable=False),
        sa.Column("cropped_lip_image_url", sa.Text(), nullable=False),
        sa.Column("rgb_r", sa.Integer(), nullable=False),
        sa.Column("rgb_g", sa.Integer(), nullable=False),
        sa.Column("rgb_b", sa.Integer(), nullable=False),
        sa.Column("lip_type", sa.String(20), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("recommendations", JSONB(), nullable=False),
        sa.Column("status", sa.String(20), server_default="completed"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "lipsticks",
        sa.Column("id", UUID(as_uuid=False), primary_key=True),
        sa.Column("shade_name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("rgb_r", sa.Integer(), nullable=False),
        sa.Column("rgb_g", sa.Integer(), nullable=False),
        sa.Column("rgb_b", sa.Integer(), nullable=False),
        sa.Column("lip_type_tag", sa.String(20), nullable=False),
        sa.Column("metadata", JSONB(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("lipsticks")
    op.drop_table("analyses")
    op.drop_table("users")
