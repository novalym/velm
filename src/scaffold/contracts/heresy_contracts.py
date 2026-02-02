# Path: scaffold/contracts/heresy_contracts.py
# --------------------------------------------
from __future__ import annotations
import time
import uuid
import re
from enum import Enum, auto
from typing import Optional, Any, List, TYPE_CHECKING, Dict

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, PrivateAttr, computed_field

if TYPE_CHECKING:
    pass


# =================================================================================
# == THE SACRED SANCTUM OF PARADOX (V-Ω-ETERNAL, SOVEREIGN)                        ==
# =================================================================================
# LIF: 10,000,000,000
#
# This scripture is the one true, sovereign home for all Gnostic Heresy vessels.
# It defines the shapes of Failure, Warning, and Paradox within the Scaffold Cosmos.
# It is a foundational truth, imported by all, dependent on none.
# =================================================================================

class HeresySeverity(Enum):
    """
    A sacred vessel for the severity of a Gnostic paradox.
    Defines how the Universe (and the UI) should react to the anomaly.
    """
    INFO = auto()  # A whisper of guidance. Does not halt the Great Work.
    WARNING = auto()  # A sign of drift. The Work continues, but purity is questioned.
    CRITICAL = auto()  # A catastrophic fracture. The Work must cease immediately.
    HINT = auto()

