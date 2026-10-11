from __future__ import annotations

import httpx
from typing import List

from science_research.models.paper import Paper


class ScopusAdapter:
    """Real Scopus API integration using the REST API."""

    def __init__(self, api_key: str | None = None, institution_token: str | None = None):
        self.api_key = api_key
        self.institution_token = institution_token
        self.base_url = "https://api.elsevier.com/content/search/scopus"

    def search(self, query: str, *, domain: str = "general", limit: int = 20) -> List[Paper]:
        """Search Scopus API and return papers.
        
        Valid key: Returns real papers from Scopus
        Invalid/no key: Returns empty list (silently fails, falls back to Crossref/OpenAlex)
        """
        if not self.api_key:
            return []

        headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": self.api_key,
            "User-Agent": "ScienceResearchAssistant/0.1",
        }

        params = {
            "query": query,
            "count": min(limit, 200),  # Scopus limits per-page to 200
            "view": "COMPLETE",
            "sort": "-citedby-count",  # Sort by citation count descending
        }

        try:
            response = httpx.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=20.0,
            )
            
            # Check for authorization errors
            if response.status_code == 401:
                print("❌ Scopus API key invalid or expired")
                return []
            elif response.status_code == 403:
                print("❌ Scopus API key does not have search access")
                return []
            elif response.status_code != 200:
                print(f"❌ Scopus API error: {response.status_code}")
                return []
                
            response.raise_for_status()
        except httpx.TimeoutException:
            print("⚠️ Scopus API timeout - using fallback sources")
            return []
        except Exception as e:
            print(f"⚠️ Scopus API error: {e}")
            return []

        try:
            data = response.json()
        except Exception:
            print("⚠️ Could not parse Scopus response")
            return []

        papers: List[Paper] = []
        entries = data.get("search-results", {}).get("entry", [])
        
        if not entries:
            print("ℹ️ No results from Scopus for this query")
            return []

        for entry in entries[:limit]:
            try:
                # Extract fields from Scopus API response
                paper_id = entry.get("eid")
                title = entry.get("dc:title", "")
                authors_list = entry.get("dc:creator", [])
                if isinstance(authors_list, str):
                    authors = [authors_list]
                else:
                    authors = authors_list if authors_list else []
                
                year = entry.get("prism:coverDate", "")[:4] if entry.get("prism:coverDate") else None
                year = int(year) if year and year.isdigit() else None
                
                journal = entry.get("prism:publicationName", "")
                doi = entry.get("prism:doi", "")
                url = entry.get("link", [{}])[0].get("@href", "") if entry.get("link") else ""
                abstract = entry.get("dc:description", "")
                citation_count = entry.get("citedby-count", 0)
                citation_count = int(citation_count) if citation_count else 0
                
                # Extract keywords from entry
                keywords = [domain, "peer-reviewed", "scopus"]
                if entry.get("authkeywords"):
                    keywords.extend(entry.get("authkeywords", "").split(";"))

                papers.append(
                    Paper(
                        paper_id=f"scopus-{paper_id}",
                        title=title,
                        authors=authors,
                        year=year,
                        journal=journal,
                        doi=doi,
                        url=url,
                        abstract=abstract,
                        keywords=keywords[:10],  # Limit keywords
                        source="scopus",
                        peer_reviewed=True,
                        full_text_available=False,  # Depends on institutional access
                        access_type="licensed",
                        citation_count=citation_count,
                    )
                )
            except Exception as e:
                print(f"⚠️ Error parsing Scopus entry: {e}")
                continue

        print(f"✅ Retrieved {len(papers)} papers from Scopus")
        return papers
