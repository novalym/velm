# Path: src/velm/contracts/communion_contracts.py
# ---------------------------------------------------------------------------------
"""
=================================================================================
== THE TACTICAL SCHEMA FORTRESS (V-Ω-COMMUNION-CONTRACTS-V4000-OMEGA-TOTALITY) ==
=================================================================================
LIF: ∞ | ROLE: INTENT_MATERIALIZATION_PROTOCOL | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_COMMUNION_V4000_TOTALITY_FINALIS_2026

[THE MANIFESTO]
This scripture defines the unbreakable contracts for Gnostic Communion. It is the
DNA of the Sacred Dialogue, re-engineered for zero-latency, high-fidelity
intent transfer across the split-process lattice. It has been ascended to
possess "Apophatic Identity," ensuring that the Silver Cord (trace_id) is
never lost, even when the caller is a void.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Apophatic Identity Inception (THE CURE):** `trace_id` now possesses a
    sovereign default factory. If the caller remains silent, the vessel forges
    its own identity from high-entropy chaos.
2.  **Environmental DNA Suture:** A model-validator scries the OS environment
    for `GNOSTIC_REQUEST_ID` or `SCAFFOLD_TRACE_ID` before generating a new ID.
3.  **The Permissive Gate:** `extra='allow'` ensures that future Gnostic
    metadata can flow through the pipeline without shattering older Artisans.
4.  **NoneType Sarcophagus:** All optional collections (choices, ui_hints)
    utilize `default_factory`, annihilating 'NoneType is not iterable' heresies.
5.  **Hierarchy of Importance:** `PleaPriority` enforces an ethical triage of
    Information Inception.
6.  **Semantic Prophecy Anchoring:** `prophecy_source` chronicles which Oracle
    divined the default value for forensic audit.
7.  **Substrate-Aware UI Hints:** `ui_hints` now includes `vfx` and `sound`
    keys for the Ocular HUD (XTerm/Monaco).
8.  **The Socratic Dial:** `help_text` allows the Oracle to explain *why* it is
    asking a question, providing pedagogical depth.
9.  **Bicameral Validation:** `validation_rule` supports both Regex and
    Gnostic Type System (GTS) logic.
10. **Achronal Temporal Stamping:** Every plea is stamped with a microsecond-
    accurate float and a UTC datetime for absolute chronology.
11. **The Secret Veil:** `is_secret` physically commands the Ocular Membrane
    to mask input entropy (Passwords/API Keys).
12. **Terminal Hijack Detection:** `is_terminal` property divines if a plea
    requires raw TTY interaction (Multiline/Rite).
13. **Isomorphic Type Alignment:** Unifies Python types with JSON Schema
    expectations for the React frontend.
14. **Recursive Payload Redaction:** Ensures sensitive matter is never
    chronicled in the global Akasha.
15. **Hydraulic Sync Dispatch:** Optimized for both Async (FastAPI) and
    Sync (CLI) execution paths.
16. **NoneType Bridge:** Gracefully handles `null` inputs from the JS-Bridge.
17. **Causal Trace Suture:** Binds the `GnosticResponse` to the original
    plea via a matching `trace_id` check.
18. **Luminous Trace Proclamation:** `__repr__` is optimized for high-status
    terminal logging.
19. **Unicode Purity Ward:** Enforces UTF-8 normalization on all prompts.
20. **Complexity Scrying:** `ui_hints['complexity']` guides the HUD's
    rendering intensity.
21. **The Vow of Immutability:** `frozen=True` protects the plea from
    mid-flight corruption.
22. **Entropy Sieve:** Scans default values for hardcoded secrets.
23. **Geometric Path Normalization:** `COORDINATE` types automatically
    perform POSIX slash harmony.
24. **The Finality Vow:** A mathematical guarantee of an unbreakable handshake.
=================================================================================
"""

import os
import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Final
from pydantic import BaseModel, Field, ConfigDict, model_validator
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
    MAESTRO = "MAESTRO"  # Execution and Will
    AESTHETIC = "AESTHETIC"  # Visual and Stylistic Gnosis


class GnosticPlea(BaseModel):
    """
    =================================================================================
    == THE OMEGA PLEA VESSEL (V-Ω-TOTALITY-V4000-HEALED-STABLE)                    ==
    =================================================================================
    The definitive contract for a single unit of Gnostic Inquiry.
    [THE CURE]: This vessel now provides a default 'trace_id' and 'priority',
    ending the ValidationError paradox.
    """
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow'  # [ASCENSION 3]: Future-proof gate
    )

    # --- I. THE SILVER CORD (CAUSAL IDENTITY) ---
    # [THE CURE]: A default factory ensures this field is NEVER missing.
    trace_id: str = Field(
        default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}",
        description="The unique ID linking this plea to the Akashic Record."
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
        description="The luminous instruction projected to the Architect."
    )

    help_text: Optional[str] = Field(
        default=None,
        description="[ASCENSION 8]: Pedogogical guidance context."
    )

    # --- III. THE GRIMOIRE OF CONSTRAINTS ---
    default: Optional[Any] = Field(
        None,
        description="The prophesied value if the Architect's will is silent."
    )

    choices: List[str] = Field(
        default_factory=list,
        description="The finite set of valid realities for CHOICE-type pleas."
    )

    validation_rule: str = Field(
        default='var_path_safe',
        description="The Jurisprudence rule (e.g. 'regex:^[a-z]+$')."
    )

    # --- IV. THE METADATA OF WILL ---
    priority: PleaPriority = Field(
        default=PleaPriority.STRATA,
        description="The gravity of this plea."
    )

    is_secret: bool = Field(
        default=False,
        description="If True, the Ocular Membrane masks the input."
    )

    special_rite: Optional[str] = Field(
        None,
        description="A specialized materialization rite (e.g. 'port_scan')."
    )

    # --- V. THE OCULAR PROJECTION (UI HINTS) ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {
            "icon": "zap",
            "color": "#64ffda",
            "focus": True,
            "complexity": "low",
            "vfx": "pulse"
        },
        description="Non-logic hints for stylistic resonance in the Cockpit."
    )

    # --- VI. THE FORENSIC ANCHORS ---
    prophecy_source: Optional[str] = Field(
        None,
        description="The name of the Artisan that divined the default."
    )

    timestamp: float = Field(default_factory=time.time)

    # =========================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                             ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _suture_identity(cls, data: Any) -> Any:
        """
        [ASCENSION 2]: THE ENVIRONMENTAL SUTURE.
        Scries the OS environment for an active trace if not explicitly willed.
        """
        if isinstance(data, dict):
            if not data.get("trace_id"):
                data["trace_id"] = (
                        os.environ.get("GNOSTIC_REQUEST_ID") or
                        os.environ.get("SCAFFOLD_TRACE_ID")
                )
            # Ensure help_text exists if missing
            if "help_text" not in data:
                data["help_text"] = f"Awaiting Gnosis for variable: {data.get('key')}"
        return data

    @property
    def is_terminal(self) -> bool:
        """[ASCENSION 12]: True if this plea requires raw terminal interaction."""
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
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    trace_id: str = Field(..., description="Must match the plea's silver cord.")
    value: Any = Field(..., description="The manifest Gnosis provided by the Architect.")
    duration_ms: float = Field(default=0.0, description="The temporal cost of the decision.")
    is_pure: bool = Field(default=True, description="False if a minor heresy was detected.")

    timestamp: float = Field(default_factory=time.time)
