from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App Metadata
    APP_TITLE: str = "HealthSphere Patient Service"
    APP_DESCRIPTION: str = "Enterprise microservice for managing patient demographics and records."
    APP_VERSION: str = "1.0.0"

    # Database Configuration
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")

    # Environment
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # Kafka (Placeholder)
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
