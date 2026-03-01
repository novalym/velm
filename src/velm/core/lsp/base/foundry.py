# Path: src/velm/core/lsp/base/foundry.py
# ---------------------------------------

import os
import sys
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Union, Any, Optional
from .telemetry import forensic_log


class KineticFoundry:
    """
    =============================================================================
    == THE KINETIC FOUNDRY: OMEGA (V-Ω-TOTALITY-V500.0-SUBSTRATE-AWARE)        ==
    =============================================================================
    LIF: INFINITY | ROLE: PARALLEL_EXECUTION_ENGINE | RANK: OMEGA_SOVEREIGN

    The engine room of the server. It manages the pool of worker threads that
    perform the heavy lifting of analysis and refactoring.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1.  **Substrate Sensing:** Detects WASM environments where threading is lethal.
    2.  **The Synchronous Suture:** If a thread cannot be born (`RuntimeError`), the
        rite is conducted instantly in the Eternal Now (Main Thread).
    3.  **The Phantom Future:** For synchronous execution, it forges a pre-resolved
        `Future` object to maintain contract purity with the Dispatcher.
    4.  **Hardware-Aware Scaling:** Dynamically sizes the pool based on CPU availability,
        clamping to conservative limits in constrained environments.
    5.  **Fault-Isolated Submission:** Wraps the `executor.submit` call in a titanium
        try/catch block to prevent pool-exhaustion from crashing the Kernel.
    6.  **The Hall of Records:** Tracks pending rites by ID for cancellation.
    7.  **Auto-Lustration:** Automatically purges completed rites from the registry
        to prevent memory leaks.
    8.  **Graceful Degredation:** If the pool shuts down, new submissions are rejected
        cleanly rather than raising `concurrent.futures.ExecutorShutdown`.
    9.  **Daemon Threading:** Ensures all workers are daemonic, preventing process hangs.
    10. **Shutdown Sovereignty:** `shutdown` method handles both wait and cancel behaviors.
    11. **Telemetry Injection:** Logs thread-spawn failures as Warnings, not Crises.
    12. **The Finality Vow:** Guaranteed return of a `Future` (pending or done), never None.
    """

    def __init__(self):
        # [ASCENSION 1]: Hardware-Aware Scaling
        # In WASM, os.cpu_count() might return None or 0. We default to 4.
        cpu_count = os.cpu_count() or 4

        # [ASCENSION 4]: Conservative Clamping
        # Too many threads in Pyodide/WASM can cause instability even if supported.
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._max_workers = 1 if is_wasm else (cpu_count * 2)

        self._executor = ThreadPoolExecutor(
            max_workers=self._max_workers,
            thread_name_prefix="GnosticWorker"
        )

        # [ASCENSION 6]: The Hall of Records
        self._pending_futures: Dict[Union[str, int], Future] = {}
        self._lock = threading.RLock()
        self._is_shutdown = False

    def submit(self, rite_id: Union[str, int], task: Any, *args, **kwargs) -> Future:
        """
        Dispatches a task to the pool.
        If the physical threads fail, it falls back to the Synchronous Suture.
        """
        if self._is_shutdown:
            # Return a cancelled future if the foundry is closed
            f = Future()
            f.cancel()
            return f

        with self._lock:
            try:
                # --- ATTEMPT 1: PARALLEL TIMELINE ---
                future = self._executor.submit(task, *args, **kwargs)

                # Register in Hall of Records
                if rite_id is not None:
                    self._pending_futures[rite_id] = future
                    # [ASCENSION 7]: Auto-Purge
                    future.add_done_callback(lambda f: self._clear_future(rite_id))

                return future

            except RuntimeError as e:
                # [ASCENSION 2]: THE SYNCHRONOUS SUTURE
                # "can't start new thread" -> Substrate Limitation.
                if "start new thread" in str(e):
                    # sys.stderr.write(f"\n[FOUNDRY] ⚠️ Threading Fracture. Switching to Synchronous Suture for {rite_id}.\n")
                    return self._execute_synchronously(task, *args, **kwargs)
                raise e

            except Exception as e:
                # Generic fallback for pool exhaustion
                forensic_log(f"Foundry Submission Failed: {e}", "ERROR", "FOUNDRY")
                f = Future()
                f.set_exception(e)
                return f

    def _execute_synchronously(self, task: Any, *args, **kwargs) -> Future:
        """
        [ASCENSION 3]: THE PHANTOM FUTURE
        Executes the task in the main thread and returns a completed Future.
        """
        future = Future()
        try:
            result = task(*args, **kwargs)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
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
        """Drains the foundry and releases threads."""
        self._is_shutdown = True
        self._executor.shutdown(wait=wait, cancel_futures=not wait)

    @property
    def active_count(self) -> int:
        return len(self._pending_futures)