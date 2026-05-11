from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import OptionalUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import InventoryItem, Medicine, Pharmacy
from app.services.pharmacy_service import haversine_km
from app.services.meili_service import search_medicine
from app.services.trust_service import build_trust_summary

router = APIRouter()

@router.get("/search")
async def search(
    q: str = Query(..., min_length=2),
    locale: str = "en",
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    actor_id = current_user["sub"] if current_user else "anonymous"
    results = await search_medicine(db, query=q, actor_id=actor_id, locale=locale)
    return {"user": actor_id, **results}


@router.get("/{medicine_id}")
async def get_medicine_detail(
    medicine_id: str,
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    medicine = await db.get(Medicine, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {
        "requested_by": current_user["sub"] if current_user else "anonymous",
        "medicine": {
            "id": medicine.id,
            "canonical_name": medicine.canonical_name,
            "generic_name": medicine.generic_name,
            "strength": medicine.strength,
            "form": medicine.form,
            "therapeutic_class": medicine.therapeutic_class,
            "metadata": medicine.metadata_json,
        },
    }


@router.get("/{medicine_id}/availability")
async def get_medicine_availability(
    medicine_id: str,
    lat: float = 8.9915,
    lon: float = 38.7894,
    radius_km: float = 8.0,
    current_user: OptionalUserDep = ...,
    db: SessionDep = ...,
):
    medicine = await db.get(Medicine, medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")

    stmt = (
        select(InventoryItem, Pharmacy)
        .join(Pharmacy, Pharmacy.id == InventoryItem.pharmacy_id)
        .where(InventoryItem.medicine_id == medicine_id)
        .where(InventoryItem.quantity_available > 0)
    )
    rows = (await db.execute(stmt)).all()
    pharmacies: list[dict] = []
    for inventory, pharmacy in rows:
        distance_km = haversine_km(lat, lon, pharmacy.latitude, pharmacy.longitude)
        if distance_km > radius_km:
            continue
        trust = await build_trust_summary(db, pharmacy.id)
        pharmacies.append(
            {
                "pharmacy_id": pharmacy.id,
                "name": pharmacy.name,
                "city": pharmacy.city,
                "region": pharmacy.region,
                "distance_km": round(distance_km, 2),
                "quantity_available": inventory.quantity_available,
                "state": inventory.state,
                "confidence_score": inventory.confidence_score,
                "trust_score": trust["score"],
                "verified_pharmacist": pharmacy.verified_pharmacist,
            }
        )
    pharmacies.sort(key=lambda item: (-item["trust_score"], item["distance_km"]))
    return {"requested_by": current_user["sub"] if current_user else "anonymous", "medicine_id": medicine_id, "pharmacies": pharmacies}
