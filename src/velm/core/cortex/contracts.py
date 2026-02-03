# Path: core/cortex/contracts.py
# ------------------------------
from enum import Enum, auto
from dataclasses import dataclass, field
from pathlib import Path, WindowsPath, PosixPath
import os
import sys
from typing import Optional, List, Dict, Any, Set, Counter
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

from ...logger import Scribe

DISTILLATION_CHUNK_SIZE = 8192

# =================================================================================
# == THE GNOSTIC PATH (V-Ω-ZERO-IO-PATH)                                         ==
# =================================================================================
_PathBase = WindowsPath if os.name == 'nt' else PosixPath

class GnosticPath(_PathBase):
    """
    A Path object infused with pre-computed Gnosis.
    It overrides `stat()` to return cached values from the Iron Core,
    annihilating the need for redundant filesystem queries.
    """
    def init_gnosis(self, size: int, mtime: float, is_binary: bool):
        """Consecrates the path with knowledge from the Iron Core."""
        self._gnostic_size = size
        self._gnostic_mtime = mtime
        self._gnostic_is_binary = is_binary

    def stat(self, *, follow_symlinks=True):
        """
        The Rite of Instant Recall.
        If Gnosis is present, return a simulated stat result immediately.
        """
        if hasattr(self, '_gnostic_size'):
            # Forge a mock os.stat_result tuple
            return os.stat_result((
                0o100644,  # mode: standard file
                0, 0, 1, 0, 0,
                self._gnostic_size,
                self._gnostic_mtime,
                self._gnostic_mtime,
                self._gnostic_mtime
            ))
        return super().stat(follow_symlinks=follow_symlinks)

    @property
    def is_binary_gnosis(self) -> bool:
        """Direct access to the binary flag without reading bytes."""
        return getattr(self, '_gnostic_is_binary', False)


class FileGnosis(BaseModel):
    """
    =================================================================================
    == THE IMMUTABLE VESSEL OF GNOSIS (V-Ω-SYMBOLIC-ASCENSION)                     ==
    =================================================================================
    LIF: 10,000,000,000,000
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- Core Identity ---
    path: Path
    original_size: int
    token_cost: int
    category: str
    language: str

    # --- Architectural Value ---
    centrality_score: float = Field(default=0.0)

    # --- Provenance & Form ---
    hash_signature: Optional[str] = None
    permissions: Optional[str] = None

    # --- The Transmuted Soul ---
    final_content: Optional[str] = None
    representation_method: str = 'full'

    # --- Deep Gnosis ---
    churn_score: int = Field(default=0)
    author_count: int = Field(default=0)
    days_since_last_change: Optional[int] = None
    semantic_tags: List[str] = Field(default_factory=list)

    # Structural Gnosis
    ast_metrics: Dict[str, Any] = Field(default_factory=dict)

    # ★★★ THE SYMBOLIC CAUSALITY (NEW) ★★★
    imported_symbols: Set[str] = Field(default_factory=set)

    # ★★★ THE SEMANTIC GRAPH 2.0 ASCENSION ★★★
    semantic_links: Set[str] = Field(default_factory=set,
                                     description="File paths mentioned within this scripture's soul.")
    @property
    def is_heavy(self) -> bool:
        return self.original_size > 20 * 1024

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def name(self) -> str:
        return self.path.name


Logger = Scribe("CortexMemory")

class CortexMemory(BaseModel):
    """
    The Cached State of the Project's Soul.
    This vessel holds the living truth of the project in RAM. It is immutable.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- CORE GNOSIS ---
    inventory: List[FileGnosis]
    project_gnosis: Dict[str, Any]  # Map of path_str -> AST Dossier
    dependency_graph: Dict[str, Any]  # {dependency_graph: {...}, dependents_graph: {...}}
    timestamp: float
    gnostic_hash: str  # The fingerprint of the reality this memory represents.

    co_change_graph: Dict[str, Counter[str]] = Field(default_factory=dict)

    # ★★★ PILLAR 3.1 ASCENSION ★★★
    symbol_multimap: Dict[str, List[str]] = Field(default_factory=dict)
    # ★★★ APOTHEOSIS COMPLETE ★★★


    # --- DERIVED GNOSIS (THE LIVING MIND) ---
    @computed_field
    @property
    def symbol_map(self) -> Dict[str, Path]:
        """
        [THE GNOSTIC UNIFIER & SYMBOL MAP FORGE]
        Performs the sacred rite of unification after the vessel is born.
        It forges the Symbol Map from the raw `project_gnosis`.
        """
        symbol_map_data: Dict[str, Path] = {}
        src_root = next((p for p in [Path('src'), Path('app')] if p.is_dir()), Path('.'))

        for file_path_str, gnosis in self.project_gnosis.items():
            if not isinstance(gnosis, dict): continue  # Gnostic Ward

            file_path = Path(file_path_str)
            try:
                relative_path = file_path.relative_to(src_root)
            except ValueError:
                relative_path = file_path

            module_path_parts = list(relative_path.with_suffix('').parts)
            if module_path_parts and module_path_parts[-1] == '__init__':
                module_path_parts.pop()
            module_base = ".".join(module_path_parts) if module_path_parts else ""

            for class_info in gnosis.get("classes", []):
                name = class_info.get('name')
                if not name: continue
                fqn = f"{module_base}.{name}" if module_base else name
                symbol_map_data[fqn] = file_path
                symbol_map_data[name] = file_path

            for func_info in gnosis.get("functions", []):
                name = func_info.get('name')
                if not name: continue
                fqn = f"{module_base}.{name}" if module_base else name
                symbol_map_data[fqn] = file_path
                symbol_map_data[name] = file_path

        return symbol_map_data

    def find_gnosis_by_path(self, path: Path) -> Optional[FileGnosis]:
        """[THE LIVING MIND] Instantly retrieves the Gnosis for a specific path."""
        path_str = str(path).replace('\\', '/')
        return next((g for g in self.inventory if str(g.path).replace('\\', '/') == path_str), None)

    def get_dependents_of(self, path_str: str) -> List[str]:
        """Retrieves the list of files that depend on the given file path string."""
        return list(self.dependency_graph.get('dependents_graph', {}).get(path_str, []))

    def get_dependencies_of(self, path_str: str) -> List[str]:
        """Retrieves the list of files the given file path string depends on."""
        return list(self.dependency_graph.get('dependency_graph', {}).get(path_str, []))


