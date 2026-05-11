from datetime import datetime, timedelta
from io import BytesIO

import pytest
from PIL import Image
from sqlalchemy import select

from app.db.models import AuditEvent, InventoryItem, Medicine, Pharmacy, Reservation, SyncOperation
from app.services.seed_service import seed_reference_data

pytestmark = pytest.mark.asyncio


async def load_seed_data(db_session):
    await seed_reference_data(db_session)
    await db_session.commit()


async def test_search_resolves_alias_and_logs_event(client, db_session):
    await load_seed_data(db_session)

    response = await client.get("/api/v1/medicine/search", params={"q": "Panadol"})
    assert response.status_code == 200
    body = response.json()
    assert body["results"][0]["canonical_name"] == "Paracetamol"
    assert body["search_failure"] is False

    events = list((await db_session.execute(select(AuditEvent).where(AuditEvent.event_type == "MedicineSearchPerformed"))).scalars())
    assert len(events) == 1


async def test_inventory_verification_and_reservation_flow(client, db_session):
    await load_seed_data(db_session)
    pharmacy = (await db_session.execute(select(Pharmacy).where(Pharmacy.name == "Tikur Care Pharmacy"))).scalar_one()
    medicine = (await db_session.execute(select(Medicine).where(Medicine.canonical_name == "Paracetamol"))).scalar_one()

    client.user_context["roles"] = ["pharmacist"]
    verify_response = await client.post(
        "/api/v1/inventory/verify",
        json={
            "pharmacy_id": pharmacy.id,
            "medicine_id": medicine.id,
            "action": "set",
            "quantity": 18,
        },
    )
    assert verify_response.status_code == 200

    client.user_context["roles"] = ["patient"]
    reservation_response = await client.post(
        "/api/v1/reservations/",
        json={"pharmacy_id": pharmacy.id, "medicine_id": medicine.id, "quantity": 2},
    )
    assert reservation_response.status_code == 200
    reservation_body = reservation_response.json()
    assert reservation_body["status"] == "pending_approval"

    inventory = (await db_session.execute(select(InventoryItem).where(InventoryItem.pharmacy_id == pharmacy.id, InventoryItem.medicine_id == medicine.id))).scalar_one()
    reservations = list((await db_session.execute(select(Reservation))).scalars())
    assert inventory.quantity_reserved == 2
    assert len(reservations) == 1


async def test_pharmacy_trust_and_counterfeit_views(client, db_session):
    await load_seed_data(db_session)
    pharmacy = (await db_session.execute(select(Pharmacy).where(Pharmacy.name == "Tikur Care Pharmacy"))).scalar_one()
    medicine = (await db_session.execute(select(Medicine).where(Medicine.canonical_name == "Paracetamol"))).scalar_one()

    client.user_context["roles"] = ["pharmacist"]
    trust_response = await client.get(f"/api/v1/trust/{pharmacy.id}/score")
    assert trust_response.status_code == 200
    assert trust_response.json()["score"] > 0

    risk_response = await client.post(
        "/api/v1/counterfeit/analyze-risk",
        params={"pharmacy_id": pharmacy.id, "medicine_id": medicine.id},
    )
    assert risk_response.status_code == 200
    assert 0 <= risk_response.json()["risk_score"] <= 1


async def test_telecom_and_sync_ingestion(client, db_session):
    await load_seed_data(db_session)

    telecom_response = await client.post(
        "/api/v1/telecom/sms-webhook",
        json={"sender_number": "+251900000001", "message": "STOCK AMOX500 14"},
    )
    assert telecom_response.status_code == 200
    assert telecom_response.json()["status"] == "parsed_and_applied"

    sync_response = await client.post(
        "/api/v1/sync/push",
        json={
            "client_id": "edge-device-1",
            "timestamp": datetime.utcnow().isoformat(),
            "operations": [
                {"type": "inventory_snapshot", "payload": {"batch": 1}},
                {"type": "manual_review", "payload": {"prescription_id": "rx-1"}},
            ],
        },
    )
    assert sync_response.status_code == 200
    body = sync_response.json()
    assert body["operations_received"] == 2
    sync_ops = list((await db_session.execute(select(SyncOperation))).scalars())
    assert len(sync_ops) == 2


async def test_audit_replay_returns_time_bounded_events(client, db_session):
    await load_seed_data(db_session)
    pharmacy = (await db_session.execute(select(Pharmacy).where(Pharmacy.name == "Tikur Care Pharmacy"))).scalar_one()
    medicine = (await db_session.execute(select(Medicine).where(Medicine.canonical_name == "Paracetamol"))).scalar_one()

    client.user_context["roles"] = ["pharmacist"]
    await client.post(
        "/api/v1/inventory/verify",
        json={"pharmacy_id": pharmacy.id, "medicine_id": medicine.id, "action": "set", "quantity": 10},
    )

    start = (datetime.utcnow() - timedelta(minutes=5)).isoformat()
    end = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
    client.user_context["roles"] = ["admin"]
    replay_response = await client.post(
        "/api/v1/audit/replay",
        params={"event_type": "InventoryUpdated", "start_time": start, "end_time": end},
    )
    assert replay_response.status_code == 200
    assert replay_response.json()["replayed_events_count"] >= 1


async def test_ocr_upload_produces_signed_url_and_metrics(client, db_session):
    await load_seed_data(db_session)
    client.user_context["roles"] = ["patient"]

    image = Image.new("RGB", (24, 24), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    response = await client.post(
        "/api/v1/ocr/upload",
        files={"file": ("prescription.png", buffer.getvalue(), "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["upload"]["signed_url"].startswith("/api/v1/ocr/files/")

    metrics_response = await client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics = metrics_response.json()
    assert metrics["counters"]["ocr_requests_total"] >= 1


async def test_rbac_blocks_patient_from_inventory_verification(client, db_session):
    await load_seed_data(db_session)
    pharmacy = (await db_session.execute(select(Pharmacy).where(Pharmacy.name == "Tikur Care Pharmacy"))).scalar_one()
    medicine = (await db_session.execute(select(Medicine).where(Medicine.canonical_name == "Paracetamol"))).scalar_one()

    client.user_context["roles"] = ["patient"]
    response = await client.post(
        "/api/v1/inventory/verify",
        json={"pharmacy_id": pharmacy.id, "medicine_id": medicine.id, "action": "set", "quantity": 11},
    )
    assert response.status_code == 403
