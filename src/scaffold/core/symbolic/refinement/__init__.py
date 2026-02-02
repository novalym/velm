# Path: src/scaffold/core/symbolic/refinement/__init__.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: LINGUISTIC_REFINEMENT_GATEWAY | RANK: SOVEREIGN
# AUTH: Ω_REFINEMENT_INIT_TOTALITY
# =========================================================================================

"""
=================================================================================
== THE REFINEMENT STRATUM (V-Ω-LINGUISTIC-SYNERGY)                            ==
=================================================================================
@gnosis:title The Refinement Package
@gnosis:stratum STRATUM-1 (LINGUISTIC LENS)
@gnosis:summary The bicameral gateway for text deconstruction and synthesis.

This package orchestrates the "Linguistic Cycle" of the Symbolic Engine.
It houses the dual-organs of Gnostic Perception and Alchemical Emission.

[THE REFINEMENT CYCLE]:
1. THE PURIFIER: Smashes high-entropy raw text into Gnostic Atoms.
2. THE ALCHEMIST: Transfigures deterministic logic into humanized scripture.

[METABOLIC PHILOSOPHY]:
Logic without Voice is cold; Voice without Logic is hollow.
The Refinement Stratum ensures that the Monolith speaks with the absolute
authority of its Industrial Grimoire while maintaining the human warmth
required for conversion.
=================================================================================
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

# --- I. THE PRIMARY ORGANS ---
from .purifier import GnosticPurifier
from .alchemist import GnosticAlchemist

# [ASCENSION 1]: TYPE-GUARDED SYNERGY
# Enables IDE resonance while preventing circular dependency fractures.
if TYPE_CHECKING:
    from ..contracts import GnosticAtom, SymbolicManifest

Logger = logging.getLogger("Scaffold:Refinement")

# =============================================================================
# == II. THE REFINEMENT GAZE (UNIFIED INTERFACE)                             ==
# =============================================================================

class RefinementGaze:
    """
    [THE UNIFIED LENS]
    A sovereign utility that wraps the Purifier and Alchemist into
    a single metabolic unit.
    """

    def __init__(self):
        self.purifier = GnosticPurifier()
        self.alchemist = GnosticAlchemist()
        self.version = "1.0.0-TOTALITY"

    def deconstruct(self, raw_text: str) -> Tuple[str, List[GnosticAtom]]:
        """
        [THE RITE OF PERCEPTION]
        Direct delegation to the Purifier to extract atomic intent.
        """
        return self.purifier.purify_and_atomize(raw_text)

    def manifest(self,
                 manifest: SymbolicManifest,
                 strata: Dict[str, Any],
                 context: Dict[str, Any]) -> str:
        """
        [THE RITE OF EXPRESSION]
        Direct delegation to the Alchemist to forge the final phonic matter.
        """
        return self.alchemist.transmute(manifest, strata, context)


# =========================================================================
# == III. SOVEREIGN EXPORT GATEWAY                                       ==
# =========================================================================

__all__ = [
    "GnosticPurifier",
    "GnosticAlchemist",
    "RefinementGaze"
]

# == SCRIPTURE SEALED: THE REFINEMENT GATEWAY IS UNBREAKABLE ==