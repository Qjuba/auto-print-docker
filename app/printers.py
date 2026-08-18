from __future__ import annotations

import logging
import os
import re
import socket
import subprocess
import threading
from dataclasses import dataclass
from urllib.parse import urlsplit

from app.settings import settings

logger = logging.getLogger(__name__)
_cups_queue_warning_lock = threading.Lock()
_no_destinations_warning_emitted = False


class PrinterError(RuntimeError):
    pass


@dataclass
class CommandResult:
    stdout: str
    stderr: str


def _log_cups_queue_error(error: PrinterError) -> None:
    global _no_destinations_warning_emitted
    message = str(error)
    if "no destinations added" not in message.lower():
        logger.warning("Could not read CUPS queues: %s", message)
        return

    with _cups_queue_warning_lock:
        if _no_destinations_warning_emitted:
            return
        _no_destinations_warning_emitted = True
    logger.warning("Could not read CUPS queues: %s", message)


def _reset_no_destinations_warning() -> None:
    global _no_destinations_warning_emitted
    with _cups_queue_warning_lock:
        _no_destinations_warning_emitted = False


def _run(args: list[str], timeout: int = 12) -> CommandResult:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "CUPS_SERVER": settings.cups_server})
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PrinterError(f"Missing system tool: {args[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise PrinterError("The printing service timed out") from exc
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "Unknown CUPS error").strip()
        raise PrinterError(message[:800])
    return CommandResult(result.stdout, result.stderr)


def list_printers() -> list[dict]:
    try:
        devices = _run(["lpstat", "-v"]).stdout
    except PrinterError as exc:
        _log_cups_queue_error(exc)
        return []
    _reset_no_destinations_warning()

    statuses: dict[str, dict] = {}
    try:
        for line in _run(["lpstat", "-p", "-d"]).stdout.splitlines():
            match = re.match(r"printer\s+(\S+)\s+(.*)", line)
            if match:
                name, description = match.groups()
                lowered = description.lower()
                state = "idle" if "idle" in lowered else "disabled" if "disabled" in lowered else "busy"
                statuses[name] = {"state": state, "message": description}
    except PrinterError:
        pass

    try:
        current_name = None
        for line in _run(["lpstat", "-l", "-p"]).stdout.splitlines():
            match = re.match(r"printer\s+(\S+)\s+", line)
            if match:
                current_name = match.group(1)
            elif current_name and line.strip().startswith("Location:"):
                statuses.setdefault(current_name, {}).update(
                    {"location": line.split(":", 1)[1].strip()}
                )
    except PrinterError:
        pass

    printers = []
    for line in devices.splitlines():
        match = re.match(r"device for (\S+):\s+(.+)", line)
        if not match:
            continue
        name, uri = match.groups()
        status = {
            "state": "unknown",
            "message": "No status information",
            "location": "",
            **statuses.get(name, {}),
        }
        printers.append({"name": name, "uri": uri, **status})
    return sorted(printers, key=lambda item: item["name"].lower())


def discover_printers() -> list[dict]:
    found: dict[str, dict] = {}
    try:
        output = _run(["ippfind", "--timeout", "4", "--print-uri"], timeout=7).stdout
        for line in output.splitlines():
            uri = line.strip()
            if uri.startswith(("ipp://", "ipps://")):
                found[uri] = {"uri": uri, "source": "IPP/mDNS"}
    except PrinterError as exc:
        logger.info("mDNS discovery returned no devices: %s", exc)

    try:
        for line in _run(["lpinfo", "-v"], timeout=8).stdout.splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2 and parts[1].startswith(("ipp://", "ipps://")):
                found.setdefault(parts[1], {"uri": parts[1], "source": "CUPS"})
    except PrinterError:
        pass
    return list(found.values())


def printer_connection_status(printer: dict, timeout: float = 2.5) -> dict:
    """Check whether a direct IPP printer endpoint accepts network connections."""
    uri = str(printer.get("uri", ""))
    parsed = urlsplit(uri)
    if parsed.scheme not in {"ipp", "ipps"}:
        return {"reachable": None, "message": printer.get("message", "No status information")}
    if not parsed.hostname:
        return {"reachable": False, "message": "The printer IPP address is invalid"}

    try:
        port = parsed.port or 631
    except ValueError:
        return {"reachable": False, "message": "The port in the printer IPP address is invalid"}
    try:
        connection = socket.create_connection((parsed.hostname, port), timeout=timeout)
        connection.close()
    except OSError:
        return {
            "reachable": False,
            "message": (
                f"The printer is not responding at {parsed.hostname}:{port}. "
                "Check that it is powered on and connected to the network."
            ),
        }
    return {"reachable": True, "message": "The printer is reachable"}


def ensure_printer_reachable(printer: dict) -> None:
    status = printer_connection_status(printer)
    if status["reachable"] is False:
        raise PrinterError(status["message"])


def add_printer(name: str, uri: str, location: str = "") -> None:
    args = ["lpadmin", "-p", name, "-E", "-v", uri, "-m", "everywhere"]
    if location:
        args.extend(["-L", location])
    _run(args, timeout=30)
    logger.info("Added printer queue %s", name)


def update_printer(name: str, uri: str, location: str = "") -> None:
    args = ["lpadmin", "-p", name, "-E", "-v", uri, "-m", "everywhere", "-L", location]
    _run(args, timeout=30)
    logger.info("Updated printer queue %s", name)


def submit_print(printer_name: str, file_path: str, title: str) -> str | None:
    output = _run(["lp", "-d", printer_name, "-t", title[:120], "--", file_path], timeout=30).stdout
    match = re.search(r"request id is\s+(\S+)", output)
    return match.group(1) if match else None
