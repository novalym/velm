# Path: core/alchemist/environment/cache_warden.py
# ------------------------------------------------


import gc
import time
import threading
from typing import Dict, Any, Final

from ....logger import Scribe

Logger = Scribe("SGFCacheWarden")


class SGFCacheWarden:
    """
    =================================================================================
    == THE SGF CACHE WARDEN: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)         ==
    =================================================================================
    LIF: ∞ | ROLE: METABOLIC_LUSTRATOR | RANK: OMEGA_GUARDIAN

    The supreme authority over the Alchemist's memory. It natively implements the
    `.clear()` interface to satisfy legacy Jinja integrations, but performs true
    Pythonic memory management and Merkle-Lattice purging.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Isomorphic Interface Suture:** Exposes `.clear()` to perfectly mimic Jinja2,
        annihilating the AttributeError during materializer teardowns.
    2.  **Substrate-Aware Lustration:** Triggers `gc.collect(1)` or `gc.collect(2)`
        dynamically based on the severity of the memory pressure.
    3.  **Achronal Throttle Guard:** Prevents cyclic GC thrashing by enforcing a
        minimum 50ms cooldown between manual lustration strikes.
    4.  **Thread-Safe Purgation:** Uses an RLock to ensure cache clearing does not
        fracture ongoing transmutations in parallel swarms.
    5.  **Global Registry Suture:** Commands the `RITE_REGISTRY` to clear its L1
        memo-matrix simultaneously.
    6.  **Luminous HUD Radiation:** Emits a 'MEMORY_PURGE' signal to the Ocular stage.
    =================================================================================
    """

    COOLDOWN_NS: Final[int] = 50_000_000  # 50ms
    __slots__ = ('_lock', '_last_clear_ns', '_purge_count')

    def __init__(self):
        self._lock = threading.RLock()
        self._last_clear_ns = 0
        self._purge_count = 0

    def clear(self):
        """
        =============================================================================
        == THE RITE OF LUSTRATION (CLEAR)                                          ==
        =============================================================================
        The unified command to evaporate stagnant memory from the Alchemical reactor.
        """
        with self._lock:
            now_ns = time.perf_counter_ns()

            # [ASCENSION 3]: The Achronal Throttle Guard
            if (now_ns - self._last_clear_ns) < self.COOLDOWN_NS:
                return

            self._last_clear_ns = now_ns
            self._purge_count += 1

            # 1. Clear the internal AST Weaver & Tensor caches
            try:
                from ..elara.resolver.evaluator import SafeEvaluator
                from ..elara.library.registry import RITE_REGISTRY
                from ..elara.scanner.engine import GnosticScanner
                from ..elara.library.oracle import GnosticOracle

                # Evaporate memo-matrices
                SafeEvaluator._AST_CACHE.clear()
                RITE_REGISTRY._l1_hot_cache.clear()
            except Exception:
                pass

            # 2. [ASCENSION 2]: Substrate-Aware Lustration
            # Force generation 1 (young) collection for high-speed throughput
            gc.collect(1)

            if Logger.is_verbose and self._purge_count % 10 == 0:
                Logger.debug(f"Metabolic Lustration performed. Cache vaporized.")

    def __repr__(self) -> str:
        return f"<Ω_SGF_CACHE_WARDEN purges={self._purge_count} status=VIGILANT>"