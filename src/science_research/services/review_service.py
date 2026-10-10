from __future__ import annotations

from typing import Any, Dict, List

from science_research.models.paper import Paper


class ReviewService:
    def __init__(self):
        pass

    def summarize(self, papers: List[Paper]) -> Dict[str, Any]:
        return {
            "total_papers": len(papers),
            "source_breakdown": {source: sum(1 for p in papers if p.source == source) for source in sorted({p.source for p in papers})},
            "journal_breakdown": {journal: sum(1 for p in papers if p.journal == journal) for journal in sorted({p.journal or "unknown" for p in papers})},
            "average_citation_count": round(sum(p.citation_count or 0 for p in papers) / max(len(papers), 1), 2),
        }

    def detect_gaps(self, papers: List[Paper]) -> List[str]:
        if not papers:
            return ["No papers available for gap detection."]

        gaps = [
            "Limited integration of multi-source evidence across disciplines.",
            "Sparse validation against independent datasets or field measurements.",
            "Insufficient long-term comparative analysis across relevant conditions.",
            "Need for stronger methodological reproducibility and benchmark reporting.",
        ]
        return gaps

    def build_questions(self, topic: str, gaps: List[str]) -> List[str]:
        return [
            f"How can {topic.lower()} be modeled more accurately using multi-source evidence?",
            f"What methodological gap remains unresolved in current {topic.lower()} research?",
            f"Which validation strategy most effectively reduces uncertainty in {topic.lower()} studies?",
        ]
