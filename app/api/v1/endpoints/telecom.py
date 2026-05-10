from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.deps import SessionDep
from app.services.telecom_service import process_stock_command

router = APIRouter()

class TelecomWebhook(BaseModel):
    sender_number: str
    message: str # e.g. "STOCK AMOX500 12"

@router.post("/sms-webhook")
async def handle_sms_inventory_update(
    webhook: TelecomWebhook,
    db: SessionDep = ...,
):
    try:
        result = await process_stock_command(db, sender_number=webhook.sender_number, message=webhook.message)
        await db.commit()
        return result
    except ValueError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
