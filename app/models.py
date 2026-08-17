from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, utcnow


class StoredFile(Base):
    __tablename__ = "stored_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(64), unique=True)
    media_type: Mapped[str] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    printer_name: Mapped[str | None] = mapped_column(String(127), nullable=True)
    file_id: Mapped[int | None] = mapped_column(ForeignKey("stored_files.id", ondelete="SET NULL"), nullable=True)
    schedule_type: Mapped[str] = mapped_column(String(20), default="interval")
    interval_value: Mapped[int] = mapped_column(Integer, default=60)
    interval_unit: Mapped[str] = mapped_column(String(10), default="minutes")
    daily_time: Mapped[str] = mapped_column(String(5), default="08:00")
    time_of_day: Mapped[str] = mapped_column(String(5), default="08:00")
    days_of_week: Mapped[str] = mapped_column(String(30), default="0,1,2,3,4,5,6")
    monthly_day: Mapped[int] = mapped_column(Integer, default=1)
    days_of_month: Mapped[str] = mapped_column(String(100), default="1")
    timezone: Mapped[str] = mapped_column(String(64), default="Europe/Warsaw")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    selected_file: Mapped[StoredFile | None] = relationship()


class PrintHistory(Base):
    __tablename__ = "print_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    file_name: Mapped[str] = mapped_column(String(255), default="—")
    printer_name: Mapped[str] = mapped_column(String(127), default="—")
    trigger: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(16))
    message: Mapped[str] = mapped_column(Text, default="")
    cups_job_id: Mapped[str | None] = mapped_column(String(64), nullable=True)


def ensure_config(session) -> AppConfig:
    config = session.get(AppConfig, 1)
    if config is None:
        config = AppConfig(id=1)
        session.add(config)
        session.flush()
    return config
