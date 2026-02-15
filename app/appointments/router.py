from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.tenant import get_current_context
from app.appointments.schemas import AppointmentCreate, AppointmentOut
from app.appointments.service import create_appointment, list_appointments
from app.core.permissions import require_role

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentOut)
def create(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    ctx=Depends(require_role("recepcao", "admin"))
):
    return create_appointment(db, ctx["tenant_id"], data)


@router.get("/", response_model=list[AppointmentOut])
def list_all(
    db: Session = Depends(get_db),
    ctx=Depends(get_current_context)
):
    return list_appointments(db, ctx["tenant_id"])