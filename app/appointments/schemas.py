from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: str
    scheduled_at: datetime


class AppointmentOut(AppointmentCreate):
    id: str
    status: str

    class Config:
        from_attributes = True