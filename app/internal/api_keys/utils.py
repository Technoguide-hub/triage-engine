import secrets


def generate_api_key(prefix: str = "sk_live") -> str:
    """
    Gera API Key segura no padrão SaaS.
    Ex: sk_live_xxxxxxxxxxxxxxxxx
    """
    token = secrets.token_urlsafe(32)
    return f"{prefix}_{token}"
