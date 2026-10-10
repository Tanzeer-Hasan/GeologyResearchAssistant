from fastapi import FastAPI

app = FastAPI(title="Science and Engineering Research Assistant")


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
