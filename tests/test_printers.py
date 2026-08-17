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
