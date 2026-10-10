from __future__ import annotations

import os
from typing import List

from science_research.adapters.crossref_adapter import CrossrefAdapter
from science_research.adapters.institutional_adapter import InstitutionalAdapter
from science_research.adapters.openalex_adapter import OpenAlexAdapter
from science_research.adapters.scholar_adapter import GoogleScholarAdapter
from science_research.adapters.scopus_adapter import ScopusAdapter
from science_research.models.paper import Paper


class SourceRegistryService:
    """A unified registry that fetches results from multiple source providers."""

    def __init__(self):
        self.sources = [
            InstitutionalAdapter(
                institution_name=os.getenv("INSTITUTION_NAME"),
                institution_proxy=os.getenv("INSTITUTION_PROXY_URL"),
                sso_enabled=os.getenv("INSTITUTION_SSO_ENABLED", "false").lower() == "true",
            ),
            ScopusAdapter(
                api_key=os.getenv("SCOPUS_API_KEY"),
                institution_token=os.getenv("SCOPUS_INST_TOKEN"),
            ),
            CrossrefAdapter(email=os.getenv("CROSSREF_EMAIL")),
            OpenAlexAdapter(email=os.getenv("OPENALEX_EMAIL")),
            GoogleScholarAdapter(enabled=os.getenv("GOOGLE_SCHOLAR_ENABLED", "false").lower() == "true"),
        ]

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        all_papers: List[Paper] = []
        for source in self.sources:
            try:
                all_papers.extend(source.search(query, domain=domain, limit=limit))
            except Exception:
                continue

        unique: List[Paper] = []
        seen = set()
        for paper in all_papers:
            key = (paper.title.lower(), paper.doi or paper.url or paper.journal or "")
            if key in seen:
                continue
            seen.add(key)
            unique.append(paper)
        return unique[:limit]
