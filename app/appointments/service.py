from sqlalchemy.orm import Session
from app.appointments.models import Appointment
from app.appointments.schemas import AppointmentCreate


def create_appointment(db: Session, tenant_id: str, data: AppointmentCreate):
    appt = Appointment(tenant_id=tenant_id, **data.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


def list_appointments(db: Session, tenant_id: str):
    return db.query(Appointment).filter(Appointment.tenant_id == tenant_id).all()