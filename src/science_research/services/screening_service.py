from __future__ import annotations

from typing import List

from science_research.models.paper import Paper


class ScreeningService:
    def __init__(self, min_year: int = 2000):
        self.min_year = min_year

    def screen(self, papers: List[Paper], *, domain: str = "general") -> List[Paper]:
        screened: List[Paper] = []
        for paper in papers:
            if paper.peer_reviewed is False:
                continue
            if paper.year is not None and paper.year < self.min_year:
                continue
            if not paper.title or len(paper.title.strip()) < 5:
                continue
            if domain and domain.lower() not in (paper.title.lower() + " " + (paper.abstract or "").lower()):
                # soft filter: keep papers with the domain in metadata or abstract
                if paper.keywords and domain.lower() not in [k.lower() for k in paper.keywords]:
                    continue
            screened.append(paper)
        return screened
