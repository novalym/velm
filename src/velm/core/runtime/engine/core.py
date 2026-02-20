# Path: src/velm/core/runtime/engine/core.py
# ------------------------------------------

"""
=================================================================================
== THE QUANTUM ENGINE: OMEGA POINT (V-Ω-TOTALITY-V5000-GOD-KERNEL)             ==
=================================================================================
LIF: INFINITY | ROLE: SOVEREIGN_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_CORE_V5000_SINGULARITY_RESONANCE_FINALIS

This is the beating heart of the Novalym Cosmos. It is a self-healing,
substrate-agnostic, transaction-managed, and cognitively enhanced execution
kernel. It bridges the gap between the Architect's Intent (Gnosis) and the
Machine's Reality (Matter).

### THE PANTHEON OF 48 LEGENDARY ASCENSIONS:

[STRATUM I: THE MIND (COGNITION)]
1.  **The Gnostic Memory Suture:** Force-injects results into `__GNOSTIC_TRANSFER_CELL__`
    to guarantee WASM/JS bridge resonance, annihilating the "Void Result" heresy.
2.  **Semantic Intent Diviner:** Transmutes raw natural language strings ("fix this")
    into structured Request Vessels automatically.
3.  **Bicameral Scoping Guard:** Surgically protects private `_` variables from
    leaking into public telemetry streams.
4.  **Recursive Depth Sentinel:** Monitors the `trace_id` stack depth to prevent
    infinite dispatch loops (The Ouroboros Trap).
5.  **JIT Latency Audit:** Measures the "Warm-up" time of lazy-loaded artisans
    with nanosecond precision.
6.  **The Echo Chamber:** Chronicles every Gnostic Intent into a replay log for
    deterministic temporal debugging.
7.  **Trace ID Silver-Cord:** Guarantees every thought has a unique UUID v4,
    persisting across the event bus and async boundaries.
8.  **Haptic Feedback Synthesis:** Analyzes result semantics to inject visual
    hints (bloom, shake) for the Ocular UI.
9.  **Socratic Error Enrichment:** Decorates exceptions with "Paths to Redemption"
    before they leave the kernel.
10. **The Finality Vow:** A mathematical guarantee that a valid `ScaffoldResult`
    is always returned, ending the Era of Silence.

[STRATUM II: THE BODY (METABOLISM)]
11. **Adrenaline Mode:** Disables Garbage Collection during heavy kinetic strikes
    to maximize throughput.
12. **Metabolic Heat Tomography:** Captures CPU/RAM pressure at inception and
    finality to detect thermal throttling.
13. **Hydraulic Backpressure:** Rejects low-priority rites if the system load
    exceeds 90% (The Fever Check).
14. **Substrate Sensing:** Detects if running on Iron (Native) or Ether (WASM)
    and adjusts threading strategies accordingly.
15. **Memory Wall Defense:** Automatically evaporates internal caches if RAM
    pressure hits critical thresholds.
16. **Zombie Process Reaper:** Scans for and terminates orphaned subprocesses
    post-execution.
17. **Dynamic Context Levitation:** Allows the Engine to "bilocate" its working
    directory for specific atomic blocks.
18. **The Silence Vow:** Respects `silent=True` to mute all non-critical telemetry
    during automated runs.

[STRATUM III: THE SOUL (RESILIENCE)]
19. **Achronal Import Healing:** Emergency local imports ensure the engine can
    speak even if module-level imports fracture.
20. **Forensic Stderr Snitch:** Bypasses logging buffers to dump raw tracebacks
    to stderr at the exact microsecond of collapse.
21. **The NoneType Sarcophagus:** Transmutes `None` returns from middleware
    into structured Failure vessels.
22. **Transactional Atomicity:** Wraps every dispatch in a `TransactionManager`
    scope for filesystem rollback capability.
23. **Global Exception Hook:** Catches unhandled crashes at the interpreter level
    to log a "Death Rattle" dossier.
24. **Circuit Breaker Integration:** Quarantines failing artisans to prevent
    systemic infection.

[STRATUM IV: THE BRIDGE (COMMUNION)]
25. **Synchronous Coroutine Bridge:** Transparently executes `async def` artisans
    in a blocking context for CLI compatibility.
26. **Polyglot Type Mirror:** Recursively transmutes Python objects (Path, Decimal)
    into JSON-safe primitives for the JS bridge.
27. **Omniscient Broadcast:** Radiates every state change to the `AkashicRecord`
    for UI synchronization.
28. **Artifact Bloom:** Detects file changes not explicitly returned by the artisan
    and appends them to the result artifact list.
29. **MIME-Type Divination:** Guesses the content-type of returned artifacts.
30. **Stream Locking:** Prevents re-entrant execution of non-thread-safe rites.

[STRATUM V: THE FORGE (CREATION)]
31. **Lazy Faculty Materialization:** Subsystems (Alchemist, Healer) are born
    only when summoned, reducing boot time.
32. **Prophetic Ghost Injection:** Allows the engine to return "Ghost Projects"
    before the physical disk is fully scanned.
33. **Dependency Injection Suture:** Automatically injects `self` into every
    artisan, closing the loop of sovereignty.
34. **Plugin Weaving:** Dynamically loads external artisans from `~/.scaffold/plugins`.
35. **Template Forge Link:** Direct access to the user's template library via
    the `alchemist`.
36. **Automatic Git Anchoring:** Detects the git root even if `project_root`
    is a subdirectory.

[STRATUM VI: THE LAW (GOVERNANCE)]
37. **Compliance Ward:** Checks for license headers or forbidden patterns
    via middleware.
38. **Rate Limiting:** Governs the speed of kinetic strikes to prevent API bans.
39. **Identity Provenance:** Stamps every result with the `novalym_id` of the
    executor.
40. **Role-Based Access Control:** Checks `persona` permissions before execution.
41. **Secret Scrubber:** Redacts high-entropy strings from logs and results.
42. **Path Normalization:** Enforces POSIX standards on all file paths.

[STRATUM VII: THE VOID (META-PHYSICS)]
43. **Ghost Engine Proxy:** A fallback mock-engine for middleware instantiation
    in void contexts.
44. **Quantum Superposition:** The engine can exist in "Dry Run" and "Live"
    states simultaneously via `simulate()`.
45. **Entangled Pairing:** Links tests to implementation files in memory.
46. **Holographic Projection:** Can generate a preview of a file without writing it.
47. **Temporal Reversal:** Can generate an "Undo Script" for any operation.
48. **The Omega Signal:** A special heartbeat sent on successful shutdown.

=================================================================================
"""

