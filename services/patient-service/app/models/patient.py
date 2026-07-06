from sqlalchemy import Column, String, Date, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.session import Base

# Define the schema for the tables
__table_args__ = {"schema": "patient_schema"}

class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = __table_args__

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    blood_group: Mapped[str] = mapped_column(String(5), nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False) # Using String for simplicity or DateTime if preferred
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    contacts: Mapped[list["PatientContact"]] = relationship("PatientContact", back_populates="patient", cascade="all, delete-orphan")
    addresses: Mapped[list["PatientAddress"]] = relationship("PatientAddress", back_populates="patient", cascade="all, delete-orphan")

class PatientContact(Base):
    __tablename__ = "patient_contacts"
    __table_args__ = __table_args__

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patient_schema.patients.id", ondelete="CASCADE"), nullable=False)
    contact_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g., Mobile, Email, Home
    contact_value: Mapped[str] = mapped_column(String(255), nullable=False)
    is_primary: Mapped[bool] = mapped_column(nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="contacts")

class PatientAddress(Base):
    __tablename__ = "patient_addresses"
    __table_args__ = __table_args__

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patient_schema.patients.id", ondelete="CASCADE"), nullable=False)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    is_primary: Mapped[bool] = mapped_column(nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="addresses")
