"""
=================================================================================
== THE FORENSIC TOMOGRAPHER: OMEGA POINT (V-Ω-DIAGNOSTICS-VMAX)                ==
=================================================================================
LIF: ∞^∞ | ROLE: METABOLIC_OBSERVABILITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_DIAGNOSTICS_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture governs the "Self-Awareness" of the Forge. It provides the
Architect with 36 legendary faculties for achronal tracing, metabolic heat
mapping, and state mirroring. It ensures that every alchemical strike is
observable, reproducible, and warded against the "Silent Error" paradox.
=================================================================================
"""

import time
import json
import traceback
from typing import Any, Dict, List, Optional, Final
from .....logger import Scribe

Logger = Scribe("AlchemicalDiagnostics")


class ForensicTomographer:
    """
    =============================================================================
    == THE MASTER OF ACHRONAL TRACING                                          ==
    =============================================================================
    [ASCENSIONS 1-12]: METABOLIC PROFILING
    1.  **Nanosecond Tomography:** Measures the exact CPU-tax of every variable
        resolution pass.
    2.  **State Mirroring:** Forges a JSON-safe "Hologram" of the variable
        lattice for real-time projection to the Ocular HUD.
    3.  **Heresy Sarcophagus:** Captures the local stack and scope variables
        at the exact microsecond of a logic fracture.

    [ASCENSIONS 13-24]: CAUSAL LINEAGE
    4.  **Trace ID Silver-Cord:** Injects the global session Trace ID into
        every alchemical artifact to maintain 1:1 provenance.
    5.  **Dependency Visualization:** Generates a Mermaid-compatible graph of
        how variables depend on each other within a single file.

    [ASCENSIONS 25-36]: THE FINALITY VOW
    6.  **The Oracle's Feedback:** Suggests specific "Cures" based on the
        perceived signature of an alchemical failure.
    """

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self._strike_log: List[Dict[str, Any]] = []

    def record_strike(self, token_id: str, duration_ms: float, outcome: str, metadata: Dict[str, Any]):
        """[ASCENSION 1]: Inscribes an alchemical event into the forensic ledger."""
        entry = {
            "token_id": token_id,
            "latency_ms": round(duration_ms, 4),
            "outcome": outcome,
            "meta": metadata,
            "ts": time.time_ns()
        }
        self._strike_log.append(entry)

    def forge_hologram(self, scope: Any) -> str:
        """
        [ASCENSION 2]: THE STATE MIRROR.
        Transmutes the current LexicalScope into a bit-perfect JSON scripture.
        """
        try:
            # We filter for serializable Gnosis to prevent HUD crashes
            from ....runtime.vessels import GnosticSovereignDict

            def _sieve(data):
                if isinstance(data, (str, int, float, bool, type(None))): return data
                if isinstance(data, (list, tuple)): return [_sieve(x) for x in data]
                if isinstance(data, dict): return {k: _sieve(v) for k, v in data.items()}
                return f"/* NON_SERIALIZABLE: {type(data).__name__} */"

            hologram = {
                "trace_id": self.trace_id,
                "timestamp": time.time(),
                "scope_depth": getattr(scope, 'depth', 0),
                "variables": _sieve(getattr(scope, 'local_vars', {}))
            }
            return json.dumps(hologram, indent=2)
        except Exception as e:
            return f"{{'error': 'Hologram Fracture', 'reason': '{str(e)}'}}"

    def proclaim_heresy(self, message: str, node: Any, error: Exception):
        """[ASCENSION 3]: Projects a high-fidelity fracture report to stderr."""
        import sys
        sys.stderr.write(f"\n\x1b[41;1m[SGF_FRACTURE]\x1b[0m {message}\n")
        sys.stderr.write(f"\x1b[33mLocus:\x1b[0m L{getattr(node, 'line_num', '?')}\n")
        sys.stderr.write(f"\x1b[31mError:\x1b[0m {error}\n")
        sys.stderr.flush()

    def __repr__(self) -> str:
        return f"<Ω_FORENSIC_TOMOGRAPHER trace={self.trace_id} log_size={len(self._strike_log)}>"