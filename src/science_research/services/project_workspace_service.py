from __future__ import annotations

from typing import Any, Dict, List, Optional

from science_research.models.citation import Citation
from science_research.models.paper import Paper
from science_research.models.project import Project


class ProjectWorkspaceService:
    """Stores project state in memory for a research workflow workspace."""

    def __init__(self):
        self._projects: Dict[str, Dict[str, Any]] = {}

    def create_project(self, title: str, domain: str, description: str = "") -> Project:
        project = Project(project_id=f"proj-{len(self._projects) + 1:04d}", title=title, domain=domain, description=description)
        self._projects[project.project_id] = {
            "project": project,
            "papers": [],
            "questions": [],
            "methodology": {},
            "analysis": {},
            "citations": [],
        }
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        project_bundle = self._projects.get(project_id)
        return project_bundle["project"] if project_bundle else None

    def list_projects(self) -> List[Project]:
        return [bundle["project"] for bundle in self._projects.values()]

    def add_paper(self, project_id: str, paper: Paper) -> Paper:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        self._projects[project_id]["papers"].append(paper)
        return paper

    def add_question(self, project_id: str, question: Dict[str, Any]) -> Dict[str, Any]:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        self._projects[project_id]["questions"].append(question)
        return question

    def set_methodology(self, project_id: str, methodology: Dict[str, Any]) -> Dict[str, Any]:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        self._projects[project_id]["methodology"] = methodology
        return methodology

    def set_analysis(self, project_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        self._projects[project_id]["analysis"] = analysis
        return analysis

    def add_citation(self, project_id: str, citation: Citation) -> Citation:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        self._projects[project_id]["citations"].append(citation)
        return citation

    def export_bibliography(self, project_id: str) -> Dict[str, Any]:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        citations = self._projects[project_id]["citations"]
        return {
            "project_id": project_id,
            "citations": [citation.to_dict() for citation in citations],
            "bibtex": "\n\n".join(citation.to_bibtex() for citation in citations),
        }

    def summary(self, project_id: str) -> Dict[str, Any]:
        if project_id not in self._projects:
            raise KeyError(f"Project {project_id} does not exist")
        bundle = self._projects[project_id]
        project = bundle["project"]
        return {
            "project": project.model_dump(),
            "paper_count": len(bundle["papers"]),
            "question_count": len(bundle["questions"]),
            "methodology": bundle["methodology"],
            "analysis": bundle["analysis"],
            "citation_count": len(bundle["citations"]),
        }
