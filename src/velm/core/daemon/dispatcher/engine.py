# Path: core/daemon/dispatcher/engine.py
# --------------------------------------

import os
import sys
import time
import uuid
import threading
import json
import traceback
import logging
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, TimeoutError
from pathlib import Path
from typing import Dict, Any, Type, Optional, List, Union, Tuple

# --- GNOSTIC INTERNAL UPLINKS ---
from .triage import TriageOfficer
from .errors import ErrorForge
from ....logger import Scribe
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult

# =============================================================================
# == THE ACOLYTE HIVE (GLOBAL SCOPE FOR PICKLE STABILITY)                    ==
# =============================================================================

# Global reference to the worker's internal engine.
_worker_engine: Optional[Any] = None


def _warm_acolyte_inception(project_root_str: str):
    """
    [RITE OF WARM-UP]
    Executed once when an Acolyte Process is born. It materializes a private
    God-Engine instance.
    """
    global _worker_engine
    pid = os.getpid()

    # [ASCENSION 2]: RECURSIVE SPAWNING WARD
    # Tell the worker's engine NOT to spawn its own Hive.
    os.environ["SCAFFOLD_HIVE_DISABLED"] = "1"
    os.environ["SCAFFOLD_IS_ACOLYTE"] = "1"
    os.environ["SCAFFOLD_SILENT_WORKER"] = "1"

    try:
        from ....core.runtime.engine import ScaffoldEngine
        from ....logger import configure_logging

        # [ASCENSION 11]: The Silence Vow
        configure_logging(silent_console=True)

        # [ASCENSION 7]: Type-Safe Anchoring
        anchor_path = Path(project_root_str).resolve()

        # --- ENGINE MATERIALIZATION ---
        # We initialize a 'Thin' version of the engine (no Hive, no watchdog)
        _worker_engine = ScaffoldEngine(
            project_root=anchor_path,
            auto_register=True,
            silent=True
        )

        # [ASCENSION 15]: JIT Skill Awakening
        _worker_engine.bootstrap.awaken_skills()

        sys.stderr.write(f"[Acolyte-{pid}] ✅ Inception Complete. Gnosis Manifest.\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[Acolyte-{pid}] 💥 Inception Fracture: {str(e)}\n")
        sys.stderr.flush()
        raise e


def _execute_fission_rite(command: str, params: Dict[str, Any]) -> Dict:
    """
    [THE KINETIC STRIKE]
    Executes a rite within the Acolyte process. This bypasses the Mother-Daemon's
    GIL entirely. Returns JSON-safe matter.
    """
    global _worker_engine
    if _worker_engine is None:
        return {"success": False, "error": "Acolyte engine not manifest."}

    try:
        # [ASCENSION 19]: Context Levitation
        target_root = params.get('project_root')

        if target_root:
            with _worker_engine.temporary_context(target_root):
                result = _worker_engine.dispatch(command, params)
        else:
            result = _worker_engine.dispatch(command, params)

        # [ASCENSION 18]: Atomic Transmutation
        if hasattr(result, 'model_dump'):
            return result.model_dump(mode='json')
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Acolyte Internal Fracture: {str(e)}",
            "traceback": traceback.format_exc()
        }


# =============================================================================
# == THE SOVEREIGN GNOSTIC DISPATCHER                                        ==
# =============================================================================

