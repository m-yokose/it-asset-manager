from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.limiter import limiter
from app.core.security import create_access_token, verify_password
from app.models.account import Account

router = APIRouter()
templates = Jinja2Templates(directory=settings.templates_dir)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.username == username).first()
    if not account or not verify_password(password, account.hashed_password):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "ユーザー名またはパスワードが正しくありません"},
            status_code=401,
        )

    token = create_access_token({"sub": str(account.id)})
    response = RedirectResponse(url="/assets", status_code=303)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        samesite="strict",
    )
    return response


@router.post("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response
