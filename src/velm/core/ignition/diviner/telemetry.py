# Path: scaffold/core/ignition/diviner/telemetry.py
# --------------------------------------------------
# LIF: INFINITY // AUTH_CODE: DIVINER_TELEMETRY_V1

import time
from typing import List, Dict

class ForensicScribe:
    """
    =============================================================================
    == THE FORENSIC SCRIBE (V-Ω- تصمیم-LOGGING)                                ==
    =============================================================================
    [ASCENSION 78]: Chronicling the path to Gnosis.
    """
    def __init__(self):
        self.start_time = time.perf_counter()
        self.milestones: List[Dict] = []

    def record(self, event: str, metadata: Dict = None):
        elapsed = (time.perf_counter() - self.start_time) * 1000
        self.milestones.append({
            "event": event,
            "latency_ms": round(elapsed, 3),
            "meta": metadata or {}
        })

    def finalize(self) -> List[str]:
        return [f"[{m['latency_ms']}ms] {m['event']}" for m in self.milestones]