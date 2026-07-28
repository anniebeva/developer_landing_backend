from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AIAnalysisResult(BaseModel):
    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
    ]

    priority: Literal[
        "high",
        "medium",
        "low",
    ]

    summary: str


class ContactAnalysisResponse(BaseModel):
    id: int

    sentiment: str
    priority: str
    summary: str

    model: str | None

    created_at: datetime

    class Config:
        from_attributes = True
