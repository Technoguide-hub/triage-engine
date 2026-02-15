from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
)
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # 🔗 vínculo com o tenant
    tenant_id = Column(String, index=True, nullable=False)

    # 🔑 chave pública usada pelo cliente
    key = Column(String(128), unique=True, index=True, nullable=False)

    # identificação humana (ex: "Integração Clinica X")
    name = Column(String(100), nullable=False)

    # controle de acesso
    is_active = Column(Boolean, nullable=False, default=True)

    # rate limit
    rate_limit_per_minute = Column(Integer, nullable=False, default=60)

    # auditoria
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    revoked_at = Column(DateTime, nullable=True)