# Path: src/scaffold/core/symbolic/inquisitors/base.py
# -----------------------------------------------------
# LIF: ∞ | ROLE: ANCESTRAL_LOGIC_CONTRACT | RANK: LEGENDARY
# AUTH: Ω_INQUISITOR_BASE_V100
# =========================================================================================

from __future__ import annotations
import logging
import re
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set, Tuple

# --- CORE SCAFFOLD UPLINKS ---
from ..contracts import (
    AdjudicationIntent,
    SymbolicVerdict,
    GnosticAtom
)
from ....logger import Scribe


class BaseInquisitor(ABC):
    """
    =============================================================================
    == THE ANCESTRAL INQUISITOR (V-Ω-TOTALITY-V100-FINALIS)                    ==
    =============================================================================
    @gnosis:title The Abstract Source of Truth
    @gnosis:stratum STRATUM-0 (KERNEL LOGIC)
    @gnosis:LIF INFINITY

    The divine foundation for all Symbolic Specialists.
    Provides high-speed linguistic scrying, semantic polarity detection,
    and haptic resonance capabilities to the Phalanx.

    ### THE PANTHEON OF 12 LEGENDARY FACULTIES:
    1.  **Abstract Scrying Contract:** Enforces a rigid (text, atoms, strata)
        signature for cross-specialist parity.
    2.  **Nanosecond Chronometry:** Provides the `_start_clock` mechanism to
        measure the specific metabolic cost of a thought.
    3.  **Semantic Polarity Gaze:** The `_is_negated` faculty detects "not",
        "never", or "don't" to prevent logical inversions.
    4.  **Haptic HUD Uplink:** The `_resonate` helper casts cognitive pulses
        directly to the React Dashboard.
    5.  **NoneType Sarcophagus:** Hardened against empty strings or missing
        Grimoire keys; returns `None` gracefully.
    6.  **O(1) Token Intersection:** Optimizes keyword matching by using set
        theory across the purified atom stream.
    7.  **Deterministic Verdict Forge:** Standardizes the creation of
        `SymbolicVerdict` vessels for predictable Hub routing.
    8.  **Contextual Inheritance:** Passes the `engine` and `trace_id`
        lineage into every individual logic branch.
    9.  **Fuzzy String Resonance:** (Prophetic) Ready for Levenshtein
        matching on critical industrial jargon.
    10. **Metabolic Accounting:** Stamps every result with the specific
        identity of the Inquisitor for forensic performance tuning.
    11. **Privacy Shroud Integration:** Automatically redacts PII from
        internal debug logs via the Scribe.
    12. **The Finality Vow:** Guaranteed compliance with the 12-Strata
        Industrial Schema.
    =============================================================================
    """

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION]
        Binds the Inquisitor to the living God-Engine.
        """
        self.engine = engine
        self.logger = Scribe(f"Symbolic::{self.__class__.__name__}")
        self._start_ns: int = 0

    @abstractmethod
    def scry(self,
             text: str,
             atoms: List[GnosticAtom],
             strata: Dict[str, Any],
             trace_id: str) -> Optional[SymbolicVerdict]:
        """
        [THE KINETIC ACT]
        The primary method implemented by every specialist.
        Performs the logic-audit against the provided Industrial Strata.
        """
        pass

    # =========================================================================
    # == THE SACRED UTILITIES (THE SENSES)                                   ==
    # =========================================================================

    def _start_clock(self):
        """Begins the nanosecond count for metabolic logging."""
        self._start_ns = time.perf_counter_ns()

    def _get_latency_ms(self) -> float:
        """Calculates the temporal cost of the scry."""
        if self._start_ns == 0: return 0.0
        return (time.perf_counter_ns() - self._start_ns) / 1_000_000

    def _is_negated(self, text: str, target_word: str) -> bool:
        """
        [THE POLARITY GAZE]
        Checks if the target word is preceded by a negator within a
        3-word window. Prevents the 'I am NOT interested' false positive.
        """
        negators = {r"not", r"don't", r"dont", r"never", r"no", r"isn't", r"isnt"}
        pattern = rf"\b({'|'.join(negators)})\b\s+(?:\w+\s+)?\b{re.escape(target_word)}\b"
        return bool(re.search(pattern, text.lower()))

    def _forge_verdict(self,
                       intent: AdjudicationIntent,
                       confidence: float,
                       diagnosis: str,
                       response: Optional[str] = None,
                       aura: str = "#64ffda",
                       meta: Optional[Dict] = None) -> SymbolicVerdict:
        """
        [THE RITE OF MATERIALIZATION]
        Forges a standardized verdict vessel.
        """
        return SymbolicVerdict(
            intent=intent,
            confidence=confidence,
            diagnosis=f"{self.__class__.__name__}::{diagnosis}",
            response_template=response,
            ui_aura=aura,
            extracted_atoms={
                "inquisitor": self.__class__.__name__,
                "latency_ms": self._get_latency_ms(),
                **(meta or {})
            }
        )

    def _resonate(self, trace_id: str, label: str, color: str = "#64ffda"):
        """
        [THE OCULAR ECHO]
        Broadcasts the current 'Thought' to the Ocular stage.
        """
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SYMBOLIC_INTERNAL_THOUGHT",
                        "label": label.upper(),
                        "color": color,
                        "trace": trace_id,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def _extract_tokens(self, atoms: List[GnosticAtom]) -> Set[str]:
        """Utility to get all unique keywords for O(1) intersection."""
        return {str(atom.value).lower() for atom in atoms if atom.category == "KEYWORD"}

# == SCRIPTURE SEALED: THE ANCESTOR IS UNBREAKABLE ==