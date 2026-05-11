from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import InventoryItem, Medicine, MedicineAlias, Pharmacy
from app.services.text_utils import normalize_text


async def seed_reference_data(db: AsyncSession) -> None:
    count = (await db.execute(select(func.count(Medicine.id)))).scalar_one()
    if count:
        return

    medicines = [
        Medicine(
            canonical_name="Paracetamol",
            generic_name="Acetaminophen",
            strength="500mg",
            form="tablet",
            therapeutic_class="Analgesic",
            search_vector=normalize_text("Paracetamol Acetaminophen PCM Panadol"),
        ),
        Medicine(
            canonical_name="Amoxicillin",
            generic_name="Amoxicillin",
            strength="500mg",
            form="capsule",
            therapeutic_class="Antibiotic",
            search_vector=normalize_text("Amoxicillin AMOX500"),
        ),
        Medicine(
            canonical_name="Salbutamol Inhaler",
            generic_name="Salbutamol",
            strength="100mcg",
            form="inhaler",
            therapeutic_class="Bronchodilator",
            search_vector=normalize_text("Salbutamol Ventolin asthma inhaler blue inhaler"),
        ),
    ]
    db.add_all(medicines)
    await db.flush()

    aliases = [
        ("Paracetamol", "en"),
        ("Acetaminophen", "en"),
        ("PCM", "en"),
        ("Panadol", "en"),
        ("Amoxicillin", "en"),
        ("AMOX500", "en"),
        ("Salbutamol", "en"),
        ("Ventolin", "en"),
        ("blue asthma medicine", "en"),
    ]
    alias_map = {
        "Paracetamol": medicines[0].id,
        "Acetaminophen": medicines[0].id,
        "PCM": medicines[0].id,
        "Panadol": medicines[0].id,
        "Amoxicillin": medicines[1].id,
        "AMOX500": medicines[1].id,
        "Salbutamol": medicines[2].id,
        "Ventolin": medicines[2].id,
        "blue asthma medicine": medicines[2].id,
    }
    db.add_all(
        [
            MedicineAlias(
                medicine_id=alias_map[alias],
                alias=alias,
                normalized_alias=normalize_text(alias),
                locale=locale,
            )
            for alias, locale in aliases
        ]
    )

    pharmacies = [
        Pharmacy(
            name="Tikur Care Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=8.9806,
            longitude=38.7578,
            contact_phone="+251900000001",
            verified_pharmacist=True,
            response_speed_score=0.9,
            stock_reliability_score=0.88,
            fulfillment_score=0.86,
            counterfeit_risk_score=0.05,
        ),
        Pharmacy(
            name="Bole Family Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=8.9915,
            longitude=38.7894,
            contact_phone="+251900000002",
            verified_pharmacist=True,
            response_speed_score=0.82,
            stock_reliability_score=0.8,
            fulfillment_score=0.79,
            counterfeit_risk_score=0.08,
        ),
    ]
    db.add_all(pharmacies)
    await db.flush()

    db.add_all(
        [
            InventoryItem(
                pharmacy_id=pharmacies[0].id,
                medicine_id=medicines[0].id,
                quantity_available=50,
                confidence_score=0.86,
                state="recently_verified",
            ),
            InventoryItem(
                pharmacy_id=pharmacies[0].id,
                medicine_id=medicines[1].id,
                quantity_available=20,
                confidence_score=0.8,
                state="estimated",
            ),
            InventoryItem(
                pharmacy_id=pharmacies[1].id,
                medicine_id=medicines[2].id,
                quantity_available=12,
                confidence_score=0.78,
                state="recently_verified",
            ),
        ]
    )
