from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Any, Dict

class PatientEvent(BaseModel):
    """
    Standard event schema for all patient-related events.
    """
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(..., description="The type of event (e.g., patient.created, patient.updated, patient.deleted)")
    event_version: str = Field("1.0", description="Version of the event schema")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_service: str = Field("patient-service", description="The service that produced the event")
    correlation_id: UUID = Field(..., description="ID to track the request across microservices")
    payload: Dict[str, Any] = Field(..., description="The actual data associated with the event")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary, ensuring UUIDs and datetimes are stringified.
        """
        return self.model_dump()
