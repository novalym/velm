# Path: core/alchemist/elara/resolver/inclusion/engine.py
# -----------------------------------------------------------

import time
from typing import Any, List, Optional, TYPE_CHECKING
from .matter import MatterInceptor
from .mind import MindInhaler
from .forensics import InclusionTomographer

if TYPE_CHECKING:
    from ..context import LexicalScope


class InclusionEmissary:
    """
    =============================================================================
    == THE INCLUSION EMISSARY: OMEGA FACADE (V-Ω-TOTALITY-VMAX)                ==
    =============================================================================
    LIF: ∞^∞ | ROLE: MULTIVERSAL_REALITY_MERGER | RANK: OMEGA_SOVEREIGN_PRIME

    [THE MANIFESTO]
    The monolithic era is over. The Emissary is now a hyper-intelligent facade
    delegating to specialized organs for Matter Inception and Mind Inhalation.
    """

    def __init__(self, engine_ref: Any):
        """[THE RITE OF INCEPTION]"""
        self.engine = engine_ref

    # =========================================================================
    # == THE STATELESS PROXY GATES                                           ==
    # =========================================================================

    def conduct_include(self, path_str: str, scope: 'LexicalScope', ignore_missing: bool = False) -> str:
        """
        [MATTER INCEPTION]: Injects physical code matter into the stream.
        """
        start = time.perf_counter_ns()
        result = MatterInceptor.include(self, path_str, scope, ignore_missing)

        # [ASCENSION 10]: Metabolic Tomography
        tax = InclusionTomographer.record_tax(start)
        # (Internal telemetry can be added here)

        return result

    def conduct_import(self, path_str: str, alias: str, scope: 'LexicalScope'):
        """
        [MIND INHALATION]: Siphons logic and variables into a warded namespace.
        """
        MindInhaler.inhale_namespace(self, path_str, alias, scope)

    def conduct_from_import(self, path_str: str, targets: List[str], scope: 'LexicalScope'):
        """
        [SELECTIVE DESTRUCTURING]: Extracts specific atoms from a library.
        """
        MindInhaler.inhale_selective(self, path_str, targets, scope)

    def __repr__(self) -> str:
        return f"<Ω_INCLUSION_EMISSARY status=RESONANT mode=MULTIVERSAL_FUSION>"