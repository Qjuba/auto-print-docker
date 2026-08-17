from __future__ import annotations

import logging
import tempfile
from datetime import datetime

from app.database import session_scope
from app.files import stored_path
from app.models import PrintHistory, ensure_config
from app.printers import PrinterError, ensure_printer_reachable, list_printers, submit_print
from app.settings import settings

logger = logging.getLogger(__name__)


def perform_print(trigger: str = "manual", test_page: bool = False) -> PrintHistory:
    with session_scope() as session:
        config = ensure_config(session)
        printer = config.printer_name or "—"
        file_name = "Strona testowa AutoPrint" if test_page else (
            config.selected_file.original_name if config.selected_file else "—"
        )
        history = PrintHistory(
            file_name=file_name,
            printer_name=printer,
            trigger=trigger,
            status="failed",
            message="",
        )
        session.add(history)
        session.flush()

        try:
            if not config.printer_name:
                raise PrinterError("Nie wybrano drukarki")
            queue = next(
                (item for item in list_printers() if item["name"] == config.printer_name),
                None,
            )
            if queue is None:
                raise PrinterError("Wybrana drukarka nie jest dostępna w CUPS")
            if queue["state"] == "disabled":
                raise PrinterError(f"Drukarka jest wyłączona: {queue['message']}")
            ensure_printer_reachable(queue)
            temporary_name = None
            if test_page:
                settings.data_dir.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", prefix="autoprint-test-", dir=settings.data_dir,
                    encoding="utf-8", delete=False
                ) as test_file:
                    temporary_name = test_file.name
                    test_file.write(
                        "AUTOPRINT — STRONA TESTOWA\n\n"
                        f"Drukarka: {config.printer_name}\n"
                        f"Data: {datetime.now().astimezone().isoformat(timespec='seconds')}\n\n"
                        "Jeżeli widzisz tę stronę, połączenie CUPS/IPP działa poprawnie.\n"
                    )
                path = temporary_name
            else:
                if not config.selected_file:
                    raise PrinterError("Nie wybrano pliku do drukowania")
                path_obj = stored_path(config.selected_file.stored_name)
                if not path_obj.is_file():
                    raise PrinterError("Wybrany plik nie istnieje w magazynie")
                path = str(path_obj)

            try:
                job_id = submit_print(config.printer_name, path, file_name)
            finally:
                if temporary_name:
                    __import__("pathlib").Path(temporary_name).unlink(missing_ok=True)
            history.status = "submitted"
            history.cups_job_id = job_id
            history.message = "Zadanie zostało przyjęte przez CUPS"
            logger.info("Przekazano wydruk %s do %s (%s)", file_name, printer, trigger)
        except Exception as exc:
            history.status = "failed"
            history.message = str(exc)[:1000]
            logger.error("Wydruk %s nie powiódł się: %s", trigger, exc)
        session.flush()
        session.expunge(history)
        return history


def scheduled_print_job() -> None:
    perform_print(trigger="automatic")
