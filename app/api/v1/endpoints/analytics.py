from sqlalchemy import func, select

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import AuditEvent, CommunityStockReport, InventoryItem, Pharmacy, Reservation

router = APIRouter()

@router.get("/shortages")
async def regional_shortages(current_user: dict = Depends(require_roles("pharmacist", "admin")), db: SessionDep = ...):
    shortage_stmt = (
        select(Pharmacy.region, func.count(InventoryItem.id))
        .join(Pharmacy, Pharmacy.id == InventoryItem.pharmacy_id)
        .where(InventoryItem.quantity_available <= 5)
        .group_by(Pharmacy.region)
    )
    search_failure_stmt = (
        select(AuditEvent.payload)
        .where(AuditEvent.event_type == "MedicineSearchPerformed")
        .order_by(AuditEvent.created_at.desc())
        .limit(20)
    )
    shortages = [
        {"region": region, "low_stock_items": count}
        for region, count in (await db.execute(shortage_stmt)).all()
    ]
    failures = [
        payload["query"]
        for payload in (await db.execute(search_failure_stmt)).scalars().all()
        if payload.get("db_hits") == 0
    ]
    return {"region_breakdown": shortages, "recent_search_failures": failures, "requested_by": current_user["sub"]}

@router.get("/heatmaps")
async def get_heatmaps(current_user: dict = Depends(require_roles("pharmacist", "admin")), db: SessionDep = ...):
    reservation_stmt = (
        select(Pharmacy.latitude, Pharmacy.longitude, func.count(Reservation.id))
        .join(Reservation, Reservation.pharmacy_id == Pharmacy.id)
        .group_by(Pharmacy.id)
    )
    report_stmt = (
        select(Pharmacy.latitude, Pharmacy.longitude, func.count(CommunityStockReport.id))
        .join(CommunityStockReport, CommunityStockReport.pharmacy_id == Pharmacy.id)
        .group_by(Pharmacy.id)
    )
    reservation_points = [
        {"lat": lat, "lon": lon, "weight": weight, "source": "reservations"}
        for lat, lon, weight in (await db.execute(reservation_stmt)).all()
    ]
    report_points = [
        {"lat": lat, "lon": lon, "weight": weight, "source": "community_reports"}
        for lat, lon, weight in (await db.execute(report_stmt)).all()
    ]
    return {"requested_by": current_user["sub"], "data": reservation_points + report_points}
