from __future__ import annotations

from typing import Any, Dict, List

from science_research.models.paper import Paper
from science_research.services.research_design_service import MethodologyService, ResearchDesignService


class ResearchPlanService:
    def __init__(self):
        self.design_service = ResearchDesignService()
        self.methodology_service = MethodologyService()

    def build_plan(self, topic: str, gaps: List[str], domain: str = "general") -> Dict[str, Any]:
        questions = self.design_service.generate_questions(topic, gaps, domain=domain)
        best_question = self.design_service.select_best_question(questions)
        methodology = self.methodology_service.design(topic, best_question["text"], domain=domain)
        return {
            "topic": topic,
            "domain": domain,
            "questions": questions,
            "selected_question": best_question,
            "methodology": methodology,
        }
