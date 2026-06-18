from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db, require_admin
from app.core.config import settings
from app.models.account import Account
from app.schemas.user import UserCreate, UserUpdate
from app.services import user_service

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_dir)


@router.get("/", response_class=HTMLResponse)
def user_list(
    request: Request,
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account),
):
    users = user_service.get_users(db)
    return templates.TemplateResponse(
        "users/list.html",
        {"request": request, "users": users, "current_account": current_account},
    )


@router.get("/new", response_class=HTMLResponse)
def user_new(
    request: Request,
    current_account: Account = Depends(require_admin),
):
    return templates.TemplateResponse(
        "users/form.html",
        {"request": request, "user": None, "current_account": current_account},
    )


@router.post("/new")
def user_create(
    name: str = Form(...),
    department: Optional[str] = Form(None),
    email: str = Form(...),
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    user_service.create_user(db, UserCreate(name=name, department=department or None, email=email))
    return RedirectResponse(url="/users", status_code=303)


@router.get("/{user_id}/edit", response_class=HTMLResponse)
def user_edit_page(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    user = user_service.get_user(db, user_id)
    return templates.TemplateResponse(
        "users/form.html",
        {"request": request, "user": user, "current_account": current_account},
    )


@router.post("/{user_id}/edit")
def user_update(
    user_id: int,
    name: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    user_service.update_user(db, user_id, UserUpdate(name=name, department=department, email=email))
    return RedirectResponse(url="/users", status_code=303)


@router.post("/{user_id}/delete")
def user_delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_account: Account = Depends(require_admin),
):
    user_service.delete_user(db, user_id)
    return RedirectResponse(url="/users", status_code=303)
