from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import InventoryItem, Pharmacy
from app.services.trust_service import build_trust_summary


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * radius * asin(sqrt(a))


async def rank_nearby_pharmacies(db: AsyncSession, *, lat: float, lon: float, radius_km: float) -> list[dict]:
    pharmacies = list((await db.execute(select(Pharmacy).where(Pharmacy.active.is_(True)))).scalars().all())
    ranked: list[dict] = []
    for pharmacy in pharmacies:
        distance_km = haversine_km(lat, lon, pharmacy.latitude, pharmacy.longitude)
        if distance_km > radius_km:
            continue

        trust = await build_trust_summary(db, pharmacy.id)
        inventory_confidence = trust["components"]["inventory_confidence"]
        distance_factor = max(0.0, 1 - (distance_km / max(radius_km, 1)))
        smart_rank = round(
            trust["score"] * 0.65 + distance_factor * 100 * 0.2 + inventory_confidence * 100 * 0.15,
            2,
        )
        ranked.append(
            {
                "pharmacy_id": pharmacy.id,
                "name": pharmacy.name,
                "city": pharmacy.city,
                "region": pharmacy.region,
                "distance_km": round(distance_km, 2),
                "trust_score": trust["score"],
                "inventory_confidence": round(inventory_confidence * 100, 2),
                "smart_rank": smart_rank,
                "verified_pharmacist": pharmacy.verified_pharmacist,
            }
        )
    ranked.sort(key=lambda row: (-row["smart_rank"], row["distance_km"]))
    return ranked
