from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import CurrentUserDep, RedisDep, SessionDep
from app.core.security import require_roles
from app.services.reservation_service import create_reservation_record, expire_stale_reservations

router = APIRouter()

class ReservationCreate(BaseModel):
    pharmacy_id: str
    medicine_id: str
    quantity: int

@router.post("/")
async def create_reservation(
    req: ReservationCreate,
    current_user: dict = Depends(require_roles("patient", "admin")),
    redis: RedisDep = ...,
    db: SessionDep = ...,
):
    try:
        expired = await expire_stale_reservations(db)
        reservation = await create_reservation_record(
            db,
            user_id=current_user["sub"],
            pharmacy_id=req.pharmacy_id,
            medicine_id=req.medicine_id,
            quantity=req.quantity,
        )
        await db.commit()
    except ValueError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        await redis.xadd(
            "events:reservation",
            {"reservation_id": reservation.id, "user_id": current_user["sub"], "quantity": req.quantity},
        )
    except Exception:
        pass
    return {
        "status": "pending_approval",
        "reservation_id": reservation.id,
        "expires_at": reservation.expires_at,
        "expired_reservations_processed": expired,
    }
