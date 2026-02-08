# Path: src/velm/core/runtime/engine/intelligence/predictor/__init__.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: COGNITIVE_Spinal_Junction | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PREDICTOR_V460_SINGULARITY_FINALIS
# =========================================================================================

"""
===========================================================================================
== THE PREFRONTAL CORTEX (V-Ω-TOTALITY)                                                  ==
===========================================================================================
@gnosis:title The Intent Prediction Stratum
@gnosis:summary The unified cognitive engine for stochastic and deterministic precognition.
@gnosis:capability RECURSIVE_INTENT_RECONSTRUCTION
LIF: INFINITY
===========================================================================================
"""

from pathlib import Path
from typing import Optional, Any, Dict, List, Final

# --- THE SOVEREIGN IMPORTS ---
from .oracle import IntentPredictor
from .contracts import (
    PredictionProphecy,
    GnosticWeightsDossier,
    HeresyState,
    WeightNode
)

# --- THE ACHRONAL METADATA ---
__intelligence_version__: Final[str] = "4.6.0-Totality"
__lif_index__: Final[str] = "INFINITY"
__auth_code__: Final[str] = "Ω_PREDICTOR_V460_FINALIS"
__rank__: Final[str] = "OMEGA_SOVEREIGN"


# =========================================================================================
# == THE RITE OF FORGING (FACTORY)                                                       ==
# =========================================================================================

def forge_oracle(project_root: Path, engine: Optional[Any] = None) -> IntentPredictor:
    """
    =======================================================================================
    == THE RITE OF ORACLE INCEPTION                                                      ==
    =======================================================================================
    The definitive method for awakening the Predictor.
    [ASCENSION 2]: Automatically prepares the physical substrate for memory.
    """
    # 1. Sanctum Verification
    cache_dir = project_root / ".scaffold" / "cache" / "intelligence"
    if not cache_dir.exists():
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            # Fallback to the void if the disk is locked
            pass

    # 2. Materialization
    return IntentPredictor(persistence_root=project_root, engine=engine)


# =========================================================================================
# == THE GNOSTIC EXPORTS                                                                 ==
# =========================================================================================

__all__ = [
    # The Facade
    "IntentPredictor",

    # The Contracts
    "PredictionProphecy",
    "GnosticWeightsDossier",
    "HeresyState",
    "WeightNode",

    # The Rites
    "forge_oracle",

    # The Provenance
    "__intelligence_version__",
    "__lif_index__",
    "__auth_code__"
]

# == SCRIPTURE SEALED: THE COGNITIVE STRATUM IS NOW RESONANT ==