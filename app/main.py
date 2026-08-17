from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db, migrate_database
from app.files import save_validated_upload, stored_path
from app.models import PrintHistory, StoredFile, ensure_config
from app.printers import (
    PrinterError,
    add_printer,
    discover_printers,
    list_printers,
    printer_connection_status,
    update_printer,
)
from app.scheduler import next_run_time, preview_times, start_scheduler, stop_scheduler, sync_schedule
from app.schemas import AddPrinterRequest, LoginRequest, ScheduleRule, ScheduleUpdate
from app.security import (
    SESSION_COOKIE,
    SESSION_TTL_SECONDS,
    SecurityMiddleware,
    create_session_token,
    valid_credentials,
)
from app.settings import settings
from app.tasks import perform_print

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
logger = logging.getLogger(__name__)


def configure_logging() -> None:
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s — %(message)s")
    root = logging.getLogger()
    root.setLevel(settings.log_level)
    if not any(isinstance(handler, RotatingFileHandler) for handler in root.handlers):
        file_handler = RotatingFileHandler(
            settings.log_dir / "app.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    configure_logging()
    Base.metadata.create_all(engine)
    migrate_database()
    start_scheduler()
    logger.info("AutoPrint uruchomiony")
    try:
        yield
    finally:
        stop_scheduler()
        logger.info("AutoPrint zatrzymany")


app = FastAPI(
    title="AutoPrint",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)
app.add_middleware(SecurityMiddleware)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def file_json(file: StoredFile | None) -> dict | None:
    if not file:
        return None
    return {
        "id": file.id,
        "name": file.original_name,
        "size": file.size,
        "media_type": file.media_type,
        "sha256": file.sha256,
        "created_at": iso(file.created_at),
    }


def history_json(item: PrintHistory) -> dict:
    return {
        "id": item.id,
        "created_at": iso(item.created_at),
        "file_name": item.file_name,
        "printer_name": item.printer_name,
        "trigger": item.trigger,
        "status": item.status,
        "message": item.message,
        "cups_job_id": item.cups_job_id,
    }


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/dashboard", status_code=307)


@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
@app.get("/settings", response_class=HTMLResponse, include_in_schema=False)
@app.get("/history", response_class=HTMLResponse, include_in_schema=False)
@app.get("/logs", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"max_upload_mb": settings.max_upload_mb})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/auth/status")
def auth_status(request: Request):
    return {"enabled": settings.auth_enabled, "authenticated": request.state.authenticated}


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    if not settings.auth_enabled:
        return {"ok": True}
    if not valid_credentials(payload.username, payload.password):
        raise HTTPException(401, "Nieprawidłowa nazwa użytkownika lub hasło")
    response = JSONResponse({"ok": True})
    response.set_cookie(
        SESSION_COOKIE,
        create_session_token(),
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="strict",
        path="/",
    )
    return response


@app.post("/api/auth/logout")
def logout():
    response = JSONResponse({"ok": True})
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response


@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    config = ensure_config(db)
    db.commit()
    last = db.scalars(select(PrintHistory).order_by(desc(PrintHistory.created_at)).limit(1)).first()
    printers = list_printers()
    selected_printer = next((item for item in printers if item["name"] == config.printer_name), None)
    if selected_printer:
        connection = printer_connection_status(selected_printer)
        selected_printer = {**selected_printer, **connection}
        if connection["reachable"] is False:
            selected_printer["state"] = "unavailable"
    return {
        "enabled": config.enabled,
        "printer_name": config.printer_name,
        "printer_status": selected_printer or ({"state": "unavailable", "message": "Drukarka nie odpowiada"} if config.printer_name else None),
        "file": file_json(config.selected_file),
        "schedule": {
            "type": config.schedule_type,
            "interval_value": config.interval_value,
            "interval_unit": config.interval_unit,
            "time_of_day": config.time_of_day,
            "days_of_week": [int(day) for day in config.days_of_week.split(",") if day != ""],
            "days_of_month": [int(day) for day in config.days_of_month.split(",") if day and day != "last"],
            "last_day_of_month": "last" in config.days_of_month.split(","),
            "timezone": config.timezone,
        },
        "last_print": history_json(last) if last else None,
        "next_run": iso(next_run_time()),
        "auth_enabled": settings.auth_enabled,
    }


