# Path: scaffold/core/kernel/transaction/contracts.py
# ---------------------------------------------------
# =========================================================================================
# == THE OMEGA TRANSACTIONAL CONTRACTS (V-Ω-TOTALITY-V2000.5-FINALIS)                    ==
# =========================================================================================
# LIF: ∞ | ROLE: GNOSTIC_LEDGER_DEFINITIONS | RANK: OMEGA_SINGULARITY
# AUTH_CODE: !(@)#(#)(@#()@!#)(@#!!!
# =========================================================================================

from __future__ import annotations
from enum import Enum, auto
from uuid import UUID, uuid4
from typing import Any, Dict, Optional, List, Union, Final
import time
from pydantic import BaseModel, Field, ConfigDict, computed_field


# =========================================================================================
# == STRATUM-0: THE TAXONOMY OF KINETIC WILL                                             ==
# =========================================================================================

class LedgerOperation(str, Enum):
    """
    =============================================================================
    == THE VERBS OF REALITY (LedgerOperation)                                  ==
    =============================================================================
    The complete Gnostic alphabet of physical and logical mutations.
    """
    SET_VAR = "SET_VAR"
    WRITE_FILE = "WRITE_FILE"
    DELETE_FILE = "DELETE_FILE"
    MKDIR = "MKDIR"
    RMDIR = "RMDIR"
    RENAME = "RENAME"
    CHMOD = "CHMOD"
    EXEC_SHELL = "EXEC_SHELL"
    SYMLINK = "SYMLINK"      # [ASCENSION 2]
    HARDLINK = "HARDLINK"    # [ASCENSION 2]
    ATOMIC_SWAP = "SWAP"     # [ASCENSION 2]
    VAULT_LOCK = "LOCK"      # [ASCENSION 2]
    RECONCILE = "RECONCILE"  # [ASCENSION 2]
    RESTORE_FILE = "RESTORE_FILE"
    GHOST_RESTORE = "GHOST_RESTORE"


class SubstrateDNA(str, Enum):
    """The physical plane where the transaction manifested."""
    IRON = "iron_native"    # Bare Metal / VM / Container
    ETHER = "ether_wasm"    # Browser / Pyodide
    VOID = "void_sim"       # Quantum Simulation / Dry-run


class RiteCategory(str, Enum):
    """The semantic intent of the transaction."""
    GENESIS = "GENESIS"       # Creation of a new reality
    EVOLUTION = "EVOLUTION"   # Mutation of existing reality (Transmute)
    DESTRUCTION = "DESTRUCTION" # Return to void (Clean/Excise)
    INSPECTION = "INSPECTION" # Passive Gaze (Audit)
    HEALING = "HEALING"       # Automated Redemption (Lazarus)


# =========================================================================================
# == STRATUM-1: THE OMEGA FORENSIC DOSSIER                                               ==
# =========================================================================================

class TransactionalGnosis(BaseModel):
    """
    =============================================================================
    == THE VESSEL OF THE FALLEN RITE (V-Ω-TOTALITY-V2000-HEALED)               ==
    =============================================================================
    @gnosis:title TransactionalGnosis
    @gnosis:summary The definitive, immutable chronicle of a transaction's soul.
    @gnosis:LIF INFINITY (THE UNBREAKABLE RECORD)

    The "black box" recorder of the Scaffold Cosmos. It has been ascended to
    possess absolute forensic memory, capturing the event-stream of micro-mutations
    and hardware vitals at the moment of paradoxical collapse.
    =============================================================================
    """
    # === THE VOW OF IMMUTABILITY & GNOSTIC PURITY ===
    model_config = ConfigDict(
        frozen=True,
        extra='forbid',
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- I. THE SILVER CORD (IDENTITY) ---
    trace_id: str = Field(
        ...,
        description="The unique, globally-resonant ID linking this failure to the Akasha."
    )

    tx_id: str = Field(
        ...,
        description="The unique, immutable identifier for this specific transactional reality."
    )

    rite_name: str = Field(
        ...,
        description="The sacred name of the rite (e.g., 'Genesis: sentinel-api')."
    )

    rite_category: RiteCategory = Field(
        default=RiteCategory.EVOLUTION,
        description="The semantic classification of the willed intent."
    )

    # --- II. THE CONTEXTUAL SOUL (MEMORY) ---
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="The complete Gnostic context (variables) at the moment of collapse."
    )

    # [ASCENSION 1 & THE CURE]: THE QUANTUM EVENT STREAM
    # This captures the 'How' - the exact sequence of micro-events leading to failure.
    event_stream: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="The chronological event-sourced ledger of all internal state changes."
    )

    # --- III. METABOLIC TOMOGRAPHY (ENERGY) ---
    substrate: SubstrateDNA = Field(
        default=SubstrateDNA.IRON,
        description="The physical or virtual plane where the strike occurred."
    )

    # [ASCENSION 4]: NANOSECOND CHRONOMETRY
    birth_ns: int = Field(
        default_factory=time.perf_counter_ns,
        description="The nanosecond-epoch of transaction inception."
    )

    death_ns: int = Field(
        default_factory=time.perf_counter_ns,
        description="The nanosecond-epoch of transactional collapse."
    )

    vitals_snapshot: Dict[str, Any] = Field(
        default_factory=dict,
        description="The thermodynamic state (CPU/RAM/IO) at the moment of fracture."
    )

    # --- IV. THE MANIFEST OF MATTER (RESULTS) ---
    dossier_count: int = Field(
        ...,
        description="The number of file operations recorded before the paradox."
    )

    edict_count: int = Field(
        ...,
        description="The number of Maestro's Edicts (post-run commands) recorded."
    )

    heresy_count: int = Field(
        ...,
        description="The number of non-critical heresies perceived before the final collapse."
    )

    # [ASCENSION 5]: INTEGRITY SEALS
    final_merkle_root: str = Field(
        default="0xVOID",
        description="The SHA-256 Merkle root of the staged reality at collapse."
    )

    # --- V. THE PATH OF REDEMPTION (CAUSALITY) ---
    is_simulation: bool = Field(
        ...,
        description="A vow proclaiming whether this rite was a prophecy (True) or a materialization (False)."
    )

    reversal_plan: Optional[List[str]] = Field(
        None,
        description="A pre-calculated sequence of edicts to manually heal the substrate."
    )

    # =========================================================================
    # == COMPUTED REALITIES                                                  ==
    # =========================================================================

    @computed_field
    @property
    def lifespan_ms(self) -> float:
        """Calculates the metabolic age of the transaction in milliseconds."""
        return (self.death_ns - self.birth_ns) / 1_000_000

    @computed_field
    @property
    def entropy_index(self) -> float:
        """Heuristic ratio of heresy to work performed."""
        total_ops = self.dossier_count + self.edict_count
        if total_ops == 0: return 0.0
        return self.heresy_count / total_ops

    # =========================================================================
    # == THE FINALITY VOW                                                    ==
    # =========================================================================

    def __repr__(self) -> str:
        return f"<Ω_TX_GNOSIS id={self.tx_id[:8]} rite={self.rite_name} status=COLLAPSED>"