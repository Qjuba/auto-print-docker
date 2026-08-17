from io import BytesIO

from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app


def valid_pdf() -> bytes:
    stream = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(stream)
    return stream.getvalue()


def test_upload_dashboard_and_failed_manual_print():
    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200

        auth = client.get("/api/auth/status")
        assert auth.json() == {"enabled": False, "authenticated": True}

        page = client.get("/")
        assert page.status_code == 200
        assert page.url.path == "/dashboard"
        assert "AutoPrint" in page.text
        assert "frame-ancestors 'none'" in page.headers["content-security-policy"]

        cross_origin = client.delete(
            "/api/files/current",
            headers={"Origin": "https://attacker.example"},
        )
        assert cross_origin.status_code == 403

        rejected = client.post(
            "/api/files",
            files={"file": ("payload.exe", b"MZ", "application/octet-stream")},
        )
        assert rejected.status_code == 415

        uploaded = client.post(
            "/api/files",
            files={"file": ("document.pdf", valid_pdf(), "application/pdf")},
        )
        assert uploaded.status_code == 200
        assert uploaded.json()["name"] == "document.pdf"

        dashboard = client.get("/api/dashboard")
        assert dashboard.status_code == 200
        assert dashboard.json()["file"]["name"] == "document.pdf"

        preview = client.post(
            "/api/schedule/preview",
            json={
                "schedule_type": "monthly",
                "time_of_day": "08:00",
                "days_of_month": [1, 15],
                "last_day_of_month": True,
                "timezone": "Europe/Warsaw",
            },
        )
        assert preview.status_code == 200
        assert len(preview.json()["occurrences"]) == 5

        printed = client.post("/api/print/manual")
        assert printed.status_code == 200
        assert printed.json()["status"] == "failed"
        assert "drukarki" in printed.json()["message"]
