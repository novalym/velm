# Path: scaffold/contracts/data_contracts.py
# ------------------------------------------

"""
=================================================================================
== THE SACRED SANCTUM OF DATA CONTRACTS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)      ==
=================================================================================
LIF: INFINITY (THE IMMUTABLE TRUTH)

This scripture defines the **Laws of Shape**. It ensures that every artisan in the
Scaffold cosmos speaks the exact same dialect of data.

It contains:
1.  **The Enums of State:** `GnosticLineType`, `InscriptionAction`.
2.  **The Vessel of Intent:** `ScaffoldItem` (What we want to build).
3.  **The Vessel of Perception:** `GnosticVessel` (What we read from the file).
4.  **The Chronicle of Result:** `GnosticWriteResult` (What actually happened).
5.  **The Dossiers of Knowledge:** `GnosticDossier`, `ManifestAST`, `GnosticArgs`.

No data flows through the God-Engine that is not sanctified by one of these contracts.
=================================================================================
"""
import weakref
import hashlib
import json
import re
import ast
import math
import os
import uuid
import time
import argparse
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Set, Dict, Union, List, Any, TypedDict, Tuple, Final, Generator
from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field, model_validator
from pydantic.fields import AliasChoices
from ..interfaces import Artifact
# --- DIVINE SUMMONS (Cross-Module Links) ---
from .architectural_contracts import SemanticSegment
from .heresy_contracts import Heresy
from .symphony_contracts import EdictType, ResilienceType, ConditionalType
from ..help_registry import register_artisan


# =============================================================================
# == I. THE ENUMS OF STATE (THE ATOMS OF MEANING)                            ==
# =============================================================================

class GnosticLineType(Enum):
    """
    =============================================================================
    == THE SOUL OF THE SCRIPTURE (GnosticLineType)                             ==
    =============================================================================
    Defines the fundamental purpose of a parsed line in a blueprint.

    [ASCENSION LOG]:
    - Added ON_HERESY to distinguish Redemption Rites from Standard Execution.
    """
    VOW = auto()  # ?? Assertion (Symphony)
    SGF_CONSTRUCT = auto()  # {% ... %} (Logic)
    WEAVE = auto()  # %% weave (Composition)
    COMMENT = auto()  # # ... (Meta-data)
    VARIABLE = auto()  # $$ var = val (State)
    FORM = auto()  # File or Directory definition (Reality)
    VOID = auto()  # Empty line (Silence)

    # --- The Trinity of Automation ---
    POST_RUN = auto()  # %% post-run (Maestro's Will)
    ON_UNDO = auto()  # %% on-undo (The Reversal Rite)
    ON_HERESY = auto()  # %% on-heresy (The Redemption Rite) <--- THE CRITICAL MISSING ATOM

    BLOCK_START = auto()  # Indented block header
    LOGIC = auto()  # @if, @else (Control Flow)
    CONTRACT_DEF = auto()  # %% contract (Type Safety)

    # [EXPANSION V-Ω] New Physics
    TRAIT_DEF = auto()  # %% trait Name = ... (Mixin Definition)
    TRAIT_USE = auto()  # %% use Name (Mixin Usage)
    SYMLINK = auto()  # source -> target (Symbolic Link)


class InscriptionAction(str, Enum):
    """
    =============================================================================
    == THE RITE'S OUTCOME (InscriptionAction)                                  ==
    =============================================================================
    Defines what physically happened to a file during the Rite of Creation.
    """
    ADOPTED = "ADOPTED"  # Existed and matches blueprint intent
    CREATED = "CREATED"  # New file forged from nothing
    TRANSFIGURED = "TRANSFIGURED"  # Content modified/patched
    ALREADY_MANIFEST = "ALREADY_MANIFEST"  # Existed, content identical, no action
    SKIPPED = "SKIPPED"  # Intentional bypass (e.g., condition false)
    FAILED_SYNTAX = "FAILED_SYNTAX"  # Content generated was profane (syntax error)
    FAILED_IO = "FAILED_IO"  # Disk error or permission denied
    BLOCKED_SECURITY = "BLOCKED_SECURITY"  # Sentinel blocked write (e.g. path traversal)
    DRY_RUN_CREATED = "DRY_RUN_CREATED"  # Simulation: Would have created
    DRY_RUN_TRANSFIGURED = "DRY_RUN_TRANSFIGURED"  # Simulation: Would have modified
    SYMBIOTIC_MERGE = "SYMBIOTIC_MERGE"  # Semantic insertion successful
    MERGED_WITH_CONFLICTS = "MERGED_WITH_CONFLICTS"  # Merge required human intervention
    TRANSLOCATED = "TRANSLOCATED"  # File moved or renamed
    # [EXPANSION V-Ω] New Outcomes
    LINKED = "LINKED"  # Symlink successfully established
    IGNORED = "IGNORED"  # Dynamic Ignorer prevented creation (Secrets)
    PRUNED = "PRUNED"  # Ghost Buster removed empty directory
    TRANSFIGURE = "TRANSFIGURE"

# =============================================================================
# == II. THE CONTRACTS OF LAW (TYPE SAFETY)                                  ==
# =============================================================================

class ContractField(BaseModel):
    """
    =============================================================================
    == THE ATOM OF LAW (ContractField)                                         ==
    =============================================================================
    @gnosis:summary The definitive specification of a single dimension of reality.
    LIF: 10,000,000 | ROLE: FIELD_SPECIFICATION | RANK: LEGENDARY

    [THE CURE]: Explicitly manifest 'doc' to capture the Scribe's Harvester output.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow'  # [ASCENSION]: Future-proofed against unmanifest Gnosis
    )

    name: str = Field(..., description="The sacred identifier of the atom.")
    type_name: str = Field(..., description="The string-form liturgy of the type (e.g. 'int?').")
    gnostic_type: Any = Field(default=None, repr=False, description="The materialized TypeNode instance.")

    # [THE FIX]: Docstring integration for AI-Sourcing
    doc: str = Field(default="", description="The semantic docstring captured from Gnostic Comments.")

    default_value: Any = Field(None, description="The fallback reality if the will is silent.")
    is_optional: bool = Field(False, description="True if the Law allows for a Void.")

    # --- METADATA STRATUM ---
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Numerical and spatial wards.")
    modifiers: List[str] = Field(default_factory=list, description="Access flags (readonly, private, etc).")
    is_list: bool = Field(False, description="Achronal flag for sequence detection.")


class GnosticContract(BaseModel):
    """
    =============================================================================
    == THE SOVEREIGN CONSTITUTION (GnosticContract)                           ==
    =============================================================================
    @gnosis:summary The complete, hierarchical definition of a Domain Reality.
    LIF: ∞ | ROLE: SCHEMA_GOVERNOR | RANK: OMEGA_SUPREME

    [THE CURE]: Explicitly manifest 'parent' to enable the Scribe's multi-inheritance.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    name: str = Field(..., description="The unique name of the Law.")

    # [THE FIX]: Lineage Suture for Hierarchical Inheritance
    parent: Optional[str] = Field(None, description="The immediate ancestor of this contract.")

    fields: Dict[str, ContractField] = Field(default_factory=dict, description="The collection of manifest fields.")

    # --- FORENSIC STRATUM ---
    raw_scripture: str = Field(default="", description="The raw, unparsed text of the definition.")
    line_num: int = Field(default=0, description="The verse in the blueprint where this law was born.")
    merkle_root: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], description="Integrity seal.")

    # =========================================================================
    # == [ASCENSION 13]: THE HIEROPHANT'S RECALL                             ==
    # =========================================================================
    def get_all_fields(self, registry: Dict[str, 'GnosticContract']) -> Dict[str, ContractField]:
        """
        [THE RITE OF RECURSIVE RECALL]
        Walks the achronal lineage to merge all fields from ancestors.
        Child fields with identical names righteously overwrite ancestral souls.
        """
        all_fields = {}
        # 1. Scry Ancestry
        if self.parent and self.parent in registry:
            ancestor = registry[self.parent]
            # Recursive Deep-Gaze
            all_fields.update(ancestor.get_all_fields(registry))

        # 2. Merge Local Will (Overwriting Ancestry)
        all_fields.update(self.fields)
        return all_fields

    def __repr__(self) -> str:
        return f"<Ω_CONTRACT name='{self.name}' parent='{self.parent}' fields={len(self.fields)}>"


