import time
from fastapi import HTTPException, status

# Estrutura em memória
# {
#   api_key_id: {
#       "window_start": timestamp,
#       "count": int
#   }
# }
_rate_limit_store: dict[str, dict] = {}


def check_rate_limit(
    api_key_id: str,
    limit_per_minute: int,
):
    """
    Rate limit simples por API key.
    Janela fixa de 60 segundos.
    """

    now = time.time()
    window_size = 60  # segundos

    record = _rate_limit_store.get(api_key_id)

    # Primeira chamada
    if not record:
        _rate_limit_store[api_key_id] = {
            "window_start": now,
            "count": 1,
        }
        return

    elapsed = now - record["window_start"]

    # Janela expirada → reset
    if elapsed > window_size:
        _rate_limit_store[api_key_id] = {
            "window_start": now,
            "count": 1,
        }
        return

    # Dentro da janela
    if record["count"] >= limit_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit excedido. Tente novamente em alguns segundos.",
        )

    record["count"] += 1
