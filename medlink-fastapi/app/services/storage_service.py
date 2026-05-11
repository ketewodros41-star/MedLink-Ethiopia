from __future__ import annotations

import base64
import hashlib
import hmac
from pathlib import Path
from time import time
from uuid import uuid4

from app.core.config import settings


class LocalPrescriptionStorage:
    def __init__(self, base_dir: str) -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_prescription(self, *, user_id: str, content: bytes, suffix: str) -> dict:
        sha256 = hashlib.sha256(content).hexdigest()
        object_id = f"{user_id}-{uuid4().hex}{suffix}"
        object_path = self.base_path / object_id
        object_path.write_bytes(content)
        signed_url = self._sign_url(object_id)
        return {
            "object_id": object_id,
            "sha256": sha256,
            "size_bytes": len(content),
            "signed_url": signed_url,
        }

    def _sign_url(self, object_id: str) -> str:
        expires_at = int(time()) + settings.SIGNED_URL_TTL_SECONDS
        payload = f"{object_id}:{expires_at}"
        signature = hmac.new(settings.SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).digest()
        encoded_sig = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        return f"/api/v1/ocr/files/{object_id}?expires={expires_at}&sig={encoded_sig}"


storage = LocalPrescriptionStorage(settings.PRESCRIPTION_STORAGE_DIR)
