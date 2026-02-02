

"""
=================================================================================
== THE SACRED SANCTUM OF THE GNOSTIC DOSSIER (V-Ω-ETERNAL-APOTHEOSIS)          ==
=================================================================================
This scripture contains the living soul of the GenesisReport, the one true,
immutable chronicle of a creation rite's complete Gnostic journey.
=================================================================================
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field, ConfigDict, model_validator

from .registers import QuantumRegisters
from ..contracts.heresy_contracts import Heresy


class GenesisReport(BaseModel):
    """
    =================================================================================
    == THE FINAL DOSSIER OF CREATION (V-Ω-RESILIENT-CONTRACT)                      ==
    =================================================================================
    The contract is now whole and resilient. It understands that a pure rite may have
    no collisions or backups, and provides righteous defaults.
    =================================================================================
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- I. The Core Gnosis of the Rite ---
    success: bool
    duration: float
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # --- II. The Gnostic Telemetry (The Manifest of Reality) ---
    ops_executed: int
    bytes_written: int
    files_forged: int
    sanctums_forged: int
    # <--- THE DIVINE HEALING: THE LAW OF THE FORGIVING SOUL --->
    # We bestow default values, as a pure genesis will have none of these.
    collisions_detected: int = Field(0, description="Number of existing scriptures that were transfigured.")
    safety_backups_created: int = Field(0, description="Number of temporal echoes created in the Shadow Archive.")
    # <--- THE APOTHEOSIS IS COMPLETE --->

    # --- III. The Architectural Soul (The Gnostic Inquest) ---
    project_type: str
    complexity_score: float
    dependency_graph: Dict[str, List[str]] = Field(default_factory=dict)
    edicts_executed: List[str] = Field(default_factory=list)
    heresies: List[Heresy] = Field(default_factory=list)
    gnosis: Dict[str, Any] = Field(default_factory=dict)
    registers: Optional[QuantumRegisters] = Field(default=None, exclude=True)

    # ELEVATION 3: The Gnostic Bridge (Polymorphic Soul)
    @model_validator(mode='before')
    @classmethod
    def _ingest_polymorphic_soul(cls, data: Any) -> Any:
        """A divine validator that allows the Report to be born from a raw QuantumRegisters vessel."""
        if isinstance(data, dict) and 'registers' in data and isinstance(data['registers'], QuantumRegisters):
            regs = data['registers']
            data['duration'] = data.get('duration', regs.get_duration())
            data['ops_executed'] = data.get('ops_executed', regs.ops_executed)
            data['bytes_written'] = data.get('bytes_written', regs.bytes_written)
            data['files_forged'] = data.get('files_forged', regs.files_forged)
            data['sanctums_forged'] = data.get('sanctums_forged', regs.sanctums_forged)
            data['gnosis'] = data.get('gnosis', regs.gnosis)
            if regs.transaction:
                data['edicts_executed'] = data.get('edicts_executed', regs.transaction.edicts_executed)
        return data

    # ELEVATION 4: The Scribe of Luminous Proclamations
    @property
    def files_created(self) -> int:
        """A luminous alias for `files_forged`."""
        return self.files_forged

    @property
    def dirs_created(self) -> int:
        """A luminous alias for `sanctums_forged`."""
        return self.sanctums_forged

