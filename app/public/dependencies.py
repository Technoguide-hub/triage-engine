from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.public.models import ApiKey

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)

def get_api_context(
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db),
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key ausente",
        )

    record = (
        db.query(ApiKey)
        .filter(
            ApiKey.key == api_key,
            ApiKey.is_active.is_(True),
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida ou revogada",
        )

    # auditoria leve
    record.last_used_at = datetime.utcnow()
    db.commit()

    return {
        "api_key_id": record.id,
        "tenant_id": record.tenant_id,
        "rate_limit": record.rate_limit_per_minute,
        "api_key_record": record,   # 🔥 ISSO RESOLVE TUDO
    }
