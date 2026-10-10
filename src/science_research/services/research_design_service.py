from __future__ import annotations

from typing import Any, Dict, List

from science_research.models.paper import Paper


class ResearchDesignService:
    def __init__(self):
        pass

    def generate_questions(self, topic: str, gaps: List[str], domain: str = "general") -> List[Dict[str, Any]]:
        candidate_questions = [
            {
                "text": f"How can {topic.lower()} be modeled more accurately by integrating multi-source evidence in {domain.lower()} research?",
                "rationale": "Current literature suggests fragmented methods and inconsistent validation strategies.",
                "novelty_score": 0.89,
                "feasibility": "high",
                "impact": "high",
            },
            {
                "text": f"What methodological factors most strongly explain uncertainty in {topic.lower()} studies within {domain.lower()} applications?",
                "rationale": "There is evidence of unresolved uncertainty propagation and limited comparative benchmarking.",
                "novelty_score": 0.82,
                "feasibility": "high",
                "impact": "high",
            },
            {
                "text": f"Which validation framework yields the most robust assessment of {topic.lower()} performance under real-world conditions?",
                "rationale": "Several studies report partial validation but lack consistent cross-method comparison.",
                "novelty_score": 0.79,
                "feasibility": "medium",
                "impact": "high",
            },
            {
                "text": f"What are the dominant drivers of heterogeneity in {topic.lower()} across spatial, temporal, or experimental scales?",
                "rationale": "The literature indicates inconsistent treatment of scale effects and contextual variability.",
                "novelty_score": 0.76,
                "feasibility": "medium",
                "impact": "high",
            },
        ]

        if gaps:
            for gap in gaps:
                candidate_questions.append(
                    {
                        "text": f"How could {topic.lower()} research address the following issue: {gap}?",
                        "rationale": gap,
                        "novelty_score": 0.7,
                        "feasibility": "medium",
                        "impact": "medium",
                    }
                )

        return sorted(candidate_questions, key=lambda q: q["novelty_score"], reverse=True)

    def select_best_question(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not questions:
            return {"text": "No research question available."}
        return max(questions, key=lambda q: (q["novelty_score"], q["impact"] == "high"))


class MethodologyService:
    def __init__(self):
        pass

    def design(self, topic: str, question: str, domain: str = "general") -> Dict[str, Any]:
        return {
            "topic": topic,
            "domain": domain,
            "selected_question": question,
            "research_hypothesis": f"The proposed approach improves the accuracy and interpretability of {topic.lower()} by integrating evidence, validating results, and testing dominant sources of uncertainty.",
            "study_design": "comparative observational and experimental design with validation and sensitivity analysis",
            "data_sources": [
                "peer-reviewed literature",
                "institutional datasets",
                "field measurements or experiment outputs",
                "simulation or computational benchmarks",
                "public or open reference datasets",
            ],
            "variables": [
                "independent variables related to the scientific system",
                "intermediate drivers or control factors",
                "response variables and performance measures",
                "uncertainty and sensitivity indicators",
            ],
            "methods": [
                "systematic literature synthesis",
                "quantitative comparison of methods",
                "statistical or mechanistic modeling",
                "cross-validation and uncertainty quantification",
                "visual and tabular interpretation of results",
            ],
            "validation_strategy": [
                "benchmark against established methods",
                "sensitivity analysis",
                "out-of-sample validation",
                "uncertainty propagation and robustness checks",
            ],
            "expected_outputs": [
                "research questions and hypotheses",
                "processed data tables",
                "figures and graphs",
                "model diagnostics and validation metrics",
                "manuscript-ready results and discussion",
            ],
        }
