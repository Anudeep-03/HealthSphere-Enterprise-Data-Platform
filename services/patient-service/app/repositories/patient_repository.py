from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.patient import Patient, PatientContact, PatientAddress
from app.repositories.base import BaseRepository
from uuid import UUID
from typing import Optional, List

class PatientRepository(BaseRepository[Patient]):
    def __init__(self, session: AsyncSession):
        super().__init__(Patient, session)

    async def get_with_details(self, patient_id: UUID) -> Optional[Patient]:
        """
        Fetch patient along with contacts and addresses.
        """
        stmt = (
            select(Patient)
            .options(selectinload(Patient.contacts), selectinload(Patient.addresses))
            .where(Patient.id == patient_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_with_details(self) -> List[Patient]:
        """
        List all patients with their details.
        """
        stmt = (
            select(Patient)
            .options(selectinload(Patient.contacts), selectinload(Patient.addresses))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_patient(self, patient_id: UUID, update_data: dict) -> Optional[Patient]:
        """
        Update patient basic information.
        """
        patient = await self.get(patient_id)
        if not patient:
            return None

        for key, value in update_data.items():
            setattr(patient, key, value)

        await self.session.commit()
        await self.session.refresh(patient)
        return patient

    async def update_contacts(self, patient_id: UUID, contacts_data: List[dict]):
        """
        Replace all contacts for a patient.
        """
        # Delete existing contacts first
        await self.session.execute(
            select(PatientContact).where(PatientContact.patient_id == patient_id)
        )
        # In a real implementation, we'd use a bulk delete
        # For simplicity in this microservice, we'll fetch and delete
        existing = await self.session.execute(select(PatientContact).where(PatientContact.patient_id == patient_id))
        for contact in existing.scalars():
            await self.session.delete(contact)

        # Add new contacts
        for data in contacts_data:
            contact = PatientContact(**data, patient_id=patient_id)
            self.session.add(contact)

        await self.session.commit()

    async def update_addresses(self, patient_id: UUID, addresses_data: List[dict]):
        """
        Replace all addresses for a patient.
        """
        existing = await self.session.execute(select(PatientAddress).where(PatientAddress.patient_id == patient_id))
        for addr in existing.scalars():
            await self.session.delete(addr)

        for data in addresses_data:
            addr = PatientAddress(**data, patient_id=patient_id)
            self.session.add(addr)

        await self.session.commit()