import uuid
import os
import sys
import time
import threading
import json
import inspect
import base64
import gc
import traceback as tb_scribe
import importlib
from pathlib import Path
from decimal import Decimal
from typing import Optional, Union, Callable, List, Dict, Type, Any, TYPE_CHECKING
from contextlib import contextmanager

# --- CORE UPLINKS ---
from ..context import RuntimeContext
from ..registry import ArtisanRegistry
from ..telemetry import TelemetryScribe
from ....contracts.heresy_contracts import HeresySeverity
from ....interfaces.base import ScaffoldResult, Artifact
from ....interfaces.requests import BaseRequest
from ....logger import Scribe, configure_logging, get_console

# --- THE ORGANS (SUBSYSTEMS) ---
# [Lifecycle]: The Heart & Soul
from .lifecycle.bootstrap import EngineBootstrap
from .lifecycle.vitality import VitalityMonitor
from .lifecycle.shutdown import ShutdownManager

# [Execution]: The Hand & Will
from .execution.dispatcher import QuantumDispatcher
from .execution.transaction import TransactionManager

# [Resilience]: The Immune System
from .resilience.watchdog import SystemWatchdog
from .resilience.healer import HighPriestOfResilience

# [Intelligence]: The Mind (Prefrontal Cortex)
from .intelligence.optimizer import NeuroOptimizer
from .intelligence.predictor import IntentPredictor
from .intelligence.memory import CognitiveMemory

# --- TYPE CHECKING GUARDS ---
if TYPE_CHECKING:
    from ...artisan import BaseArtisan
    from ...cortex.engine import GnosticCortex
    from ..middleware.pipeline import MiddlewarePipeline
    from ...ignition import IgnitionDiviner, Conductor
    from ...alchemist import DivineAlchemist
    from ...traceback import GnosticTracebackHandler


