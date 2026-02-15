from pydantic import BaseModel
from datetime import date


class PatientCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    birth_date: date | None = None


class PatientOut(PatientCreate):
    id: str

    class Config:
        from_attributes = True