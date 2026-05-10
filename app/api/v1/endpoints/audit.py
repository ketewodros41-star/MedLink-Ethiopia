from datetime import datetime

from sqlalchemy import select

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import require_roles
from app.db.models import AuditEvent

router = APIRouter()

@router.post("/replay")
async def replay_events(
    event_type: str,
    start_time: str,
    end_time: str,
    current_user: dict = Depends(require_roles("admin")),
    db: SessionDep = ...,
):
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Dates must be ISO formatted") from exc

    stmt = (
        select(AuditEvent)
        .where(AuditEvent.event_type == event_type)
        .where(AuditEvent.created_at >= start_dt)
        .where(AuditEvent.created_at <= end_dt)
        .order_by(AuditEvent.created_at.asc())
    )
    events = list((await db.execute(stmt)).scalars().all())
    return {
        "requested_by": current_user["sub"],
        "replayed_events_count": len(events),
        "status": "completed",
        "events": [
            {
                "event_id": event.id,
                "aggregate_type": event.aggregate_type,
                "aggregate_id": event.aggregate_id,
                "payload": event.payload,
                "created_at": event.created_at,
            }
            for event in events
        ],
    }
