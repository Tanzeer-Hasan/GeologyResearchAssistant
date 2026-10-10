from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from science_research.services.analysis_service import AnalysisService
from science_research.services.report_service import ReportService
from science_research.services.research_plan_service import ResearchPlanService
from science_research.services.search_service import SearchService, ScopusProvider
from science_research.services.screening_service import ScreeningService
from science_research.services.review_service import ReviewService


st.set_page_config(page_title="Research Assistant Dashboard", layout="wide")
st.title("Science and Engineering Research Assistant")

with st.sidebar:
    st.header("Project")
    project_title = st.text_input("Project title", value="AI-driven research workflow")
    domain = st.selectbox(
        "Domain",
        [
            "general",
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
    )
    topic = st.text_input("Research topic", value="sustainable energy systems")
    query = st.text_input("Search query", value="sustainable energy systems optimization")
    run_button = st.button("Run research workflow")


if run_button:
    with st.spinner("Searching, screening, and designing the study..."):
        providers = [ScopusProvider(api_key=None)]
        search_service = SearchService(providers=providers)
        papers = search_service.search(query, domain=domain, limit=10)

        screened = ScreeningService().screen(papers, domain=domain)
        review_service = ReviewService()
        gap_summary = review_service.detect_gaps(screened)
        plan_service = ResearchPlanService()
        plan = plan_service.build_plan(topic, gap_summary, domain=domain)

        analysis_service = AnalysisService(output_dir=str(ROOT / "outputs"))
        analysis = analysis_service.run(topic, domain=domain)

        report_service = ReportService()
        report = report_service.generate_report(
            topic=topic,
            domain=domain,
            selected_question=plan["selected_question"]["text"],
            methodology=plan["methodology"],
            analysis=analysis,
        )

    st.success("Research workflow completed.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Papers found", len(papers))
    col2.metric("Papers screened", len(screened))
    col3.metric("Selected question", "1")

    st.subheader("1. Literature summary")
    st.json({
        "query": query,
        "domain": domain,
        "screened_count": len(screened),
        "summary": review_service.summarize(screened),
        "gaps": gap_summary,
    })

    st.subheader("2. Research questions")
    for idx, question in enumerate(plan["questions"][:5], start=1):
        with st.expander(f"Question {idx}: {question['text']}"):
            st.write(f"Rationale: {question['rationale']}")
            st.write(f"Novelty score: {question['novelty_score']}")
            st.write(f"Feasibility: {question['feasibility']}")
            st.write(f"Impact: {question['impact']}")

    st.subheader("3. Selected research question")
    st.write(plan["selected_question"]["text"])

    st.subheader("4. Methodology")
    st.json(plan["methodology"])

    st.subheader("5. Analysis results")
    st.json({
        "summary_statistics": analysis.get("summary_statistics", {}),
        "generated_files": analysis.get("generated_files", []),
    })

    st.subheader("6. Draft report")
    st.markdown(f"## {report['title']}")
    st.write(report["abstract"])
    st.write("### Objective")
    st.write(report["objective"])
    st.write("### Research question")
    st.write(report["research_question"])
    st.write("### Discussion points")
    for i, point in enumerate(report["discussion_points"], start=1):
        st.write(f"{i}. {point}")
    st.write("### Conclusion")
    st.write(report["conclusion"])

else:
    st.info("Enter a topic and click 'Run research workflow' to start the pipeline.")
