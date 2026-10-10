from __future__ import annotations

from typing import List

from science_research.models.paper import Paper


class GoogleScholarAdapter:
    """Google Scholar adapter stub for discovery work. Real scraping should be guarded and rate-limited."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        if not self.enabled:
            return []
        return [
            Paper(
                paper_id="scholar-demo-1",
                title=f"{query.title()} in {domain.title()} Literature",
                authors=["Scholar Author"],
                year=2023,
                journal="Discovery Journal",
                doi="10.1000/scholar-demo",
                abstract="Discovered through Google Scholar; metadata requires verification.",
                keywords=[domain, "scholar"],
                source="google_scholar",
                peer_reviewed=True,
                full_text_available=False,
                access_type="discovery_only",
            )
        ][:limit]