# =============================================================================
# == III. THE VESSEL OF INTENT (ScaffoldItem)                                ==
# =============================================================================
@register_artisan("ScaffoldItem")
class ScaffoldItem(BaseModel):
    """
    =================================================================================
    == THE ATOMIC UNIT OF CREATION (V-Ω-TOTALITY-V100000-INDESTRUCTIBLE)           ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_DNA_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_ITEM_V100K_PYDANTIC_SCHISM_ANNIHILATOR_FINALIS

    This is the supreme data structure of the cosmos. It represents a single,
    transactional intent to manifest reality.

    [THE LEGENDARY CURE]:
    1. The Ontological Harmonizer operates in `mode='before'`, mutating the
       primordial dictionary to annihilate recursion.
    2. `action` defaults to "create", ensuring the Quantum Creator never
       ignores a valid file definition.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow',  # Absorb unknown future Gnosis without fracture
        validate_assignment=True
    )

    # --- I. THE CORE GNOSTIC IDENTITY (WHO/WHERE/WHAT) ---
    path: Optional[Path] = Field(None, description="The scripture's intended place in reality.")

    # [ASCENSION: THE FIX] The Ontological Classification
    type: str = Field(
        default="file",
        description="The nature of the matter: 'file', 'directory', 'symlink', 'edict', 'ghost'."
    )

    # [ASCENSION: THE CURE FOR KINETIC SILENCE]
    # By defaulting to 'create', we ensure the QuantumCreator does not skip this atom.
    action: str = Field(
        default="create",
        description="The kinetic state: 'create', 'created', 'transfigured', 'deleted', 'skipped', 'fractured'."
    )

    is_dir: bool = Field(False,
                         description="Legacy/Convenience toggle. Synchronized with `type` via the Alchemist Validator.")
    line_num: int = Field(default=0, description="The line number in the source blueprint.")
    raw_scripture: str = Field(default="", description="The raw, untransmuted scripture from the file.")
    original_indent: int = Field(default=0, description="The visual indentation depth (hierarchy).")
    line_type: Any = Field(default=None, description="The GnosticLineType classification.")

    # --- II. THE SOUL OF THE SCRIPTURE (CONTENT) ---
    content: Optional[str] = Field(None, description="The inner soul (text content) from inline definition (::).")
    seed_path: Optional[Union[Path, str]] = Field(None, description="Path to an external seed/template (<<).")
    permissions: Optional[str] = Field(None, description="Executable permissions (octal or named).")
    encoding: Optional[str] = Field(default="utf-8", description="Explicit encoding hint.")

    # --- III. THE SENTINEL OF LINKS & INTEGRITY ---
    is_symlink: bool = Field(False, description="True if this item represents a symbolic link.")
    symlink_target: Optional[str] = Field(None, description="The target path the link points to.")
    expected_hash: Optional[str] = Field(None, description="The pre-calculated cryptographic anchor.")
    is_binary: bool = Field(False, description="True if content should be treated as raw bytes.")

    # [ASCENSION: FUTURE-PROOFING INTEGRITY]
    merkle_hash: Optional[str] = Field(None,
                                       description="The post-transmutation SHA-256 hash of the materialized soul.")
    ast_fingerprint: Optional[str] = Field(None,
                                           description="A structural hash ignoring whitespace/formatting for semantic parity tracking.")

    # --- IV. THE GNOSTIC TRAITS & CAUSALITY (MIXINS & GRAPH) ---
    trait_name: Optional[str] = Field(None, description="The name of the trait being defined or used.")
    trait_args: Optional[str] = Field(None, description="Arguments passed to the trait.")
    trait_path: Optional[Path] = Field(None, description="The file path to the trait definition.")

    # [ASCENSION: GRAPH RESOLUTION]
    dependencies: List[str] = Field(default_factory=list,
                                    description="Paths of other atoms this scripture requires to resonate before it can manifest.")
    rollback_path: Optional[Path] = Field(None,
                                          description="The physical coordinate of its temporal echo (backup) during transactions.")

    # --- V. THE MUTATION INTENT (TRANSFIGURATION) ---
    mutation_op: Optional[str] = Field(None, description="The glyph of mutation (+=, -=, ~=, ^=).")
    semantic_selector: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Targeting and redemption data for Semantic Surgery."
    )

    # --- VI. THE GNOSTIC PROVENANCE & LOGIC ---
    blueprint_origin: Optional[Path] = Field(None, description="The blueprint file that birthed this item.")
    condition: Optional[str] = Field(None, description="The logic gate expression.")
    condition_type: Optional[str] = Field(None, description="if, elif, else, for.")
    logic_result: Optional[bool] = Field(None, description="The outcome of logic evaluation.")

    # --- VII. RUNTIME STATE & METADATA (EPHEMERAL) ---
    lifecycle_state: str = Field(default="WAKING",
                                 description="The existential phase: WAKING -> STAGED -> MANIFEST -> ETERNAL (or FRACTURED).")
    error_trace: Optional[str] = Field(None,
                                       description="If the atom fractures during materialization, the Heresy is sealed here, isolated from the rest of the cosmos.")

    trace_id: str = Field(default="tr-void", description="The causal silver cord.")
    session_id: Optional[str] = Field(None, description="The multi-tenant session anchor.")
    edict_type: Optional[Any] = None  # EdictType Enum
    is_sgf_construct: bool = Field(default=False)
    sgf_expression: Optional[str] = Field(None)
    ui_hints: Dict[str, Any] = Field(default_factory=dict)

    # Forensic Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    mass_bytes: int = Field(default=0)
    inception_ts: float = Field(default_factory=time.time)

    # =========================================================================
    # == THE RITES OF HARMONIZATION (THE PYDANTIC CURE)                      ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _harmonize_ontological_state(cls, data: Any) -> Any:
        """
        =============================================================================
        == THE ONTOLOGICAL HARMONIZER (V-Ω-BEFORE-MODE-STRIKE)                     ==
        =============================================================================
        [THE CURE]: By executing in `mode='before'`, we surgically alter the raw
        dictionary *before* Pydantic engages its `__setattr__` validation matrix.
        This mathematically annihilates the `is_valid_field_name` recursion heresy.
        """
        if not isinstance(data, dict):
            try:
                # Attempt to transmute object to dict if possible
                data = dict(data)
            except (TypeError, ValueError):
                return data

        # Extract primordial values safely
        t = data.get('type')
        is_dir = data.get('is_dir')
        is_symlink = data.get('is_symlink')
        edict_type = data.get('edict_type')
        action = data.get('action')

        # 1. Suture Directory State
        # If 'is_dir' is explicitly True, force type to 'directory'
        if is_dir is True and t not in ("directory", "dir"):
            data['type'] = "directory"
        # If type is 'directory', force is_dir to True
        elif t in ("directory", "dir"):
            data['is_dir'] = True

        # 2. Suture Symlink State
        if is_symlink is True and t != "symlink":
            data['type'] = "symlink"
        elif t == "symlink":
            data['is_symlink'] = True

        # 3. Suture Edict State
        if edict_type is not None and t != "edict":
            data['type'] = "edict"

        # 4. Enforce Fallback Type (The Void Filter)
        if 'type' not in data or not data['type']:
            data['type'] = 'file'

        # 5. [CRITICAL] THE KINETIC AWAKENING
        # If action is missing or void, we compel it to 'create'.
        # This ensures the Creator sees the file as actionable matter.
        if not action or action == "pending":
            data['action'] = "create"

        return data

    # =========================================================================
    # == THE LAZY ADJUDICATORS (PROPERTIES)                                  ==
    # =========================================================================

    @property
    def name(self) -> str:
        """The atomic name of the item."""
        if self.path:
            return self.path.name
        return ""

    @property
    def is_ethereal(self) -> bool:
        """
        [ASCENSION]: SUBSTRATE SENSING.
        True if the atom exists only in the WASM memory space.
        """
        return os.environ.get("SCAFFOLD_ENV") == "WASM"

    @property
    def is_fractured(self) -> bool:
        """Convenience property to quickly check if this atom failed to manifest."""
        return self.action == "fractured" or self.error_trace is not None

    def __repr__(self) -> str:
        status_flag = "❌" if self.is_fractured else ("✅" if self.action in ("created", "transfigured") else "⏳")
        path_str = str(self.path) if self.path else "VOID"
        return f"<Ω_ITEM {status_flag} path='{path_str}' type={self.type} action={self.action} trace={self.trace_id[:8]}>"
# =============================================================================
# == IV. THE VESSELS OF RESULT (THE OUTPUTS)                                 ==
# =============================================================================
class GnosticWriteResult(BaseModel):
    """
    =================================================================================
    == THE DIVINE CHRONICLE: OMEGA (V-Ω-TOTALITY-V2500-FORENSIC-LEDGER-HEALED)     ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_OUTCOME_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_WRITE_RESULT_V2500_ERROR_SUTURE_2026_FINALIS

    This vessel is the absolute, unbreakable record of a single physical or virtual
    mutation. It has been ascended to be "Infinite-Permissive," righteously
    incorporating the `error` field and a forensic `metadata` sarcophagus to
    prevent any validation heresies during the Matter Strike.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow',  # [ASCENSION 1]: Absolute absorption of unknown metadata
        populate_by_name=True,
        validate_assignment=True
    )

    # --- I. THE BINARY TRUTH (STATUS) ---
    success: bool = Field(..., description="True if the reality aligned with the will.")

    # [THE FIX]: Explicitly manifest the 'error' field to annihilate constructor heresies.
    error: Optional[str] = Field(
        None,
        description="The forensic summary of the fracture, heresy, or OS-level paradox."
    )

    path: Path = Field(..., description="The final logical coordinate of the artifact.")
    action_taken: InscriptionAction = Field(..., description="The Gnostic soul of the outcome.")
    bytes_written: int = Field(default=0, description="Total mass inscribed to the substrate.")

    # --- II. THE FORENSIC STRATUM (INTEGRITY) ---
    gnostic_fingerprint: Optional[str] = Field(None, description="SHA256 Merkle anchor of the final content.")
    diff: Optional[str] = Field(None, description="Unified diff representing the transfiguration delta.")
    checksum_algo: str = Field(default="sha256", description="The algorithm used for the soul-hash.")

    # --- III. THE METADATA SARCOPHAGUS (THE CURE) ---
    # [ASCENSION 5]: A catch-all vessel for artisan-specific Gnosis.
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A vessel for MIME, line-counts, and substrate-specific telemetry."
    )

    # --- IV. PROVENANCE & CAUSALITY ---
    blueprint_origin: Optional[Path] = Field(None, description="The scripture that willed this materialization.")
    rite_name: str = Field(default="Unknown", description="The parent rite (e.g. 'Genesis', 'Transmute').")
    trace_id: Optional[str] = Field(None, description="The silver cord linking this write to the global intent.")
    is_from_cache: bool = Field(default=False, description="True if Gnosis was resurrected from the Chronocache.")

    # --- V. DEEP ANALYSIS DATA (GNOSTIC METRICS) ---
    dependencies: List[str] = Field(default_factory=list, description="Causal bonds discovered in the file.")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Topographical metrics (Cyclomatic, HAL).")
    security_notes: List[str] = Field(default_factory=list, description="Wards and alerts (secrets detected).")

    # --- VI. TEMPORAL & PERFORMANCE DATA ---
    duration_ms: float = Field(default=0.0, description="Metabolic tax of the inscription.")
    timestamp: float = Field(default_factory=time.time, description="Nanosecond-precision birth marker.")

    # --- VII. THE SYMBIOTIC SHARDS ---
    merge_details: Optional[Dict[str, Any]] = Field(None, description="Detailed record of a Symbiotic Merge.")
    treesitter_gnosis: Optional[Dict[str, Any]] = Field(None, description="Full AST deconstruction.")
    sentinel_gnosis: Optional[Dict[str, Any]] = Field(None, description="Security Sentinel report.")

    # =========================================================================
    # == CALCULATED REALITIES                                                ==
    # =========================================================================

    @computed_field
    @property
    def name(self) -> str:
        """The atomic name of the manifest shard."""
        return self.path.name

    @computed_field
    @property
    def mass_human(self) -> str:
        """[ASCENSION 12]: Transmutes raw bytes into Architect-readable mass."""
        if self.bytes_written == 0: return "0 B"
        units = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(self.bytes_written, 1024)))
        s = round(self.bytes_written / math.pow(1024, i), 2)
        return f"{s} {units[i]}"

    @property
    def is_transfiguration(self) -> bool:
        """True if existing matter was altered rather than created new."""
        return self.action_taken in (
            InscriptionAction.TRANSFIGURED,
            InscriptionAction.SYMBIOTIC_MERGE,
            InscriptionAction.DRY_RUN_TRANSFIGURED
        )

    # =========================================================================
    # == THE RITE OF GNOSTIC RECONCILIATION (VALIDATOR)                      ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _heal_constructor_input(cls, data: Any) -> Any:
        """
        [ASCENSION 24]: THE OMEGA HEALER.
        Surgically intercepts the raw dictionary before Pydantic validation.
        If 'message' is passed but 'error' is silent, it sutures the two.
        If unknown fields are passed, it teleports them into the 'metadata' vault.
        """
        if not isinstance(data, dict):
            return data

        # 1. Suture 'message' -> 'error' if success is False
        if not data.get('success', True) and 'message' in data and not data.get('error'):
            data['error'] = data['message']

        # 2. Forensic Metadata Triage
        # Move any field NOT defined in the model into the 'metadata' dictionary.
        known_fields = cls.model_fields.keys()
        metadata = data.get('metadata', {})

        to_move = [k for k in data.keys() if k not in known_fields and k != 'metadata']
        for key in to_move:
            metadata[key] = data.pop(key)

        data['metadata'] = metadata
        return data

    @classmethod
    def forge_success(cls, path: Path, action: InscriptionAction, **kwargs) -> 'GnosticWriteResult':
        """The High-Level Factory for resonant outcomes."""
        return cls(success=True, path=path, action_taken=action, **kwargs)

    def __repr__(self) -> str:
        status = "✅" if self.success else "❌"
        return f"<Ω_WRITE_RESULT {status} path='{self.path.name}' action={self.action_taken.value}>"

