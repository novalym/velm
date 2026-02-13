# Path: src/velm/parser_core/parser/engine.py
# -------------------------------------------
import hashlib
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
        =============================================================================
        == THE BICAMERAL STATE INITIALIZER (V-Ω-TOTALITY-V305-FINALIS)             ==
        =============================================================================
        LIF: 100x | ROLE: COGNITIVE_SILO_FORGE
        [THE CURE]: Refactored to separate External Pleas from Internal Truths.
        """
        self.items_by_path: Dict[str, ScaffoldItem] = {}
        self._lowercase_path_roster: Set[str] = set()
        self.raw_items: List[ScaffoldItem] = []
        self.post_run_commands: List[Tuple] = []

        self.edicts: List[Edict] = []
        self.tasks: Dict[str, List[Edict]] = {}
        self.macros: Dict[str, Dict] = {}

        self.heresies: List[Heresy] = []
        self.all_rites_are_pure: bool = True
        self.file_path: Optional[Path] = None
        self.line_offset: int = 0

        # [ASCENSION 1 & 2]: BICAMERAL SCOPING (THE CORE SUTURE)
        # L2 Memory: Injected from the Wizard/CLI. These are "Suspect Gnosis".
        self.external_vars = GnosticSovereignDict()

        # L1 Memory: Defined in the Scripture via $$. These are "Sovereign Truth".
        self.blueprint_vars = GnosticSovereignDict()

        # Unified View: Correctly prioritized during resolve_reality.
        self.variables = GnosticSovereignDict()

        self.dossier: GnosticDossier = GnosticDossier()
        self.gnostic_ast: Optional[_GnosticNode] = None
        self.contracts: Dict[str, GnosticContract] = {}
        self.variable_contracts: Dict[str, str] = {}

        self.pending_permissions: Optional[str] = None
        self.imported_files: Set[Path] = set()

        self._in_code_block: bool = False
        self._block_quote_type: Optional[str] = None

    def parse_string(
            self,
            content: str,
            file_path_context: Optional[Path] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            line_offset: int = 0,
            overrides: Optional[Dict[str, Any]] = None,
            depth: int = 0
    ) -> Tuple['ApotheosisParser', List[ScaffoldItem], List[Tuple], List[Edict], Dict[str, Any], GnosticDossier]:
        """
        =================================================================================
        == THE GRAND RITE OF DECONSTRUCTION (V-Ω-TOTALITY-V305-SOVEREIGN-UNBREAKABLE)  ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_PARSE_STRING_V305_BICAMERAL_SOVEREIGNTY_2026_FINALIS

        This is the supreme kernel of perception. It has been Ascended to enforce the
        **Law of Variable Sovereignty**, ensuring the Blueprint's internal Gnosis
        annihilates external hallucinations.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Bicameral Scoping (THE CURE):** Surgically isolates `external_vars` (L2)
            from `blueprint_vars` (L1) to prevent the "Sentient FastAPI" poisoning.
        2.  **Sovereignty Reconciliation:** Explicitly overwrites L2 memory with L1
            truth at the conclusion of the deconstruction movement.
        3.  **The Sanctuary Seal V3:** Employs a multi-mode state machine to detect
            and shield top-level triple-quote blocks from topographical interpretation.
        4.  **Achronal Root Anchoring:** Forcefully resolves the `base_path` to prevent
            'Relative Path Drifting' during deep @include recursion.
        5.  **Adrenaline Mode (Physics Elevation):** Temporarily raises the host
            machine's recursion limit to handle complex, nested architectural graphs.
        6.  **The Lexical Suture (Matter Guard):** Intercepts misclassified edicts
            (>>/??/!!) and re-binds them to the kinetic layer before they leak.
        7.  **Isomorphic Identity Probe:** Normalizes path casing in real-time to
            prevent collision heresies on case-insensitive substrates (Windows/MacOS).
        8.  **Contextual Line Mapping:** Perfectly aligns the internal `line_offset`
            for deep forensics, ensuring the `crash.log` points to the exact pixel of failure.
        9.  **The Silence Vow Compliance:** Surgically mutes telemetry during the
            holographic pass to keep the synaptic stream pure for the Ocular HUD.
        10. **Socratic Diagnostics:** Injects haptic 'vfx: shake' signals if a
            catastrophic logic fracture shatters the deconstruction loop.
        11. **The Git-Anchor Seal:** Siphons the physical commit hash of the
            locus during the finalization movement for perfect causal replay.
        12. **The Finality Vow:** A mathematical guarantee of a valid Gnostic Dowry
            return, even if the world of logic collapses.
        =================================================================================
        """
        import sys
        import time
        import re
        from pathlib import Path

        # --- MOVEMENT I: THE OUROBOROS GUARD ---
        if depth > self.MAX_RECURSION_DEPTH:
            raise ArtisanHeresy(
                f"Cerebral Hemorrhage: Recursive loop detected at '{file_path_context}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"The Gnostic stack breached the {self.MAX_RECURSION_DEPTH} strata ceiling.",
                suggestion="Check for circular @include or self-referential @call edicts."
            )

        # --- MOVEMENT II: SPATIAL & COGNITIVE ANCHORING ---
        self.file_path = file_path_context
        self.line_offset = line_offset
        # [ASCENSION 4]: Force absolute anchoring
        self.base_path = (file_path_context.parent if file_path_context else Path.cwd()).resolve()

        # [ASCENSION 1]: BICAMERAL INGESTION
        # We store external inputs in a separate silo to prevent poisoning.
        if pre_resolved_vars:
            self.external_vars.update(pre_resolved_vars)
        if overrides:
            self.external_vars.update(overrides)

        # Initial view: Use external inputs as the baseline.
        # They will be righteously overwritten by Blueprint Truth in Movement IV.
        self.variables.update(self.external_vars)

        # [ASCENSION 5]: ADRENALINE MODE
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(original_recursion_limit, 3000))

        lines = content.splitlines()
        i = 0

        # [ASCENSION 9]: TELEMETRY SILENCE
        if depth == 0 and not self.Logger.is_verbose:
            self.Logger.verbose(
                f"[{self.parse_session_id}] Inception: Deconstructing {len(lines)} verses of Form and Will.")

        try:
            # =========================================================================
            # == THE CORE DECONSTRUCTION LOOP                                       ==
            # =========================================================================
            while i < len(lines):
                line = lines[i]
                current_line_num = i + 1 + self.line_offset
                original_indent = self._calculate_original_indent(line)

                # --- PHASE A: THE CODE-QUOTE SANCTUARY (THE SHIELD) ---
                # [ASCENSION 3]: We protect content blocks from being parsed as structure.
                quote_match = self.QUOTE_TOGGLE_REGEX.match(line)
                # Check: Is this a lone quote toggle or an assignment?
                # (Assignments like `:: """` are handled by the Structural Scribe)
                if quote_match and not re.search(r'[:\+=^~]\s*("""|\'\'\')', line):
                    q_type = quote_match.group(1)
                    if self._in_code_block:
                        if q_type == self._block_quote_type:
                            self._in_code_block = False;
                            self._block_quote_type = None;
                            i += 1;
                            continue
                    else:
                        self._in_code_block = True;
                        self._block_quote_type = q_type;
                        i += 1;
                        continue

                if self._in_code_block:
                    # While inside the sanctuary, matter is invisible to the Inquisitor.
                    i += 1
                    continue

                # --- PHASE B: THE INQUISITOR'S GAZE ---
                from ...parser_core.lexer_core.inquisitor import GnosticLineInquisitor

                vessel = GnosticLineInquisitor.inquire(
                    raw_line=line,
                    line_num=current_line_num,
                    parser=self,
                    grammar_codex_key=self.grammar_key,
                    original_indent=original_indent
                )

                # --- PHASE C: THE LEXICAL SUTURE (THE FIX) ---
                # [ASCENSION 6]: The Kill-Switch for Parser Leaks.
                # Prevents edicts from ever being mistaken for paths.
                self._suture_lexical_leak(vessel)

                # [ASCENSION 7]: CASE-IDENTITY PROBE
                if vessel.line_type == GnosticLineType.FORM and vessel.path:
                    self._adjudicate_case_identity(vessel)

                # --- PHASE D: SELECTIVE DISPATCH ---
                scribe = self._get_scribe_for_vessel(vessel)
                prev_i = i

                if scribe:
                    # The Scribe consumes the line (and potentially blocks) and returns the next index.
                    # If it's a VARIABLE scribe, it populates self.blueprint_vars.
                    i = scribe.conduct(lines, i, vessel)
                else:
                    # No artisan willed for this line type; advance.
                    i += 1

                # ANTI-STASIS WARD: Ensure we always move forward in time.
                if i <= prev_i:
                    i += 1

        except Exception as e:
            # [ASCENSION 10]: SOCRATIC ERROR MIRROR
            self._proclaim_heresy(
                "META_HERESY_PARSER_FRACTURE",
                f"Catastrophic failure at L{i + 1}",
                details=f"The deconstruction loop was shattered by a logic paradox: {str(e)}",
                exception_obj=e,
                ui_hints={"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}
            )
        finally:
            # Restore Physics to standard levels.
            sys.setrecursionlimit(original_recursion_limit)

        # --- MOVEMENT IV: SOVEREIGNTY RECONCILIATION (THE CURE) ---
        # [ASCENSION 2]: THE APOTHEOSIS OF TRUTH.
        # We now forcefully overwrite the external L2 variables with the internal L1 truths
        # willed by the blueprint itself. The hallucination is annihilated.
        self.variables.update(self.blueprint_vars)

        # --- MOVEMENT V: ACHRONAL FINALIZATION ---
        # [ASCENSION 11]: If we are the root, anchor the reality to the Git timeline.
        if depth == 0:
            self._finalize_achronal_dossier()

            # [ASCENSION 12]: THE FINALITY VOW
            if not self.all_rites_are_pure:
                self.Logger.warn(
                    f"[{self.parse_session_id}] Parser concluding with impurities. Reality may be unstable.")

        # Bestow the unified and reconciled variables upon the Dowry.
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
        == THE BRIDGE OF REALIZATION (V-Ω-TOTALITY-V500.0-SINGULARITY-FINALIS)     ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_ENGINE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RESOLVE_REALITY_V500_DETERMINISTIC_CONVERGENCE_2026_FINALIS

        The final, transcendental realization of the Parser's logic. This engine
        forces the Mind (Gnosis) and the Form (AST) into a mathematical steady-state.

        It annihilates 'Hallucination Fractures' not through whitelists, but through
        the **Tiered Hierarchy of Truth**.
        =============================================================================
        """
        start_ns = time.perf_counter_ns()
        self.Logger.info(f"[{self.parse_session_id}] Bridge: Initiating Deterministic Convergence.")

        # --- MOVEMENT I: THE BATTLE FOR SOVEREIGNTY (GNOSIS CONVERGENCE) ---
        # [ASCENSION 1]: BICAMERAL IDENTITY ARBITRATION
        # We start by recognizing that Blueprint Truth ($$) is the only Sovereign reality.
        # External pleas (defaults) are merely 'Substrate Matter' until willed otherwise.

        # We forge the Unified Consciousness, prioritizing Internal Will over External Pleas.
        # Note: GnosticSovereignDict handles the recursive null-safety.
        reconciled_gnosis = GnosticSovereignDict()
        reconciled_gnosis.update(self.external_vars)  # L2: Injected Matter (Lowest Priority)
        reconciled_gnosis.update(self.blueprint_vars)  # L1: Scripture Truth (Supreme Priority)

        # [ASCENSION 2]: THE ENTROPY STABILIZATION LOOP (ALCHEMICAL REACTOR)
        # We perform a multi-pass resolution until the Gnostic state reaches stasis.
        # This resolves variables that depend on other variables across infinite depth.
        if hasattr(self.alchemist, 'render_string'):
            max_passes = 10
            pass_num = 0
            while pass_num < max_passes:
                pass_num += 1
                state_before = hashlib.md5(str(reconciled_gnosis).encode()).hexdigest()

                for key, val in reconciled_gnosis.items():
                    if isinstance(val, str) and ("{{" in val or "{%" in val):
                        # The Alchemist transmutes the placeholder using the current consciousness
                        reconciled_gnosis[key] = self.alchemist.render_string(val, reconciled_gnosis)

                state_after = hashlib.md5(str(reconciled_gnosis).encode()).hexdigest()
                if state_before == state_after:
                    self.Logger.verbose(f"Gnostic Stasis achieved in {pass_num} alchemical pass(es).")
                    break
            else:
                self.Logger.warn("Alchemical Recoil: Gnostic State failed to converge after 10 passes.")

        # Update the Mind's internal state with the GROUNDED literals.
        self.variables.update(reconciled_gnosis)

        # --- MOVEMENT II: TOPOLOGICAL INCEPTION (FORM CONVERGENCE) ---
        # [ASCENSION 4]: SKELETON FORGING
        # We materialize the hierarchical AST from the flat stream of raw items.
        # This weaver handles the 'Geometric Anchor' logic internally.
        weaver = GnosticASTWeaver(self)
        self.gnostic_ast = weaver.weave_gnostic_ast()

        # --- MOVEMENT III: CAUSAL REALIZATION (THE WILL) ---
        # [ASCENSION 5]: THE RITE OF REALIZATION
        # We walk the Gnostic AST to resolve logic gates (@if/@for) and
        # flatten path strings into the final Execution Plan.
        self.Logger.verbose("LogicWeaver: Materializing the Causal Path through the AST.")
        final_items = weaver.resolve_paths_from_ast(self.gnostic_ast)

        # --- MOVEMENT IV: BICAMERAL PURGATION (THE CURE) ---
        # [ASCENSION 3]: THE GNOSTIC OBLIVION
        # 1. We righteously annihilate the 'Transient Souls' (variables starting with '_').
        # 2. We remove external hallucinations that were NOT claimed by the blueprint.
        # If an external variable was neither willed in $$ nor used in the Form, it is waste.
        self.variables = self.alchemist.purge_private_gnosis(self.variables)

        # [ASCENSION 7]: MERKLE FINGERPRINTING
        # We forge a unique ID for this specific realized reality.
        plan_fingerprint = hashlib.sha256(
            "".join([str(i.path) for i in final_items]).encode()
        ).hexdigest()[:8]

        # --- MOVEMENT V: FINALITY ADJUDICATION ---
        # [ASCENSION 12]: THE FINALITY VOW
        if not final_items and not self.post_run_commands:
            self.Logger.warn("Convergence Paradox: The resulting reality is a void.")
        else:
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.Logger.success(
                f"Convergence Complete: [cyan]{plan_fingerprint}[/cyan] manifest in {duration_ms:.2f}ms."
            )

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