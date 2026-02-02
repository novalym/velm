# Path: core/artisans/analyze/static_inquisitor/inquisitor.py
# -----------------------------------------------------------

import traceback
import sys
import uuid
from typing import List, Dict, Any, Optional

# --- THE DIVINE SUMMONS OF THE PANTHEON ---
from .detectors.variables import VariableDetector
from .detectors.paths import PathDetector
from .detectors.atomic import AtomicDetector

from ....contracts.data_contracts import ScaffoldItem, GnosticDossier
from ....jurisprudence_core.jurisprudence import forge_heresy_vessel
from ....logger import Scribe

Logger = Scribe("ForensicInquisitor")


class StaticInquisitor:
    """
    =================================================================================
    == THE GRAND ADJUDICATOR (V-Ω-MODULAR-ORCHESTRATOR-FINALIS)                    ==
    =================================================================================
    LIF: ∞ (THE UNIFIED MIND)

    The Central Intelligence that coordinates the specialized Detectors.
    It guarantees that a fracture in one detector does not blind the others.
    """

    def __init__(self, grammar: str, alchemist=None):
        self.grammar = grammar
        self.alchemist = alchemist

        # --- THE PANTHEON OF DETECTORS ---
        self.detectors = [
            VariableDetector(grammar),
            PathDetector(grammar),
            AtomicDetector(grammar),
        ]

    def audit(self, content: str, variables: Dict, items: List[ScaffoldItem],
              edicts: List, dossier: GnosticDossier) -> List[Dict[str, Any]]:

        # [ASCENSION 1]: FORENSIC LOGGING
        # sys.stderr.write(f"[Inquisitor] Auditing {len(items)} items with {self.grammar} laws.\n")

        all_diagnostics = []

        # --- THE RITE OF DELEGATION ---
        for detector in self.detectors:
            try:
                # The detector performs its specialized gaze
                results = detector.detect(content, variables, items, edicts, dossier)
                if results:
                    all_diagnostics.extend(results)

            except Exception as e:
                # --- THE WARD OF RESILIENCE ---
                # A failure in one detector must not blind the entire Inquisitor.
                Logger.error(f"Detector '{type(detector).__name__}' shattered: {e}", exc_info=True)

                # Also print to stderr for the LSP Bridge to capture
                sys.stderr.write(f"[Inquisitor] 💥 Detector Fracture ({type(detector).__name__}): {e}\n")

                # We proclaim a Meta-Heresy to warn the Architect of the tool failure
                all_diagnostics.append(self._forge_meta_heresy(e, detector))

        return all_diagnostics

    def _forge_meta_heresy(self, error: Exception, detector: Any) -> Dict[str, Any]:
        """
        Forges a special heresy when a Detector crashes.
        """
        tb = traceback.format_exc()
        detector_name = type(detector).__name__

        # Use the raw forge function since we are outside a detector class context
        vessel = forge_heresy_vessel(
            key="META_HERESY_DETECTOR_FAILURE",
            line_num=0,
            line_content=f"Detector: {detector_name}",
            details=f"Internal Analysis Error in {detector_name}: {str(error)}\n{tb}",
            internal_line=0
        )

        return {
            "message": vessel.message,
            "severity": 1,  # CRITICAL
            "internal_line": 0,
            "source": "StaticInquisitor",
            "code": "META_HERESY",
            "details": vessel.details,
            "suggestion": "Report this bug to the Scaffold Architects.",
            "data": {
                "error": str(error),
                "traceback": tb,
                "detector": detector_name
            }
        }