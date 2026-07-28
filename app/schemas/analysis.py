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

    source: Literal[
        "ai",
        "fallback",
    ]


class ContactAnalysisResponse(BaseModel):
    """Schema for contact analysis response."""

    id: int

    sentiment: str
    priority: str
    summary: str
    source: str

    model: str | None

    created_at: datetime
