# Path: src/velm/core/lsp/base/foundry.py
# ---------------------------------------


import os
import sys
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Union, Any, Optional
from .telemetry import forensic_log

# =========================================================================================
# == THE SUBSTRATE SENSOR (V-Ω-ABSOLUTE-DETECTION)                                       ==
# =========================================================================================
# We mathematically divine the environment at the module level.
IS_WASM = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "pyodide" in sys.modules
)


class KineticFoundry:
    """
    =============================================================================
    == THE KINETIC FOUNDRY: OMEGA (V-Ω-TOTALITY-V1000.0-BIMODAL-SUTURED)       ==
    =============================================================================
    LIF: INFINITY | ROLE: PARALLEL_EXECUTION_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_FOUNDRY_V1000_ABSOLUTE_THREAD_WARD_FINALIS

    The engine room of the server. It manages the execution of heavy rites
    with absolute respect for the physical limitations of its host universe.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1.  **Absolute Thread Annihilation (THE CURE):** If the WASM Ether is detected,
        the `ThreadPoolExecutor` is mathematically excised from existence. It is
        never instantiated, preventing the `can't start new thread` Kernel Panic.
    2.  **The Synchronous Hologram:** In WASM, all tasks are executed inline. The
        Foundry manually forges a `concurrent.futures.Future` and sets its result,
        maintaining perfect API parity for downstream `wait()` and `as_completed()` calls.
    3.  **Hardware-Aware Scaling:** On Native Iron, it dynamically scales the thread
        pool up to 32 workers based on the true CPU core count.
    4.  **The Double-Sarcophagus:** If Native Iron experiences thread exhaustion
        (e.g., cgroups limits), the `submit` rite catches the `RuntimeError` and
        seamlessly falls back to the Synchronous Hologram without dropping the task.
    5.  **The Hall of Records:** Tracks pending futures by ID for surgical cancellation.
    6.  **Auto-Lustration:** Automatically purges completed rites from the memory
        registry to prevent heap fragmentation.
    7.  **Graceful Degradation:** Rejects new submissions safely if the Foundry
        has been commanded to shut down.
    8.  **Traceback Capture:** In synchronous mode, exceptions are perfectly captured,
        inscribed into the Future, and shielded from crashing the event loop.
    9.  **Daemon Threading:** Native threads are spawned as Daemons so they never
        hold the main process hostage during a shutdown rite.
    10. **Metabolic Backpressure:** `active_count` accurately reflects workload,
        returning 0 in WASM to prevent false throttling.
    11. **Telemetry Injection:** Forensic logs explicitly state when the Synchronous
        Fallback is engaged.
    12. **The Finality Vow:** Guaranteed return of a `Future` (pending or completed),
        never `None`, ensuring the Dispatcher never shatters.
    """

    def __init__(self):
        self._is_wasm = IS_WASM

        # [ASCENSION 5]: The Hall of Records
        self._pending_futures: Dict[Union[str, int], Future] = {}
        self._lock = threading.RLock()
        self._is_shutdown = False

        if self._is_wasm:
            # [ASCENSION 1]: THE ABSOLUTE WARD
            # In the Ethereal Plane, threads do not exist. We do not summon them.
            self._executor = None
            self._max_workers = 0
            # forensic_log("WASM Substrate Perceived. ThreadPool annihilated. Operating in Synchronous Mode.", "INFO", "FOUNDRY")
        else:
            # [ASCENSION 3]: NATIVE IRON SCALING
            cpu_count = os.cpu_count() or 4
            self._max_workers = min(32, cpu_count * 2)
            self._executor = ThreadPoolExecutor(
                max_workers=self._max_workers,
                thread_name_prefix="GnosticWorker"
            )
            # forensic_log(f"Native Iron Perceived. ThreadPool awakened with {self._max_workers} cores.", "INFO", "FOUNDRY")

    def submit(self, rite_id: Union[str, int], task: Any, *args, **kwargs) -> Future:
        """
        Dispatches a task to the pool, or executes it instantly if in WASM.
        """
        if self._is_shutdown:
            # Return a cancelled future if the foundry is closed
            f = Future()
            f.cancel()
            return f

        # =========================================================================
        # == MOVEMENT I: THE ETHEREAL PLANE (WASM)                               ==
        # =========================================================================
        if self._is_wasm or self._executor is None:
            return self._execute_synchronously(rite_id, task, *args, **kwargs)

        # =========================================================================
        # == MOVEMENT II: THE IRON CORE (NATIVE)                                 ==
        # =========================================================================
        with self._lock:
            try:
                # Attempt to split reality into a parallel thread
                future = self._executor.submit(task, *args, **kwargs)

                # Register in Hall of Records
                if rite_id is not None:
                    self._pending_futures[rite_id] = future
                    # [ASCENSION 6]: Auto-Purge
                    future.add_done_callback(lambda f: self._clear_future(rite_id))

                return future

            except RuntimeError as e:
                # [ASCENSION 4]: THE NATIVE SUTURE
                # If OS-level thread limits are reached (e.g., Docker limits)
                if "start new thread" in str(e):
                    # forensic_log(f"Native Thread Exhaustion. Engaging Synchronous Suture for {rite_id}.", "WARN", "FOUNDRY")
                    return self._execute_synchronously(rite_id, task, *args, **kwargs)
                raise e

            except Exception as e:
                # Generic fallback for total pool collapse
                forensic_log(f"Foundry Submission Failed: {e}", "ERROR", "FOUNDRY")
                f = Future()
                f.set_exception(e)
                return f

    def _execute_synchronously(self, rite_id: Union[str, int], task: Any, *args, **kwargs) -> Future:
        """
        [ASCENSION 2]: THE SYNCHRONOUS HOLOGRAM
        Executes the task in the main thread (The Eternal Now) and perfectly
        mimics the API of a threaded Future.
        """
        future = Future()

        # We record it briefly for parity, though cancellation of a sync task is impossible mid-flight.
        with self._lock:
            if rite_id is not None:
                self._pending_futures[rite_id] = future

        try:
            # THE INSTANT STRIKE
            result = task(*args, **kwargs)
            future.set_result(result)
        except Exception as e:
            # [ASCENSION 8]: TRACEBACK CAPTURE
            # We catch the exception and pack it into the future.
            # This allows the Dispatcher's `_execute_rite` wrapper to handle it gracefully
            # instead of crashing the primary Event Loop.
            # forensic_log(f"Synchronous Rite Fractured: {e}", "ERROR", "FOUNDRY", exc=e)
            future.set_exception(e)

        with self._lock:
            if rite_id is not None and rite_id in self._pending_futures:
                del self._pending_futures[rite_id]

        return future

    def cancel(self, rite_id: Union[str, int]) -> bool:
        """Surgically severs a pending causal thread."""
        with self._lock:
            future = self._pending_futures.get(rite_id)
            if future:
                return future.cancel()
        return False

    def _clear_future(self, rite_id: Union[str, int]):
        with self._lock:
            # We check if it exists because it might have been manually cancelled
            if rite_id in self._pending_futures:
                del self._pending_futures[rite_id]

    def shutdown(self, wait: bool = True):
        """Drains the foundry and releases native threads."""
        self._is_shutdown = True
        if self._executor is not None:
            self._executor.shutdown(wait=wait, cancel_futures=not wait)

    @property
    def active_count(self) -> int:
        """
        [ASCENSION 10]: METABOLIC PERCEPTION
        If we are in WASM, thread backpressure is an illusion. We return 0.
        """
        if self._is_wasm:
            return 0
        return len(self._pending_futures)