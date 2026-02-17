import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.public.rate_limit import check_rate_limit
from app.public.api_key_auth import get_api_context
from app.triage.service import create_triage
from app.public.triage.schemas import PublicTriageCreate

router = APIRouter(
    prefix="/v1/triage",
    tags=["Public Triage API"],
)


@router.post(
    "/",
    summary="Create triage (public API)",
    description="Pré-triagem estruturada com IA clínica responsável",
)
def public_triage(
    data: PublicTriageCreate,
    db: Session = Depends(get_db),
    ctx: dict = Depends(get_api_context),
):
    # 🔐 Rate limit
    check_rate_limit(
        api_key_id=ctx["api_key_id"],
        limit_per_minute=ctx["rate_limit"],
    )

    # 🧠 Executa motor (sem efeitos colaterais)
    triage = create_triage(
    db=db,
    tenant_id=ctx["tenant_id"],
    data=data,
    clinic_type=data.clinic_type,
    external_id=data.external_id,
    enable_alerts=False,
)

    return {
        "id": triage.id,
        "external_id": triage.external_id,
        "urgencia": triage.urgencia,
        "ai_summary": json.loads(triage.ai_summary),
        "created_at": triage.created_at,
    }

@router.get("/health")
def health():
    return {"status": "public api online"}
