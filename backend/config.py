"""Carrega configuração local; ambiente e .env têm prioridade sobre JSON."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

CONFIG_KEYS = {
    "DATABASE_URL", "SQL_ECHO", "CORS_ORIGINS", "AUTH_SECRET",
    "AUTH_TOKEN_TTL_MINUTES", "ADMIN_NAME", "ADMIN_EMAIL", "ADMIN_PASSWORD",
    "DEVICE_OFFLINE_TIMEOUT_SECONDS", "DEVICE_API_KEY",
}


def load_json_config(path: Path):
    if not path.is_file():
        return
    try:
        values = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Configuração JSON inválida em {path}: {error}") from error
    if not isinstance(values, dict):
        raise RuntimeError(f"Configuração JSON inválida em {path}: use um objeto de chaves e valores")
    unknown = values.keys() - CONFIG_KEYS
    if unknown:
        raise RuntimeError(f"Configuração JSON inválida em {path}: chaves desconhecidas: {', '.join(sorted(unknown))}")
    for key, value in values.items():
        if isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, int) or isinstance(value, str):
            value = str(value)
        else:
            raise RuntimeError(f"Configuração JSON inválida em {path}: {key} deve ser texto, número inteiro ou booleano")
        os.environ.setdefault(key, value)


# A simulação fornece banco e credenciais isolados pelo ambiente.
if os.getenv("ULTRON_SIMULATION", "").strip().lower() != "true":
    backend_dir = Path(__file__).resolve().parent
    load_dotenv(backend_dir / ".env", override=False)
    load_json_config(backend_dir / "config.json")
