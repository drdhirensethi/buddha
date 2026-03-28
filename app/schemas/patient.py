from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.medication import MedicationRead
from app.schemas.visit import VisitRead


class PatientBase(BaseModel):
    patient_code: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    sex: str = Field(min_length=1, max_length=20)
    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    address: str | None = None
    emergency_contact_name: str | None = Field(default=None, max_length=255)
    emergency_contact_phone: str | None = Field(default=None, max_length=30)
    primary_caregiver_name: str | None = Field(default=None, max_length=255)
    primary_caregiver_phone: str | None = Field(default=None, max_length=30)


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: date | None = None
    sex: str | None = Field(default=None, min_length=1, max_length=20)
    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None
    address: str | None = None
    emergency_contact_name: str | None = Field(default=None, max_length=255)
    emergency_contact_phone: str | None = Field(default=None, max_length=30)
    primary_caregiver_name: str | None = Field(default=None, max_length=255)
    primary_caregiver_phone: str | None = Field(default=None, max_length=30)


class PatientListItem(BaseModel):
    id: int
    patient_code: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PatientRead(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    visits: list[VisitRead] = Field(default_factory=list)
    medications: list[MedicationRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
