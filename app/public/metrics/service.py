from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.triage.models import TriageSession


def get_api_metrics(
    db: Session,
    tenant_id: str,
    days: int = 30,
):
    since = datetime.utcnow() - timedelta(days=days)

    # Total de triagens
    total = (
        db.query(func.count(TriageSession.id))
        .filter(
            TriageSession.tenant_id == tenant_id,
            TriageSession.created_at >= since,
        )
        .scalar()
    )

    # Distribuição por urgência
    urgency_rows = (
        db.query(
            TriageSession.urgencia,
            func.count(TriageSession.id),
        )
        .filter(
            TriageSession.tenant_id == tenant_id,
            TriageSession.created_at >= since,
        )
        .group_by(TriageSession.urgencia)
        .all()
    )

    urgency_distribution = {
        urg: count for urg, count in urgency_rows
    }

    return {
        "period_days": days,
        "total_triages": total,
        "by_urgency": urgency_distribution,
    }
