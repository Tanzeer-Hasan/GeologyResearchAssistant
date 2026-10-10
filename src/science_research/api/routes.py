from __future__ import annotations

from fastapi import APIRouter

from science_research.models.paper import Paper
from science_research.services.search_service import SearchService, ScopusProvider
from science_research.services.screening_service import ScreeningService
from science_research.services.review_service import ReviewService

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok", "service": "ScienceAndEngineeringResearchAssistant"}


@router.get("/literature/search")
def search_literature(query: str, domain: str = "general", limit: int = 10):
    providers = [ScopusProvider(api_key=None)]
    service = SearchService(providers=providers)
    papers = service.search(query, domain=domain, limit=limit)
    screened = ScreeningService().screen(papers, domain=domain)
    review = ReviewService()
    return {
        "query": query,
        "domain": domain,
        "paper_count": len(screened),
        "papers": [paper.model_dump() for paper in screened],
        "summary": review.summarize(screened),
        "gaps": review.detect_gaps(screened),
    }
