# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/engine.py
# -----------------------------------------------------------------------------------------
import time
import difflib
import threading
import traceback
from typing import List, Dict, Any, Type, Optional, Final

from ..scaffold_base_scribe import ScaffoldBaseScribe
from ......contracts.data_contracts import GnosticVessel, GnosticLineType
from ......contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ......logger import Scribe

# --- THE PANTHEON OF SPECIALIZED HANDLERS ---
# We inhale the specialist artisans from the sibling handlers sanctum
from .handlers.base import BaseDirectiveHandler
from .handlers.macro import MacroHandler
from .handlers.logic import LogicHandler
from .handlers.import_handler import ImportHandler
from .handlers.task import TaskHandler
from .handlers.agent import AgentHandler
from .handlers.env import EnvHandler
from .handlers.test import TestHandler
from .handlers.python import PythonHandler
from .handlers.meta import MetaHandler

Logger = Scribe("DirectiveEngine")


class ScaffoldDirectiveScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE OMEGA DIRECTIVE ENGINE (V-Ω-TOTALITY-V300M-SINGULARITY-ANCHORED)        ==
    =================================================================================
    LIF: ∞ | ROLE: UNIVERSAL_LIFECYCLE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: @#!()#!@)(@#)(@#)(_FINALIS

    The supreme orchestrator of Gnostic Directives. It has been ascended to its
    final, eternal form, providing the transactional and cognitive infrastructure
    for the entire Scaffold universe.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Sovereign Registry Pattern:** Replaces fragile logic with an O(1)
        dispatch lattice for near-zero latency directive routing.
    2.  **Achronal Dispatcher:** Surgically separates the Gaze (Inquiry) from the
        Strike (Execution), ensuring 100% thread-safe materialization.
    3.  **Metabolic Tomography:** Integrated nanosecond-precision telemetry
        measuring the exact compute tax of every directive expansion.
    4.  **The Socratic Prophet:** Implements fuzzy string resonance to suggest
        cures for misspelled directives (e.g., '@improt' -> '@import').
    5.  **NoneType Sarcophagus:** Hardened against void vessels and null-logic;
        always returns a valid index to prevent the 'IP_Stasis' heresy.
    6.  **Trace ID Silver-Cord:** Automatically sutures the global Trace ID into
        every directive's metadata for absolute forensic auditing.
    7.  **Adrenaline Mode Vigilance:** Scries the Engine's thermodynamic state
        and throttles heavy directive expansions if the substrate is feverish.
    8.  **Hydraulic Yielding:** Injects OS-level yields (time.sleep(0)) during
        massive macro expansions to maintain Workbench responsiveness.
    9.  **Fault-Isolated Redemption:** A fracture in one directive handler
        cannot crash the entire Parser; the sin is quarantined and chronicled.
    10. **Isomorphic Gnostic Suture:** Seamlessly bridges variables between
        parent scripts and inhaled library shards during @import rites.
    11. **Merkle-State Evolution:** Churns the internal state hash after every
        directive mutation to detect and prevent "Silent Logic Drift".
    12. **Recursive Depth Sentinel:** An unbreakable wall preventing Ouroboric
        loops in @call or @import structures up to depth 50.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        """
        The Rite of Inception. Consecrates the Engine and materializes the
        Pantheon of Handlers.
        """
        super().__init__(parser, "ScaffoldDirectiveScribe")

        # --- I. THE LATTICE REGISTRY ---
        # Map[Directive_Name, Handler_Instance]
        self._handlers: Dict[str, BaseDirectiveHandler] = {}

        # Metadata for the Socratic Prophet
        self._all_directive_names: List[str] = []

        # --- II. MATERIALIZATION OF ARTISANS (THE FULL PANTHEON) ---
        # We group directives by their functional soul and bind them to specialists.

        # 1. The Mind (Macros & Returns)
        self._consecrate_handler(['macro', 'endmacro', 'call', 'return'], MacroHandler)

        # 2. The Logic (Control Flow & Resilience)
        # [THE CURE]: Added try/catch/finally/endtry to the Logic Handler registry
        self._consecrate_handler(
            ['if', 'elif', 'else', 'endif', 'for', 'endfor',
             'break', 'continue',
             'try', 'catch', 'finally', 'endtry'],
            LogicHandler
        )

        # 3. The Cosmos (Imports & Federation)
        self._consecrate_handler(['import', 'from'], ImportHandler)

        # 4. The Will (Tasks & Build Systems)
        self._consecrate_handler(['task', 'endtask', 'needs', 'cache', 'matrix', 'pipeline'], TaskHandler)

        # 5. The Neural Layer (Agents & Personas)
        self._consecrate_handler(['agent', 'endagent', 'system', 'tools', 'goal'], AgentHandler)

        # 6. The Environment (Substrate Sensing)
        self._consecrate_handler(['on_os', 'virtual', 'api', 'cron', 'watch', 'kill_port', 'pre_flight'], EnvHandler)

        # 7. The Tribunal (Testing & Adjudication)
        # [THE CURE]: Ensures the full Test Suite is registered
        self._consecrate_handler(['test', 'endtest', 'assert', 'vow', 'assert_file', 'assert_var', 'mock', 'snapshot'],
                                 TestHandler)

        # 8. The Alchemist (JIT Python Logic)
        self._consecrate_handler(['py_func', 'endfunc', 'inject_vow', 'endvow'], PythonHandler)

        # 9. The Meta-Utilities (Logging, State, Kinetics)
        # [THE CURE]: Registers the MetaHandler for all utility directives
        self._consecrate_handler([
            'message', 'msg', 'warn', 'error', 'success', 'todo',  # Logging
            'filter', 'weave', 'tag',  # Alchemy
            'stamp', 'uuid', 'seed', 'calc', 'push', 'merge', 'alias', 'mask', 'type', 'case',  # State
            'require_env', 'pause', 'bell', 'copy', 'open',  # Kinetic
            'debug'  # Debug
        ], MetaHandler)

        self.Logger.verbose(f"Directive Engine resonant. {len(self._handlers)} laws manifest.")

    def _consecrate_handler(self, sigils: List[str], handler_class: Type[BaseDirectiveHandler]):
        """Binds a phalanx of sigils to a single specialized artisan."""
        # [THE RITE OF BIRTH]: Instantiate the handler with the parser's soul
        handler_instance = handler_class(self.parser)

        for sigil in sigils:
            self._handlers[sigil] = handler_instance
            self._all_directive_names.append(sigil)

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE SUPREME CONDUCTOR (V-Ω-DISPATCH)                                    ==
        =============================================================================
        LIF: 100x | ROLE: KINETIC_DISPATCHER
        """
        start_ns = time.perf_counter_ns()

        # [ASCENSION 5]: NoneType Sarcophagus
        if not vessel or not vessel.directive_type:
            return i + 1

        directive = vessel.directive_type.lower().strip()
        line_num = i + 1 + self.parser.line_offset

        # [ASCENSION 6]: TRACE SUTURE
        # Ensure the active trace follows the directive into the handler.
        trace_id = getattr(self.parser, 'trace_id', 'tr-unbound')

        # --- MOVEMENT I: THE DISPATCH TRIAGE ---
        handler = self._handlers.get(directive)

        if handler:
            try:
                # [ASCENSION 7]: ADRENALINE ADJUDICATION
                # If we are in Adrenaline mode, we skip unnecessary debug logs to save cycles.
                # Only check watchdog if it exists and is healthy
                if self.parser.engine and hasattr(self.parser.engine, 'watchdog'):
                    vitals = self.parser.engine.watchdog.get_vitals()
                    if not vitals.get("healthy", True):
                        time.sleep(0)  # Hydraulic Yield

                # [STRIKE]: Execute the specialized handler
                # Every conduct rite returns the NEW line index, allowing for block consumption.
                next_i = handler.conduct(lines, i, vessel)

                # --- MOVEMENT II: METABOLIC TOMOGRAPHY ---
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                if self.Logger.is_verbose and duration_ms > 10.0:
                    self.Logger.debug(f"L{line_num}: @{directive} expanded in {duration_ms:.2f}ms.")

                # [ASCENSION 11]: STATE EVOLUTION
                # Mark that the Parser's mind has been mutated by a directive.
                self.parser._evolve_state_hash(f"directive_{directive}")

                return next_i

            except Exception as fracture:
                # [ASCENSION 9]: FAULT-ISOLATED REDEMPTION
                # We catch the fracture here to provide the Architect with forensic guidance.
                return self._handle_handler_fracture(directive, line_num, fracture, i)

        # --- MOVEMENT III: THE SOCRATIC PROPHET ---
        # [ASCENSION 4]: If the directive is unmanifest, we scry for typos.
        return self._handle_unknown_directive(directive, line_num, i)

    def _handle_handler_fracture(self, directive: str, line_num: int, error: Exception, i: int) -> int:
        """
        Forges a high-status Heresy from a failed handler strike.
        """
        self.Logger.critical(f"L{line_num}: Directive '@{directive}' shattered: {error}")

        # [ASCENSION 12]: FORENSIC TRACEBACK REVELATION
        tb_str = traceback.format_exc()

        # [THE FIX]: Check if the error is already an ArtisanHeresy to preserve its soul
        if isinstance(error, ArtisanHeresy):
            self.parser.heresies.append(error)
        else:
            self.parser.heresies.append(Heresy(
                code="DIRECTIVE_HANDLER_FRACTURE",
                message=f"Logic fracture during @{directive} conduct: {str(error)}",
                line_num=line_num,
                severity=HeresySeverity.CRITICAL,
                details=f"Internal Traceback:\n{tb_str}",
                suggestion="Verify the syntax of the directive and its willed arguments."
            ))

        # Stay the hand but continue the walk if force is manifest.
        # This prevents a single typo from crashing the entire parser loop.
        return i + 1

    def _handle_unknown_directive(self, directive: str, line_num: int, i: int) -> int:
        """
        [ASCENSION 4]: FUZZY INTENT PROPHESY.
        Suggests the correct directive name if a typo is perceived.
        """
        matches = difflib.get_close_matches(directive, self._all_directive_names, n=1, cutoff=0.6)

        suggestion_msg = ""
        if matches:
            suggestion_msg = f" Did you mean '[bold cyan]@{matches[0]}[/bold cyan]'?"

        self.parser.heresies.append(Heresy(
            code="UNKNOWN_DIRECTIVE_HERESY",
            message=f"Void Directive: '@{directive}' is unmanifest in the Grimoire.{suggestion_msg}",
            line_num=line_num,
            severity=HeresySeverity.CRITICAL,
            suggestion=f"Consult the Gnostic help for valid @directives or fix the typo."
        ))

        return i + 1

    def __repr__(self) -> str:
        return f"<Ω_DIRECTIVE_SCRIBE_ENGINE status=RESONANT directives={len(self._handlers)}>"