import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.software_license import SoftwareLicense
from app.schemas.software_license import SoftwareLicenseCreate, SoftwareLicenseUpdate


def get_licenses(db: Session, skip: int = 0, limit: int = 100) -> list[SoftwareLicense]:
    return db.query(SoftwareLicense).order_by(SoftwareLicense.software_name).offset(skip).limit(limit).all()


def get_expiring_soon(db: Session, days: int = 30) -> list[SoftwareLicense]:
    threshold = datetime.date.today() + datetime.timedelta(days=days)
    return (
        db.query(SoftwareLicense)
        .filter(SoftwareLicense.expiration_date <= threshold)
        .filter(SoftwareLicense.expiration_date >= datetime.date.today())
        .order_by(SoftwareLicense.expiration_date)
        .all()
    )


def get_license(db: Session, license_id: int) -> Optional[SoftwareLicense]:
    return db.query(SoftwareLicense).filter(SoftwareLicense.id == license_id).first()


def create_license(db: Session, data: SoftwareLicenseCreate) -> SoftwareLicense:
    lic = SoftwareLicense(**data.model_dump())
    db.add(lic)
    db.commit()
    db.refresh(lic)
    return lic


def update_license(db: Session, license_id: int, data: SoftwareLicenseUpdate) -> Optional[SoftwareLicense]:
    lic = get_license(db, license_id)
    if not lic:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(lic, key, value)
    db.commit()
    db.refresh(lic)
    return lic


def delete_license(db: Session, license_id: int) -> bool:
    lic = get_license(db, license_id)
    if not lic:
        return False
    db.delete(lic)
    db.commit()
    return True