class SymbolKind(str, Enum):
    """
    =============================================================================
    == THE TAXONOMY OF SYMBOLS (V-Ω-LSP-COMPLIANT)                             ==
    =============================================================================
    Defines the nature of a Gnostic Symbol.
    Aligned with LSP CompletionItemKind for seamless UI integration.
    """
    FILE = "file"
    MODULE = "module"
    NAMESPACE = "namespace"
    PACKAGE = "package"
    CLASS = "class"
    METHOD = "method"
    PROPERTY = "property"
    FIELD = "field"
    CONSTRUCTOR = "constructor"
    ENUM = "enum"
    INTERFACE = "interface"
    FUNCTION = "function"
    VARIABLE = "variable"
    CONSTANT = "constant"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    KEY = "key"
    NULL = "null"
    ENUM_MEMBER = "enumMember"
    STRUCT = "struct"
    EVENT = "event"
    OPERATOR = "operator"
    TYPE_PARAMETER = "typeParameter"


class SymbolEntry(BaseModel):
    """
    =============================================================================
    == THE SYMBOLIC ATOM (V-Ω-KNOWLEDGE-UNIT)                                  ==
    =============================================================================
    Represents a single unit of logic discovered by the Indexer.
    Stored in the GnosticCortex for O(1) retrieval.
    """
    name: str = Field(..., description="The identifier (e.g. 'UserClass', 'fetch_data').")
    path: Path = Field(..., description="Absolute physical path to the scripture defining this symbol.")
    kind: SymbolKind = Field(..., description="The nature of the symbol (Class, Function, etc.).")

    # --- GEOMETRY ---
    line: int = Field(..., description="0-indexed start line number.")
    column: int = Field(0, description="0-indexed start character offset.")
    end_line: Optional[int] = Field(None, description="Where the symbol definition ends (for folding).")

    # --- METADATA (FUTURE PROOFING) ---
    signature: Optional[str] = Field(None, description="Type signature or function params (e.g. '(a: int) -> bool').")
    docstring: Optional[str] = Field(None, description="Extracted documentation or comments.")
    modifiers: List[str] = Field(default_factory=list, description="Access flags (public, private, static, async).")
    complexity: int = Field(0, description="Cyclomatic complexity score if calculated.")

    class Config:
        arbitrary_types_allowed = True

