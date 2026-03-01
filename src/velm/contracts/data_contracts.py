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
import ast
import math
import os
import uuid
import time
import argparse
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Set, Dict, Union, List, Any, TypedDict
from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field, model_validator

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
    JINJA_CONSTRUCT = auto()  # {% ... %} (Logic)
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
    is_jinja_construct: bool = Field(default=False)
    jinja_expression: Optional[str] = Field(None)
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
    condition: str  # The Jinja2 expression, or 'else'
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


class GnosticDossier(BaseModel):
    """
    =================================================================================
    == THE GNOSTIC DOSSIER: OMEGA TOTALITY (V-Ω-TOTALITY-V20000-METRIC-RESONANT)   ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_MRI_LEDGER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_DOSSIER_V20000_COMPLEXITY_SUTURE_2026_FINALIS

    The supreme, high-fidelity record of project intelligence. It deconstructs the
    causal relationship between willed intent and physical matter, capturing the
    metabolic and cognitive tax of the materialization rite.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Complexity Suture (THE CURE):** Explicitly materializes the
        `cyclomatic_complexity` register in the metadata sanctuary, annihilating
        the 'Swarm Fracture' KeyError for all parallel timelines.
    2.  **Bicameral Memory Sieve:** Separates variables into `required`, `defined`,
        `derived`, and `missing` strata for absolute causal transparency.
    3.  **The Logic Graph Anchor:** Houses the `logic_graph`, a collection of LogicNodes
        representing the branching paths of the Architect's Will.
    4.  **Apophatic Null-Safety:** Every collection utilizes `default_factory`,
        ensuring that `.add()` or `.update()` never strikes a NoneType void.
    5.  **Thermodynamic Tomography:** Metadata initializer now includes
        `entropy_velocity` and `metabolic_tax` for real-time performance scrying.
    6.  **Sovereign Validation Registry:** `validation_rules` maps discovered variables
        to their respective Gnostic Jurisprudence laws (Ports, Emails, IDs).
    7.  **Isomorphic Type Inference:** The `inferred_types` sub-stratum (within metadata)
        stores the Pythonic primitives guessed by the Oracle during AST visitation.
    8.  **Topological Aura Mapping:** Explicit slots in metadata for categorizing
        where Gnosis is summoned (Path, Form, Logic, Will, Ritual).
    9.  **Hydraulic Merge Capability:** Designed with bit-perfect parity for the
        Parallel Swarm's `_merge_partial_dossier` rite.
    10. **Achronal Status Vigil:** Tracks the `achronal_status` (PENDING, RESONANT,
        FRACTURED) of the discovery lifecycle.
    11. **Cognitive Load Tomography:** Future-proofed with `cognitive_load_index`
        to calculate the "Human Understanding Cost" of the blueprint.
    12. **The Finality Vow:** A mathematical guarantee of a complete, serializable
        record of Truth, warded by Pydantic V2 titanium-grade validation.
    ... [Continuous through 24 levels of Gnostic Transcendence]
    =================================================================================
    """
    model_config = ConfigDict(
        frozen=False,
        arbitrary_types_allowed=True,
        extra='allow',
        populate_by_name=True
    )

    # --- STRATUM 0: THE GNOSTIC SETS (VARIABLES) ---
    required: Set[str] = Field(
        default_factory=set,
        description="The complete set of variables summoned by templates and logic."
    )

    defined: Set[str] = Field(
        default_factory=set,
        description="Variables willed into existence via $$ blocks or CLI injections."
    )

    missing: Set[str] = Field(
        default_factory=set,
        description="The Gnosis Gap: (Required - Defined). These atoms must be willed to achieve resonance."
    )

    derived: Set[str] = Field(
        default_factory=set,
        description="Variables calculated by the Alchemist from other Gnostic roots."
    )

    all_vars: Set[str] = Field(
        default_factory=set,
        description="The union of all known Gnostic identities in the current session."
    )

    # --- STRATUM 1: THE CAUSAL LINKS (DEPENDENCIES) ---
    dependencies: Dict[str, Set[str]] = Field(
        default_factory=dict,
        description="Mapping of files or variables to their required upstream souls."
    )

    validation_rules: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of variables to their Gnostic Jurisprudence contracts."
    )

    # --- STRATUM 2: THE CHRONICLE OF SIN (HERESIES) ---
    heresies: List[Any] = Field(
        default_factory=list,
        description="Ledger of non-fatal paradoxes and warnings found during discovery."
    )

    # --- STRATUM 3: THE TOPOGRAPHY OF WILL (GRAPHS) ---
    logic_graph: List[LogicNode] = Field(
        default_factory=list,
        description="The hierarchical tree of control flow (If/For/Try) willed by the Architect."
    )

    execution_plan: Optional[List[ScaffoldItem]] = Field(
        default=None,
        description="The final, flattened sequence of matter shards to be manifest in reality."
    )

    # --- STRATUM 4: METABOLIC FORENSICS (METADATA SANCTUARY) ---
    # =========================================================================
    # == [THE CURE]: THE OMNISCIENT METADATA INITIALIZER                     ==
    # =========================================================================
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "topology": {
                "path": set(),
                "form": set(),
                "logic": set(),
                "will": set(),
                "ritual": set()
            },
            "inferred_types": {},
            "cyclomatic_complexity": 0,  # <<< THE CRITICAL SUTURE
            "cognitive_load_index": 0.0,
            "discovery_latency_ms": 0.0,
            "achronal_status": "PENDING",
            "entropy_velocity": 0.0,
            "atom_density": 0.0
        },
        description="Sanctuary for high-order telemetry, HUD hints, and type inference Gnosis."
    )

    # =========================================================================
    # == CALCULATED REALITIES                                                ==
    # =========================================================================

    @property
    def is_resonant(self) -> bool:
        """Returns True if the Gnosis Gap is closed (No missing variables)."""
        return len(self.missing) == 0

    @property
    def complexity_rating(self) -> str:
        """Adjudicates the complexity based on the willed logic nodes."""
        cc = self.metadata.get("cyclomatic_complexity", 0)
        if cc < 5: return "ZEN"
        if cc < 15: return "RESONANT"
        if cc < 30: return "FEVERISH"
        return "CRITICAL"

    def __repr__(self) -> str:
        status = "RESONANT" if self.is_resonant else f"GAP({len(self.missing)})"
        cc = self.metadata.get("cyclomatic_complexity", 0)
        return f"<Ω_GNOSTIC_DOSSIER status={status} cc={cc} req={len(self.required)} def={len(self.defined)}>"

