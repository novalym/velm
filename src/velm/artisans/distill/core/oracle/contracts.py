# Path: artisans/distill/core/oracle/contracts.py
# -----------------------------------------------


from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional
from pathlib import Path

# --- THE DIVINE SUMMONS ---
from .....core.cortex.contracts import CortexMemory, FileGnosis, DistillationProfile



@dataclass
class OracleContext:
    """
    =============================================================================
    == THE VESSEL OF ACCUMULATED GNOSIS (V-Ω-STATE-CONTAINER-HEALED)           ==
    =============================================================================
    A mutable, flowing vessel that travels through the Oracle's pipeline.
    It accumulates Perception, Divination, Propagation, and Adjudication data.

    [HEALED]: Now carries the `active_symbols` attribute to satisfy the
    ContentWeaver's contract.
    """
    # --- The Architect's Will ---
    root: Path
    profile: DistillationProfile

    # --- Stage 1: Perception (The Cortex) ---
    memory: Optional[CortexMemory] = None

    # --- Stage 2: Divination (The Seeds) ---
    query_intent: Dict[str, Any] = field(default_factory=dict)
    seed_files: Set[str] = field(default_factory=set)
    # A map of "Why is this file here?" (e.g., "Semantic Search", "Stack Trace")
    context_reasons: Dict[str, List[str]] = field(default_factory=dict)

    # --- Stage 3: Propagation (The Web) ---
    # Files touched by dynamic tracing or causal expansion
    traced_files: Set[str] = field(default_factory=set)
    # Scores calculated by the Causal Engine (Impact/Ripple effect)
    impact_scores: Dict[str, int] = field(default_factory=dict)
    # Captured runtime values (variable states)
    runtime_state: Any = None

    # [THE FIX] The Set of Active Symbols (for Skeletonizer filtering)
    # This allows the Oracle to pass specific symbol focuses down to the Weaver.
    active_symbols: Optional[Set[str]] = None

    # --- Stage 4: Adjudication (The Verdict) ---
    ranked_inventory: List[FileGnosis] = field(default_factory=list)
    # Map: Path -> RepresentationTier (e.g. 'full', 'skeleton')
    governance_plan: Dict[Path, str] = field(default_factory=dict)
    budget_limit: int = 0

    # --- Telemetry (The Pulse) ---
    stats: Dict[str, Any] = field(default_factory=dict)

    def add_reason(self, path: str, reason: str):
        """Inscribes a reason for a file's inclusion into the Gnostic Record."""
        self.context_reasons.setdefault(path, []).append(reason)

    def record_stat(self, key: str, value: Any):
        """Updates the internal telemetry ledger."""
        self.stats[key] = value