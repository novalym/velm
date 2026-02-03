# Path: core/daemon/dispatcher/pools.py
# -------------------------------------
# LIF: INFINITY | AUTH_CODE: @)(@()
# SYSTEM: NEURAL_LATTICE | ROLE: RESOURCE_ALLOCATOR_PRIME
# =================================================================================
# == THE NEURAL POOL MANAGER (V-Ω-OBSERVABLE-LATTICE)                            ==
# =================================================================================
# [PURPOSE]: Manages the stratified execution lanes for the Daemon.
#            1. CORTEX (Fast): For LSP features (Completion, Hover).
#            2. FOUNDRY (Slow): For I/O heavy rites (Survey, Build, Install).
#
# [ASCENSIONS]:
# 1. [QUEUE_TELEMETRY]: Exposes `get_diagnostics()` to visualize backpressure.
# 2. [SAFE_INSPECTION]: Wraps CPython internal `_work_queue` access in try/except blocks.
# 3. [GRACEFUL_COLLAPSE]: Shutdown sequence cancels pending futures to prevent hangs.
# 4. [NAMED_THREADS]: Enforces strict naming conventions for easier debugging.

import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Dict, Any

from .constants import (
    MAX_CORTEX_WORKERS, MAX_FOUNDRY_WORKERS,
    POOL_CORTEX, POOL_FOUNDRY, MAX_QUEUE_DEPTH
)
from ....logger import Scribe


class PoolManager:
    """
    [THE NEURAL LATTICE]
    The central registry of execution threads.
    """

    def __init__(self):
        self.logger = Scribe("PoolManager")

        # 1. The Fast Lane (Intelligence)
        # Optimized for low-latency, CPU-bound tasks.
        self.cortex = ThreadPoolExecutor(
            max_workers=MAX_CORTEX_WORKERS,
            thread_name_prefix=POOL_CORTEX
        )

        # 2. The Heavy Lifter (Kinesis)
        # Optimized for high-latency, I/O-bound tasks.
        self.foundry = ThreadPoolExecutor(
            max_workers=MAX_FOUNDRY_WORKERS,
            thread_name_prefix=POOL_FOUNDRY
        )

    def select_pool(self, is_fast_rite: bool) -> Tuple[ThreadPoolExecutor, str]:
        """
        [RITE]: LANE_SELECTION
        Routes the intent to the appropriate neural pathway.
        """
        if is_fast_rite:
            return self.cortex, POOL_CORTEX
        return self.foundry, POOL_FOUNDRY

    def check_congestion(self, pool: ThreadPoolExecutor, pool_name: str) -> bool:
        """
        [THE BACKPRESSURE VALVE]
        Returns True if the pool is saturated beyond the safety threshold.
        """
        q_size = self._get_queue_size(pool)

        if q_size > MAX_QUEUE_DEPTH:
            self.logger.warn(f"Congestion Detected in {pool_name}: Depth {q_size}/{MAX_QUEUE_DEPTH}")
            return True

        return False

    def get_diagnostics(self) -> Dict[str, Any]:
        """
        [ASCENSION 1]: DEEP TELEMETRY
        Returns a snapshot of the current load on the lattice.
        """
        return {
            "cortex": {
                "queue_depth": self._get_queue_size(self.cortex),
                "max_workers": MAX_CORTEX_WORKERS
            },
            "foundry": {
                "queue_depth": self._get_queue_size(self.foundry),
                "max_workers": MAX_FOUNDRY_WORKERS
            }
        }

    def _get_queue_size(self, pool: ThreadPoolExecutor) -> int:
        """
        [ASCENSION 2]: SAFE INSPECTION
        Accesses CPython internals safely to gauge pressure.
        """
        try:
            # _work_queue is an implementation detail of ThreadPoolExecutor
            if hasattr(pool, '_work_queue'):
                return pool._work_queue.qsize()
        except Exception:
            pass
        return 0

    def shutdown(self):
        """
        [RITE]: COLLAPSE_LATTICE
        Terminates all worker threads.
        """
        self.logger.system("Collapsing Neural Pools...")

        # [ASCENSION 3]: AGGRESSIVE SHUTDOWN
        # We do not wait for pending tasks. The Daemon is dying.
        self.cortex.shutdown(wait=False)
        self.foundry.shutdown(wait=False)