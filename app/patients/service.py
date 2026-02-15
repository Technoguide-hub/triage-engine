from sqlalchemy.orm import Session
from app.patients.models import Patient
from app.patients.schemas import PatientCreate


def create_patient(db: Session, tenant_id: str, data: PatientCreate):
    patient = Patient(tenant_id=tenant_id, **data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def list_patients(db: Session, tenant_id: str):
    return db.query(Patient).filter(Patient.tenant_id == tenant_id).all()