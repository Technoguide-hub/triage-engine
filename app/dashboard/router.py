from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.tenant import get_current_context
from app.dashboard.service import get_odonto_dashboard
from app.core.permissions import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/odonto")
def odonto_dashboard(
    db: Session = Depends(get_db),
    ctx=Depends(require_role("dentista", "admin")),
):
    return get_odonto_dashboard(db, ctx["tenant_id"])
