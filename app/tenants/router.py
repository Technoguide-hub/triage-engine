from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.tenants.models import Tenant
from app.core.tenant import get_current_context

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.get("/me")
def get_my_tenant(
    ctx=Depends(get_current_context),
    db: Session = Depends(get_db)
):
    return db.query(Tenant).filter(Tenant.id == ctx["tenant_id"]).first()