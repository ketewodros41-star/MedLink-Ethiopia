from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SyncOperation, SyncStatus
from app.services.audit_service import record_audit_event


async def queue_sync_operations(
    db: AsyncSession,
    *,
    user_id: str,
    client_id: str,
    operations: list[dict],
) -> list[SyncOperation]:
    created: list[SyncOperation] = []
    for operation in operations:
        op_type = str(operation.get("type", "unknown"))
        payload = operation.get("payload", {})
        status = SyncStatus.APPLIED.value if op_type in {"inventory_snapshot", "reservation_ping"} else SyncStatus.QUEUED.value
        sync_op = SyncOperation(
            client_id=client_id,
            user_id=user_id,
            operation_type=op_type,
            payload=payload,
            status=status,
        )
        db.add(sync_op)
        await db.flush()
        created.append(sync_op)
        await record_audit_event(
            db,
            event_type="OfflineSyncQueued",
            actor_id=user_id,
            aggregate_type="sync_operation",
            aggregate_id=sync_op.id,
            payload={"client_id": client_id, "operation_type": op_type, "status": status},
        )
    return created
