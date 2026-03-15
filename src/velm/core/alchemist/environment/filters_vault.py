# Path: core/alchemist/environment/filters_vault.py
# -------------------------------------------------


import threading
from collections.abc import MutableMapping
from typing import Dict, Any, Iterator, Callable

from ..elara.library.registry import RITE_REGISTRY
from ....logger import Scribe

Logger = Scribe("SGFFiltersVault")


class SGFFiltersVault(MutableMapping):
    """
    =================================================================================
    == THE SGF FILTERS VAULT: OMEGA POINT (V-Ω-TOTALITY-VMAX-BICAMERAL-MAPPING)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: POLYMORPHIC_RITE_PROVIDER | RANK: OMEGA_SOVEREIGN

    [THE MASTER CURE]: This is a mathematically brilliant Trojan Horse. It behaves
    *exactly* like a standard Python Dictionary to satisfy the `scaffold_scribe.py`
    and legacy Jinja introspectors (`alchemist.env.filters.items()`).

    However, underneath its skin, it is a **Bicameral Router**. It dynamically
    merges ad-hoc filters defined in blueprints (`@filter`) with the infinite
    power of the SGF `RITE_REGISTRY`.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Bicameral Iteration:** `__iter__` seamlessly chains local user filters
        and global SGF rites without duplicating memory.
    2.  **O(1) Dynamic Fallback:** `__getitem__` checks local RAM, then instantly
        scries the SGF registry, returning the raw callable for `inspect`.
    3.  **Jinja-Parity Suture:** Allows `alchemist.env.filters['my_filter'] = lambda...`
        to work natively without modifying the immutable core registry.
    4.  **Thread-Safe Mutation:** Uses RLock to ensure ad-hoc injections from
        parallel macro expansions do not collide.
    =================================================================================
    """

    def __init__(self):
        self._local_filters: Dict[str, Callable] = {}
        self._lock = threading.RLock()

    def __getitem__(self, key: str) -> Callable:
        """[ASCENSION 2]: O(1) Dynamic Fallback."""
        with self._lock:
            # 1. Scry Local Ad-Hoc Filters
            if key in self._local_filters:
                return self._local_filters[key]

            # 2. Scry the Omniscient SGF Registry
            rite = RITE_REGISTRY.get_rite_metadata(key)
            if rite and hasattr(rite, 'handler'):
                return rite.handler

        raise KeyError(f"Gnostic Filter '{key}' is unmanifest.")

    def __setitem__(self, key: str, value: Callable):
        """[ASCENSION 3]: Jinja-Parity Suture for @filter injections."""
        if not callable(value):
            raise ValueError(f"Filter '{key}' must be a Callable Soul.")
        with self._lock:
            self._local_filters[key] = value
            Logger.verbose(f"Ad-Hoc Filter '{key}' sutured into the local vault.")

    def __delitem__(self, key: str):
        with self._lock:
            del self._local_filters[key]

    def __iter__(self) -> Iterator[str]:
        """[ASCENSION 1]: Bicameral Iteration for Introspectors."""
        with self._lock:
            # Yield Local filters first
            yield from self._local_filters

            # Yield Global SGF filters, avoiding duplicates
            for k in RITE_REGISTRY._GLOBAL_INDEX.keys():
                if k not in self._local_filters:
                    yield k

    def __len__(self) -> int:
        with self._lock:
            # Fast length calculation across both strata
            return len(self._local_filters) + len(
                [k for k in RITE_REGISTRY._GLOBAL_INDEX if k not in self._local_filters])

    def __repr__(self) -> str:
        return f"<Ω_SGF_FILTERS_VAULT local={len(self._local_filters)} global={len(RITE_REGISTRY._GLOBAL_INDEX)}>"