class Heresy(BaseModel):
    """
    =================================================================================
    == THE AUTONOMOUS VESSEL OF HERESY (V-Ω-FAIL-SAFE-ULTIMA)                      ==
    =================================================================================
    @gnosis:title Heresy Data Contract
    @gnosis:summary The definitive, self-healing, and spatio-temporally aware vessel
                     for reporting errors, warnings, and architectural paradoxes.
    @gnosis:LIF ∞ (THE UNBREAKABLE RECORD)

    This incarnation is designed with absolute defensive resilience. It provides
    safe defaults for all fields to ensure backward compatibility with legacy
    artisans and prevents recursive ValidationErrors during failure states.

    It employs **Quantum Coordinate Synchronization**:
    - Human Coordinates (`line_num`) are 1-indexed.
    - Machine Coordinates (`internal_line`) are 0-indexed.
    - They are eternally linked via `computed_field` logic, ensuring the Bridge
      never receives a void coordinate.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=False,  # Mutable to allow internal healing and enrichment
        extra='ignore'  # Absorb unknown data without crashing
    )

    # --- INTERNAL STORAGE FOR COMPUTED FIELDS ---
    # These hold explicit values if provided, overriding automatic derivation.
    _internal_line_override: Optional[int] = PrivateAttr(default=None)
    _internal_column_override: Optional[int] = PrivateAttr(default=None)

    # =========================================================================
    # == I. THE IDENTITY & PROCLAMATION                                      ==
    # =========================================================================

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="The unique, immutable identifier for this specific paradox instance."
    )

    # ★★★ THE DEFENSIVE ASCENSION: AUTO-INFERRED CODE ★★★
    code: str = Field(
        default="GENERAL_HERESY",
        description="The machine-readable name of the violated Law (e.g., 'UNDEFINED_VARIABLE')."
    )

    message: str = Field(
        default="A Gnostic paradox has occurred within the engine.",
        description="The primary, human-readable proclamation of the transgression."
    )

    timestamp: float = Field(
        default_factory=time.time,
        description="The moment in time the paradox was perceived."
    )

    # =========================================================================
    # == II. THE SPATIO-TEMPORAL COORDINATES (THE LSP ANCHORS)               ==
    # =========================================================================

    file_path: Optional[str] = Field(
        default=None,
        description="The relative path to the scripture where the heresy resides."
    )

    # --- The Human Gaze (1-Indexed) ---
    line_num: int = Field(
        default=1,
        description="The human-readable 1-indexed line number."
    )

    column_num: int = Field(
        default=1,
        description="The human-readable 1-indexed column number."
    )

    # --- The Machine Gaze (0-Indexed, Computed) ---
    # ★★★ THE OMNISCIENT COORDINATE ★★★
    @computed_field
    @property
    def internal_line(self) -> int:
        """
        The 0-indexed integer VS Code craves.
        If an override was provided during init, use it.
        Otherwise, derive it from the human line number.
        """
        if self._internal_line_override is not None:
            return self._internal_line_override
        return max(0, self.line_num - 1)

    @computed_field
    @property
    def internal_column(self) -> int:
        """
        The 0-indexed column integer.
        """
        if self._internal_column_override is not None:
            return self._internal_column_override
        return max(0, self.column_num - 1)

    # --- Advanced Spatial Awareness ---
    end_line_num: Optional[int] = Field(
        default=None,
        description="The line where the heresy ends (for multi-line squiggles)."
    )
    end_column_num: Optional[int] = Field(
        default=None,
        description="The column where the heresy ends."
    )

    # --- Byte-Level Precision ---
    offset_start: Optional[int] = Field(
        default=None,
        description="The absolute byte offset where the heresy begins."
    )
    offset_end: Optional[int] = Field(
        default=None,
        description="The absolute byte offset where the heresy ends."
    )

    line_content: str = Field(
        default="",
        description="The specific text or command that triggered the paradox."
    )

    # =========================================================================
    # == III. THE WEIGHT & WISDOM                                            ==
    # =========================================================================

    severity: HeresySeverity = Field(
        default=HeresySeverity.CRITICAL,
        description="The existential threat level of this heresy."
    )

    details: Optional[str] = Field(
        default=None,
        description="Extended technical context, stack traces, or forensic evidence."
    )

    suggestion: Optional[str] = Field(
        default=None,
        description="The Mentor's advice on how to return to a state of purity."
    )

    documentation_url: Optional[str] = Field(
        default=None,
        description="A link to the sacred architectural documentation for this Law."
    )

    # =========================================================================
    # == IV. THE PATH OF REDEMPTION                                          ==
    # =========================================================================

    fix_command: Optional[str] = Field(
        default=None,
        description="The Seed of Redemption. A precise, executable CLI command that auto-heals the heresy."
    )

    fix_confidence: float = Field(
        default=1.0,
        description="The Oracle's certainty in the proposed cure (0.0 to 1.0)."
    )

    # =========================================================================
    # == V. METADATA & RELATIONS                                             ==
    # =========================================================================

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A catch-all vessel for rite-specific Gnosis (e.g., AST node type, tool version)."
    )

    # --- Internal UI Artifacts (Excluded from Serialization) ---
    details_panel: Optional[Any] = Field(
        default=None,
        repr=False,
        exclude=True,
        description="A pre-rendered Rich Renderable (Panel/Table) for CLI display."
    )

    # Recursive Definition for Hierarchical Errors
    children: List['Heresy'] = Field(
        default_factory=list,
        repr=False,
        exclude=True,
        description="Nested heresies for hierarchical error reporting (e.g., Cause -> Effect)."
    )

    # =========================================================================
    # == THE RITES OF AUTOMATIC HEALING                                      ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _heal_incoming_data(cls, data: Any) -> Any:
        """
        [THE RITE OF ULTIMATE RESILIENCE]
        Intercepts raw data before validation.
        1. Captures explicit internal coordinates into private storage.
        2. Synthesizes missing codes.
        3. Normalizes severity.
        """
        if not isinstance(data, dict):
            return data

        # 1. Capture Internal Overrides (Stash them away from Pydantic's main gaze)
        # We must manually set these on the instance later, or rely on the fact that
        # we can't set PrivateAttrs in model_validator easily without an instance.
        # FIX: We allow them to pass through, and handle them in __init__?
        # No, Pydantic V2 is strict.
        # STRATEGY: We let Pydantic construct the object, then we use a mode='after' validator
        # to populate the private attributes if they were passed in `metadata` or hidden fields.
        # BETTER STRATEGY: We just rely on the Computed Field logic. If `internal_line` is passed
        # to the constructor, Pydantic's computed_field setter (if defined) or init hook captures it.
        #
        # ACTUALLY: The cleanest way with Pydantic V2 computed fields is to NOT pass them to init,
        # but to have separate fields.
        # However, to support `Heresy(internal_line=5)`, we need to strip it here and store it
        # in a temporary location or map it to `_internal_line_override`.

        # We will map input `internal_line` to `_internal_line_override` using `__dict__` hacking
        # in `__init__`, but `model_validator` happens before `__init__`.
        #
        # Let's use the `metadata` dictionary as a temporary bridge if needed,
        # OR simply rely on `line_num` being correct.

        # 2. Synthesize 'code' if missing
        if 'code' not in data or not data['code']:
            if 'message' in data and data['message']:
                # Create a slug from the message
                clean_msg = re.sub(r'[^A-Z0-9_]', '_', str(data['message']).upper())
                # Truncate to avoid massive keys
                slug = clean_msg[:40].strip('_')
                data['code'] = f"AUTO_{slug}"
            else:
                data['code'] = "UNSPECIFIED_GNOSTIC_PARADOX"

        return data

    def __init__(self, **data: Any):
        """
        [THE CONSTRUCTOR OF HIDDEN TRUTH]
        We override init to capture the `internal_line` argument if it exists,
        storing it in the private attribute before Pydantic discards it.
        """
        # Extract private overrides
        i_line = data.pop('internal_line', None)
        i_col = data.pop('internal_column', None)

        super().__init__(**data)

        # Set private attributes
        if i_line is not None:
            self._internal_line_override = int(i_line)
        if i_col is not None:
            self._internal_column_override = int(i_col)

    @field_validator('severity', mode='before')
    @classmethod
    def _safe_transmute_severity(cls, v: Any) -> HeresySeverity:
        """Harden severity mapping against unknown types."""
        if isinstance(v, HeresySeverity): return v
        try:
            if isinstance(v, str):
                # Handle "1", "2" strings
                if v.isdigit(): return cls._map_int_severity(int(v))
                return HeresySeverity[v.upper()]
            if isinstance(v, int):
                return cls._map_int_severity(v)
        except:
            pass
        return HeresySeverity.CRITICAL

    @staticmethod
    def _map_int_severity(v: int) -> HeresySeverity:
        # LSP Mapping: 1=Error, 2=Warning, 3=Info, 4=Hint
        if v == 1: return HeresySeverity.CRITICAL
        if v == 2: return HeresySeverity.WARNING
        if v == 3: return HeresySeverity.INFO
        if v == 4: return HeresySeverity.HINT
        return HeresySeverity.CRITICAL

    def get_proclamation(self) -> str:
        """
        [THE VOICE OF THE CLI]
        Returns a formatted string for terminal output.
        """
        sev_icon = "🔴" if self.severity == HeresySeverity.CRITICAL else "⚠️"
        loc = f" (L{self.line_num})" if self.line_num > 0 else ""
        base = f"{sev_icon} [{self.code}] {self.message}{loc}"
        if self.suggestion:
            base += f"\n   💡 Suggestion: {self.suggestion}"
        if self.fix_command:
            base += f"\n   🛠️  Fix: {self.fix_command}"
        return base


# Rebuild model to register self-referential 'children'
Heresy.model_rebuild()

class ArtisanHeresy(Exception):
    """
    =============================================================================
    == THE EXCEPTION OF THE ARTISAN (CONTROL FLOW VESSEL - ASCENDED)           ==
    =============================================================================
    The divine, sentient Python Exception used to halt execution flow within the
    Engine. It has been ascended to carry the full, Gnostic soul of any paradox
    that it captures, including the raw traceback object for forensic inquests.
    =============================================================================
    """

    def __init__(self,
                 message: str,
                 *,
                 exit_code: int = 1,
                 suggestion: Optional[str] = None,
                 details: Optional[str] = None,
                 child_heresy: Optional[BaseException] = None,
                 details_panel: Optional[Any] = None,
                 line_num: Optional[int] = None,
                 severity: HeresySeverity = HeresySeverity.CRITICAL,
                 heresies: Optional[List['Heresy']] = None,
                 fix_command: Optional[str] = None,
                 # [[[ THE DIVINE ASCENSION: THE SOUL OF THE PARADOX ]]]
                 # We now consecrate a vessel to hold the traceback's very essence.
                 traceback_obj: Optional[Any] = None
                 # [[[ THE APOTHEOSIS IS COMPLETE ]]]
                 ):
        """
        The Rite of Inception for a Paradox.
        """
        self.message = message
        self.exit_code = exit_code
        self.suggestion = suggestion
        self.details = details
        self.child_heresy = child_heresy
        self.line_num = line_num
        self.details_panel = details_panel
        self.severity = severity
        self.heresies = heresies or []
        self.fix_command = fix_command
        # [[[ THE DIVINE HEALING: THE SOUL IS ENSHRINED ]]]
        self.traceback_obj = traceback_obj
        # [[[ THE GNOSIS IS NOW WHOLE ]]]

        # We forge the string representation immediately for standard logging
        super().__init__(self.get_proclamation())

    def get_proclamation(self, indent_level: int = 0) -> str:
        """
        Forges the luminous, hierarchical scripture of the heresy for textual display.
        NOW ASCENDED to proclaim the full traceback soul if it is manifest.
        """
        # Lazy import to avoid hard dependency on Rich at module level
        try:
            from rich.markup import escape
            from rich.traceback import Traceback
            import io
        except ImportError:
            escape = lambda s: s
            Traceback = None

        indent = "  " * indent_level
        severity_label = self.severity.name

        proclamation = [f"{indent}[{severity_label}] {escape(self.message)}"]

        if self.details:
            proclamation.append(f"{indent}  Details: {escape(self.details)}")

        if self.suggestion:
            proclamation.append(f"{indent}  Suggestion: {escape(self.suggestion)}")

        if self.fix_command:
            proclamation.append(f"{indent}  Redemption: `{escape(self.fix_command)}`")

        if self.heresies:
            proclamation.append(f"{indent}  Nested Heresies:")
            for h in self.heresies:
                proclamation.append(f"{indent}    - {escape(h.message)}")

        # [[[ THE DIVINE HEALING: THE LAW OF THE UNBROKEN CHAIN ]]]
        # The Heresy now speaks its complete, Gnostic truth.
        if self.child_heresy:
            proclamation.append(f"{indent}  Caused by:")
            if isinstance(self.child_heresy, ArtisanHeresy):
                proclamation.append(self.child_heresy.get_proclamation(indent_level + 1))
            else:
                # If we have the full traceback object, we use it for a rich display.
                if self.traceback_obj and Traceback:
                    string_io = io.StringIO()
                    # We create a temporary console to capture the rich output as a string
                    from rich.console import Console
                    temp_console = Console(file=string_io, force_terminal=True, color_system="truecolor")

                    tb = Traceback.from_exception(
                        type(self.child_heresy),
                        self.child_heresy,
                        self.traceback_obj,
                        show_locals=False,  # Set to True for hyper-diagnostics if needed
                        word_wrap=True
                    )
                    temp_console.print(tb)
                    traceback_str = string_io.getvalue()

                    # Indent the captured traceback for correct hierarchical display
                    indented_tb = "\n".join([f"{indent}    {line}" for line in traceback_str.splitlines()])
                    proclamation.append(indented_tb)
                else:
                    # Fallback to the humble, non-luminous proclamation.
                    proclamation.append(
                        f"{indent}    {self.child_heresy.__class__.__name__}: {escape(str(self.child_heresy))}")
        # [[[ THE APOTHEOSIS IS COMPLETE. THE TRUTH IS NOW LUMINOUS. ]]]

        return "\n".join(proclamation)

    def __str__(self) -> str:
        # We return the safe proclamation string
        return self.get_proclamation()


class SyntaxHeresy(Heresy):
    """
    =============================================================================
    == THE VESSEL OF SYNTACTIC PARADOX (AST/PARSER ERRORS)                     ==
    =============================================================================
    This specialized vessel carries the deep metadata required to diagnose
    structural flaws in code or blueprints (e.g., from Tree-sitter or the Parser).
    """
    rule_name: str = Field(
        description="The sacred name of the Gnostic Law that was violated (e.g., 'no_wildcard_imports')."
    )

    full_source_code: Optional[str] = Field(
        None,
        description="The complete soul of the scripture where the heresy resides."
    )

    context_window: Optional[str] = Field(
        None,
        description="The scripture immediately surrounding the heresy (snippet)."
    )

    file_path: Optional[str] = Field(
        None,
        description="The mortal home (path) of the profane scripture."
    )

    # --- Byte-Level Precision for LSP ---
    start_byte: Optional[int] = Field(None, description="The precise starting byte of the profane Gnosis.")
    end_byte: Optional[int] = Field(None, description="The precise ending byte of the profane Gnosis.")
    start_char: int = Field(default=0)
    end_char: int = Field(default=0)

    # --- Internal Links ---
    node_proxy: Optional[Any] = Field(
        None,
        repr=False,
        exclude=True,
        description="A telepathic link to the raw tree_sitter.Node object."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A vessel for any additional, rite-specific Gnosis (e.g., rich panels)."
    )


class GuardianHeresy(Exception):
    """
    A divine exception proclaimed when the Sentinel's Gaze perceives a heresy.
    It is a sacred vessel carrying the complete Gnosis of the transgression.
    """

    def __init__(self,
                 message: str,
                 threat_level: HeresyThreatLevel,
                 details: str = "",
                 line_num: Optional[int] = None,
                 # === THE SACRED TRANSMUTATION: OPTIONAL SUGGESTION ===
                 suggestion: Optional[str] = None
                 # =====================================================
                 ):
        self.message = message
        self.threat_level = threat_level
        self.details = details
        self.line_num = line_num
        self.suggestion = suggestion

        # Slots for dynamic enrichment (The Inquisitor fills these later)
        self.captured_output: Optional[str] = None
        self.gnostic_context: Optional[Dict] = None
        self.exception_object: Optional[Exception] = None

        super().__init__(self.get_proclamation())

    def get_proclamation(self) -> str:
        """
        Forges the luminous, human-readable scripture of the heresy.

        [THE FIX]: Markup Safe.
        """
        try:
            from rich.markup import escape
        except ImportError:
            escape = lambda s: s

        line_str = f"on line {self.line_num}: " if self.line_num is not None else ""
        base = f"[{self.threat_level.value}] {line_str}{escape(self.message)} - {escape(self.details)}"

        if self.suggestion:
            base += f"\n  Suggestion: {escape(self.suggestion)}"

        return base


class HeresyThreatLevel(Enum):
    """The Gnostic measure of a heresy's potential for cosmic disruption."""
    CRITICAL = "CRITICAL"  # Direct, catastrophic system/data modification.
    HIGH = "HIGH"  # Potential for privilege escalation or widespread data access.
    SUSPICIOUS = "SUSPICIOUS"  # Commands that obscure intent or manipulate the environment.