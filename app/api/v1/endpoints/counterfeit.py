from sqlalchemy import func, select

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import CommunityStockReport, InventoryItem, Pharmacy

router = APIRouter()

@router.post("/analyze-risk")
async def analyze_counterfeit_risk(
    pharmacy_id: str,
    medicine_id: str,
    current_user: dict = Depends(require_roles("pharmacist", "admin")),
    db: SessionDep = ...,
):
    pharmacy = await db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    inventory_stmt = select(InventoryItem).where(
        InventoryItem.pharmacy_id == pharmacy_id,
        InventoryItem.medicine_id == medicine_id,
    )
    inventory = (await db.execute(inventory_stmt)).scalar_one_or_none()
    negative_reports_stmt = select(func.count(CommunityStockReport.id)).where(
        CommunityStockReport.pharmacy_id == pharmacy_id,
        CommunityStockReport.medicine_id == medicine_id,
        CommunityStockReport.is_available.is_(False),
    )
    negative_reports = (await db.execute(negative_reports_stmt)).scalar_one()
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    risk_score = round(
        pharmacy.counterfeit_risk_score * 0.5
        + (1 - inventory.confidence_score) * 0.35
        + min(negative_reports * 0.05, 0.15),
        3,
    )
    flags: list[str] = []
    if inventory.confidence_score < 0.5:
        flags.append("low_inventory_confidence")
    if negative_reports >= 2:
        flags.append("repeat_negative_community_signals")
    if pharmacy.counterfeit_risk_score >= 0.2:
        flags.append("pharmacy_profile_high_risk")

    return {"requested_by": current_user["sub"], "risk_score": risk_score, "flags": flags}
