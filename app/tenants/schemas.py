from pydantic import BaseModel

class TenantCreate(BaseModel):
    name: str
    clinic_type: str

class TenantResponse(BaseModel):
    id: str
    name: str
    clinic_type: str

    class Config:
        from_attributes = True
