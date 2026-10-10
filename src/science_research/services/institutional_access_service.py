from __future__ import annotations

import os
from typing import Any, Dict


class InstitutionalAccessService:
    """Provides institutional access status and configuration for paper discovery."""

    def __init__(self):
        self.institution_name = os.getenv("INSTITUTION_NAME")
        self.proxy_url = os.getenv("INSTITUTION_PROXY_URL")
        self.sso_enabled = os.getenv("INSTITUTION_SSO_ENABLED", "false").lower() == "true"
        self.scopus_api_key = os.getenv("SCOPUS_API_KEY")
        self.scopus_inst_token = os.getenv("SCOPUS_INST_TOKEN")

    def status(self) -> Dict[str, Any]:
        return {
            "institution_name": self.institution_name,
            "proxy_configured": bool(self.proxy_url),
            "sso_enabled": self.sso_enabled,
            "scopus_api_configured": bool(self.scopus_api_key),
            "scopus_inst_token_configured": bool(self.scopus_inst_token),
            "access_mode": "licensed" if self.institution_name or self.proxy_url else "open",
        }
