"""Hardware-independent event envelope: machine identity and a state snapshot."""
from datetime import datetime
from typing import Any, Annotated
from pydantic import BaseModel, ConfigDict, Field, StrictBool, FiniteFloat, model_validator
from schemas.common import UTCModel


class EventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    machine_id: str = Field(min_length=1, max_length=36, description="UUID, código ou alias numérico da máquina cadastrada (1 = CNC-001)")
    states: dict[str, StrictBool] = Field(min_length=1, max_length=64, description="Snapshot completo dos estados observados; ausente significa não informado")
    analog_signals: dict[str, Annotated[FiniteFloat, Field(strict=True)]] = Field(default_factory=dict, max_length=64, description="Medições opcionais; current/corrente em A. Ausente não representa zero")
    extra_signals: dict[str, Any] = Field(default_factory=dict, max_length=64)
    event_id: str | None = Field(default=None, min_length=1, max_length=100)
    timestamp: datetime | None = None

    @model_validator(mode="after")
    def non_negative_current(self):
        for key in ("current", "corrente"):
            if key in self.analog_signals and self.analog_signals[key] < 0:
                raise ValueError("Corrente em A deve ser não negativa")
        return self


class EventResponse(UTCModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    machine_id: str
    states: dict[str, bool]
    analog_signals: dict[str, float] = Field(default_factory=dict)
    extra_signals: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime
    received_at: datetime
