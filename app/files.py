from __future__ import annotations

import hashlib
import os
import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader

from app.settings import settings

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}
MEDIA_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".txt": "text/plain",
}


def clean_original_name(value: str | None) -> str:
    name = Path((value or "plik").replace("\\", "/")).name
    name = re.sub(r"[\x00-\x1f\x7f]", "", name).strip()
    return name[:255] or "plik"


async def save_validated_upload(upload: UploadFile) -> dict:
    original_name = clean_original_name(upload.filename)
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(415, "Dozwolone formaty: PDF, PNG, JPG/JPEG oraz TXT")

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{extension}"
    destination = settings.upload_dir / stored_name
    limit = settings.max_upload_mb * 1024 * 1024
    size = 0
    digest = hashlib.sha256()
    try:
        with destination.open("xb") as target:
            while chunk := await upload.read(1024 * 1024):
                size += len(chunk)
                if size > limit:
                    raise HTTPException(413, f"Plik przekracza limit {settings.max_upload_mb} MB")
                digest.update(chunk)
                target.write(chunk)
        if size == 0:
            raise HTTPException(400, "Plik jest pusty")
        os.chmod(destination, 0o640)
        _validate_content(destination, extension)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await upload.close()
    return {
        "original_name": original_name,
        "stored_name": stored_name,
        "media_type": MEDIA_TYPES[extension],
        "size": size,
        "sha256": digest.hexdigest(),
    }


def _validate_content(path: Path, extension: str) -> None:
    try:
        if extension == ".pdf":
            with path.open("rb") as handle:
                if handle.read(5) != b"%PDF-":
                    raise ValueError("Brak sygnatury PDF")
            reader = PdfReader(str(path), strict=True)
            if not reader.pages:
                raise ValueError("Dokument PDF nie zawiera stron")
        elif extension in {".png", ".jpg", ".jpeg"}:
            with Image.open(path) as image:
                expected = "PNG" if extension == ".png" else "JPEG"
                if image.format != expected:
                    raise ValueError("Zawartość nie odpowiada rozszerzeniu pliku")
                if image.width * image.height > 40_000_000:
                    raise ValueError("Obraz ma zbyt dużą rozdzielczość")
                image.verify()
        else:
            raw = path.read_bytes()
            if b"\x00" in raw:
                raise ValueError("Plik TXT wygląda jak plik binarny")
            raw.decode("utf-8-sig")
    except (ValueError, UnicodeDecodeError, UnidentifiedImageError, OSError, Exception) as exc:
        # PdfReader raises several parser-specific exception types; all mean invalid input here.
        raise HTTPException(422, f"Nieprawidłowy lub uszkodzony plik: {str(exc)[:180]}") from exc


def stored_path(stored_name: str) -> Path:
    if not re.fullmatch(r"[a-f0-9]{32}\.(?:pdf|png|jpg|jpeg|txt)", stored_name):
        raise ValueError("Nieprawidłowa nazwa pliku")
    root = settings.upload_dir.resolve()
    path = (root / stored_name).resolve()
    if path.parent != root:
        raise ValueError("Plik poza katalogiem danych")
    return path
