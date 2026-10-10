# Science and Engineering Research Assistant — System Design

## 1. Goal

Build a modular research assistant for science and engineering that helps researchers from literature discovery through final scientific reporting. The system must:

- search only peer-reviewed literature
- respect institutional access and licensing
- identify research gaps
- formulate research questions and hypotheses
- design methods and experiments
- execute code and analyses
- generate figures, tables, and graphs
- write a manuscript with citations

This is not a general-purpose chatbot. It is a research workflow engine.

## 2. High-level architecture

The system is organized into six layers:

1. Source Access Layer
2. Screening and Metadata Layer
3. Literature Intelligence Layer
4. Research Design Layer
5. Execution and Analysis Layer
6. Reporting and Publication Layer

Each layer is independent and can be extended by domain-specific adapters.

## 3. Core components

### 3.1 Source Access Layer

Responsibilities:
- Discover peer-reviewed sources
- Route queries to appropriate metadata providers
- Respect institutional access rules
- Detect full-text availability and licensing

Primary modules:
- SearchProviderRegistry
- ScopusClient
- CrossrefClient
- OpenAlexClient
- GoogleScholarAdapter
- InstitutionalAccessManager
- DOIResolver

Design notes:
- Google Scholar is treated as a discovery mechanism, not the only authoritative source.
- Scopus and institutional repositories are preferred for structured metadata.
- Access is determined by institution credentials, SSO, or proxy configuration.

### 3.2 Screening and Metadata Layer

Responsibilities:
- normalize paper metadata
- filter journal and paper types
- remove duplicates
- score relevance and quality
- identify accessibility status

Primary modules:
- PaperNormalizer
- JournalFilter
- DuplicateRemover
- RelevanceScorer
- EvidenceQualityInspector
- AccessStatusChecker

Metadata stored per paper:
- title
- authors
- year
- journal
- volume
- issue
- pages
- DOI
- abstract
- keywords
- URL
- source
- peer_reviewed
- full_text_available
- access_type
- citation_count

### 3.3 Literature Intelligence Layer

Responsibilities:
- summarize literature
- extract themes and topics
- detect gaps and contradictions
- cluster papers by subfield or method
- build evidence maps

Primary modules:
- LiteratureSummarizer
- TopicExtractor
- TrendAnalyzer
- GapDetector
- ContradictionAnalyzer
- ConceptMapBuilder

Typical outputs:
- annotated literature summary
- topic clusters
- evidence matrix
- identified research gaps
- chronological trends

### 3.4 Research Design Layer

Responsibilities:
- turn literature gaps into research questions
- propose hypotheses
- choose method families
- formulate experimental or computational design
- evaluate feasibility

Primary modules:
- ResearchQuestionGenerator
- HypothesisFormulator
- MethodologyPlanner
- DomainMethodLibrary
- StudyDesignEngine
- FeasibilityChecker

This layer connects evidence to a concrete research plan.

### 3.5 Execution and Analysis Layer

Responsibilities:
- ingest datasets and files
- run analysis pipelines
- validate models and results
- create figures, maps, tables, and graphs
- generate reproducible scientific outputs

Primary modules:
- DataLoader
- Preprocessor
- AnalysisRunner
- StatisticalModeler
- MachineLearningPipeline
- SimulationEngine
- VisualizationEngine
- UncertaintyAnalyzer

Supported domains:
- earth and environmental sciences
- materials science
- chemistry and chemical engineering
- physics and applied physics
- civil, mechanical, and electrical engineering
- energy systems
- biomedical and life sciences
- computer science and applied AI

### 3.6 Reporting and Publication Layer

Responsibilities:
- write review and original research drafts
- structure paper sections
- generate citations and references
- compile tables and figures
- maintain manuscript history

Primary modules:
- LiteratureReviewWriter
- ManuscriptAssembler
- CitationManager
- ReferenceFormatter
- FigureBinder
- ResultsSummaryWriter

Outputs:
- review paper draft
- research proposal
- full manuscript
- figures and tables
- bibliography

## 4. Core data model

### 4.1 Project
A project captures a research objective.

Fields:
- project_id
- title
- domain
- description
- status
- created_at
- updated_at

### 4.2 Topic
A topic is the research theme loaded into the system.

Fields:
- topic_id
- project_id
- name
- keywords
- scope
- inclusion_criteria
- exclusion_criteria

### 4.3 Paper
A normalized record for each literature item.

Fields:
- paper_id
- topic_id
- title
- authors
- year
- journal
- abstract
- doi
- url
- source
- peer_reviewed
- accessibility
- citation_count
- keywords
- notes

### 4.4 ResearchQuestion
A question generated from the literature gap.

Fields:
- question_id
- project_id
- text
- rationale
- evidence_basis
- novelty_score
- priority

### 4.5 Methodology
A proposed workflow for the chosen problem.

Fields:
- methodology_id
- project_id
- question_id
- design_type
- data_sources
- analysis_methods
- validation_strategy
- assumptions

