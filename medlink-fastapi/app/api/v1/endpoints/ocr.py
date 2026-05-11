from pathlib import Path
from time import time

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import CurrentUserDep
from app.core.config import settings
from app.core.security import require_roles
from app.services.ocr_service import process_prescription_image
from app.services.storage_service import storage
from app.services.upload_security_service import validate_upload
import base64
import hashlib
import hmac

router = APIRouter()

@router.post("/upload")
async def upload_prescription(
    current_user: dict = Depends(require_roles("patient", "pharmacist", "admin")),
    file: UploadFile = File(...)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")

    contents = await file.read()
    upload_metadata = validate_upload(file, contents)
    stored_object = storage.save_prescription(
        user_id=current_user["sub"],
        content=contents,
        suffix=".jpg" if upload_metadata["detected_type"] == "jpeg" else ".png",
    )
    results = process_prescription_image(contents)

    return {
        "status": "processed",
        "user": current_user["sub"],
        "upload": {**upload_metadata, **stored_object},
        "extracted_data": results
    }


@router.get("/files/{object_id}")
async def get_uploaded_prescription(object_id: str, expires: int, sig: str):
    if expires < int(time()):
        raise HTTPException(status_code=403, detail="Signed URL expired")
    payload = f"{object_id}:{expires}"
    expected = base64.urlsafe_b64encode(
        hmac.new(settings.SIGNING_SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=403, detail="Invalid file signature")
    file_path = Path(settings.PRESCRIPTION_STORAGE_DIR) / object_id
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
