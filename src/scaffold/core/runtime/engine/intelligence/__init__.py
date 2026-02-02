# Path: core/runtime/engine/intelligence/__init__.py
# --------------------------------------------------

"""
=================================================================================
== THE INTELLIGENCE SUBSYSTEM (V-Ω-PRECOGNITIVE-CORE)                          ==
=================================================================================
The Mind of the God-Engine.

[FACULTIES]:
1. Optimizer (NeuroOptimizer): Tunes physics based on hardware.
2. Predictor (IntentPredictor): Guesses the next logical rite.
3. Memory (CognitiveMemory): Short-term session context store.
4. Cache (SmartCache): L2/L3 persistence strategies.
"""

from .optimizer import NeuroOptimizer
from .predictor import IntentPredictor
from .memory import CognitiveMemory
from .cache import SmartCache

__all__ = [
    "NeuroOptimizer",
    "IntentPredictor",
    "CognitiveMemory",
    "SmartCache"
]