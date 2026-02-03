# Path: artisans/analyze/static_inquisitor/detectors/base.py
# ----------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
import re

from .....contracts.data_contracts import ScaffoldItem, GnosticDossier
from .....contracts.heresy_contracts import HeresySeverity
from .....jurisprudence_core.jurisprudence import forge_heresy_vessel


class BaseDetector(ABC):
    """
    =============================================================================
    == THE ANCESTRAL SOUL OF DETECTION (V-Ω-STRICT-TYPING-ULTIMA)              ==
    =============================================================================
    LIF: 10,000,000,000 (THE UNBREAKABLE CONTRACT)

    The abstract base class for all Logic Detectors.
    It provides the standardized `_forge_diagnostic` rite, which acts as a
    sanitizing firewall between internal Python logic and external LSP requirements.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **The Severity Normalizer:** Strictly maps strings ('CRITICAL') and raw integers
        to valid LSP Severity codes (1=Error, 2=Warning, 3=Info, 4=Hint).
        Annihilates "Severity 8" heresies.
    2.  **The Geometric Adjuster:** Automatically converts 1-based Human line numbers
        to 0-based Machine line numbers, preventing off-by-one rendering errors.
    3.  **The Markup Stripper:** Removes rich console tags (`[bold]`) from messages
        so they appear clean in the Editor's Problems panel.
    4.  **The Contextual Bridge:** Ensures `data` payload always contains the `heresy_key`
        and `suggestion`, essential for the `RepairArtisan` to function.
    """

    def __init__(self, grammar: str):
        self.grammar = grammar

    @abstractmethod
    def detect(self,
               content: str,
               variables: Dict,
               items: List[ScaffoldItem],
               edicts: List,
               dossier: GnosticDossier) -> List[Dict[str, Any]]:
        """
        The Rite of Detection.
        Must return a list of diagnostic dictionaries ready for the Inquisitor.
        """
        pass

    def _forge_diagnostic(self, key: str, line: int, item: Optional[ScaffoldItem], data: Dict = None) -> Dict:
        """
        [THE RITE OF FORGING]
        Transmutes a raw finding into a pure, LSP-compliant Diagnostic Dictionary.
        """
        # 1. Fallback for Line Content
        line_content = item.raw_scripture if item else "Gnostic Hierarchy"

        # 2. Geometric Safety: Ensure line is an integer and non-negative
        # Input 'line' is expected to be 0-indexed logic from the detector.
        # However, for display in human logs (forge_heresy_vessel), we need 1-based.
        safe_internal_line = max(0, int(line) if line is not None else 0)
        safe_human_line = safe_internal_line + 1

        details = data.get("details") if data else None
        severity_label = data.get("severity_override", "WARNING")

        # 3. Summon the Heresy Vessel (For text generation)
        vessel = forge_heresy_vessel(
            key=key,
            line_num=safe_human_line,
            line_content=line_content,
            details=details,
            internal_line=safe_internal_line
        )

        # 4. The Severity Filter (The Fix for Severity 8)
        # LSP Standard: 1=Error, 2=Warning, 3=Info, 4=Hint
        severity_map = {
            "CRITICAL": 1,
            "ERROR": 1,
            "WARNING": 2,
            "INFO": 3,
            "HINT": 4,
            "1": 1, "2": 2, "3": 3, "4": 4
        }

        # Handle raw integers or strings
        raw_sev = str(severity_label).upper()

        if raw_sev in severity_map:
            bridge_severity = severity_map[raw_sev]
        else:
            # Fallback for unknown severities (like 8)
            bridge_severity = 2

            # 5. Message Sanitization (Remove [bold] tags for VS Code display)
        clean_message = re.sub(r'\[/?\w+\]', '', vessel.message)

        # 6. The Final Vessel
        return {
            "message": clean_message,
            "severity": bridge_severity,
            "internal_line": safe_internal_line,
            "source": self.__class__.__name__,
            "code": key,
            "details": vessel.details,
            "suggestion": vessel.suggestion,
            # Ensure 'data' is never None and contains the keys for the Healer
            "data": {
                **(data or {}),
                "heresy_key": key,
                "suggestion": vessel.suggestion
            }
        }