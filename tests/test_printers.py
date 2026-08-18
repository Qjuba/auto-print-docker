from types import SimpleNamespace

import pytest

from app import printers


def test_add_printer_uses_argument_list_without_shell(monkeypatch):
    captured = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(printers.subprocess, "run", fake_run)
    printers.add_printer("Canon_1", "ipp://192.0.2.10/ipp/print", "Biuro")
    assert captured["args"] == [
        "lpadmin", "-p", "Canon_1", "-E", "-v", "ipp://192.0.2.10/ipp/print",
        "-m", "everywhere", "-L", "Biuro",
    ]
    assert captured["kwargs"]["check"] is False


def test_failed_cups_command_is_reported(monkeypatch):
    monkeypatch.setattr(
        printers.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="printer offline"),
    )
    with pytest.raises(printers.PrinterError, match="offline"):
        printers.submit_print("Canon", "/tmp/file.pdf", "Test")


def test_missing_cups_destinations_are_logged_once_until_recovery(monkeypatch, caplog):
    state = {"available": False}

    def fake_run(args, **_kwargs):
        if not state["available"]:
            raise printers.PrinterError("lpstat: No destinations added.")
        if args == ["lpstat", "-v"]:
            return printers.CommandResult("device for Canon: ipp://printer.local/ipp/print", "")
        return printers.CommandResult("", "")

    monkeypatch.setattr(printers, "_run", fake_run)
    monkeypatch.setattr(printers, "_no_destinations_warning_emitted", False)

    with caplog.at_level("WARNING", logger="app.printers"):
        assert printers.list_printers() == []
        assert printers.list_printers() == []
        state["available"] = True
        assert len(printers.list_printers()) == 1
        state["available"] = False
        assert printers.list_printers() == []

    messages = [record.getMessage() for record in caplog.records]
    assert messages == [
        "Could not read CUPS queues: lpstat: No destinations added.",
        "Could not read CUPS queues: lpstat: No destinations added.",
    ]


def test_update_printer_keeps_existing_queue_name(monkeypatch):
    captured = {}

    def fake_run(args, **_):
        captured["args"] = args
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(printers.subprocess, "run", fake_run)
    printers.update_printer("Canon_1", "ipps://192.0.2.10/ipp/print", "Magazyn")
    assert captured["args"] == [
        "lpadmin", "-p", "Canon_1", "-E", "-v", "ipps://192.0.2.10/ipp/print",
        "-m", "everywhere", "-L", "Magazyn",
    ]


def test_network_printer_is_reported_as_reachable(monkeypatch):
    closed = []

    class Connection:
        def close(self):
            closed.append(True)

    monkeypatch.setattr(
        printers.socket,
        "create_connection",
        lambda address, timeout: Connection(),
    )
    result = printers.printer_connection_status(
        {"uri": "ipp://192.0.2.10/ipp/print", "message": "idle"}
    )
    assert result == {"reachable": True, "message": "The printer is reachable"}
    assert closed == [True]


def test_unreachable_network_printer_is_reported_to_user(monkeypatch):
    def refuse_connection(*_args, **_kwargs):
        raise OSError("host unreachable")

    monkeypatch.setattr(printers.socket, "create_connection", refuse_connection)
    queue = {"uri": "ipps://printer.local/ipp/print", "message": "idle"}
    result = printers.printer_connection_status(queue)
    assert result["reachable"] is False
    assert "printer.local:631" in result["message"]
    with pytest.raises(printers.PrinterError, match="not responding"):
        printers.ensure_printer_reachable(queue)


def test_non_network_queue_keeps_cups_status(monkeypatch):
    monkeypatch.setattr(
        printers.socket,
        "create_connection",
        lambda *_args, **_kwargs: pytest.fail("socket should not be used"),
    )
    result = printers.printer_connection_status({"uri": "usb://Canon/G3010", "message": "idle"})
    assert result == {"reachable": None, "message": "idle"}
