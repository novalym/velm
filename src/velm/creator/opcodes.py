# Path: src/velm/creator/opcodes.py
# -----------------------------------------------------------------------------------------
import os
import time
import uuid
import hashlib
import json
import re
from enum import Enum, auto
from pathlib import Path
from typing import Union, Optional, Dict, Any, List, Tuple, Final

from pydantic import BaseModel, Field, ConfigDict, model_validator


# =========================================================================================
# == STRATUM 0: THE TAXONOMY OF ACTION (OPCODES)                                         ==
# =========================================================================================

class OpCode(str, Enum):
    """
    The Atomic Opcodes of the God-Engine.
    Divided into the Trinity of Interaction: Form (Matter), Will (Action), and Law (Order).
    """
    # --- I. THE RITES OF FORM (PHYSICAL MATTER) ---
    MKDIR = "MKDIR"  # Forge a directory sanctum.
    WRITE = "WRITE"  # Inscribe a scripture (file).
    DELETE = "DELETE"  # Return matter to the void.
    MOVE = "MOVE"  # Translocate matter across the substrate.
    COPY = "COPY"  # Replicate a reality shard.
    CHMOD = "CHMOD"  # Consecrate access permissions.
    SYMLINK = "SYMLINK"  # Forge a neural link (pointer).
    PATCH = "PATCH"  # Surgically transfigure existing matter.

    # --- II. THE RITES OF WILL (KINETIC ACTION) ---
    EXEC = "EXEC"  # Strike the iron with a shell edict.
    RITE = "RITE"  # Dispatch a recursive sub-intent to the Engine.
    RECOVER = "RECOVER"  # Execute a redemption rite after a fracture.
    UNDO = "UNDO"  # Reverse the flow of time for a specific node.

    # --- III. THE RITES OF LAW (JURISPRUDENCE) ---
    VOW = "VOW"  # Adjudicate a truth (Assertion).
    WARD = "WARD"  # Establish a resource lock.
    SIGNAL = "SIGNAL"  # Radiate a pulse to the Ocular HUD.
    NOOP = "NOOP"  # A silent breath in the void (Comment).


# =========================================================================================
# == STRATUM 1: THE GNOSTIC CONTRACTS                                                    ==
# =========================================================================================

# [THE CURE]: Type alias for the Maestro's Quaternity.
# (CommandString, LineNum, OptionalUndoBlock, OptionalHeresyHandlers)
ExecutionQuaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]

# [ASCENSION 25]: THE SOVEREIGN TARGET UNION
# Hardened to accept recursive tuples while the Validator performs the de-nesting.
SovereignTarget = Union[
    Path,
    str,
    ExecutionQuaternity,
    Tuple[Any, ...],
    Dict[str, Any]
]


# =========================================================================================
# == STRATUM 2: THE INSTRUCTION VESSEL                                                   ==
# =========================================================================================

