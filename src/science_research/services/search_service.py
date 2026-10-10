from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from science_research.models.paper import Paper


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        raise NotImplementedError


class ScopusProvider(SearchProvider):
    def __init__(self, api_key: str | None = None, institution_token: str | None = None):
        self.api_key = api_key
        self.institution_token = institution_token

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        if not self.api_key:
            return []

        return [
            Paper(
                paper_id="scopus-demo-1",
                title=f"{query.title()} in {domain.title()} Research",
                authors=["Author A", "Author B"],
                year=2024,
                journal="Journal of Applied Science",
                doi="10.1000/example",
                abstract="Peer-reviewed study relevant to the research question.",
                keywords=[domain, "peer-reviewed", query.lower()],
                source="scopus",
                peer_reviewed=True,
                full_text_available=True,
                access_type="licensed",
                citation_count=18,
            )
        ]


class CrossrefProvider(SearchProvider):
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        return []


class OpenAlexProvider(SearchProvider):
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        return []


class GoogleScholarProvider(SearchProvider):
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        return []


class SearchService:
    def __init__(self, providers: list[SearchProvider] | None = None):
        self.providers = providers or []

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        papers: List[Paper] = []
        for provider in self.providers:
            papers.extend(provider.search(query, domain=domain, limit=limit))
        unique = []
        seen = set()
        for paper in papers:
            key = (paper.title.lower(), paper.doi or paper.url or paper.journal or "")
            if key in seen:
                continue
            seen.add(key)
            unique.append(paper)
        return unique[:limit]
