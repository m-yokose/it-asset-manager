from typing import Optional

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    asset_type: Optional[str] = None,
    keyword: Optional[str] = None,
) -> list[Asset]:
    q = db.query(Asset)
    if status:
        q = q.filter(Asset.status == status)
    if asset_type:
        q = q.filter(Asset.asset_type == asset_type)
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(
            Asset.hostname.ilike(like)
            | Asset.model.ilike(like)
            | Asset.serial_number.ilike(like)
        )
    return q.order_by(Asset.id.desc()).offset(skip).limit(limit).all()


def count_assets(db: Session) -> dict:
    total = db.query(Asset).count()
    by_status = {}
    for status in ("使用中", "保管", "廃棄"):
        by_status[status] = db.query(Asset).filter(Asset.status == status).count()
    return {"total": total, **by_status}


def get_asset(db: Session, asset_id: int) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.id == asset_id).first()


def create_asset(db: Session, data: AssetCreate) -> Asset:
    asset = Asset(**data.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def update_asset(db: Session, asset_id: int, data: AssetUpdate) -> Optional[Asset]:
    asset = get_asset(db, asset_id)
    if not asset:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset_id: int) -> bool:
    asset = get_asset(db, asset_id)
    if not asset:
        return False
    db.delete(asset)
    db.commit()
    return True
