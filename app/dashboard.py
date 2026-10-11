from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from science_research.config import settings
from science_research.services.analysis_service import AnalysisService
from science_research.services.report_service import ReportService
from science_research.services.research_plan_service import ResearchPlanService
from science_research.services.search_service import (
    SearchService,
    ScopusProvider,
    CrossrefProvider,
    OpenAlexProvider,
)
from science_research.services.screening_service import ScreeningService
from science_research.services.review_service import ReviewService


st.set_page_config(page_title="Research Assistant Dashboard", layout="wide")
st.title("Science and Engineering Research Assistant")

# Display available sources in sidebar
with st.sidebar:
    st.header("📊 Available Search Sources")
    
    sources_available = []
    sources_unavailable = []
    
    if settings.scopus_api_key:
        sources_available.append("✅ Scopus (licensed)")
    else:
        sources_unavailable.append("❌ Scopus (requires API key)")
    
    sources_available.append("✅ Crossref (free, public)")
    sources_available.append("✅ OpenAlex (free, public)")
    
    if settings.google_scholar_enabled:
        sources_available.append("✅ Google Scholar (discovery only)")
    
    for source in sources_available:
        st.success(source)
    
    for source in sources_unavailable:
        st.warning(source)
    
    st.divider()
    st.header("🔑 API Keys & Settings")
    
    # Allow users to input API keys temporarily for this session
    with st.expander("Configure API Keys", expanded=False):
        scopus_key = st.text_input(
            "Scopus API Key",
            value=settings.scopus_api_key or "",
            type="password",
            help="Get one at https://dev.elsevier.com/",
        )
        crossref_email = st.text_input(
            "Crossref Email",
            value=settings.crossref_email or "",
            help="For better rate limits and service",
        )
        openalex_email = st.text_input(
            "OpenAlex Email",
            value=settings.openalex_email or "",
            help="Optional but recommended",
        )
        
        if st.button("Save for this session"):
            st.session_state.scopus_key = scopus_key or None
            st.session_state.crossref_email = crossref_email or None
            st.session_state.openalex_email = openalex_email or None
            st.success("API keys updated for this session")
    
    st.divider()
    st.header("🔬 Project Settings")
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
    run_button = st.button("🚀 Run research workflow")


if run_button:
    # Get API keys from session or config
    scopus_key = st.session_state.get("scopus_key") or settings.scopus_api_key
    crossref_email = st.session_state.get("crossref_email") or settings.crossref_email
    openalex_email = st.session_state.get("openalex_email") or settings.openalex_email
    
    # Build provider list based on available keys
    providers = []
    
    if scopus_key:
        providers.append(ScopusProvider(api_key=scopus_key))
    
    providers.append(CrossrefProvider(email=crossref_email))
    providers.append(OpenAlexProvider(email=openalex_email))
    
    with st.spinner("Searching, screening, and designing the study..."):
        try:
            search_service = SearchService(providers=providers)
            papers = search_service.search(query, domain=domain, limit=10)
            
            if not papers:
                st.error(
                    "⚠️ No papers found. This may be because:\n\n"
                    "1. The search query is too specific or unusual\n"
                    "2. Network issues prevented searching\n"
                    "3. API rate limits were exceeded\n\n"
                    "Try adjusting your search query or checking your API keys in the sidebar."
                )
            else:
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

                st.success("✅ Research workflow completed.")

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
        except Exception as e:
            st.error(f"❌ Error during research workflow: {str(e)}")
            st.info("Check that all required services are available and your API keys are valid.")

else:
    st.info("📝 Enter a topic and click '🚀 Run research workflow' to start the pipeline.")
    st.divider()
    st.markdown("""
    ### How to use this tool:
    
    1. **Configure API Keys** (optional): Add your Scopus API key or email addresses in the sidebar to enable additional search sources
    2. **Select Domain**: Choose a research domain (geology, chemistry, engineering, etc.)
    3. **Enter Topic & Query**: Specify your research topic and search query
    4. **Run Workflow**: Click the button to start the research pipeline
    
    The system will:
    - Search peer-reviewed literature across multiple sources
    - Screen and rank papers by relevance
    - Identify research gaps
    - Generate research questions
    - Design methodology
    - Run analysis and generate visualizations
    - Draft a research report
    
    ### Available Search Sources:
    - **Crossref**: Free metadata from CrossRef (all papers)
    - **OpenAlex**: Free metadata from OpenAlex (millions of papers)
    - **Scopus**: Licensed access (requires API key)
    """)
