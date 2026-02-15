import json
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.triage.models import TriageSession


def get_odonto_dashboard(db: Session, tenant_id: str):
    triages = (
        db.query(TriageSession)
        .filter(TriageSession.tenant_id == tenant_id)
        .all()
    )

    total = len(triages)

    urgencia_count = {
        "baixa": 0,
        "media": 0,
        "alta": 0,
    }

    indicadores = {
        "dor_aguda": 0,
        "sangramento": 0,
        "suspeita_abscesso": 0,
        "falha_analgesico": 0,
    }

    alertas = []

    for t in triages:
        urgencia_count[t.urgencia] += 1

        answers = json.loads(t.raw_answers)

        intensidade = answers.get("intensidade")
        sangramento = answers.get("sangramento")
        inchaco = answers.get("inchaco")
        medicacao = answers.get("uso_medicacao", "")

        if intensidade == "alta":
            indicadores["dor_aguda"] += 1

        if sangramento == "sim":
            indicadores["sangramento"] += 1

        if inchaco == "sim" and intensidade in ["media", "alta"]:
            indicadores["suspeita_abscesso"] += 1
            alertas.append({
                "triage_id": t.id,
                "motivo": "Suspeita de abscesso",
            })

        if "sem melhora" in medicacao.lower():
            indicadores["falha_analgesico"] += 1

    return {
        "resumo": {
            "total_triagens": total,
            "urgencia": urgencia_count,
        },
        "indicadores_clinicos": indicadores,
        "alertas": alertas,
    }
