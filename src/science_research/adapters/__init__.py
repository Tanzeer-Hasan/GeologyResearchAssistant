from .crossref_adapter import CrossrefAdapter
from .institutional_adapter import InstitutionalAdapter
from .openalex_adapter import OpenAlexAdapter
from .scholar_adapter import GoogleScholarAdapter
from .scopus_adapter import ScopusAdapter

__all__ = [
    "ScopusAdapter",
    "CrossrefAdapter",
    "OpenAlexAdapter",
    "GoogleScholarAdapter",
    "InstitutionalAdapter",
]
