from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import CurrentUserDep, RedisDep, SessionDep
from app.core.security import require_roles
from app.services.inventory_service import verify_inventory_action

router = APIRouter()

class InventoryVerifyRequest(BaseModel):
    pharmacy_id: str
    medicine_id: str
    action: str
    quantity: int | None = None

@router.post("/verify")
async def verify_inventory(
    req: InventoryVerifyRequest,
    current_user: dict = Depends(require_roles("pharmacist", "admin")),
    redis: RedisDep = ...,
    db: SessionDep = ...,
):
    try:
        inventory = await verify_inventory_action(
            db,
            user_id=current_user["sub"],
            pharmacy_id=req.pharmacy_id,
            medicine_id=req.medicine_id,
            action=req.action,
            quantity=req.quantity,
        )
        await db.commit()
    except ValueError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    event_payload = {
        "user_id": current_user["sub"],
        "pharmacy_id": req.pharmacy_id,
        "medicine_id": req.medicine_id,
        "action": req.action,
        "quantity_available": inventory.quantity_available,
        "confidence_score": inventory.confidence_score,
    }
    try:
        await redis.xadd("events:inventory_verification", event_payload)
    except Exception:
        pass
    return {"status": "verification_recorded", "data": event_payload, "inventory_id": inventory.id}
