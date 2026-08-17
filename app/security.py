from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from urllib.parse import urlsplit

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.settings import settings

SESSION_COOKIE = "autoprint_session"
SESSION_TTL_SECONDS = 12 * 60 * 60
PUBLIC_PATHS = {
    "/",
    "/dashboard",
    "/settings",
    "/history",
    "/logs",
    "/favicon.ico",
    "/health",
    "/api/auth/status",
    "/api/auth/login",
}


def _session_secret() -> bytes:
    value = f"autoprint\0{settings.admin_username}\0{settings.admin_password}"
    return hashlib.sha256(value.encode()).digest()


def create_session_token() -> str:
    expires = str(int(time.time()) + SESSION_TTL_SECONDS)
    signature = hmac.new(_session_secret(), expires.encode(), hashlib.sha256).digest()
    encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{expires}.{encoded}"


def valid_session_token(token: str | None) -> bool:
    if not token or "." not in token:
        return False
    expires, supplied = token.split(".", 1)
    if not expires.isdigit() or int(expires) < int(time.time()):
        return False
    expected = base64.urlsafe_b64encode(
        hmac.new(_session_secret(), expires.encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    return secrets.compare_digest(supplied, expected)


def valid_credentials(username: str, password: str) -> bool:
    return secrets.compare_digest(username, settings.admin_username) and secrets.compare_digest(
        password, settings.admin_password
    )


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public = request.url.path in PUBLIC_PATHS or request.url.path.startswith("/static/")
        authenticated = not settings.auth_enabled or valid_session_token(
            request.cookies.get(SESSION_COOKIE)
        )
        request.state.authenticated = authenticated
        if settings.auth_enabled and not public and not authenticated:
            return JSONResponse({"detail": "Wymagane jest zalogowanie"}, status_code=401)

        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            origin = request.headers.get("origin")
            if origin:
                parsed = urlsplit(origin)
                if parsed.netloc.lower() != request.headers.get("host", "").lower():
                    return JSONResponse({"detail": "Odrzucono żądanie z innego źródła"}, status_code=403)

        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
        )
        return response
