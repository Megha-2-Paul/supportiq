"""Validated API request and response schemas."""
from pydantic import BaseModel, Field, field_validator


class TicketRequest(BaseModel):
    text: str = Field(min_length=3, max_length=10000)

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Message must contain at least 3 non-whitespace characters")
        return value


class BatchTicketRequest(BaseModel):
    tickets: list[TicketRequest] = Field(min_length=1, max_length=1000)


class PredictionResponse(BaseModel):
    intent: str
    confidence: float = Field(ge=0, le=1)
    department: str
    priority: str
    priority_reasons: list[str] = Field(default_factory=list)
    sentiment: str
    needs_human_review: bool
    model_version: str
