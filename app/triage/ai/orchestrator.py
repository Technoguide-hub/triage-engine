import json
from typing import Literal

from app.core.config import settings
from app.ai.client import get_openai_client
from app.triage.ai_schema import TriageAISummary

from app.triage.ai.medical_prompt import MEDICAL_SYSTEM_INSTRUCTIONS
from app.triage.ai.dental_prompt import DENTAL_SYSTEM_INSTRUCTIONS


ClinicType = Literal["clinico geral", "odonto"]


# ------------------------------------------------------------------
# Fallback seguro (NUNCA quebra o fluxo do sistema)
# ------------------------------------------------------------------
def _fallback_summary() -> TriageAISummary:
    return TriageAISummary(
        resumo_curto="Resumo automático indisponível no momento.",
        soap={
            "S": "não informado",
            "O": "não informado",
            "A": "não informado",
            "P": "não informado",
        },
        red_flags=[],
        urgencia="baixa",
        perguntas_para_consulta=[],
    )


# ------------------------------------------------------------------
# System instructions conforme tipo da clínica
# ------------------------------------------------------------------
def _get_system_instructions(clinic_type: ClinicType) -> str:
    if clinic_type == "odonto":
        return DENTAL_SYSTEM_INSTRUCTIONS
    return MEDICAL_SYSTEM_INSTRUCTIONS  # default seguro


# ------------------------------------------------------------------
# Prompt médico (genérico)
# ------------------------------------------------------------------
def _build_medical_prompt(answers: dict) -> str:
    return f"""
Dados de pré-triagem fornecidos pelo paciente (JSON):
{json.dumps(answers, ensure_ascii=False, indent=2)}

Tarefa:
- Organize as informações conforme o formato solicitado.
- Não invente dados.
- Se algo não estiver disponível, use "não informado".
- Retorne APENAS JSON válido no esquema definido.
"""


# ------------------------------------------------------------------
# Prompt odontológico
# ------------------------------------------------------------------
def _build_dental_prompt(answers: dict) -> str:
    return f"""
Dados de pré-triagem odontológica (JSON):
{json.dumps(answers, ensure_ascii=False, indent=2)}

TAREFA:
1) Gere um resumo odontológico claro e objetivo.
2) Preencha SOAP (S, O, A, P) exatamente como strings.
3) Liste red_flags odontológicas relevantes.
4) Classifique urgencia corretamente.
5) Gere perguntas úteis para o dentista.

Retorne APENAS JSON válido conforme o formato obrigatório.
"""


# ------------------------------------------------------------------
# ORQUESTRADOR PRINCIPAL
# ------------------------------------------------------------------
def generate_triage_summary(
    answers: dict,
    clinic_type: ClinicType = "clinico geral",
) -> TriageAISummary:
    """
    Orquestrador central da IA de pré-triagem.

    - Decide prompt conforme tipo da clínica
    - Nunca quebra o fluxo clínico
    - Usa apenas settings (sem os.getenv)
    """

    # 🔒 Feature flag natural
    if not settings.OPENAI_API_KEY:
        return _fallback_summary()

    client = get_openai_client()
    system_instructions = _get_system_instructions(clinic_type)

    prompt = (
        _build_dental_prompt(answers)
        if clinic_type == "odonto"
        else _build_medical_prompt(answers)
    )

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=system_instructions,
            input=prompt,
        )

        output_text = response.output_text.strip()
        data = json.loads(output_text)

        return TriageAISummary.model_validate(data)

    except Exception as e:
        print("🔥 OpenAI error:", str(e))

    return TriageAISummary(
        resumo_curto="Falha ao gerar resumo automático.",
        soap={
            "S": "não informado",
            "O": "não informado",
            "A": "revisar manualmente",
            "P": "revisar manualmente",
        },
        red_flags=[],
        urgencia="media",
        perguntas_para_consulta=[],
    )
def generate_triage_summary(
    answers: dict,
    clinic_type: ClinicType = "clinico geral",
) -> TriageAISummary:

    print("🔍 OPENAI_API_KEY:", bool(settings.OPENAI_API_KEY))
    print("🔍 OPENAI_MODEL:", settings.OPENAI_MODEL)

    if not settings.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não encontrada")
        return _fallback_summary()

    client = get_openai_client()
    system_instructions = _get_system_instructions(clinic_type)

    prompt = (
        _build_dental_prompt(answers)
        if clinic_type == "odonto"
        else _build_medical_prompt(answers)
    )

    try:
        print("🚀 Chamando OpenAI...")
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=system_instructions,
            input=prompt,
        )

        print("✅ Resposta recebida")

        output_text = response.output_text
        print("📦 Output:", output_text)

        data = json.loads(output_text)

        return TriageAISummary.model_validate(data)

    except Exception as e:
        print("🔥 ERRO OPENAI:", str(e))
        raise e  # 👈 IMPORTANTE
