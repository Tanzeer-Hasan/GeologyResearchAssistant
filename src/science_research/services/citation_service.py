from __future__ import annotations

from typing import Any, Dict, List, Sequence

from science_research.models.citation import Citation
from science_research.models.paper import Paper


class CitationService:
    """Builds citations from literature results and exports them as BibTeX or JSON."""

    @staticmethod
    def from_papers(papers: Sequence[Paper]) -> List[Citation]:
        citations: List[Citation] = []
        for index, paper in enumerate(papers, start=1):
            author_list = paper.authors or ["Unknown Author"]
            key = (paper.doi or paper.title or f"ref-{index}").replace(" ", "-").replace("/", "-")
            citations.append(
                Citation(
                    citation_id=f"cit-{index:04d}",
                    key=key,
                    title=paper.title,
                    authors=author_list,
                    year=paper.year,
                    journal=paper.journal,
                    doi=paper.doi,
                    url=paper.url,
                    source=paper.source,
                    notes=paper.notes,
                )
            )
        return citations

    @staticmethod
    def export_bibtex(papers: Sequence[Paper]) -> str:
        return "\n\n".join(citation.to_bibtex() for citation in CitationService.from_papers(papers))

    @staticmethod
    def export_json(papers: Sequence[Paper]) -> List[Dict[str, Any]]:
        return [citation.to_dict() for citation in CitationService.from_papers(papers)]
