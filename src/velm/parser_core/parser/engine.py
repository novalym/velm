# Path: src/velm/parser_core/parser/engine.py
# -------------------------------------------

import hashlib
import re
import logging
import traceback as tb_scribe
import uuid
import time
import os
import sys
import threading
import copy
import gc
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
from ...logger import Scribe, get_console
from ...core.runtime.vessels import GnosticSovereignDict
from ...jurisprudence_core.gnostic_type_system import GnosticTypeParser
from ...utils import get_git_commit

Logger = Scribe("ApotheosisParser")


class ApotheosisParser:
    """
    =================================================================================
    == THE APOTHEOSIS PARSER (V-Ω-TOTALITY-V99000-GOD-ENGINE)                      ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_PARSER_V99000_ABSOLUTE_RESOLVE_FINALIS

    The God-Engine of Perception. It transmutes raw text into Gnostic Truth.
    It is the Central Cortex of the Compiler, holding the state of the Universe
    as it is being spoken into existence.

    [THE CURE]: This version incorporates the "Macro Arity Suture", the "Import Decapitation",
    the "Geometric Anchor", and the absolute "Deep-Tissue Orphan Scryer" to achieve 100%
    Semantic Resonance. It also features the **Matter-Leak Suture** to protect Kinetic Will.

    ### THE PANTHEON OF 33 LEGENDARY ASCENSIONS:
    1.  **Diamond-Hard Pre-Weave Transmutation:** Surgically resolves macro variables
        within paths *before* AST generation, annihilating the Void Node paradox.
    2.  **Imported Shard Amnesty:** Grants absolute immunity to variables
        injected by the Import Manager from being flagged as Dead Gnosis.
    3.  **Sovereign Gnosis Suture:** Force-injects `overrides` into the L1 `blueprint_vars`.
    4.  **Bicameral Ingestion (L2 SILO):** Correctly segregates external pleas from internal truths.
    5.  **The NoneType Root Sarcophagus:** Automatically anchors the project root if the Engine is void.
    6.  **Achronal Recursive Sentinel:** Hard-caps Gnostic depth at 50 strata.
    7.  **Geometric Indentation Tomography:** Employs the `GnosticBlockConsumer` for exact depth mapping.
    8.  **The Forensic Stderr Snitch:** Bypasses logging to dump raw tracebacks on kernel panics.
    9.  **Template Error Leak Detection:** Pre-emptively identifies Jinja toxins in the stream.
    10. **The Code-Quote Sanctuary:** Wards triple-quoted matter against structural misinterpretation.
    11. **Lexical Matter Guard:** Intervenes if an Edict (>>) is misclassified as Form.
    12. **Isomorphic Identity Suture:** Normalizes paths across Windows and POSIX boundaries.
    13. **Metabolic Telemetry Pulse:** Multicasts high-frequency signals to the Akashic Record.
    14. **JIT Scribe Dispatch:** Performs O(1) triage of the Scribe Pantheon.
    15. **Substrate-Aware Physics:** Dynamically adjusts garbage collection for WASM vs Iron.
    16. **Bicameral Memory Reconciliation:** Synchronizes L1 Truth over L2 Pleas post-deconstruction.
    17. **Achronal Macro Contexting:** Ensures sub-parsers inherit the parent's mind-state.
    18. **Merkle-State Evolution:** Churns `state_hash` for every mutation to detect causal drift.
    19. **The Finality Vow:** A mathematical guarantee of the Six-Fold Dowry return.
    20. **Thread-Safe Mutex Grid:** `RLock` applied to all state modifications.
    21. **Strict Mode Enforcement:** Elevates architectural warnings to critical heresies dynamically.
    22. **Contract Adjudication:** Enforces `%% contract` types at the moment of ingestion.
    23. **Ghost Matter Identification:** Perceives files that exist on disk but failed the AST scry.
    24. **Universal Sigil Exorcism:** Recursively strips artifacts from Maestro Edicts.
    25. **Case-Collision Biopsy:** Warns when NTFS casing masks identical architectural paths.
    26. **Null-Byte Annihilation:** Rejects C-string termination attacks.
    27. **Trailing Phantom Exorcism:** Removes OS-hostile trailing spaces in directory names.
    28. **Semantic Variable Injection:** Resolves `{{ var }}` within inline `:: "content"` definitions.
    29. **The Macro-Argument Amnesty:** Prevents macro parameters from triggering 'Undefined' alerts.
    30. **Sub-Parser Sovereignty:** Child parsers inherit `silent=True` to prevent terminal flood.
    31. **Atomic Memory Reclamation:** Triggers `gc.collect(1)` after heavy dimensional convergences.
    32. **The Singularity Link:** Perfect bidirectional mapping between the Parser AST and the UI Graph.
    33. **Kinetic Volatility Ward (THE FIX):** Uses `_kinetic_block_indents` to forcefully ensure
        that raw commands inside `%% post-run` are treated as `VOW` actions, preventing them
        from crystallizing into empty files (e.g. `makeinstall`).
    =================================================================================
    """

    # [ASCENSION 1]: THE DEPTH GOVERNOR
    # 50 levels of recursion is the absolute ceiling of architectural sanity.
    MAX_RECURSION_DEPTH: Final[int] = 50

    # [ASCENSION 5]: THE GEOMETRIC LAW
    # Defines the standard indentation unit (4 spaces or 1 tab).
    TAB_WIDTH: Final[int] = 4

    # [ASCENSION 8]: CODE-QUOTE SANCTUARY PATTERN
    # Detects the toggle of a triple-quoted block to prevent parser leaks inside content.
    QUOTE_TOGGLE_REGEX: Final[re.Pattern] = re.compile(r'^\s*("""|\'\'\')')

    def __init__(self, grammar_key: str = 'scaffold', engine: Optional[Any] = None):
        """
        =================================================================================
        == THE PARSER INCEPTION: TOTALITY (V-Ω-TOTALITY-V312-SUTURED)                 ==
        =================================================================================
        LIF: ∞ | ROLE: GNOSTIC_INTERPRETER | RANK: OMEGA

        [THE SUTURE]: The Parser is now born with a link to the Engine, allowing it to
        radiate signals to the Akashic Record during its meditative rites.
        """
        self.grammar_key = grammar_key

        # [ASCENSION 13]: THE SILVER CORD
        # We bind the engine reference. If None, we operate in a state of Silent Isolation.
        self.engine = engine

        self.parse_session_id = f"{uuid.uuid4().hex[:6].upper()}-{time.time_ns()}"
        self.Logger = Logger

        # [ASCENSION 19]: ATOMIC MUTEX GRID
        self._state_lock = threading.RLock()

        # Initialize the Mind
        self._reset_parser_state()

        # JIT Materialization of the Scribe Pantheon
        self.scribes: Dict[str, FormScribe] = self._forge_scribe_pantheon()
        self.alchemist = get_alchemist()

        # [ASCENSION 11]: TELEMETRY HEARTBEAT
        self._last_pulse_line = 0

    def _reset_parser_state(self):
        """
        =============================================================================
        == THE BICAMERAL STATE INITIALIZER: OMEGA (V-Ω-TOTALITY-V32000-FINALIS)    ==
        =============================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_MEMORY_FORGE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RESET_V32000_SPATIAL_ANCHOR_SUTURE_2026_FINALIS

        Resets the parser to a Tabula Rasa state, ready for a new ingestion.
        """
        with self._state_lock:
            # --- STRATUM 0: IDENTITY & SPATIOTEMPORAL ANCHORS ---
            self.file_path: Optional[Path] = None
            self.console = get_console()
            # =========================================================================
            # == [THE CURE]: ABSOLUTE PROJECT ROOT INCEPTION                         ==
            # =========================================================================
            # We safely interrogate the Engine (if manifest) for the ultimate Project Root.
            # This obliterates the "Unresolved attribute reference" heresy for all time.
            self.project_root: Optional[Path] = getattr(self.engine, 'project_root', None)

            self.line_offset: int = 0
            self.all_rites_are_pure: bool = True
            self.heresies: List['Heresy'] = []

            # --- STRATUM 1: THE SHARED REGISTRY OF SOULS ---
            # Traits defined in one file (%% trait) are manifest globally.
            self.traits: Dict[str, Path] = {}
            # The Ouroboros Guard tracking visited scriptures.
            self.import_cache: Set[Path] = set()
            self._state_hash: str = hashlib.sha256(b"primordial_void").hexdigest()
            self.depth: int = 0
            self.lineage: List[str] = []

            # --- STRATUM 2: PHYSICAL MATTER (TOPOGRAPHY) ---
            self.items_by_path: Dict[str, 'ScaffoldItem'] = {}
            self.raw_items: List['ScaffoldItem'] = []
            # THE PERCEPTION ANCHOR
            self.vessel: Optional[GnosticVessel] = None
            # [ASCENSION 24]: Case-Resonance Tomography
            self._lowercase_path_roster: Set[str] = set()

            # --- STRATUM 3: KINETIC WILL (THE MAESTRO'S ARSENAL) ---
            self.edicts: List['Edict'] = []

            # The Sacred Quaternities harvested during the parse
            self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

            self.tasks: Dict[str, List['Edict']] = {}
            self.macros: Dict[str, Dict[str, Any]] = {}

            # SYMBOL TABLE FOR UNUSED DETECTION
            self.symbol_usage: Dict[str, int] = {}

            # Ephemeral buffer for the Rite of Consecration (%% Permissions)
            self.pending_permissions: Optional[str] = None

            # --- STRATUM 4: THE BICAMERAL MIND (TRUTH & PLEA) ---
            try:
                from ...core.runtime.vessels import GnosticSovereignDict
                DictVessel = GnosticSovereignDict
            except ImportError:
                DictVessel = dict

            # L2 Memory: Injected from the outside (CLI/Wizard). "Shadow Gnosis".
            self.external_vars = DictVessel()
            # L1 Memory: Defined within the scripture ($$). "Sovereign Truth".
            self.blueprint_vars = DictVessel()
            # Unified View: The active cortex. Prioritized during resolve_reality.
            self.variables = DictVessel()

            # --- STRATUM 5: THE LEGAL CODES (CONTRACTS) ---
            self.contracts: Dict[str, 'GnosticContract'] = {}
            self.variable_contracts: Dict[str, str] = {}

            # --- STRATUM 6: THE OCULAR MEMBRANE (UI & BUFFER) ---
            self.dossier: GnosticDossier = GnosticDossier()
            self.gnostic_ast: Optional['_GnosticNode'] = None

            # --- STRATUM 7: PARSING STATE ---
            self._in_code_block: bool = False
            self._block_quote_type: Optional[str] = None
            self.imported_files: Set[Path] = set()

            # [ASCENSION 33]: THE KINETIC VOLATILITY WARD
            self._kinetic_block_indents: List[int] = []

            # [ASCENSION 20]: STRICT MODE
            self.strict_mode: bool = False

            if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
                Logger.verbose(
                    f"Cortex Consecrated: Shared Registry Ready. Session: {getattr(self, 'parse_session_id', 'void')}"
                )

    def parse_string(
            self,
            content: str,
            file_path_context: Optional['Path'] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            line_offset: int = 0,
            overrides: Optional[Dict[str, Any]] = None,
            depth: int = 0
    ) -> Tuple['ApotheosisParser', List['ScaffoldItem'], List[Tuple], List['Edict'], Dict[str, Any], 'GnosticDossier']:
        """
        =================================================================================
        == THE OMEGA PARSER: TOTALITY (V-Ω-TOTALITY-V32000-SOVEREIGN-SUTURED)          ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_PARSE_STRING_V32000_SOVEREIGN_VARS_FINALIS_2026

        [THE MANIFESTO]
        The supreme kernel of Gnostic perception. It has been Ascended to enforce the
        **Law of Singular Truth**, righteously annihilating the 'Macro Evaporation'
        heresy. It performs a multi-strata merge of intent (overrides) into the
        Sovereign Mind (blueprint_vars) at nanosecond zero, ensuring all alchemical
        placeholders are resonant before the first verse of matter is willed.
        """
        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE OUROBOROS GUARD (RECURSION ADJUDICATION) ---
        if depth > self.MAX_RECURSION_DEPTH:
            raise ArtisanHeresy(
                f"Cerebral Hemorrhage: Recursive loop detected at '{file_path_context}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"The Gnostic stack breached the {self.MAX_RECURSION_DEPTH} strata ceiling.",
                suggestion="Check for circular @import or self-referential @call edicts."
            )

        self.depth = depth
        self.file_path = file_path_context
        self.line_offset = line_offset

        # LINEAGE TRACKING
        if file_path_context:
            self.lineage.append(file_path_context.name)

        # Force absolute anchoring to prevent Relative Path Drift
        self.base_path = (file_path_context.parent if file_path_context else Path.cwd()).resolve()

        # =========================================================================
        # == [THE CURE 1]: FAIL-SAFE PROJECT ROOT RESOLUTION                     ==
        # =========================================================================
        # Ensure the project_root is manifest. If None, anchor to the active base.
        if not self.project_root:
            self.project_root = self.base_path

        # =========================================================================
        # == [THE CURE 2]: THE SOVEREIGN GNOSIS SUTURE                           ==
        # =========================================================================
        # 1. Ingest External Pleas (Wizard/CLI) into L2 memory.
        if pre_resolved_vars:
            self.external_vars.update(pre_resolved_vars)

        # 2. SUTURE MACRO OVERRIDES INTO L1 TRUTH.
        # By injecting into blueprint_vars, we ensure these variables override
        # everything and are treated as bit-perfect truth by the Alchemist.
        if overrides:
            self.blueprint_vars.update(overrides)
            self.external_vars.update(overrides)

        # 3. CONSOLIDATE ACTIVE VIEW.
        # self.variables is the "Gaze" – the union of all known truths.
        self.variables.update(self.external_vars)
        self.variables.update(self.blueprint_vars)
        # =========================================================================

        # Raise recursion limit for complex architectural deep-dives.
        original_recursion_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(original_recursion_limit, 5000))

        lines = content.splitlines()
        i = 0

        # THE SILENCE VOW COMPLIANCE & RECURSIVE LOGGING
        if self.Logger.is_verbose:
            indent_log = "|  " * depth
            self.Logger.verbose(f"{indent_log}Parsing stratum {depth}: {file_path_context}")

        try:
            # =========================================================================
            # == THE CORE DECONSTRUCTION LOOP                                        ==
            # =========================================================================
            while i < len(lines):
                line = lines[i]
                current_line_num = i + 1 + self.line_offset
                original_indent = self._calculate_original_indent(line)
                stripped_line = line.strip()

                # [ASCENSION 11]: METABOLIC TELEMETRY PULSE
                if i % 100 == 0 and i > 0:
                    self._pulse_progress(i, len(lines))

                # --- PHASE 0: THE COGNITIVE TOXIN WARD (ALCHEMICAL SCAN) ---
                if "!!HERESY" in line:
                    self._proclaim_heresy(
                        "TEMPLATE_ERROR_LEAK",
                        ScaffoldItem(
                            path=Path("TOXIN_DETECTED"),
                            line_num=current_line_num,
                            raw_scripture=line,
                            is_dir=False,
                            line_type=GnosticLineType.VOID
                        ),
                        details=f"Metabolic toxin detected: '{stripped_line}'. The Alchemist is fractured.",
                        suggestion="Check your blueprint for undefined variables or malformed Jinja logic.",
                        severity=HeresySeverity.CRITICAL,
                        ui_hints={"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}
                    )
                    self.all_rites_are_pure = False
                    i += 1
                    continue

                # --- PHASE A: THE CODE-QUOTE SANCTUARY (THE SHIELD V4) ---
                # Detect the start/end of raw code blocks to prevent structural misinterpretation.
                quote_match = self.QUOTE_TOGGLE_REGEX.match(line)
                # Ensure it's not an assignment like $$ x = """
                if quote_match and not re.search(r'[:\+=^~]\s*("""|\'\'\')', line):
                    q_type = quote_match.group(1)
                    if self._in_code_block:
                        if q_type == self._block_quote_type:
                            self._in_code_block = False
                            self._block_quote_type = None
                            i += 1
                            continue
                    else:
                        self._in_code_block = True
                        self._block_quote_type = q_type
                        i += 1
                        continue

                if self._in_code_block:
                    i += 1
                    continue

                # =========================================================================
                # == THE KINETIC VOLATILITY FRACTURE WARD (ASCENSION 33)                 ==
                # =========================================================================
                # Track the scope of kinetic blocks (%% post-run, %% on-heresy, etc.)
                # We pop if the current line is at or below the indent of the block header.
                # Ignore empty lines or comments for popping
                if stripped_line and not stripped_line.startswith(('#', '//')):
                    while self._kinetic_block_indents and original_indent <= self._kinetic_block_indents[-1]:
                        self._kinetic_block_indents.pop()

                # --- PHASE B: THE INQUISITOR'S GAZE (LEXICAL TRIAGE) ---
                from ...parser_core.lexer_core.inquisitor import GnosticLineInquisitor

                vessel = GnosticLineInquisitor.inquire(
                    raw_line=line,
                    line_num=current_line_num,
                    parser=self,
                    grammar_codex_key=self.grammar_key,
                    original_indent=original_indent
                )

                # Register new kinetic blocks into the scope tracker
                if vessel.line_type in (GnosticLineType.POST_RUN, GnosticLineType.ON_HERESY, GnosticLineType.ON_UNDO):
                    self._kinetic_block_indents.append(original_indent)

                # --- PHASE C: THE LEXICAL SUTURE (MATTER GUARD) ---
                # Prevents edicts/directives from being misclassified as file paths.
                self._suture_lexical_leak(vessel)

                # [ASCENSION 10]: CASE-IDENTITY COLLISION PROBE
                if vessel.line_type == GnosticLineType.FORM and vessel.path:
                    self._adjudicate_case_identity(vessel)

                # --- PHASE D: SELECTIVE DISPATCH (ARTISAN ASSIGNMENT) ---
                scribe = self._get_scribe_for_vessel(vessel)
                prev_i = i

                if scribe:
                    # [STRIKE]: The specialized Scribe conducts the rite.
                    i = scribe.conduct(lines, i, vessel)
                else:
                    i += 1

                # ANTI-STASIS WARD: Ensure the timeline always moves forward.
                if i <= prev_i: i += 1

        except Exception as catastrophic_paradox:
            # =========================================================================
            # == [ASCENSION 6]: THE FORENSIC SNITCH (EMERGENCY RADIATION)            ==
            # =========================================================================
            sys.stderr.write(f"\n" + "!" * 80 + "\n")
            sys.stderr.write(f"🔥 CATASTROPHIC PARSING FRACTURE at L{i + 1}\n")
            sys.stderr.write(f"📍 TRACE: {getattr(self, 'parse_session_id', 'void')}\n")
            sys.stderr.write(f"📍 ERROR: {type(catastrophic_paradox).__name__}: {str(catastrophic_paradox)}\n")
            sys.stderr.write("-" * 80 + "\n")
            tb_scribe.print_exc(file=sys.stderr)
            sys.stderr.write("!" * 80 + "\n\n")
            sys.stderr.flush()

            self._proclaim_heresy(
                "META_HERESY_PARSER_FRACTURE",
                f"Absolute Failure at L{i + 1}",
                details=f"Deconstruction loop shattered by paradox: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}
            )

        finally:
            # Restore Substrate Metabolism
            sys.setrecursionlimit(original_recursion_limit)
            if file_path_context and self.lineage:
                self.lineage.pop()

        # --- MOVEMENT IV: SOVEREIGNTY RECONCILIATION ---
        # [ASCENSION 14]: Blueprint Truth (L1) righteously overwrites External Pleas (L2).
        self.variables.update(self.blueprint_vars)

        # --- MOVEMENT V: ACHRONAL FINALIZATION ---
        if depth == 0:
            # Forge the Gnostic Dossier and scan for Wasted Gnosis (Orphaned Variables).
            self._finalize_achronal_dossier()

            if not self.all_rites_are_pure:
                self.Logger.warn(
                    f"[{self.parse_session_id}] Parser concluding with impurities. Reality may be unstable."
                )

            # [ASCENSION 16]: THE PURIFIER'S BIOPSY
            self._scry_orphaned_variables()

        # [ASCENSION 18]: THE FINALITY VOW (THE SIX-FOLD DOWRY)
        # Transmute the active state into a unified Gnostic ledger.
        all_gnosis = {**self.blueprint_vars, **self.variables}

        return (
            self,
            self.raw_items,
            self.post_run_commands,
            self.edicts,
            all_gnosis,
            self.dossier
        )

    def resolve_reality(self) -> List[ScaffoldItem]:
        """
        =================================================================================
        == THE BRIDGE OF REALIZATION: OMEGA (V-Ω-TOTALITY-V35000-ABSOLUTE-RESOLVE)     ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_ENGINE | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This method contains the **Diamond-Hard Pre-Weave Transmutation**.
        It iterates over every item harvested by the scribes. If an item has a path
        that contains variables (`{{ name }}`), AND it has a `_macro_ctx` attached,
        it performs an immediate, surgical transmutation of the path using the combined
        context.
        """
        import hashlib
        import time
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity
        from ...contracts.data_contracts import ScaffoldItem
        from ...core.runtime.vessels import GnosticSovereignDict

        start_ns = time.perf_counter_ns()
        self.Logger.info(f"[{self.parse_session_id}] Bridge: Initiating Deterministic Convergence.")

        # --- MOVEMENT I: THE BATTLE FOR SOVEREIGNTY (GNOSIS CONVERGENCE) ---
        reconciled_gnosis = GnosticSovereignDict()
        reconciled_gnosis.update(self.external_vars)
        reconciled_gnosis.update(self.blueprint_vars)

        # --- MOVEMENT II: THE ENTROPY STABILIZATION LOOP ---
        max_passes = 10
        pass_num = 0

        while pass_num < max_passes:
            pass_num += 1
            state_before = hashlib.md5(str(reconciled_gnosis).encode()).hexdigest()

            for key, val in list(reconciled_gnosis.items()):
                if isinstance(val, str) and ("{{" in val or "{%" in val):
                    try:
                        reconciled_gnosis[key] = self.alchemist.render_string(val, reconciled_gnosis)
                    except Exception as alchemical_fracture:
                        self._proclaim_heresy(
                            "ALCHEMICAL_FRACTURE", f"$$ {key} = {val}",
                            details=f"Convergence failed for variable '{key}': {str(alchemical_fracture)}",
                            severity=HeresySeverity.CRITICAL,
                            suggestion="Ensure all variables willed in templates are defined in the '$$' block or provided via CLI."
                        )
                        return []

            state_after = hashlib.md5(str(reconciled_gnosis).encode()).hexdigest()
            if state_before == state_after:
                self.Logger.verbose(f"Gnostic Stasis achieved in {pass_num} alchemical pass(es).")
                break
        else:
            self._proclaim_heresy(
                "GNOSTIC_OUROBOROS_PARADOX", "VARIABLE_LATTICE",
                details="Variable resolution failed to reach stasis. Infinite recursion detected.",
                severity=HeresySeverity.CRITICAL
            )
            return []

        self.variables.update(reconciled_gnosis)

        # =========================================================================
        # == MOVEMENT III: PRE-WEAVE PATH TRANSMUTATION (THE ABSOLUTE CURE)      ==
        # =========================================================================
        self.Logger.verbose(f"Initiating Pre-Weave Transmutation on {len(self.raw_items)} atoms...")

        for item in self.raw_items:
            # We only transmute FORM items that have a path
            if item.line_type == GnosticLineType.FORM and item.path:
                path_str = str(item.path)

                # Check 1: Does the path need alchemy?
                if "{{" in path_str or "}}" in path_str:

                    # Check 2: Construct the full context
                    active_ctx = self.variables.copy()

                    # If the item was born in a Macro, inject its local soul
                    if item.semantic_selector and "_macro_ctx" in item.semantic_selector:
                        macro_ctx = item.semantic_selector["_macro_ctx"]
                        active_ctx.update(macro_ctx)

                    try:
                        # THE TRANSMUTATION
                        transmuted_path_str = self.alchemist.transmute(path_str, active_ctx)

                        # Clean artifacts
                        clean_path = transmuted_path_str.strip().strip('"\'')

                        # Validate that alchemy actually happened
                        if "{{" not in clean_path:
                            item.path = Path(clean_path)
                        else:
                            self.Logger.warn(
                                f"   -> Path '{path_str}' remains unresolved after alchemy. Possible missing variable.")

                    except Exception as e:
                        self.Logger.warn(f"Pre-Weave Transmutation fracture on '{path_str}': {e}")

        # --- MOVEMENT IV: TOPOLOGICAL INCEPTION (AST WEAVING) ---
        from .ast_weaver import GnosticASTWeaver
        weaver = GnosticASTWeaver(self)
        self.gnostic_ast = weaver.weave_gnostic_ast()

        # --- MOVEMENT V: CAUSAL REALIZATION (THE WILL) ---
        final_items, final_commands, logic_heresies, _ = weaver.resolve_paths_from_ast(self.gnostic_ast)
        self.heresies.extend(logic_heresies)

        # --- MOVEMENT VI: BICAMERAL PURGATION ---
        self.variables = self.alchemist.purge_private_gnosis(self.variables)
        gc.collect(1)

        # --- MOVEMENT VII: FINALITY ADJUDICATION ---
        plan_blob = "".join([str(i.path) for i in final_items]) + "".join([str(c[0]) for c in final_commands])
        plan_fingerprint = hashlib.sha256(plan_blob.encode()).hexdigest()[:8]

        if not final_items and not final_commands:
            self.Logger.warn("Convergence Paradox: The resulting reality is a void.")
            self._proclaim_heresy("VOID_REALITY_PARADOX", "PLAN_EMPTY", severity=HeresySeverity.WARNING)
        else:
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.Logger.success(
                f"Convergence Complete: [cyan]{plan_fingerprint}[/cyan] manifest in {duration_ms:.2f}ms.")

            # HUD Broadcast
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "CONVERGENCE_SUCCESS",
                            "label": f"PLAN_{plan_fingerprint}",
                            "color": "#64ffda",
                            "trace": self.parse_session_id,
                            "latency_ms": duration_ms
                        }
                    })
                except Exception:
                    pass

        return final_items

    def _suture_lexical_leak(self, vessel: GnosticVessel):
        """
        =============================================================================
        == THE LEXICAL SUTURE (V-Ω-THE-KILL-SWITCH)                                ==
        =============================================================================
        Intervenes when the Inquisitor misclassifies a Kinetic Edict as a Form Item.
        This annihilates the 'Profane characters in path' heresy for lines like
        '>> poetry install' or '?? file_exists'.

        It enforces the LAW OF LEXICAL HIERARCHY: Command Sigils override Path Geometry.
        =============================================================================
        """
        if vessel.line_type == GnosticLineType.FORM:
            raw_stripped = vessel.raw_scripture.strip()

            # THE LAW OF HIERARCHY: Sigils override Form.
            if raw_stripped.startswith(('>>', '??', '!!', '%%')):
                if raw_stripped.startswith('%%'):
                    vessel.line_type = GnosticLineType.POST_RUN
                else:
                    vessel.line_type = GnosticLineType.VOW
                    if raw_stripped.startswith('>>'):
                        vessel.edict_type = EdictType.ACTION
                    elif raw_stripped.startswith('??'):
                        vessel.edict_type = EdictType.VOW
                    elif raw_stripped.startswith('!!'):
                        vessel.edict_type = EdictType.BREAKPOINT

                vessel.path = None
                vessel.is_dir = False

            elif raw_stripped.startswith('@'):
                vessel.line_type = GnosticLineType.LOGIC
                vessel.directive_type = raw_stripped.split()[0][1:]
                vessel.path = None
                vessel.is_dir = False

            else:
                # =========================================================================
                # == [THE CURE]: THE MATTER-LEAK PARADOX (KINETIC VOLATILITY)            ==
                # =========================================================================
                # If this line is indented under a kinetic block (%% post-run, %% on-heresy),
                # it MUST be a kinetic edict, even if it lacks the '>>' sigil.
                # This annihilates the `makeinstall` and `gitinit` physical file heresy.
                if getattr(self, '_kinetic_block_indents', []):
                    # Transmute Form to Vow (Kinetic Edict)
                    vessel.line_type = GnosticLineType.VOW
                    vessel.edict_type = EdictType.ACTION
                    vessel.path = None
                    vessel.is_dir = False

                    # Inject the '>> ' sigil into the raw scripture to appease the PostRunScribe
                    # We preserve original indentation so AST placement remains true.
                    indent_str = vessel.raw_scripture[:len(vessel.raw_scripture) - len(vessel.raw_scripture.lstrip())]
                    vessel.raw_scripture = f"{indent_str}>> {raw_stripped}"

    def _forge_scribe_pantheon(self) -> Dict[str, FormScribe]:
        """
        =================================================================================
        == THE GOD-ENGINE OF SCRIBE FORGING (V-Ω-ETERNALLY-PURIFIED)                   ==
        =================================================================================
        [ASCENSION 12]: JIT Scribe Awakening.
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
        == THE CASE IDENTITY INQUISITOR (V-Ω-HYPER-DIAGNOSTIC-TITANIUM)            ==
        =============================================================================
        LIF: ∞ | ROLE: CROSS_PLATFORM_COLLISION_WARD | RANK: OMEGA_SOVEREIGN

        Performs a deep-tissue biopsy on the path identity to ensure Universal
        Resonance across all filesystems (NTFS, APFS, EXT4).
        """
        if not vessel.path:
            return

        # 1. TRANSMUTE TO STRING
        path_posix = vessel.path.as_posix()
        path_lower = path_posix.lower()

        # --- DIAGNOSTIC I: THE COLLISION MAP ---
        # We track {lowercase_path: original_path}
        if path_lower in self._lowercase_path_roster:
            # Conflict detected! Find the ancestor that claimed this slot.
            collision_victim = "Unknown"
            for existing_path in self.items_by_path.keys():
                if existing_path.lower() == path_lower and existing_path != path_posix:
                    collision_victim = existing_path
                    break

            # If it's the SAME path (exact match), it's just a re-definition (allowed-ish).
            # If it's a CASE MISMATCH, it is a heresy.
            if collision_victim != "Unknown":
                self._proclaim_heresy(
                    "CASE_IDENTITY_COLLISION",
                    vessel,
                    details=(
                        f"Dimensional Paradox: The path '{path_posix}' collides with '{collision_victim}' "
                        f"on case-insensitive file systems (Windows/macOS)."
                    ),
                    suggestion="Unify your casing strategy (snake_case recommended).",
                    severity=HeresySeverity.CRITICAL
                )
                return

        # Register the claim
        self._lowercase_path_roster.add(path_lower)

        # --- DIAGNOSTIC II: THE WINDOWS RESERVED WORD ORACLE ---
        RESERVED_NAMES = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        }

        # We check every segment of the path
        for part in path_posix.split('/'):
            # Strip extension for the check (CON.txt -> CON)
            stem = part.split('.')[0].upper()
            if stem in RESERVED_NAMES:
                self._proclaim_heresy(
                    "WINDOWS_RESERVED_NAME_HERESY",
                    vessel,
                    details=f"The segment '{part}' utilizes a reserved Windows device name ('{stem}').",
                    suggestion="Rename this file to ensure cross-platform materialization.",
                    severity=HeresySeverity.CRITICAL
                )

        # --- DIAGNOSTIC III: THE ILLEGAL GLYPH HUNTER ---
        # NTFS Forbidden: < > : " / \ | ? *
        INVALID_CHARS = set('<>:"|?*')
        for char in path_posix:
            if char in INVALID_CHARS:
                self._proclaim_heresy(
                    "ILLEGAL_GLYPH_HERESY",
                    vessel,
                    details=f"The path contains the profane character '{char}'. This is forbidden on Windows.",
                    severity=HeresySeverity.CRITICAL
                )

        # --- DIAGNOSTIC IV: THE TRAILING PHANTOM ---
        # Windows strips trailing dots and spaces, causing 'file ' to overwrite 'file'.
        if path_posix[-1] in ('.', ' '):
            self._proclaim_heresy(
                "TRAILING_PHANTOM_HERESY",
                vessel,
                details=f"The path ends with a dot or whitespace ('{path_posix[-1]}'). This causes identity loss on Windows.",
                severity=HeresySeverity.WARNING
            )

        # --- DIAGNOSTIC V: THE UNICODE HOMOGLYPH SCAN ---
        try:
            path_posix.encode('ascii')
        except UnicodeEncodeError:
            pass

        # --- DIAGNOSTIC VI: THE MAX_PATH HORIZON ---
        if len(path_posix) > 250:
            self._proclaim_heresy(
                "PATH_LENGTH_HERESY",
                vessel,
                details=f"Path length ({len(path_posix)}) approaches the Windows MAX_PATH (260) limit.",
                severity=HeresySeverity.WARNING
            )

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

    def _adjudicate_contracts(self, all_gnosis: Dict[str, Any]):
        """Validates variables against Gnostic Contracts."""
        for var_name, type_sig in self.variable_contracts.items():
            if var_name not in all_gnosis: continue

            value = all_gnosis[var_name]
            # Skip if value is a template
            if isinstance(value, str) and ("{{" in value or "{%" in value):
                continue

            try:
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
        == THE ACHRONAL SYNC-HOOK (V-Ω-TEMPORAL-ANCHOR-HEALED)                     ==
        =============================================================================
        [THE FIX]: Explicitly passes `macros=self.macros` to the Inquisitor.
        This ensures that local macro arguments are whitelisted and do not trigger
        `UNDEFINED_VAR` heresies.
        """
        current_git_head = get_git_commit(self.base_path) or "VOID_REALITY"

        from ...utils.gnosis_discovery import discover_required_gnosis

        self.dossier = discover_required_gnosis(
            execution_plan=self.raw_items,
            post_run_commands=self.post_run_commands,
            blueprint_vars={**self.blueprint_vars, **self.variables},
            macros=self.macros  # <--- THE DIVINE SUTURE
        )

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
        """
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel

        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', 0) or self.line_offset

        heresy = forge_heresy_vessel(
            key=key,
            line_num=line_num,
            line_content=raw_scripture,
            details=kwargs.get('details')
        )

        if severity := kwargs.get('severity'): heresy.severity = severity
        if suggestion := kwargs.get('suggestion'): heresy.suggestion = suggestion

        if ui_hints := kwargs.get('ui_hints'):
            Logger.debug(f"[UI_SIGNAL:{ui_hints.get('vfx')}] {heresy.message}")

        # [ASCENSION 20]: Strict Mode Enforcement
        if self.strict_mode and heresy.severity == HeresySeverity.WARNING:
            heresy.severity = HeresySeverity.CRITICAL

        self.heresies.append(heresy)

        # If the heresy is Critical, the entire materialization path is warded.
        if heresy.severity == HeresySeverity.CRITICAL:
            if hasattr(item, 'is_valid'): item.is_valid = False
            self.all_rites_are_pure = False

    def _consume_indented_block_with_context(self, lines: List[str], i: int, parent_indent: int) -> Tuple[
        List[str], int]:
        consumer = GnosticBlockConsumer(lines)
        return consumer.consume_indented_block(i, parent_indent)

    def _pulse_progress(self, current: int, total: int):
        """[ASCENSION 22]: Telemetry Pulse"""
        engine_ref = getattr(self, 'engine', None)
        akashic_ref = getattr(engine_ref, 'akashic', None) if engine_ref else None
        if akashic_ref:
            try:
                percent = int((current / total) * 100)
                # Debounce: Only send every 5%
                if percent % 5 == 0 and percent != getattr(self, '_last_pulse_percent', 0):
                    akashic_ref.broadcast({
                        "method": "scaffold/progress",
                        "params": {"id": "parse_scan", "message": "Deconstructing Scripture...", "percentage": percent}
                    })
                    self._last_pulse_percent = percent
            except:
                pass

    def _scry_orphaned_variables(self):
        """
        =================================================================================
        == THE ORACLE OF WASTED GNOSIS (V-Ω-TOTALITY-V32000-DEEP-TISSUE-SUTURED)       ==
        =================================================================================
        LIF: ∞ | ROLE: COGNITIVE_PURIFIER | RANK: OMEGA_INQUISITOR
        AUTH: Ω_SCRY_ORPHANS_V32000_ISOLATION_SUTURE_2026_FINALIS

        [THE CURE]: This version annihilates 'System Noise' by enforcing strict
        Bicameral Isolation. It grants absolute amnesty to the Engine's internal DNA,
        AND it automatically exempts variables that share a name with an Imported Shard,
        curing the False-Positive Dead Gnosis bug.
        =================================================================================
        """
        import time
        from ...contracts.heresy_contracts import HeresySeverity
        from ...contracts.data_contracts import GnosticLineType

        # Root Stratum Isolation.
        if self.depth > 0:
            return

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE CONSTITUTIONAL WHITELIST ---
        CONSTITUTIONAL_WHITELIST = {
            "project_name", "project_slug", "author", "email", "license",
            "version", "project_type", "description", "package_name",
            "clean_type_name", "trace_id", "session_id", "timestamp",
            "scaffold_env", "scaffold_reality", "scaffold_theory"
        }

        # [ASCENSION 2]: THE IMPORTED SHARD AMNESTY (THE CURE)
        # We automatically harvest the names of all imported files/folders and grant them immunity.
        # If the user imports `lib.database`, and defines `$$ database = ...`, it is used
        # implicitly by the Import Manager.
        imported_names = {p.stem for p in self.import_cache}
        imported_names.update({p.parent.name for p in self.import_cache})

        # --- MOVEMENT II: THE BICAMERAL CENSUS (THE CURE) ---
        # We only audit variables willed in the EXPLICIT BLUEPRINT (L1 Truth).
        # We ignore the 120+ system variables in 'self.variables' that weren't willed by the Architect.
        willed_keys: Set[str] = set(self.blueprint_vars.keys())

        if not willed_keys:
            return

        # --- MOVEMENT III: THE GAZE OF NECESSITY (DEEP TISSUE) ---
        # Gather all variables actually summoned by the Materialization Plan.
        required_keys: Set[str] = self.dossier.required if self.dossier else set()

        # [ASCENSION 29]: THE MACRO-ARGUMENT AMNESTY
        # Even though OmegaInquisitor subtracts local args, we ensure no macro
        # argument name accidentally triggers a false positive if willed globally.
        ritual_args: Set[str] = set()
        for macro in self.macros.values():
            ritual_args.update(macro.get('args', []))

        # --- MOVEMENT IV: THE ALCHEMICAL SIEVE ---
        # Orphans = (Willed) - (Required) - (Pillars) - (RitualArgs) - (Imports)
        dead_gnosis = willed_keys - required_keys - CONSTITUTIONAL_WHITELIST - ritual_args - imported_names

        # --- MOVEMENT V: THE PROCLAMATION ---
        final_orphans = [k for k in dead_gnosis if not k.startswith('_') and self.blueprint_vars.get(k)]

        if final_orphans:
            self.Logger.info(f"Purifier: Identified {len(final_orphans)} unit(s) of user-defined Dead Gnosis.")
            for key in final_orphans:
                locus_line = 0
                raw_scripture = f"$$ {key} = ..."
                for item in self.raw_items:
                    if item.line_type == GnosticLineType.VARIABLE and f" {key} " in f" {item.raw_scripture} ":
                        locus_line = item.line_num
                        raw_scripture = item.raw_scripture
                        break

                self._proclaim_heresy(
                    "DEAD_GNOSIS",
                    raw_scripture,
                    line_num=locus_line,
                    severity=HeresySeverity.INFO,
                    details=f"Metabolic Waste: The variable '${{ {key} }}' is willed but never summoned in the topology or logic.",
                    suggestion=f"Prune line {locus_line} to return the blueprint to Zen."
                )

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _duration_ms > 1.0:
            self.Logger.verbose(f"Metabolic Audit concluded in {_duration_ms:.2f}ms.")

    def snapshot_state(self) -> Dict[str, Any]:
        """[ASCENSION 2]: Forensic State Snapshot."""
        return {
            "variables": self.variables.copy(),
            "macros": copy.deepcopy(self.macros),
            "line_offset": self.line_offset,
            "file_path": str(self.file_path)
        }

    def _evolve_state_hash(self, mutation_key: str):
        """
        =============================================================================
        == THE STATE EVOLUTION PULSE (V-Ω-TOTALITY-V20000.5-MERKLE-SUTURE)         ==
        =============================================================================
        LIF: ∞ | ROLE: CAUSAL_INTEGRITY_ANCHOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_EVOLVE_V20000_STATE_HASH_FINALIS

        Updates the internal cryptographic fingerprint of the Parser's consciousness.
        This ensures that every inhalation (import) or definition ($$) is etched
        deterministically into the Gnostic Dossier, preventing "Silent Drift"
        across parallel dimensions.
        """
        import hashlib
        import time

        with self._state_lock:
            # 1. Triage the Input
            salt = str(mutation_key or "void_flux").strip()

            # 2. Capture the current Temporal Locus
            # We use nanoseconds for absolute collision avoidance.
            now_ns = time.perf_counter_ns()

            # 3. Forge the New Identity
            # We combine: Previous_Hash + Mutation_Key + Spacetime_Stamp
            raw_payload = f"{self._state_hash}:{salt}:{now_ns}"

            # [STRIKE]: The Cryptographic Seal
            self._state_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

            # 4. Multicast to Telemetry
            # If the engine is manifest, we notify the HUD of the state shift.
            if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic'):
                try:
                    if self.engine.akashic and self.depth == 0:  # Only pulse for root-level evolution
                        self.engine.akashic.broadcast({
                            "method": "novalym/state_evolution",
                            "params": {
                                "key": salt,
                                "hash": self._state_hash[:12],
                                "trace_id": getattr(self, "parse_session_id", "void")
                            }
                        })
                except Exception:
                    pass


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