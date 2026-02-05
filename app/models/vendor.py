from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from .base import TimestampMixin


class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(255))
    city_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    area_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("areas.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    city: Mapped["City"] = relationship("City", back_populates="vendors")
    area: Mapped["Area"] = relationship("Area", back_populates="vendors")

    vendor_types: Mapped[list["VendorType"]] = relationship(
        "VendorType",
        secondary="vendor_vendor_types",
        back_populates="vendors",
    )
    materials: Mapped[list["Material"]] = relationship(
        "Material",
        secondary="vendor_materials",
        back_populates="vendors",
    )
    brands: Mapped[list["Brand"]] = relationship(
        "Brand",
        secondary="vendor_brands",
        back_populates="vendors",
    )
    target_groups: Mapped[list["TargetGroup"]] = relationship(
        "TargetGroup",
        secondary="vendor_target_groups",
        back_populates="vendors",
    )

