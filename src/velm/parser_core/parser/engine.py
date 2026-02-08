# Path: src/velm/parser_core/parser/engine.py
# -------------------------------------------


import re
import logging
import uuid
import time
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union, Set, Final

# --- THE DIVINE SUMMONS OF GNOSTIC SUBSTRATES ---
from .ast_weaver import GnosticASTWeaver
from .parser_scribes import SCRIBE_PANTHEON, FormScribe
from ..block_consumer import GnosticBlockConsumer

# --- CONTRACTS & VESSELS ---
from ...contracts.data_contracts import (
    ScaffoldItem, GnosticVessel, GnosticDossier, GnosticLineType, _GnosticNode, GnosticContract
)
from ...contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ...contracts.symphony_contracts import Edict, EdictType
from ...core.alchemist import get_alchemist
from ...logger import Scribe
from ...core.runtime.vessels import GnosticSovereignDict
from ...jurisprudence_core.gnostic_type_system import GnosticTypeParser
from ...utils import get_git_commit

Logger = Scribe("ApotheosisParser")


class ApotheosisParser:
    """
    =================================================================================
    == THE APOTHEOSIS PARSER (V-Ω-TOTALITY-V302-ETERNAL-GUARDIAN)                  ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN

    The God-Engine of Perception. It transmutes raw text into Gnostic Truth.
    Ascended to V302 to annihilate the "Parser Leak" heresy via the Law of Lexical Hierarchy
    and the Code-Quote Sanctuary.
    """

    # [ASCENSION 1]: THE DEPTH GOVERNOR
    # 25 levels of recursion is the absolute ceiling of architectural sanity.
    MAX_RECURSION_DEPTH: Final[int] = 25

    # [ASCENSION 5]: THE GEOMETRIC LAW
    # Defines the standard indentation unit (4 spaces or 1 tab).
    TAB_WIDTH: Final[int] = 4

    # [ASCENSION 6]: CODE-QUOTE SANCTUARY PATTERN
    # Detects the toggle of a triple-quoted block to prevent parser leaks inside content.
    QUOTE_TOGGLE_REGEX: Final[re.Pattern] = re.compile(r'^\s*("""|\'\'\')')

    def __init__(self, grammar_key: str = 'scaffold'):
        """[ELEVATION 1] The Gnostic Triage of Tongues."""
        if grammar_key not in SCRIBE_PANTHEON:
            raise ArtisanHeresy(f"Unknown Grammar Key: {grammar_key}")

        self.grammar_key = grammar_key
        # [ASCENSION 6]: Nanosecond Session Identity
        self.parse_session_id = f"{uuid.uuid4().hex[:6].upper()}-{time.time_ns()}"
        self.Logger = Logger

        # Initialize the Mind
        self._reset_parser_state()

        # JIT Materialization of the Scribe Pantheon
        self.scribes: Dict[str, FormScribe] = self._forge_scribe_pantheon()
        self.alchemist = get_alchemist()

    def _reset_parser_state(self):
        """
        [ASCENSION 8]: ATOMIC STATE PURGE V2.
        Returns the mind to a state of Tabula Rasa. Explicitly clears complex objects
        to ensure no ghost data lingers between rites.
        """
        self.items_by_path: Dict[str, ScaffoldItem] = {}
        # [ASCENSION 3]: Case-Identity Registry
        self._lowercase_path_roster: Set[str] = set()

        self.raw_items: List[ScaffoldItem] = []
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        self.edicts: List[Edict] = []
        self.tasks: Dict[str, List[Edict]] = {}
        self.macros: Dict[str, Dict[str, Any]] = {}

        self.heresies: List[Heresy] = []
        self.all_rites_are_pure: bool = True
        self.file_path: Optional[Path] = None
        self.line_offset: int = 0

        # [ASCENSION 2]: BICAMERAL SCOPING (NULL-SAFE)
        self.variables = GnosticSovereignDict()
        self.blueprint_vars = GnosticSovereignDict()

        self.dossier: GnosticDossier = GnosticDossier()
        self.gnostic_ast: Optional[_GnosticNode] = None
        self.contracts: Dict[str, GnosticContract] = {}
        self.variable_contracts: Dict[str, str] = {}

        self.pending_permissions: Optional[str] = None
        self.imported_files: Set[Path] = set()

        # Staging for multi-line block modifiers
        self.pending_undo_block: Optional[List[str]] = None
        self.pending_heresy_block: Optional[List[str]] = None

        # [ASCENSION 6]: Sanctuary State
        self._in_code_block: bool = False
        self._block_quote_type: Optional[str] = None

    def parse_string(
            self,
            content: str,
            file_path_context: Optional[Path] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            line_offset: int = 0,
            overrides: Optional[Dict[str, Any]] = None,
            depth: int = 0  # [ASCENSION 1]: Recursive Depth Tracking
    ) -> Tuple['ApotheosisParser', List[ScaffoldItem], List[Tuple], List[Edict], Dict[str, Any], GnosticDossier]:
        """
        =================================================================================
        == THE GRAND RITE OF DECONSTRUCTION (CANCELLABLE & WARDED)                     ==
        =================================================================================
        LIF: ∞ | The Core loop where Intent becomes Matter.
        """
        # --- 1. OUROBOROS DEPTH GUARD ---
        if depth > self.MAX_RECURSION_DEPTH:
            raise ArtisanHeresy(
                f"Cerebral Hemorrhage: Recursive loop detected at '{file_path_context}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"The Gnostic stack breached Stratum {self.MAX_RECURSION_DEPTH}.",
                suggestion="Identify the circular @include or @call directive and sever the loop."
            )

        # --- 2. CONTEXTUAL ANCHORING ---
        self.file_path = file_path_context
        self.line_offset = line_offset
        self.base_path = file_path_context.parent if file_path_context else Path.cwd()

        # Ingest External Gnosis into the Sarcophagus
        if pre_resolved_vars: self.variables.update(pre_resolved_vars)
        if overrides: self.variables.update(overrides)

        # [ASCENSION 4]: RUNTIME RECURSION CACHE
        # We temporarily elevate the Python recursion limit to handle deep structures safely.
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(original_recursion_limit, 2000))

        lines = content.splitlines()
        i = 0

        # [ASCENSION 2]: VARIABLE RESOLUTION LOGGING
        if depth == 0:
            Logger.debug(
                f"[{self.parse_session_id}] Ingesting {len(lines)} lines. Active Keys: {list(self.variables.keys())[:5]}...")

        try:
            while i < len(lines):
                line = lines[i]
                current_line_num = i + 1 + self.line_offset
                original_indent = self._calculate_original_indent(line)

                # --- MOVEMENT I: THE CODE-QUOTE SANCTUARY (ASCENSION 6) ---
                # Detect the toggle of a triple-quoted block to prevent parser leaks
                # if indentation logic fails inside a content block.
                quote_match = self.QUOTE_TOGGLE_REGEX.match(line)

                # IMPORTANT: We only engage sanctuary if this isn't an assignment (:: """)
                # because assignments are handled by the StructuralScribe's block consumer.
                # This sanctuary is for top-level or orphaned docstrings.
                if quote_match and not re.match(r'.*[:\+=^~]\s*("""|\'\'\')', line):
                    quote_type = quote_match.group(1)
                    if self._in_code_block:
                        if quote_type == self._block_quote_type:
                            self._in_code_block = False
                            self._block_quote_type = None
                            # We treat the closing line as a comment/void
                            i += 1
                            continue
                    else:
                        self._in_code_block = True
                        self._block_quote_type = quote_type
                        # We treat the opening line as a comment/void
                        i += 1
                        continue

                if self._in_code_block:
                    # While in sanctuary, the line is shielded from interpretation.
                    i += 1
                    continue

                # --- MOVEMENT II: THE INQUISITOR'S GAZE ---
                from ...parser_core.lexer_core.inquisitor import GnosticLineInquisitor

                # [ASCENSION 8]: CONTEXTUAL LINE OFFSET PASSED
                vessel = GnosticLineInquisitor.inquire(
                    raw_line=line,
                    line_num=current_line_num,
                    parser=self,
                    grammar_codex_key=self.grammar_key,
                    original_indent=original_indent
                )

                # --- MOVEMENT III: THE LEXICAL SUTURE (THE FIX) ---
                # The Kill Switch for Parser Leaks.
                self._suture_lexical_leak(vessel)

                # [ASCENSION 3]: CASE-IDENTITY PROBE
                if vessel.line_type == GnosticLineType.FORM and vessel.path:
                    self._adjudicate_case_identity(vessel)

                # --- MOVEMENT IV: SELECTIVE DISPATCH TO SCRIBE ---
                scribe = self._get_scribe_for_vessel(vessel)
                prev_i = i

                if scribe:
                    # Scribe consumes logic and returns the next line index
                    i = scribe.conduct(lines, i, vessel)
                else:
                    # No scribe found (VOID or Unknown), advance manually
                    i += 1

                # ANTI-STASIS WARD: Ensure we always move forward
                if i <= prev_i:
                    i += 1

        except Exception as e:
            # [ASCENSION 3]: HAPTIC FEEDBACK FOR HERESY
            # We inject 'vfx': 'shake' to signal the UI of a critical parsing fracture.
            self._proclaim_heresy(
                "META_HERESY_PARSER_FRACTURE",
                f"Catastrophic failure at L{i + 1}",
                details=f"The Parser soul was shattered by an unhandled paradox: {e}",
                exception_obj=e,
                ui_hints={"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}
            )
        finally:
            # Restore Physics
            sys.setrecursionlimit(original_recursion_limit)

        # --- 3. [ASCENSION 4]: ACHRONAL SYNC-HOOK (GIT ANCHOR) ---
        # If this is the root parse (depth 0), we anchor the dossier to the Git state.
        if depth == 0:
            self._finalize_achronal_dossier()

            # [ASCENSION 7]: FINALITY VOW CHECK
            if not self.all_rites_are_pure:
                Logger.warn(
                    f"[{self.parse_session_id}] Parser concluding with impurities. Heresies perceived: {len(self.heresies)}")

        all_gnosis = {**self.blueprint_vars, **self.variables}
        return (self, self.raw_items, self.post_run_commands, self.edicts, all_gnosis, self.dossier)

    def _suture_lexical_leak(self, vessel: GnosticVessel):
        """
        =============================================================================
        == THE LEXICAL SUTURE (V-Ω-THE-KILL-SWITCH)                                ==
        =============================================================================
        Intervenes when the Inquisitor misclassifies a Kinetic Edict as a Form Item.
        This annihilates the 'Profane characters in path' heresy for lines like
        '>> poetry install' or '?? file_exists'.

        It enforces the LAW OF LEXICAL HIERARCHY: Command Sigils override Path Geometry.
        """
        if vessel.line_type == GnosticLineType.FORM:
            raw_stripped = vessel.raw_scripture.strip()

            # THE LAW OF HIERARCHY: Sigils override Form.
            if raw_stripped.startswith(('>>', '??', '!!', '%%')):
                # It is a Post-Run Edict (or Vow/State), NOT a file path.
                # We forcefully reclassify it to prevent it from entering the StructuralScribe.
                # 'POST_RUN' is the safest bucket for generic command-like lines in the Scaffold grammar.
                vessel.line_type = GnosticLineType.POST_RUN
                # We clear attributes that might confuse downstream logic
                vessel.path = None
                vessel.is_dir = False

            elif raw_stripped.startswith('@'):
                # It is a Logic Directive, NOT a file path.
                vessel.line_type = GnosticLineType.LOGIC
                vessel.directive_type = raw_stripped.split()[0][1:]
                vessel.path = None
                vessel.is_dir = False

    # =============================================================================
    # == II. THE SCRIBE PANTHEON (SKILL MATERIALIZATION)                         ==
    # =============================================================================

    def _forge_scribe_pantheon(self) -> Dict[str, FormScribe]:
        """
        =================================================================================
        == THE GOD-ENGINE OF SCRIBE FORGING (V-Ω-ETERNALLY-PURIFIED)                   ==
        =================================================================================
        [ASCENSION 7]: JIT Scribe Awakening.
        Instantiates only the artisans willed by the active grammar grimoire.
        """
        from .parser_scribes import SCRIBE_PANTHEON, FormScribe

        pantheon: Dict[str, FormScribe] = {}
        grimoire = SCRIBE_PANTHEON.get(self.grammar_key)

        if not grimoire:
            raise ArtisanHeresy(f"META-HERESY: The Grimoire holds no Gnosis for '{self.grammar_key}'.")

        # We extract unique classes to avoid redundant instantiation
        unique_scribes = set(grimoire.values())

        for ScribeClass in unique_scribes:
            if not issubclass(ScribeClass, FormScribe): continue

            # [THE RITE OF PURE CONSECRATION]
            # Each scribe is born with a telepathic link back to the Master Parser.
            instance_key = ScribeClass.__name__.lower()
            try:
                pantheon[instance_key] = ScribeClass(self)
            except Exception as e:
                Logger.error(f"Paradox forging '{ScribeClass.__name__}': {e}")
                raise

        return pantheon

    def _get_scribe_for_vessel(self, vessel: GnosticVessel) -> Optional[FormScribe]:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC TRIAGE (V-Ω-ETERNAL-APOTHEOSIS)                   ==
        =================================================================================
        LIF: 100x | ROLE: DISPATCH_CONDUCTOR

        Annihilates the 'if/elif' heresy. Performs a single O(1) Gaze into the
        Grimoire to find the specialized artisan for the current line.
        """
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID:
            return None

        # 1. Scry the specific Grammar Map
        from .parser_scribes import SCRIBE_PANTHEON
        scribe_map = SCRIBE_PANTHEON.get(self.grammar_key, {})

        # 2. Triage the Intent (Dual Gaze for Symphony, Singular for Scaffold)
        ScribeClass = None
        if self.grammar_key == 'symphony':
            # Seek the Edict's soul first, then fallback to general LineType (Comments)
            ScribeClass = scribe_map.get(vessel.edict_type) or scribe_map.get(vessel.line_type)
        else:
            ScribeClass = scribe_map.get(vessel.line_type)

        if ScribeClass:
            return self.scribes.get(ScribeClass.__name__.lower())

        # 3. [THE FINALITY WARNING]
        self.Logger.warn(f"L{vessel.line_num}: No Scribe consecrated for {vessel.line_type.name}")
        return None

    # =============================================================================
    # == III. THE LAWS OF GEOMETRY (CASE-IDENTITY & HIERARCHY)                   ==
    # =============================================================================

    def _adjudicate_case_identity(self, vessel: GnosticVessel):
        """
        =============================================================================
        == THE CASE-IDENTITY SENTINEL (V-Ω-TOTALITY)                               ==
        =============================================================================
        [ASCENSION 3]: The Windows/Linux Schism Fix.
        Scries sibling paths to prevent case-insensitive collisions.
        """
        if not vessel.path: return

        path_posix = vessel.path.as_posix()
        path_lower = path_posix.lower()

        # Check if a sibling already exists with different casing
        if path_lower in self._lowercase_path_roster:
            # We must find the original casing for the Heresy Proclamation
            for existing in self.items_by_path.keys():
                if existing.lower() == path_lower and existing != path_posix:
                    self._proclaim_heresy(
                        "AMBIGUOUS_IDENTITY_HERESY",
                        vessel,
                        severity=HeresySeverity.CRITICAL,
                        details=f"Identity Collision: '{path_posix}' conflicts with '{existing}' in case-insensitive environments.",
                        suggestion="Unify the casing of your scriptures to ensure stability on Windows/MacOS."
                    )
                    return

        self._lowercase_path_roster.add(path_lower)

    def _proclaim_final_item(self, vessel: GnosticVessel):
        """Materializes a Gnostic Vessel into a persistent ScaffoldItem."""
        if not vessel.is_valid or vessel.line_type == GnosticLineType.VOID:
            return

        item = ScaffoldItem.model_validate(vessel.model_dump())

        # Suture pending permissions from previous % commands
        if self.pending_permissions:
            item.permissions = self.pending_permissions
            self.pending_permissions = None

        # Logic and Jinja blocks are appended to the raw stream
        if item.line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT, GnosticLineType.POST_RUN,
                              GnosticLineType.VARIABLE, GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
            self.raw_items.append(item)
            return

        # Form items are mapped for O(1) dependency scrying
        if item.line_type == GnosticLineType.FORM and item.path:
            self.items_by_path[item.path.as_posix()] = item

        self.raw_items.append(item)

    # =============================================================================
    # == IV. THE ADJUDICATION OF STATE (VARIABLES & CONTRACTS)                   ==
    # =============================================================================

    def _adjudicate_contracts(self, all_gnosis: Dict[str, Any]):
        """
        Validates the manifest variables against the Gnostic Contracts (Types).
        [ASCENSION 2]: Bicameral Aware - Ignores private souls during global validation.
        """
        for var_name, type_sig in self.variable_contracts.items():
            # Skip if the variable is a template or unmanifest
            if var_name not in all_gnosis: continue

            value = all_gnosis[var_name]
            if isinstance(value, str) and ("{{" in value or "{%" in value):
                continue

            try:
                # [ASCENSION 2]: Scoped Validation
                # We do not enforce strict contracts on private '_' variables
                # unless explicitly willed.
                if var_name.startswith("_"):
                    continue

                gnostic_type = GnosticTypeParser.parse(type_sig)
                gnostic_type.validate(value, f"$$ {var_name}", self.contracts)
            except ValueError as e:
                self._proclaim_heresy(
                    "CONTRACT_VIOLATION",
                    f"$$ {var_name}",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Value: {value}\nContract: {type_sig}\nError: {str(e)}"
                )

    # =============================================================================
    # == V. THE ACHRONAL FINALIZER & FORENSIC SCRIBING                         ==
    # =============================================================================

    def _finalize_achronal_dossier(self):
        """
        =============================================================================
        == THE ACHRONAL SYNC-HOOK (V-Ω-TEMPORAL-ANCHOR)                            ==
        =============================================================================
        [ASCENSION 4]: Siphons the physical Git state into the Dossier.
        This allows the Crystal Mind (DB) to detect if the Architect has performed
        a 'git checkout' outside the UI, triggering a re-scan.
        """
        # 1. Scry the physical Git reality
        current_git_head = get_git_commit(self.base_path) or "VOID_REALITY"

        # 2. Finalize the Dossier Intelligence
        # We perform a deep-scan for variables that were willed but never used.
        from ...utils.gnosis_discovery import discover_required_gnosis

        self.dossier = discover_required_gnosis(
            execution_plan=self.raw_items,
            post_run_commands=self.post_run_commands,
            blueprint_vars={**self.blueprint_vars, **self.variables}
        )

        # 3. Anchor the Metadata
        self.dossier.metadata = {
            "git_head_anchor": current_git_head,
            "parse_session": self.parse_session_id,
            "achronal_status": "STABLE" if self.all_rites_are_pure else "FRACTURED",
            "bicameral_mode": "ACTIVE"
        }

    def _calculate_original_indent(self, line: str) -> int:
        """[ASCENSION 5]: The Geometric Auditor. Measures visual depth."""
        consumer = GnosticBlockConsumer([])
        return consumer._measure_visual_depth(line)

    def _proclaim_heresy(self, key: str, item: Union[GnosticVessel, ScaffoldItem, str], **kwargs):
        """
        =============================================================================
        == THE UNIVERSAL HERESY PROCLAMATION (V-Ω-TOTALITY)                        ==
        =============================================================================
        [ASCENSION 10]: The absolute gateway to the Jurisprudence system.
        [ASCENSION 3]: Now accepts UI hints (Haptic Feedback) via kwargs.
        """
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel

        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', 0) or self.line_offset

        # Forge the Socratic vessel
        heresy = forge_heresy_vessel(
            key=key,
            line_num=line_num,
            line_content=raw_scripture,
            details=kwargs.get('details')
        )

        # Apply overrides from the Artisan
        if severity := kwargs.get('severity'): heresy.severity = severity
        if suggestion := kwargs.get('suggestion'): heresy.suggestion = suggestion

        # [ASCENSION 3]: HAPTIC FEEDBACK INJECTION
        # We broadcast the Haptic signal if present
        if ui_hints := kwargs.get('ui_hints'):
            # Ideally, we would attach this to the Heresy object if it supported it.
            # For now, we log a special tag for the Middleware to pick up.
            Logger.debug(f"[UI_SIGNAL:{ui_hints.get('vfx')}] {heresy.message}")

        self.heresies.append(heresy)

        # If the heresy is Critical, the entire materialization path is warded.
        if heresy.severity == HeresySeverity.CRITICAL:
            if hasattr(item, 'is_valid'): item.is_valid = False
            self.all_rites_are_pure = False

    # =============================================================================
    # == VI. THE BRIDGE OF REALIZATION (CONVERGENCE)                             ==
    # =============================================================================

    def resolve_reality(self) -> List[ScaffoldItem]:
        """
        =============================================================================
        == THE BRIDGE OF REALIZATION (V-Ω-TOTALITY-V200.0-SINGULARITY-FINALIS)     ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_ENGINE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RESOLVE_REALITY_V300_RECURSIVE_FINALIS

        The final, alien-like realization of the Parser's logic. It forces the Mind
        and the Form to reach a mathematical steady-state before materialization.
        Annihilates 'Geometric Paradoxes' and 'Ghost Variables'.
        =============================================================================
        """
        self.Logger.info(f"[{self.parse_session_id}] Bridge: Initiating Convergence Sequence.")

        # --- MOVEMENT I: DNA STABILIZATION (THE MIND) ---
        # [ASCENSION 2]: BICAMERAL SCOPING (PRIVATE VS PUBLIC)
        # We merge variables, but the Alchemist's Reactor will respect the '_' boundary.
        merged_gnosis = GnosticSovereignDict({**self.variables, **self.blueprint_vars})

        # [RECURSIVE CONVERGENCE REACTOR]
        # We command the Alchemist to perform the multi-pass resolution pass.
        # This resolves variables that depend on other variables.
        if hasattr(self.alchemist, 'render_string'):
            self.Logger.verbose("Alchemist: Initiating Recursive Convergence Loop.")
            # We treat the entire variable map as a single Gnostic Graph
            for key, val in merged_gnosis.items():
                if isinstance(val, str) and "{{" in val:
                    merged_gnosis[key] = self.alchemist.render_string(val, merged_gnosis)

            # [ASCENSION 3]: L1 MEMORY SYNCHRONIZATION
            # Update the Mind's internal state with the GROUNDED literals.
            self.variables.update(merged_gnosis)

        # --- MOVEMENT II: SKELETON FORGING (THE FORM) ---
        # [ASCENSION 4]: Materialize the hierarchical AST.
        weaver = GnosticASTWeaver(self)
        self.gnostic_ast = weaver.weave_gnostic_ast()

        # --- MOVEMENT III: REALITY MAPPING (THE WILL) ---
        # [ASCENSION 5]: THE RITE OF REALIZATION.
        # Resolves logic gates (@if/@for) and flattens path strings into a Final Plan.
        self.Logger.verbose("LogicWeaver: Walking Gnostic AST to materialize Causal Path.")
        final_items = weaver.resolve_paths_from_ast(self.gnostic_ast)

        # --- MOVEMENT IV: BICAMERAL PURGE (THE CURE) ---
        # [ASCENSION 3]: We righteously annihilate the Transient Souls.
        # Variables starting with '_' are deleted from the final variable context
        # before it is sent to the Materializer, preventing scope-leakage.
        self.variables = self.alchemist.purge_private_gnosis(self.variables)

        # --- MOVEMENT V: FINALITY ADJUDICATION ---
        # [ASCENSION 12]: THE FINALITY VOW.
        if not final_items and not self.post_run_commands:
            self.Logger.warn("Convergence Warning: The resulting reality is a void. No form or will perceived.")

        return final_items

    # --- HELPER: BLOCK CONSUMPTION BRIDGE ---
    # Needed for Scribes to consume blocks while respecting parser state
    def _consume_indented_block_with_context(self, lines: List[str], i: int, parent_indent: int) -> Tuple[
        List[str], int]:
        consumer = GnosticBlockConsumer(lines)
        return consumer.consume_indented_block(i, parent_indent)


# =============================================================================
# == VII. THE ALCHEMICAL SINGLETON                                           ==
# =============================================================================

_parser_instance = None


def get_parser(grammar: str = "scaffold") -> ApotheosisParser:
    """Summons a persistent, shared instance of the High Priest."""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = ApotheosisParser(grammar_key=grammar)
    return _parser_instance

# == SCRIPTURE SEALED: THE APOTHEOSIS PARSER HAS ACHIEVED SINGULARITY ==