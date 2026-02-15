from fastapi import Depends, HTTPException, status
from app.core.tenant import get_current_context


def require_role(*allowed_roles: str):
    def checker(ctx=Depends(get_current_context)):
        user_role = ctx["role"]

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente"
            )

        return ctx

    return checker