from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.tenant import get_current_context
from app.patients.schemas import PatientCreate, PatientOut
from app.patients.service import create_patient, list_patients

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientOut)
def create(
    data: PatientCreate,
    db: Session = Depends(get_db),
    ctx=Depends(get_current_context)
):
    return create_patient(db, ctx["tenant_id"], data)


@router.get("/", response_model=list[PatientOut])
def list_all(
    db: Session = Depends(get_db),
    ctx=Depends(get_current_context)
):
    return list_patients(db, ctx["tenant_id"])