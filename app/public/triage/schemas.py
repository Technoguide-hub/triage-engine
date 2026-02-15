from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class PublicTriageCreate(BaseModel):
    """
    Schema público para parceiros externos.
    NÃO depende do conceito de appointment interno.
    """

    external_id: Optional[str] = Field(
        None,
        description="ID da consulta/paciente no sistema externo",
        example="consulta_789"
    )

    answers: Dict[str, Any] = Field(
        ...,
        description="Respostas estruturadas da pré-triagem",
        example={
            "queixa_principal": "Dor forte no dente",
            "inicio": "há 2 dias",
            "intensidade": "8/10"
        }
    )