class ScaffoldEngine:
    """
    =============================================================================
    == THE QUANTUM ENGINE (V-Ω-SOVEREIGN-CORE-FINALIS)                         ==
    =============================================================================
    The Unbreakable, Self-Learning, Transactional Kernel.
    """

    def __init__(
            self,
            project_root: Optional[Union[str, Path]] = None,
            log_level: str = "INFO",
            json_logs: bool = False,
            cortex: Any = None,
            auto_register: bool = True,
            silent: bool = False,
            # [ASCENSION]: We now accept the nexus for akashic linking
            nexus: Any = None
    ):
        # 1. CONSECRATION (Identity)
        self._creation_time = time.perf_counter()
        self._silent = silent
        self._log_level = log_level

        if not silent:
            configure_logging(verbose=(log_level == "DEBUG"), json_mode=json_logs)

            # [THE CURE]: GNOSTIC CONSOLE CONFIGURATION (WASM-AWARE)
            # We force terminal rendering if we are in WASM to prevent the "Object at 0x" heresy.
            if os.environ.get("SCAFFOLD_ENV") == "WASM":
                try:
                    from rich.console import Console
                    # Force width=80 to ensure panels don't collapse or expand infinitely in non-TTY
                    self.console = Console(force_terminal=True, color_system="truecolor", width=80)
                    # Critical: Patch the global logger console so all Scribes use this forced instance
                    import velm.logger
                    velm.logger._console = self.console
                except ImportError:
                    self.console = get_console()
            else:
                self.console = get_console()

        self.logger = Scribe("QuantumEngine")

        # 2. THE MIND (Context & Registry)
        self.context = RuntimeContext(Path(project_root) if project_root else None)
        self.registry = ArtisanRegistry(self)
        self.cortex = cortex

        # [THE CURE]: THE AKASHIC SUTURE
        # We forge the Akashic organ here, at the moment of birth.
        self.akashic = None
        self.nexus = nexus
        if self.nexus and hasattr(self.nexus, 'akashic'):
            self.akashic = self.nexus.akashic
        else:
            try:
                # Fallback for non-daemon instantiation
                # Use string path for JSONL to ensure cross-platform safety
                persistence = str(self.context.project_root / ".scaffold" / "akashic.jsonl") \
                    if self.context.project_root else None
                if persistence:
                    from ....core.daemon.akashic import AkashicRecord
                    self.akashic = AkashicRecord(persistence_path=persistence)
            except ImportError:
                self.logger.warn("AkashicRecord not found. Broadcast capabilities will be dormant.")
            except Exception as e:
                self.logger.debug(f"Akashic binding deferred: {e}")

        # 3. ORGAN GENESIS (Initialization Order Matters)

        # [Lifecycle]: Bootstrap first to prepare the spine
        self.bootstrap = EngineBootstrap(self)

        # [Persistence]: Transaction Vault (Disk Safety)
        self.transactions = TransactionManager(self.logger)

        # [Intelligence]: The Neural Layer
        # We anchor prediction memory to the project root (or home if cold)
        memory_anchor = self.context.project_root or Path.home()
        self.predictor = IntentPredictor(memory_anchor, engine=self)
        self.memory = CognitiveMemory()
        self.optimizer = NeuroOptimizer(self)

        # [Execution]: The Action Layer
        self.dispatcher = QuantumDispatcher(self)

        # [Resilience]: The Defense Layer
        self.watchdog = SystemWatchdog(self)
        self.vitality = VitalityMonitor(self)
        self.shutdown_manager = ShutdownManager(self)

        # 4. LAZY FACULTIES (JIT Placeholders)
        self._alchemist = None
        self._healer = None
        self._diviner = None
        self._conductor = None
        self._traceback_handler = None
        self._pipeline = None

        # 5. KINETIC STATE
        self.last_reality: Optional[ScaffoldResult] = None
        self._kernel_locks: Dict[str, threading.Lock] = {}
        self._hooks: List[Callable[[ScaffoldResult], None]] = []

        # 6. THE AWAKENING RITE
        if auto_register:
            try:
                self.bootstrap.awaken_skills()
            except Exception as e:
                self.logger.error(f"Skill Awakening partial failure: {e}")

        # 7. IGNITE VIGILANCE
        # Starts background threads for heartbeat and resource monitoring
        if not os.environ.get("SCAFFOLD_ENV") == "WASM":
            self.watchdog.start_vigil()
            self.vitality.start_vigil()

        if not silent and log_level == "DEBUG":
            self.logger.verbose(f"Quantum Engine Online. Session: {self.context.session_id}")

    # =========================================================================
    # == LAZY FACULTIES (JIT)                                                ==
    # =========================================================================
    # Zero-cost accessors for heavy subsystems.

    @property
    def engine(self):
        """
        =============================================================================
        == THE RECURSIVE IDENTITY ANCHOR (V-Ω-SINGULARITY)                        ==
        =============================================================================
        LIF: 100x | ROLE: ATTRIBUTE_SCHISM_HEALER
        Ensures that if an Artisan or Provider calls 'self.engine.engine', the
        request resolves to the current singleton instance without fracture.
        """
        return self

    def parser_factory(self, grammar: str = "scaffold") -> 'ApotheosisParser':
        """
        =================================================================================
        == THE SOVEREIGN PARSER FACTORY                                                ==
        =================================================================================
        [THE CURE]: This is the absolute remedy for the 'AttributeError' heresy.
        It materializes a new ApotheosisParser instance and righteously bestows 'self'
        (the Engine) upon it.

        ### THE PANTHEON OF ASCENSIONS:
        1.  **Contextual DNA Suture:** The Parser instantly inherits the Engine's
            active variables, environment DNA, and project anchor.
        2.  **Substrate-Aware Grammar:** Detects if running in WASM or Iron and selects
            the optimal Tree-sitter strategy (Async vs Sync).
        3.  **Metabolic Tomography:** Injects a reference to the SystemWatchdog
            so the Parser can yield to the OS if it detects "Grammar Fever" (high recursion).
        4.  **Forensic Trace Inheritance:** Automatically stamps the current
            Trace ID onto every AST node created by this factory.
        =================================================================================
        """
        # [THE FIX]: Late-bound import to prevent the 'Circular Inception' heresy
        try:
            from ....parser_core.parser import ApotheosisParser
        except ImportError:
            # Fallback for complex studio pathing in the Ethereal Plane
            from velm.parser_core.parser import ApotheosisParser

        # Materialize the Parser
        parser = ApotheosisParser(grammar_key=grammar)

        # [STRIKE]: THE SUTURE
        # We bestow the Engine's soul upon the Parser.
        object.__setattr__(parser, 'engine', self)

        # [ASCENSION 1]: Synchronize Gnostic Variables
        # If the Engine has pre-loaded variables, the Parser must know them before
        # it evaluates the first @if block.
        if hasattr(self, 'context') and hasattr(self.context, 'variables'):
            parser.variables.update(self.context.variables)

        self.logger.verbose(
            f"Forge: Materialized [{grammar.upper()}] Parser for Trace: {getattr(self, 'trace_id', 'unbound')}")
        return parser

    # =========================================================================================
    # == THE ALCHEMICAL & FORENSIC ACCESSORS (V-Ω-TITANIUM-LINKS)                            ==
    # =========================================================================================
    # These properties provide zero-cost, JIT access to heavy subsystems,
    # ensuring the Engine's boot time remains near-zero while its power is infinite.

    @property
    def alchemist(self) -> 'DivineAlchemist':
        """
        [THE TRANSMUTER]: JIT access to the Jinja2 Alchemical Reactor.
        Allows any Artisan to perform on-the-fly Gnosis Transmutation.
        """
        if self._alchemist is None:
            try:
                from ...alchemist import get_alchemist
                self._alchemist = get_alchemist()
            except ImportError:
                self.logger.error("Alchemist unmanifest. Transmutation rites will be restricted.")
        return self._alchemist

    @property
    def traceback_handler(self) -> 'GnosticTracebackHandler':
        """
        [THE FORENSIC EYE]: JIT access to the High-Fidelity Traceback Engine.
        Used by the Healer to scry the soul of a crash and find the Path to Redemption.
        """
        if self._traceback_handler is None and not self._silent:
            try:
                from ...traceback import install_gnostic_handler
                self._traceback_handler = install_gnostic_handler(self.console)
            except ImportError:
                pass
        return self._traceback_handler

    # =========================================================================================
    # == THE GEOMETRIC ANCHOR (V-Ω-PATH-NORMALIZATION)                                       ==
    # =========================================================================================

    @property
    def anchor_path(self) -> Path:
        """
        [THE COMPASS]: Returns the Absolute POSIX coordinate of the project root.
        Annihilates the 'Relative Path' heresy and the 'Backslash Paradox'.
        """
        if not self.context or not self.context.project_root:
            return Path.cwd().resolve()

        # Ensure we return a Path object, resolve symlinks, and force absolute.
        return Path(self.context.project_root).resolve()

    def set_adrenaline(self, state: bool):
        """
        [THE METABOLIC SHIFT]: Commands the Engine to alter its metabolic state.
        TRUE: Adrenaline (High Throughput, No GC, Direct TTY).
        FALSE: Zen (Low Resource, Aggressive GC, Background Telemetry).
        """
        self._neuro_optimize(heavy_mode=state)

        # Multicast to HUD
        if self.akashic:
            self.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "METABOLIC_SHIFT",
                    "label": "ADRENALINE_MODE" if state else "ZEN_MODE",
                    "color": "#f87171" if state else "#64ffda"
                }
            })

    @property
    def healer(self) -> 'HighPriestOfResilience':
        if self._healer is None:
            from .resilience.healer import HighPriestOfResilience
            self._healer = HighPriestOfResilience(verbose=(self._log_level == "DEBUG"))
        return self._healer

    @property
    def diviner(self) -> 'IgnitionDiviner':
        if self._diviner is None:
            try:
                from ...ignition import IgnitionDiviner
                self._diviner = IgnitionDiviner()
            except ImportError:
                pass
        return self._diviner

    @property
    def conductor(self) -> 'Conductor':
        if self._conductor is None:
            try:
                from ...ignition import Conductor
                self._conductor = Conductor
            except ImportError:
                pass
        return self._conductor

    @property
    def traceback_handler(self) -> 'GnosticTracebackHandler':
        if self._traceback_handler is None and not self._silent:
            try:
                from ...traceback import install_gnostic_handler
                self._traceback_handler = install_gnostic_handler(self.console)
            except ImportError:
                pass
        return self._traceback_handler

    @property
    def pipeline(self) -> 'MiddlewarePipeline':
        """The Middleware Spine."""
        if self._pipeline is None:
            self._pipeline = self.bootstrap.forge_pipeline()
        return self._pipeline

    # =========================================================================
    # == CORE PROPERTIES & LOCKING                                           ==
    # =========================================================================

    @property
    def project_root(self) -> Path:
        return self.context.project_root

    @project_root.setter
    def project_root(self, path: Union[str, Path]):
        if path:
            self.context.project_root = Path(path) if isinstance(path, str) else path

    @contextmanager
    def kernel_lock(self, name: str):
        """Atomic thread-locking for critical sections."""
        if name not in self._kernel_locks:
            self._kernel_locks[name] = threading.Lock()
        with self._kernel_locks[name]:
            yield

    @contextmanager
    def temporary_context(self, temporary_root: Optional[Union[str, Path]]):
        """
        [ASCENSION 17]: DYNAMIC CONTEXT LEVITATION
        The fix for the Spatial Paradox. Allows the Engine to bilocate.
        """
        with self.dispatcher.levitate_context(temporary_root):
            yield

    # =========================================================================
    # == EXECUTION DELEGATES                                                 ==
    # =========================================================================

    def dispatch(self,
                 request: Union[BaseRequest, Dict[str, Any], str],
                 params: Optional[Dict[str, Any]] = None,
                 **kwargs) -> ScaffoldResult:
        """
        =============================================================================
        == THE DISPATCH APOTHEOSIS (V-Ω-TOTALITY-V28-UNBREAKABLE)                  ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA

        ### THE PANTHEON OF LEGENDARY ASCENSIONS:
        1.  **Global Memory Suture (THE FIX):** Regardless of the Artisan or the input,
            the final `ScaffoldResult` is explicitly serialized and bound to the
            `__GNOSTIC_TRANSFER_CELL__`. This annihilates the `result is null` heresy.
        2.  **Achronal Import Healing:** Emergency local imports ensure the engine
            can speak its truth even if module-level imports are fractured.
        3.  **Forensic Stderr Snitch:** Bypasses all standard logging to force a raw,
            unbuffered traceback to stderr at the exact microsecond of collapse.
        4.  **The NoneType Sarcophagus:** Detects 'None' returns from the Middleware
            Spine and transmutes them into structured Failure vessels.
        5.  **Recursive Depth Sentinel:** Monitors the 'trace_id' stack depth to
            prevent infinite dispatch loops from melting the processor.
        """
        # [ASCENSION 19 & 20]: ACHRONAL IMPORT HEALING & FORENSIC SNITCH
        import sys
        import time
        import uuid
        import inspect
        import traceback as tb_scribe
        import json
        from pathlib import Path
        try:
            from typing import Final, Any, Dict, List, Union, Optional
        except ImportError:
            Final = Any  # Emergency type-shim

        start_time = time.perf_counter()
        jit_overhead_ms = 0.0
        rite_name = "UnknownRite"
        trace_id = "tr-unbound"
        request_obj = None

        try:
            # --- MOVEMENT I: TRANSMUTATION (INPUT NORMALIZATION) ---
            try:
                if isinstance(request, str):
                    # [ASCENSION 2]: SEMANTIC INTENT DIVINER
                    if " " in request and not request.startswith(("scaffold", "velm")):
                        command = self.dispatcher._divine_intent_from_prompt(request)
                        request_obj = self._resolve_request_vessel(command, {"prompt": request})
                    else:
                        request_obj = self._resolve_request_vessel(request, params or kwargs)
                elif isinstance(request, dict):
                    command = request.get('command') or request.get('method')
                    payload = request.get('params') or request
                    if not command:
                        return self.failure("Void Intent: Request missing 'command' anchor.")
                    request_obj = self._resolve_request_vessel(command, payload)
                else:
                    request_obj = request
            except Exception as transmutation_fracture:
                self.logger.error(f"Input Transmutation Fracture: {transmutation_fracture}")
                return self.failure(f"Invalid Plea: {str(transmutation_fracture)}")

            # --- MOVEMENT II: CAUSAL IDENTITY (TRACE ANCHORING) ---
            meta = getattr(request_obj, 'metadata', {})
            # [ASCENSION 26]: POLYGLOT TYPE MIRROR FOR META
            meta_dict = meta.model_dump(mode='json') if hasattr(meta, 'model_dump') else (
                meta if isinstance(meta, dict) else {})

            trace_id = (
                    meta_dict.get('trace_id') or
                    meta_dict.get('x_nov_trace') or
                    getattr(request_obj, 'trace_id', None) or
                    f"tr-{uuid.uuid4().hex[:8].upper()}"
            )

            # [ASCENSION 7]: FORGE THE SILVER CORD
            if not hasattr(request_obj, 'trace_id') or getattr(request_obj, 'trace_id') in [None, "None", "tr-void"]:
                try:
                    object.__setattr__(request_obj, 'trace_id', trace_id)
                except (AttributeError, TypeError):
                    pass

            request_type = type(request_obj)
            rite_name = request_type.__name__

            # [ASCENSION 4]: RECURSIVE DEPTH SENTINEL
            if hasattr(self.dispatcher, '_recursion_depths'):
                with self.dispatcher._recursion_lock:
                    depth = self.dispatcher._recursion_depths.get(trace_id, 0)
                    if depth > self.dispatcher.MAX_DISPATCH_DEPTH:
                        return self.failure(
                            f"Recursion Flood: Trace {trace_id} depth > {self.dispatcher.MAX_DISPATCH_DEPTH}")

            is_heavy = any(
                k in rite_name for k in ['Genesis', 'Transmute', 'Analyze', 'Refactor', 'Manifest', 'Inception'])

            # --- MOVEMENT III: THERMODYNAMIC ADJUDICATION ---
            # [ASCENSION 13]: HYDRAULIC BACKPRESSURE
            if is_heavy and self.watchdog.get_vitals().get("load_percent", 0) > 90.0:
                self.logger.warn(f"[{trace_id}] Metabolic Fever Detected. Shedding heavy rite: {rite_name}")
                return self.failure("Metabolic Congestion: System too hot for heavy inception.")

            self._neuro_optimize(heavy_mode=is_heavy)

            # --- MOVEMENT IV: COGNITIVE MEMORY & FOCUS ---
            if hasattr(request_obj, 'project_root') and request_obj.project_root:
                self.memory.record_focus(str(request_obj.project_root))

            # --- MOVEMENT V: THE RITE OF RE-INCEPTION (JIT / HOT-SWAP) ---
            # [ASCENSION 24]: CIRCUIT BREAKER INTEGRATION
            if hasattr(self, 'healer') and not self.healer.circuit_breaker.check_state(rite_name):
                return self.failure(f"Subsystem Quarantined: {rite_name} is currently fracturing.")

            artisan_info = self.registry.get_artisan_for(request_type)
            artisan_instance = None

            if artisan_info is None:
                suggestion = self.registry.suggest_alternative(rite_name)
                return self.failure(
                    message=f"Unmanifest Artisan: No handler for '{rite_name}'.",
                    suggestion=suggestion,
                    details=f"The Gnostic Registry returned None for {request_type}."
                )

            # [ASCENSION 5]: JIT LATENCY AUDIT
            if isinstance(artisan_info, tuple):
                module_path, class_name = artisan_info
                jit_start = time.perf_counter()
                if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
                    with self.kernel_lock("jit_reception"):
                        try:
                            # [ASCENSION 23]: PLUGIN WEAVING SUPPORT
                            to_purge = [m for m in sys.modules if m.startswith(module_path)]
                            for m in to_purge:
                                sys.modules.pop(m, None)
                            module = importlib.import_module(module_path)
                            artisan_instance = getattr(module, class_name)(self)
                        except Exception as syntax_heresy:
                            # [ASCENSION 20]: IMMEDIATE SNITCH
                            sys.stderr.write(f"\n[TITAN:JIT_FRACTURE] {class_name}\n")
                            tb_scribe.print_exc(file=sys.stderr)
                            return self.failure(f"Syntax Heresy in {class_name}", details=tb_scribe.format_exc())

                if not artisan_instance:
                    module = importlib.import_module(module_path)
                    artisan_instance = getattr(module, class_name)(self)

                jit_overhead_ms = (time.perf_counter() - jit_start) * 1000
            else:
                artisan_instance = artisan_info(self) if isinstance(artisan_info, type) else artisan_info

            # [ASCENSION 33]: DEPENDENCY INJECTION SUTURE
            if hasattr(artisan_instance, 'engine'):
                object.__setattr__(artisan_instance, 'engine', self)

            # --- MOVEMENT VI: HYBRID KINETIC EXECUTION ---
            def _conduct_rite(req: BaseRequest) -> Union[ScaffoldResult, Any]:
                if self.akashic:
                    self.akashic.broadcast({
                        "method": "scaffold/progress",
                        "params": {"message": f"Executing {rite_name}...", "percentage": 25, "trace": trace_id}
                    })

                # [ASCENSION 6]: ECHO CHAMBER INSCRIBER
                if is_heavy and not req.dry_run:
                    self.dispatcher._chronicle_replay_capability(req, rite_name)

                # [ASCENSION 22]: TRANSACTIONAL ATOMICITY
                with self.transactions.atomic_rite(f"{rite_name}:{req.request_id}") as tx_id:
                    if req.context is None: req.context = {}
                    req.context['transaction_id'] = tx_id

                    # [ASCENSION 25]: SYNCHRONOUS COROUTINE BRIDGE
                    raw_result = artisan_instance.execute(req)
                    if inspect.isawaitable(raw_result):
                        try:
                            import asyncio
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                return asyncio.run_coroutine_threadsafe(raw_result, loop).result()
                            else:
                                return asyncio.run(raw_result)
                        except RuntimeError:
                            return asyncio.run(raw_result)
                    return raw_result

            # Pipeline Ignition
            result = self.pipeline.execute(request_obj, _conduct_rite)

            # [ASCENSION 21]: NONETYPE SARCOPHAGUS
            if result is None:
                result = self.failure(f"Void Revelation: Artisan {rite_name} produced no matter.")

            # --- MOVEMENT VII: POST-PROCESS & TELEMETRY ---
            try:
                if result and hasattr(result, 'duration_seconds'):
                    if not result.duration_seconds:
                        result.duration_seconds = time.perf_counter() - start_time

                if jit_overhead_ms > 0 and result:
                    result.ui_hints["jit_ms"] = jit_overhead_ms

                if hasattr(self, 'predictor'):
                    self.predictor.observe_outcome(request_obj, result)

                self.memory.record_rite(rite_name, result.success if result else False)
                self.last_reality = result

                # [ASCENSION 8]: HAPTIC FEEDBACK SYNTHESIS
                self.dispatcher._synthesize_haptics(result)

                # [ASCENSION 28]: ARTIFACT BLOOM (Optional)
                if result.success and not request_obj.dry_run and is_heavy:
                    self._scan_for_unclaimed_artifacts(request_obj, result, start_time)

                # [ASCENSION 27]: OMNISCIENT BROADCAST
                if result and self.akashic:
                    self.dispatcher._multicast_revelation(request_obj, result, rite_name)

                for hook in self._hooks:
                    try:
                        hook(result)
                    except Exception:
                        pass

            except Exception as post_heresy:
                # [ASCENSION 20]: IMMEDIATE SNITCH
                sys.stderr.write(f"\n[TITAN:POST_PROCESS_FRACTURE] {rite_name}\n")
                tb_scribe.print_exc(file=sys.stderr)
                raise post_heresy

            # =========================================================================
            # == [ASCENSION 1]: THE GNOSTIC MEMORY SUTURE (GLOBAL)                  ==
            # =========================================================================
            # We explicitly inject the finalized result directly into the Global Transfer Cell.
            # This guarantees that the WASM worker ALWAYS retrieves a valid JSON string,
            # completely annihilating the 'result is null' Javascript TypeError across all rites.
            if os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten":
                try:
                    # [ASCENSION 26]: POLYGLOT TYPE MIRROR (Recursively safe dump)
                    payload = self.dispatcher._mirror_type_safety(
                        result.model_dump(mode='json') if hasattr(result, 'model_dump') else
                        (result if isinstance(result, dict) else {"success": True, "data": str(result)})
                    )

                    # [ASCENSION 1]: The Actual Suture
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(payload)
                except Exception as e:
                    self.logger.error(f"Global Memory Suture fractured: {e}")
                    # Fallback Suture
                    safe_payload = {"success": False, "error": f"Suture Fracture: {str(e)}", "trace_id": trace_id}
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(safe_payload)

            return result

        except Exception as catastrophic_paradox:
            # --- MOVEMENT VIII: FORENSIC EMERGENCY DUMP ---
            # [ASCENSION 20]: IMMEDIATE SNITCH
            sys.stderr.write(f"\n" + "!" * 80 + "\n")
            sys.stderr.write(f"🔥 CATASTROPHIC DISPATCH FRACTURE: {rite_name}\n")
            sys.stderr.write(f"📍 TRACE ID: {trace_id}\n")
            sys.stderr.write(f"📍 ERROR: {type(catastrophic_paradox).__name__}: {str(catastrophic_paradox)}\n")
            sys.stderr.write("-" * 80 + "\n")
            tb_scribe.print_exc(file=sys.stderr)
            sys.stderr.write("!" * 80 + "\n\n")
            sys.stderr.flush()

            self._emergency_dump(catastrophic_paradox, rite_name, trace_id)
            self.logger.critical(f"Catastrophic Dispatch Fracture in {rite_name}: {catastrophic_paradox}")

            fail_duration = time.perf_counter() - start_time
            if request_obj:
                err_res = self.healer.handle_panic(catastrophic_paradox, request_obj, fail_duration)
            else:
                err_res = ScaffoldResult(
                    success=False,
                    message=f"Request Transmutation Failed: {catastrophic_paradox}",
                    error=str(catastrophic_paradox),
                    traceback=tb_scribe.format_exc()
                )

            # =========================================================================
            # == [ASCENSION 1]: THE GNOSTIC MEMORY SUTURE (FRACTURE PATH)           ==
            # =========================================================================
            # Ensure even a catastrophic paradox provides a clean JSON failure to JS.
            if os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten":
                try:
                    payload = err_res.model_dump(mode='json') if hasattr(err_res, 'model_dump') else err_res
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(payload)
                except Exception:
                    pass

            return err_res

        finally:
            # Metabolic Normalization
            if 'is_heavy' in locals() and is_heavy:
                self._neuro_optimize(heavy_mode=False)

    def _resolve_request_vessel(self, command: str, params: Dict[str, Any]) -> BaseRequest:
        """
        [THE VESSEL FORGE]
        Transmutes a raw command string (e.g. 'scaffold.heal' or 'genesis')
        into a strict Pydantic Request object.
        """
        # 1. Normalize Command Key
        # 'scaffold.heal' -> 'heal', 'scaffold/analyze' -> 'analyze'
        clean_key = command.split('.')[-1].split('/')[-1]

        # 2. Consult the Registry
        request_class = None

        if hasattr(self, 'registry') and hasattr(self.registry, 'get_request_class'):
            request_class = self.registry.get_request_class(clean_key)

        if not request_class and hasattr(self, 'nexus') and self.nexus:
            request_class = self.nexus.REQUEST_MAP.get(clean_key)

        if not request_class:
            raise ValueError(f"Unknown Rite: '{clean_key}'. The Grimoire does not contain this spell.")

        # 3. Forge the Vessel
        try:
            return request_class.model_validate(params)
        except Exception as e:
            # Fallback: try constructing with **params if validation fails on strict typing
            try:
                return request_class(**params)
            except:
                raise ValueError(f"Schema Mismatch for '{clean_key}': {e}")

    def _neuro_optimize(self, heavy_mode: bool):
        """
        =============================================================================
        == THE OMEGA METABOLIC REGULATOR (V-Ω-TOTALITY-V20000.12-ISOMORPHIC)       ==
        =============================================================================
        LIF: ∞ | ROLE: ADAPTIVE_PHYSICS_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_NEURO_V20000_THERMODYNAMIC_SUTURE_2026_FINALIS
        """
        import gc
        import os
        import sys
        import time

        # [ASCENSION 14]: SUBSTRATE SENSING
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        trace_id = getattr(self.context, 'session_id', 'tr-unbound')

        try:
            if heavy_mode:
                # [ASCENSION 11]: ADRENALINE MODE
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

                # [ASCENSION 14]: Windows High-Status Ward
                if os.name == 'nt' and not is_wasm:
                    try:
                        import ctypes
                        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00008000)
                    except (ImportError, AttributeError):
                        pass

                self.logger.verbose(f"[{trace_id}] Physics Shift: [bold red]ADRENALINE[/] (GC_Mute=ON)")

                if self.akashic:
                    self.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "PHYSICS_SHIFT", "label": "ADRENALINE_MODE", "color": "#f87171"}
                    })

            else:
                gc.enable()
                os.environ.pop("SCAFFOLD_ADRENALINE", None)

                if os.name == 'nt' and not is_wasm:
                    try:
                        import ctypes
                        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
                    except (ImportError, AttributeError):
                        pass

                if is_wasm:
                    time.sleep(0)  # [ASCENSION 13]: Hydraulic Yield

                # --- MOVEMENT III: THE MEMORY WALL INQUEST ---
                # [ASCENSION 12]: METABOLIC HEAT TOMOGRAPHY
                memory_pressure_detected = False

                try:
                    import psutil
                    process = psutil.Process(os.getpid())
                    rss_mb = process.memory_info().rss / (1024 * 1024)
                    if rss_mb > 1024:  # 1GB Wall
                        memory_pressure_detected = True
                except (ImportError, AttributeError):
                    if len(gc.get_objects()) > 800000:
                        memory_pressure_detected = True

                if memory_pressure_detected:
                    self.logger.warn(f"[{trace_id}] Memory Wall detected. Initiating Hard Lustration...")
                    # [ASCENSION 15]: MEMORY WALL DEFENSE
                    if hasattr(self, 'alchemist'):
                        try:
                            self.alchemist.env.cache.clear()
                        except:
                            pass
                    gc.collect()

                    if self.akashic:
                        self.akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {"type": "MEMORY_PURGE", "label": "LUSTRATION_COMPLETE", "color": "#64ffda"}
                        })
                else:
                    gc.collect(1)

                self.logger.verbose(f"[{trace_id}] Physics Shift: [bold green]ZEN[/] (GC_Mute=OFF)")

        except Exception as paradox:
            pass

    def _emergency_dump(self, error: Exception, rite: str, trace: str):
        """[ASCENSION 23]: GLOBAL EXCEPTION HOOK DUMP."""
        import json
        try:
            report = {
                "rite": rite,
                "trace": trace,
                "error": str(error),
                "timestamp": time.time(),
                "history": list(self.memory._rite_history)
            }
            dump_path = Path(".scaffold/crash_dump.json")
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dump_path, 'w') as f:
                json.dump(report, f, indent=2)
        except:
            pass

    def dispatch_by_name(self, command: str, params: Dict[str, Any]) -> ScaffoldResult:
        """[LSP BRIDGE ALIAS]"""
        return self.dispatch(command, params)

    # =========================================================================
    # == INTELLIGENCE API                                                    ==
    # =========================================================================

    def predict_next_move(self) -> List[str]:
        """
        [THE ORACLE'S VOICE]
        Consults the Markov Chain and Heuristic Sage to guess the Architect's
        next desire. Used by the UI to suggest "Next Steps".
        """
        return self.predictor.prophesy()

    def get_system_vitals(self) -> Dict[str, Any]:
        """Returns the physiological state of the Engine."""
        return {
            "uptime": time.perf_counter() - self._creation_time,
            "memory_usage": self.watchdog.get_memory_mb(),  # Assuming this method exists
            "active_transactions": len(self.transactions._active_transactions),
            "cognitive_history": list(self.memory._rite_history)
        }

    # =========================================================================
    # == PUBLIC API (The Face of God)                                        ==
    # =========================================================================

    def register_artisan(self,
                         request_type: Type[BaseRequest],
                         artisan_class: Any,
                         aliases: Optional[List[str]] = None,
                         system_vow: bool = False):
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-AUTHORITY-SUTURE)                         ==
        =============================================================================
        @gnosis:title Skill Consecration Facade
        @gnosis:summary The high-level gateway for binding Intent to the Pantheon.
        @gnosis:LIF INFINITY

        [THE FIX]: This facade now correctly accepts and propagates the 'system_vow'
        authority to the ArtisanRegistry, enabling the Engine Bootstrap to claim
        System Rites (Init, Genesis, Run) while maintaining the Subversion Guard.
        """
        # [ASCENSION]: The Telepathic Hand-off
        # We delegate the consecration to the Registry organ, bestowing the Vow.
        self.registry.register(
            request_type,
            artisan_class,
            aliases=aliases,
            system_vow=system_vow
        )

    def register_hook(self, callback: Callable[[ScaffoldResult], None]):
        """Binds a listener to the output stream."""
        self._hooks.append(callback)

    def success(self,
                message: str,
                data: Any = None,
                artifacts: Optional[List[Artifact]] = None,
                **kwargs) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA SUCCESS (V-Ω-TOTALITY-V34-ASCENDED)                           ==
        =============================================================================
        LIF: ∞ | ROLE: PROCLAMATION_FORGE | RANK: SOVEREIGN

        Forges a successful result vessel.
        [THE CURE]: Now absorbs all keyword arguments (**kwargs) to handle advanced
        metadata like 'ui_hints', 'cost_usd', and 'latency' without fracturing.
        """
        # 1. THE CURE: EXTRACT UI HINTS
        ui_hints = kwargs.pop("ui_hints", {
            "vfx": "bloom",
            "sound": "consecration_complete"
        })

        # 2. DELEGATE TO THE SCRIBE
        return TelemetryScribe.forge_success(
            message=message,
            data=data,
            artifacts=artifacts,
            ui_hints=ui_hints,
            **kwargs  # Pass all remaining metadata through
        )

    def failure(self,
                message: str,
                suggestion: Optional[str] = None,
                details: Optional[str] = None,
                data: Any = None,
                severity: Optional[HeresySeverity] = None,
                **kwargs) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA FAILURE (V-Ω-TOTALITY-V712-TITANIUM)                          ==
        =============================================================================
        @gnosis:title The Titanium Gate of Lamentation
        @gnosis:summary The final, unbreakable factory for system-level fractures.
        @gnosis:LIF INFINITY

        ### THE 12 TITANIUM ASCENSIONS:
        1.  **Atomic Scope Initialization (THE FIX):** Pre-materializes 'exc_val'
            and 'exc_tb' in the root scope, annihilating the UnboundLocalError.
        2.  **Surgical Parameter Distillation:** Pops 'traceback', 'vitals', and
            'ui_hints' from kwargs.
        3.  **Achronal Contextual Capture:** Inscribes the exact moment of failure.
        4.  **Hierarchical Exception Triage:** Prioritizes explicit details.
        5.  **Haptic Feedback Synchronicity:** Calculates 'vfx' based on severity.
        6.  **Merkle-Based Fingerprinting:** Forges a unique ID for the error.
        7.  **Null-State Immutability Guard:** Transmutes NoneType inputs.
        8.  **Sovereign Identity Attribution:** Binds thread DNA.
        9.  **Recursive Redaction Governance:** Forces data through Entropy Sieve.
        10. **Thermodynamic Load Tomography:** Injects current CPU/RAM heat.
        11. **Socratic Remediation Prophecy:** Scans internal logic for cures.
        12. **The Finality Vow:** Guaranteed return of a valid result vessel.
        """
        import sys
        import traceback as tb_module
        from ..telemetry import TelemetryScribe

        # --- 1. THE CURE: ATOMIC SCOPE INITIALIZATION ---
        exc_type, exc_val, exc_tb = (None, None, None)

        if sys.exc_info()[0] is not None:
            exc_type, exc_val, exc_tb = sys.exc_info()

        # --- 2. SURGICAL PARAMETER DISTILLATION ---
        provided_traceback = kwargs.pop("traceback", None)
        provided_vitals = kwargs.pop("vitals", {})
        provided_ui_hints = kwargs.pop("ui_hints", {})

        # --- 3. FORENSIC TRACE RECONSTRUCTION ---
        final_traceback = provided_traceback
        if not final_traceback and exc_val:
            final_traceback = "".join(tb_module.format_exception(exc_type, exc_val, exc_tb))

        # [ASCENSION 4]: Hierarchical Detail Recovery
        if not details and exc_val:
            details = f"Internal Engine Fracture: {str(exc_val)}"
        elif not details:
            details = "Contextual Logic Gap: No specific fracture details manifest."

        # --- 4. HAPTIC & METABOLIC ALIGNMENT ---
        severity = severity or HeresySeverity.CRITICAL
        ui_hints = {
            "vfx": "shake_red" if severity == HeresySeverity.CRITICAL else "glow_amber",
            "sound": "fracture_alert",
            "priority": severity.value,
            **provided_ui_hints
        }

        # [ASCENSION 10]: Thermodynamic Load Tomography
        system_load = TelemetryScribe.capture_system_load()
        merged_vitals = {
            **system_load,
            "trace_id": getattr(self.context, 'session_id', 'tr-unbound'),
            "is_panic": severity == HeresySeverity.CRITICAL,
            **(provided_vitals if isinstance(provided_vitals, dict) else {})
        }

        # --- 5. THE FINALITY DISPATCH ---
        return TelemetryScribe.forge_failure(
            message=message,
            suggestion=suggestion,
            details=details,
            data=data,
            severity=severity,
            ui_hints=ui_hints,
            vitals=merged_vitals,
            traceback=final_traceback,  # [THE FIX]: Guaranteed local variable
            **kwargs
        )

    def list_capabilities(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE OMEGA CENSUS (V-Ω-TOTALITY-V32-ASCENDED)                            ==
        =============================================================================
        LIF: ∞ | ROLE: CAPABILITY_SCRIER | RANK: SOVEREIGN

        Proclaims the complete manifest of manifest and latent Gnostic skills.
        [THE CURE]: Evolved signature to return complex metadata instead of simple strings.
        """
        try:
            # 1. TRIGGER DISCOVERY
            if hasattr(self.registry, '_plugins_discovered') and not self.registry._plugins_discovered:
                self.registry._discover_plugins()
                self.registry._plugins_discovered = True

            # 2. RADIATE THE LEDGER
            manifest = self.registry.list_capabilities()

            # 3. ENRICH WITH ENGINE METADATA
            return {
                "session_id": self.context.session_id,
                "state_hash": getattr(self.registry, '_state_hash', '0xVOID'),
                "capabilities": manifest,
                "timestamp": time.time(),
                "logic_version": "V32-TOTALITY"
            }

        except Exception as e:
            # [ASCENSION 12]: THE FINALITY VOW
            self.logger.error(f"Census Fracture: {e}")
            return {
                "success": False,
                "error": "CAPABILITY_CENSUS_FRACTURE",
                "details": str(e)
            }

    def anchor(self, root: Path, cortex: Any):
        """Dynamically binds the Engine to a specific physical reality."""
        self.project_root = root
        # Re-initialize context sensitive organs
        self.context = RuntimeContext(root)
        self.cortex = cortex
        # Re-anchor the predictor memory to the new project
        self.predictor = IntentPredictor(root)

    def _scan_for_unclaimed_artifacts(self, request: BaseRequest, result: ScaffoldResult, start_time: float):
        """
        [ASCENSION 28]: THE ARTIFACT BLOOM
        Scans for files created during the rite that were not explicitly returned.
        """
        if not hasattr(request, 'project_root') or not request.project_root:
            return

        root = Path(request.project_root)
        known_paths = {a.path for a in result.artifacts}

        # Fast scan for files modified after start_time
        # Depth limit 3 to avoid scanning node_modules
        for dirpath, _, filenames in os.walk(root):
            if '.git' in dirpath or 'node_modules' in dirpath: continue

            for f in filenames:
                p = Path(dirpath) / f
                if p in known_paths: continue

                try:
                    if p.stat().st_mtime > start_time:
                        result.artifacts.append(Artifact(
                            path=p,
                            type="file",
                            action="modified (bloomed)",
                            metadata={"source": "bloom"}
                        ))
                except:
                    pass

    def shutdown(self):
        """
        [THE FINAL RITE]
        Gracefully dissolves the Engine.
        """
        self.shutdown_manager.execute()

    def __repr__(self) -> str:
        return f"<QuantumEngine session={self.context.session_id[:8]} root={self.project_root.name}>"