@app.put("/api/config")
def update_config(payload: ScheduleUpdate, db: Session = Depends(get_db)):
    config = ensure_config(db)
    if payload.enabled and not config.file_id:
        raise HTTPException(422, "Prześlij plik przed włączeniem automatycznego drukowania")
    existing_names = {item["name"] for item in list_printers()}
    if payload.printer_name and payload.printer_name not in existing_names:
        raise HTTPException(422, "Wybrana kolejka drukarki nie istnieje w CUPS")
    config.enabled = payload.enabled
    config.printer_name = payload.printer_name
    config.schedule_type = payload.schedule_type
    config.interval_value = payload.interval_value
    config.interval_unit = payload.interval_unit
    config.time_of_day = payload.time_of_day
    config.days_of_week = ",".join(str(day) for day in payload.days_of_week)
    month_days = [str(day) for day in payload.days_of_month]
    if payload.last_day_of_month:
        month_days.append("last")
    config.days_of_month = ",".join(month_days)
    config.timezone = payload.timezone
    db.commit()
    sync_schedule()
    return {"ok": True, "next_run": iso(next_run_time())}


@app.post("/api/schedule/preview")
def schedule_preview(payload: ScheduleRule):
    return {"occurrences": [iso(value) for value in preview_times(payload)]}


@app.post("/api/files")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    metadata = await save_validated_upload(file)
    new_file = StoredFile(**metadata)
    config = ensure_config(db)
    previous = config.selected_file
    db.add(new_file)
    db.flush()
    config.file_id = new_file.id
    if previous:
        previous_path = stored_path(previous.stored_name)
        db.delete(previous)
    else:
        previous_path = None
    db.commit()
    if previous_path:
        previous_path.unlink(missing_ok=True)
    return file_json(new_file)


@app.delete("/api/files/current")
def delete_file(db: Session = Depends(get_db)):
    config = ensure_config(db)
    current = config.selected_file
    if not current:
        return {"ok": True}
    path = stored_path(current.stored_name)
    config.enabled = False
    config.file_id = None
    db.delete(current)
    db.commit()
    path.unlink(missing_ok=True)
    sync_schedule()
    return {"ok": True}


@app.get("/api/printers")
def printers():
    return {"items": list_printers()}


@app.get("/api/printers/discover")
def printer_discovery():
    return {"items": discover_printers()}


@app.post("/api/printers")
def create_printer(payload: AddPrinterRequest):
    try:
        add_printer(payload.name, payload.uri, payload.location)
    except PrinterError as exc:
        raise HTTPException(502, f"CUPS odrzucił drukarkę: {exc}") from exc
    return {"ok": True}


@app.put("/api/printers/{printer_name}")
def edit_printer(printer_name: str, payload: AddPrinterRequest):
    if payload.name != printer_name:
        raise HTTPException(422, "Nazwy istniejącej kolejki nie można zmienić")
    if printer_name not in {item["name"] for item in list_printers()}:
        raise HTTPException(404, "Kolejka drukarki nie istnieje")
    try:
        update_printer(printer_name, payload.uri, payload.location)
    except PrinterError as exc:
        raise HTTPException(502, f"CUPS odrzucił zmiany: {exc}") from exc
    return {"ok": True}


@app.post("/api/print/manual")
def manual_print():
    return history_json(perform_print("manual"))


@app.post("/api/print/test")
def test_print():
    return history_json(perform_print("manual", test_page=True))


@app.get("/api/history")
def history(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items = db.scalars(
        select(PrintHistory).order_by(desc(PrintHistory.created_at)).offset(offset).limit(limit)
    ).all()
    return {"items": [history_json(item) for item in items]}


@app.get("/api/logs")
def logs(lines: int = Query(default=150, ge=10, le=500)):
    path = settings.log_dir / "app.log"
    if not path.exists():
        return {"lines": []}
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        content = handle.readlines()[-lines:]
    return {"lines": [line.rstrip() for line in content]}
