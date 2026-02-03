# Path: scaffold/core/kernel/transaction/contracts.py
# ---------------------------------------------------

from __future__ import annotations
from enum import Enum
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
import time
from pydantic import BaseModel, Field, ConfigDict


class LedgerOperation(str, Enum):
    """The Gnostic verbs of every atomic action in the cosmos."""
    SET_VAR = "SET_VAR"
    WRITE_FILE = "WRITE_FILE"
    DELETE_FILE = "DELETE_FILE"
    MKDIR = "MKDIR"
    RMDIR = "RMDIR"
    RENAME = "RENAME"
    CHMOD = "CHMOD"
    EXEC_SHELL = "EXEC_SHELL"
    # [PHASE III] New Ops
    RESTORE_FILE = "RESTORE_FILE"




class TransactionalGnosis(BaseModel):
    """
    =============================================================================
    == THE VESSEL OF THE FALLEN RITE (V-Ω-FORENSIC-DOSSIER)                    ==
    =============================================================================
    The sacred, immutable vessel carrying the complete Gnosis of a transaction's
    state at the moment of its paradoxical collapse. It is the "black box" recorder,
    the core of our forensic archival system, ensuring that no failure is ever a
    true mystery.
    =============================================================================
    """
    # === THE VOW OF IMMUTABILITY & GNOSTIC PURITY ===
    # We forbid extra fields to ensure the contract is never profaned.
    model_config = ConfigDict(frozen=True, extra='forbid')

    # --- Core Identity & Context ---
    rite_name: str = Field(
        ...,
        description="The sacred name of the rite that was being conducted (e.g., 'Genesis: my-app')."
    )
    tx_id: str = Field(
        ...,
        description="The unique, immutable identifier for this specific transactional reality."
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="The complete Gnostic context (variables) at the moment of the paradox."
    )

    # --- Telemetry of the Rite ---
    dossier_count: int = Field(
        ...,
        description="The number of file operations (writes) recorded before the paradox."
    )
    edict_count: int = Field(
        ...,
        description="The number of Maestro's Edicts (post-run commands) recorded."
    )
    heresy_count: int = Field(
        ...,
        description="The number of non-critical heresies perceived before the final collapse."
    )

    # --- Metaphysical State ---
    is_simulation: bool = Field(
        ...,
        description="A vow proclaiming whether this rite was a prophecy (True) or a materialization (False)."
    )


