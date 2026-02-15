from pydantic import BaseModel

class TenantOut(BaseModel):
    id: str
    name: str
    clinic_type: str

    class Config:
        from_attributes = True