from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AuditEvent


async def record_audit_event(
    db: AsyncSession,
    *,
    event_type: str,
    actor_id: str,
    aggregate_type: str,
    aggregate_id: str,
    payload: Mapping[str, object],
) -> AuditEvent:
    event = AuditEvent(
        event_type=event_type,
        actor_id=actor_id,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        payload=dict(payload),
    )
    db.add(event)
    await db.flush()
    return event
