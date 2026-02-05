from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class VendorBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    city_id: uuid.UUID
    area_id: uuid.UUID
    is_active: bool = True


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    city_id: Optional[uuid.UUID] = None
    area_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None


class VendorRead(VendorBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

