"""Machine event ingestion. Hardware producers are external adapters."""
from datetime import timedelta
from uuid import NAMESPACE_URL, uuid5

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import CNC, MachineEvent, Telemetry
from schemas.event import EventCreate, EventResponse
from schemas.observation import Observation
from services.clock import utcnow, normalize_datetime, OFFLINE_TIMEOUT_SECONDS, MAX_CLOCK_SKEW_SECONDS
from services.ingestAuth import require_ingest_key
from services.eventRepository import latest_event
from services.machineState import derive_status

router = APIRouter(prefix="/events", tags=["Machine events"])


def store_event(db, machine, data, now, *, device_id=None):
    """Persist one observation under a locked machine; caller commits.

    The compatibility adapter retains its old idempotency namespace. Direct
    producers use machine identity, independent of serial/MAC/firmware.
    """
    occurred_at = normalize_datetime(data.timestamp) if data.timestamp else now
    if occurred_at > now + timedelta(seconds=MAX_CLOCK_SKEW_SECONDS):
        raise HTTPException(422, "Timestamp futuro: sincronize o relógio ou omita timestamp")
    identity = device_id or machine.id
    reading_id = str(uuid5(NAMESPACE_URL, f"scomptec:{identity}:{data.event_id}")) if data.event_id else None
    if reading_id:
        existing = db.scalar(select(MachineEvent).where(MachineEvent.id == reading_id))
        if existing is None and device_id:
            existing = db.get(Telemetry, reading_id)
        if existing is not None:
            fields = ("machine_active", "voltage_24v", "digital_signals", "analog_signals", "extra_signals")
            def value(obj, field):
                result = getattr(obj, field)
                return result or {} if field == "extra_signals" else result
            if any(value(existing, field) != value(data, field) for field in fields) or (data.timestamp and normalize_datetime(existing.timestamp) != occurred_at):
                raise HTTPException(409, "event_id já utilizado com outra leitura")
            return existing, False

    latest = latest_event(db, machine.id)
    reading = MachineEvent(
        machine_id=machine.id, device_id=device_id, timestamp=occurred_at, received_at=now,
        machine_active=data.machine_active, voltage_24v=data.voltage_24v,
        digital_signals=data.digital_signals, analog_signals=data.analog_signals,
        extra_signals=data.extra_signals or {},
    )
    if reading_id:
        reading.id = reading_id
    previous_seen = normalize_datetime(machine.last_seen) if machine.last_seen else None
    next_status = derive_status(data)
    if latest is None or occurred_at >= latest.timestamp:
        continuity_broken = bool(latest and (
            occurred_at - normalize_datetime(latest.timestamp) > timedelta(seconds=OFFLINE_TIMEOUT_SECONDS)
            or (previous_seen and now - previous_seen > timedelta(seconds=OFFLINE_TIMEOUT_SECONDS))
        ))
        if machine.status != next_status or continuity_broken or machine.status_since is None:
            machine.status = next_status
            machine.status_since = occurred_at
    machine.last_seen = now
    db.add(reading)
    db.flush()
    return reading, True


@router.post("", response_model=EventResponse, status_code=201, dependencies=[Depends(require_ingest_key)])
def receive_event(data: EventCreate, db: Session = Depends(get_db)):
    # Numeric IDs emitted by collectors resolve to stable machine codes:
    # "1" -> CNC-001. No dependence on device or MAC registration.
    identity = data.machine_id
    code = f"CNC-{int(identity):03d}" if identity.isascii() and identity.isdecimal() else identity
    machine = db.scalar(select(CNC).where((CNC.id == identity) | (CNC.code == code)).with_for_update())
    if machine is None:
        raise HTTPException(404, "Máquina não encontrada; cadastre-a em /api/cncs")
    normalized = Observation(
        event_id=data.event_id, timestamp=data.timestamp,
        machine_active=data.states.get("em_execucao", data.states.get("ciclo", False)),
        digital_signals=data.states,
    )
    reading, _ = store_event(db, machine, normalized, utcnow())
    db.commit()
    db.refresh(reading)
    return reading
