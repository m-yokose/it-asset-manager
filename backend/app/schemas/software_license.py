import datetime
from typing import Optional

from pydantic import BaseModel


class SoftwareLicenseBase(BaseModel):
    software_name: str
    license_key: Optional[str] = None
    expiration_date: Optional[datetime.date] = None
    license_count: int = 1


class SoftwareLicenseCreate(SoftwareLicenseBase):
    pass


class SoftwareLicenseUpdate(BaseModel):
    software_name: Optional[str] = None
    license_key: Optional[str] = None
    expiration_date: Optional[datetime.date] = None
    license_count: Optional[int] = None


class SoftwareLicenseResponse(SoftwareLicenseBase):
    id: int

    model_config = {"from_attributes": True}