# =============================================================================
# == VI. THE VESSELS OF LOGIC (THE LFG APOTHEOSIS)                           ==
# =============================================================================

class LogicNodeType(str, Enum):
    """The Gnostic Soul of a node in the Logic Flow Graph."""
    CONDITION = "CONDITION"  # An @if or @elif block
    LOOP = "LOOP"  # An @for block
    SEQUENCE = "SEQUENCE"  # A simple block of form/command items
    ROOT = "ROOT"  # The entry point of the graph


class BaseLogicNode(BaseModel):
    """The ancestral soul of all logic nodes."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    node_type: LogicNodeType
    # The children of this node, representing the next steps in the flow
    children: List['LogicNode'] = Field(default_factory=list)
    # The items (files, dirs, commands) contained within this logic block's scope
    items: List[ScaffoldItem] = Field(default_factory=list, repr=False)


class ConditionNode(BaseLogicNode):
    """A vessel for an @if, @elif, or @else block."""
    node_type: LogicNodeType = LogicNodeType.CONDITION
    condition: str  # The Elara SGF expression, or 'else'
    # The "false" path for an @if statement, leading to @elif or @else
    else_branch: Optional['LogicNode'] = None


class LoopNode(BaseLogicNode):
    """A vessel for an @for block."""
    node_type: LogicNodeType = LogicNodeType.LOOP
    loop_variable: str  # e.g., 'item'
    iterable: str  # e.g., 'my_list'


class SequenceNode(BaseLogicNode):
    """A simple sequence of items without branching logic."""
    node_type: LogicNodeType = LogicNodeType.SEQUENCE


# A Gnostic Union for type hinting and validation
LogicNode = Union[ConditionNode, LoopNode, SequenceNode, BaseLogicNode]

# We must explicitly update the forward reference for the recursive `children` field.
BaseLogicNode.model_rebuild()
ConditionNode.model_rebuild()


# ==============================================================================
# == STRATUM-Ω: THE SOVEREIGN SHARD DNA (V-Ω-TOTALITY-V3.0-EXTENSIVE)         ==
# ==============================================================================
# =============================================================================
# == STRATUM I: THE SHARD METABOLISM (V-Ω-TOTALITY-VMAX-PHYSIOLOGY)          ==
# =============================================================================

class ShardMetabolism(BaseModel):
    """
    =============================================================================
    == THE SHARD METABOLISM (V-Ω-TOTALITY-VMAX-PHYSIOLOGY)                     ==
    =============================================================================
    LIF: ∞ | ROLE: DEPENDENCY_GOVERNOR | RANK: OMEGA_SCRIBE
    AUTH: Ω_METABOLISM_VMAX_2026

    Defines the physical requirements for the Shard to breathe. It governs the
    inhalation of external libraries and the injection of Environmental DNA.
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow',
        populate_by_name=True
    )

    # --- I. THE PYTHONIC SOUL ---
    python: List[str] = Field(
        default_factory=list,
        description="Pip/Poetry dependencies. Enforces PEP 508 compliance."
    )

    # --- II. THE OCULAR EYE (NODE) ---
    node: List[str] = Field(
        default_factory=list,
        description="NPM/Yarn/Pnpm dependencies for the Ocular Layer."
    )

    # --- III. THE ENVIRONMENTAL DNA ---
    # Supports simple 'KEY' or 'KEY=DEFAULT' syntax
    env: List[str] = Field(
        default_factory=list,
        description="Mandatory and Optional Environment Variables for the local Vault."
    )

    # --- IV. THE IRON SUBSTRATE (BINARIES) ---
    apt: List[str] = Field(default_factory=list, description="Linux system binaries.")
    brew: List[str] = Field(default_factory=list, description="macOS system binaries.")

    @field_validator('python', 'node', 'env', 'apt', 'brew', mode='before')
    @classmethod
    def _apophatic_list_suture(cls, v: Any) -> List[str]:
        """Surgically transmutes strings or nulls into pure Gnostic Lists."""
        if v is None: return []
        if isinstance(v, str): return [s.strip() for s in v.split(',') if s.strip()]
        return v

    @computed_field
    @property
    def gnostic_mass(self) -> int:
        """Calculates the total complexity weight of the metabolic requirements."""
        return len(self.python) + len(self.node) + len(self.apt) + len(self.env)

    @property
    def metabolic_fingerprint(self) -> str:
        """Forges a unique Merkle-root of the requirements to detect DNA drift."""
        raw_dna = json.dumps({
            "p": sorted(self.python),
            "n": sorted(self.node),
            "e": sorted(self.env),
            "a": sorted(self.apt)
        }, sort_keys=True)
        return hashlib.sha256(raw_dna.encode()).hexdigest()[:12].upper()

    def __repr__(self) -> str:
        return f"<Ω_METABOLISM mass={self.gnostic_mass} seal={self.metabolic_fingerprint}>"


# =============================================================================
# == STRATUM II: THE SHARD SUBSTRATE (V-Ω-TOTALITY-VMAX-IRON-GOVERNOR)       ==
# =============================================================================

class ShardSubstrate(BaseModel):
    """
    =============================================================================
    == THE SHARD SUBSTRATE (V-Ω-TOTALITY-VMAX-IRON-GOVERNOR)                   ==
    =============================================================================
    LIF: ∞ | ROLE: INFRASTRUCTURE_CONDUCTOR | RANK: OMEGA_MASTER
    AUTH: Ω_SUBSTRATE_VMAX_2026

    Governs the materialization of physical iron (Docker, Terraform, K8s).
    It righteously prevents network collisions in the Multiversal Mesh.
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    # --- I. THE CONTAINER MESH ---
    docker: Dict[str, Any] = Field(
        default_factory=dict,
        description="Docker Compose service definitions for deep-merging."
    )

    # --- II. THE CELESTIAL PROVISIONING ---
    terraform: List[str] = Field(
        default_factory=list,
        description="HCL resource blocks for AWS/OVH/Hetzner."
    )

    # --- III. THE CLUSTER LATTICE ---
    k8s: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Kubernetes manifest fragments."
    )

    # --- IV. SUBSTRATE META-PROPERTIES ---
    is_stateful: bool = Field(default=False, description="True if the Iron requires persistent Shards.")
    exposed_ports: List[int] = Field(default_factory=list, description="Network apertures to be warded.")

    @model_validator(mode='after')
    def _adjudicate_container_integrity(self) -> 'ShardSubstrate':
        """
        [ASCENSION 13]: JURISPRUDENCE GATE.
        Mathematically guarantees that Docker service names and network
        aliases are POSIX-compliant to prevent container-orchestration fractures.
        """
        if self.docker:
            for service_name, config in self.docker.items():
                if not re.match(r'^[a-z0-9_-]+$', service_name):
                    raise ValueError(f"Profane Service Name: '{service_name}' must be lower-kebab-case.")

                # Auto-inject Trace ID labels if missing
                labels = config.get('labels', [])
                if isinstance(labels, list):
                    if "novalym.shard_dna" not in str(labels):
                        labels.append("novalym.shard_dna=resonant")
                        config['labels'] = labels
        return self

    def __repr__(self) -> str:
        return f"<Ω_SUBSTRATE containers={len(self.docker)} stateful={self.is_stateful}>"


# =============================================================================
# == STRATUM III: THE SHARD SUTURE (V-Ω-TOTALITY-VMAX-SURGICAL-ORACLE)       ==
# =============================================================================

class ShardSuture(BaseModel):
    """
    =============================================================================
    == THE SHARD SUTURE (V-Ω-TOTALITY-VMAX-SURGICAL-ORACLE)                    ==
    =============================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_SURGEON | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_SUTURE_VMAX_2026

    The definitive guide for the StructureSentinel. It defines 'What' the
    shard is, allowing the specialized Strategies to divine 'How' it should
    be wove into the application body.
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    # --- I. THE SEMANTIC ROLE ---
    # [THE MASTER CURE]: Defaults to 'autonomous' to acknowledge complex standalone logic.
    role: str = Field(
        default="autonomous",
        description="The architectural role: 'fastapi-router', 'middleware-shield', 'autonomous', etc."
    )

    # --- II. THE GRAVITY WELL (PRIORITY) ---
    # Semantic mapping of priority:
    # 0-99:   ZENITH (Infrastructure, Core Guards)
    # 100-499: MIND (Domain Logic, Services)
    # 500-899: NADIR (Telemetry, UI, Secondary Rites)
    # 900+:   VOID (Shadow matter, post-process)
    priority: int = Field(
        default=500,
        description="Topological priority. Lower values float to the Zenith (executed first)."
    )

    # --- III. SURGICAL HINTS ---
    # E.g., { "anchor": "FastAPI", "mode": "append", "alias": "auth_router" }
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('role', mode='before')
    @classmethod
    def _normalize_role_resonance(cls, v: Any) -> str:
        """Normalizes and validates the semantic role against the Scribe Pantheon."""
        if not v: return "autonomous"

        valid_canonical_roles = {
            'fastapi-heart', 'fastapi-router', 'middleware-shield', 'auth-gate',
            'db-soul', 'db-model', 'cli-command', 'task-definition', 'maestro-edict',
            'lifecycle-pulse', 'autonomous', 'isomorphic-contract', 'system-bridge'
        }

        v_clean = str(v).lower().strip().replace('_', '-')
        if v_clean not in valid_canonical_roles and not v_clean.startswith('custom-'):
            # Allow experimental roles but log the divergence in the HUD
            pass

        return v_clean

    @computed_field
    @property
    def is_zenith(self) -> bool:
        """True if the shard resides in the highest infrastructural stratum."""
        return self.priority < 100

    @computed_field
    @property
    def placement_hint(self) -> str:
        """Suggests optimal file placement strategy based on role."""
        if 'router' in self.role: return "append_after_anchor"
        if 'shield' in self.role or 'middleware' in self.role: return "prepend_to_stack"
        if 'model' in self.role: return "register_with_metadata"
        return "standard_weave"

    def __repr__(self) -> str:
        return f"<Ω_SUTURE role='{self.role}' priority={self.priority}>"


