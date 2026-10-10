import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    app_name: str = Field(default="ScienceAndEngineeringResearchAssistant")
    app_env: str = Field(default="development")
    app_port: int = Field(default=8000)
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    llm_model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    scopus_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("SCOPUS_API_KEY"))
    scopus_inst_token: Optional[str] = Field(default_factory=lambda: os.getenv("SCOPUS_INST_TOKEN"))
    institution_name: Optional[str] = Field(default_factory=lambda: os.getenv("INSTITUTION_NAME"))
    institution_proxy_url: Optional[str] = Field(default_factory=lambda: os.getenv("INSTITUTION_PROXY_URL"))
    institution_sso_enabled: bool = Field(default_factory=lambda: os.getenv("INSTITUTION_SSO_ENABLED", "false").lower() == "true")
    google_scholar_enabled: bool = Field(default_factory=lambda: os.getenv("GOOGLE_SCHOLAR_ENABLED", "false").lower() == "true")
    crossref_email: Optional[str] = Field(default_factory=lambda: os.getenv("CROSSREF_EMAIL"))
    openalex_email: Optional[str] = Field(default_factory=lambda: os.getenv("OPENALEX_EMAIL"))
    zotero_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ZOTERO_API_KEY"))
    zotero_library_id: Optional[str] = Field(default_factory=lambda: os.getenv("ZOTERO_LIBRARY_ID"))
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./research.db"))
    secret_key: str = Field(default_factory=lambda: os.getenv("SECRET_KEY", "change-me"))


settings = Settings()
