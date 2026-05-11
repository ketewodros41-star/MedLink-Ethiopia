from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.db.models import Pharmacy, UserRole

router = APIRouter()


class DemoLoginRequest(BaseModel):
    role: str
    username: str


@router.post("/demo-login")
async def demo_login(payload: DemoLoginRequest, db: SessionDep = ...):
    role = payload.role.strip().lower()
    if role not in {UserRole.PATIENT.value, UserRole.PHARMACIST.value, UserRole.ADMIN.value}:
        raise HTTPException(status_code=400, detail="Unsupported role")

    token_payload = {
        "sub": payload.username.strip() or "demo-user",
        "roles": [role],
        "profile": f"{role}/{payload.username.strip() or 'demo-user'}",
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }

    if role == UserRole.PHARMACIST.value:
        pharmacy = (await db.execute(select(Pharmacy).order_by(Pharmacy.created_at.asc()))).scalars().first()
        if pharmacy is None:
            raise HTTPException(status_code=500, detail="No pharmacy configured for demo login")
        token_payload["pharmacy_id"] = pharmacy.id
        token_payload["pharmacy_name"] = pharmacy.name

    token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "user": token_payload}
