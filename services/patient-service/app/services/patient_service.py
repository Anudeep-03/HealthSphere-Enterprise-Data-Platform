from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate, PatientRead
from app.models.patient import Patient, PatientContact, PatientAddress
from app.utils.exceptions import PatientNotFoundException, DatabaseOperationError
from app.utils.logging import logger
from app.kafka.producer import kafka_producer
from app.kafka.schemas import PatientEvent
import uuid
from typing import List, Optional

class PatientService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = PatientRepository(session)

    async def _publish_patient_event(self, event_type: str, patient_id: uuid.UUID, payload: dict):
        """
        Helper to construct and publish a patient event.
        """
        event = PatientEvent(
            event_type=event_type,
            correlation_id=uuid.uuid4(), # In a real system, this would be passed from the request header
            payload={
                "id": str(patient_id),
                **payload
            }
        )
        await kafka_producer.publish_event(event)

    async def create_patient(self, patient_in: PatientCreate) -> PatientRead:
        try:
            # Create patient base model
            patient_data = patient_in.model_dump(exclude={"contacts", "addresses"})
            patient = Patient(**patient_data)

            # Create the patient first to get the ID
            created_patient = await self.repository.create(patient)
            patient_id = created_patient.id

            # Add contacts
            if patient_in.contacts:
                for contact in patient_in.contacts:
                    contact_obj = PatientContact(**contact.model_dump(), patient_id=patient_id)
                    self.session.add(contact_obj)

            # Add addresses
            if patient_in.addresses:
                for addr in patient_in.addresses:
                    addr_obj = PatientAddress(**addr.model_dump(), patient_id=patient_id)
                    self.session.add(addr_obj)

            await self.session.commit()
            await self.session.refresh(created_patient)

            logger.info(f"Successfully created patient with ID: {patient_id}")

            # PUBLISH EVENT AFTER SUCCESSFUL COMMIT
            await self._publish_patient_event(
                event_type="patient.created",
                patient_id=patient_id,
                payload=patient_in.model_dump()
            )

            # Fetch fully loaded object for response
            full_patient = await self.repository.get_with_details(patient_id)
            return PatientRead.model_validate(full_patient)

        except Exception as e:
            logger.error(f"Error creating patient: {str(e)}")
            raise DatabaseOperationError(f"Could not create patient: {str(e)}")

    async def get_patient(self, patient_id: uuid.UUID) -> PatientRead:
        patient = await self.repository.get_with_details(patient_id)
        if not patient:
            raise PatientNotFoundException(str(patient_id))
        return PatientRead.model_validate(patient)

    async def list_patients(self) -> List[PatientRead]:
        patients = await self.repository.list_with_details()
        return [PatientRead.model_validate(p) for p in patients]

    async def update_patient(self, patient_id: uuid.UUID, patient_in: PatientUpdate) -> PatientRead:
        try:
            # Check if patient exists
            patient = await self.repository.get(patient_id)
            if not patient:
                raise PatientNotFoundException(str(patient_id))

            # Update basic info
            update_data = patient_in.model_dump(exclude_unset=True)
            contacts_data = update_data.pop("contacts", None)
            addresses_data = update_data.pop("addresses", None)

            updated_patient = await self.repository.update_patient(patient_id, update_data)

            # Update contacts if provided
            if contacts_data is not None:
                await self.repository.update_contacts(patient_id, contacts_data)

            # Update addresses if provided
            if addresses_data is not None:
                await self.repository.update_addresses(patient_id, addresses_data)

            logger.info(f"Successfully updated patient with ID: {patient_id}")

            # PUBLISH EVENT AFTER SUCCESSFUL COMMIT
            await self._publish_patient_event(
                event_type="patient.updated",
                patient_id=patient_id,
                payload=patient_in.model_dump(exclude_unset=True)
            )

            full_patient = await self.repository.get_with_details(patient_id)
            return PatientRead.model_validate(full_patient)

        except PatientNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating patient {patient_id}: {str(e)}")
            raise DatabaseOperationError(f"Could not update patient: {str(e)}")

    async def delete_patient(self, patient_id: uuid.UUID) -> bool:
        try:
            success = await self.repository.delete(patient_id)
            if not success:
                raise PatientNotFoundException(str(patient_id))

            logger.info(f"Successfully deleted patient with ID: {patient_id}")

            # PUBLISH EVENT AFTER SUCCESSFUL COMMIT
            await self._publish_patient_event(
                event_type="patient.deleted",
                patient_id=patient_id,
                payload={"status": "deleted"}
            )

            return True
        except PatientNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error deleting patient {patient_id}: {str(e)}")
            raise DatabaseOperationError(f"Could not delete patient: {str(e)}")
