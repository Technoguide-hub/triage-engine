from pydantic import BaseModel, Field
from typing import List, Literal

Urgency = Literal["baixa", "media", "alta", "emergencia"]

class TriageAISummary(BaseModel):
    resumo_curto: str = Field(..., description="Resumo em 2-4 linhas para o médico.")
    soap: dict = Field(..., description="Estrutura SOAP: S, O, A, P (strings).")
    red_flags: List[str] = Field(default_factory=list, description="Sinais de alerta.")
    urgencia: Urgency = Field(..., description="Classificação de urgência.")
    perguntas_para_consulta: List[str] = Field(default_factory=list, description="Perguntas objetivas para o médico.")
