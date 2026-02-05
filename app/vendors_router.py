from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import get_db
from app.models import Vendor
from app.schemas import VendorCreate, VendorUpdate, VendorRead


router = APIRouter(prefix="/vendors", tags=["vendors"])


def _get_vendor_or_404(
    db: Session,
    vendor_id: uuid.UUID,
) -> Vendor:
    stmt = (
        select(Vendor)
        .where(Vendor.id == vendor_id)
        .where(Vendor.deleted_at.is_(None))
    )
    vendor = db.execute(stmt).scalar_one_or_none()
    if vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    return vendor


@router.post(
    "",
    response_model=VendorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_vendor(
    payload: VendorCreate,
    db: Session = Depends(get_db),
) -> Vendor:
    vendor = Vendor(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        city_id=payload.city_id,
        area_id=payload.area_id,
        is_active=payload.is_active,
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.get(
    "",
    response_model=List[VendorRead],
)
def list_vendors(
    db: Session = Depends(get_db),
    city_id: Optional[uuid.UUID] = Query(default=None),
    area_id: Optional[uuid.UUID] = Query(default=None),
    is_active: Optional[bool] = Query(default=True),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[Vendor]:
    stmt = select(Vendor).where(Vendor.deleted_at.is_(None))

    if city_id is not None:
        stmt = stmt.where(Vendor.city_id == city_id)
    if area_id is not None:
        stmt = stmt.where(Vendor.area_id == area_id)
    if is_active is not None:
        stmt = stmt.where(Vendor.is_active == is_active)

    stmt = stmt.offset(offset).limit(limit)

    result = db.execute(stmt).scalars().all()
    return list(result)


@router.get(
    "/{vendor_id}",
    response_model=VendorRead,
)
def get_vendor(
    vendor_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Vendor:
    return _get_vendor_or_404(db, vendor_id)


@router.put(
    "/{vendor_id}",
    response_model=VendorRead,
)
def update_vendor(
    vendor_id: uuid.UUID,
    payload: VendorUpdate,
    db: Session = Depends(get_db),
) -> Vendor:
    vendor = _get_vendor_or_404(db, vendor_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vendor, field, value)

    vendor.updated_at = datetime.utcnow()

    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete(
    "/{vendor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vendor(
    vendor_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> None:
    vendor = _get_vendor_or_404(db, vendor_id)

    # Soft delete: mark deleted_at and deactivate
    vendor.deleted_at = datetime.utcnow()
    vendor.is_active = False

    db.add(vendor)
    db.commit()

