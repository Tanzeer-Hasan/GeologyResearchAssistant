from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from science_research.db import create_project, list_projects, save_analysis_run, save_methodology, save_paper, save_question
from science_research.services.analysis_service import AnalysisService
from science_research.services.report_service import ReportService
from science_research.services.research_plan_service import ResearchPlanService
from science_research.services.search_service import SearchService, ScopusProvider
from science_research.services.screening_service import ScreeningService
from science_research.services.review_service import ReviewService

router = APIRouter(prefix="/api")


class ProjectCreateRequest(BaseModel):
    title: str
    domain: str
    description: str = ""


@router.get("/health")
def health():
    return {"status": "ok", "service": "ScienceAndEngineeringResearchAssistant"}


@router.post("/projects")
def create_project_endpoint(payload: ProjectCreateRequest):
    project = create_project(payload.title, payload.domain, payload.description)
    return {"project": project}


@router.get("/projects")
def get_projects():
    return {"projects": list_projects()}


@router.get("/literature/search")
def search_literature(query: str, domain: str = "general", limit: int = 10, project_id: int | None = None):
    providers = [ScopusProvider(api_key=None)]
    service = SearchService(providers=providers)
    papers = service.search(query, domain=domain, limit=limit)
    screened = ScreeningService().screen(papers, domain=domain)
    review = ReviewService()

    if project_id is not None:
        for paper in screened:
            save_paper(project_id, paper.model_dump())

    return {
        "query": query,
        "domain": domain,
        "paper_count": len(screened),
        "papers": [paper.model_dump() for paper in screened],
        "summary": review.summarize(screened),
        "gaps": review.detect_gaps(screened),
    }


@router.get("/research/questions")
def generate_questions(topic: str, domain: str = "general", gap: str | None = None, project_id: int | None = None):
    gaps = [gap] if gap else [
        "Limited integration of multi-source evidence across disciplines.",
        "Sparse validation against independent datasets or field measurements.",
    ]
    service = ResearchPlanService()
    plan = service.build_plan(topic, gaps, domain=domain)
    if project_id is not None:
        for question in plan["questions"]:
            save_question(project_id, question)
    return {
        "topic": topic,
        "domain": domain,
        "questions": plan["questions"],
        "selected_question": plan["selected_question"],
    }


@router.get("/research/methodology")
def generate_methodology(topic: str, question: str, domain: str = "general", project_id: int | None = None):
    service = ResearchPlanService()
    methodology = service.methodology_service.design(topic, question, domain=domain)
    if project_id is not None:
        save_methodology(project_id, methodology)
    return {
        "topic": topic,
        "domain": domain,
        "selected_question": question,
        "methodology": methodology,
    }


@router.get("/research/plan")
def generate_research_plan(topic: str, domain: str = "general", gap: str | None = None, project_id: int | None = None):
    gaps = [gap] if gap else [
        "Limited integration of multi-source evidence across disciplines.",
        "Sparse validation against independent datasets or field measurements.",
        "Insufficient long-term comparative analysis across relevant conditions.",
    ]
    service = ResearchPlanService()
    plan = service.build_plan(topic, gaps, domain=domain)
    if project_id is not None:
        for question in plan["questions"]:
            save_question(project_id, question)
        save_methodology(project_id, plan["methodology"])
    return plan


@router.get("/analysis/run")
def run_analysis(topic: str, domain: str = "general", project_id: int | None = None):
    analysis_service = AnalysisService()
    results = analysis_service.run(topic, domain=domain)
    if project_id is not None:
        save_analysis_run(project_id, topic, domain, results)
    return results


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
