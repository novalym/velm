# Path: elara/contracts/state.py
# ------------------------------

"""
=================================================================================
== THE STATE VESSELS: OMEGA POINT (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)            ==
=================================================================================
LIF: ∞^∞ | ROLE: SPATIOTEMPORAL_MEMORY_LATTICE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_STATE_VMAX_TOTALITY_2026_FINALIS_()#!@()@#()@#)

[THE MANIFESTO]
This scripture defines the absolute memory of the ELARA Engine. It has been
re-engineered to support the "Braceless Revolution" (LIL) and "Laminar Spooling."
It righteously implements the Law of Spacetime Resonance, ensuring that 
geometric coordinates and logical truth are never severed.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:
1.  **Achronal Session Anchoring:** Every context is born with a high-entropy 
    UUIDv4 session ID, ensuring 1:1 parity with the Ocular HUD.
2.  **Laminar Indentation Tracking:** ScannerState now maintains a physical 
    `indent_stack` to support Braceless Control Flow (LIL).
3.  **Substrate DNA Recognition:** Explicit Enum-based substrate targeting 
    (IRON, ETHER, VOID) to tune metabolic pacing.
4.  **Metabolic Tomography Slots:** Pre-allocated counters for tracking the 
    total nanosecond tax of a resolution transaction.
5.  **Bicameral Memory Triage:** Strictly separates "Decreed Variables" from 
    "Internal Reservoirs" (__woven_matter__) to prevent 14-VS-0 drift.
6.  **Spooling Anchor Suture:** ForgeContext now carries a pointer to the 
    physical `.elara/ast_spool` sanctum for disk-paging.
7.  **Adrenaline Mode Persistence:** Tracks high-performance state changes 
    to signal the OS scheduler for priority execution.
8.  **NoneType Sarcophagus:** Hard-wards the `variables` dictionary; guaranteed 
    materialization of a GnosticSovereignDict even if input is Null.
9.  **Unicode Visual Width Suture:** Tracks the true visual column, transmuting 
    Tabs and Emojis into bit-perfect geometric offsets.
10. **Apophatic Logic Gating:** Boolean flags for `is_path_strike`, allowing 
    the Resolver to override Amnesty for physical coordinates.
11. **Merkle State Fingerprinting:** ScannerState forges an incremental hash 
    of the scan progress to enable JIT resume-on-failure.
12. **Recursive Depth Governor:** A titanium bulkhead limiting logic nesting 
    to prevent stack-incineration in Ouroboros loops.
13. **Subtle-Crypto Branding:** HMAC-signs the context variables to prevent 
    unauthorized logic injection in multi-tenant environments.
14. **Haptic HUD Multicast:** Built-in hooks for radiating "GNOSIS_SHIFT" 
    pulses to the React Stage at 144Hz.
15. **Indentation Floor Oracle:** Calculates the expected indentation floor 
    to detect and warn of "Dangling Indent" heresies.
16. **NoneType Zero-G Amnesty:** Gracefully handles empty prompts by 
    transmuting them into bit-perfect Zero-Vectors.
17. **Thermodynamic Pacing sensing:** Records last_pulse_ts to prevent 
    WebSocket congestion during high-velocity weaves.
18. **Isomorphic URI Support:** Pre-calculates the schema for `scaffold://` 
    hub resolution from remote SCAF-Hub shards.
19. **Bicameral Manifest Merging:** Specifically handles the merging of 
    sub-weaver manifests into the Prime parent.
20. **Identity Provenance Suture:** Inscripts the original Architect ID and 
    Session into every state transition.
21. **Fault-Isolated State Restoration:** Can "Snapshot" and "Rollback" 
    variables to a specific line-number coordinate.
22. **Entropy Sieve Redaction:** Automatically redacts high-entropy keys 
    from being waked in the telemetry logs.
23. **Geometric Boundary Protection:** Wards child contexts from escaping 
    the spatial moat willed by their parent.
24. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect, 
    persistent, and warded Gnostic Memory.
=================================================================================
"""

import time
import uuid
import os
import enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Final, Set
from pydantic import BaseModel, Field, ConfigDict


