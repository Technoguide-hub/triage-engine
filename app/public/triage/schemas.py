from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from typing import Literal


class PublicTriageCreate(BaseModel):
    clinic_type: str = Field(..., description="Tipo da clínica (ex: clinico geral, odonto)")
    external_id: str = Field(..., description="ID externo do paciente no sistema cliente")
    answers: Dict

    class Config:
        json_schema_extra = {
            "example": {
                "clinic_type": "clinico geral",
                "external_id": "patient_123",
                "answers": {
                    "queixa_principal": "Dor abdominal",
                    "inicio": "há 2 dias",
                    "febre": True
                }
            }
        }
    answers: Dict[str, Any] = Field(
        ...,
        description="Respostas estruturadas da pré-triagem",
        example={
            "queixa_principal": "Dor forte no dente",
            "inicio": "há 2 dias",
            "intensidade": "8/10"
        }
    )
    
