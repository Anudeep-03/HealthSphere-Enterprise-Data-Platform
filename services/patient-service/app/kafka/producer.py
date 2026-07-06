import asyncio
import logging
from aiokafka import AIOKafkaProducer
from app.config.config import settings
from app.kafka.schemas import PatientEvent
from app.kafka.serializer import EventSerializer
from app.utils.logging import logger

class KafkaProducerService:
    """
    Reusable Kafka producer service for publishing patient events.
    Implements a singleton-like pattern for the AIOKafkaProducer instance.
    """
    def __init__(self):
        self.producer: AIOKafkaProducer = None
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = "patient.events"

    async def start(self):
        """
        Initialize and start the AIOKafkaProducer.
        """
        if self.producer is None:
            try:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    client_id="patient-service-producer",
                    # Ensure messages are persisted on at least one broker
                    acks="all"
                )
                await self.producer.start()
                logger.info(f"Kafka Producer started successfully. Connected to {self.bootstrap_servers}")
            except Exception as e:
                logger.error(f"Failed to start Kafka Producer: {str(e)}")
                raise e

    async def stop(self):
        """
        Gracefully stop the AIOKafkaProducer.
        """
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped.")

    async def publish_event(self, event: PatientEvent):
        """
        Publishes a PatientEvent to the 'patient.events' topic.
        Fails gracefully to avoid blocking the main API request.
        """
        if self.producer is None:
            logger.error("Kafka Producer not initialized. Event dropped.")
            return

        try:
            serialized_event = EventSerializer.serialize(event)
            # Use the patient_id (from payload) as the key to ensure
            # all events for a specific patient land on the same partition.
            key = str(event.payload.get("id", "default")).encode('utf-8')

            await self.producer.send_and_wait(self.topic, value=serialized_event, key=key)
            logger.info(f"Event {event.event_type} published successfully. EventID: {event.event_id}")
        except Exception as e:
            # GRACEFUL FAILURE: Log the error but do not raise it.
            # This ensures the API request succeeds if the DB commit was successful.
            logger.error(f"Kafka publish failed for event {event.event_id}: {str(e)}")

# Global instance for dependency injection
kafka_producer = KafkaProducerService()
