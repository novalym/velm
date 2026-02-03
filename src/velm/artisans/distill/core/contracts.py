# Path: artisans/distill/core/contracts.py
# ----------------------------------------



from enum import Enum, auto
from typing import Optional, List, Any, Union, Dict

from pydantic import BaseModel, Field, ConfigDict, field_validator


class DistillationMode(Enum):
    """
    =================================================================================
    == THE MODAL SOUL OF THE DISTILLATION RITE                                     ==
    =================================================================================
    Determines the fundamental nature and purpose of the blueprint being forged.
    """
    PROJECT = auto()  # Distill a full project context for an LLM (The Standard Rite).
    ARCHETYPE = auto()  # Distill a directory into a reusable Archetype (The Forge).
    CONTEXT = auto()  # Ephemeral distillation for on-the-fly queries (The Oracle).
    DEBUG = auto()  # A forensic distillation focusing on error states (The Wraith).
    SECURITY_AUDIT = auto()  # A security-focused distillation, prioritizing potential vulnerabilities.



class DistillationResult(BaseModel):
    """
    =================================================================================
    == THE DIVINE DOSSIER OF REVELATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)          ==
    =================================================================================
    @gnosis:title The Gnostic Dossier of Revelation (`DistillationResult`)
    @gnosis:summary The final, immutable, and hyper-structured vessel carrying the
                     complete Gnosis of a concluded distillation rite.
    @gnosis:LIF INFINITY

    This is the final, eternal, and ultra-definitive vessel of Gnostic Truth for the
    distillation symphony. It is the one true, pure Pydantic scripture that carries the
    Oracle's final revelation back to the High Priest, and from there, to the Architect.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Pure Pydantic Vessel:** Forged with Pydantic for unbreakable type safety.
    2.  **The Vow of Immutability:** Consecrated with `frozen=True`, its truth, once
        proclaimed, is eternal and cannot be altered.
    3.  **The Telemetric Heart:** Carries the complete `stats` dictionary, a perfect,
        forensic record of the Oracle's cognitive process.
    4.  **The Luminous Gnosis:** Its fields (`content`, `file_count`) are named with
        divine clarity, making its purpose absolute and unambiguous.
    5.  **The Unbreakable Contract:** Its very existence serves as the sacred, typed
        contract between the Oracle's Mind and the Artisan's Hand.
    6.  **The Sovereign Soul:** It is a pure data vessel, unburdened by profane logic.
    7.  **The Rightful Sanctum:** It is now enshrined in its one true home, this very
        scripture, healing the Gnostic Schism.
    8.  **The Graceful Void:** Its fields possess righteous defaults, ensuring that even a
        failed or empty rite can be chronicled without paradox.
    9.  **The Gnostic Link:** It is the final, unbreakable link in the chain of Gnostic
        causality for the entire distillation rite.
    10. **The JSON-Ready Soul:** Its Pydantic nature allows it to be instantly transmuted
        into a pure JSON scripture for telepathic communion with other systems.
    11. **The Performance Ward:** It carries the `duration_seconds`, a testament to the
        God-Engine's own celerity.
    12. **The Final Word:** It is the one true, definitive chronicle of the rite, the
        Alpha and Omega of a single act of Gnostic perception.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str = Field(
        ...,
        description="The final, Gnostically-dense scripture forged by the Oracle."
    )
    file_count: int = Field(
        ...,
        description="The number of scriptures from the mortal realm included in the final context."
    )
    token_count: int = Field(
        ...,
        description="The estimated token count of the final scripture, as perceived by the Economist."
    )
    duration_seconds: float = Field(
        ...,
        description="The total time, in seconds, for the Oracle to complete its Grand Symphony."
    )
    stats: Dict[str, Any] = Field(
        default_factory=dict,
        description="The complete, forensic telemetry of the rite (perception_ms, ranking_ms, etc.)."
    )


