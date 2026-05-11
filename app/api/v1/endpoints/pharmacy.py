from fastapi import APIRouter, Depends

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.services.pharmacy_service import rank_nearby_pharmacies

router = APIRouter()

@router.get("/nearest")
async def get_nearest_pharmacies(
    lat: float, 
    lon: float, 
    radius_km: float = 5.0,
    current_user: dict = Depends(require_roles("patient", "pharmacist", "admin")),
    db: SessionDep = ...,
):
    results = await rank_nearby_pharmacies(db, lat=lat, lon=lon, radius_km=radius_km)
    return {"status": "ok", "user": current_user["sub"], "results": results}
