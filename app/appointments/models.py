from sqlalchemy import Column, String, DateTime, ForeignKey
from app.core.database import Base
import uuid
from datetime import datetime


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True, nullable=False)

    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)

    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")  # scheduled | confirmed | canceled | done
    created_at = Column(DateTime, default=datetime.utcnow)