import httpx
from app.core.config import settings

class FHIRClient:
    def __init__(self, token: str):
        self.base_url = f"{settings.MEDPLUM_BASE_URL}/fhir/R4"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json"
        }

    async def get_patient(self, patient_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/Patient/{patient_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
            
    async def get_medication(self, medication_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/Medication/{medication_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
            
    async def get_practitioner(self, practitioner_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/Practitioner/{practitioner_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
