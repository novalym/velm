# Path: src/scaffold/core/symbolic/telemetry/__init__.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: TELEMETRY_GATEWAY | RANK: SOVEREIGN
# AUTH: Ω_TELEMETRY_INIT_TOTALITY
# =========================================================================================

"""
=================================================================================
== THE TELEMETRY STRATUM (V-Ω-OCULAR-RESONANCE)                                ==
=================================================================================
@gnosis:title The Telemetry Package
@gnosis:stratum STRATUM-4 (AKASHIC)
@gnosis:summary The projection layer for symbolic cognitive feedback.

This package orchestrates the "Visual Pulse" of the Symbolic Engine.
It ensures that the Architect is never blind to the machine's deterministic
decision-making process.

[THE RESONANCE CYCLE]:
1. THE PULSER: Translates Python logic into JSON-RPC signals.
2. THE BROADCAST: Transmits signals via WebSockets (Silver Cord).
3. THE HUD: Renders haptic animations and tints in the React Stage.
=================================================================================
"""

from __future__ import annotations
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

# --- I. THE PRIMARY ORGANS ---
from .pulse import OcularPulser

# [ASCENSION 1]: TYPE-GUARDED ORCHESTRATION
if TYPE_CHECKING:
    from ..contracts import SymbolicManifest

Logger = logging.getLogger("Scaffold:SymbolicTelemetry")

# =============================================================================
# == II. THE TELEMETRY LENS                                                  ==
# =============================================================================

class TelemetryLens:
    """
    [THE MASTER VIEWPORT]
    A sovereign utility that manages the lifecycle of the OcularPulser.
    """

    def __init__(self, engine: Any):
        self.pulser = OcularPulser(engine)
        self.version = "1.0.0-TOTALITY"

    def project_thought(self, trace_id: str, label: str, color: str = "#64ffda"):
        """Direct projection of a symbolic internal state."""
        self.pulser.fire(trace_id, "THOUGHT", color=color, label=label)

    def project_manifest(self, manifest: SymbolicManifest):
        """Projects the entire result of a symbolic adjudication."""
        self.pulser.emit_verdict(
            trace_id=manifest.trace_id,
            intent=manifest.primary_intent.value,
            latency_ms=manifest.vitals.get("latency_ms", 0.0),
            success=True # Logic assumes if we have a manifest, the engine succeeded
        )

# =========================================================================
# == III. SOVEREIGN EXPORT GATEWAY                                       ==
# =========================================================================

__all__ = [
    "OcularPulser",
    "TelemetryLens"
]

# == SCRIPTURE SEALED: THE TELEMETRY GATEWAY IS UNBREAKABLE ==