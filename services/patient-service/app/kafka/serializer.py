import json
from typing import Any
from app.kafka.schemas import PatientEvent

class EventSerializer:
    """
    Handles serialization of PatientEvent models to bytes for Kafka.
    """
    @staticmethod
    def serialize(event: PatientEvent) -> bytes:
        """
        Convert a PatientEvent model into JSON-encoded bytes.
        """
        # Convert model to dict, then use json.dumps
        # We use model_dump(mode='json') to handle UUIDs and datetimes automatically
        event_dict = event.model_dump(mode='json')
        return json.dumps(event_dict).encode('utf-8')
