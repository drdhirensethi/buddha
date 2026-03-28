from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VisitCreate(BaseModel):
    patient_id: int
    visit_date: datetime
    chief_complaint: str | None = None
    history_of_present_illness: str | None = None
    assessment_summary: str | None = None
    plan: str | None = None
    status: str = "completed"


class VisitRead(BaseModel):
    id: int
    patient_id: int
    provider_id: int
    visit_date: datetime
    chief_complaint: str | None = None
    history_of_present_illness: str | None = None
    assessment_summary: str | None = None
    plan: str | None = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

