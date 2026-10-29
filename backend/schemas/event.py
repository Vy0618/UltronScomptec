"""Hardware-independent event envelope: machine identity and a state snapshot."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from schemas.common import UTCModel


class EventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    machine_id: str = Field(min_length=1, max_length=36, description="UUID, código ou alias numérico da máquina cadastrada (1 = CNC-001)")
    states: dict[str, StrictBool] = Field(min_length=1, max_length=64, description="Snapshot completo dos estados observados; ausente significa não informado")
    event_id: str | None = Field(default=None, min_length=1, max_length=100)
    timestamp: datetime | None = None


class EventResponse(UTCModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    machine_id: str
    states: dict[str, bool]
    timestamp: datetime
    received_at: datetime
