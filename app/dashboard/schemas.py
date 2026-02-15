# app/dashboard/schemas.py
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class UrgencySummary(BaseModel):
    emergencia: int = 0
    alta: int = 0
    moderada: int = 0
    baixa: int = 0


class DashboardAlert(BaseModel):
    triage_id: str
    appointment_id: str
    urgencia: str
    created_at: datetime


class DashboardAlertsResponse(BaseModel):
    total: int
    alerts: List[DashboardAlert]

class DashboardCard(BaseModel):
    alta: int
    media: int
    baixa: int
    preventiva: int


class DashboardTriageItem(BaseModel):
    triage_id: str
    prioridade: str
    queixa: str
    created_at: datetime


class DashboardOdontoResponse(BaseModel):
    cards: DashboardCard
    prioritarios: List[DashboardTriageItem]