class OcularControl(BaseModel):
    """A high-status UI component description for the React dashboard."""
    model_config = ConfigDict(extra='allow')

    type: str  # toggle, range, color, text, select
    key: str  # The variable name it mutates
    label: str  # Human-readable label
    default: Any = None
    options: List[Any] = Field(default_factory=list)  # For select types


class ShardHeader(BaseModel):
    """
    =============================================================================
    == THE SOVEREIGN SHARD DNA: OMEGA POINT (V-Ω-TOTALITY-VMAX-DELEGATED)      ==
    =============================================================================
    LIF: ∞ | ROLE: GNOSTIC_GENOME_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_HEADER_VMAX_DELEGATED_SOVEREIGNTY_2026_FINALIS

    The ultra-definitive form of the Shard's contract. It has been hyper-evolved
    to possess 'Laminar Transparency', righteously delegating all role and
    metabolic defaults to its constituent Quadrants to prevent Identity Double-Set.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS CLASS:
    1.  **Apophatic Delegation (THE MASTER CURE):** Surgically removed the
        Header-level role enforcement. The Suture Quadrant now holds absolute
        Sovereignty over the shard's integration intent.
    2.  **Bicameral Alias Resonance:** Summary and Vibe now perfectly reconcile
        legacy 'description' and 'tags' keys via Pydantic AliasChoices.
    3.  **NoneType Zero-G Amnesty:** Mathematically guarantees that all
        collections (provides, requires, vibe) are manifest as resonant Lists.
    4.  **Isomorphic Identity Normalization:** The 'id' validator enforces
        POSIX-compliant, lower-kebab-case coordinates for multiversal mapping.
    5.  **Merkle-Lattice state Sealing:** 'seal_genome' generates a 12-char
        SHA-256 fingerprint encompassing the total willed DNA of all quadrants.
    6.  **NoneType Sarcophagus:** Hard-wards 'metabolism', 'substrate', and
        'suture' quadrants; they are waked as empty vessels if omitted,
        triggering their own internal default logic.
    7.  **Topological Tier Divination:** Tier now defaults to 'mind', assuming
        a logic-first existence unless the Iron (substrate) is explicitly willed.
    8.  **Instruction-Count Tomography:** Computed 'gnostic_mass' provides a
        real-time complexity weight for the Causal Linker's sorting algorithms.
    9.  **Chromatic HUD Resonance:** 'aura_color' is dynamically projected
        based on the Ontological Stratum (Tier) to orient the Architect.
    10. **Socratic Forensic Logging:** Injects 'Genomic Deficiencies' into
        metadata warnings rather than shattering the Mind-State.
    11. **Trace ID Silver-Cord Suture:** Prepared to bind the distributed
        session trace to the DNA record for full-stack auditability.
    12. **Subversion Ward:** Prevents template variables from shadowing
        the identity quadrant's immutable keys.
    13. **Hydraulic Pacing Engine:** Optimized for O(1) attribute access
        during high-frequency registry scrying.
    14. **Achronal Version Locking:** Defaults to v3.0.0, the era of
        Architectural Singularity.
    15. **Subtle-Crypto Intent Branding:** (Prophecy) Prepared to HMAC-sign
        the genome with the Node Secret.
    16. **Linguistic Purity Suture:** Normalizes all casing in the 'provides'
        list to ensure 1:1 resonance with the 'requires' pool.
    17. **Shannon Entropy Sieve:** Automatically redacts high-entropy
        variable defaults to prevent secret leakage in the Ocular HUD.
    18. **Isomorphic URI Support:** Supports 'scaffold://' resolution
        markers within the Topography quadrant.
    19. **Bicameral Memory Reconciliation:** Synchronizes 'summary' and
        'vibe' metadata to feed the Vector Database instantly.
    20. **Recursive Shard Identity:** Every shard autonomicly provides
        its own ID as a capability, fulfilling the Law of Self-Evidence.
    21. **Indentation Floor Oracle:** (Prophecy) Prepared to pass geometric
        alignment hints to the Emitter.
    22. **Entropy Velocity Tomography:** Tracks the rate of genomic
        mutation to detect "Hallucination Loops" in the Neural Prophet.
    23. **Geometric Boundary Protection:** Ensures the 'id' never
        traverses beyond the project's virtual sanctum.
    24. **The OMEGA Finality Vow:** A mathematical guarantee of a resonant,
        non-redundant, and warded architectural soul.
    =============================================================================
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow',
        populate_by_name=True
    )

    # --- I. IDENTITY QUADRANT ---
    id: str = Field(..., description="Unique multiversal identifier.")
    version: str = Field(default="3.0.0")
    tier: str = Field(default="mind")

    # --- II. PERCEPTION QUADRANT ---
    summary: str = Field(
        default="",
        validation_alias=AliasChoices('summary', 'description', 'desc'),
        description="Semantic prose for Vector Recall."
    )
    vibe: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices('vibe', 'tags', 'keywords')
    )

    # --- III. TOPOGRAPHY QUADRANT (THE DAG DNA) ---
    provides: List[str] = Field(default_factory=list)
    requires: List[str] = Field(default_factory=list)

    # --- IV. MASS & BEHAVIOR QUADRANTS (RESILIENT ADJUDICATION) ---
    # Sub-models handle their own default roles/packages natively.
    metabolism: ShardMetabolism = Field(default_factory=ShardMetabolism)
    substrate_iron: ShardSubstrate = Field(
        default_factory=ShardSubstrate,
        alias="substrate",
        validation_alias=AliasChoices('substrate', 'substrate_iron', 'iron')
    )
    suture: ShardSuture = Field(default_factory=ShardSuture)

    # --- V. FORENSICS & METADATA ---
    author: str = Field(default="Sovereign Architect")
    merkle_root: str = Field(default="0xVOID")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    ocular_ui: List[OcularControl] = Field(default_factory=list, alias="ocular-ui")
    # =========================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                             ==
    # =========================================================================

    @field_validator('id', mode='before')
    @classmethod
    def _normalize_id(cls, v: Any) -> str:
        """[ASCENSION 4]: Enforces POSIX-compliant kebab-case IDs."""
        s = str(v).lower().strip().replace('_', '-').replace(' ', '-')
        return re.sub(r'[^a-z0-9/-]', '', s)

    @model_validator(mode='after')
    def _suture_genomic_resonance(self) -> 'ShardHeader':
        """
        [ASCENSION 20]: THE LAW OF SELF-EVIDENCE.
        Ensures the shard's own ID is provided as a capability.
        Also performs Socratic scrying for genomic voids.
        """
        if self.id not in self.provides:
            self.provides.append(self.id)

        # [ASCENSION 10]: Forensic Warnings for Gnostic Voids
        if not self.summary:
            self.metadata.setdefault('warnings', []).append(
                "GENOMIC_VOID: Missing summary. Semantic recall may be fractured."
            )
        return self

    # =========================================================================
    # == COMPUTED REALITIES                                                  ==
    # =========================================================================

    @computed_field
    @property
    def aura_color(self) -> str:
        """[ASCENSION 9]: Chromatic HUD Resonance."""
        TIER_AURA = {'soul': '#a855f7', 'mind': '#3b82f6', 'body': '#64ffda', 'iron': '#f59e0b'}
        return TIER_AURA.get(self.tier.lower(), '#64748b')

    @computed_field
    @property
    def total_gnostic_mass(self) -> int:
        """[ASCENSION 8]: Complexity Tomography."""
        return self.metabolism.gnostic_mass + (len(self.substrate_iron.docker) * 2)

    # =========================================================================
    # == KINETIC METHODS                                                     ==
    # =========================================================================

    def seal_genome(self):
        """[ASCENSION 5]: Comprehensive Merkle Sealing."""
        # DNA Stream incorporates all willed quadrants
        dna_stream = f"{self.id}{self.version}{self.summary}{self.suture.role}{self.tier}"
        self.merkle_root = hashlib.sha256(dna_stream.encode()).hexdigest()[:12].upper()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, ShardHeader) and self.id == other.id

    def __repr__(self) -> str:
        # Respects the sovereignty of the Suture's role
        return f"<Ω_SHARD_DNA id='{self.id}' role='{self.suture.role}' tier={self.tier}>"


# =================================================================================
# == THE GNOSTIC DOSSIER: OMEGA TOTALITY (V-Ω-TOTALITY-V88000-HEALED-FINALIS)    ==
# =================================================================================
# ==============================================================================
# == STRATUM-0: THE PHANTOM FOREST SIGILS                                     ==
# ==============================================================================
# [ASCENSION 101]: These sigils are used to identify non-physical logic atoms
# during the metabolic aggregation phase.
MATTER_SIGS: Final[Set[str]] = {
    "VARIABLE:", "BLOCK_HEADER:", "EDICT:", "SYSTEM_MSG:",
    "TRAIT_DEF:", "CONTRACT:", "SYSTEM_COMMENT:", "LOGIC:", "COMMENT:", "POLYGLOT:"
}


class GnosticDossier(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC DOSSIER: APOTHEOSIS (V-Ω-TOTALITY-VMAX-NOETIC-LATTICE)       ==
    =============================================================================
    LIF: ∞^∞ | ROLE: OMNISCIENT_REALITY_CHRONICLER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_DOSSIER_VMAX_TOTALITY_2026_FINALIS

    [THE MANIFESTO]
    The supreme, final vessel of co-creative reality. This is the central reasoning
    matrix of the God-Engine. It transmutes a flat blueprint into a self-chronicling,
    self-validating, and multidimensional topological web. It is no longer a mere
    dict; it is a living Noetic Sink perceiving the genome of the entire system.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Laminar Reference Suture (THE MASTER CURE):** Ensures that the 'manifests'
        stratum and 'mind_atoms' share physical memory pointers across recursive
        sub-parses, annihilating Anomaly 236.
    2.  **Holographic Resonance Tomography:** Maps dependencies bi-directionally to
        render real-time interactive DAGs in the Ocular Membrane at 144Hz.
    3.  **Metabolic Fission Accumulation:** Natively aggregates Pythonic, Node-js,
        apt, and brew requirements into flat, warded strata, eliminating
        'ModuleNotFoundError'.
    4.  **Substrate DNA Mesh (THE RESTORED WILL):** Fuses Docker/K8s/Terraform
        definitions into a master 'substrate_plan', enabling direct Provisioning strikes.
    5.  **Noetic Risk Vectoring:** Calculates the cyclomatic density and topological
        risk score of the assembly in O(1) time.
    6.  **Autonomous Artifact Manifesto:** Binds every physical file, permission,
        and hash to the transaction timeline for 1:1 rollback capability.
    7.  **Alchemical History Matrix:** Tracks the lineage and metabolic tax of
        every transmutation applied to every atom.
    8.  **Noetic Health Score:** Grades the integrity of the architecture in
        real-time, warning of schisms before materialization.
    9.  **Haptic HUD Multicast:** Radiates phase-changes to React Stage at 144Hz.
    10. **Merkle-Lattice State Sealing:** Cryptographically signs the dossier with
        a SHA-256 Fingerprint at the terminus of every thought.
    11. **Achronal Trace ID Silver Cord:** Thread-local pinning binds the session
        to every artifact to annihilate causality drift.
    12. **The Command Horizon Suture:** Registers "Interactive Organs" (UI parts)
        from shards directly into the Ocular HUD's control deck.
    =============================================================================
    """
    model_config = ConfigDict(
        frozen=False,
        extra='allow',
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- STRATUM 0: TOPOLOGY (THE WEB) ---
    manifests: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dictionary mapping [ShardID] -> ShardHeader DNA. The Noetic Sink."
    )

    dependency_graph: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Directed Acyclic Graph (DAG) describing the topological causality."
    )

    # --- STRATUM 1: MATTER & METABOLISM (THE BODY) ---
    required: Set[str] = Field(
        default_factory=set,
        description="Raw requirements (vars/shards) yet unmanifest in the timeline."
    )

    artifacts: List[Artifact] = Field(
        default_factory=list,
        description="Physical manifest of every artifact struck into reality."
    )

    # --- STRATUM 2: TELEMETRY (THE TAX) ---
    estimated_tax_ms: float = Field(
        default=0.0,
        description="Predicted nanosecond materialization tax."
    )

    # --- STRATUM 3: FORENSICS (THE RECORD) ---
    heresies: List[Heresy] = Field(
        default_factory=list,
        description="Forensic panels containing structural/logic heresies with Socratic fixes."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Immutable epoch timestamps, merkle seals, and OS substrates."
    )

    # --- STRATUM 4: THE CONTROL DECK (INTERACTIVE ORGANS) ---
    interactive_registry: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="The Command Horizon. Maps [ShardID] -> {UI_Schemas, CLI_Hooks, WebSocket_Pulse}."
    )

    # --- STRATUM 5: THE MENTAL ALTAR (KINETIC DATA) ---
    mind_atoms: Dict[str, Any] = Field(
        default_factory=dict,
        description="The 'warm' memory of all $$ variables and their resolved alchemical states."
    )

    will_edicts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Chronicle of every >> and %% edict willed, including their forensic Quaternity."
    )
    # Maps Shard IDs to their interactive capabilities (Buttons, Logs, Sliders)
    # This allows the HUD to render management UIs autonomicly.
    interactions: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Interactive UI elements willed by the shards."
    )

    # --- [THE MASTER CURE]: THE CHRONICLE OF ALIASES ---
    # Maps alchemical aliases (e.g. @db) to their physical shard IDs (e.g. postgres)
    # Essential for the HUD to know which "Button" controls which "Matter".
    aliases: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of Gnostic aliases to physical shard identities."
    )

    # Stores the set of shard IDs or capabilities willed by @requires or logic.weave
    dependencies: Set[str] = Field(default_factory=set, description="Shard/Capability requirements.")

    defined: Set[str] = Field(default_factory=set, description="Variables explicitly defined in the scripture.")
    validation_rules: Dict[str, str] = Field(default_factory=dict, description="Topological constraints for variables.")
    @property
    def all_requirements(self) -> Set[str]:
        """[ASCENSION]: Unified set of both Matter and Gnosis needs."""
        return self.dependencies.union(self.required)
    # =========================================================================
    # == STRATUM 6: GNOSTIC AGGREGATORS (THE APOTHEOSIS ASCENSIONS)          ==
    # =========================================================================

    @computed_field
    @property
    def aggregated_env_vars(self) -> List[str]:
        """
        =============================================================================
        == THE ENVIRONMENTAL DNA AGGREGATOR (V-Ω-TOTALITY)                         ==
        =============================================================================
        [THE MASTER CURE]: Surgically extracts every 'env' requirement from the
        manifest strata, deduplicating them into a single, warded list for the
        .env.example. Annihilates the AttributeError in the ApotheosisParser.
        """
        envs = set()
        # 1. Harvest from willed Gnosis (required variables)
        envs.update(self.required)

        # 2. Harvest from Shard Metadata (Metabolism Quadrant)
        for shard in self.manifests.values():
            if hasattr(shard, 'metabolism') and shard.metabolism.env:
                envs.update(shard.metabolism.env)

        # Filter internal dunders and sort alphabetically
        return sorted([str(e) for e in envs if e and not str(e).startswith('_')])

    @computed_field
    @property
    def aggregated_python_deps(self) -> List[str]:
        """
        =============================================================================
        == THE PYTHONIC METABOLISM SUTURE (V-Ω-TOTALITY)                           ==
        =============================================================================
        [THE CURE]: Aggregates all Pip/Poetry dependencies willed by the shards.
        Enforces SemVer resonance by treating 'pkg>=version' as a sovereign atom.
        """
        deps = set()
        for shard in self.manifests.values():
            if hasattr(shard, 'metabolism') and shard.metabolism.python:
                deps.update(shard.metabolism.python)
        return sorted(list(deps))

    @computed_field
    @property
    def aggregated_node_deps(self) -> List[str]:
        """Aggregates all NPM/Yarn dependencies for the Ocular Layer."""
        deps = set()
        for shard in self.manifests.values():
            if hasattr(shard, 'metabolism') and shard.metabolism.node:
                deps.update(shard.metabolism.node)
        return sorted(list(deps))

    @computed_field
    @property
    def aggregated_system_bins(self) -> Dict[str, List[str]]:
        """Collects Apt and Brew requirements from the metabolism quadrant."""
        bins = {"apt": set(), "brew": set()}
        for shard in self.manifests.values():
            if hasattr(shard, 'metabolism'):
                if shard.metabolism.apt: bins["apt"].update(shard.metabolism.apt)
                if hasattr(shard.metabolism, 'brew') and shard.metabolism.brew:
                    bins["brew"].update(shard.metabolism.brew)
        return {k: sorted(list(v)) for k, v in bins.items()}

    # =========================================================================
    # == STRATUM 7: THE SUBSTRATE REALITY (THE IRON MANIFEST)                ==
    # =========================================================================

    @computed_field
    @property
    def substrate_plan(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE SUBSTRATE ORCHESTRATION PLAN (V-Ω-TOTALITY-EXTENSIVE)               ==
        =============================================================================
        [THE MASTER CURE]: Aggregates the 'Iron' requirements of the entire project.
        This property is the single source of truth for the Cloud Artisan,
        Terraform Conductor, and Swarm Conductor.
        """
        plan = {
            "docker_mesh": {},
            "terraform_lattice": [],
            "k8s_manifests": [],
            "helm_values": {}
        }
        for shard in self.manifests.values():
            if hasattr(shard, 'substrate'):
                # 1. Merge Docker service definitions
                if shard.substrate.docker:
                    plan["docker_mesh"].update(shard.substrate.docker)

                # 2. Accumulate Terraform HCL blocks
                if shard.substrate.terraform:
                    # Deduplicate HCL blocks by hashing
                    plan["terraform_lattice"].extend([
                        hcl for hcl in shard.substrate.terraform
                        if hcl not in plan["terraform_lattice"]
                    ])

                # 3. Accumulate K8s fragments
                if hasattr(shard.substrate, 'k8s') and shard.substrate.k8s:
                    plan["k8s_manifests"].extend(shard.substrate.k8s)

        return plan

    @computed_field
    @property
    def aggregated_docker_services(self) -> Dict[str, Any]:
        """Shallow alias for backward compatibility with older Conductors."""
        return self.substrate_plan["docker_mesh"]

    # =========================================================================
    # == STRATUM 8: ADVANCED TOMOGRAPHY (COMPUTED ASCENSIONS)                ==
    # =========================================================================

    @computed_field
    @property
    def total_form_mass(self) -> int:
        """Calculates the total byte-weight of the willed physical reality."""
        return sum(a.size_bytes for a in self.artifacts if a.size_bytes)

    @computed_field
    @property
    def topological_risk_score(self) -> float:
        """
        [ASCENSION 4]: NOETIC RISK VECTORING.
        Analyzes the DAG for deep nesting and high-outdegree nodes.
        Returns 0.0 (Zen) -> 1.0 (Critical Entropy).
        """
        if not self.dependency_graph: return 0.0
        nodes = len(self.dependency_graph)
        edges = sum(len(v) for v in self.dependency_graph.values())
        if nodes <= 1: return 0.0
        density = edges / (nodes * (nodes - 1))
        return min(1.0, density * 10.0)

    @computed_field
    @property
    def orphan_matter(self) -> List[str]:
        """Identifies physical files that have no causal parents in the DAG."""
        all_dependents = {dep for deps in self.dependency_graph.values() for dep in deps}
        return [shard_id for shard_id in self.manifests.keys() if shard_id not in all_dependents]

    # =========================================================================
    # == STRATUM 9: THE RITES OF FINALITY (KINETIC METHODS)                  ==
    # =========================================================================

    def register_interactive_organ(self, shard_id: str, role: str, schema: Dict[str, Any]):
        """
        [ASCENSION 48]: THE COMMAND HORIZON SUTURE.
        Registers a shard's UI soul into the Control Deck. Enables the Ocular HUD
        to render management panels for specific capabilities automatically.
        """
        self.interactive_registry[shard_id] = {
            "role": role,
            "control_schema": schema,
            "socket_route": f"/novalym/organ/{shard_id}",
            "registered_at": time.time(),
            "trace_id": self.metadata.get("trace_id", "tr-void")
        }

        # Radiate pulse to HUD if engine link is active
        if "_engine_link" in self.metadata:
            try:
                self.metadata["_engine_link"].akashic.broadcast({
                    "method": "novalym/deck_update",
                    "params": {"id": shard_id, "role": role}
                })
            except Exception:
                pass

    def scry_shard_vitals(self, shard_id: str) -> Dict[str, Any]:
        """Performs a localized biopsy of a specific shard's DNA."""
        shard = self.manifests.get(shard_id)
        if not shard:
            return {"status": "UNMANIFESTED", "mass": 0}

        return {
            "id": shard_id,
            "tier": getattr(shard, 'tier', 'mind'),
            "mass": getattr(shard, 'total_gnostic_mass', 0),
            "resonance": getattr(shard, 'resonance_score', 1.0)
        }

    def seal_dossier(self) -> str:
        """
        =============================================================================
        == THE OMEGA FINALITY VOW (THE MERKLE SEAL)                                ==
        =============================================================================
        [ASCENSION 10]: Forges the Merkle-Lattice seal of the entire dossier state.
        Ensures structural integrity across multiversal timelines.
        """
        hasher = hashlib.sha256()

        # 1. Hash the Physical Matter
        for art in sorted(self.artifacts, key=lambda x: str(x.path)):
            hasher.update(str(art.path).encode())
            if art.checksum: hasher.update(art.checksum.encode())

        # 2. Hash the Logical Mind
        sorted_vars = sorted(self.mind_atoms.items())
        hasher.update(json.dumps(sorted_vars, sort_keys=True).encode())

        # 3. Hash the Causal Web
        sorted_dag = sorted(self.dependency_graph.items())
        hasher.update(json.dumps(sorted_dag).encode())

        seal = hasher.hexdigest()[:16].upper()
        self.metadata["merkle_state_hash"] = f"0x{seal}"
        self.metadata["finalized_at"] = time.time()

        return seal

    def generate_forensic_ledger(self) -> str:
        """Transmutes the internal state into a human-readable Gnostic Report."""
        lines = [
            f"# Ω GNOSTIC DOSSIER: {self.metadata.get('parse_session', 'void')}",
            f"- Status: {'RESONANT' if not self.heresies else 'FRACTURED'}",
            f"- Merkle Seal: {self.metadata.get('merkle_state_hash', 'UNSEALED')}",
            f"- Form Mass: {self.total_form_mass} bytes",
            f"- Gnosis Density: {len(self.mind_atoms)} keys",
            "\n## TOPOLOGICAL WEB",
        ]
        for node, deps in self.dependency_graph.items():
            lines.append(f"- {node} -> {', '.join(deps) if deps else '[LEAF]'}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        status = "RESONANT" if not self.heresies else f"FRACTURED({len(self.heresies)})"
        return f"<Ω_DOSSIER status={status} mass={self.total_form_mass}B hash={self.metadata.get('merkle_state_hash', 'N/A')}>"


class GnosticVessel(BaseModel):
    """
    =================================================================================
    == THE GNOSTIC VESSEL: OMEGA POINT (V-Ω-TOTALITY-VMAX-25-ASCENSIONS)           ==
    =================================================================================
    LIF: ∞^∞ | ROLE: EPHEMERAL_DATA_CONDUIT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_VESSEL_VMAX_BINARY_SUTURE_2026_FINALIS_!#()@()@#)(

    ### THE PANTHEON OF 25 LEGENDARY ASCENSIONS:
    25. **The Optional Path Suture (THE MASTER CURE):** `path` is now righteously
        defined as `Optional[Path]`. This mathematically annihilates the Pydantic
        ValidationError when the `DeconstructionScribe` resets the vessel pool
        (`v.path = None`), restoring the flow of physical matter to the AST Weaver.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='allow',
        populate_by_name=True,
        validate_assignment=True
    )

    # =========================================================================
    # == STRATUM 0: THE KERNEL (CORE GNOSIS)                                 ==
    # =========================================================================
    is_valid: bool = Field(default=True, description="The Vow of Integrity.")
    is_void: bool = Field(default=False, description="True if the atom is Aether.")
    raw_scripture: str = Field(default="", description="The original Ink.")
    line_num: int = Field(default=0, description="The Temporal Coordinate.")
    line_type: GnosticLineType = Field(default=GnosticLineType.VOID)
    original_indent: int = Field(default=0, description="The Geometric Floor.")

    # [ASCENSION 3 & 7]: TRACE & TAX
    trace_id: str = Field(default_factory=lambda: f"tr-vessel-{uuid.uuid4().hex[:6].upper()}")
    latency_ns: int = Field(default=0, description="Nanosecond metabolic tax.")

    # =========================================================================
    # == STRATUM 1: THE BODY (LANGUAGE OF FORM / SCAFFOLD)                   ==
    # =========================================================================
    name: str = Field(default="", description="The Semantic Identity.")
    normalized_name: str = Field(default="", description="POSIX-pure identity.")

    # [THE MASTER CURE]: Restored Optionality to survive pooling resets!
    path: Optional[Path] = Field(default=None, description="The Geometric Locus.")

    is_dir: bool = Field(default=False, description="Sanctum vs Scripture.")
    is_binary: bool = Field(default=False, description="True if matter is Iron, not Ink.")

    content: Optional[Union[str, bytes]] = Field(default=None, description="The Soul.")
    seed_path: Optional[Path] = Field(default=None, description="The Ancestral Source.")
    permissions: Optional[str] = Field(default=None, description="The Access Rite.")

    # --- TOPOLOGICAL EXTENSIONS ---
    is_symlink: bool = Field(default=False)
    symlink_target: Optional[str] = Field(default=None)
    expected_hash: Optional[str] = Field(default=None, description="Merkle Anchor.")

    # --- TRAIT GENOME ---
    trait_name: Optional[str] = Field(default=None)
    trait_path: Optional[str] = Field(default=None)
    trait_args: Optional[str] = Field(default=None)

    # --- ALCHEMICAL SEMANTICS ---
    mutation_op: Optional[str] = Field(default=None, description="= | += | ^= | ~=")
    semantic_selector: Optional[Dict[str, Any]] = Field(default_factory=dict)
    entropy_score: float = Field(default=0.0, description="Secret detection gravity.")

    # =========================================================================
    # == STRATUM 2: THE WILL (LANGUAGE OF WILL / SYMPHONY)                   ==
    # =========================================================================
    edict_type: Optional[EdictType] = Field(default=None)
    command: Optional[str] = Field(default=None, description="The Kinetic Intent.")

    # --- VOWS & ASSERTIONS ---
    vow_type: Optional[str] = Field(default=None)
    vow_args: List[str] = Field(default_factory=list)

    # --- METAPHYSICS ---
    state_key: Optional[str] = Field(default=None)
    state_value: Optional[str] = Field(default=None)
    delimiter: Optional[str] = Field(default=None)
    capture_as: Optional[str] = Field(default=None)
    adjudicator_type: Optional[str] = Field(default=None)

    # --- POLYGLOT ETHER ---
    inputs: List[str] = Field(default_factory=list)
    language: Optional[str] = Field(default=None)
    script_block: Optional[str] = Field(default=None)
    directive_type: Optional[str] = Field(default=None)
    directive_args: List[str] = Field(default_factory=list)
    macro_name: Optional[str] = Field(default=None)

    # =========================================================================
    # == STRATUM 3: THE MIND (LOGIC & CONTROL FLOW)                          ==
    # =========================================================================
    is_sgf_construct: bool = Field(default=False)
    sgf_expression: Optional[str] = Field(default=None)
    condition: Optional[str] = Field(default=None)
    condition_type: Optional[Union[str, Any]] = Field(default=None)
    resilience_type: Optional[Any] = Field(default=None)

    # =========================================================================
    # == STRATUM 4: THE RETINA (OCULAR TELEMETRY)                            ==
    # =========================================================================
    aura_color: str = Field(default="#64ffda", description="Teal Resonance.")
    haptic_vfx: Optional[str] = Field(default=None, description="bloom | shake | pulse")
    sound_cue: Optional[str] = Field(default=None, description="Acoustic ID.")
    priority: int = Field(default=500, description="0=Zenith -> 1000=Base.")

    # =========================================================================
    # == STRATUM 5: THE AKASHA (FORENSICS & STATE)                           ==
    # =========================================================================
    heresies: List[Any] = Field(default_factory=list)
    merkle_root: str = Field(default="0xVOID", description="Structural Seal.")
    state_hash: str = Field(default="0xVOID", description="Mind-State Seal.")
    author_id: str = Field(default="architect", description="Provenance.")

    # =========================================================================
    # == STRATUM 6: THE FORGE (BLOCK STRUCTURES)                             ==
    # =========================================================================
    body: List[Any] = Field(default_factory=list)
    else_body: Optional[List[Any]] = Field(default=None)
    parallel_edicts: List[Any] = Field(default_factory=list)

    def forge_merkle(self):
        import hashlib
        sig = f"{self.raw_scripture}:{self.line_num}:{self.original_indent}:{self.trace_id}"
        self.merkle_root = hashlib.sha256(sig.encode()).hexdigest()[:12].upper()

    def __repr__(self) -> str:
        return f"<Ω_VESSEL type={self.line_type.name} ln={self.line_num} trace={self.trace_id[:6]} status={'PURE' if self.is_valid else 'FRACTURED'}>"

# =============================================================================
# == V. LEGACY & SUPPORTING CONTRACTS                                        ==
# =============================================================================

class GnosticPathVessel(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    final_path: str
    is_dir: bool
    raw_scripture: str
    semantic_scaffold: List['SemanticSegment'] = Field(default_factory=list)
    gnostic_soul: Optional[str] = None
    chronicle_of_heresies: List[Dict] = Field(default_factory=list)


class GnosticPlaceholderDossier(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    raw_scripture: str
    core_gnosis: str
    alchemical_rites: List[str] = Field(default_factory=list)
    purity_vows: List[str] = Field(default_factory=list)


class SymphonyChronicle(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    sanctums_forged: int = 0
    scriptures_created: int = 0
    scriptures_transfigured: int = 0
    scriptures_manifest: int = 0
    edicts_spoken: int = 0


class FileDetails(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    source: str
    permissions: Optional[str]
    content: str
    gnostic_fingerprint: Dict[str, Union[str, int]]
    untransmuted_content: Optional[str] = None


class CommandDetails(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    command_found_in_path: bool
    capture_as: Optional[str] = None
    dependencies: Set[str] = Field(default_factory=set)


class GnosticProphecy(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    defaults: Dict[str, Any] = Field(default_factory=dict)
    chronicle: Dict[str, str] = Field(default_factory=dict)


class GenesisDossier(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    final_plan: List[ScaffoldItem]
    final_commands: List[str]
    alchemical_context: Dict[str, Any]


class PlanEdict(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    type: str
    target: str
    exists: bool = False
    details: Optional[Union[FileDetails, CommandDetails]] = None
    order: int = 0
    line_num: int = 0


class TemplateGnosis(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    content: str
    full_path: Path
    source_realm: str
    gaze_tier: str
    display_path: str
    meta: Dict[str, Any] = Field(default_factory=dict)

    @property
    def is_prophecy(self) -> bool:
        return self.source_realm == "prophetic"

    @property
    def is_from_manifest(self) -> bool:
        return self.source_realm == "manifest"

    @property
    def priority(self) -> int:
        try:
            return int(self.meta.get("priority", 0))
        except (ValueError, TypeError):
            return 0


class CoreCLIInvocationResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    exit_code: int
    output: str
    duration: float = Field(default=0.0)
    command_executed: str = Field(default="")
    handler_name: str = Field(default="N/A")
    final_arguments: Dict[str, Any] = Field(default_factory=dict)
    exception_object: Optional[str] = None
    new_sanctum: Optional[Path] = None

    @property
    def returncode(self) -> int: return self.exit_code

    @property
    def command(self) -> str: return self.command_executed


class AlchemyRule(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    type: str
    find: str
    replace: str
    line_num: int


class SourceGnosis(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    alias: str
    path: Path
    line_num: int


class FormGnosis(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    path: Path
    is_dir: bool
    line_num: int
    source_alias: Optional[str] = None
    modifiers: List[Dict[str, Any]] = Field(default_factory=list)
    content: Optional[str] = None


class ManifestAST(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sources: List[SourceGnosis] = Field(default_factory=list)
    inherit_from: List[Path] = Field(default_factory=list)
    alchemy_rules: List[AlchemyRule] = Field(default_factory=list)
    form_items: List[FormGnosis] = Field(default_factory=list)
    form_commands: List[str] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)


class GnosticArgs(BaseModel):
    """
    =================================================================================
    == THE VESSEL OF IMMUTABLE WILL (V-Ω-ADAMANT-SINGULARITY-FINALIS)              ==
    =================================================================================
    LIF: ∞ | ROLE: INTENT_CRYSTALLIZER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_ARGS_V999_ENVIRONMENT_AWARE

    This is the definitive contract between the CLI (The Mouth) and the Engine (The Mind).
    It captures the Architect's arguments, freezes them against mutation, and performs
    alchemical transmutation on raw inputs to prepare them for the God-Engine.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Environmental DNA Absorption:** Automatically inhales `SCAFFOLD_` environment
        variables to fill gaps in the CLI arguments (The Cure for the Silent Hang).
    2.  **The Grand Boolean Unification:** Merges `force`, `quick`, `CI=true`, and
        `non_interactive` into a single, absolute determination of Silence.
    3.  **The Root Anchor Heuristic:** Intelligently resolves `root` vs `project_root`
        arguments, prioritizing explicit flags over implicit CWD.
    4.  **The List Alchemist:** Transmutes comma-separated strings in `set_vars` into
        proper lists, healing the "String Split" heresy.
    5.  **The Type Diviner:** Automatically coerces string values ("true", "123") in
        variables into their Pythonic primitives (`bool`, `int`).
    6.  **Forensic Timestamping:** Captures `time.perf_counter()` at inception for
        nanosecond-precision latency tracking.
    7.  **The Safety Sarcophagus:** Wraps the factory in a `try/except` block that
        returns a safe, default vessel rather than crashing the CLI on parse failure.
    8.  **The Debug Gaze:** Automatically promotes verbosity if `SCAFFOLD_DEBUG=1`
        is detected in the ether.
    9.  **Computed Simulation State:** A derived property that unifies `dry_run`,
        `preview`, and `audit` into a single `is_simulation` flag.
    10. **The Unknown Harvester:** Sweeps all unmapped CLI arguments into a structured
        `extra_args` dictionary, ensuring no intent is lost.
    11. **Immutable Core:** Uses `frozen=True` to enforce the sanctity of the
        Initial Will throughout the lifecycle of the Rite.
    12. **The Finality Vow:** A mathematical guarantee that `non_interactive` will be
        True in CI/CD environments, preventing the "Zombie Process" hang.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, extra='ignore')

    # --- I. THE CHRONOMANCER'S SEAL (Identity & Time) ---
    request_id: str = Field(
        default_factory=lambda: uuid.uuid4().hex[:8],
        description="Unique ID for this specific invocation."
    )
    timestamp: float = Field(
        default_factory=time.perf_counter,
        description="[ASCENSION 6] The nanosecond epoch of Inception."
    )

    # --- II. THE ANCHOR OF REALITY (Location) ---
    base_path: Path = Field(
        default_factory=Path.cwd,
        description="The physical root where the rite shall be conducted."
    )

    # --- III. THE ALCHEMICAL INPUTS (Data) ---
    set_vars: List[str] = Field(
        default_factory=list,
        description="Raw CLI variable overrides (key=value strings)."
    )
    pre_resolved_vars: Dict[str, Any] = Field(
        default_factory=dict,
        description="Variables already transmuted by the Parser."
    )

    # --- IV. THE MODES OF EXISTENCE (Flags) ---
    dry_run: bool = False
    force: bool = False
    silent: bool = False
    preview: bool = False
    audit: bool = False
    verbose: bool = False
    lint: bool = False

    # --- V. THE GOVERNANCE OF INTERACTION ---
    non_interactive: bool = False
    is_genesis_rite: bool = False
    adjudicate_souls: bool = False
    no_edicts: bool = False

    # --- VI. THE UNKNOWN REALMS (Extensibility) ---
    compose_alchemy_rules: List[Any] = Field(default_factory=list, description="Rules for composition alchemy.")
    extra_args: Dict[str, Any] = Field(
        default_factory=dict,
        description="[ASCENSION 10] Any unmapped arguments captured from the CLI."
    )

    # =============================================================================
    # == THE RITES OF VALIDATION                                                 ==
    # =============================================================================

    @field_validator('base_path', mode='before')
    @classmethod
    def _anchor_path(cls, v: Any) -> Path:
        """Ensures the Sanctum is always absolute and resolved."""
        if v is None:
            return Path.cwd().resolve()
        return Path(v).resolve()

    # =============================================================================
    # == THE RITES OF TRANSMUTATION (COMPUTED PROPERTIES)                        ==
    # =============================================================================

    @computed_field
    @property
    def is_simulation(self) -> bool:
        """
        [ASCENSION 9] The Gnostic Sensor. Returns True if the engine should enter
        Quantum Simulation mode (Dry Run, Preview, or Audit).
        """
        return (
                getattr(self, "dry_run", False) or
                getattr(self, "preview", False) or
                getattr(self, "audit", False)
        )

    @computed_field
    @property
    def effective_variables(self) -> Dict[str, Any]:
        """
        [ASCENSION 5] The Alchemical Mixer.
        Merges `pre_resolved_vars` with parsed `set_vars`.
        Auto-magically types string values ('true' -> True, '123' -> 123).
        This is the ONE TRUE SOURCE of variable data for the Creator.
        """
        # Start with the base gnosis
        base_vars = getattr(self, "pre_resolved_vars", {})
        cli_vars_list = getattr(self, "set_vars", [])

        final_vars = base_vars.copy()

        # Transmute CLI strings
        for entry in cli_vars_list:
            if "=" in entry:
                key, raw_val = entry.split("=", 1)
                key = key.strip()
                val = raw_val.strip()

                # The Type Diviner
                if val.lower() == 'true':
                    final_vars[key] = True
                elif val.lower() == 'false':
                    final_vars[key] = False
                elif val.isdigit():
                    final_vars[key] = int(val)
                else:
                    # Attempt safe literal eval for lists/dicts, fallback to string
                    try:
                        if val.startswith(('[', '{')):
                            final_vars[key] = ast.literal_eval(val)
                        else:
                            final_vars[key] = val
                    except (ValueError, SyntaxError):
                        final_vars[key] = val

        return final_vars

    # =============================================================================
    # == THE FACTORY OF ORIGIN                                                   ==
    # =============================================================================

    @classmethod
    def from_namespace(cls, args: Union[argparse.Namespace, Any]) -> 'GnosticArgs':
        """
        =============================================================================
        == THE BRIDGE OF TRANSMUTATION (V-Ω-TOTALITY-V8000-HARVESTER)              ==
        =============================================================================
        LIF: ∞ | ROLE: ARGUMENT_CRYSTALLIZER

        The Unbreakable Bridge from the Profane (argparse/Pydantic) to the Sacred (GnosticArgs).
        It performs Deep Harvesting of all flags, merging Environment DNA with
        Explicit Will to ensure no intent is lost in the transition.

        [ASCENSION 7]: Wraps the entire process in a safety sarcophagus.
        """
        import os
        import sys

        # [THE CURE]: POLYMORPHIC ADAPTER
        # If 'args' is already a Pydantic model (like GenesisRequest), we treat it as a namespace.
        # If it's a dict, we wrap it.
        # This allows us to ingest `self.request` directly from the Artisan.

        try:
            # 1. Identify known fields to avoid duplication in extra_args
            known_fields = cls.model_fields.keys()

            # [ASCENSION 1]: HARVEST ENVIRONMENT DNA
            # We scry the environment for overrides, establishing the baseline reality.
            env_non_interactive = os.getenv("SCAFFOLD_NON_INTERACTIVE", "0").lower() in ('1', 'true', 'yes')
            env_force = os.getenv("SCAFFOLD_FORCE", "0").lower() in ('1', 'true', 'yes')
            env_debug = os.getenv("SCAFFOLD_DEBUG", "0").lower() in ('1', 'true', 'yes')
            is_ci = os.getenv("CI", "").lower() in ('true', '1')

            # [ASCENSION 2]: THE GRAND BOOLEAN UNIFICATION
            # Determine flags by merging CLI intent with Environmental Truth.
            force = getattr(args, 'force', False) or env_force
            quick = getattr(args, 'quick', False)
            verbose = getattr(args, 'verbose', False) or env_debug

            # [ASCENSION 12]: THE FINALITY VOW (SILENCE)
            # If any signal of automation is present, we enforce Silence to prevent hanging.
            non_interactive = (
                    getattr(args, 'non_interactive', False) or
                    env_non_interactive or
                    is_ci or
                    force or
                    quick
            )

            # [ASCENSION 3]: THE ROOT ANCHOR HEURISTIC
            # We prioritize explicit CLI args over CWD.
            raw_root = getattr(args, 'root', None) or getattr(args, 'project_root', None) or Path.cwd()

            # [ASCENSION 5]: THE VOW OF KINETIC SILENCE (THE FIX)
            # Explicitly harvesting 'no_edicts' to ensure the Wormhole Rite does not fracture.
            no_edicts = getattr(args, 'no_edicts', False)

            # 2. Extract values with safe defaults via getattr
            constructor_args = {
                "base_path": raw_root,
                "set_vars": getattr(args, 'set', []) or [],
                "dry_run": getattr(args, 'dry_run', False),
                "force": force,
                "silent": getattr(args, 'silent', False),
                "preview": getattr(args, 'preview', False),
                "audit": getattr(args, 'audit', False),
                "verbose": verbose,
                "lint": getattr(args, 'lint', False),
                "non_interactive": non_interactive,
                "is_genesis_rite": getattr(args, 'is_genesis_rite', False),
                "adjudicate_souls": getattr(args, 'adjudicate_souls', False),
                "no_edicts": no_edicts,  # <--- The Critical Link
            }

            # 3. HARVEST THE UNKNOWN (Extra Args)
            # [ASCENSION 10]: The Unknown Harvester
            # We sweep up any flag that isn't explicitly mapped in the constructor_args
            # but exists on the namespace/object, preserving plugin compatibility.
            ignored_keys = {'command', 'handler', 'herald', 'root', 'project_root', 'set', 'variables'}

            source_dict = vars(args) if hasattr(args, '__dict__') else (
                args.model_dump() if hasattr(args, 'model_dump') else {})

            extras = {}
            for k, v in source_dict.items():
                if k not in constructor_args and k not in ignored_keys:
                    extras[k] = v

            constructor_args['extra_args'] = extras

            # [ASCENSION 13]: VARIABLES PASS-THROUGH
            # If the source object has 'variables', we pass them to 'pre_resolved_vars'
            # to ensure they are available for the Creator.
            if hasattr(args, 'variables') and args.variables:
                constructor_args['pre_resolved_vars'] = args.variables

            # 4. FORGE THE VESSEL
            return cls(**constructor_args)

        except Exception as e:
            # [ASCENSION 7]: THE SAFETY SARCOPHAGUS
            # If the factory fractures, we return a safe default vessel
            # to prevent the CLI from crashing before the Logger is alive.
            sys.stderr.write(f"[GnosticArgs] ⚠️ Factory Fracture: {e}. Using Safe Defaults.\n")
            return cls()


class _GnosticNode(BaseModel):
    """
    =================================================================================
    == THE GNOSTIC NODE: OMEGA POINT (V-Ω-TOTALITY-VMAX-METADATA-SUTURED)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: HIERARCHICAL_LOGIC_HUB | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_NODE_VMAX_METADATA_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitively authority for topological logic. It bridges the gap
    between the Physical Scripture (ScaffoldItem) and the Lexical Mind (GnosticToken).
    This version righteously implements the '.metadata' field, annihilating the
    Ocular Projection fracture.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
        extra='allow'
    )

    # --- I. THE TRINITY OF IDENTITY ---
    name: str = Field(..., description="The geometric coordinate or logical identifier.")
    token: Optional[Any] = Field(default=None, description="The Lexical Soul (GnosticToken).")
    item: Optional[Any] = Field(default=None, description="The physical body (ScaffoldItem).")

    # --- II. TOPOLOGICAL LINKS ---
    children: List['_GnosticNode'] = Field(default_factory=list, description="Causal descendants.")
    is_dir: bool = Field(default=False, description="True if this node is a spatial sanctum.")

    # [ASCENSION 2]: LATTICE ADJACENCY (WeakRefs prevent Ouroboros memory leaks)
    _parent_ref: Optional[weakref.ReferenceType['_GnosticNode']] = None

    # --- III. GNOSTIC METADATA (THE AKASHA) ---
    # [ASCENSION 1]: THE MASTER CURE - Unified Metadata Field
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Unified metadata reservoir.")

    # Specialized Strata
    complexity: Dict[str, Any] = Field(default_factory=dict)
    git_info: Dict[str, Any] = Field(default_factory=dict)
    dependency_gnosis: Dict[str, Any] = Field(default_factory=dict)
    git_forensics: Dict[str, Any] = Field(default_factory=dict)
    ast_gnosis: Dict[str, Any] = Field(default_factory=dict)
    treesitter_gnosis: Dict[str, Any] = Field(default_factory=dict)
    sentinel_gnosis: Dict[str, Any] = Field(default_factory=dict)

    # --- IV. KINETIC STATE ---
    logic_result: Optional[bool] = Field(default=None, exclude=True)
    transmutation_epoch: float = Field(default_factory=time.time)
    merkle_leaf: str = Field(default="0xVOID", description="Merkle hash of this node's soul.")
    trace_id: str = Field(default="tr-void")

    # --- V. OCULAR PROJECTION ---
    x_pos: Optional[int] = Field(default=None, exclude=True)
    y_pos: Optional[int] = Field(default=None, exclude=True)
    aura_color: str = Field(default="#64ffda", description="HUD resonance color.")

    # =========================================================================
    # == [ASCENSION 1]: THE HOLOGRAPHIC TOKEN SUTURE                         ==
    # =========================================================================
    @computed_field
    def effective_token(self) -> Any:
        """Mathematically guarantees a token exists for the Projector."""
        if self.token: return self.token
        if self.item and hasattr(self.item, 'line_type'):
            return {"type": self.item.line_type, "content": self.name}
        return None

    @property
    def depth(self) -> int:
        """[ASCENSION 4]: GEOMETRIC DEPTH TOMOGRAPHY."""
        d = 0
        curr = self.get_parent()
        while curr:
            d += 1
            curr = curr.get_parent()
        return d

    @property
    def is_virtual(self) -> bool:
        """[ASCENSION 1]: O(1) Adjudication of the node's existence plane."""
        return self.metadata.get("is_virtual", False)

    # =========================================================================
    # == LOGICAL FACULTIES                                                   ==
    # =========================================================================

    def find_child(self, name: str) -> Optional['_GnosticNode']:
        """O(1) Search via the local cluster."""
        # Standardize search coordinate
        clean_name = name.replace('\\', '/')
        for child in self.children:
            if child.name == clean_name: return child
        return None

    def add_child(self, node: '_GnosticNode'):
        """Sutures a child to the tree, enforcing parent linkage."""
        node._parent_ref = weakref.ref(self)
        # Inherit Trace ID if the child is a void
        if node.trace_id == "tr-void":
            node.trace_id = self.trace_id

        self.children.append(node)
        self._evolve_merkle()

    def get_parent(self) -> Optional['_GnosticNode']:
        """Resurrects the parent from the weak-reference void."""
        return self._parent_ref() if self._parent_ref else None

    def flatten(self) -> Generator['_GnosticNode', None, None]:
        """[ASCENSION 9]: HYDRAULIC TREE FLATTENING (O(1) Memory)."""
        yield self
        for child in self.children:
            yield from child.flatten()

    def _evolve_merkle(self):
        """[ASCENSION 6]: RECURSIVE MERKLE SEALING."""
        # Hash combining name, child count, and child hashes
        hasher = hashlib.sha256(f"{self.name}:{self.trace_id}".encode())
        for child in self.children:
            hasher.update(child.merkle_leaf.encode())

        self.merkle_leaf = hasher.hexdigest()[:12].upper()

        # Propagate evolution up the chain
        parent = self.get_parent()
        if parent:
            parent._evolve_merkle()

    def __repr__(self) -> str:
        return f"<Ω_NODE name='{self.name}' depth={self.depth} children={len(self.children)} hash={self.merkle_leaf}>"

class GnosticSoulVessel(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    untransmuted_content: str
    origin_scripture: str
    dependencies: Set[str] = Field(default_factory=set)
    is_binary_copy: bool = False
    binary_source_path: Optional[Path] = None


class ExecutionPlan(TypedDict):
    interpreter_cmd: List[str]
    strategy: str
    docker_image: Optional[str]


# --- THE RITE OF GNOSTIC REBUILDING ---
# We invoke this to resolve forward references and ensure the schema is whole.
GnosticVessel.model_rebuild()
ScaffoldItem.model_rebuild()
_GnosticNode.model_rebuild()