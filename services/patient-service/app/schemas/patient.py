from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
import re

# Regular expression for phone validation (simple global format)
PHONE_REGEX = re.compile(r"^\+?1?\d{9,15}$")

class PatientContactBase(BaseModel):
    contact_type: str = Field(..., description="Type of contact, e.g., Mobile, Email, Home")
    contact_value: str = Field(..., description="The contact value (email or phone number)")
    is_primary: Optional[bool] = False

    @field_validator("contact_value")
    @classmethod
    def validate_contact_value(cls, v, info):
        # If contact_type is Email, validate as email. If Phone, validate as phone.
        # This requires access to other fields, which is tricky in standard field_validators.
        # We will handle it in a model-level validator or by separate schemas if needed.
        return v

class PatientAddressBase(BaseModel):
    address_line1: str = Field(..., min_length=1)
    address_line2: Optional[str] = None
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    zip_code: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    is_primary: Optional[bool] = False

class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Optional[str] = Field(None, max_length=20)
    blood_group: Optional[str] = Field(None, max_length=5)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

class PatientCreate(PatientBase):
    contacts: List[PatientContactBase] = []
    addresses: List[PatientAddressBase] = []

    @field_validator("contacts")
    @classmethod
    def validate_contacts(cls, v):
        for contact in v:
            if contact.contact_type.lower() == "email":
                # Simple email regex check as we are in a list of objects
                if not re.match(r"[^@]+@[^@]+\.[^@]+", contact.contact_value):
                    raise ValueError(f"Invalid email format for contact: {contact.contact_value}")
            elif contact.contact_type.lower() == "phone":
                if not PHONE_REGEX.match(contact.contact_value):
                    raise ValueError(f"Invalid phone format for contact: {contact.contact_value}")
        return v

class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)
    blood_group: Optional[str] = Field(None, max_length=5)
    contacts: Optional[List[PatientContactBase]] = None
    addresses: Optional[List[PatientAddressBase]] = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        if v and v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

class PatientContactRead(BaseModel):
    id: UUID
    contact_type: str
    contact_value: str
    is_primary: bool

    class Config:
        from_attributes = True

class PatientAddressRead(BaseModel):
    id: UUID
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    zip_code: str
    country: str
    is_primary: bool

    class Config:
        from_attributes = True

class PatientRead(PatientBase):
    id: UUID
    created_at: str
    updated_at: str
    contacts: List[PatientContactRead] = []
    addresses: List[PatientAddressRead] = []

    class Config:
        from_attributes = True
