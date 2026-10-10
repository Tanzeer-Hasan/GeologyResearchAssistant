from __future__ import annotations

import os
from typing import List

import httpx

from science_research.models.paper import Paper


class CrossrefAdapter:
    """A lightweight Crossref adapter that supports metadata lookup and title search."""

    def __init__(self, email: str | None = None):
        self.email = email or os.getenv("CROSSREF_EMAIL")

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        headers = {"User-Agent": "ScienceResearchAssistant/0.1"}
        params = {
            "query.title": query,
            "rows": limit,
            "select": "title,author,issued,container-title,DOI,URL,abstract",
        }
        if self.email:
            params["mailto"] = self.email

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
