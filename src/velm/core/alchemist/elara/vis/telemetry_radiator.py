# Path: elara/vis/telemetry_radiator.py
# ------------------------------------

import time
import json
from typing import Any, Dict, Optional
from .....logger import Scribe


class MetabolicRadiator:
    """
    =============================================================================
    == THE METABOLIC RADIATOR (V-Ω-TOTALITY)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: HUD_SIGNAL_EMITTER | RANK: MASTER

    Acts as the high-frequency pulse transmitter for the ELARA Engine.
    It streams internal state variables directly to the HUD via WebSockets.
    """

    def __init__(self, akashic_ref: Any, trace_id: str):
        self.akashic = akashic_ref
        self.trace_id = trace_id

    def radiate_shift(self, key: str, value: Any, aura: str = "#64ffda"):
        """Radiates a single Gnosis Shift event."""
        if not self.akashic: return

        try:
            self.akashic.broadcast({
                "method": "elara/gnosis_shift",
                "params": {
                    "key": key,
                    "val": str(value)[:100],
                    "aura": aura,
                    "trace": self.trace_id,
                    "ts": time.time()
                }
            })
        except:
            pass

    def radiate_progress(self, label: str, percent: int):
        """Radiates a structural materialization progress pulse."""
        if not self.akashic: return
        try:
            self.akashic.broadcast({
                "method": "elara/progress",
                "params": {
                    "label": label,
                    "pct": percent,
                    "trace": self.trace_id
                }
            })
        except:
            pass