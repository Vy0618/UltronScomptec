from typing import Literal
from pydantic import BaseModel


class SignalOutput(BaseModel):
    code: str
    level: Literal["info", "attention", "critical"]
    title: str
    message: str
    signals: list[str]
