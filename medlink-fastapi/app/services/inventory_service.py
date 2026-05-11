from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import InventoryItem, InventoryState, Medicine, Pharmacy
from app.services.audit_service import record_audit_event


def derive_inventory_state(quantity_available: int, last_verified_at: datetime | None) -> str:
    if quantity_available <= 0:
        return InventoryState.UNAVAILABLE.value
    if last_verified_at is None:
        return InventoryState.UNVERIFIED.value
    age = datetime.now(timezone.utc) - last_verified_at
    if age <= timedelta(hours=6):
        return InventoryState.RECENTLY_VERIFIED.value
    if age <= timedelta(hours=24):
        return InventoryState.ESTIMATED.value
    return InventoryState.STALE.value


async def verify_inventory_action(
    db: AsyncSession,
    *,
    user_id: str,
    pharmacy_id: str,
    medicine_id: str,
    action: str,
    quantity: int | None,
) -> InventoryItem:
    pharmacy = await db.get(Pharmacy, pharmacy_id)
    medicine = await db.get(Medicine, medicine_id)
    if pharmacy is None or medicine is None:
        raise ValueError("Pharmacy or medicine not found")

    stmt = select(InventoryItem).where(
        InventoryItem.pharmacy_id == pharmacy_id,
        InventoryItem.medicine_id == medicine_id,
    )
    inventory = (await db.execute(stmt)).scalar_one_or_none()
    if inventory is None:
        inventory = InventoryItem(
            pharmacy_id=pharmacy_id,
            medicine_id=medicine_id,
            quantity_available=max(quantity or 0, 0),
        )
        db.add(inventory)

    normalized_action = action.casefold().strip()
    if normalized_action in {"confirm", "verified", "set"} and quantity is not None:
        inventory.quantity_available = max(quantity, 0)
    elif normalized_action == "decrement" and quantity is not None:
        inventory.quantity_available = max(inventory.quantity_available - quantity, 0)
    elif normalized_action == "increment" and quantity is not None:
        inventory.quantity_available += quantity
    elif normalized_action == "mark_unavailable":
        inventory.quantity_available = 0
    else:
        raise ValueError("Unsupported inventory action")

    inventory.verification_count += 1
    inventory.last_verified_at = datetime.now(timezone.utc)
    inventory.last_verified_by = user_id
    freshness_bonus = 0.25 if pharmacy.verified_pharmacist else 0.1
    reliability = pharmacy.stock_reliability_score * 0.4
    availability = 0.35 if inventory.quantity_available > 0 else 0.05
    inventory.confidence_score = min(round(freshness_bonus + reliability + availability, 3), 0.99)
    inventory.state = derive_inventory_state(inventory.quantity_available, inventory.last_verified_at)

    await record_audit_event(
        db,
        event_type="InventoryUpdated",
        actor_id=user_id,
        aggregate_type="inventory_item",
        aggregate_id=inventory.id,
        payload={
            "pharmacy_id": pharmacy_id,
            "medicine_id": medicine_id,
            "action": normalized_action,
            "quantity_available": inventory.quantity_available,
            "confidence_score": inventory.confidence_score,
            "state": inventory.state,
        },
    )
    await db.flush()
    return inventory
