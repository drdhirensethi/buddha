from datetime import date

from pydantic import BaseModel, ConfigDict


class MedicationRead(BaseModel):
    id: int
    name: str
    dose: str | None = None
    frequency: str | None = None
    route: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    adherence_notes: str | None = None
    active: bool

    model_config = ConfigDict(from_attributes=True)

