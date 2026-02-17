import json
from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.triage.models import TriageSession
from app.triage.schemas import TriageCreate
from app.public.triage.schemas import PublicTriageCreate
from app.triage.ai.orchestrator import generate_triage_summary
from app.notifications.alerts import alert_if_critical
from app.tenants.models import Tenant

SUPPORTED_CLINIC_TYPES = {"clinico geral", "odonto"}

# ---------------------------------------------------------------------
# CREATE TRIAGE (medical + dental | interno + API pública)
# ---------------------------------------------------------------------
def create_triage(
    db: Session,
    tenant_id: str,
    data: Union[TriageCreate, PublicTriageCreate],
    clinic_type: str | None = None,
    external_id: str | None = None,
    enable_alerts: bool = True,
) -> TriageSession:
    """
    Motor central de triagem (agnóstico).
    """

    # 1️⃣ Resolve clinic_type
    clinic_type = clinic_type or "clinico geral"

    if clinic_type not in SUPPORTED_CLINIC_TYPES:
        raise ValueError(
        f"Unsupported clinic_type '{clinic_type}'. "
        f"Supported types: {SUPPORTED_CLINIC_TYPES}"
    )

    # 2️⃣ IA
    ai = generate_triage_summary(
        answers=data.answers,
        clinic_type=clinic_type,
    )

    # 3️⃣ Campos opcionais por contrato
    appointment_id = getattr(data, "appointment_id", None)

    triage = TriageSession(
        tenant_id=tenant_id,
        appointment_id=appointment_id,  # 🔥 agora seguro
        external_id=external_id,
        raw_answers=json.dumps(data.answers, ensure_ascii=False),
        ai_summary=json.dumps(ai.model_dump(), ensure_ascii=False),
        urgencia=ai.urgencia,
    )

    db.add(triage)
    db.commit()
    db.refresh(triage)

    if enable_alerts:
        alert_if_critical(db, tenant_id, triage)

    return triage


# ---------------------------------------------------------------------
# GET TRIAGE BY APPOINTMENT
# ---------------------------------------------------------------------
def get_triage_by_appointment(
    db: Session,
    tenant_id: str,
    appointment_id: str,
) -> TriageSession | None:
    return (
        db.query(TriageSession)
        .filter(
            TriageSession.tenant_id == tenant_id,
            TriageSession.appointment_id == appointment_id,
        )
        .first()
    )


# ---------------------------------------------------------------------
# DASHBOARD – CONTADORES POR URGÊNCIA
# ---------------------------------------------------------------------
def get_urgency_counters(
    db: Session,
    tenant_id: str,
) -> dict[str, int]:
    rows = (
        db.query(TriageSession.urgencia, func.count())
        .filter(TriageSession.tenant_id == tenant_id)
        .group_by(TriageSession.urgencia)
        .all()
    )

    return {urg: count for urg, count in rows}


# ---------------------------------------------------------------------
# DASHBOARD – TRIAGENS MAIS CRÍTICAS
# ---------------------------------------------------------------------
def get_urgent_triages(
    db: Session,
    tenant_id: str,
    limit: int = 10,
):
    return (
        db.query(TriageSession)
        .filter(
            TriageSession.tenant_id == tenant_id,
            TriageSession.urgencia.in_(["alta", "emergencia"]),
        )
        .order_by(
            TriageSession.urgencia.desc(),
            TriageSession.created_at.desc(),
        )
        .limit(limit)
        .all()
    )
