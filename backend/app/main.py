import warnings
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1 import assets, auth, software, users
from app.core.config import settings
from app.core.database import Base, engine
from app.core.limiter import limiter
import app.models  # noqa: F401 — registers all models with SQLAlchemy metadata

if settings.secret_key == "change-me-in-production":
    warnings.warn(
        "⚠️  SECRET_KEY がデフォルト値です。.env で必ず変更してください。",
        stacklevel=1,
    )

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IT資産管理システム", docs_url=None, redoc_url=None)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


_static_dir = Path(settings.static_dir)
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(software.router, prefix="/software", tags=["software"])


@app.get("/")
def root():
    return RedirectResponse(url="/assets")


@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    return RedirectResponse(url="/auth/login")