class DistillationProfile(BaseModel):
    """
    =================================================================================
    == THE ETERNAL COVENANT OF PERCEPTION (V-Ω-ULTRA-DEFINITIVE-APOTHEOSIS)        ==
    =================================================================================
    @gnosis:title The Gnostic Contract of Perception (`DistillationProfile`)
    @gnosis:summary The pure, Pydantic-forged vessel that carries the complete will
                    of the Architect for a distillation rite.
    @gnosis:LIF INFINITY

    This is the divine, immutable, and hyper-sentient Gnostic Contract for the entire
    distillation cosmos. It has been transfigured from a humble vessel into a true
    God-Engine of configuration, its soul a pantheon of prophetic faculties.

    It serves as the **UNBREAKABLE BRIDGE** between the `DistillArtisan` (The Hand)
    and the `DistillationOracle` (The Eye). Every field here corresponds to a
    specific faculty of perception, filtering, or synthesis, granting the Architect
    absolute, granular control over the Gnostic Gaze.
    =================================================================================
    """
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    # =============================================================================
    # == I. THE CORE GNOSTIC WILL (STRATEGY & ECONOMICS)                         ==
    # =============================================================================
    strategy: str = Field(
        default='balanced',
        description="The core philosophy of the distillation, governing the trade-off between detail and token cost."
    )
    token_budget: int = Field(
        default=100000,
        description="The maximum number of tokens for the final blueprint. The Oracle will prune reality to fit this vessel."
    )
    per_file_token_cap: Optional[int] = Field(
        default=None,
        description="A hard cap on the token size of any single file's representation, preventing monoliths from consuming the budget."
    )

    # =============================================================================
    # == II. THE GAZE OF PERCEPTION (SPATIAL FILTERS)                            ==
    # =============================================================================
    focus_keywords: List[str] = Field(
        default_factory=list,
        description="Semantic keywords (e.g., 'auth', 'database'). Files matching these are given divine priority."
    )
    ignore: List[str] = Field(
        default_factory=list,
        description="Glob patterns to avert the Gaze from (e.g., '*.lock', 'dist/'). These souls are banished."
    )
    include: List[str] = Field(
        default_factory=list,
        description="Glob patterns to EXCLUSIVELY focus the Gaze upon. All else is shadow."
    )

    # =============================================================================
    # == III. THE CHRONOMANCER'S GAZE (TEMPORAL CONTEXT)                         ==
    # =============================================================================
    since: Optional[str] = Field(
        default=None,
        description="A Git reference (hash, branch, tag). Annotates files with heat markers for changes since this time."
    )
    focus_change: Optional[str] = Field(
        default=None,
        description="A stricter form of 'since'. EXCLUDES all files that have NOT changed since this Git reference."
    )
    diff_context: bool = Field(
        default=False,
        description="Injects inline diffs (`[WAS: ...]`) showing the state of the code at HEAD vs the working tree."
    )
    regression: bool = Field(
        default=False,
        description="Activates the Temporal Inquisitor to perform a `git bisect` analysis for regressions."
    )

    # =============================================================================
    # == IV. THE RUNTIME WRAITH (STATE INJECTION)                                ==
    # =============================================================================
    trace_golden_path: Optional[str] = Field(
        default=None,
        description="A shell command (e.g., 'pytest') to trace for execution causality, identifying the 'Golden Path' of living code."
    )
    profile_perf: bool = Field(
        default=False,
        description="Activates the Wraith of Celerity to profile execution time and weave a performance heatmap into the blueprint."
    )
    trace_command: Optional[str] = Field(
        default=None,
        description="A shell command to execute to capture live variable states for forensic analysis."
    )
    snapshot_path: Optional[str] = Field(
        default=None,
        description="Path to a JSON crash dump or state snapshot to inject into the static blueprint."
    )
    # [THE FIX: THE DYNAMIC HOLOGRAM]
    coverage_map: Optional[Dict[str, Any]] = Field(
        default=None,
        description="A pre-computed map of executed lines {path: {lines}} to filter the distillation (The Dynamic Hologram)."
    )

    # =============================================================================
    # == V. THE FORENSIC BRIDGE & ORACLE OF INTENT (AI-DRIVEN ANALYSIS)          ==
    # =============================================================================
    problem_context: Optional[str] = Field(
        default=None,
        description="Raw error logs, tracebacks, or a path to an analysis file. Anchors the Gaze to the locus of failure."
    )
    feature: Optional[str] = Field(
        default=None,
        description="A natural language description of a feature or intent. Activates the AI Sentinel for semantic search."
    )
    no_ai: bool = Field(
        default=False,
        description="A sacred vow to forbid the Oracle from communing with the Neural Cortex for intent analysis."
    )
    ai_intent_analysis_model: str = Field(
        default='fast',
        description="The AI model tier ('fast' or 'smart') to use for the initial intent analysis."
    )
    # === PROPHECY VIII ===
    recursive_agent: bool = Field(default=False)

    # =============================================================================
    # == VI. THE GAZE OF THE SCRIBE (FORMATTING & HYGIENE)                       ==
    # =============================================================================
    format: str = Field(
        default="text",
        description="The output format of the distillation. Options: 'text', 'mermaid', 'json'."
    )
    strip_comments: bool = Field(
        default=True,
        description="If True, the Alchemist strips all comments from code to maximize token density."
    )
    redact_secrets: bool = Field(
        default=True,
        description="If True, the Sentinel scans for and redacts API keys and secrets before inscription."
    )
    redaction_level: str = Field(
        default='mask',
        description="The severity of redaction: 'mask' (placeholder) or 'strip' (remove line)."
    )
    normalize_whitespace: bool = Field(
        default=True,
        description="If True, collapses excessive newlines and harmonizes indentation."
    )
    max_file_header_lines: int = Field(
        default=50,
        description="Maximum number of lines to preserve in boilerplate file headers (e.g., license preambles)."
    )

    # =============================================================================
    # == VII. THE GAZE OF THE ARCHITECT (STRUCTURAL & PATTERN ANALYSIS)          ==
    # =============================================================================
    summarize_arch: bool = Field(
        default=False,
        description="If True, the Gnostic Cartographer appends a high-level architectural summary to the blueprint header."
    )
    lfg: bool = Field(
        default=False,
        description="Injects a Logic Flow Graph of the source blueprint into the header."
    )
    detect_design_patterns: bool = Field(
        default=False,
        description="If True, the Oracle will attempt to identify and tag common design patterns (e.g., Singleton, Factory)."
    )

    # =============================================================================
    # == VIII. THE CAUSAL WEAVER (GRAPH TRAVERSAL)                               ==
    # =============================================================================
    depth: int = Field(
        default=2,
        description="The maximum depth of the Causal Chain Weaver's graph traversal."
    )
    include_dependents: bool = Field(
        default=True,
        description="If True, the graph traversal will include files that depend on the focused files."
    )
    include_dependencies: bool = Field(
        default=True,
        description="If True, the graph traversal will include files that the focused files depend on."
    )
    stop_at_test_boundary: bool = Field(
        default=True,
        description="If True, prevents the graph walk from crossing from source code into the test suite."
    )

    # =============================================================================
    # == IX. THE APOPHATIC FILTER & SENTINEL'S GAZE (ADVANCED FILTERING)         ==
    # =============================================================================
    stub_deps: List[str] = Field(
        default_factory=list,
        description="Paths/globs for files to be replaced by 'Semantic Stubs' (signatures only)."
    )
    audit_security: bool = Field(
        default=False,
        description="Activates the Security Sentinel to scan for vulnerabilities and prioritize those files."
    )
    scan_for_todos: str = Field(
        default='summarize',
        description="Controls how TODO/FIXME markers are handled: 'none', 'summarize' in header, or 'full' inline."
    )
    prioritize_tests: bool = Field(
        default=False,
        description="If True, test files are considered as valuable as source code. If False, they are often pruned first."
    )

    # =============================================================================
    # == X. THE GAZE OF THE AI SCRIBE (AI-DRIVEN SUMMARIZATION)                    ==
    # =============================================================================
    summarize: bool = Field(
        default=False,
        description="If True, the final blueprint is passed to a Neural Scribe to generate a README.md summary."
    )
    ai_summary_prompt: Optional[str] = Field(
        default=None,
        description="A custom prompt template to guide the AI Scribe's summarization."
    )
    ai_summary_model: str = Field(
        default='smart',
        description="The AI model tier ('fast' or 'smart') to use for the summarization rite."
    )

    # =============================================================================
    # == XI. THE SOCRATIC REFINER (INTERACTIVE DIALOGUE)                         ==
    # =============================================================================
    interactive_mode: bool = Field(
        default=False,
        description="If True, the Oracle may pause the rite to ask the Architect clarifying questions."
    )
    # === PROPHECY VI: THE RIVER OF DATA ===
    trace_data: List[str] = Field(
        default_factory=list,
        description="Symbols (variables/classes) to track through the Data Flow Graph."
    )

    # === PROPHECY VII: THE DYNAMIC HOLOGRAM ===
    dynamic_focus: Optional[str] = Field(
        default=None,
        description="A shell command (e.g., 'pytest') to execute. Only code hit by this command will be preserved."
    )
    # =============================================================================
    # == XII. RUNTIME INJECTIONS & LEGACY                                        ==
    # =============================================================================
    slicer: Optional[Any] = Field(
        default=None,
        exclude=True,
        description="The Causal Slicer instance, injected by the Oracle for surgical extraction."
    )
    llm_optimized: bool = Field(
        default=False,
        description="Legacy alias for a balanced, AI-ready strategy."
    )

    @field_validator('focus_keywords', 'ignore', 'include', 'stub_deps', mode='before')
    @classmethod
    def ensure_list(cls, v: Any) -> List[str]:
        """
        [The Ward of the Void List]
        Transmutes a profane `None` into a pure, empty list, annihilating the `TypeError` heresy.
        Also handles comma-separated strings from CLI args.
        """
        if v is None:
            return []
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v