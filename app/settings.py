from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data")).resolve()
    timezone: str = os.getenv("TZ", "Europe/Warsaw")
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "25"))
    admin_username: str = os.getenv("ADMIN_USERNAME", "")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "")
    cups_server: str = os.getenv("CUPS_SERVER", "/run/cups/cups.sock")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    trust_proxy_headers: bool = _bool("TRUST_PROXY_HEADERS")
    session_cookie_secure: bool = _bool("SESSION_COOKIE_SECURE")

    @property
    def database_url(self) -> str:
        override = os.getenv("DATABASE_URL")
        if override:
            return override
        return f"sqlite:///{(self.data_dir / 'autoprint.db').as_posix()}"

    @property
    def upload_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def log_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def auth_enabled(self) -> bool:
        return bool(self.admin_username and self.admin_password)


settings = Settings()
