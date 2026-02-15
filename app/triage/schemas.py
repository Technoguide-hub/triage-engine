from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


# ---------------------------
# Entrada (já existe, só referência)
# ---------------------------

class TriageCreate(BaseModel):
    appointment_id: str
    answers: Dict[str, str | int | bool | float]


# ---------------------------
# IA – blocos internos
# ---------------------------

class SOAPBlock(BaseModel):
    S: str = Field(..., description="Subjetivo")
    O: str = Field(..., description="Objetivo")
    A: str = Field(..., description="Avaliação")
    P: str = Field(..., description="Plano")


class AISummary(BaseModel):
    resumo_curto: str
    soap: SOAPBlock
    red_flags: List[str]
    urgencia: Literal["baixa", "media", "alta", "emergencia"]
    perguntas_para_consulta: List[str]


# ---------------------------
# Response principal
# ---------------------------

class TriageOut(BaseModel):
    id: str
    appointment_id: str
    urgencia: Literal["baixa", "media", "alta", "emergencia"]
    ai_summary: AISummary
