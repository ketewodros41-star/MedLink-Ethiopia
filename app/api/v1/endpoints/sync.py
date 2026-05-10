from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.services.sync_service import queue_sync_operations

router = APIRouter()

class SyncPayload(BaseModel):
    client_id: str
    timestamp: str
    operations: List[dict]

@router.post("/push")
async def push_offline_sync(
    payload: SyncPayload,
    current_user: dict = Depends(require_roles("patient", "pharmacist", "admin")),
    db: SessionDep = ...,
):
    operations = await queue_sync_operations(
        db,
        user_id=current_user["sub"],
        client_id=payload.client_id,
        operations=payload.operations,
    )
    await db.commit()
    return {
        "status": "queued",
        "operations_received": len(operations),
        "statuses": [operation.status for operation in operations],
    }
