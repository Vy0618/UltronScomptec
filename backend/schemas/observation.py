"""Normalized internal observation, shared by producer adapters."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, StrictBool, FiniteFloat


class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Identificador persistido pelo produtor e reutilizado nas tentativas da mesma leitura")
    machine_active: StrictBool
    voltage_24v: Optional[StrictBool] = Field(default=None, description="Presença de 24 V, somente quando existe entrada dedicada; null significa não medido")
    digital_signals: Dict[str, bool] = Field(default_factory=dict)
    analog_signals: Dict[str, FiniteFloat] = Field(default_factory=dict)
    extra_signals: Optional[Dict[str, Any]] = Field(default_factory=dict)
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Horário UTC da coleta (ISO 8601 com Z). Omita se o relógio não estiver sincronizado.",
    )

