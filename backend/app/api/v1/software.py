import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db, require_admin
from app.core.config import settings
from app.models.account import Account
from app.schemas.software_license import SoftwareLicenseCreate
from app.services import software_service

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_dir)


@router.get("/", response_class=HTMLResponse)
def software_list(
    request: Request,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    licenses = software_service.get_licenses(db)
    expiring = software_service.get_expiring_soon(db, days=30)
    return templates.TemplateResponse(
        "software/list.html",
        {
            "request": request,
            "licenses": licenses,
            "expiring": expiring,
            "current_account": current_account,
        },
    )


@router.get("/new", response_class=HTMLResponse)
def software_new(
    request: Request,
    current_account: Account = Depends(require_admin),
):
    return templates.TemplateResponse(
        "software/form.html",
        {"request": request, "license": None, "current_account": current_account},
    )


@router.post("/new")
def software_create(
    software_name: str = Form(...),
    license_key: Optional[str] = Form(None),
    expiration_date: Optional[str] = Form(None),
    license_count: int = Form(1),
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    software_service.create_license(
        db,
        SoftwareLicenseCreate(
            software_name=software_name,
            license_key=license_key or None,
            expiration_date=datetime.date.fromisoformat(expiration_date) if expiration_date else None,
            license_count=license_count,
        ),
    )
    return RedirectResponse(url="/software", status_code=303)


@router.post("/{license_id}/delete")
def software_delete(
    license_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    software_service.delete_license(db, license_id)
    return RedirectResponse(url="/software", status_code=303)