### 4.6 Experiment
A concrete execution instance.

Fields:
- experiment_id
- project_id
- methodology_id
- code_path
- dataset_path
- status
- results_path
- generated_figures

### 4.7 Figure and Table
Scientific output artifacts.

Fields:
- artifact_id
- project_id
- type
- title
- source
- file_path
- caption

## 5. Research workflow

### Stage 1: Define the domain and topic
- choose scientific field
- define research objective
- set search terms and inclusion criteria
- enable institutional access if needed

### Stage 2: Literature discovery
- query peer-reviewed sources
- collect metadata from Scopus / Crossref / OpenAlex / Google Scholar adapter
- route queries to institutionally accessible vendors first
- store results in a normalized database

### Stage 3: Screening and filtering
- remove non-peer-reviewed items
- remove duplicates
- filter by date, language, and field relevance
- retain only valid papers with metadata and abstract

### Stage 4: Literature synthesis
- summarize each paper
- classify by topic or method
- build evidence map
- identify gaps, contradictions, and opportunities

### Stage 5: Research question generation
- generate 5-20 candidate questions
- rank questions by novelty, feasibility, and impact
- select the strongest question

### Stage 6: Methodology design
- choose variables, datasets, and models
- specify validation approach
- define hypotheses
- define reproducible analysis plan

### Stage 7: Code and execution
- implement preprocessing and analysis scripts
- run analyses
- validate and debug results
- generate figures and tables

### Stage 8: Reporting
- write methodology section
- summarize results
- produce discussion and conclusion
- generate references and citations
- assemble final paper draft

## 6. Domain adaptation model

The core engine remains the same across all scientific domains, but each domain gets a domain adapter.

Examples:
- geoscience adapter: maps, geophysical datasets, cross-sections
- materials adapter: microstructure, mechanical testing, characterization data
- engineering adapter: design of experiments, simulation models, performance metrics
- chemistry adapter: reaction mechanisms, spectroscopy, thermodynamics
- computational science adapter: benchmark datasets, model validation, reproducibility metrics

This keeps the system general while allowing deep specialization.

## 7. Security and institutional access

The system should support:
- SSO or institution login
- access-token configuration
- license-aware source routing
- secure storage of secrets in environment variables or vaults
- explicit message when a paper is inaccessible

Do not expose credentials in project files.

## 8. Technical stack

Recommended stack:
- Python
- FastAPI
- Streamlit or React frontend
- PostgreSQL
- Redis + Celery
- SQLAlchemy
- OpenAI / Anthropic APIs
- Crossref + OpenAlex + Scopus integrations
- Pandas, NumPy, SciPy, statsmodels
- GeoPandas, Rasterio, PyProj for geospatial cases
- Matplotlib, Seaborn, Plotly
- Zotero or BibTeX for citations

## 9. Proposed module layout

```text
src/science_research/
  __init__.py
  config.py
  models/
    project.py
    paper.py
    question.py
    methodology.py
    experiment.py
  services/
    search_service.py
    screening_service.py
    review_service.py
    gap_service.py
    methodology_service.py
    analysis_service.py
    reporting_service.py
  adapters/
    scopus_adapter.py
    crossref_adapter.py
    openalex_adapter.py
    scholar_adapter.py
    institutional_adapter.py
    domain_adapter.py
  workflows/
    literature_workflow.py
    research_design_workflow.py
    execution_workflow.py
    reporting_workflow.py
  tools/
    citation_manager.py
    visualization.py
    file_manager.py
  api/
    routes.py
    schemas.py
```

## 10. Implementation roadmap

### Phase 1: Foundation
- project bootstrap
- configuration and environment management
- database schema
- domain definitions
- abstract API and service interfaces

### Phase 2: Source discovery
- search adapters
- metadata normalization
- institutional access logic
- paper storage

### Phase 3: Literature review engine
- relevance scoring
- screening workflow
- summary generation
- trend analysis and gap detection

### Phase 4: Research design engine
- question generation
- hypothesis formation
- methodology planning
- domain-specific method libraries

### Phase 5: Analysis pipeline
- dataset ingestion
- reproducible execution
- figure and table generation
- validation steps

### Phase 6: Final reporting
- manuscript generation
- reference formatting
- compiled draft and summary outputs

## 11. Success criteria

The project is successful when it can:

- search peer-reviewed literature across multiple sources
- identify relevant papers including institutional access cases
- detect a meaningful gap in a research area
- generate at least several high-quality research questions
- select a question and create a method plan
- execute code to analyze data or simulate results
- create graphs and tables from evidence
- produce a structured scientific paper draft with references

## 12. Recommended next step

Implement the first milestone:

- project and configuration skeleton
- Paper model and metadata schema
- SearchProvider abstraction
- InstitutionalAccessManager
- Screening pipeline skeleton
- Review orchestration API route

This gives a stable foundation before the more advanced research design and analysis stages.
