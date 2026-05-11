from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import OptionalUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import CommunityStockReport, Medicine, Pharmacy
from app.services.audit_service import record_audit_event

router = APIRouter()

class CommunityReport(BaseModel):
    medicine_id: str
    pharmacy_id: str
    is_available: bool
    photo_proof_url: str | None = None
    notes: str | None = None

@router.post("/report")
async def submit_stock_report(
    report: CommunityReport,
    current_user: dict = Depends(require_roles("patient", "pharmacist", "admin")),
    db: SessionDep = ...,
):
    if not report.is_available and not report.notes:
        raise HTTPException(status_code=400, detail="Unavailable reports must include notes")

    community_report = CommunityStockReport(
        user_id=current_user["sub"],
        medicine_id=report.medicine_id,
        pharmacy_id=report.pharmacy_id,
        is_available=report.is_available,
        photo_proof_url=report.photo_proof_url,
        notes=report.notes,
        reputation_weight=0.8 if report.photo_proof_url else 0.55,
    )
    db.add(community_report)
    await db.flush()
    await record_audit_event(
        db,
        event_type="CommunityReportSubmitted",
        actor_id=current_user["sub"],
        aggregate_type="community_stock_report",
        aggregate_id=community_report.id,
        payload={"pharmacy_id": report.pharmacy_id, "medicine_id": report.medicine_id, "is_available": report.is_available},
    )
    await db.commit()
    return {"status": "received", "report_id": community_report.id}


@router.get("/feed")
async def get_community_feed(
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    stmt = (
        select(CommunityStockReport, Medicine, Pharmacy)
        .join(Medicine, Medicine.id == CommunityStockReport.medicine_id)
        .join(Pharmacy, Pharmacy.id == CommunityStockReport.pharmacy_id)
        .order_by(CommunityStockReport.created_at.desc())
        .limit(20)
    )
    rows = (await db.execute(stmt)).all()
    return {
        "requested_by": current_user["sub"] if current_user else "anonymous",
        "results": [
            {
                "report_id": report.id,
                "user_id": report.user_id,
                "is_available": report.is_available,
                "notes": report.notes,
                "photo_proof_url": report.photo_proof_url,
                "reputation_weight": report.reputation_weight,
                "created_at": report.created_at,
                "medicine": {"id": medicine.id, "canonical_name": medicine.canonical_name},
                "pharmacy": {"id": pharmacy.id, "name": pharmacy.name, "city": pharmacy.city},
            }
            for report, medicine, pharmacy in rows
        ],
    }
