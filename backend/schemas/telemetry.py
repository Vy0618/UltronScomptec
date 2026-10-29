from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
from schemas.common import UTCModel


from schemas.observation import Observation as TelemetryCreate


class TelemetryResponse(UTCModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    device_id: Optional[str] = None
    machine_id: Optional[str] = None
    states: Optional[Dict[str, bool]] = None
    timestamp: datetime
    received_at: datetime
    machine_active: bool
    voltage_24v: Optional[bool] = None
    digital_signals: Optional[Dict[str, Any]] = None
    analog_signals: Optional[Dict[str, Any]] = None
    extra_signals: Optional[Dict[str, Any]] = None


class TelemetryHistoryResponse(BaseModel):
    items: List[TelemetryResponse]
    total: int
    page: int
    limit: int
