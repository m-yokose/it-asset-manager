import datetime
from typing import Optional

from pydantic import BaseModel


class AssetBase(BaseModel):
    hostname: Optional[str] = None
    asset_type: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime.date] = None
    status: str = "使用中"
    assigned_user_id: Optional[int] = None
    notes: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    hostname: Optional[str] = None
    asset_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime.date] = None
    status: Optional[str] = None
    assigned_user_id: Optional[int] = None
    notes: Optional[str] = None


class AssetResponse(AssetBase):
    id: int

    model_config = {"from_attributes": True}
