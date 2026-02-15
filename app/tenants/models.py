from sqlalchemy import Column, String
from app.core.database import Base
import uuid


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    clinic_type = Column(
        String,
        nullable=False,
        default="medical",  # medical | dental
    )