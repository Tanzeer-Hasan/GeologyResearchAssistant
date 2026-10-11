from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import httpx

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
        params = {
            "query.title": query,
            "rows": limit,
            "select": "title,author,issued,container-title,DOI,URL,abstract",
        }
        headers = {"User-Agent": "ScienceResearchAssistant/0.1"}
        try:
            response = httpx.get("https://api.crossref.org/works", params=params, headers=headers, timeout=20.0)
            response.raise_for_status()
        except Exception:
            return []

        items = response.json().get("message", {}).get("items", [])
        papers: List[Paper] = []
        for item in items[:limit]:
            title = item.get("title", [""])[0] if item.get("title") else ""
            authors = [a.get("family", "") for a in item.get("author", []) if a.get("family")]
            issued = item.get("issued", {}).get("date-parts", [[None]])[0][0]
            journal = item.get("container-title", [None])[0]
            doi = item.get("DOI")
            url = item.get("URL")
            abstract = item.get("abstract")
            if abstract:
                abstract = abstract.replace("\n", " ")
            papers.append(
                Paper(
                    paper_id=f"crossref-{doi or title.lower().replace(' ', '-')}",
                    title=title,
                    authors=authors,
                    year=issued,
                    journal=journal,
                    doi=doi,
                    url=url,
                    abstract=abstract,
                    keywords=[domain, "crossref"],
                    source="crossref",
                    peer_reviewed=True,
                    full_text_available=False,
                    access_type="metadata_only",
                )
            )
        return papers


class OpenAlexProvider(SearchProvider):
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        params = {
            "search": query,
            "per-page": limit,
        }
        try:
            response = httpx.get("https://api.openalex.org/works", params=params, timeout=20.0)
            response.raise_for_status()
        except Exception:
            return []

        papers: List[Paper] = []
        for item in response.json().get("results", [])[:limit]:
            title = item.get("display_name") or ""
            authors = [a.get("author", {}).get("display_name") for a in item.get("authorships", []) if a.get("author")]
            year = item.get("publication_year")
            journal = item.get("primary_location", {}).get("source", {}).get("display_name")
            doi = item.get("doi")
            url = item.get("id")
            abstract = item.get("abstract_inverted_index")
            abstract_text = ""
            if abstract:
                keys = list(abstract.keys())
                abstract_text = " ".join(keys)
            papers.append(
                Paper(
                    paper_id=f"openalex-{doi or title.lower().replace(' ', '-')}",
                    title=title,
                    authors=authors,
                    year=year,
                    journal=journal,
                    doi=doi,
                    url=url,
                    abstract=abstract_text,
                    keywords=[domain, "openalex"],
                    source="openalex",
                    peer_reviewed=True,
                    full_text_available=False,
                    access_type="metadata_only",
                )
            )
        return papers


class GoogleScholarProvider(SearchProvider):
    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        return []


class SearchService:
    def __init__(self, providers: list[SearchProvider] | None = None):
        if providers is not None:
            self.providers = providers
        else:
            self.providers = [CrossrefProvider(), OpenAlexProvider()]

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
