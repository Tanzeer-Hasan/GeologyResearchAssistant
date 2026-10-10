from __future__ import annotations

import os
from typing import List

import httpx

from science_research.models.paper import Paper


class OpenAlexAdapter:
    """OpenAlex search metadata adapter."""

    def __init__(self, email: str | None = None):
        self.email = email or os.getenv("OPENALEX_EMAIL")

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        params = {
            "search": query,
            "per-page": limit,
            "mailto": self.email,
        } if self.email else {
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
