from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Methodology(BaseModel):
    methodology_id: Optional[str] = Field(default=None)
    project_id: Optional[str] = None
    question_id: Optional[str] = None
    design_type: str = "observational"
    data_sources: List[str] = Field(default_factory=list)
    analysis_methods: List[str] = Field(default_factory=list)
    validation_strategy: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

    class Config:
        extra = "allow"
