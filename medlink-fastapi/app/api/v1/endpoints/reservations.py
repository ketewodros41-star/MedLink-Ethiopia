from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import CurrentUserDep, RedisDep, SessionDep
from app.core.security import require_roles
from app.db.models import InventoryItem, Medicine, Pharmacy, Reservation, ReservationStatus
from app.services.audit_service import record_audit_event
from app.services.reservation_service import create_reservation_record, expire_stale_reservations

router = APIRouter()

class ReservationCreate(BaseModel):
    pharmacy_id: str
    medicine_id: str
    quantity: int


class ReservationUpdate(BaseModel):
    status: str

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


@router.get("/mine")
async def get_my_reservations(
    current_user: dict = Depends(require_roles("patient", "admin")),
    db: SessionDep = ...,
):
    stmt = (
        select(Reservation, Medicine, Pharmacy)
        .join(Medicine, Medicine.id == Reservation.medicine_id)
        .join(Pharmacy, Pharmacy.id == Reservation.pharmacy_id)
        .where(Reservation.user_id == current_user["sub"])
        .order_by(Reservation.created_at.desc())
    )
    rows = (await db.execute(stmt)).all()
    return {
        "requested_by": current_user["sub"],
        "results": [
            {
                "reservation_id": reservation.id,
                "status": reservation.status,
                "quantity": reservation.quantity,
                "expires_at": reservation.expires_at,
                "medicine": {
                    "id": medicine.id,
                    "canonical_name": medicine.canonical_name,
                    "strength": medicine.strength,
                    "form": medicine.form,
                },
                "pharmacy": {"id": pharmacy.id, "name": pharmacy.name, "city": pharmacy.city},
            }
            for reservation, medicine, pharmacy in rows
        ],
    }


@router.get("/pharmacy-queue")
async def get_pharmacy_reservations(
    current_user: dict = Depends(require_roles("pharmacist", "admin")),
    db: SessionDep = ...,
):
    pharmacy_id = current_user.get("raw", {}).get("pharmacy_id") or current_user.get("pharmacy_id")
    if not pharmacy_id:
        raise HTTPException(status_code=400, detail="No pharmacy scope found for user")

    stmt = (
        select(Reservation, Medicine)
        .join(Medicine, Medicine.id == Reservation.medicine_id)
        .where(Reservation.pharmacy_id == pharmacy_id)
        .order_by(Reservation.created_at.desc())
    )
    rows = (await db.execute(stmt)).all()
    return {
        "requested_by": current_user["sub"],
        "pharmacy_id": pharmacy_id,
        "results": [
            {
                "reservation_id": reservation.id,
                "patient_id": reservation.user_id,
                "status": reservation.status,
                "quantity": reservation.quantity,
                "expires_at": reservation.expires_at,
                "medicine": {
                    "id": medicine.id,
                    "canonical_name": medicine.canonical_name,
                    "strength": medicine.strength,
                },
            }
            for reservation, medicine in rows
        ],
    }


@router.patch("/{reservation_id}")
async def update_reservation_status(
    reservation_id: str,
    payload: ReservationUpdate,
    current_user: dict = Depends(require_roles("pharmacist", "admin")),
    db: SessionDep = ...,
):
    pharmacy_id = current_user.get("raw", {}).get("pharmacy_id") or current_user.get("pharmacy_id")
    reservation = await db.get(Reservation, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if pharmacy_id and reservation.pharmacy_id != pharmacy_id and "admin" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Reservation is outside your pharmacy scope")

    new_status = payload.status.strip().lower()
    allowed = {
        ReservationStatus.APPROVED.value,
        ReservationStatus.CANCELLED.value,
        ReservationStatus.FULFILLED.value,
        ReservationStatus.EXPIRED.value,
    }
    if new_status not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported reservation status")

    reservation.status = new_status
    if new_status in {ReservationStatus.CANCELLED.value, ReservationStatus.EXPIRED.value}:
        inventory_stmt = select(InventoryItem).where(
            InventoryItem.pharmacy_id == reservation.pharmacy_id,
            InventoryItem.medicine_id == reservation.medicine_id,
        )
        inventory = (await db.execute(inventory_stmt)).scalar_one_or_none()
        if inventory is not None:
            inventory.quantity_reserved = max(inventory.quantity_reserved - reservation.quantity, 0)

    await record_audit_event(
        db,
        event_type=f"Reservation{new_status.title()}",
        actor_id=current_user["sub"],
        aggregate_type="reservation",
        aggregate_id=reservation.id,
        payload={"status": new_status},
    )
    await db.commit()
    return {"status": "updated", "reservation_id": reservation.id, "reservation_status": reservation.status}
