from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.public.app import public_app
from fastapi.responses import RedirectResponse

# Routers internos
from app.auth.router import router as auth_router
from app.tenants.router import router as tenant_router
from app.patients.router import router as patients_router
from app.appointments.router import router as appointments_router
from app.triage.router import router as triage_router
from app.dashboard.router import router as dashboard_router
from app.internal.api_keys.router import router as internal_api_keys_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 CRIA TABELAS AUTOMATICAMENTE NO STARTUP
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Triage Engine – Internal API",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,  # 👈 aqui está a mágica
)

# -----------------------------
# API INTERNA
# -----------------------------
app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(patients_router)
app.include_router(appointments_router)
app.include_router(triage_router)
app.include_router(dashboard_router)
app.include_router(internal_api_keys_router)

# -----------------------------
# API PÚBLICA
# -----------------------------
app.mount("/public", public_app)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/public/")