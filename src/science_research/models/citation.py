from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Citation(BaseModel):
    citation_id: Optional[str] = Field(default=None)
    key: str
    title: str
    authors: List[str] = Field(default_factory=list)
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    source: str = "unknown"
    notes: str = ""

    def to_bibtex(self) -> str:
        authors = ", ".join(self.authors) if self.authors else "Anonymous"
        year = self.year or "n.d."
        journal = self.journal or "Unspecified"
        doi = f"doi: {{{self.doi}}}" if self.doi else ""
        url = f"url = {{{self.url}}}," if self.url else ""
        lines = [
            f"@article{{{self.key},",
            f"  title = {{{self.title}}},",
            f"  author = {{{authors}}},",
            f"  year = {{{year}}},",
            f"  journal = {{{journal}}},",
            f"  {doi}" if doi else "",
            f"  {url}" if url else "",
            "}",
        ]
        return "\n".join(part for part in lines if part)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "citation_id": self.citation_id,
            "key": self.key,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "journal": self.journal,
            "doi": self.doi,
            "url": self.url,
            "source": self.source,
            "notes": self.notes,
        }
