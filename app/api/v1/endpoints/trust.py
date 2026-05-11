from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.services.trust_service import build_trust_summary

router = APIRouter()

@router.get("/{pharmacy_id}/score")
async def get_trust_score(
    pharmacy_id: str,
    current_user: dict = Depends(require_roles("pharmacist", "admin")),
    db: SessionDep = ...,
):
    try:
        trust = await build_trust_summary(db, pharmacy_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"requested_by": current_user["sub"], **trust}
