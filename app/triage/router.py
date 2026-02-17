import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.public.dependencies import get_api_context
from app.public.rate_limit import check_rate_limit

from app.triage.schemas import TriageCreate
from app.triage.service import create_triage


router = APIRouter(
    prefix="/public/triage",
    tags=["Public Triage API"],
)


@router.post(
    "/",
    summary="Criar pré-triagem clínica (API pública)",
    description="""
API pública para pré-triagem estruturada com IA clínica responsável.

Uso típico:
- Sistemas de agenda
- Prontuários eletrônicos
- ERPs clínicos
- Aplicativos próprios de clínicas/consultórios

Autenticação:
- API Key via header Authorization: Bearer <API_KEY>

Rate limit:
- Definido por API key
""",
    status_code=status.HTTP_201_CREATED,
)
def public_triage(
    data: TriageCreate,
    db: Session = Depends(get_db),
    ctx: dict = Depends(get_api_context),
):
    """
    Contrato público estável.

    Campos importantes:
    - external_id: ID do paciente/consulta no sistema externo
    - clinic_type: clinico geral | odonto
    """

    # 🔐 Rate limit
    check_rate_limit(
        api_key_id=ctx["api_key_id"],
        limit_per_minute=ctx["rate_limit"],
    )

    try:
        triage = create_triage(
            db=db,
            tenant_id=ctx["tenant_id"],
            data=data,
            clinic_type=ctx.get("clinic_type"),   # medical | dental
            external_id=data.external_id,          # ID externo do parceiro
            enable_alerts=False,                   # API pública não dispara alertas
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a pré-triagem",
        )

    # 📤 Response pública (contrato estável)
    return {
        "id": triage.id,
        "external_id": triage.external_id,
        "urgencia": triage.urgencia,
        "ai_summary": json.loads(triage.ai_summary),
        "created_at": triage.created_at,
    }
