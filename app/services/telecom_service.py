from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import MedicineAlias, Pharmacy
from app.services.inventory_service import verify_inventory_action
from app.services.text_utils import normalize_text


@dataclass
class ParsedStockCommand:
    action: str
    alias: str
    quantity: int


def parse_stock_command(message: str) -> ParsedStockCommand:
    parts = message.strip().split()
    if len(parts) != 3 or parts[0].casefold() != "stock":
        raise ValueError("Unsupported telecom command format")
    quantity = int(parts[2])
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    return ParsedStockCommand(action="set", alias=parts[1], quantity=quantity)


async def process_stock_command(db: AsyncSession, *, sender_number: str, message: str) -> dict:
    pharmacy_stmt = select(Pharmacy).where(Pharmacy.contact_phone == sender_number)
    pharmacy = (await db.execute(pharmacy_stmt)).scalar_one_or_none()
    if pharmacy is None:
        raise ValueError("Sender is not linked to a pharmacy")

    command = parse_stock_command(message)
    alias_stmt = select(MedicineAlias).where(MedicineAlias.normalized_alias == normalize_text(command.alias))
    alias = (await db.execute(alias_stmt)).scalar_one_or_none()
    if alias is None:
        raise ValueError("Medicine alias not recognized")

    inventory = await verify_inventory_action(
        db,
        user_id=f"telecom:{sender_number}",
        pharmacy_id=pharmacy.id,
        medicine_id=alias.medicine_id,
        action=command.action,
        quantity=command.quantity,
    )
    return {
        "status": "parsed_and_applied",
        "pharmacy_id": pharmacy.id,
        "medicine_id": alias.medicine_id,
        "quantity_available": inventory.quantity_available,
    }
