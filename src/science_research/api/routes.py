from __future__ import annotations

from fastapi import APIRouter

from science_research.services.analysis_service import AnalysisService
from science_research.services.report_service import ReportService
from science_research.services.research_plan_service import ResearchPlanService
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


@router.get("/research/questions")
def generate_questions(topic: str, domain: str = "general", gap: str | None = None):
    gaps = [gap] if gap else [
        "Limited integration of multi-source evidence across disciplines.",
        "Sparse validation against independent datasets or field measurements.",
    ]
    service = ResearchPlanService()
    plan = service.build_plan(topic, gaps, domain=domain)
    return {
        "topic": topic,
        "domain": domain,
        "questions": plan["questions"],
        "selected_question": plan["selected_question"],
    }


@router.get("/research/methodology")
def generate_methodology(topic: str, question: str, domain: str = "general"):
    service = ResearchPlanService()
    plan = service.build_plan(topic, ["Methodological gap detection required from literature review."], domain=domain)
    plan["selected_question"] = {"text": question}
    return {
        "topic": topic,
        "domain": domain,
        "selected_question": question,
        "methodology": service.methodology_service.design(topic, question, domain=domain),
    }


@router.get("/research/plan")
def generate_research_plan(topic: str, domain: str = "general", gap: str | None = None):
    gaps = [gap] if gap else [
        "Limited integration of multi-source evidence across disciplines.",
        "Sparse validation against independent datasets or field measurements.",
        "Insufficient long-term comparative analysis across relevant conditions.",
    ]
    service = ResearchPlanService()
    return service.build_plan(topic, gaps, domain=domain)


@router.get("/analysis/run")
def run_analysis(topic: str, domain: str = "general"):
    analysis_service = AnalysisService()
    return analysis_service.run(topic, domain=domain)


@router.get("/report/summary")
def generate_report(topic: str, domain: str = "general", question: str | None = None):
    question_text = question or "How can this research topic be investigated more reliably and reproducibly?"
    plan_service = ResearchPlanService()
    plan = plan_service.build_plan(topic, ["Need for stronger methodological consistency and validation."], domain=domain)
    analysis_service = AnalysisService()
    analysis = analysis_service.run(topic, domain=domain)
    report_service = ReportService()
    return report_service.generate_report(
        topic=topic,
        domain=domain,
        selected_question=question_text,
        methodology=plan["methodology"],
        analysis=analysis,
    )
