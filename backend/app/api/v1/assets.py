import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db, require_admin
from app.core.config import settings
from app.models.account import Account
from app.schemas.asset import AssetCreate, AssetUpdate
from app.services import asset_service, user_service

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_dir)


@router.get("/", response_class=HTMLResponse)
def asset_list(
    request: Request,
    status: Optional[str] = None,
    asset_type: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    assets = asset_service.get_assets(db, status=status, asset_type=asset_type, keyword=keyword)
    counts = asset_service.count_assets(db)
    return templates.TemplateResponse(
        "assets/list.html",
        {
            "request": request,
            "assets": assets,
            "counts": counts,
            "current_account": current_account,
            "filter_status": status,
            "filter_type": asset_type,
            "keyword": keyword,
        },
    )


@router.get("/new", response_class=HTMLResponse)
def asset_new(
    request: Request,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    users = user_service.get_users(db)
    return templates.TemplateResponse(
        "assets/form.html",
        {"request": request, "asset": None, "users": users, "current_account": current_account},
    )


@router.post("/new")
def asset_create(
    request: Request,
    hostname: Optional[str] = Form(None),
    asset_type: str = Form(...),
    manufacturer: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    serial_number: Optional[str] = Form(None),
    purchase_date: Optional[str] = Form(None),
    status: str = Form("使用中"),
    assigned_user_id: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    data = AssetCreate(
        hostname=hostname or None,
        asset_type=asset_type,
        manufacturer=manufacturer or None,
        model=model or None,
        serial_number=serial_number or None,
        purchase_date=datetime.date.fromisoformat(purchase_date) if purchase_date else None,
        status=status,
        assigned_user_id=assigned_user_id,
        notes=notes or None,
    )
    asset_service.create_asset(db, data)
    return RedirectResponse(url="/assets", status_code=303)


@router.get("/{asset_id}/edit", response_class=HTMLResponse)
def asset_edit_page(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    asset = asset_service.get_asset(db, asset_id)
    users = user_service.get_users(db)
    return templates.TemplateResponse(
        "assets/form.html",
        {"request": request, "asset": asset, "users": users, "current_account": current_account},
    )


@router.post("/{asset_id}/edit")
def asset_update(
    asset_id: int,
    hostname: Optional[str] = Form(None),
    asset_type: Optional[str] = Form(None),
    manufacturer: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    serial_number: Optional[str] = Form(None),
    purchase_date: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    assigned_user_id: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    data = AssetUpdate(
        hostname=hostname or None,
        asset_type=asset_type,
        manufacturer=manufacturer or None,
        model=model or None,
        serial_number=serial_number or None,
        purchase_date=datetime.date.fromisoformat(purchase_date) if purchase_date else None,
        status=status,
        assigned_user_id=assigned_user_id,
        notes=notes or None,
    )
    asset_service.update_asset(db, asset_id, data)
    return RedirectResponse(url="/assets", status_code=303)


@router.post("/{asset_id}/delete")
def asset_delete(
    asset_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    asset_service.delete_asset(db, asset_id)
    return RedirectResponse(url="/assets", status_code=303)
