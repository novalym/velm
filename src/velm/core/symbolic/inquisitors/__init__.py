# Path: src/scaffold/core/symbolic/inquisitors/__init__.py
# ---------------------------------------------------------
# LIF: ∞ | ROLE: SPECIALIST_REGISTRY_GATEWAY | RANK: SOVEREIGN
# AUTH: Ω_INQUISITOR_INIT_TOTALITY
# =========================================================================================

"""
=================================================================================
== THE INQUISITOR PHALANX (V-Ω-LOGIC-DYNAMICS)                                ==
=================================================================================
@gnosis:title The Phalanx of Specialists
@gnosis:stratum STRATUM-2 (CORTEX)
@gnosis:summary The collective of deterministic logic specialists.

This package orchestrates the specialized "Gaze" of the Symbolic Engine.
Each Inquisitor within this phalanx is a dedicated sovereign of a specific
industrial stratum (Money, Time, Law, Truth, Rejection).

[THE HIERARCHY OF ADJUDICATION]:
1. BOUNCER: Hard Rejection (Sovereignty over the Gate)
2. SCRIER: Urgent Triage (Sovereignty over Momentum)
3. BANKER: Fiscal Logic (Sovereignty over Capital)
4. LIBRARIAN: Factual Truth (Sovereignty over Knowledge)
5. CHRONOS: Temporal Physics (Sovereignty over Spacetime)
6. SENTINEL: Compliance Shield (Sovereignty over Law)
7. RETINA: Visual Inception (Sovereignty over Sight)
=================================================================================
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Type, TYPE_CHECKING

# --- THE ANCESTRAL CONTRACT ---
from .base import BaseInquisitor

# [ASCENSION 1]: TYPE-GUARDED ORCHESTRATION
# We use TYPE_CHECKING to allow IDE resonance without circular import heresies.
if TYPE_CHECKING:
    from .bouncer import BouncerInquisitor
    from .scrier import ScrierInquisitor
    from .banker import BankerInquisitor
    from .chronos import ChronosInquisitor
    from .librarian import LibrarianInquisitor
    from .sentinel import SentinelInquisitor
    from .retina import RetinaInquisitor

Logger = logging.getLogger("Scaffold:InquisitorPhalanx")

# =============================================================================
# == THE REGISTRY OF SOULS (JIT MAPPING)                                     ==
# =============================================================================

# [ASCENSION 5]: THE GHOST MAP
# We define the locations of the specialists to allow for dynamic materialization.
INQUISITOR_MAP: Dict[str, tuple[str, str]] = {
    "bouncer": ("scaffold::core::symbolic::inquisitors::bouncer", "BouncerInquisitor"),
    "scrier": ("scaffold::core::symbolic::inquisitors::scrier", "ScrierInquisitor"),
    "banker": ("scaffold::core::symbolic::inquisitors::banker", "BankerInquisitor"),
    "chronos": ("scaffold::core::symbolic::inquisitors::chronos", "ChronosInquisitor"),
    "librarian": ("scaffold::core::symbolic::inquisitors::librarian", "LibrarianInquisitor"),
    "sentinel": ("scaffold::core::symbolic::inquisitors::sentinel", "SentinelInquisitor"),
    "retina": ("scaffold::core::symbolic::inquisitors::retina", "RetinaInquisitor"),
}


class PhalanxConductor:
    """
    [THE CONDUCTOR]
    A stateless utility for materializing the Phalanx.
    """

    @staticmethod
    def summon_all(engine: Any) -> List[BaseInquisitor]:
        """
        [THE RITE OF SUMMONS]
        Materializes every specialist in the prescribed order of priority.
        """
        import importlib

        specialists = []

        # [THE CURE]: Linear Priority Iteration
        # Order is hardcoded to ensure Bouncer (Rejection) and Scrier (Emergency)
        # always gaze upon the matter first.
        priority_order = ["bouncer", "scrier", "banker", "chronos", "librarian", "sentinel", "retina"]

        for key in priority_order:
            module_path, class_name = INQUISITOR_MAP[key]

            # [THE IRON SUTURE]: Transmute the Sovereign Dot-Sigil back to Python paths
            # (Context: Architect's mandate for :: sigils)
            py_path = module_path.replace("::", ".")

            try:
                module = importlib.import_module(py_path)
                InquisitorClass = getattr(module, class_name)
                specialists.append(InquisitorClass(engine))

            except (ImportError, AttributeError) as fracture:
                # [ASCENSION 12]: FAULT-ISOLATED INCEPTION
                # A single missing specialist must not blind the entire Phalanx.
                Logger.critical(f"Ω_INQUISITOR_FRACTURE: Failed to lift {class_name} from the void. {fracture}")
                continue

        return specialists


# =========================================================================
# == SOVEREIGN EXPORT GATEWAY                                            ==
# =========================================================================

__all__ = [
    "BaseInquisitor",
    "PhalanxConductor",
    "INQUISITOR_MAP"
]

# == SCRIPTURE SEALED: THE PHALANX GATEWAY IS UNBREAKABLE ==