from types import SimpleNamespace

from app import security


def test_signed_session_token_and_credentials(monkeypatch):
    monkeypatch.setattr(
        security,
        "settings",
        SimpleNamespace(admin_username="operator", admin_password="secret"),
    )
    assert security.valid_credentials("operator", "secret") is True
    assert security.valid_credentials("operator", "wrong") is False
    token = security.create_session_token()
    assert security.valid_session_token(token) is True
    assert security.valid_session_token(token + "changed") is False
