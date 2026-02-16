from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.core.config import settings

from app.auth.models import User
from app.public.app import public_app

# Routers internos
from app.auth.router import router as auth_router
from app.tenants.router import router as tenant_router
from app.patients.router import router as patients_router
from app.appointments.router import router as appointments_router
from app.triage.router import router as triage_router
from app.dashboard.router import router as dashboard_router
from app.internal.api_keys.router import router as internal_api_keys_router


# ==========================================================
# LIFESPAN (startup / shutdown)
# ==========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Starting Triage Engine...")

    # ------------------------------------------------------
    # 1️⃣ Criar tabelas automaticamente (piloto)
    # ------------------------------------------------------
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables verified")

    # ------------------------------------------------------
    # 2️⃣ Criar usuário OWNER automaticamente (se configurado)
    # ------------------------------------------------------
    if settings.OWNER_EMAIL and settings.OWNER_PASSWORD:

        db: Session = SessionLocal()

        try:
            owner = (
                db.query(User)
                .filter(User.email == settings.OWNER_EMAIL)
                .first()
            )

            if not owner:
                owner = User(
                    email=settings.OWNER_EMAIL,
                    password_hash=hash_password(settings.OWNER_PASSWORD),
                    role="owner",
                )
                db.add(owner)
                db.commit()
                print("✅ Owner user created automatically")
            else:
                print("ℹ Owner already exists")

        except Exception as e:
            print(f"❌ Error creating owner: {e}")

        finally:
            db.close()

    else:
        print("⚠ OWNER_EMAIL or OWNER_PASSWORD not configured")

    print("🔥 Triage Engine ready")

    yield

    print("🛑 Shutting down Triage Engine...")


# ==========================================================
# FASTAPI APP (Internal API)
# ==========================================================
app = FastAPI(
    title="Triage Engine – Internal API",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ----------------------------------------------------------
# API INTERNA
# ----------------------------------------------------------
app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(patients_router)
app.include_router(appointments_router)
app.include_router(triage_router)
app.include_router(dashboard_router)
app.include_router(internal_api_keys_router)


# ----------------------------------------------------------
# API PÚBLICA (engine exposto)
# ----------------------------------------------------------
app.mount("/public", public_app)


# ----------------------------------------------------------
# Health check (Railway)
# ----------------------------------------------------------
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


# ----------------------------------------------------------
# Root → redireciona para Swagger público
# ----------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/public")
