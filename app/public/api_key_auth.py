from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.public.models import ApiKey
from app.tenants.models import Tenant

# Header padrão de API pública
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_context(
    api_key: str | None = Depends(api_key_header),
    db: Session = Depends(get_db),
) -> dict:
    """
    Autenticação da API pública via header:
        X-API-Key: <api_key>

    Retorna contexto padronizado para routers públicos:
      - tenant_id
      - api_key_id
      - rate_limit (req/min)
      - clinic_type (medical|dental)
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "X-API-Key"},
        )

    record = (
        db.query(ApiKey)
        .filter(ApiKey.key == api_key, ApiKey.is_active.is_(True))
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "X-API-Key"},
        )

    # Resolve clinic_type pelo tenant (motor fica agnóstico)
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == record.tenant_id)
        .first()
    )
    clinic_type = tenant.clinic_type if tenant else "medical"

    return {
        "tenant_id": record.tenant_id,
        "api_key_id": record.id,
        "rate_limit": record.rate_limit_per_minute,
        "clinic_type": clinic_type,
    }
