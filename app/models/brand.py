from __future__ import annotations

import uuid

from sqlalchemy import Boolean, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from .base import TimestampMixin


class Brand(Base, TimestampMixin):
    __tablename__ = "brands"
    __table_args__ = (UniqueConstraint("code", name="uq_brands_code"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    vendors: Mapped[list["Vendor"]] = relationship(
        "Vendor",
        secondary="vendor_brands",
        back_populates="brands",
    )
    materials: Mapped[list["Material"]] = relationship(
        "Material",
        secondary="brand_materials",
        back_populates="brands",
    )

