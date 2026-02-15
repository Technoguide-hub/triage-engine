from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.tenants.models import Tenant


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_context(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")

        if not user_id or not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        # 🔍 Busca o tenant no banco
        tenant = (
            db.query(Tenant)
            .filter(Tenant.id == tenant_id)
            .first()
        )

        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant not found",
            )

        return {
            "user_id": user_id,
            "tenant_id": tenant.id,
            "clinic_type": tenant.clinic_type,  # 👈 AQUI ESTÁ O GANHO
            "role": role,
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
