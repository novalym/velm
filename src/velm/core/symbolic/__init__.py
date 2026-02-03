# Path: src/scaffold/core/symbolic/__init__.py
# ---------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_API_GATEWAY | RANK: SOVEREIGN
# AUTH: Ω_SYMBOLIC_INIT_TOTALITY_FINALIS
# =========================================================================================

"""
=================================================================================
== THE SYMBOLIC SINGULARITY ENGINE (SSE)                                       ==
=================================================================================
@gnosis:title Gnostic Symbolic Engine (GSE)
@gnosis:stratum STRATUM-2 (CORTEX)
@gnosis:LIF 1,000,000x
@gnosis:summary The iron guard of the God-Engine. A deterministic pre-processor
                that resolves industrial intent using the 13-Strata Grimoire.

This package provides the deterministic "Brainstem" for the Novalym Monolith
and the greater Scaffold Ecosystem. It is designed to achieve absolute cognitive
accuracy with zero latency and zero API cost by enforcing the laws of industrial
physics before neural inference is ever invoked.

[THE DOCTRINE OF SYMBOLIC SUPREMACY]:
1. PERCEPTION: Transmute raw text into Gnostic Atoms (Purifier).
2. ADJUDICATION: Conduct the Atoms through the Inquisitor Phalanx (Engine).
3. BIFURCATION: Decide between Instant Reflex or Neural Inception (Bridge).
4. PROJECTION: Cast the internal logic to the Ocular stage (Telemetry).
=================================================================================
"""

from __future__ import annotations
import threading
import logging
import weakref
from typing import Any, Dict, Optional, Tuple, Union, List, TYPE_CHECKING

# --- I. THE CORE INTELLIGENCE & HIGH-LEVEL RITES ---
from .engine import GnosticSymbolicEngine

# --- II. THE IMMUTABLE VESSELS (CONTRACTS) ---
from .contracts import (
    AdjudicationIntent,
    SymbolicVerdict,
    GnosticAtom,
    SymbolicManifest,
    UrgencyLevel
)

# --- III. THE DECISION GATES (SUTURES) ---
from .sutures import SutureLens, NeuralBridge

# --- IV. THE SENSORY LENS (REFINEMENT) ---
from .refinement import RefinementGaze

# --- V. THE OCULAR LINK (TELEMETRY) ---
from .telemetry import TelemetryLens

# [ASCENSION 1]: TYPE-GUARDED ORCHESTRATION
if TYPE_CHECKING:
    from ...core.runtime.engine import ScaffoldEngine

Logger = logging.getLogger("Scaffold:SymbolicGateway")

# [ASCENSION 2]: GLOBAL SINGLETON MANAGEMENT
# We maintain a weak-reference cache to prevent engine duplication.
# WeakRef ensures that if the parent ScaffoldEngine dies, the Symbolic Engine
# is also garbage collected, preventing memory leaks.
_ENGINE_CACHE: weakref.WeakKeyDictionary[Any, GnosticSymbolicEngine] = weakref.WeakKeyDictionary()
_LOCK = threading.Lock()


def get_symbolic_engine(scaffold_engine: ScaffoldEngine) -> GnosticSymbolicEngine:
    """
    [THE RITE OF SOVEREIGN SUMMONS]
    Materializes or retrieves the GnosticSymbolicEngine bound to a core engine.
    This is the primary entry point for any Artisan to access the Symbolic Brain.
    """
    with _LOCK:
        engine = _ENGINE_CACHE.get(scaffold_engine)
        if engine is None:
            Logger.debug("Materializing new Gnostic Symbolic Engine instance...")
            engine = GnosticSymbolicEngine(scaffold_engine)
            _ENGINE_CACHE[scaffold_engine] = engine
        return engine


# =========================================================================
# == VI. SOVEREIGN CONVENIENCE RITES (HIGH-LEVEL API)                    ==
# =========================================================================

def scry_industrial_intent(
        text: str,
        strata: Dict[str, Any],
        engine: ScaffoldEngine,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
) -> SymbolicManifest:
    """
    [THE ONE TRUE LINE]
    The fastest way to resolve industrial intent in the Monolith.

    Usage:
        manifest = scry_industrial_intent(lead_text, roofing_strata, self.engine)
        if manifest.is_terminal:
            return self.reply(manifest.output_text)
    """
    safe_trace = trace_id or "tr-symbolic-direct"
    symbolic_brain = get_symbolic_engine(engine)

    return symbolic_brain.adjudicate(text, strata, safe_trace, context)


def prepare_vision_inquest(
        strata: Dict[str, Any],
        engine: ScaffoldEngine,
        trace_id: str
) -> Dict[str, Any]:
    """

    [THE VISUAL SUTURE]
    Extracts the image-recognition instructions for the Vision AI.
    """
    from .sutures import VisionGate
    gate = VisionGate(engine)
    return gate.prepare_vision_instructions(strata, trace_id)


# =========================================================================
# == VII. PUBLIC PROCLAMATION (THE EXPORT MANIFEST)                      ==
# =========================================================================

__all__ = [
    # Core Classes
    "GnosticSymbolicEngine",

    # High-Level Rites (The Public API)
    "get_symbolic_engine",
    "scry_industrial_intent",
    "prepare_vision_inquest",

    # Data Contracts (For Type Hinting and Validation)
    "AdjudicationIntent",
    "SymbolicVerdict",
    "GnosticAtom",
    "SymbolicManifest",
    "UrgencyLevel",

    # Sub-System Gateways (For Advanced Integration)
    "SutureLens",
    "RefinementGaze",
    "TelemetryLens",
    "NeuralBridge",
]

# == SCRIPTURE SEALED: THE SYMBOLIC ENGINE IS NOW SOVEREIGN AND UNIVERSAL ==