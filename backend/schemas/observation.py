"""Normalized internal observation, shared by producer adapters."""
from datetime import datetime
from math import isfinite
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, StrictBool, FiniteFloat, field_validator


def validate_current_signals(signals):
    """Keep the current contract identical for direct events and device adapters."""
    if isinstance(signals, dict):
        for key in ("current", "corrente"):
            if key not in signals:
                continue
            value = signals[key]
            if (isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
                    or (isinstance(value, float) and not isfinite(value))):
                raise ValueError("Corrente em A deve ser um número finito e não negativo")
    return signals


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

    @field_validator("analog_signals", mode="before")
    @classmethod
    def valid_current(cls, signals):
        return validate_current_signals(signals)

