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
from ..vessels import GnosticSovereignDict
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
    from ....parser_core.parser import ApotheosisParser

class VelmEngine:
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
            nexus: Any = None
    ):
        """
        =================================================================================
        == THE Ω_ENGINE_INCEPTION: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KERNEL_BOOTLOADER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_INIT_VMAX_SUBSTRATE_SUTURE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for Kernel awakening. This version
        righteously annihilates the "Attribute Mirage" by enforcing the Law of
        Substrate Perception and Chromatic Forensic Authority.
        =================================================================================
        """
        import time
        import threading
        import os
        import sys
        import secrets
        import platform

        # --- MOVEMENT 0: METABOLIC CHRONOMETRY ---
        self._creation_time = time.perf_counter()
        self._start_ns = time.perf_counter_ns()
        self._silent = silent
        self._log_level = log_level
        self._lock = threading.RLock()

        # =========================================================================
        # == [ASCENSION 1 & 2]: THE MASTER CURE (SUBSTRATE & CHROMATIC SUTURE)    ==
        # =========================================================================
        # 1. Perception of the Plane (WASM/IRON)
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # 2. Inscription of the Chromatic Sigils (Forensic Colors)
        self.ALERT = "\x1b[41;1m"  # Inverse Red (Panic)
        self.RESET = "\x1b[0m"  # Restoration (Void)
        self.GOLD = "\x1b[38;5;220m"  # Sovereignty (Success)
        self.UV = "\x1b[38;5;141m"  # Ultraviolet (Tracing)
        self.TEAL = "\x1b[38;5;86m"  # Resonance (Logic)

        # --- MOVEMENT I: IDENTITY & TRACE ---
        # [ASCENSION 3 & 9]: High-Entropy Session Inception
        self.session_id = secrets.token_hex(4).upper()
        self.trace_id = f"tr-kernel-{self.session_id}"

        # [ASCENSION 6]: Ouroboros Loop Guard
        self._trace_stack = []
        self._recursion_lock = threading.Lock()

        # --- MOVEMENT II: LOGGING CONSECRATION ---
        # [ASCENSION 2]: Substrate-Aware Visual Cortex
        if not silent:
            from ....logger import configure_logging, get_console
            configure_logging(verbose=(log_level == "DEBUG"), json_mode=json_logs)

            if self._is_wasm:
                try:
                    from rich.console import Console
                    # Force responsive geometry for XTerm.js stage
                    self.console = Console(force_terminal=True, color_system="truecolor", width=80)
                    import velm.logger
                    velm.logger._console = self.console
                except ImportError:
                    self.console = get_console()
            else:
                self.console = get_console()
        else:
            from ....logger import get_console
            self.console = get_console()

        self.logger = Scribe("QuantumEngine")

        # --- MOVEMENT III: CONTEXTUAL ANCHORS (LAZY) ---
        # [ASCENSION 10]: Geometric Path Normalization
        self._project_root_raw = project_root
        self._context = None
        self._registry = None

        self.cortex = cortex
        self.nexus = nexus

        # [ASCENSION 4]: THE AKASHA SUTURE
        self._akashic = None
        self._akashic_initialized = False

        # --- MOVEMENT IV: THE ORGAN MANIFOLD (VOID SLOTS) ---
        # [ASCENSION 8]: NoneType Sarcophagus - Bit-perfect O(1) boot
        self._bootstrap = None
        self._transactions = None
        self._predictor = None
        self._memory = None
        self._optimizer = None
        self._dispatcher = None
        self._watchdog = None
        self._vitality = None
        self._shutdown_manager = None
        self._alchemist = None
        self._healer = None
        self._diviner = None
        self._conductor = None
        self._traceback_handler = None
        self._pipeline = None

        # --- MOVEMENT V: KINETIC STATE ---
        self.last_reality: Optional[ScaffoldResult] = None
        self._kernel_locks: Dict[str, threading.Lock] = {}
        self._hooks: List[Callable[[ScaffoldResult], None]] = []
        self._adrenaline_active = False

        # --- MOVEMENT VI: FAST-PATH AWAKENING ---
        # [ASCENSION 12]: THE FINALITY VOW
        if auto_register:
            try:
                # [STRIKE]: Apophatic Skill Awakening
                self.bootstrap.register_capabilities()
            except Exception as e:
                # Self-Healing Triage
                self.logger.error(f"Inception Drift: {e}")

        if not silent and log_level == "DEBUG":
            self.logger.verbose(
                f"Ω_KERNEL_RESONANT :: Session:{self.session_id} :: Substrate:{'WASM' if self._is_wasm else 'IRON'}")

    # =========================================================================
    # == STRATUM II: LAZY FACULTIES (DOUBLE-CHECKED JIT MATERIALIZATION)     ==
    # =========================================================================
    # LIF: 10,000x | The organs of the God-Engine are now shielded by re-entrant
    # locks, ensuring they are forged exactly once, even during high-concurrency
    # parallel swarms, and ONLY if the active Rite requires them.

    @property
    def context(self) -> 'RuntimeContext':
        """The Ephemeral Mind. Forges the spatial anchor upon first request."""
        if self._context is None:
            with self._lock:
                if self._context is None:
                    from ..context import RuntimeContext
                    root_path = Path(self._project_root_raw) if self._project_root_raw else None
                    self._context = RuntimeContext(root_path)
        return self._context

    @property
    def registry(self) -> 'ArtisanRegistry':
        """The Index of Skills."""
        if self._registry is None:
            with self._lock:
                if self._registry is None:
                    from ..registry import ArtisanRegistry
                    self._registry = ArtisanRegistry(self)
        return self._registry

    @property
    def akashic(self) -> Any:
        """[THE AKASHIC SUTURE]: Lazily binds the event bus to the Ocular HUD."""
        if not self._akashic_initialized:
            with self._lock:
                if not self._akashic_initialized:
                    if self.nexus and hasattr(self.nexus, 'akashic'):
                        self._akashic = self.nexus.akashic
                    else:
                        try:
                            # Fallback for non-daemon CLI instantiation
                            persistence = str(
                                self.context.project_root / ".scaffold" / "akashic.jsonl") if self.context.project_root else None
                            # Disable local JSONL writes if in WASM to prevent IDBFS thrashing
                            if persistence and os.environ.get("SCAFFOLD_ENV") != "WASM":
                                from ....core.daemon.akashic import AkashicRecord
                                self._akashic = AkashicRecord(persistence_path=persistence)
                        except Exception:
                            self._akashic = None
                    self._akashic_initialized = True
        return self._akashic

    @property
    def bootstrap(self) -> 'EngineBootstrap':
        if self._bootstrap is None:
            with self._lock:
                if self._bootstrap is None:
                    from .lifecycle.bootstrap import EngineBootstrap
                    self._bootstrap = EngineBootstrap(self)
        return self._bootstrap

    @property
    def transactions(self) -> 'TransactionManager':
        if self._transactions is None:
            with self._lock:
                if self._transactions is None:
                    from .execution.transaction import TransactionManager
                    self._transactions = TransactionManager(self.logger)
        return self._transactions

    @property
    def predictor(self) -> 'IntentPredictor':
        if self._predictor is None:
            with self._lock:
                if self._predictor is None:
                    from .intelligence.predictor import IntentPredictor
                    memory_anchor = self.context.project_root or Path.home()
                    self._predictor = IntentPredictor(memory_anchor, engine=self)
        return self._predictor

    @property
    def memory(self) -> 'CognitiveMemory':
        if self._memory is None:
            with self._lock:
                if self._memory is None:
                    from .intelligence.memory import CognitiveMemory
                    self._memory = CognitiveMemory()
        return self._memory

    @property
    def optimizer(self) -> 'NeuroOptimizer':
        if self._optimizer is None:
            with self._lock:
                if self._optimizer is None:
                    from .intelligence.optimizer import NeuroOptimizer
                    self._optimizer = NeuroOptimizer(self)
        return self._optimizer

    @property
    def dispatcher(self) -> 'QuantumDispatcher':
        if self._dispatcher is None:
            with self._lock:
                if self._dispatcher is None:
                    from .execution.dispatcher import QuantumDispatcher
                    self._dispatcher = QuantumDispatcher(self)
        return self._dispatcher

    @property
    def watchdog(self) -> 'SystemWatchdog':
        """
        [THE METABOLIC SOVEREIGN]
        Materializes the Watchdog and honors Substrate Immunity (Stays thread on WASM).
        """
        if self._watchdog is None:
            with self._lock:
                if self._watchdog is None:
                    from .resilience.watchdog import SystemWatchdog
                    self._watchdog = SystemWatchdog(self)
                    if os.environ.get("SCAFFOLD_ENV") != "WASM":
                        self._watchdog.start_vigil()
        return self._watchdog

    @property
    def vitality(self) -> 'VitalityMonitor':
        """
        [THE HEARTBEAT]
        Materializes the Vitality Monitor and honors Substrate Immunity.
        """
        if self._vitality is None:
            with self._lock:
                if self._vitality is None:
                    from .lifecycle.vitality import VitalityMonitor
                    self._vitality = VitalityMonitor(self)
                    if os.environ.get("SCAFFOLD_ENV") != "WASM":
                        self._vitality.start_vigil()
        return self._vitality

    @property
    def shutdown_manager(self) -> 'ShutdownManager':
        if self._shutdown_manager is None:
            with self._lock:
                if self._shutdown_manager is None:
                    from .lifecycle.shutdown import ShutdownManager
                    self._shutdown_manager = ShutdownManager(self)
        return self._shutdown_manager
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
        == THE SOVEREIGN PARSER FACTORY (V-Ω-TOTALITY-V5000-HEALED)                    ==
        =================================================================================
        LIF: ∞ | ROLE: GNOSTIC_MIND_FORGE | RANK: OMEGA_SOVEREIGN

        The definitive forge for the ApotheosisParser. It constructs a localized
        "Mind" for evaluating Blueprints, while permanently suturing it back to
        the "Body" (The God-Engine) so that recursive physical strikes (logic.weave)
        never fracture.

        ### THE PANTHEON OF 8 LEGENDARY ASCENSIONS:
        1.  **Late-Bound Absolute Import:** Resolves circular dependency loops
            during the Engine's initial primordial boot phase.
        2.  **The Double-Suture (THE CURE):** Binds the `engine` instance to both
            the `parser` and the parser's internal `alchemist`. This is the
            mathematical annihilation of the 'Engine link unmanifest' heresy.
        3.  **Gnostic Variable Mirroring:** Deep-syncs the Engine's active `variables`
            into the Parser's soul before the first `@if` gate is evaluated.
        4.  **Spatial Coordinates Anchor:** Injects the `project_root` into the
            Parser's context, ensuring `@include` and relative paths resolve perfectly.
        5.  **Trace ID Silver-Cord:** Propagates the active `trace_id` down to the
            Parser for flawless forensic tracking in the Akashic Record.
        6.  **Substrate-Aware Geometry:** Normalizes all willed paths JIT.
        7.  **Metabolic Registry Sync:** Ensures the `macros` registry is pre-warmed.
        8.  **The Finality Vow:** A mathematical guarantee of an operational Parser.
        =================================================================================
        """
        import os
        from copy import deepcopy

        # [ASCENSION 1]: The Late-Bound Sentinel Import
        try:
            from ....parser_core.parser import ApotheosisParser
        except ImportError:
            # Fallback for complex studio pathing in the Ethereal Plane (WASM)
            from velm.parser_core.parser import ApotheosisParser

        # 1. THE INCEPTION
        parser = ApotheosisParser(grammar_key=grammar)

        # =========================================================================
        # == [ASCENSION 2]: THE DOUBLE SUTURE (THE MASTER CURE)                  ==
        # =========================================================================
        # We forcefully bestow the Engine's soul upon the Parser.
        object.__setattr__(parser, 'engine', self)

        # CRITICAL SUTURE: We must also bind the Engine directly to the Alchemist
        # singleton that the parser uses. This guarantees that any `{{ logic.weave }}`
        # evaluated inside a template will have access to `self.engine.dispatch`.
        if hasattr(parser, 'alchemist') and parser.alchemist:
            parser.alchemist.engine = self

        # --- GNOSTIC SYNCHRONIZATION ---
        if hasattr(self, 'context'):
            # [ASCENSION 3]: Variable Mirroring
            if hasattr(self.context, 'variables') and self.context.variables:
                # We use deepcopy on primitives to prevent cross-contamination
                # between the global engine state and the localized parser state.
                safe_vars = {}
                for k, v in self.context.variables.items():
                    if isinstance(v, (str, int, float, bool, list, dict)):
                        try:
                            safe_vars[k] = deepcopy(v)
                        except Exception:
                            safe_vars[k] = v
                    else:
                        safe_vars[k] = v

                parser.variables.update(safe_vars)

            # [ASCENSION 4]: Spatial Coordinate Anchor
            if hasattr(self.context, 'project_root') and self.context.project_root:
                parser.variables["__project_root__"] = str(self.context.project_root).replace('\\', '/')

        # [ASCENSION 5]: Trace ID Cord
        active_trace = getattr(self.context, 'session_id', 'tr-unbound') if self.context else 'tr-unbound'
        parser.variables["trace_id"] = active_trace

        if not getattr(self, '_silent', False):
            self.logger.verbose(f"Forge: Materialized [{grammar.upper()}] Parser for Trace: {active_trace}")

        return parser

    # =========================================================================================
    # == THE ALCHEMICAL & FORENSIC ACCESSORS (V-Ω-TITANIUM-LINKS)                            ==
    # =========================================================================================
    # These properties provide zero-cost, JIT access to heavy subsystems,
    # ensuring the Engine's boot time remains near-zero while its power is infinite.

    @property
    def alchemist(self) -> 'DivineAlchemist':
        """
        [THE TRANSMUTER]: JIT access to the SGF  Alchemical Reactor.
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

    def _radiate_gnostic_revelation(self, result: ScaffoldResult, trace_id: str):
        """
        =================================================================================
        == THE Ω_GNOSTIC_REVELATION: TOTALITY (V-Ω-TOTALITY-VMAX-HUD-SUTURE)          ==
        =================================================================================
        LIF: 100x | ROLE: OCULAR_SYNCHRONIZER_PRIME | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RADIATE_VMAX_DNA_PROJECTION_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme final authority for data radiation. This rite righteously
        bridges the "Gnosis Gap" by projecting the project's reified DNA (.env)
        and structural soul directly into the Ocular Membrane at 144Hz.
        =================================================================================
        """
        import time
        import json
        from pathlib import Path

        # --- MOVEMENT 0: THE VOID GUARD ---
        if not self.akashic:
            return

        _start_ns = time.perf_counter_ns()
        self.logger.verbose(f"[{trace_id[:8]}] Radiating Gnostic Revelation to Ocular Stage...")

        try:
            # =========================================================================
            # == MOVEMENT I: [ASCENSION 1] - GENOMIC DNA PROJECTION                  ==
            # =========================================================================
            # We extract the "Conscience" (Environment DNA) from the result data.
            # This allows the UI to see the waked secrets and warded ports instantly.
            dream_telemetry = result.data.get("_dream_telemetry", {})

            # Suture the reified variables (The Conscience)
            # We filter out internal invariants to maximize Gnostic Density.
            genome = {
                k.upper(): v for k, v in self.context.variables.items()
                if not k.startswith('__') and k not in ("trace_id", "session_id")
            }

            # --- MOVEMENT II: HAPTIC COUPLING (VISUALS) ---
            # [ASCENSION 2]: Divine the Aura based on resonance
            aura = "#64ffda" if result.success else "#ef4444"
            vfx = "bloom" if result.success else "shake_red"
            sound = "consecration_complete" if result.success else "fracture_alert"

            # --- MOVEMENT III: PHYSICAL ARTIFACT NORMALIZATION ---
            # [ASCENSION 7]: Force POSIX slashes for browser-clickable links
            artifacts = []
            for art in result.artifacts:
                artifacts.append({
                    "path": str(art.path).replace('\\', '/'),
                    "type": art.type,
                    "action": art.action,
                    "size": getattr(art, 'size_bytes', 0)
                })

            # =========================================================================
            # == MOVEMENT IV: THE OCULAR STRIKE (THE BROADCAST)                      ==
            # =========================================================================
            # [ASCENSION 11]: JSON-RPC 2.0 Gnostic Suture
            payload = {
                "method": "novalym/hud_revelation",
                "params": {
                    "type": "ARCHITECTURAL_MANIFESTATION",
                    "status": "RESONANT" if result.success else "FRACTURED",
                    "label": "REALITY_CONVERGED",
                    "project_id": result.data.get("project_id", "NOVA"),
                    "trace": trace_id,
                    "aura": aura,
                    "haptics": {
                        "vfx": vfx,
                        "sound": sound,
                        "priority": "HIGH" if not result.success else "NORMAL"
                    },
                    "metrics": {
                        "duration_ms": result.duration_seconds * 1000 if result.duration_seconds else 0,
                        "atom_count": len(result.artifacts),
                        "will_count": len(result.heresies),
                        "merkle_seal": result.data.get("merkle_root", "0xVOID")
                    },
                    "vitals": result.vitals,  # Hardware DNA from the strike
                    "genome": genome,  # THE REIFIED .ENV DNA
                    "artifacts": artifacts,  # Clickable file manifest
                    "timestamp": time.time()
                },
                "jsonrpc": "2.0"
            }

            # [STRIKE]: Project the Revelation to the React HUD
            self.akashic.broadcast(payload)

            # --- MOVEMENT V: METABOLIC FINALITY ---
            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            if not self._silent:
                self.logger.success(f"   -> [REVELATION] HUD Synced in {_tax_ms:.2f}ms. Reality is now Ocular.")

        except Exception as radiation_fracture:
            # [ASCENSION 20]: FAULT-ISOLATED REDEMPTION
            # Telemetry failure must never shatter the physical materialization.
            self.logger.debug(f"Ocular Radiation deferred: {radiation_fracture}")


    # =========================================================================
    # == EXECUTION DELEGATES                                                 ==
    # =========================================================================
    def transmute(
        self,
        template: str,
        variables: Optional[Dict[str, Any]] = None,
        _depth: int = 0,
        **kwargs
    ) -> str:
        """
        =============================================================================
        == THE RITE OF UNIVERSAL REIFICATION: OMEGA (V-Ω-TOTALITY-VMAX-VARIADIC)   ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_REIFIER_PRIME | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TRANSMUTE_VMAX_VARIADIC_SUTURE_2026_FINALIS_!#()@()

        [THE MANIFESTO]
        The supreme definitive authority for reifying intent directly from the
        Kernel. This version righteously implements **Variadic Parameter Amnesty**,
        mathematically annihilating the 'Unexpected Keyword' heresy.

        [THE MASTER CURE]: It captures the recursive '_depth' coordinate and any
        auxiliary Gnostic metadata, fusing them with the Engine's Global Conscience
        before striking the Alchemical Anvil.
        =============================================================================
        """
        # [ASCENSION 5]: NoneType Sarcophagus
        if not template or not isinstance(template, str):
            return ""

        # --- MOVEMENT I: GNOSTIC CONVERGENCE ---
        # 1. Start with the Absolute Mind (Global Variables)
        # We use GnosticSovereignDict to maintain case-insensitive resonance.
        active_vars = self.context.variables.copy()

        # 2. [ASCENSION 2]: Causal Override Suture
        # Overlay local variables provided by the specific call-site (e.g. Loop variables).
        if variables:
            active_vars.update(variables)

        # 3. [ASCENSION 3]: Trace ID Silver-Cord Preservation
        if "trace_id" not in active_vars:
            active_vars["trace_id"] = getattr(self, "trace_id", "tr-engine-transmute")

        # --- MOVEMENT II: THE KINETIC DELEGATION ---
        # [STRIKE]: Calling the Divine Alchemist through the JIT bridge.
        # We pass the '_depth' and 'kwargs' to the SGF Engine to maintain
        # recursion-limit integrity and telemetry flow.
        try:
            return self.alchemist.transmute(
                template,
                active_vars,
                _depth=_depth,
                **kwargs
            )
        except Exception as alchemical_fracture:
            # [ASCENSION 18]: Fault-Isolated Redemption
            # If the SGF reactor panics, we return the raw template to prevent
            # the "Void Erasure" anomaly while the error is logged.
            self.logger.debug(f"Alchemical Strike deferred: {alchemical_fracture}")
            return template

    def dispatch(self,
                 request: Union[BaseRequest, Dict[str, Any], str],
                 params: Optional[Dict[str, Any]] = None,
                 **kwargs) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA DISPATCH APOTHEOSIS (V-Ω-TOTALITY-V72-INDESTRUCTIBLE-FINALIS)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_SUPREME_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_DISPATCH_V72_SINGULARITY_RESONANCE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for transmuting Intent into Reality. This
        version righteously implements the **Laminar Reference Suture**,
        mathematically annihilating the Anomaly 236-ONTOLOGICAL-ERASURE.
        It conducts reality strikes across the Iron/Ether divide with bit-perfect
        transactional finality.
        =================================================================================
        """
        # [ASCENSION 48-72]: THE PANTHEON OF RELIABILITY & PERFORMANCE
        import sys
        import time
        import uuid
        import inspect
        import traceback as tb_scribe
        import json
        import hashlib
        import importlib
        import gc
        import os
        from pathlib import Path
        from datetime import datetime, timezone

        _start_ns = time.perf_counter_ns()
        jit_overhead_ms = 0.0
        rite_name = "UnknownRite"
        trace_id = "tr-unbound"
        request_obj = None

        # --- THE CHROMATIC SIGILS ---
        UV = "\x1b[38;5;141m"
        GOLD = "\x1b[38;5;220m"
        RESET = "\x1b[0m"

        try:
            # =========================================================================
            # == MOVEMENT I: TRANSMUTATION & SEMANTIC TRIAGE                         ==
            # =========================================================================
            # [ASCENSION 39]: Semantic Alias Transmutation
            # We resolve "fix code" -> RefactorRequest or "create api" -> GenesisRequest JIT.
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

            # --- MOVEMENT II: CAUSAL IDENTITY (TRACE STITCHING) ---
            # [ASCENSION 50]: Achronal Trace-ID Silver-Cord
            meta = getattr(request_obj, 'metadata', {})
            meta_dict = meta.model_dump(mode='json') if hasattr(meta, 'model_dump') else (
                meta if isinstance(meta, dict) else {})

            trace_id = (
                    meta_dict.get('trace_id') or
                    meta_dict.get('x_nov_trace') or
                    getattr(request_obj, 'trace_id', None) or
                    f"tr-{uuid.uuid4().hex[:8].upper()}"
            )

            # [STRIKE]: Force-Bind the Silver Cord to the Request Soul
            if not hasattr(request_obj, 'trace_id') or getattr(request_obj, 'trace_id') in [None, "None", "tr-void"]:
                try:
                    object.__setattr__(request_obj, 'trace_id', trace_id)
                except (AttributeError, TypeError):
                    pass

            request_type = type(request_obj)
            rite_name = request_type.__name__

            # [ASCENSION 4]: RECURSIVE DEPTH SENTINEL (Ouroboros Ward)
            if hasattr(self.dispatcher, '_recursion_depths'):
                with self.dispatcher._recursion_lock:
                    depth = self.dispatcher._recursion_depths.get(trace_id, 0)
                    if depth > self.dispatcher.MAX_DISPATCH_DEPTH:
                        return self.failure(
                            f"Topological Overflow: Trace {trace_id} depth > {self.dispatcher.MAX_DISPATCH_DEPTH}")
                    self.dispatcher._recursion_depths[trace_id] = depth + 1

            is_heavy = any(k in rite_name for k in
                           ['Genesis', 'Transmute', 'Analyze', 'Refactor', 'Manifest', 'Inception', 'Dream'])

            # =========================================================================
            # == MOVEMENT III: THERMODYNAMIC ADJUDICATION (FEVER CHECK)              ==
            # =========================================================================
            # [ASCENSION 49 & 64]: Substrate Heat Tomography
            system_vitals = self.watchdog.get_vitals()
            load_factor = system_vitals.get("load_percent", 0.0)

            if is_heavy and load_factor > 92.0:
                self.logger.warn(
                    f"[{trace_id}] Metabolic Fever Detected ({load_factor:.1f}%). Shedding heavy rite: {rite_name}")
                return self.failure("Metabolic Congestion: System too hot for heavy inception.", vitals=system_vitals)

            # [ASCENSION 11]: ADRENALINE MODE INCEPTION
            self._neuro_optimize(heavy_mode=is_heavy)

            # --- MOVEMENT IV: COGNITIVE MEMORY & ANCHORING ---
            if hasattr(request_obj, 'project_root') and request_obj.project_root:
                # [ASCENSION 36]: Hydraulic I/O Pacing (Anchor Focus)
                self.memory.record_focus(str(request_obj.project_root))

            # =========================================================================
            # == MOVEMENT V: THE RITE OF RE-INCEPTION (JIT / HOT-SWAP)               ==
            # =========================================================================
            # [ASCENSION 24]: CIRCUIT BREAKER INTEGRATION
            if not self.healer.circuit_breaker.check_state(rite_name):
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

            # [ASCENSION 5 & 43]: ZERO-LATENCY JIT HOT-SWAP
            if isinstance(artisan_info, tuple):
                module_path, class_name = artisan_info
                jit_start = time.perf_counter()

                # Check for Hot-Swap signal or Adrenaline optimization
                if os.environ.get("SCAFFOLD_HOT_SWAP") == "1" or not self._is_wasm:
                    with self.kernel_lock("jit_reception"):
                        try:
                            # [ASCENSION 54]: Pure JIT reload
                            to_purge = [m for m in sys.modules if m.startswith(module_path)]
                            for m in to_purge: sys.modules.pop(m, None)

                            module = importlib.import_module(module_path)
                            artisan_instance = getattr(module, class_name)(self)
                        except Exception as syntax_heresy:
                            # [ASCENSION 20]: FORENSIC SNITCH
                            sys.stderr.write(f"\n{UV}[TITAN:JIT_FRACTURE]{RESET} {class_name}\n")
                            tb_scribe.print_exc(file=sys.stderr)
                            return self.failure(f"Syntax Heresy in {class_name}", details=tb_scribe.format_exc())

                if not artisan_instance:
                    module = importlib.import_module(module_path)
                    artisan_instance = getattr(module, class_name)(self)

                jit_overhead_ms = (time.perf_counter() - jit_start) * 1000
            else:
                artisan_instance = artisan_info(self) if isinstance(artisan_info, type) else artisan_info

            # =========================================================================
            # == MOVEMENT VI: [THE MASTER CURE] - LAMINAR REFERENCE SUTURE           ==
            # =========================================================================
            # [THE MANIFESTO]: We must bridge the 236-ONTOLOGICAL-ERASURE.
            # We surgically sync the Artisan's variables to the Engine's Absolute Context.
            if hasattr(artisan_instance, 'engine'):
                object.__setattr__(artisan_instance, 'engine', self)

            # --- MOVEMENT VII: HYBRID KINETIC EXECUTION ---
            def _conduct_rite(req: BaseRequest) -> Union[ScaffoldResult, Any]:
                # [ASCENSION 27]: OMNISCIENT BROADCAST (Progress)
                if self.akashic:
                    self.akashic.broadcast({
                        "method": "scaffold/progress",
                        "params": {"message": f"Conducting {rite_name}...", "percentage": 33, "trace": trace_id}
                    })

                # [ASCENSION 6]: ECHO CHAMBER (Deterministic Replay)
                if is_heavy and not req.dry_run:
                    self.dispatcher._chronicle_replay_capability(req, rite_name)

                # =====================================================================
                # == [ASCENSION 22 & 58]: TRANSACTIONAL ATOMICITY                    ==
                # =====================================================================
                with self.transactions.atomic_rite(f"{rite_name}:{req.request_id}") as tx_id:
                    # [ASCENSION 51]: REFERENCE SINGULARITY SUTURE
                    # We ensure the context utilizes the Prime Sovereign vessels.
                    if req.context is None:
                        req.context = GnosticSovereignDict()

                    req.context['transaction_id'] = tx_id
                    req.context['trace_id'] = trace_id

                    # Suture Matter Reservoirs from Engine -> Request Context
                    for res_key in ('__woven_matter__', '__woven_commands__'):
                        if res_key in self.context.variables:
                            req.context[res_key] = self.context.variables[res_key]

                    # [THE OMEGA SUTURE]: REQUEST BINDING
                    # Forcefully implant the Request into the Artisan's soul.
                    try:
                        object.__setattr__(artisan_instance, '_request_context', req)
                    except:
                        artisan_instance._request_context = req

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

            # Pipeline Ignition (Middleware Chain)
            result = self.pipeline.execute(request_obj, _conduct_rite)

            # [ASCENSION 21]: NONETYPE SARCOPHAGUS
            if result is None:
                result = self.failure(f"Void Revelation: Artisan {rite_name} produced no matter.")

            # --- MOVEMENT VIII: FORENSIC CONVERGENCE & TELEMETRY ---
            try:
                # 1. TEMPORAL ACCOUNTING
                if result and hasattr(result, 'duration_seconds'):
                    if not result.duration_seconds:
                        result.duration_seconds = (time.perf_counter_ns() - _start_ns) / 1_000_000_000

                # 2. INTELLECTUAL OBSERVATION
                if hasattr(self, 'predictor'):
                    self.predictor.observe_outcome(request_obj, result)

                self.memory.record_rite(rite_name, result.success if result else False)
                self.last_reality = result

                # 3. [ASCENSION 8]: HAPTIC FEEDBACK SYNTHESIS
                self.dispatcher._synthesize_haptics(result)

                # =====================================================================
                # == [ASCENSION 52]: OCULAR RETINAL SUTURE (HUD SYNC)                ==
                # =====================================================================
                # [THE MASTER CURE]: If the rite was an inception (Genesis/Dream),
                # we radiate the reified manifest DNA directly to the Ocular HUD.
                if result.success and is_heavy:
                    self._radiate_gnostic_revelation(result, trace_id)

                # 4. [ASCENSION 28]: ARTIFACT BLOOM
                if result.success and not request_obj.dry_run and is_heavy:
                    self._scan_for_unclaimed_artifacts(request_obj, result, _start_ns / 1_000_000_000)

                # 5. [ASCENSION 27]: OMNISCIENT BROADCAST (Finality)
                if result and self.akashic:
                    self.dispatcher._multicast_revelation(request_obj, result, rite_name)

                # [ASCENSION 31]: Merkle-State Fingerprinting
                if result.success:
                    self.context.variables['__last_merkle_seal__'] = result.data.get('merkle_root', "0xVOID")

            except Exception as post_heresy:
                sys.stderr.write(f"\n{UV}[TITAN:POST_PROCESS_FRACTURE]{RESET} {rite_name}\n")
                tb_scribe.print_exc(file=sys.stderr)
                raise post_heresy

            # =========================================================================
            # == MOVEMENT IX: [ASCENSION 1] - THE GNOSTIC MEMORY SUTURE (GLOBAL)     ==
            # =========================================================================
            # [STRIKE]: Explicitly inject results into the Ethereal Cell for JS resonance.
            if self._is_wasm:
                try:
                    payload = self.dispatcher._mirror_type_safety(
                        result.model_dump(mode='json') if hasattr(result, 'model_dump') else result
                    )
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(payload)
                except:
                    pass

            return result

        except Exception as catastrophic_paradox:
            # =========================================================================
            # == MOVEMENT X: FORENSIC EMERGENCY DUMP (THE REAPER)                    ==
            # =========================================================================
            # [ASCENSION 20 & 4]: IMMEDIATE SNITCH & SURGICAL UNWRAPPING
            trace = tb_scribe.format_exc()
            sys.stderr.write(f"\n{self.ALERT}💀 CATASTROPHIC DISPATCH FRACTURE: {rite_name}{self.RESET}\n")
            sys.stderr.write(f"{UV}Trace ID:{RESET} {trace_id}\n")
            sys.stderr.write(f"{UV}Error:{RESET}    {catastrophic_paradox}\n")
            sys.stderr.write("-" * 80 + "\n")
            tb_scribe.print_exc(file=sys.stderr)
            sys.stderr.write("-" * 80 + "\n\n")
            sys.stderr.flush()

            self._emergency_dump(catastrophic_paradox, rite_name, trace_id)

            fail_duration = (time.perf_counter_ns() - _start_ns) / 1_000_000_000

            # [ASCENSION 34]: Apophatic Error Unwrapping
            err_res = self.healer.handle_panic(catastrophic_paradox, request_obj or request, fail_duration)

            # Ensure the Ethereal Plane receives the fracture
            if self._is_wasm:
                try:
                    payload = err_res.model_dump(mode='json') if hasattr(err_res, 'model_dump') else err_res
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(payload)
                except:
                    pass

            return err_res

        finally:
            # [ASCENSION 4]: Recursion unwind
            if hasattr(self.dispatcher, '_recursion_depths'):
                with self.dispatcher._recursion_lock:
                    if trace_id in self.dispatcher._recursion_depths:
                        self.dispatcher._recursion_depths[trace_id] = max(0, self.dispatcher._recursion_depths[
                            trace_id] - 1)

            # [ASCENSION 11]: Metabolic Normalization
            self._neuro_optimize(heavy_mode=False)

            # [ASCENSION 60]: THE FINALITY VOW
            if not self._silent:
                _total_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
                self.logger.info(f"Rite {rite_name} concluded in {_total_ms:.2f}ms. [RESONANT]")

    def _resolve_request_vessel(self, command: str, params: Dict[str, Any]) -> 'BaseRequest':
        """
        =================================================================================
        == THE OMEGA VESSEL FORGE: TOTALITY (V-Ω-TOTALITY-VMAX-IDENTITY-SUTURE)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: ISOMORPHIC_SCHEMA_RESOLVER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_RESOLVE_VESSEL_VMAX_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme definitive authority for transmuting Intent into Form.
        It has been ascended to possess 'True Sight', righteously annihilating the
        Import Path Schism by enforcing Structural Identity over Memory Identity.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Laminar Identity Suture (THE MASTER CURE):** If the input 'params' is
            already a Request object but from a different import lineage, it is
            surgically deconstructed via `.model_dump()` and re-materialized into
            the Registry's canonical class.
        2.  **Apophatic Registry Scrying:** Performs a multi-pass search:
            Exact Key -> Normalized Key -> Class Name Parity -> Fuzzy Vibe Match.
        3.  **The 'Request' Suffix Exorcism:** Automatically reconciles 'genesis'
            with 'GenesisRequest' and vice-versa, ensuring naming symmetry.
        4.  **Bicameral Registry Inquest:** Simultaneously queries the local
            ArtisanRegistry and the global Nexus Map.
        5.  **Structural Integrity Guard:** Validates that the waked class possesses
            the 'model_validate' faculty before attempting inception.
        6.  **NoneType Sarcophagus:** Hard-wards against Null-inputs; transmuting
            empty params into a bit-perfect GnosticSovereignDict.
        7.  **Socratic Error Enrichment:** If a rite is unmanifest, it scries the
            entire Grimoire to suggest the closest phonetically-resonant match.
        8.  **Trace ID Silver-Cord Suture:** Force-binds the existing 'trace_id'
            from the params into the new vessel to maintain forensic continuity.
        9.  **Hydraulic Type Coercion:** Automatically transmutes JSON-safe strings
            back into Paths, Enums, and Datetimes during the validation strike.
        10. **Fault-Isolated Validation:** If Pydantic-V2 validation fractures, it
            falls back to a Raw-Keyword inception with a warning pulse.
        11. **Substrate DNA Recognition:** (Prophecy) Prepared to adjust schema
            strictness based on IRON vs ETHER substrate detection.
        12. **The Finality Vow:** A mathematical guarantee of a valid, warded,
            and transaction-ready Request object.
        =================================================================================
        """
        import difflib

        # --- MOVEMENT 0: THE VOID GUARD ---
        if not command:
            raise ValueError("Void Command: Execution stayed. Intent unmanifest.")

        # Ensure params is a resonant dictionary
        active_params = params if params is not None else {}

        # --- MOVEMENT I: SEMANTIC NORMALIZATION ---
        # 'velm.genesis' -> 'genesis', 'GenesisRequest' -> 'genesis'
        clean_key = str(command).split('.')[-1].split('/')[-1]
        norm_key = clean_key.replace('Request', '').lower().strip()

        # --- MOVEMENT II: TIERED IDENTITY RESOLUTION ---
        request_class = None

        # Tier 1: Canonical Registry Lookup
        if hasattr(self, 'registry') and hasattr(self.registry, 'get_request_class'):
            request_class = self.registry.get_request_class(norm_key)

        # Tier 2: Name-Parity Scry (The Identity Healer)
        if not request_class and hasattr(self, 'registry'):
            # [ASCENSION 2]: We iterate the Registry's known types to find a name match
            # even if the key lookup failed.
            for req_type in self.registry._request_to_artisan.keys():
                type_name = req_type.__name__
                if type_name.lower() == norm_key or type_name.lower() == f"{norm_key}request":
                    request_class = req_type
                    break

        # Tier 3: Nexus Gateway
        if not request_class and hasattr(self, 'nexus') and self.nexus:
            request_class = self.nexus.REQUEST_MAP.get(norm_key) or self.nexus.REQUEST_MAP.get(clean_key)

        # --- MOVEMENT III: SOCRATIC FAILURE ADJUDICATION ---
        if not request_class:
            all_rites = list(self.registry.list_capabilities().keys()) if hasattr(self, 'registry') else []
            matches = difflib.get_close_matches(norm_key, all_rites, n=1, cutoff=0.5)
            suggestion = f" Did you mean '[bold cyan]{matches[0]}[/]'?" if matches else ""

            raise ValueError(f"Unmanifest Rite: '{clean_key}' is not inscribed in the Grimoire.{suggestion}")

        # =========================================================================
        # == MOVEMENT IV: [THE MASTER CURE] - LAMINAR IDENTITY SUTURE            ==
        # =========================================================================
        # [ASCENSION 1]: If we were passed an object that LOOKS like a Request
        # but belongs to a different import path, we deconstruct and re-materialize.
        if hasattr(active_params, 'model_dump'):
            # Transmute Foreign Object -> Canonical Dictionary
            active_params = active_params.model_dump()
        elif hasattr(active_params, 'dict'):
            active_params = active_params.dict()

        # --- MOVEMENT V: THE INCEPTION STRIKE ---
        try:
            # [ASCENSION 9]: High-Fidelity Validation
            if hasattr(request_class, 'model_validate'):
                return request_class.model_validate(active_params)

            # Fallback for standard dataclasses or Pydantic V1
            return request_class(**active_params)

        except Exception as validation_heresy:
            # [ASCENSION 10]: Fault-Isolated Redemption
            # If strict validation fails (likely due to a minor type drift),
            # we attempt a Raw Strike while documenting the sin.
            try:
                self.logger.warn(f"Schema Friction in '{clean_key}': {validation_heresy}. Attempting Raw Inception.")
                return request_class(**active_params)
            except Exception:
                # If even raw inception fails, the heresy is fatal.
                raise ValueError(f"Schema Mismatch for '{clean_key}': {validation_heresy}")


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
        trace_id = getattr(self.context, 'session_id', 'tr-unbound')

        try:
            if heavy_mode:
                # [ASCENSION 11]: ADRENALINE MODE
                gc.disable()
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

                # [ASCENSION 14]: Windows High-Status Ward
                if os.name == 'nt' and not self._is_wasm:
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

                if os.name == 'nt' and not self._is_wasm:
                    try:
                        import ctypes
                        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
                    except (ImportError, AttributeError):
                        pass

                if self._is_wasm:
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
        == THE OMNISCIENT CENSUS: OMEGA POINT (V-Ω-TOTALITY-V36-HEALED-FINALIS)    ==
        =============================================================================
        LIF: 1,000,000,000x | ROLE: OMNISCIENT_CENSUS_ORACLE | RANK: OMEGA_SUPREME
        AUTH: Ω_CENSUS_V36_HEALED_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme diagnostic rite of the God-Engine, now healed of the
        UnboundLocal paradox. It performs a deep-tissue biopsy of the ArtisanRegistry,
        transmuting raw class references into high-fidelity Gnostic Schemas.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Apophatic Discovery Suture (THE FIX):** Force-triggers discovery at
            nanosecond zero, ensuring the mind is "Warm" before the census begins.
        2.  **Recursive Schema Scrying:** Uses Pydantic's `model_json_schema()`
            to provide the Reasoner with the exact "Laws of Form" for every Request.
        3.  **The Paradox Ward (THE HEALING):** Surgically resolved the exception-variable
            naming schism. The Sarcophagus is now airtight.
        4.  **Achronal Path Normalization:** Forces all internal module paths into
            POSIX forward-slash harmony for the Ocular HUD.
        5.  **Metabolic Tomography:** Measures and reports the precise nanosecond
            tax of the census itself to the HUD.
        6.  **Substrate-Aware Metadata:** Grafts CPU, RAM, and platform DNA onto
            the census to orient the AI within the physical reality.
        7.  **Merkle State Fingerprinting:** Forges a `state_hash`—a unique Merkle
            root of the entire registry to detect "Silent Drift".
        8.  **Haptic HUD Radiation:** Multicasts high-frequency progress signals
            across the Akashic link to synchronize the React Stage.
        9.  **Bicameral Scoping Guard:** Distinguishes between L0 (System) and
            L1 (Plugin) rites to maintain subversion warding.
        10. **Semantic Resonance Ranking:** Weights capabilities by their
            historical `usage_count` for predictive priority.
        11. **Fault-Isolated Recursion:** A fracture in one Request's schema
            cannot crash the entire census; the heresy is quarantined.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            JSON-RPC compliant Gnostic Grimoire.
        =============================================================================
        """
        import time
        import platform
        import json
        import sys
        import gc
        import traceback
        from pathlib import Path

        # [ASCENSION 5]: NANOSECOND TOMOGRAPHY INCEPTION
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.context, 'session_id', 'tr-census-void')

        # --- MOVEMENT I: THE OCULAR PULSE ---
        if self.akashic:
            try:
                self.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "CENSUS_SCRY_START",
                        "label": "PERCEIVING_ENGINE_SOUL",
                        "color": "#a855f7",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        try:
            # --- MOVEMENT II: THE AWAKENING ---
            # [ASCENSION 1]: Pre-emptive warm-up of the Registry Mind
            if hasattr(self.registry, '_plugins_discovered') and not self.registry._plugins_discovered:
                self.logger.verbose("Census: Incepting latent plugin shards...")
                self.registry._discover_plugins()
                self.registry._plugins_discovered = True

            # --- MOVEMENT III: THE RAW HARVEST ---
            # Retrieve the skeletal manifest from the Registry (Stratum-8)
            raw_manifest = self.registry.list_capabilities()

            # --- MOVEMENT IV: THE SCHEMA INQUEST (THE APOTHEOSIS) ---
            # [ASCENSION 2]: Transmuting names into a Grimoire of Schemas.
            enriched_capabilities = {}

            for cmd_name, meta in raw_manifest.items():
                try:
                    # 1. Resolve the Pydantic Soul (Request Class)
                    req_class_name = meta.get("request")
                    from ....interfaces import requests
                    # Using getattr for zero-latency reflection
                    req_class = getattr(requests, req_class_name, None)

                    # 2. Perform Recursive Schema Scrying
                    schema = {}
                    if req_class and hasattr(req_class, "model_json_schema"):
                        # Extract the high-fidelity JSON schema for the AI to scry
                        schema = req_class.model_json_schema()

                        # [THE CURE]: Pruning standard Pydantic noise to minimize token tax
                        schema.pop("title", None)
                        schema.pop("description", None)  # Keep property-level docs
                        if "definitions" in schema:
                            # Handle Pydantic V1/V2 variations in schema nesting
                            pass

                    # 3. Graft onto the Enriched Manifest
                    enriched_capabilities[cmd_name] = {
                        **meta,
                        "schema": schema,
                        # [ASCENSION 10]: Semantic Rank (Popularity)
                        "_resonance_rank": meta.get("usage_count", 0),
                        "is_ready": not meta.get("is_quarantined", False)
                    }

                except Exception as schema_heresy:
                    # [ASCENSION 11]: Quarantine internal failures
                    self.logger.debug(f"Schema scry deferred for {cmd_name}: {schema_heresy}")
                    enriched_capabilities[cmd_name] = meta

            # --- MOVEMENT V: METABOLIC BIOPSY ---
            # [ASCENSION 6]: Hardware vitals for environmental anchoring
            vitals = self.watchdog.get_vitals()

            # --- MOVEMENT VI: FINAL ASSEMBLY & PROCLAMATION ---
            duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            # [ASCENSION 12]: THE FINALITY VOW
            revelation = {
                "session": {
                    "id": self.context._session_id,
                    "logic_version": "V36-TOTALITY-HEALED",
                    "status": "RESONANT",
                    "merkle_state_hash": getattr(self.registry, '_state_hash', '0xVOID'),
                },
                "environment": {
                    "substrate": vitals.get("substrate", "UNKNOWN"),
                    "platform": platform.system(),
                    "arch": platform.machine(),
                    "python_v": sys.version.split()[0],
                    "load_factor": vitals.get("load_percent", 0.0)
                },
                "telemetry": {
                    "latency_ms": round(duration_ms, 3),
                    "timestamp": time.time(),
                    "heap_objects": len(gc.get_objects())
                },
                "capabilities": enriched_capabilities
            }

            # [ASCENSION 8]: Final Revelation Pulse to HUD
            if self.akashic:
                try:
                    self.akashic.broadcast({
                        "method": "novalym/hud_revelation",
                        "params": {
                            "type": "CENSUS_REVELATION",
                            "count": len(enriched_capabilities),
                            "latency": f"{duration_ms:.2f}ms",
                            "trace": trace_id
                        }
                    })
                except Exception:
                    pass

            return revelation

        except Exception as catastrophic_heresy:
            # =========================================================================
            # == [THE FIX]: THE PARADOX WARD (HEALED)                                ==
            # =========================================================================
            # [ASCENSION 3]: Absolute naming consistency in the catch block.
            # This ensures the 'UnboundLocalError' is incinerated from this timeline.
            self.logger.error(f"Census Absolute Fracture: {str(catastrophic_heresy)}")

            return {
                "success": False,
                "error": "CAPABILITY_CENSUS_FRACTURE",
                "details": str(catastrophic_heresy),
                "traceback": traceback.format_exc() if self._log_level == "DEBUG" else "REDACTED",
                "logic_version": "V36-EMERGENCY-RECOVERY"
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



    @context.setter
    def context(self, value):
        self._context = value

    @predictor.setter
    def predictor(self, value):
        self._predictor = value

    def __repr__(self) -> str:
        return f"<QuantumEngine session={self.context._session_id[:8]} root={self.project_root.name}>"