from __future__ import annotations

from typing import List

from science_research.models.paper import Paper


class ScopusAdapter:
    """Scopus integration placeholder with a real API contract shape."""

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
                journal="Applied Research Journal",
                doi="10.1000/scopus-demo",
                abstract="Peer-reviewed paper retrieved through the Scopus search API.",
                keywords=[domain, "peer-reviewed", query.lower()],
                source="scopus",
                peer_reviewed=True,
                full_text_available=True,
                access_type="licensed",
                citation_count=25,
            )
        ][:limit]
