import datetime

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SoftwareLicense(Base):
    __tablename__ = "software_licenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    software_name: Mapped[str] = mapped_column(String(100), nullable=False)
    license_key: Mapped[str | None] = mapped_column(String(200), nullable=True)
    expiration_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    license_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
