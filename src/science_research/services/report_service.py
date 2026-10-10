from __future__ import annotations

from typing import Any, Dict


class ReportService:
    """Builds a readable scientific report from the research plan and analysis results."""

    def __init__(self):
        pass

    def generate_report(self, topic: str, domain: str, selected_question: str, methodology: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"{topic} in {domain.title()}",
            "abstract": (
                f"This study investigates {topic.lower()} within the {domain.lower()} domain. "
                f"The central research question is: {selected_question}. "
                f"The methodology combines literature synthesis, structured comparison, and reproducible analysis to evaluate the main drivers of variability and uncertainty."
            ),
            "objective": f"To assess and improve understanding of {topic.lower()} using a domain-aware, evidence-based research framework.",
            "research_question": selected_question,
            "methodology_summary": methodology,
            "results_summary": {
                "summary_statistics": analysis.get("summary_statistics", {}),
                "generated_files": analysis.get("generated_files", []),
            },
            "discussion_points": [
                "The findings suggest that multi-source evidence improves interpretability.",
                "Uncertainty remains a major source of variability and should be reported clearly.",
                "Further validation is needed under broader conditions and with independent datasets.",
            ],
            "conclusion": (
                f"The study provides a structured approach for investigating {topic.lower()} and demonstrates how evidence synthesis, methodology design, and reproducible analysis can support scientific conclusions."
            ),
        }