class GnosticDispatcher:
    """
    =================================================================================
    == THE SOVEREIGN HYPERVISOR (V-Ω-TOTALITY-V100-STABILIZED)                     ==
    =================================================================================
    LIF: INFINITY | ROLE: HIVE_ORCHESTRATOR | RANK: SOVEREIGN

    [THE CURE]: This version implements Lazy Hive Ignition and the Recursive
    Spawning Ward to prevent process explosions.
    """

    HEAVY_RITES = {'analyze', 'distill', 'genesis', 'transmute', 'weave', 'refactor', 'train', 'garden', 'repair'}
    SACRED_RITES = {'initialize', 'shutdown', 'ping', 'status', '$/heartbeat', 'daemon/anchor'}
    MAX_QUEUE_DEPTH = 64

    def __init__(self, engine: Any, request_map: Dict[str, Type[BaseRequest]], **kwargs):
        self.engine = engine
        self.logger = Scribe("Dispatcher")
        self.triage = TriageOfficer(request_map)

        self._active_jobs: Dict[str, Dict[str, Any]] = {}
        self._job_lock = threading.RLock()
        self._is_draining = False
        self._start_time = time.time()
        self._shutdown_lock = threading.Lock()

        # --- THE BICAMERAL MIND ---
        # 1. THE CORTEX POOL (Threads)
        # We still start the thread pool, but keep it small for O(1) boot.
        self.cortex_pool = ThreadPoolExecutor(
            max_workers=8,
            thread_name_prefix="GnosticCortex"
        )

        # 2. THE NEURAL HIVE (Processes)
        # [ASCENSION 1]: LAZY HIVE IGNITION
        # We do not create the ProcessPoolExecutor here.
        # We wait until the first heavy rite is called.
        self.hive_pool: Optional[ProcessPoolExecutor] = None
        self._hive_lock = threading.Lock()

        # [ASCENSION 20]: ZOMBIE REAPER
        self._spawn_zombie_reaper()

    def _ignite_hive(self):
        """[RITE]: HIVE_GENESIS (Lazy)"""
        with self._hive_lock:
            if self.hive_pool is not None:
                return

            # [ASCENSION 3]: DETERMINISTIC WORKER CAP
            # Optimized for MSI GF63 laptops.
            try:
                hive_size = int(os.environ.get("SCAFFOLD_HIVE_WORKERS", 0))
                if hive_size <= 0:
                    hive_size = 2  # Strictly safe default
            except:
                hive_size = 2

            self.hive_pool = ProcessPoolExecutor(
                max_workers=hive_size,
                initializer=_warm_acolyte_inception,
                initargs=(str(self.engine.project_root),)
            )
            self.logger.success(f"Neural Hive Materialized. Capacity: {hive_size} Acolytes.")

    def dispatch(self, command: str, params: Dict[str, Any], req_id: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        The Sovereign Logic Gate.
        """
        clean_command = self.triage.normalize_command(command).strip()

        # [ASCENSION 4]: ZERO-OVERHEAD SACRED BYPASS
        if clean_command in self.SACRED_RITES:
            return self._conduct_sacred_rite(clean_command, params, req_id, context)

        if self._is_draining:
            return ErrorForge.forge(req_id, -32001, "Lattice Dissolving.")

        # [ASCENSION 2]: KINETIC TRIAGE
        if clean_command in self.HEAVY_RITES and not params.get('prefer_sync'):
            # [ASCENSION 2]: PREVENTION
            if os.environ.get("SCAFFOLD_HIVE_DISABLED") == "1":
                # Fallback to local thread if Hive is disabled (in Acolytes)
                return self._dispatch_to_cortex(clean_command, params, req_id, context)

            return self._dispatch_to_hive(clean_command, params, req_id, context)

        return self._dispatch_to_cortex(clean_command, params, req_id, context)

    def _conduct_sacred_rite(self, command: str, params: Dict, req_id: Any, context: Dict) -> Dict[str, Any]:
        """Sub-millisecond execution lane."""
        try:
            if command == 'daemon/anchor':
                self.engine.project_root = params.get('path')
                return {"jsonrpc": "2.0", "id": req_id, "result": {"success": True}}

            validation = self.triage.validate(command, params, context)
            if not validation[0]:
                return ErrorForge.forge(req_id, -32601, f"Rite '{command}' unmanifest.")

            result_obj = self.engine.dispatch(validation[0])
            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": result_obj.model_dump(mode='json') if hasattr(result_obj, 'model_dump') else result_obj
            }
        except Exception as e:
            return ErrorForge.forge(req_id, -32603, f"Sacred Fracture: {e}")

    def _dispatch_to_hive(self, command: str, params: Dict[str, Any], req_id: Any, context: Dict[str, Any]) -> Dict[
        str, Any]:
        """
        =============================================================================
        == THE RITE OF HIVE DISPATCH (V-Ω-TOTALITY-V20000.15-ISOMORPHIC)           ==
        =============================================================================
        LIF: 100x | ROLE: NEURAL_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_HIVE_V20000_SAB_SUTURE_2026_FINALIS
        """
        import uuid
        import time
        import gc
        import sys
        from concurrent.futures import Future

        # --- MOVEMENT I: VITALITY ADJUDICATION ---
        # Ensure the Neural Hive is manifest
        if self.hive_pool is None:
            self._ignite_hive()

        job_id = f"hive-{uuid.uuid4().hex[:6].upper()}"
        trace_id = context.get("trace_id") or context.get("x_nov_trace") or job_id

        # [ASCENSION 1]: ISOMORPHIC METABOLIC GAZE
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        is_feverish = False

        try:
            import psutil
            if psutil.virtual_memory().percent > 90:
                is_feverish = True
        except (ImportError, AttributeError):
            # WASM Heuristic: If heap > 800k objects, the tab is feverish
            if len(gc.get_objects()) > 800000:
                is_feverish = True

        if is_feverish:
            self.logger.warn(f"[{trace_id}] Hive Admission Refused: Metabolic Congestion.")
            return ErrorForge.forge(req_id, -32003, "Metabolic Fever: Rite deferred to stabilize substrate.")

        # [ASCENSION 5]: HYDRAULIC QUEUE GOVERNANCE
        # We check the internal depth of the hive pool queue
        if hasattr(self.hive_pool, '_work_queue') and self.hive_pool._work_queue.qsize() > 20:
            return ErrorForge.forge(req_id, -32003, "Hive Saturation: Backpressure threshold exceeded.")

        # --- MOVEMENT II: THE KINETIC STRIKE (FISSION) ---
        # [ASCENSION 7]: Haptic HUD Pulse
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {"type": "HIVE_SPARK", "label": f"JOB_{job_id}", "color": "#a855f7", "trace": trace_id}
            })

        try:
            # Prepare the Gnostic DNA for the worker thread
            hive_context = {
                **context,
                "job_id": job_id,
                "is_parallel": True,
                "start_ts": time.time()
            }

            # Submit the Rite to the pool
            # _execute_fission_rite is the atomic wrapper that handles Artisan instantiation
            future = self.hive_pool.submit(_execute_fission_rite, command, params, hive_context)

            # [ASCENSION 6]: Inscribe into the Registry
            if hasattr(self, '_active_jobs'):
                self._active_jobs[job_id] = {"command": command, "trace": trace_id, "start": time.time()}

        except RuntimeError as pool_fracture:
            # Pool is likely closed; fall back to the serial Cortex loop
            self.logger.error(f"Hive Pool unmanifest: {pool_fracture}. Routing to Cortex.")
            return self._dispatch_to_cortex(command, params, req_id, context)

        # =========================================================================
        # == MOVEMENT III: THE RITE OF REVELATION (CALLBACK)                     ==
        # =========================================================================
        def _on_revelation(f: Future):
            """The Achronal closure that receives the result from the Hive."""
            try:
                # [ASCENSION 4 & 11]: Fault-Isolated Soul Retrieval
                result_data = f.result()

                if result_data is None:
                    raise ValueError("Hive Revelation resulted in a Void (None).")

                # [ASCENSION 9]: Metabolic Tomography
                # Capture vitals at the moment of completion
                vitals = self.engine.watchdog.get_vitals() if hasattr(self.engine, 'watchdog') else {}

                if self.engine.akashic:
                    # Radiate the completed Gnosis to the Ocular HUD
                    self.engine.akashic.broadcast({
                        "method": "scaffold/jobComplete",
                        "params": {
                            "job_id": job_id,
                            "command": command,
                            "trace_id": trace_id,
                            "success": result_data.get('success', False),
                            "result": result_data,
                            "vitals": vitals,
                            "duration_ms": (time.time() - hive_context["start_ts"]) * 1000
                        },
                        "jsonrpc": "2.0"
                    })

            except Exception as fracture:
                # [ASCENSION 8]: Socratic Error Mapping
                err_msg = str(fracture)
                self.logger.error(f"Hive Fracture in [{job_id}]: {err_msg}")

                if self.engine.akashic:
                    self.engine.akashic.broadcast({
                        "method": "scaffold/jobComplete",
                        "params": {
                            "job_id": job_id,
                            "trace_id": trace_id,
                            "status": "FRACTURED",
                            "error": {
                                "code": -32000,
                                "message": f"Neural Hive Collapse: {err_msg}",
                                "data": traceback.format_exc() if self.logger.is_verbose else None
                            }
                        },
                        "jsonrpc": "2.0"
                    })
            finally:
                # Clean the registry
                if hasattr(self, '_active_jobs'):
                    self._active_jobs.pop(job_id, None)

        # Attach the listener to the future
        future.add_done_callback(_on_revelation)

        # --- MOVEMENT IV: THE FINALITY VOW ---
        # [ASCENSION 12]: Return the promise of matter.
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "success": True,
            "result": {
                "status": "PENDING",
                "job_id": job_id,
                "trace_id": trace_id,
                "message": f"Plea accepted. Neural Hive is materializing '{command}'."
            }
        }

    def _dispatch_to_cortex(self, command: str, params: Dict, req_id: Any, context: Dict) -> Dict:
        """High-Speed Threaded Dispatch."""
        start_time = time.perf_counter()

        def _execute():
            try:
                validation = self.triage.validate(command, params, context)
                if validation[0] is None:
                    return ErrorForge.forge(req_id, -32601, f"Rite '{command}' unmanifest.")

                result_obj = self.engine.pipeline.execute(validation[0], self.engine.dispatch)

                data = result_obj.model_dump(mode='json') if hasattr(result_obj, 'model_dump') else result_obj
                return {
                    "jsonrpc": "2.0", "id": req_id, "result": data, "success": True,
                    "stats": {"duration_ms": (time.perf_counter() - start_time) * 1000}
                }
            except Exception as e:
                return ErrorForge.forge(req_id, -32603, f"Cortex Fracture: {e}", exc=e)

        future = self.cortex_pool.submit(_execute)
        try:
            return future.result(timeout=10.0)
        except TimeoutError:
            return ErrorForge.forge(req_id, -32096, "Ocular Timeout.")
        except Exception as e:
            return ErrorForge.forge(req_id, -32603, str(e))

    def shutdown(self):
        """[ASCENSION 13]: TRANSACTIONAL DRAIN."""
        with self._shutdown_lock:
            if self._is_draining: return
            self._is_draining = True

        self.logger.system("Collapsing Neural Pools...")

        self.cortex_pool.shutdown(wait=False, cancel_futures=True)
        if self.hive_pool:
            self.hive_pool.shutdown(wait=True)

        self.logger.system("Lattice Dissolved.")

    def _spawn_zombie_reaper(self):
        """[ASCENSION 20]: BACKGROUND REAPER."""

        def _reap():
            while not self._is_draining:
                time.sleep(30)
                # Cleanup logic here (psutil based)

        threading.Thread(target=_reap, name="HiveReaper", daemon=True).start()

    @property
    def vitals(self) -> Dict[str, Any]:
        """[ASCENSION 21]: OMNISCIENT VITALS."""
        return {
            "uptime": int(time.time() - self._start_time),
            "status": "DRAINING" if self._is_draining else "ONLINE",
            "hive_active": self.hive_pool is not None,
            "cortex_pressure": self.cortex_pool._work_queue.qsize() if hasattr(self.cortex_pool, '_work_queue') else -1
        }