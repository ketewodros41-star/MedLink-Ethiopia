from __future__ import annotations

import hashlib

from fastapi import HTTPException, UploadFile

from app.core.config import settings


def detect_image_type(content: bytes) -> str | None:
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if content.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    return None


def validate_upload(file: UploadFile, content: bytes) -> dict:
    if len(content) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Upload exceeds size limit")

    detected_type = detect_image_type(content)
    if detected_type not in {"jpeg", "png"}:
        raise HTTPException(status_code=400, detail="Upload content is not a valid JPEG or PNG")

    sha256 = hashlib.sha256(content).hexdigest()
    return {
        "content_type": file.content_type,
        "detected_type": detected_type,
        "sha256": sha256,
        "size_bytes": len(content),
    }
