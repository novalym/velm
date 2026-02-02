# Path: scaffold/artisans/services/clerk/domains/base.py
# -------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from ..client import ClerkClient
from .....logger import Scribe

class BaseClerkDomain(ABC):
    """
    =============================================================================
    == THE BASE CLOISTER (V-Ω-IDENTITY-CONTRACT)                               ==
    =============================================================================
    LIF: ∞ | ROLE: ABSTRACT_IDENTITY_GOVERNOR | RANK: LEGENDARY

    The foundational blueprint for all Clerk capability strata.
    Provides alchemical utilities for metadata manipulation and error shielding.
    """

    def __init__(self, client: ClerkClient, engine: Any):
        self.client = client
        self.engine = engine
        self.logger = Scribe("ClerkDomain")
    @abstractmethod
    def execute(self, request: Any) -> Any:
        """The core rite of the domain."""
        pass

    def _merge_metadata(self, existing: Optional[Dict], incoming: Optional[Dict]) -> Dict:
        """
        [THE RITE OF ACCUMULATION]
        Ensures new Gnosis is woven into existing metadata without
        annihilating previous truths.
        """
        base = existing or {}
        if not incoming:
            return base

        # Perform deep merge (non-recursive for flat Clerk metadata)
        return {**base, **incoming}

    def _handle_rejection(self, res: Dict[str, Any]) -> str:
        """Transmutes raw Clerk errors into Socratic Heresies."""
        if isinstance(res, dict) and res.get("error"):
            body = res.get("body", {})
            errors = body.get("errors", [])
            if errors:
                return f"{errors[0].get('message')} (Code: {errors[0].get('code')})"
            return str(body)
        return "Unknown Identity Paradox."