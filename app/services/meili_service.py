from __future__ import annotations

import meilisearch
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.metrics import metrics_registry
from app.db.models import Medicine, MedicineAlias
from app.services.audit_service import record_audit_event
from app.services.text_utils import normalize_text

client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)


def get_medicine_index():
    return client.index("medicines")


async def search_medicine(
    db: AsyncSession,
    *,
    query: str,
    actor_id: str,
    locale: str = "en",
) -> dict:
    normalized = normalize_text(query)
    alias_stmt = (
        select(MedicineAlias, Medicine)
        .join(Medicine, MedicineAlias.medicine_id == Medicine.id)
        .where(
            or_(
                MedicineAlias.normalized_alias.contains(normalized),
                Medicine.search_vector.contains(normalized),
            )
        )
        .limit(settings.SEARCH_RESULT_LIMIT)
    )
    rows = (await db.execute(alias_stmt)).all()

    results: list[dict] = []
    seen: set[str] = set()
    for alias, medicine in rows:
        if medicine.id in seen:
            continue
        seen.add(medicine.id)
        results.append(
            {
                "medicine_id": medicine.id,
                "canonical_name": medicine.canonical_name,
                "generic_name": medicine.generic_name,
                "strength": medicine.strength,
                "form": medicine.form,
                "matched_alias": alias.alias,
                "locale": alias.locale,
            }
        )

    meili_results: dict | None = None
    if settings.MEILI_ENABLED:
        try:
            meili_results = get_medicine_index().search(query, {"limit": settings.SEARCH_RESULT_LIMIT})
        except Exception:
            meili_results = None

    await record_audit_event(
        db,
        event_type="MedicineSearchPerformed",
        actor_id=actor_id,
        aggregate_type="medicine_search",
        aggregate_id=normalized or "empty",
        payload={
            "query": query,
            "locale": locale,
            "normalized_query": normalized,
            "db_hits": len(results),
            "meili_hits": len(meili_results.get("hits", [])) if meili_results else 0,
        },
    )
    metrics_registry.incr("medicine_search_total")
    if len(results) == 0:
        metrics_registry.incr("medicine_search_failures_total")
    return {
        "query": query,
        "normalized_query": normalized,
        "results": results,
        "search_failure": len(results) == 0,
        "meilisearch": meili_results,
    }
