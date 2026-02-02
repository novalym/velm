# Path: scaffold/core/ai/__init__.py
# ----------------------------------

"""
=================================================================================
== THE NEURAL SANCTUM (V-Ω-MODULAR-GATEWAY)                                    ==
=================================================================================
This is the public face of the AI subsystem. It exposes the God-Engine, the
Configuration Contracts, and the Provider Interfaces to the rest of the cosmos.

It shields the outer world from the internal fractalization of the `engine/` and
`providers/` directories.
"""

# 1. The Central Intelligence
from .engine import AIEngine

# 2. The Immutable Vessels (Data Contracts)
from .contracts import (
    AIConfig,
    NeuralPrompt,
    NeuralRevelation,
    LLMProvider
)

# 3. The Public Proclamation
__all__ = [
    "AIEngine",
    "AIConfig",
    "NeuralPrompt",
    "NeuralRevelation",
    "LLMProvider"
]