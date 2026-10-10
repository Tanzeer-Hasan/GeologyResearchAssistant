# Science and Engineering Research Assistant

A multidisciplinary AI research workflow for science and engineering that supports:

- peer-reviewed literature discovery
- institutional access and login-aware source routing
- literature review synthesis and gap identification
- research question generation and hypothesis formulation
- methodology design for experimental, computational, and analytical studies
- code execution for modeling, simulation, and analysis
- generation of figures, maps, tables, and graphs
- citation-aware reporting and manuscript drafting

## Project goals

This project is designed as a general scientific research assistant for domains such as:

- geology and geophysics
- materials science and engineering
- chemistry and chemical engineering
- physics and applied physics
- civil, mechanical, and aerospace engineering
- environmental science and engineering
- biomedical and life sciences
- computer science and data-intensive engineering
- energy systems and renewable technologies
- applied mathematics and computational science

It is not just a chatbot: it is a structured research pipeline that aims to:

1. Search only peer-reviewed sources
2. Allow institution-based access to full-text papers
3. Screen and rank papers by quality, relevance, method quality, and evidence strength
4. Summarize the literature and identify missing research areas
5. Convert gaps into research questions and hypotheses
6. Build methods and analysis workflows
7. Run code to generate results and validate findings
8. Produce publication-quality figures, graphs, and summary tables
9. Write a draft paper with proper citations

## Core architecture

- Search and metadata layer
  - Scopus API
  - Google Scholar discovery
  - Crossref / OpenAlex metadata enrichment
  - institutional proxy or SSO support
  - domain-specific repositories and databases
- Quality and screening layer
  - journal and venue filtering
  - peer-reviewed validation
  - duplicate removal
  - relevance scoring
  - methods and evidence checks
- Review intelligence layer
  - abstract summarization
  - theme extraction
  - concept clustering
  - gap detection
  - trend and contradiction analysis
- Research design layer
  - research question generation
  - hypothesis formulation
  - methodology design
  - experimental or computational design
- Execution layer
  - Python analysis scripts
  - geospatial, statistical, and computational workflows
  - plotting and reporting
  - reproducible scientific output

## Recommended stack

- Python
- FastAPI
- Streamlit
- SQLAlchemy / PostgreSQL
- Celery + Redis
- Scopus API client
- Crossref + OpenAlex metadata
- Google Scholar discovery adapters
- GeoPandas, Rasterio, PyProj, Cartopy (for geospatial work)
- NumPy, SciPy, pandas, statsmodels
- Matplotlib, Seaborn, Plotly
- Zotero or BibTeX integration
- OpenAI or Anthropic model APIs
- Jupyter notebooks for exploratory analysis

## Domain-driven workflow

The system should support any scientific field by allowing the user to specify a domain and search scope. The same pipeline applies across disciplines:

1. Select a domain or topic
2. Search peer-reviewed journals only
3. Filter by journal quality and access availability
4. Collect metadata and full texts
5. Extract themes and identify gaps
6. Generate research questions
7. Choose a focused question
8. Build a review around that question
9. Develop the methodology
10. Implement analysis scripts
11. Run experiments or computational studies
12. Generate figures, tables, and graphs
13. Draft the final paper with references

## Example research domains

- Earth and environmental sciences
- geology and geophysics
- materials engineering
- chemical engineering
- mechanical engineering
- civil engineering
- electrical and electronic engineering
- computer science and AI
- biomedical engineering
- energy and sustainability systems

## Institutional access

The system is designed with an institution-aware access pattern:

- institutional login via SSO or access token
- institution-specific proxy and licensed database routing
- automatic handling of full-text availability status
- source prioritization based on licensed access and permissions
- secure handling of credentials through environment variables or a vault

## Folder structure

- app/
  - main.py
- src/science_research/
  - __init__.py
  - config.py
  - search/
    - __init__.py
    - sources.py
  - literature/
    - __init__.py
    - review_agent.py
  - core/
    - __init__.py
    - gap_analysis.py
    - methodology.py
  - analysis/
    - __init__.py
    - visualization.py
- docs/
- tests/
- .env.example
- requirements.txt

## Environment configuration

Copy `.env.example` to a local `.env` file and fill in the values relevant to your institution and APIs.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then launch the app:

```bash
uvicorn app.main:app --reload
```

## Notes

This repository is intentionally scaffolded to support expansion into a full science-and-engineering research assistant workflow. It is designed as a versatile foundation for multidisciplinary research, not a single-domain chatbot.

## License

MIT
