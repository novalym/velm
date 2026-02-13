# Path: src/velm/contracts/communion_contracts.py
# ---------------------------------------------------------------------------------
"""
=================================================================================
== THE TACTICAL SCHEMA FORTRESS (V-Ω-COMMUNION-CONTRACTS-V3000-MILITARY-GRADE) ==
=================================================================================
LIF: ∞ | ROLE: INTENT_MATERIALIZATION_PROTOCOL | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_COMMUNION_V3000_TRACE_FINALIS_2026

This scripture defines the unbreakable contracts for Gnostic Communion. It is the
DNA of the Sacred Dialogue, re-engineered for zero-latency, high-fidelity
intent transfer across the split-process lattice.
=================================================================================
"""

from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, Final
from pydantic import BaseModel, Field, ConfigDict
from rich.text import Text


class DialogueState(str, Enum):
    """
    =============================================================================
    == THE ONTOLOGY OF BEING (DialogueState)                                   ==
    =============================================================================
    Defines the current metaphysical coordinate of the Oracle's mind.
    """
    INQUIRY = "INQUIRY"  # Oracle is scrying for Gnosis
    ADJUDICATION = "ADJUDICATION"  # Council is judging the response
    PURIFICATION = "PURIFICATION"  # Matter is being scrubbed of entropy
    STATIONARY = "STATIONARY"  # The Mind is at rest/waiting
    COMPLETE = "COMPLETE"  # Genesis is manifest
    STAYED = "STAYED"  # The Architect has retracted the Will
    FRACTURED = "FRACTURED"  # A logic paradox has occurred


class GnosticPleaType(str, Enum):
    """
    =============================================================================
    == THE TAXONOMY OF INTENT (GnosticPleaType)                                ==
    =============================================================================
    Defines the physical form the input must take to satisfy the contract.
    """
    TEXT = "TEXT"  # Simple alphanumeric matter
    CONFIRM = "CONFIRM"  # Binary Truth/Falsehood
    CHOICE = "CHOICE"  # Selection from a willed set
    MULTILINE = "MULTILINE"  # Heavy prose or code matter
    VAULT_SECRET = "VAULT"  # High-entropy matter (auto-hidden)
    COORDINATE = "COORD"  # Filesystem path resolution


class PleaPriority(str, Enum):
    """[ASCENSION 5]: The Hierarchy of Importance."""
    IDENTITY = "IDENTITY"  # Core project DNA (Crucial)
    STRATA = "STRATA"  # Technology and Frameworks
    Maestro = "MAESTRO"  # Execution and Will
    AESTHETIC = "AESTHETIC"  # Visual and Stylistic Gnosis


class GnosticPlea(BaseModel):
    """
    =================================================================================
    == THE OMEGA PLEA VESSEL (V-Ω-TOTALITY-V3000-UNBREAKABLE)                      ==
    =================================================================================
    The definitive contract for a single unit of Gnostic Inquiry.
    Warded with the 12 Legendary Ascensions.
    """
    model_config = ConfigDict(
        frozen=True,  # [ASCENSION 12]: Immutability Vow
        arbitrary_types_allowed=True,
        extra='forbid'  # [ASCENSION 11]: Zero-Entropy Strictness
    )

    # --- I. THE SILVER CORD (CAUSAL IDENTITY) ---
    trace_id: str = Field(
        ...,
        description="The unique, globally-resonant ID linking this plea to the Akashic Record."
    )

    key: str = Field(
        ...,
        description="The Gnostic identifier (e.g. 'project_name') for the resulting variable."
    )

    # --- II. THE FORM OF THE INQUIRY ---
    plea_type: GnosticPleaType = Field(
        default=GnosticPleaType.TEXT,
        description="The expected structure of the incoming response."
    )

    prompt_text: Union[str, Text] = Field(
        ...,
        description="The luminous instruction projected to the Architect's Ocular Interface."
    )

    # --- III. THE GRIMOIRE OF CONSTRAINTS ---
    default: Optional[Any] = Field(
        None,
        description="The prophesied value if the Architect's will is silent."
    )

    choices: Optional[List[str]] = Field(
        None,
        description="The finite set of valid realities for CHOICE-type pleas."
    )

    validation_rule: str = Field(
        default='var_path_safe',
        description="The Jurisprudence rule warded against this plea (e.g. 'regex:^[a-z]+$')."
    )

    # --- IV. THE METADATA OF WILL ---
    priority: PleaPriority = Field(
        default=PleaPriority.STRATA,
        description="The gravity of this plea in the overall project inception."
    )

    is_secret: bool = Field(
        default=False,
        description="If True, the Ocular Membrane must shroud the input (Privacy Veil)."
    )

    special_rite: Optional[str] = Field(
        None,
        description="A specialized materialization rite (e.g. 'editor_inquest', 'port_scan')."
    )

    # --- V. THE OCULAR PROJECTION (UI HINTS) ---
    # [ASCENSION 9]: Instructions for the React/Monaco Membrane
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {
            "icon": "zap",
            "color": "#64ffda",
            "focus": True,
            "complexity": "low"
        },
        description="Non-logic hints for stylistic resonance in the Cockpit."
    )

    # --- VI. THE FORENSIC ANCHORS ---
    prophecy_source: Optional[str] = Field(
        None,
        description="The name of the Artisan or Oracle that prophesied the default value."
    )

    # =========================================================================
    # == CALCULATED REALITIES                                                ==
    # =========================================================================

    @property
    def is_terminal(self) -> bool:
        """[ASCENSION 10]: True if this plea requires direct terminal hijacking."""
        return self.special_rite is not None or self.plea_type == GnosticPleaType.MULTILINE

    def __repr__(self) -> str:
        return f"<Ω_PLEA key='{self.key}' trace='{self.trace_id[:8]}' type={self.plea_type.value}>"


class GnosticResponse(BaseModel):
    """
    =================================================================================
    == THE REVELATION VESSEL (GnosticResponse)                                     ==
    =================================================================================
    Carries the Architect's response back to the Mind.
    """
    model_config = ConfigDict(frozen=True)

    trace_id: str = Field(..., description="Must match the plea's silver cord.")
    value: Any = Field(..., description="The manifest Gnosis provided by the Architect.")
    duration_ms: float = Field(default=0.0, description="The temporal cost of the human decision.")
    is_pure: bool = Field(default=True, description="False if the Validator detected a minor heresy.")

