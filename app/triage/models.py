from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class TriageSession(Base):
    __tablename__ = "triage_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True, nullable=False)

    # 🔁 NÃO é mais obrigatório
    appointment_id = Column(String, nullable=True)

    # 🔑 API pública
    external_id = Column(String, nullable=True)

    raw_answers = Column(String, nullable=False)
    ai_summary = Column(String, nullable=False)
    urgencia = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,)
