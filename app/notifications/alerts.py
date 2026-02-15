from sqlalchemy.orm import Session
from app.auth.models import User
from app.notifications.email import send_email_alert


def alert_if_critical(db: Session, tenant_id: str, triage):
    if triage.urgencia not in ("alta", "emergencia"):
        return

    admins = (
        db.query(User)
        .filter(
            User.tenant_id == tenant_id,
            User.role == "admin"
        )
        .all()
    )

    subject = f"🚨 Triagem {triage.urgencia.upper()} detectada"

    body = f"""
ATENÇÃO:

Uma triagem foi classificada como {triage.urgencia.upper()}.

Consulta: {triage.appointment_id}

Resumo IA:
{triage.ai_summary}

Acesse o sistema imediatamente.
"""

    for admin in admins:
        send_email_alert(admin.email, subject, body)
