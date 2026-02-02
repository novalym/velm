# Path: src/scaffold/core/symbolic/sutures/__init__.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: DECISION_GATEWAY_REGISTRY | RANK: SOVEREIGN
# AUTH: Ω_SUTURES_INIT_TOTALITY
# =========================================================================================

"""
=================================================================================
== THE SUTURES STRATUM (V-Ω-COGNITIVE-ROUTING)                                 ==
=================================================================================
@gnosis:title The Sutures Package
@gnosis:stratum STRATUM-2 (CORTEX DECISION)
@gnosis:summary The final adjudicators that bridge Symbolic and Neural logic.

This package orchestrates the "Handover Logic" of the God-Engine. It houses
the sovereign gates that decide how the machine's energy (Metabolic Tax) is
spent across Linguistic and Visual horizons.

[THE SUTURE PHALANX]:
1. NEURAL_BRIDGE: Governs the transition from Deterministic to Generative text.
2. VISION_GATE: Governs the transition from Symbolic to Multimodal perception.
=================================================================================
"""

from __future__ import annotations
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

# --- I. THE SOVEREIGN GATES ---
from .neural_bridge import NeuralBridge
from .vision_gate import VisionGate

# [ASCENSION 1]: TYPE-GUARDED ORCHESTRATION
if TYPE_CHECKING:
    from ..contracts import SymbolicManifest

Logger = logging.getLogger("Scaffold:SymbolicSutures")

# =============================================================================
# == II. THE SUTURE LENS (UNIFIED INTERFACE)                                ==
# =============================================================================

class SutureLens:
    """
    [THE MASTER ADJUDICATOR]
    A sovereign utility that manages the high-level handoff logic
    between the different cognitive hemispheres.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.bridge = NeuralBridge(engine)
        self.gate = VisionGate(engine)
        self.version = "1.0.0-TOTALITY"

    def determine_path(self, manifest: SymbolicManifest, lead_text: str) -> bool:
        """
        [THE DECISION RITE]
        Shortcut to determine if AI is needed for the current text plea.
        """
        should_use_ai, rationale = self.bridge.adjudicate_handoff(manifest, lead_text)
        Logger.debug(f"[{manifest.trace_id}] Suture Decision: AI={should_use_ai} | {rationale}")
        return should_use_ai


# =========================================================================
# == III. SOVEREIGN EXPORT GATEWAY                                       ==
# =========================================================================

__all__ = [
    "NeuralBridge",
    "VisionGate",
    "SutureLens"
]

# == SCRIPTURE SEALED: THE SUTURE GATEWAY IS UNBREAKABLE ==