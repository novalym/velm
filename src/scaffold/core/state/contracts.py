# Path: scaffold/core/state/contracts.py
# --------------------------------------

from __future__ import annotations

import time
from enum import Enum
from uuid import UUID, uuid4
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class LedgerOperation(str, Enum):
    """
    =================================================================================
    == THE GNOSTIC VERBS OF CAUSALITY                                              ==
    =================================================================================
    The sacred, immutable alphabet of every atomic action that can transfigure the
    state of the mortal realm (the filesystem) or the engine's mind (variables).
    """
    # --- State Transfigurations ---
    SET_VAR = "SET_VAR"
    """Inscribes or alters a variable in the Gnostic Store."""

    # --- Filesystem Formations ---
    WRITE_FILE = "WRITE_FILE"
    """Inscribes the soul (content) of a scripture."""
    DELETE_FILE = "DELETE_FILE"
    """Returns a scripture to the void."""
    MKDIR = "MKDIR"
    """Forges a new sanctum (directory)."""
    RMDIR = "RMDIR"
    """Returns a sanctum to the void."""
    RENAME = "RENAME"
    """Transfigures the name or location of a scripture or sanctum."""
    CHMOD = "CHMOD"
    """Consecrates the permissions of a scripture."""

    # --- Maestro's Will ---
    EXEC_SHELL = "EXEC_SHELL"
    """Conducts a command in the mortal realm's shell."""

    # --- Chronomancer's Rites (Inverse Operations) ---
    RESTORE_FILE = "RESTORE_FILE"
    """Resurrects a scripture from the Void Manager (trash). [Legacy]"""


class InverseOp(BaseModel):
    """
    =================================================================================
    == THE SACRED SCRIPTURE OF REVERSAL                                            ==
    =================================================================================
    An immutable, Gnostic instruction that teaches the Chronomancer how to unwind a
    single moment in time. It is the core of the Universal Undo Protocol.
    """
    # The Vow of Immutability: An inverse action, once proclaimed, is eternal.
    model_config = ConfigDict(frozen=True)

    op: LedgerOperation = Field(..., description="The Gnostic verb of the reversal rite.")
    params: Dict[str, Any] = Field(..., description="The Gnosis required to conduct the reversal.")


class LedgerEntry(BaseModel):
    """
    =================================================================================
    == THE VESSEL OF TEMPORAL GNOSIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)             ==
    =================================================================================
    A single, immutable verse in the Gnostic Chronicle. It is a perfect, atomic
    record of a state transition, its contract now eternally whole and unbreakable,
    honoring both the ancient and the ascended tongues.
    =================================================================================
    """
    # --- I. The Temporal & Causal Coordinates ---
    id: UUID = Field(default_factory=uuid4, description="The unique soul of this specific moment in time.")
    timestamp: float = Field(default_factory=time.time, description="The precise moment the vow was inscribed.")

    # --- II. The Will of the Artisan ---
    actor: str = Field(...,
                       description="The name of the Artisan that performed the rite (e.g., 'IOConductor', 'Maestro').")
    operation: LedgerOperation = Field(..., description="The sacred Gnostic verb of the action performed.")

    # --- III. The Scripture of Reversal (The Path Backwards) ---
    inverse_action: Optional[InverseOp] = Field(None,
                                                description="The precise, executable instructions for reversing this rite.")

    # === THE DIVINE HEALING: THE RESURRECTION OF THE ANCIENT TONGUE ===
    # These sacred, though legacy, attributes are resurrected to honor the ancient
    # contracts spoken by the IOConductor and MaestroUnit. The heresy of the
    # unexpected argument is annihilated for all time.
    reversible: bool = Field(True, description="[LEGACY] A vow proclaiming if this moment can be unwound.")
    inverse_state: Optional[Dict[str, Any]] = Field(None,
                                                    description="[LEGACY] The Gnosis required for the legacy reversal rite.")
    # === THE APOTHEOSIS IS COMPLETE ===

    # --- IV. The Quantum State Snapshot (THE SOUL OF THE PAST) ---
    snapshot_content: Optional[bytes] = Field(None,
                                              description="The raw, untransmuted soul (byte content) of a scripture as it existed before the rite.")
    snapshot_metadata: Dict[str, Any] = Field(default_factory=dict,
                                              description="The metadata of a scripture (permissions, mtime) before the rite.")

    # --- V. The Forward Gnosis (The Path Forwards) ---
    forward_state: Dict[str, Any] = Field(...,
                                          description="The Gnosis that was required to perform the original, forward rite.")

    # --- VI. Forensic Gnosis ---
    metadata: Dict[str, Any] = Field(default_factory=dict,
                                     description="Contextual Gnosis like source line numbers or blueprint origin.")


class RiteLedger(BaseModel):
    """
    =================================================================================
    == THE SCROLL OF A SINGLE RITE (ASCENDED)                                      ==
    =================================================================================
    The complete, ordered chronicle of a single transaction. This vessel holds the
    entire symphony of atomic actions performed during one Great Work, ready to be
    inscribed into the Void for the Chronomancer's future Gaze. Its name is now pure.
    =================================================================================
    """
    rite_id: str = Field(..., description="The unique ID of the transaction this ledger chronicles.")
    rite_name: str = Field(..., description="The sacred name of the rite that was conducted.")
    entries: List[LedgerEntry] = Field(default_factory=list, description="The ordered verses of the chronicle.")

class GnosticState(BaseModel):
    """
    =================================================================================
    == THE SOUL OF THE ENGINE                                                      ==
    =================================================================================
    The complete, serializable soul of the Scaffold Engine at a single moment in time.
    This is the vessel that is frozen into the Shadow Archive for forensic analysis
    or session restoration.
    """
    schema_version: str = "1.0"
    session_id: str
    variables: Dict[str, Any] = Field(default_factory=dict)

    # Prophecy: A future ascension will enshrine the complete file manifest,
    # dependency graph, and other Gnostic truths within this vessel for a
    # perfect, self-contained snapshot of reality.

