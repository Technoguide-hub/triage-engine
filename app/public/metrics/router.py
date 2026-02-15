from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.public.dependencies import get_api_context
from app.public.rate_limit import check_rate_limit
from app.public.metrics.service import get_api_metrics

router = APIRouter(
    prefix="/v1/metrics",
    tags=["Public Metrics API"],
)


@router.get(
    "/",
    summary="Usage metrics by API key",
    description="Métricas de uso da API de pré-triagem",
)
def metrics(
    db: Session = Depends(get_db),
    ctx: dict = Depends(get_api_context),
):
    # 🔐 rate limit também se aplica aqui
    check_rate_limit(
        api_key_id=ctx["api_key_id"],
        limit_per_minute=ctx["rate_limit"],
    )

    return get_api_metrics(
        db=db,
        tenant_id=ctx["tenant_id"],
    )