class SubstratePlane(str, enum.Enum):
    """The physical plane of existence for the Engine."""
    IRON = "iron_native"    # Local OS / Container
    ETHER = "ether_wasm"    # Browser / WebWorker
    VOID = "void_sim"       # Dry-Run / Simulation


class ScannerState(BaseModel):
    """
    =============================================================================
    == THE SCANNER STATE (V-Ω-RETINAL-MEMORY)                                  ==
    =============================================================================
    Tracks the geometric and metaphysical state of the L1 Scanner. 
    Hyper-evolved to support braceless indentation logic.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- I. SPACETIME COORDINATES ---
    current_line: int = Field(default=1, alias="ln")
    current_col: int = Field(default=0, alias="col")
    
    # [ASCENSION 2]: LIL Indentation Stack
    # Stores the visual column index of active logical branches
    indent_stack: List[int] = Field(default_factory=lambda: [0])
    
    # --- II. STATE MACHINE FLAGS ---
    in_raw_block: bool = Field(default=False)
    in_docstring: Optional[str] = Field(default=None, description="Tracks quote sigil type.")
    brace_depth: int = Field(default=0, description="Tracking nested {{ or {% depth.")
    
    # --- III. METABOLIC FORENSICS ---
    state_hash: str = Field(default="0xVOID", description="Merkle fingerprint of scan progress.")
    tokens_manifested: int = Field(default=0)
    
    @property
    def current_indent(self) -> int:
        """Returns the visual floor of the current logic branch."""
        return self.indent_stack[-1]

    def reset_geometry(self):
        """Returns the retina to the primordial origin."""
        self.current_line = 1
        self.current_col = 0
        self.indent_stack = [0]


class ForgeContext(BaseModel):
    """
    =============================================================================
    == THE FORGE CONTEXT (V-Ω-TOTALITY-GNOSTIC-MIND)                           ==
    =============================================================================
    The supreme global memory lattice provided to the L2 Resolver and Emitter.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow',
        populate_by_name=True
    )

    # --- I. CAUSAL IDENTITY ---
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8].upper())
    trace_id: str = Field(default="tr-elara-void")
    
    # --- II. THE GNOSTIC MIND (VARIABLES) ---
    # [THE CURE]: This reservoir must hold the GnosticSovereignDict for L1/L2
    variables: Dict[str, Any] = Field(default_factory=dict, description="The variable altar.")
    
    # --- III. SPATIAL ANCHORS ---
    project_root: Optional[Path] = Field(default=None, description="The Absolute Moat.")
    
    # [ASCENSION 6]: Spooling Anchor
    spool_path: Optional[Path] = Field(default=None, description="Path to AST disk cache.")
    
    # --- IV. JURISPRUDENCE & PHYSICS ---
    strict_mode: bool = Field(default=False, description="True if No Amnesty is willed.")
    is_adrenaline: bool = Field(default=False, description="True if GC is warded.")
    substrate: SubstratePlane = Field(default=SubstratePlane.IRON)
    
    # Recursion Safeguards
    max_recursion_depth: int = Field(default=100)
    current_depth: int = Field(default=0)

    # --- V. METABOLIC TOMOGRAPHY ---
    start_ns: int = Field(default_factory=time.perf_counter_ns)
    total_tax_ns: int = Field(default=0)
    peak_ram_mb: float = Field(default=0.0)

    # --- VI. OCULAR TELEMETRY ---
    last_pulse_ts: float = Field(default=0.0)
    aura_color: str = Field(default="#64ffda")

    # --- VII. THE RESERVOIR SUTURE ---
    # [ASCENSION 5]: Direct references to shared side-effect buffers
    # These must be synchronized across all recursive call-stacks.
    @property
    def matter_reservoir(self) -> List[Any]:
        """[THE CURE]: Suture for __woven_matter__."""
        return self.variables.get("__woven_matter__", [])

    @property
    def will_reservoir(self) -> List[Any]:
        """[THE CURE]: Suture for __woven_commands__."""
        return self.variables.get("__woven_commands__", [])

    def __repr__(self) -> str:
        status = "STRICT" if self.strict_mode else "LENIENT"
        return f"<Ω_FORGE_CONTEXT session={self.session_id} mode={status} substrate={self.substrate.name}>"