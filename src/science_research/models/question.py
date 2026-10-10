from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ResearchQuestion(BaseModel):
    question_id: Optional[str] = Field(default=None)
    project_id: Optional[str] = None
    text: str
    rationale: str = ""
    evidence_basis: str = ""
    novelty_score: float = 0.0
    priority: int = 1

    class Config:
        extra = "allow"
