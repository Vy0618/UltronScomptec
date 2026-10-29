"""Optional ingestion authentication, independent of producer hardware."""
import os
import secrets
from fastapi import Header, HTTPException


def require_ingest_key(x_api_key: str = Header(default=''), x_device_key: str = Header(default='')):
    key = os.getenv('INGEST_API_KEY') or os.getenv('DEVICE_API_KEY', '')
    provided = x_api_key or x_device_key
    if key and not secrets.compare_digest(key.encode(), provided.encode()):
        raise HTTPException(401, 'Chave de ingestão inválida')
