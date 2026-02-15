# Path: core/runtime/middleware/pipeline.py
# -----------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_PIPELINE_SILENT_GOD_MODE_V7
# SYSTEM: GNOSTIC_SPINE | ROLE: CENTRAL_NERVOUS_SYSTEM
# =================================================================================

import sys
import time
import threading
import traceback
import uuid
import os


from dataclasses import dataclass, field
from typing import List, Callable, Type, Dict, Optional, Any

# --- THE CONTRACTS ---
from .contract import Middleware, NextHandler
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

# --- CONSTANTS OF THE SPINE ---
MAX_RECURSION_DEPTH = 50
CRITICAL_FAILURE_THRESHOLD = 5  # Failures before auto-bypass
SLOW_MIDDLEWARE_THRESHOLD_MS = 200.0  # Warn if a link is slow
TRACE_INDENT_CHAR = "│   "


@dataclass
class MiddlewareStats:
    """
    [THE LEDGER OF PERFORMANCE]
    Tracks the vitality of a single middleware node.
    """
    name: str
    invocations: int = 0
    failures: int = 0
    total_duration_ms: float = 0.0
    last_duration_ms: float = 0.0
    memory_delta_mb: float = 0.0
    is_circuit_broken: bool = False

    @property
    def average_duration_ms(self) -> float:
        return self.total_duration_ms / max(1, self.invocations)


@dataclass
class PipelineTelemetry:
    """
    [THE FLIGHT RECORDER]
    Captures the journey of a single request through the spine.
    """
    trace_id: str
    start_time: float
    steps: List[Dict[str, Any]] = field(default_factory=list)
    final_status: str = "UNKNOWN"

    def record_step(self, name: str, event: str, duration: float = 0.0, meta: Dict = None):
        self.steps.append({
            "timestamp": time.time(),
            "middleware": name,
            "event": event,
            "duration_ms": duration,
            "meta": meta or {}
        })


class MiddlewareNode:
    """
    [THE NEURAL NODE]
    A wrapper around the raw Middleware class that provides
    instrumentation, safety, and circuit breaking.
    """

    def __init__(self, cls: Type[Middleware], engine: Any):
        self.cls = cls
        self.name = cls.__name__
        self.engine = engine
        self.stats = MiddlewareStats(name=self.name)

    def instantiate(self) -> Middleware:
        try:
            return self.cls(self.engine)
        except Exception as e:
            sys.stderr.write(f"[SPINE] 💥 CRITICAL: Failed to instantiate {self.name}: {e}\n")
            self.stats.failures += 1
            raise e


