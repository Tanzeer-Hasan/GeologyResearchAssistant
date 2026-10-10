from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


ProjectStatus = Literal["draft", "searching", "screening", "reviewing", "designing", "analysis", "reporting", "completed"]


class Project(BaseModel):
    project_id: Optional[str] = Field(default=None)
    title: str
    domain: str
    description: str = ""
    status: ProjectStatus = "draft"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        extra = "allow"
