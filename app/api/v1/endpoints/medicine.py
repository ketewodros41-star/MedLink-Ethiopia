from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.services.meili_service import search_medicine

router = APIRouter()

@router.get("/search")
async def search(
    q: str = Query(..., min_length=2),
    locale: str = "en",
    current_user: dict = Depends(require_roles("patient", "pharmacist", "admin")),
    db: SessionDep = ...,
):
    results = await search_medicine(db, query=q, actor_id=current_user["sub"], locale=locale)
    return {"user": current_user["sub"], **results}
