from fastapi import APIRouter, Depends

from app.api.v1.endpoints import (
    medicine, ocr, inventory, sync, trust,
    community, telecom, reservations, pharmacy,
    analytics, counterfeit, audit
)
from app.services.rate_limit_service import enforce_rate_limit

api_router = APIRouter()

@api_router.get("/status")
def status():
    return {"status": "ok", "service": "MedLink Ethiopia Backend", "mode": "production-oriented-foundation"}

# Core AI & Search
api_router.include_router(medicine.router, prefix="/medicine", tags=["medicine"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"], dependencies=[Depends(enforce_rate_limit)])

# Core Inventory & Trust Data
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(trust.router, prefix="/trust", tags=["trust"], dependencies=[Depends(enforce_rate_limit)])

# Ordering & geographic
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(pharmacy.router, prefix="/pharmacy", tags=["pharmacy"], dependencies=[Depends(enforce_rate_limit)])

# Analytics & Advanced features
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(counterfeit.router, prefix="/counterfeit", tags=["counterfeit"], dependencies=[Depends(enforce_rate_limit)])

# Edge connectivity & Logging
api_router.include_router(sync.router, prefix="/sync", tags=["sync"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(telecom.router, prefix="/telecom", tags=["telecom"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(community.router, prefix="/community", tags=["community"], dependencies=[Depends(enforce_rate_limit)])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"], dependencies=[Depends(enforce_rate_limit)])
