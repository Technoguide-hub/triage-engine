from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.public.models import ApiKey
from app.tenants.models import Tenant

from app.internal.api_keys.schema import ApiKeyCreate, ApiKeyOut
from app.internal.api_keys.utils import generate_api_key


router = APIRouter(
    prefix="/internal/api-keys",
    tags=["Internal API Keys"],
)


@router.post(
    "/",
    response_model=ApiKeyOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create API Key (internal)",
    description="Cria uma API Key para integração com parceiros",
)
def create_api_key(
    payload: ApiKeyCreate,
    db: Session = Depends(get_db),
):
    """
    Endpoint INTERNO.
    Usado para onboarding de clientes/parceiros.
    """

    # 🔍 Valida tenant
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == payload.tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado",
        )

    # 🔑 Gera API Key
    api_key_value = generate_api_key()

    api_key = ApiKey(
        tenant_id=payload.tenant_id,
        key=api_key_value,
        name=payload.name,
        rate_limit_per_minute=payload.rate_limit_per_minute,
        is_active=True,
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return ApiKeyOut(
    id=str(api_key.id),
    key=api_key.key,
    name=api_key.name,
    tenant_id=str(api_key.tenant_id),
    rate_limit_per_minute=api_key.rate_limit_per_minute,
)