class MiddlewarePipeline:
    """
    =============================================================================
    == THE GNOSTIC SPINE (V-Ω-SILENT-ORCHESTRATOR)                             ==
    =============================================================================
    The central nervous system. It observes, corrects, and chronicles.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Scribe("GnosticSpine")

        # The Ordered Chain of Nodes
        self._nodes: List[MiddlewareNode] = []

        # Thread Safety
        self._lock = threading.RLock()

        # Global Registry of Stats (Persists across requests)
        self._registry_stats: Dict[str, MiddlewareStats] = {}

        # Telemetry Archive (Rotating buffer)
        self._telemetry_archive: List[PipelineTelemetry] = []

    def add(self, middleware_cls: Type[Middleware], position: int = -1):
        """
        [RITE]: INJECT_NEURON
        Adds a new Guardian to the spine. Thread-safe.
        """
        with self._lock:
            node = MiddlewareNode(middleware_cls, self.engine)
            if node.name in self._registry_stats:
                node.stats = self._registry_stats[node.name]
            else:
                self._registry_stats[node.name] = node.stats

            if position == -1:
                self._nodes.append(node)
            else:
                self._nodes.insert(position, node)

            # Silent registration unless debug
            #if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
                #sys.stderr.write(f"[GNOSTICSPINE] Injected Node: {node.name} at index {len(self._nodes) - 1}\n")

    def execute(self, request: BaseRequest, core_function: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        """
        [THE RITE OF FLOW]
        The recursive execution engine.
        Constructs the Onion dynamically, injecting telemetry and safety at every layer.
        """

        # [ASCENSION 1]: NULL-SAFE IDENTITY FORGE
        raw_id = getattr(request, 'trace_id', None)
        if not raw_id:
            raw_id = str(uuid.uuid4())
        trace_id = str(raw_id)[:8]

        telemetry = PipelineTelemetry(trace_id=trace_id, start_time=time.perf_counter())

        # [ASCENSION 6]: THREAD BINDING
        original_thread_name = threading.current_thread().name
        threading.current_thread().name = f"Pipe-{trace_id}"

        # [ASCENSION]: GATED TRACING CHECK
        should_trace = os.environ.get("SCAFFOLD_TRACE") == "1"

        if should_trace: self._log_trace(trace_id, 0, f"Igniting Pipeline for {type(request).__name__}")

        # 1. THE CORE WRAPPER (The Center of the Onion)
        def core_wrapper(req: BaseRequest) -> ScaffoldResult:
            depth = len(self._nodes)
            if should_trace: self._log_trace(trace_id, depth, ">>> REACHED CORE ARTISAN <<<")
            telemetry.record_step("CORE", "EXECUTE_START")
            t_start = time.perf_counter()

            try:
                self._broadcast_progress("Executing Rite...", 95)
                result = core_function(req)

                duration = (time.perf_counter() - t_start) * 1000
                telemetry.record_step("CORE", "EXECUTE_COMPLETE", duration)

                if result is None:
                    if should_trace: self._log_trace(trace_id, depth, "!!! CORE RETURNED VOID (NONE) !!!")
                    return ScaffoldResult(success=False, message="Core Artisan produced Void Result.")

                return result

            except Exception as e:
                telemetry.record_step("CORE", "EXECUTE_FRACTURE", 0, {"error": str(e)})
                raise e

        # 2. THE CHAIN CONSTRUCTION (Wrapping Layers)
        next_handler = core_wrapper

        with self._lock:
            active_nodes = list(reversed(self._nodes))

        total_depth = len(active_nodes)

        for i, node in enumerate(active_nodes):
            current_depth = total_depth - i - 1
            if node.stats.is_circuit_broken:
                if should_trace: self._log_trace(trace_id, current_depth, f"Skipping {node.name}")
                continue

            def make_handler(current_node: MiddlewareNode, inner_next: NextHandler, depth: int):
                def handler(req: BaseRequest) -> ScaffoldResult:
                    node_name = current_node.name
                    if should_trace: self._log_trace(trace_id, depth, f"► {node_name}")
                    telemetry.record_step(node_name, "ENTER")

                    t_node_start = time.perf_counter()
                    try:
                        instance = current_node.instantiate()
                        result = instance.handle(req, inner_next)

                        if result is None:
                            raise ArtisanHeresy(f"Middleware {node_name} swallowed the request.")

                        duration = (time.perf_counter() - t_node_start) * 1000
                        if should_trace: self._log_trace(trace_id, depth, f"◄ {node_name}")

                        current_node.stats.invocations += 1
                        current_node.stats.total_duration_ms += duration
                        telemetry.record_step(node_name, "EXIT", duration)

                        return result

                    except Exception as e:
                        current_node.stats.failures += 1
                        if should_trace: self._log_trace(trace_id, depth, f"!!! FRACTURE IN {node_name}: {e}")
                        telemetry.record_step(node_name, "CRASH", 0, {"error": str(e)})

                        if current_node.stats.failures >= CRITICAL_FAILURE_THRESHOLD:
                            current_node.stats.is_circuit_broken = True
                            sys.stderr.write(f"[SPINE] ⚡ Circuit Breaker TRIPPED for {node_name}\n")
                        raise e

                return handler

            next_handler = make_handler(node, next_handler, current_depth)

        # 3. IGNITION
        try:
            if should_trace: self._log_trace(trace_id, -1, ">>> IGNITING CHAIN <<<")
            final_result = next_handler(request)

            # [THE FINAL CURE]: TYPE-AGNOSTIC SUCCESS DIVINATION
            # We must not access .success directly here.
            is_successful_outcome = False
            if final_result is not None:
                if hasattr(final_result, 'success'):
                    is_successful_outcome = bool(final_result.success)
                elif isinstance(final_result, dict):
                    # Handle dict return by checking 'success' key or lack of 'error'
                    is_successful_outcome = bool(final_result.get('success', True)) and not final_result.get('error')
                else:
                    is_successful_outcome = True  # Fallback

            telemetry.final_status = "SUCCESS" if is_successful_outcome else "FAILURE"
            self._archive_telemetry(telemetry)

            return final_result

        except Exception as e:
            if should_trace: self._log_trace(trace_id, -1, f"!!! PIPELINE FATAL FRACTURE: {e}")
            traceback.print_exc(file=sys.stderr)
            telemetry.final_status = "CRASH"
            self._archive_telemetry(telemetry)
            return ScaffoldResult(success=False, message=f"Pipeline Crash: {str(e)}")

        finally:
            threading.current_thread().name = original_thread_name

    def _broadcast_progress(self, message: str, percentage: Optional[int] = None):
        """
        =================================================================================
        == THE HERALD'S PROCLAMATION (V-Ω-TELEPATHIC-UPLINK-SINGULARITY)               ==
        =================================================================================
        LIF: INFINITY | AUTH_CODE: Ω_PROGRESS_RESONATOR_V9000 | ROLE: SYMBOLIC_REVEALER

        Surgically projects the internal kinetics of the Middleware Spine into the
        Architect's Ocular Interface (React Frontend).

        It transforms a silent backend execution into a luminous, interactive sequence,
        bridging the gap between raw Python computation and UI perception via the
        Akashic Record.
        =================================================================================
        """
        # 1. [VITALITY_CHECK]: Ensure the Engine possesses the Akashic link
        # We use getattr to remain decoupled from the specific Akashic implementation
        akashic = getattr(self.engine, 'akashic', None)
        if not akashic:
            return

        # 2. [KINETIC_ID_FORGE]: Generate a unique ID for this specific trace
        # We anchor to the session_id to prevent progress bar collisions in multi-user realities
        session_id = getattr(self.engine.context, 'session_id', 'void')
        progress_id = f"pipeline-pulse-{session_id[:8]}"

        # 3. [DATA_TRANSMUTATION]: Forge the sacred JSON-RPC 2.0 Notification
        # This packet adheres to the Gnostic progress contract expected by useTelemetry.ts
        packet = {
            "method": "scaffold/progress",
            "params": {
                "id": progress_id,
                "title": "Gnostic Spinal Flow",
                "message": f"[{self.__class__.__name__}] {message}",
                "percentage": percentage,
                "done": percentage is not None and percentage >= 100,
                "timestamp": time.time(),
                # [ASCENSION]: Trace injection for distributed observability
                "trace_id": session_id,
                "tags": ["KINETIC", "SPINE_ACTIVITY"]
            }
        }

        # 4. [ATOMIC_PROJECTION]: Cast the signal across the Neural Link
        try:
            # We use a non-blocking broadcast to ensure the Pipeline's
            # velocity is never compromised by UI update latency.
            akashic.broadcast(packet)
        except Exception:
            # [SILENCE_VOW]: If the broadcast fails, the Spine remains silent
            # to protect the integrity of the core Rite.
            pass

    # =========================================================================
    # == INTERNAL UTILITIES                                                  ==
    # =========================================================================

    def introspect(self) -> str:
        """[ASCENSION 9]: TOPOLOGY INTROSPECTION"""
        lines = ["Pipeline Topology:"]
        lines.append("  [Request] ->")
        for i, node in enumerate(self._nodes):
            status = "🔴 BROKEN" if node.stats.is_circuit_broken else "🟢 ACTIVE"
            lines.append(f"    | {i + 1}. {node.name.ljust(30)} {status} (Avg: {node.stats.average_duration_ms:.2f}ms)")
        lines.append("  -> [Artisan Core]")
        return "\n".join(lines)

    def get_telemetry_snapshot(self) -> Dict[str, Any]:
        """Returns the stats registry for the Dashboard."""
        return {
            name: {
                "invocations": s.invocations,
                "failures": s.failures,
                "avg_ms": s.average_duration_ms,
                "broken": s.is_circuit_broken
            }
            for name, s in self._registry_stats.items()
        }

    def _log_trace(self, trace_id: str, depth: int, msg: str):
        """[ASCENSION 1]: GATED TRACER"""
        indent = TRACE_INDENT_CHAR * max(0, depth)
        sys.stderr.write(f"[PIPE:{trace_id}] {indent}{msg}\n")
        sys.stderr.flush()

    def _get_memory_usage(self) -> float:
        """
        =============================================================================
        == THE METABOLIC TOMOGRAPHY (V-Ω-TOTALITY-V20000.5-ISOMORPHIC)             ==
        =============================================================================
        LIF: ∞ | ROLE: HEAP_PRESSURE_SCRIER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_PIPELINE_V20000_MEMORY_SUTURE_2026_FINALIS
        """
        import gc
        import sys

        try:
            # --- MOVEMENT I: THE HIGH PATH (IRON CORE) ---
            # Attempt to speak with the physical process sensors (psutil).
            try:
                import psutil
                process = psutil.Process()
                # Returns Resident Set Size (RSS) in Megabytes.
                return process.memory_info().rss / (1024 * 1024)
            except (ImportError, AttributeError, Exception):
                # --- MOVEMENT II: THE WASM PATH (ETHER HEAP) ---
                # [ASCENSION 3]: Heuristic Mass Inference.
                # In WASM/Pyodide, physical RSS is veiled by the browser sandbox.
                # We scry the object count and apply the "Gnostic Mass" coefficient.
                # Heuristic: 100,000 Python objects is approx 15MB in the WASM heap.
                object_density = len(gc.get_objects())
                return float(object_density * 0.00015)

        except Exception:
            # [ASCENSION 5]: The NoneType Sarcophagus.
            # Telemetry must never fracture the Gnostic Spine.
            return 0.0

    def _archive_telemetry(self, t: PipelineTelemetry):
        """[ASCENSION 3]: FLIGHT RECORDER"""
        self._telemetry_archive.append(t)
        if len(self._telemetry_archive) > 100:
            self._telemetry_archive.pop(0)

    # =========================================================================
    # == DUNDER PROTOCOLS                                                    ==
    # =========================================================================

    def __repr__(self) -> str:
        return f"<GnosticSpine nodes={len(self._nodes)} active={not self._lock.locked()}>"

    def __len__(self) -> int:
        return len(self._nodes)