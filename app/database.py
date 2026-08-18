from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False, "timeout": 30} if settings.database_url.startswith("sqlite") else {},
    pool_pre_ping=True,
)


if settings.database_url.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def configure_sqlite(connection, _):
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    with SessionLocal() as session:
        yield session


def migrate_database() -> None:
    """Apply the small, additive migrations supported by the standalone app."""
    inspector = inspect(engine)
    if "app_config" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("app_config")}
    with engine.begin() as connection:
        if "monthly_day" not in columns:
            connection.execute(text("ALTER TABLE app_config ADD COLUMN monthly_day INTEGER NOT NULL DEFAULT 1"))
        if "time_of_day" not in columns:
            connection.execute(text("ALTER TABLE app_config ADD COLUMN time_of_day VARCHAR(5) NOT NULL DEFAULT '08:00'"))
            connection.execute(text("UPDATE app_config SET time_of_day = daily_time"))
        if "days_of_month" not in columns:
            connection.execute(text("ALTER TABLE app_config ADD COLUMN days_of_month VARCHAR(100) NOT NULL DEFAULT '1'"))
            connection.execute(text("UPDATE app_config SET days_of_month = CAST(monthly_day AS TEXT)"))
        if "cron_expression" not in columns:
            connection.execute(
                text("ALTER TABLE app_config ADD COLUMN cron_expression VARCHAR(128) NOT NULL DEFAULT '0 8 * * *'")
            )
        connection.execute(text("UPDATE app_config SET schedule_type = 'weekly' WHERE schedule_type = 'daily'"))
