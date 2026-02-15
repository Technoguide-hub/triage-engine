from pydantic import BaseModel, Field
from typing import Optional


class ApiKeyCreate(BaseModel):
    tenant_id: str = Field(..., description="ID do tenant dono da API key")
    name: str = Field(..., description="Nome identificador da chave")
    rate_limit_per_minute: int = Field(
        default=60,
        description="Limite de requisições por minuto",
    )


class ApiKeyOut(BaseModel):
    id: str
    key: str
    name: str
    tenant_id: str
    rate_limit_per_minute: int