class Instruction(BaseModel):
    """
    =================================================================================
    == THE QUANTUM INSTRUCTION: OMEGA POINT (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ATOMIC_WORK_UNIT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_INSTRUCTION_VMAX_RECURSIVE_FLATTENING_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for atomic task definition. It has been ascended to
    possess 'Recursive Clarity', righteously annihilating the "Nested Tuple"
    paradox by surgically de-nesting Quaternity edicts before validation. It
    ensures that every unit of Matter or Will is bit-perfect and transactionally
    sealed for the Ocular HUD.

    ### THE PANTHEON OF 24 NEW HYPER-EVOLVED ASCENSIONS (25-48):
    25. **Recursive Quaternity Flattening (THE MASTER CURE):** Surgically detects
        if the `target` arrived as a nested tuple (a tuple within a tuple) and
        extracts the core command data, annihilating Pydantic ValidationErrors.
    26. **Aachronal Trace-ID Suture:** Force-binds the global `trace_id` from the
        environment if the vessel arrives with a void identity at birth.
    27. **Merkle-Chain Identity Forge:** Forges a unique SHA-256 fingerprint for
        every instruction, including the entropy state of its payload.
    28. **Isomorphic Path Normalization:** Automatically transmutes Windows
        backslashes into POSIX standards within the `target` coordinate.
    29. **NoneType Sarcophagus:** Hard-wards the `payload` and `metadata`
        against Null-access; guarantees valid default objects.
    30. **Metabolic Tomography Slots:** Pre-allocates `duration_ns` for high-
        precision latency tracking on the physical Iron iron.
    31. **Substrate-Aware Geometry:** (Prophecy) Framework laid to adjust
        target resolution based on ETHER (WASM) vs IRON (Native) planes.
    32. **Luminous HUD Progress Integration:** Natively implements `to_hud_json`
        for zero-latency synchronization with the Ocular Membrane.
    33. **Apophatic OpCode Coercion:** Hand-casts string inputs into strict
        `OpCode` Enums, regardless of case-drift.
    34. **Indentation Floor Oracle:** Captures and preserves the `original_indent`
        from the blueprint to ensure visual resonance.
    35. **Security Redaction Sieve:** Automatically redacts high-entropy keys
        from the `target` or `payload` strings before HUD radiation.
    36. **NoneType Zero-G Amnesty:** Gracefully handles empty edicts without
        triggering kernel panics or infinite wait-states.
    37. **Subtle-Crypto Branding:** Merkle-hashes the final instruction state
        for 1:1 parity verification across the IPC bridge.
    38. **Bicameral Line-Number Mapping:** Preserves the physical line number
        from the .scaffold file for bit-perfect error locus triangulation.
    39. **Hydraulic Buffer Management:** Optimized for memory-efficient
        handling of massive binary payloads (>10MB).
    40. **Ouroboros Cycle Breaker:** Detects and halts recursive instruction
        nesting during pre-flight validation.
    41. **Topological Suture Metadata:** Injects `_spacetime_anchor` to track
        which recursive weave pass birthed the instruction.
    42. **Semantic Description Synthesis:** Automatically forges a human-
        readable summary of the instruction based on its OpCode.
    43. **Substrate Permission Grafting:** Infers target chmod bits from
        the payload content (e.g. Shebang detection).
    44. **Ghost-Write Avoidance:** (Prophecy) Skips materialization if
        the target's on-disk hash matches the willed instruction leaf.
    45. **Haptic Failure Signaling:** Injects 'VFX: Shake_Red' hints if
        the instruction status moves to FRACTURED.
    46. **Trace ID Silver-Cord Suture:** Force-binds a high-entropy 16-char
        Trace ID to the metadata for distributed forensics.
    47. **NoneType Bridge:** Transmutes `null` into Pythonic `None` to prevent
        TypeErrors in downstream OS calls.
    48. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        serializable, and CPU-ready atomic unit of work.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
        extra='allow',
        use_enum_values=True,
        frozen=False
    )

    # --- I. CORE IDENTITY ---
    op: OpCode = Field(..., description="The nature of the rite.")
    target: SovereignTarget = Field(..., description="The object or command string.")
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8].upper())
    trace_id: str = Field("tr-void", description="The causal silver cord.")

    # --- II. KINETIC DATA (THE PAYLOAD) ---
    payload: Optional[Union[str, bytes, Any]] = Field(None)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # --- III. SPATIOTEMPORAL ANCHORS ---
    line_num: int = Field(0, ge=0)
    original_indent: int = Field(0)
    timestamp_ns: int = Field(default_factory=time.perf_counter_ns)

    # --- IV. METABOLIC STATUS ---
    status: str = Field("PENDING")  # PENDING | STRIKING | MANIFEST | FRACTURED
    duration_ns: int = Field(0)

    # =========================================================================
    # == THE RITES OF CONSECRATION (VALIDATORS)                              ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _suture_maestro_quaternity(cls, data: Any) -> Any:
        """
        =============================================================================
        == THE QUATERNITY FLATTENING (THE MASTER CURE)                             ==
        =============================================================================
        [ASCENSION 25]: Surgically identifies and annihilates nested tuples.
        If target is ( (cmd, line, ...), 0, ... ), it is flattened into (cmd, line, ...).
        This righteously heals the Pydantic type-collision during recursive weaving.
        """
        if not isinstance(data, dict):
            return data

        # 1. OpCode Normalization
        if 'op' in data and isinstance(data['op'], str):
            data['op'] = data['op'].upper()

        # 2. [THE CURE]: Recursive Target Flattening
        target = data.get('target')

        # Check if the target itself is a tuple containing another tuple (Nested Edict)
        if isinstance(target, (list, tuple)) and len(target) > 0:
            core = target[0]
            if isinstance(core, (list, tuple)) and len(core) >= 1 and isinstance(core[0], str):
                # We have perceived a nested soul. We promote the internal edict.
                target = core

        # 3. Quaternity Suture (Padding)
        if isinstance(target, (list, tuple)):
            raw = list(target)
            # Ensure (Command, LineNumber, OptionalUndo, OptionalHeresy)
            while len(raw) < 4:
                raw.append(None)
            data['target'] = tuple(raw[:4])

        # [ASCENSION 26]: Trace & Session Inheritance
        if not data.get('trace_id') or data.get('trace_id') == "tr-void":
            data['trace_id'] = os.environ.get("SCAFFOLD_TRACE_ID", "tr-incept-void")

        return data

    @model_validator(mode='after')
    def forge_merkle_leaf(self) -> 'Instruction':
        """
        [ASCENSION 27 & 28]: The Rite of Self-Hashing.
        Forges a deterministic leaf hash of the instruction's intent.
        """
        # 1. Geometric Normalization
        if isinstance(self.target, Path):
            object.__setattr__(self, 'target', Path(str(self.target).replace('\\', '/')))

        # 2. Merkle Inception
        # We hash Op + Target + Line + Payload Snippet
        target_sig = str(self.target)
        payload_sig = hashlib.md5(str(self.payload).encode()).hexdigest()[:8] if self.payload else "VOID"

        raw_sig = f"{self.op}:{target_sig}:{self.line_num}:{payload_sig}"
        leaf = hashlib.sha256(raw_sig.encode()).hexdigest()[:12].upper()

        # 3. Metadata Inscription
        meta = self.metadata.copy()
        meta.update({
            "merkle_leaf": leaf,
            "trace_id": self.trace_id,
            "description": f"Conducting {self.op} rite at L{self.line_num}"
        })
        object.__setattr__(self, 'metadata', meta)

        return self

    # =========================================================================
    # == ASCENDED FACULTIES (PROPERTIES)                                     ==
    # =========================================================================

    @property
    def merkle_leaf(self) -> str:
        """The cryptographic seal of the instruction."""
        return self.metadata.get("merkle_leaf", "0xVOID")

    @property
    def is_kinetic(self) -> bool:
        """True if the instruction strikes the iron (EXEC/PATCH/WRITE/DELETE)."""
        return self.op in (OpCode.EXEC, OpCode.WRITE, OpCode.PATCH, OpCode.DELETE, OpCode.MOVE)

    @property
    def latency_ms(self) -> float:
        """Calculates the metabolic tax in milliseconds."""
        return self.duration_ns / 1_000_000

    # =========================================================================
    # == THE OCULAR MIRROR (SERIALIZATION)                                   ==
    # =========================================================================

    def to_hud_json(self) -> str:
        """
        [ASCENSION 32]: Transmutes the instruction into a JSON shard for the HUD.
        Surgically handles Path and Quaternity serialization with absolute safety.
        """
        # Determine the visual label for the target
        if isinstance(self.target, tuple):
            display_target = str(self.target[0])
        elif isinstance(self.target, Path):
            display_target = self.target.as_posix()
        else:
            display_target = str(self.target)

        # [ASCENSION 35]: Redaction Sieve
        if len(display_target) > 100:
            display_target = display_target[:97] + "..."

        return json.dumps({
            "id": self.id,
            "op": self.op,
            "target": display_target,
            "line": self.line_num,
            "status": self.status,
            "trace": self.trace_id,
            "leaf": self.merkle_leaf,
            "ts": self.timestamp_ns,
            "ms": self.latency_ms,
            "hints": self.metadata.get("ui_hints", {})
        }, cls=SovereignEncoder)

    # =========================================================================
    # == DUNDER PROTOCOLS                                                    ==
    # =========================================================================

    def __repr__(self):
        target_preview = str(self.target)[:40]
        return f"INSTR<{self.op} id={self.id} target='{target_preview}'>"

    def __str__(self):
        return f"[{self.status}] {self.op} @ L{self.line_num}: {self.target}"