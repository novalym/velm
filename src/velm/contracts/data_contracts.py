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
import uuid
import time
import argparse
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Set, Dict, Union, List, Any, TypedDict
from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field

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
    """Defines a single field in a %% contract definition."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    type_name: str
    gnostic_type: Any = Field(default=None, repr=False)  # The parsed type object
    default_value: Any = None
    is_optional: bool = False
    constraints: Dict[str, Any] = Field(default_factory=dict)
    is_list: bool = False


class GnosticContract(BaseModel):
    """Defines a full %% contract schema (a collection of fields)."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    fields: Dict[str, ContractField] = Field(default_factory=dict)
    raw_scripture: str = ""
    line_num: int = 0


# =============================================================================
# == III. THE VESSEL OF INTENT (ScaffoldItem)                                ==
# =============================================================================

@register_artisan("ScaffoldItem")
class ScaffoldItem(BaseModel):
    """
    =============================================================================
    == THE ATOMIC UNIT OF CREATION (V-Ω-ETERNAL-APOTHEOSIS-SEMANTIC)           ==
    =============================================================================
    LIF: ∞

    This is the most important data structure in the cosmos. It represents a
    single intent to create, modify, or verify a piece of reality.
    It flows from the Parser -> Creator -> Writer.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- I. The Core Gnostic Identity (Who/Where) ---
    path: Optional[Path] = Field(None, description="The scripture's intended place in reality.")
    is_dir: bool = Field(False, description="True if this represents a sanctum (directory).")
    line_num: int = Field(default=0, description="The line number in the source blueprint.")
    raw_scripture: str = Field(default="", description="The raw, untransmuted scripture from the file.")
    original_indent: int = Field(default=0, description="The visual indentation depth (hierarchy).")
    line_type: Any = Field(default=None, description="The GnosticLineType classification.")

    # --- II. The Soul of the Scripture (Content) ---
    content: Optional[str] = Field(None, description="The inner soul (text content) from inline definition (::).")
    seed_path: Optional[Union[Path, str]] = Field(None, description="Path to an external seed/template (<<).")

    # [UPDATED] Permissions can now be named ('executable') or octal ('755')
    permissions: Optional[str] = Field(None, description="Executable permissions (octal or named).")

    # [NEW] Encoding Hint (The Encoding Healer)
    encoding: Optional[str] = Field(None, description="Explicit encoding hint (e.g., 'latin-1') for reading seeds.")

    # --- [EXPANSION V-Ω] The Sentinel of Links (Symlinks) ---
    is_symlink: bool = Field(False, description="True if this item represents a symbolic link.")
    symlink_target: Optional[str] = Field(None, description="The target path the link points to.")

    # --- [EXPANSION V-Ω] The Hash Anchor (Integrity Lock) ---
    expected_hash: Optional[str] = Field(None,
                                         description="The cryptographic anchor (SRI) for integrity verification (algo:digest).")

    # --- [EXPANSION V-Ω] The Binary Diviner ---
    is_binary: bool = Field(False, description="True if content should be treated as raw bytes (e.g. base64 decoded).")

    # --- [EXPANSION V-Ω] The Gnostic Traits (Mixins) ---
    # Used when this item defines a trait usage or definition
    trait_name: Optional[str] = Field(None, description="The name of the trait being defined or used.")
    trait_args: Optional[str] = Field(None, description="Arguments passed to the trait (e.g. overrides).")
    trait_path: Optional[str] = Field(None, description="The file path to the trait definition.")

    # --- III. The Mutation Intent (Transfiguration) ---
    mutation_op: Optional[str] = Field(None, description="The glyph of mutation (+=, -=, ~=, ^=) or None.")
    semantic_selector: Optional[Dict[str, str]] = Field(None,
                                                        description="Targeting data for Semantic Surgery (@inside).")

    # --- IV. The Gnostic Provenance & Causality ---
    blueprint_origin: Optional[Path] = Field(None, description="The blueprint file that birthed this item.")
    condition: Optional[str] = Field(None, description="The Gnostic condition that governs this item's existence.")
    condition_type: Optional[str] = Field(None, description="The type of logic gate ('if', 'elif', 'else').")

    # --- V. Runtime State & Metadata (Ephemeral) ---
    content_hash: Optional[str] = None
    git_status: Optional[str] = None
    last_modified: Optional[float] = None
    is_empty: Optional[bool] = None
    semantic_scaffold: List[Any] = Field(default_factory=list)
    gnostic_soul_variable: Optional[str] = None
    edict_type: Optional[Any] = None
    blueprint_context: List['ScaffoldItem'] = Field(default_factory=list, repr=False)
    is_jinja_construct: bool = Field(default=False)
    jinja_expression: Optional[str] = Field(None)
    vows: List[str] = Field(default_factory=list)

    @property
    def name(self) -> str:
        """The atomic name of the item."""
        return self.path.name if self.path else ""


# =============================================================================
# == IV. THE VESSELS OF RESULT (THE OUTPUTS)                                 ==
# =============================================================================

class GnosticWriteResult(BaseModel):
    """
    =============================================================================
    == THE DIVINE CHRONICLE OF INSCRIPTION (V-Ω-MUTABLE-TRUTH)                 ==
    =============================================================================
    This vessel chronicles the exact outcome of a write operation. It is the
    fundamental unit of the Transaction Log.

    It holds the Truth of what happened: Success, Failure, Hash, Diff, and Security.
    """
    model_config = ConfigDict(frozen=False, arbitrary_types_allowed=True)

    success: bool = Field(description="True if the inscription was pure and successful.")
    path: Path = Field(description="The final physical path of the artifact.")
    action_taken: InscriptionAction = Field(description="The Gnostic soul of the outcome (CREATED, SKIPPED, etc.).")
    bytes_written: int = Field(description="Total bytes inscribed to disk.")

    # Forensic Data
    gnostic_fingerprint: Optional[str] = Field(None, description="SHA256 hash of the final content.")
    diff: Optional[str] = Field(None, description="Unified diff if content was modified.")

    # Metadata
    blueprint_origin: Optional[Path] = Field(None, description="The blueprint that commanded this write.")
    rite_name: str = Field(default="Unknown", description="The parent rite (e.g. 'Genesis', 'Patch').")
    is_from_cache: bool = Field(default=False, description="If Gnosis was resurrected from cache.")

    # Analysis
    dependencies: Optional[List[str]] = Field(default_factory=list, description="Dependencies discovered in the file.")
    metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Complexity metrics.")
    security_notes: List[str] = Field(default_factory=list, description="Security warnings (secrets found).")
    duration_ms: float = Field(default=0.0, description="Time taken to perform the write.")

    # Deep Analysis Data
    merge_details: Optional[Dict[str, Any]] = Field(None)
    treesitter_gnosis: Optional[Dict[str, Any]] = Field(None)
    sentinel_gnosis: Optional[Dict[str, Any]] = Field(None)

    @property
    def name(self) -> str: return self.path.name

    @property
    def stem(self) -> str: return self.path.stem

    @property
    def suffix(self) -> str: return self.path.suffix


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
    """The collected intelligence from a parsing run."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    required: Set[str] = Field(default_factory=set)
    defined: Set[str] = Field(default_factory=set)
    derived: Set[str] = Field(default_factory=set)
    all_vars: Set[str] = Field(default_factory=set)
    dependencies: Dict[str, Set[str]] = Field(default_factory=dict)
    validation_rules: Dict[str, str] = Field(default_factory=dict)
    heresies: List[Any] = Field(default_factory=list)

    # === THE DIVINE ASCENSION ===
    # The Dossier is now bestowed with a vessel to hold the graph of Will.
    logic_graph: List[LogicNode] = Field(default_factory=list)
    # ============================

    execution_plan: Optional[List[ScaffoldItem]] = Field(default=None)


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
    == THE VESSEL OF IMMUTABLE WILL (V-Ω-ADAMANT-SINGULARITY)                      ==
    =================================================================================
    LIF: ∞ (THE FROZEN MOMENT OF INTENT)

    This is the definitive contract between the CLI (The Mouth) and the Engine (The Mind).
    It captures the Architect's arguments, freezes them against mutation, and performs
    alchemical transmutation on raw inputs to prepare them for the God-Engine.

    It is forged with **Adamant Stability**: Fields possess defaults to prevent
    `AttributeError` during forensic inspection of failed rites.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, extra='ignore')

    # --- I. THE CHRONOMANCER'S SEAL (Identity & Time) ---
    request_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8],
                            description="Unique ID for this specific invocation.")
    timestamp: float = Field(default_factory=time.time, description="The precise moment the Will was spoken.")

    # --- II. THE ANCHOR OF REALITY (Location) ---
    base_path: Path = Field(default_factory=Path.cwd,
                            description="The physical root where the rite shall be conducted.")

    # --- III. THE ALCHEMICAL INPUTS (Data) ---
    set_vars: List[str] = Field(default_factory=list, description="Raw CLI variable overrides (key=value strings).")
    pre_resolved_vars: Dict[str, Any] = Field(default_factory=dict,
                                              description="Variables already transmuted by the Parser.")

    # --- IV. THE MODES OF EXISTENCE (Flags) ---
    # We provide direct defaults (= False) to ensure attributes exist immediately.
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
    extra_args: Dict[str, Any] = Field(default_factory=dict,
                                       description="Any unmapped arguments captured from the CLI.")

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
        The Gnostic Sensor. Returns True if the engine should enter
        Quantum Simulation mode (Dry Run, Preview, or Audit).

        [THE ADAMANT FIX]: Uses getattr to prevent AttributeError during
        traceback inspection if the vessel is fractured.
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
        The Alchemical Mixer.
        Merges `pre_resolved_vars` with parsed `set_vars`.
        Auto-magically types string values ('true' -> True, '123' -> 123).
        This is the ONE TRUE SOURCE of variable data for the Creator.
        """
        # Start with the base gnosis
        # We use getattr again for safety during crashes
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
                        # Only eval if it looks like a structure to avoid accidental eval of strings
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
    def from_namespace(cls, args: argparse.Namespace) -> 'GnosticArgs':
        """
        The Bridge from the Profane (argparse) to the Sacred (GnosticArgs).
        Extracts known fields and sweeps the rest into `extra_args`.
        """
        # 1. Identify known fields to avoid duplication in extra_args
        known_fields = cls.model_fields.keys()

        # 2. Extract values with safe defaults via getattr
        constructor_args = {
            "base_path": getattr(args, 'root', None) or getattr(args, 'project_root', None) or Path.cwd(),
            "set_vars": getattr(args, 'set', []) or [],
            "dry_run": getattr(args, 'dry_run', False),
            "force": getattr(args, 'force', False),
            "silent": getattr(args, 'silent', False),
            "preview": getattr(args, 'preview', False),
            "audit": getattr(args, 'audit', False),
            "verbose": getattr(args, 'verbose', False),
            "lint": getattr(args, 'lint', False),
            "non_interactive": getattr(args, 'non_interactive', False),
            "is_genesis_rite": getattr(args, 'is_genesis_rite', False),
            "adjudicate_souls": getattr(args, 'adjudicate_souls', False),
            "no_edicts": getattr(args, 'no_edicts', False),
        }

        # 3. Harvest the Unknown (Extra Args)
        # We filter out the keys we just extracted AND internal argparse keys like 'command' or 'func'
        ignored_keys = {'command', 'handler', 'herald', 'root', 'project_root', 'set'}

        extras = {}
        for k, v in vars(args).items():
            if k not in known_fields and k not in ignored_keys:
                extras[k] = v

        constructor_args['extra_args'] = extras

        # 4. Forge the Vessel

        return cls(**constructor_args)

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