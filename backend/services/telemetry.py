"""Compatibility adapter for existing device telemetry producers."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import CNC, Device
from schemas.telemetry import TelemetryCreate, TelemetryResponse
from services.clock import utcnow
from services.deviceAuth import require_device_key
from services.events import store_event
from services.machineState import derive_status  # Compatibility for existing integrations.

router = APIRouter(prefix="/devices", tags=["Telemetry adapter"])


@router.post("/{device_id}/telemetry", response_model=TelemetryResponse, status_code=201, dependencies=[Depends(require_device_key)])
def create_telemetry(device_id: str, data: TelemetryCreate, db: Session = Depends(get_db)):
    device = db.scalar(select(Device).where(Device.id == device_id).with_for_update())
    if device is None:
        raise HTTPException(404, "Dispositivo não encontrado")
    machine = db.scalar(select(CNC).where(CNC.id == device.cnc_id).with_for_update())
    now = utcnow()
    reading, created = store_event(db, machine, data, now, device_id=device.id)
    if created:
        device.last_seen = now
    db.commit()
    db.refresh(reading)
    return reading
