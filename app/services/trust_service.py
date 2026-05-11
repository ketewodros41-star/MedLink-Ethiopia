from __future__ import annotations

from sqlalchemy import Select, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CommunityStockReport, InventoryItem, Pharmacy


async def build_trust_summary(db: AsyncSession, pharmacy_id: str) -> dict:
    pharmacy = await db.get(Pharmacy, pharmacy_id)
    if pharmacy is None:
        raise ValueError("Pharmacy not found")

    inventory_stmt: Select[tuple[float | None]] = select(func.avg(InventoryItem.confidence_score)).where(
        InventoryItem.pharmacy_id == pharmacy_id
    )
    report_stmt = select(
        func.count(CommunityStockReport.id),
        func.sum(case((CommunityStockReport.is_available.is_(True), 1), else_=0)),
    ).where(CommunityStockReport.pharmacy_id == pharmacy_id)

    avg_confidence = (await db.execute(inventory_stmt)).scalar_one_or_none() or 0.0
    total_reports, positive_reports = (await db.execute(report_stmt)).one()
    total_reports = total_reports or 0
    positive_reports = positive_reports or 0
    community_ratio = positive_reports / total_reports if total_reports else 0.5

    weighted_score = (
        pharmacy.response_speed_score * 0.2
        + pharmacy.stock_reliability_score * 0.25
        + pharmacy.fulfillment_score * 0.2
        + avg_confidence * 0.25
        + community_ratio * 0.1
    )
    final_score = round(weighted_score * 100, 2)

    flags: list[str] = []
    if pharmacy.counterfeit_risk_score >= 0.25:
        flags.append("counterfeit_risk_elevated")
    if avg_confidence < 0.45:
        flags.append("inventory_low_confidence")
    if total_reports >= 3 and community_ratio < 0.45:
        flags.append("community_trust_declining")

    return {
        "pharmacy_id": pharmacy.id,
        "score": final_score,
        "components": {
            "response_speed": pharmacy.response_speed_score,
            "stock_reliability": pharmacy.stock_reliability_score,
            "fulfillment": pharmacy.fulfillment_score,
            "inventory_confidence": round(avg_confidence, 3),
            "community_ratio": round(community_ratio, 3),
        },
        "flags": flags,
    }
