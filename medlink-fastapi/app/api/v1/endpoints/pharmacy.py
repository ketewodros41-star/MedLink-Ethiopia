from sqlalchemy import select

from fastapi import APIRouter, Depends

from app.api.deps import OptionalUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import Pharmacy
from app.services.pharmacy_service import rank_nearby_pharmacies
from app.services.trust_service import build_trust_summary

router = APIRouter()

@router.get("/nearest")
async def get_nearest_pharmacies(
    lat: float, 
    lon: float, 
    radius_km: float = 5.0,
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    results = await rank_nearby_pharmacies(db, lat=lat, lon=lon, radius_km=radius_km)
    return {"status": "ok", "user": current_user["sub"] if current_user else "anonymous", "results": results}


@router.get("/directory")
async def get_pharmacy_directory(
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    pharmacies = list((await db.execute(select(Pharmacy).where(Pharmacy.active.is_(True)).order_by(Pharmacy.name.asc()))).scalars())
    results = []
    for pharmacy in pharmacies:
        trust = await build_trust_summary(db, pharmacy.id)
        results.append(
            {
                "id": pharmacy.id,
                "name": pharmacy.name,
                "city": pharmacy.city,
                "region": pharmacy.region,
                "contact_phone": pharmacy.contact_phone,
                "verified_pharmacist": pharmacy.verified_pharmacist,
                "trust_score": trust["score"],
                "flags": trust["flags"],
            }
        )
    return {"requested_by": current_user["sub"] if current_user else "anonymous", "results": results}
