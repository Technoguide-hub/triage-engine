from fastapi import FastAPI

from app.public.triage.router import router as public_triage_router
from app.public.metrics.router import router as public_metrics_router
from app.public.auth.router import router as public_auth_router

public_app = FastAPI(
    title="Triage Engine API",
    description="""
API pública de Pré-Triagem Clínica com IA responsável.

Uso:
- Softwares médicos
- Softwares odontológicos
- ERPs clínicos
- Sistemas de agenda

Autenticação:
- API Key via header X-API-Key
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Rotas públicas
public_app.include_router(public_auth_router)
public_app.include_router(public_triage_router)
public_app.include_router(public_metrics_router)
