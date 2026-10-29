from datetime import datetime, timezone
import os

OFFLINE_TIMEOUT_SECONDS = int(os.getenv("EVENT_OFFLINE_TIMEOUT_SECONDS") or os.getenv("DEVICE_OFFLINE_TIMEOUT_SECONDS", "90"))
MAX_CLOCK_SKEW_SECONDS = 60
if OFFLINE_TIMEOUT_SECONDS < 10:
    raise ValueError("EVENT_OFFLINE_TIMEOUT_SECONDS deve ser pelo menos 10")


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)


def normalize_datetime(value):
    if value is None:
        return utcnow()
    return value.astimezone(timezone.utc).replace(tzinfo=None, microsecond=0) if value.tzinfo else value.replace(microsecond=0)


def is_online(last_seen, *, future_tolerance_seconds=0):
    """Check freshness, allowing bounded clock skew only for collection times.

    Event reception is stamped by this server and keeps a zero tolerance.
    Collection timestamps use the same tolerance as event ingestion.
    """
    return bool(last_seen and -future_tolerance_seconds <= (utcnow() - normalize_datetime(last_seen)).total_seconds() <= OFFLINE_TIMEOUT_SECONDS)
