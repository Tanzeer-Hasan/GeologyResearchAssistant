from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from science_research.api.routes import router as science_router

app = FastAPI(title="Science and Engineering Research Assistant")
app.include_router(science_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ScienceAndEngineeringResearchAssistant"}


@app.get("/")
def root():
    return {
        "message": "Science and Engineering Research Assistant is running.",
        "features": [
            "peer-reviewed literature search",
            "institutional access routing",
            "domain-aware literature review",
            "gap analysis",
            "research question and hypothesis generation",
            "methodology design",
            "analysis runner",
            "visualization generator",
            "citation-aware reporting",
        ],
        "supported_domains": [
            "geology",
            "geophysics",
            "materials science",
            "chemistry",
            "engineering",
            "environmental science",
            "computer science",
            "biomedical science",
            "energy systems",
        ],
    }
