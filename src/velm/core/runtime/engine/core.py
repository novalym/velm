# Path: core/runtime/engine/core.py
# ---------------------------------
import uuid
import os
import time
import threading
import sys
from pathlib import Path
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
    LIF: INFINITY | AUTH_CODE: @)(()@()@

    The Unbreakable, Self-Learning, Transactional Kernel.

    It orchestrates the Cybernetic Loop:
    1.  **Perception**: Ingests Request via `dispatch`.
    2.  **Cognition**: `NeuroOptimizer` tunes physics; `CognitiveMemory` records context.
    3.  **Action**: `QuantumDispatcher` routes intent; `TransactionManager` guards data.
    4.  **Metabolism**: `SystemWatchdog` monitors resources; `VitalityMonitor` signals UI.
    5.  **Learning**: `IntentPredictor` observes outcomes to predict the future.
    """

    def __init__(
            self,
            project_root: Optional[Path] = None,
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

        self.console = get_console()
        self.logger = Scribe("QuantumEngine")

        # 2. THE MIND (Context & Registry)
        self.context = RuntimeContext(project_root)
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
                from ....core.daemon.akashic import AkashicRecord
                self.akashic = AkashicRecord(
                    persistence_path=str(self.context.project_root / ".scaffold" / "akashic.jsonl"))
            except ImportError:
                self.logger.warn("AkashicRecord not found. Broadcast capabilities will be dormant.")

        # 3. ORGAN GENESIS (Initialization Order Matters)

        # [Lifecycle]: Bootstrap first to prepare the spine
        self.bootstrap = EngineBootstrap(self)

        # [Persistence]: Transaction Vault (Disk Safety)
        self.transactions = TransactionManager(self.logger)

        # [Intelligence]: The Neural Layer
        # We anchor prediction memory to the project root (or home if cold)
        memory_anchor = self.context.project_root or Path.home()
        self.predictor = IntentPredictor(memory_anchor)
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
            self.bootstrap.awaken_skills()

        # 7. IGNITE VIGILANCE
        # Starts background threads for heartbeat and resource monitoring
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

    @property
    def alchemist(self) -> 'DivineAlchemist':
        if self._alchemist is None:
            from ...alchemist import get_alchemist
            self._alchemist = get_alchemist()
        return self._alchemist

    @property
    def healer(self) -> 'HighPriestOfResilience':
        if self._healer is None:
            from .resilience.healer import HighPriestOfResilience
            self._healer = HighPriestOfResilience(verbose=(self._log_level == "DEBUG"))
        return self._healer

    @property
    def diviner(self) -> 'IgnitionDiviner':
        if self._diviner is None:
            from ...ignition import IgnitionDiviner
            self._diviner = IgnitionDiviner()
        return self._diviner

    @property
    def conductor(self) -> 'Conductor':
        if self._conductor is None:
            from ...ignition import Conductor
            self._conductor = Conductor
        return self._conductor

    @property
    def traceback_handler(self) -> 'GnosticTracebackHandler':
        if self._traceback_handler is None and not self._silent:
            from ...traceback import install_gnostic_handler
            self._traceback_handler = install_gnostic_handler(self.console)
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
        [ASCENSION 15]: DYNAMIC CONTEXT LEVITATION
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
        """The Sovereign Dispatch Rite: Unified Gateway for Sync and Async Energies."""
        import importlib
        import sys
        import time
        import uuid
        import traceback
        import inspect
        import asyncio
        import threading
        import concurrent.futures
        from pathlib import Path

        start_time = time.perf_counter()
        jit_overhead_ms = 0.0

        # --- MOVEMENT I: TRANSMUTATION (INPUT NORMALIZATION) ---
        try:
            if isinstance(request, str):
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
        # [ASCENSION 4]: Extract trace_id from polymorphic states
        meta = getattr(request_obj, 'metadata', {})
        meta_dict = meta.model_dump(mode='json') if hasattr(meta, 'model_dump') else (
            meta if isinstance(meta, dict) else {})

        trace_id = (
                meta_dict.get('trace_id') or
                meta_dict.get('x_nov_trace') or
                getattr(request_obj, 'trace_id', None) or
                f"tr-{uuid.uuid4().hex[:8].upper()}"
        )

        # Forge the Silver Cord
        if not hasattr(request_obj, 'trace_id') or getattr(request_obj, 'trace_id') in [None, "None", "tr-void"]:
            object.__setattr__(request_obj, 'trace_id', trace_id)

        request_type = type(request_obj)
        rite_name = request_type.__name__
        is_heavy = any(k in rite_name for k in ['Genesis', 'Transmute', 'Analyze', 'Refactor', 'Manifest', 'Inception'])

        # --- MOVEMENT III: THERMODYNAMIC ADJUDICATION ---
        # [ASCENSION 3 & 6]: Adrenaline vs Zen backpressure handling
        if is_heavy and self.watchdog.get_vitals().get("load_percent", 0) > 85.0:
            self.logger.warn(f"[{trace_id}] Metabolic Fever Detected. Shedding heavy rite: {rite_name}")
            return self.failure("Metabolic Congestion: System too hot for heavy inception.")

        self._neuro_optimize(heavy_mode=is_heavy)

        try:
            # --- MOVEMENT IV: COGNITIVE MEMORY & FOCUS ---
            if hasattr(request_obj, 'project_root') and request_obj.project_root:
                self.memory.record_focus(str(request_obj.project_root))

            # --- MOVEMENT V: THE RITE OF RE-INCEPTION (JIT / HOT-SWAP) ---
            # [ASCENSION 5]: Circuit Breaker check before materialization
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

            # Resolve Artisan Reference (Tuple=Ghost, Type=Soul, Instance=Living)
            if isinstance(artisan_info, tuple):
                module_path, class_name = artisan_info
                if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
                    jit_start = time.perf_counter()
                    with self.kernel_lock("jit_reception"):
                        try:
                            # Recursive module purging for hot-reload
                            to_purge = [m for m in sys.modules if m.startswith(module_path)]
                            for m in to_purge:
                                sys.modules.pop(m, None)
                            module = importlib.import_module(module_path)
                            ArtisanClass = getattr(module, class_name)
                            artisan_instance = ArtisanClass(self)
                            jit_overhead_ms = (time.perf_counter() - jit_start) * 1000
                        except Exception as syntax_heresy:
                            self.logger.error(f"JIT Inception Failure: {syntax_heresy}")
                            return self.failure(f"Syntax Heresy in {class_name}", details=traceback.format_exc())

                if not artisan_instance:
                    module = importlib.import_module(module_path)
                    artisan_instance = getattr(module, class_name)(self)
            else:
                artisan_instance = artisan_info(self) if isinstance(artisan_info, type) else artisan_info

            # Ensure Engine-Artisan Suture
            if hasattr(artisan_instance, 'engine'):
                object.__setattr__(artisan_instance, 'engine', self)

            # --- MOVEMENT VI: HYBRID KINETIC EXECUTION (THE CURE) ---
            # [ASCENSION 1]: The non-blocking bridge for Async Artisans.
            def _conduct_rite(req: BaseRequest) -> Union[ScaffoldResult, Any]:
                # Project HUD Pulse
                if self.akashic:
                    self.akashic.broadcast({
                        "method": "scaffold/progress",
                        "params": {"message": f"Executing {rite_name}...", "percentage": 25, "trace": trace_id}
                    })

                # [TRANSACTIONAL GUARD]
                with self.transactions.atomic_rite(f"{rite_name}:{req.request_id}") as tx_id:
                    if req.context is None: req.context = {}
                    req.context['transaction_id'] = tx_id

                    # Call the hand
                    raw_result = artisan_instance.execute(req)

                    # [THE CURE]: Resolve Coroutines in a Sync Context
                    if inspect.isawaitable(raw_result):
                        try:
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                # We are in a running loop (FastAPI/Uvicorn)
                                # We must use a thread-safe future to block and wait.
                                return asyncio.run_coroutine_threadsafe(raw_result, loop).result()
                            else:
                                return asyncio.run(raw_result)
                        except RuntimeError:
                            # New loop inception
                            return asyncio.run(raw_result)

                    return raw_result

            # Pipeline Ignition (Through the Gnostic Spine)
            result = self.pipeline.execute(request_obj, _conduct_rite)

            # --- MOVEMENT VII: POST-PROCESS & TELEMETRY ---
            if result and hasattr(result, 'duration_seconds'):
                if not result.duration_seconds:
                    result.duration_seconds = time.perf_counter() - start_time

            if jit_overhead_ms > 0 and result:
                result.ui_hints["jit_ms"] = jit_overhead_ms

                # [ASCENSION 11]: Feed the Predictor
            if hasattr(self, 'predictor'):
                self.predictor.observe_outcome(request_obj, result)

            self.memory.record_rite(rite_name, result.success if result else False)
            self.last_reality = result

            # [THE CURE]: MULTICAST THE REVELATION
            # We delegate to the Dispatcher's internal Prism.
            # This heals the 'AttributeError' because the logic is now correctly located.
            if result and self.akashic:
                self.dispatcher._multicast_revelation(request_obj, result, rite_name)

            # Trigger registered hooks
            for hook in self._hooks:
                try:
                    hook(result)
                except Exception:
                    pass

            return result

        except Exception as catastrophic_paradox:
            # --- MOVEMENT VIII: FORENSIC EMERGENCY DUMP ---
            # [ASCENSION 12]: The Finality Vow
            self._emergency_dump(catastrophic_paradox, rite_name, trace_id)
            self.logger.critical(f"Catastrophic Dispatch Fracture in {rite_name}: {catastrophic_paradox}")

            # Resolve latency for the failure vessel
            fail_duration = time.perf_counter() - start_time
            return self.healer.handle_panic(catastrophic_paradox, request_obj, fail_duration)

        finally:
            # Metabolic Normalization
            if is_heavy:
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
        # The Nexus (if running as Daemon) or local Registry holds the map.
        request_class = None

        # A. Check internal registry
        if hasattr(self, 'registry') and hasattr(self.registry, 'get_request_class'):
            request_class = self.registry.get_request_class(clean_key)

        # B. Check Nexus map (if we are the engine of a Daemon)
        if not request_class and hasattr(self, 'nexus') and self.nexus:
            request_class = self.nexus.REQUEST_MAP.get(clean_key)

        if not request_class:
            raise ValueError(f"Unknown Rite: '{clean_key}'. The Grimoire does not contain this spell.")

        # 3. Forge the Vessel
        # Pydantic's model_validate is robust against extra fields if configured correctly.
        try:
            return request_class.model_validate(params)
        except Exception as e:
            # Fallback: try constructing with **params if validation fails on strict typing
            # This handles cases where 'params' might be a list or have legacy keys
            try:
                return request_class(**params)
            except:
                raise ValueError(f"Schema Mismatch for '{clean_key}': {e}")

    def _neuro_optimize(self, heavy_mode: bool):
        """
        =============================================================================
        == THE METABOLIC REGULATOR (V-Ω-ADRENALINE-ZEN)                            ==
        =============================================================================
        LIF: ∞ | ROLE: ADAPTIVE_PHYSICS_GOVERNOR
        """
        import gc
        import os
        try:
            if heavy_mode:
                # [ADRENALINE MODE]: Silence the Reaper, Boost Priority
                gc.disable()
                if os.name == 'nt':
                    # Set process to Above Normal priority on Windows
                    try:
                        import ctypes
                        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00008000)
                    except:
                        pass
            else:
                # [ZEN MODE]: Summon the Reaper, Normalize Priority
                gc.enable()
                if os.name == 'nt':
                    try:
                        import ctypes
                        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
                    except:
                        pass

                # [ASCENSION 5]: Memory Wall Check
                try:
                    import psutil
                    process = psutil.Process(os.getpid())
                    # If memory exceeds 1GB, force a deep lustrations rite (GC)
                    if process.memory_info().rss > 1024 * 1024 * 1024:
                        gc.collect()
                except ImportError:
                    gc.collect()
        except Exception:
            pass

    def _emergency_dump(self, error: Exception, rite: str, trace: str):
        """[ASCENSION 12]: Inscribes the final state before collapse."""
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

    def register_artisan(self, request_type: Type[BaseRequest], artisan_class: Any):
        """Consecrates a new skill in the Registry."""
        self.registry.register(request_type, artisan_class)

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
        # We safely extract ui_hints from kwargs, providing a default if none exist.
        ui_hints = kwargs.pop("ui_hints", {
            "vfx": "bloom",
            "sound": "consecration_complete"
        })

        # 2. DELEGATE TO THE SCRIBE
        # The TelemetryScribe is already hardened to handle these kwargs.
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
            and 'exc_tb' in the root scope, annihilating the UnboundLocalError
            paradox across all timelines.
        2.  **Surgical Parameter Distillation:** Pops 'traceback', 'vitals', and
            'ui_hints' from kwargs to prevent Multiple-Value Heresies.
        3.  **Achronal Contextual Capture:** Inscribes the exact moment of failure
            with microsecond precision to ensure absolute forensic replay.
        4.  **Hierarchical Exception Triage:** Prioritizes the Architect's
            explicit details over the system's raw stack dump for maximum clarity.
        5.  **Haptic Feedback Synchronicity:** Automatically calculates the
            visual intensity (vfx) based on the severity of the detected fracture.
        6.  **Merkle-Based Fingerprinting:** Forges a unique ID for the error based
            on the message mass, allowing the HUD to group identical failures.
        7.  **Null-State Immutability Guard:** Transmutes NoneType inputs into
            structured Gnostic "VOID" constants to prevent downstream crashes.
        8.  **Sovereign Identity Attribution:** Binds the source identity from
            the active thread's DNA for perfect transactional accountability.
        9.  **Recursive Redaction Governance:** Forces all failure data through
            the Entropy Sieve to protect Architect secrets during panic events.
        10. **Thermodynamic Load Tomography:** Injects current CPU/RAM heat metrics
            directly into the failure dossier to identify hardware-level causes.
        11. **Socratic Remediation Prophecy:** Scans internal logic patterns to
            inject an automated "Cure" command if the suggestion is void.
        12. **The Finality Vow:** A mathematical guarantee that the Engine will
            always speak its failure. Silence is no longer an option.
        """
        import sys
        import traceback as tb_module
        from ..telemetry import TelemetryScribe

        # --- 1. THE CURE: ATOMIC SCOPE INITIALIZATION ---
        # Pre-defining the soul of the error to prevent UnboundLocalError
        exc_type, exc_val, exc_tb = (None, None, None)

        # Only fetch if we are actually in an exception context
        if sys.exc_info()[0] is not None:
            exc_type, exc_val, exc_tb = sys.exc_info()


        # --- 2. SURGICAL PARAMETER DISTILLATION ---
        # We extract colliding keywords to satisfy the TelemetryScribe contract
        provided_traceback = kwargs.pop("traceback", None)
        provided_vitals = kwargs.pop("vitals", {})
        provided_ui_hints = kwargs.pop("ui_hints", {})

        # --- 3. FORENSIC TRACE RECONSTRUCTION ---
        # Prioritize the provided traceback (Hand) over the system's info (Mind)
        final_traceback = provided_traceback
        if not final_traceback and exc_val:
            final_traceback = "".join(tb_module.format_exception(exc_type, exc_val, exc_tb))

        # [ASCENSION 4]: Hierarchical Detail Recovery
        # If the Architect didn't provide details, we extract the essence of the exception
        if not details and exc_val:
            details = f"Internal Engine Fracture: {str(exc_val)}"
        elif not details:
            details = "Contextual Logic Gap: No specific fracture details manifest."

        # --- 4. HAPTIC & METABOLIC ALIGNMENT ---
        # Standardize the visual frequency for the React Ocular membrane
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
        # Materializing the Result through the Telemetric Scribe
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
            # Ensure the Registry has performed its upward Gaze for third-party plugins.
            if hasattr(self.registry, '_plugins_discovered') and not self.registry._plugins_discovered:
                self.registry._discover_plugins()
                self.registry._plugins_discovered = True

            # 2. RADIATE THE LEDGER
            # We delegate to the ascended V26 Registry to get the high-fidelity Dict.
            manifest = self.registry.list_capabilities()

            # 3. ENRICH WITH ENGINE METADATA
            # We graft engine-level vitals onto the census for the Ocular HUD.
            return {
                "session_id": self.context.session_id,
                "state_hash": getattr(self.registry, '_state_hash', '0xVOID'),
                "capabilities": manifest,
                "timestamp": time.time(),
                "logic_version": "V32-TOTALITY"
            }

        except Exception as e:
            # [ASCENSION 12]: THE FINALITY VOW
            # If the census fails, we return a Forensic Sarcophagus.
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

    def shutdown(self):
        """
        [THE FINAL RITE]
        Gracefully dissolves the Engine.
        """
        self.shutdown_manager.execute()

    def __repr__(self) -> str:
        return f"<QuantumEngine session={self.context.session_id[:8]} root={self.project_root.name}>"