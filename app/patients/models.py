from sqlalchemy import Column, String, Date, DateTime
from app.core.database import Base
from datetime import datetime
import uuid


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    document = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    sex = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
