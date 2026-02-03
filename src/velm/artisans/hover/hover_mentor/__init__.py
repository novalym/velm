# Path: scaffold/artisans/hover/hover_mentor/__init__.py
# -----------------------------------------------------

"""
=================================================================================
== THE HIGH CONDUCTOR OF WISDOM (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)      ==
=================================================================================
LIF: INFINITY (THE UNBREAKABLE VOICE)

The sovereign entry point for the Mentorship Sub-Sanctum. It orchestrates the
Trinity of Guidance (Grimoire, Inquisitor, Warden) and performs the Rite of
Ranking to ensure the most critical Gnosis (Security) is proclaimed first.
=================================================================================
"""
from typing import List, Dict, Any, Optional
from .grimoire import STATIC_GRIMOIRE
from .inquisitor import ContextualInquisitor
from .warden import SecurityWarden


class HoverMentor:
    """The Supreme Orchestrator of Gnostic Guidance."""

    @staticmethod
    def get_guidance(token: str, context_lines: List[str], line_idx: int) -> List[str]:
        """
        The Grand Rite of Revelation.
        Synthesizes static law, contextual logic, and security strictures.
        """
        # 1. The Gaze of the Warden (Priority: CRITICAL)
        # Security always takes precedence in the Gnostic timeline.
        warden = SecurityWarden(token, context_lines, line_idx)
        security_findings = warden.judge()

        # 2. The Gaze of the Inquisitor (Priority: WARNING/INFO)
        # Analyzes structural integrity and best practices.
        inquisitor = ContextualInquisitor(token, context_lines, line_idx)
        contextual_findings = inquisitor.analyze()

        # 3. The Gaze of the Grimoire (Priority: REFERENCE)
        # Static definitions from the standard library.
        static_wisdom = STATIC_GRIMOIRE.get(token, [])

        # --- THE RITE OF RANKING ---
        # We order the proclamation: Security -> Logic -> Reference
        full_dossier = security_findings + contextual_findings + static_wisdom

        return full_dossier


# The Public Gateway
def get_mentors_guidance(token: str, context_lines: List[str], line_idx: int = 0) -> List[str]:
    """The definitive gateway for the HoverHierophant."""
    return HoverMentor.get_guidance(token, context_lines, line_idx)