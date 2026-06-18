from sqlalchemy import Boolean, Integer, String  # noqa: F401 (Boolean kept for is_active)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Account(Base):
    """システムログイン用アカウント（IT管理者）"""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="viewer")  # "admin" | "viewer"
