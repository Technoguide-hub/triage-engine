from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.public.dependencies import get_api_context
from app.tenants.models import Tenant
from app.public.models import ApiKey
from app.core.tenant import get_current_context
from app.core.permissions import require_role



router = APIRouter(
    prefix="/v1/auth",
    tags=["Public Auth"],
)


@router.get(
    "/status",
    summary="API Key status",
    description="""
Endpoint de onboarding para clientes da API.

Usado para:
- Validar API Key
- Conferir vínculo com tenant
- Ver tipo de clínica (medical | dental)
- Ver limites de uso

Recomendado como primeira chamada após gerar a API Key.
""",
)
def api_key_status(
    db: Session = Depends(get_db),
    ctx: dict = Depends(get_api_context),
):
    """
    Retorna o status completo da API Key ativa.
    """

    api_key: ApiKey = ctx["api_key_record"]

    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == api_key.tenant_id)
        .first()
    )

    clinic_type = tenant.clinic_type if tenant else None

    return {
        "api_key": {
            "id": api_key.id,
            "name": api_key.name,
            "is_active": api_key.is_active,
        },
        "tenant": {
            "id": api_key.tenant_id,
            "clinic_type": clinic_type,
        },
        "limits": {
            "rate_limit_per_minute": api_key.rate_limit_per_minute,
        },
        "usage": {
            "last_used_at": api_key.last_used_at,
        },
        "engine": {
            "triage": True,
            "medical": clinic_type == "medical",
            "dental": clinic_type == "dental",
        },
    }
