from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import AuditEvent, InventoryItem, Reservation, ReservationStatus
from app.services.audit_service import record_audit_event


async def create_reservation_record(
    db: AsyncSession,
    *,
    user_id: str,
    pharmacy_id: str,
    medicine_id: str,
    quantity: int,
) -> Reservation:
    if quantity <= 0 or quantity > settings.MAX_RESERVATION_QTY:
        raise ValueError(f"Reservation quantity must be between 1 and {settings.MAX_RESERVATION_QTY}")

    active_count_stmt = select(func.count(Reservation.id)).where(
        Reservation.user_id == user_id,
        Reservation.status.in_([ReservationStatus.PENDING.value, ReservationStatus.APPROVED.value]),
    )
    active_count = (await db.execute(active_count_stmt)).scalar_one()
    if active_count >= 3:
        raise ValueError("Reservation quota exceeded")

    inventory_stmt = select(InventoryItem).where(
        InventoryItem.pharmacy_id == pharmacy_id,
        InventoryItem.medicine_id == medicine_id,
    )
    inventory = (await db.execute(inventory_stmt)).scalar_one_or_none()
    if inventory is None or inventory.quantity_available - inventory.quantity_reserved < quantity:
        raise ValueError("Insufficient verified inventory")

    inventory.quantity_reserved += quantity
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.DEFAULT_RESERVATION_WINDOW_MINUTES)
    reservation = Reservation(
        user_id=user_id,
        pharmacy_id=pharmacy_id,
        medicine_id=medicine_id,
        quantity=quantity,
        approval_required=not bool(inventory.last_verified_by),
        expires_at=expires_at,
    )
    db.add(reservation)
    await db.flush()

    await record_audit_event(
        db,
        event_type="ReservationCreated",
        actor_id=user_id,
        aggregate_type="reservation",
        aggregate_id=reservation.id,
        payload={
            "pharmacy_id": pharmacy_id,
            "medicine_id": medicine_id,
            "quantity": quantity,
            "expires_at": expires_at.isoformat(),
        },
    )
    return reservation


async def expire_stale_reservations(db: AsyncSession) -> int:
    stmt = select(Reservation).where(
        Reservation.status == ReservationStatus.PENDING.value,
        Reservation.expires_at < datetime.now(timezone.utc),
    )
    reservations = list((await db.execute(stmt)).scalars().all())
    for reservation in reservations:
        reservation.status = ReservationStatus.EXPIRED.value
        inventory_stmt = select(InventoryItem).where(
            InventoryItem.pharmacy_id == reservation.pharmacy_id,
            InventoryItem.medicine_id == reservation.medicine_id,
        )
        inventory = (await db.execute(inventory_stmt)).scalar_one_or_none()
        if inventory is not None:
            inventory.quantity_reserved = max(inventory.quantity_reserved - reservation.quantity, 0)
        await record_audit_event(
            db,
            event_type="ReservationExpired",
            actor_id="system",
            aggregate_type="reservation",
            aggregate_id=reservation.id,
            payload={"user_id": reservation.user_id},
        )
    return len(reservations)
