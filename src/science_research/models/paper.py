from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Paper(BaseModel):
    paper_id: Optional[str] = Field(default=None)
    title: str
    authors: List[str] = Field(default_factory=list)
    year: Optional[int] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    source: str = "unknown"
    peer_reviewed: bool = True
    full_text_available: bool = False
    access_type: str = "unknown"
    citation_count: Optional[int] = None
    notes: str = ""

    class Config:
        extra = "allow"
