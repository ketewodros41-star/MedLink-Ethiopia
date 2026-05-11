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
        Medicine(
            canonical_name="Metformin",
            generic_name="Metformin",
            strength="500mg",
            form="tablet",
            therapeutic_class="Antidiabetic",
            search_vector=normalize_text("Metformin diabetes sugar Glucophage"),
        ),
        Medicine(
            canonical_name="Omeprazole",
            generic_name="Omeprazole",
            strength="20mg",
            form="capsule",
            therapeutic_class="Proton Pump Inhibitor",
            search_vector=normalize_text("Omeprazole Losec stomach acid ulcer"),
        ),
        Medicine(
            canonical_name="Ciprofloxacin",
            generic_name="Ciprofloxacin",
            strength="500mg",
            form="tablet",
            therapeutic_class="Antibiotic",
            search_vector=normalize_text("Ciprofloxacin Cipro antibiotic infection"),
        ),
        Medicine(
            canonical_name="Amlodipine",
            generic_name="Amlodipine",
            strength="5mg",
            form="tablet",
            therapeutic_class="Antihypertensive",
            search_vector=normalize_text("Amlodipine blood pressure hypertension Norvasc"),
        ),
        Medicine(
            canonical_name="Artemether-Lumefantrine",
            generic_name="Artemether + Lumefantrine",
            strength="20mg/120mg",
            form="tablet",
            therapeutic_class="Antimalarial",
            search_vector=normalize_text("Artemether Lumefantrine malaria Coartem AL"),
        ),
    ]
    db.add_all(medicines)
    await db.flush()

    aliases = [
        ("Paracetamol", medicines[0].id, "en"),
        ("Acetaminophen", medicines[0].id, "en"),
        ("PCM", medicines[0].id, "en"),
        ("Panadol", medicines[0].id, "en"),
        ("Amoxicillin", medicines[1].id, "en"),
        ("AMOX500", medicines[1].id, "en"),
        ("Salbutamol", medicines[2].id, "en"),
        ("Ventolin", medicines[2].id, "en"),
        ("blue asthma medicine", medicines[2].id, "en"),
        ("Metformin", medicines[3].id, "en"),
        ("Glucophage", medicines[3].id, "en"),
        ("Omeprazole", medicines[4].id, "en"),
        ("Losec", medicines[4].id, "en"),
        ("Ciprofloxacin", medicines[5].id, "en"),
        ("Cipro", medicines[5].id, "en"),
        ("Amlodipine", medicines[6].id, "en"),
        ("Norvasc", medicines[6].id, "en"),
        ("Coartem", medicines[7].id, "en"),
        ("AL", medicines[7].id, "en"),
        ("malaria medicine", medicines[7].id, "en"),
    ]
    db.add_all(
        [
            MedicineAlias(
                medicine_id=medicine_id,
                alias=alias,
                normalized_alias=normalize_text(alias),
                locale=locale,
            )
            for alias, medicine_id, locale in aliases
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
        Pharmacy(
            name="Piassa Medical Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=9.0227,
            longitude=38.7469,
            contact_phone="+251900000003",
            verified_pharmacist=True,
            response_speed_score=0.85,
            stock_reliability_score=0.83,
            fulfillment_score=0.81,
            counterfeit_risk_score=0.06,
        ),
        Pharmacy(
            name="Kazanchis Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=9.0102,
            longitude=38.7614,
            contact_phone="+251900000004",
            verified_pharmacist=False,
            response_speed_score=0.7,
            stock_reliability_score=0.68,
            fulfillment_score=0.65,
            counterfeit_risk_score=0.12,
        ),
        Pharmacy(
            name="Sarbet Health Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=8.9672,
            longitude=38.7401,
            contact_phone="+251900000005",
            verified_pharmacist=True,
            response_speed_score=0.88,
            stock_reliability_score=0.85,
            fulfillment_score=0.84,
            counterfeit_risk_score=0.04,
        ),
        Pharmacy(
            name="Megenagna Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=9.0205,
            longitude=38.8018,
            contact_phone="+251900000006",
            verified_pharmacist=True,
            response_speed_score=0.75,
            stock_reliability_score=0.72,
            fulfillment_score=0.7,
            counterfeit_risk_score=0.09,
        ),
        Pharmacy(
            name="Jimma Road Community Pharmacy",
            city="Addis Ababa",
            region="Addis Ababa",
            latitude=8.9543,
            longitude=38.7289,
            contact_phone="+251900000007",
            verified_pharmacist=False,
            response_speed_score=0.65,
            stock_reliability_score=0.6,
            fulfillment_score=0.58,
            counterfeit_risk_score=0.15,
        ),
        Pharmacy(
            name="Bishoftu General Pharmacy",
            city="Bishoftu",
            region="Oromia",
            latitude=8.7517,
            longitude=38.9886,
            contact_phone="+251900000008",
            verified_pharmacist=True,
            response_speed_score=0.78,
            stock_reliability_score=0.75,
            fulfillment_score=0.73,
            counterfeit_risk_score=0.07,
        ),
        Pharmacy(
            name="Hawassa Medhanit Pharmacy",
            city="Hawassa",
            region="Sidama",
            latitude=7.0622,
            longitude=38.4767,
            contact_phone="+251900000009",
            verified_pharmacist=True,
            response_speed_score=0.8,
            stock_reliability_score=0.77,
            fulfillment_score=0.76,
            counterfeit_risk_score=0.06,
        ),
        Pharmacy(
            name="Bahir Dar Lake Pharmacy",
            city="Bahir Dar",
            region="Amhara",
            latitude=11.5936,
            longitude=37.3906,
            contact_phone="+251900000010",
            verified_pharmacist=True,
            response_speed_score=0.76,
            stock_reliability_score=0.74,
            fulfillment_score=0.72,
            counterfeit_risk_score=0.08,
        ),
    ]
    db.add_all(pharmacies)
    await db.flush()

    db.add_all(
        [
            # Tikur Care
            InventoryItem(pharmacy_id=pharmacies[0].id, medicine_id=medicines[0].id, quantity_available=80, confidence_score=0.92, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[0].id, medicine_id=medicines[1].id, quantity_available=35, confidence_score=0.85, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[0].id, medicine_id=medicines[3].id, quantity_available=60, confidence_score=0.88, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[0].id, medicine_id=medicines[4].id, quantity_available=45, confidence_score=0.86, state="estimated"),
            # Bole Family
            InventoryItem(pharmacy_id=pharmacies[1].id, medicine_id=medicines[2].id, quantity_available=12, confidence_score=0.78, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[1].id, medicine_id=medicines[5].id, quantity_available=25, confidence_score=0.8, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[1].id, medicine_id=medicines[6].id, quantity_available=40, confidence_score=0.82, state="estimated"),
            # Piassa Medical
            InventoryItem(pharmacy_id=pharmacies[2].id, medicine_id=medicines[0].id, quantity_available=100, confidence_score=0.9, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[2].id, medicine_id=medicines[7].id, quantity_available=30, confidence_score=0.85, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[2].id, medicine_id=medicines[1].id, quantity_available=20, confidence_score=0.75, state="estimated"),
            # Kazanchis
            InventoryItem(pharmacy_id=pharmacies[3].id, medicine_id=medicines[0].id, quantity_available=15, confidence_score=0.55, state="stale"),
            InventoryItem(pharmacy_id=pharmacies[3].id, medicine_id=medicines[4].id, quantity_available=10, confidence_score=0.5, state="stale"),
            # Sarbet Health
            InventoryItem(pharmacy_id=pharmacies[4].id, medicine_id=medicines[3].id, quantity_available=90, confidence_score=0.91, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[4].id, medicine_id=medicines[6].id, quantity_available=55, confidence_score=0.89, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[4].id, medicine_id=medicines[2].id, quantity_available=8, confidence_score=0.8, state="estimated"),
            # Megenagna
            InventoryItem(pharmacy_id=pharmacies[5].id, medicine_id=medicines[5].id, quantity_available=18, confidence_score=0.7, state="estimated"),
            InventoryItem(pharmacy_id=pharmacies[5].id, medicine_id=medicines[7].id, quantity_available=22, confidence_score=0.72, state="estimated"),
            # Jimma Road
            InventoryItem(pharmacy_id=pharmacies[6].id, medicine_id=medicines[0].id, quantity_available=5, confidence_score=0.4, state="unverified"),
            # Bishoftu
            InventoryItem(pharmacy_id=pharmacies[7].id, medicine_id=medicines[7].id, quantity_available=40, confidence_score=0.82, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[7].id, medicine_id=medicines[1].id, quantity_available=28, confidence_score=0.78, state="estimated"),
            # Hawassa
            InventoryItem(pharmacy_id=pharmacies[8].id, medicine_id=medicines[3].id, quantity_available=70, confidence_score=0.84, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[8].id, medicine_id=medicines[6].id, quantity_available=35, confidence_score=0.81, state="recently_verified"),
            # Bahir Dar
            InventoryItem(pharmacy_id=pharmacies[9].id, medicine_id=medicines[7].id, quantity_available=50, confidence_score=0.83, state="recently_verified"),
            InventoryItem(pharmacy_id=pharmacies[9].id, medicine_id=medicines[0].id, quantity_available=60, confidence_score=0.79, state="estimated"),
        ]
    )
