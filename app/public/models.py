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

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, nullable=False)

    key = Column(String(128), unique=True, nullable=False)

    is_active = Column(Boolean, default=True)
    rate_limit_per_minute = Column(Integer, default=60)

    created_at = Column(DateTime, server_default=func.now())
    last_used_at = Column(DateTime, nullable=True)