class GnosticVessel(BaseModel):
    """
    =============================================================================
    == THE PURE VESSEL OF GNOSTIC PERCEPTION (V-Ω-ETERNAL-APOTHEOSIS)          ==
    =============================================================================
    LIF: 100,000,000,000,000

    This is the ephemeral data packet that flows from the Lexer (Raw) to the Parser
    (Structured). It holds the intermediate state of a line being deconstructed.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    # --- Core Gnosis ---
    is_valid: bool = True
    raw_scripture: str = ""
    line_num: int = 0
    line_type: GnosticLineType = GnosticLineType.VOID
    original_indent: int = 0

    # --- Scaffold: The Language of Form ---
    name: str = ""
    path: Path = Field(default_factory=Path)
    is_dir: bool = False
    content: Optional[str] = None
    seed_path: Optional[Path] = None
    permissions: Optional[str] = None

    # [EXPANSION V-Ω] New Features
    is_symlink: bool = False
    symlink_target: Optional[str] = None
    expected_hash: Optional[str] = None

    trait_name: Optional[str] = None
    trait_path: Optional[str] = None
    trait_args: Optional[str] = None

    # --- The Alchemical Gnosis (Mutation & Semantics) ---
    mutation_op: Optional[str] = None
    semantic_selector: Optional[Dict[str, str]] = None

    # --- Symphony: The Language of Will ---
    edict_type: Optional[EdictType] = None
    command: Optional[str] = None
    vow_type: Optional[str] = None
    vow_args: List[str] = Field(default_factory=list)
    state_key: Optional[str] = None
    state_value: Optional[str] = None
    delimiter: Optional[str] = None
    capture_as: Optional[str] = None
    adjudicator_type: Optional[str] = None
    inputs: List[str] = Field(default_factory=list)
    language: Optional[str] = None
    script_block: Optional[str] = None
    directive_type: Optional[str] = None
    directive_args: List[str] = Field(default_factory=list)
    macro_name: Optional[str] = None

    # --- Logic & Control Flow ---
    is_jinja_construct: bool = False
    jinja_expression: Optional[str] = None
    condition: Optional[str] = None
    condition_type: Optional[Union[str, 'ConditionalType']] = None
    resilience_type: Optional['ResilienceType'] = None

    # --- Heresy & Parser State ---
    heresies: List['Heresy'] = Field(default_factory=list)

    # --- Symphony Block Structures ---
    body: List[Any] = Field(default_factory=list)
    else_body: Optional[List[Any]] = None
    parallel_edicts: List[Any] = Field(default_factory=list)


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
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    item: Optional['ScaffoldItem'] = None
    children: List['_GnosticNode'] = Field(default_factory=list)
    is_dir: bool = False
    complexity: Optional[Dict[str, Any]] = None
    git_info: Optional[Dict[str, Any]] = None
    dependency_gnosis: Optional[Dict[str, Any]] = None
    git_forensics: Optional[Dict[str, Any]] = None
    ast_gnosis: Optional[Dict[str, Any]] = None
    treesitter_gnosis: Optional[Dict[str, Any]] = None
    sentinel_gnosis: Optional[Dict[str, Any]] = None
    logic_result: Optional[bool] = Field(default=None, exclude=True)
    x_pos: Optional[int] = Field(default=None, exclude=True)
    y_pos: Optional[int] = Field(default=None, exclude=True)

    def find_child(self, name: str) -> Optional['_GnosticNode']:
        for child in self.children:
            if child.name == name: return child
        return None


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