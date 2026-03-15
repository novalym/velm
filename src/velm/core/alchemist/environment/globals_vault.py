# Path: core/alchemist/environment/globals_vault.py
# -------------------------------------------------


import threading
from collections.abc import MutableMapping
from typing import Dict, Any, Iterator, Callable

from ....logger import Scribe

Logger = Scribe("SGFGlobalsVault")


class SGFGlobalsVault(MutableMapping):
    """
    =================================================================================
    == THE SGF GLOBALS VAULT: OMEGA POINT (V-Ω-TOTALITY-VMAX-STATE-ISOLATION)      ==
    =================================================================================
    LIF: ∞ | ROLE: DYNAMIC_FUNCTION_HOLDER | RANK: OMEGA_SOVEREIGN

    This organ holds globally available Python functions, macros, and constants.
    It replaces `.env.globals` and serves as the destination for the `@py_func`
    directive.

    ### THE PANTHEON OF 8 LEGENDARY ASCENSIONS:
    1.  **State Isolation Suture:** Prevents `eval` and `exec` leakage from
        polluting the actual Python `globals()`, confining them to this warded object.
    2.  **Thread-Safe Registration:** Uses an RLock to ensure parallel blueprint
        parsing doesn't overwrite dynamic functions.
    3.  **Transparent Introspection:** Conforms to `MutableMapping` to allow
        the `scaffold_scribe` to iterate over its contents seamlessly.
    4.  **Auto-Pruning Sieve:** Allows the engine to drop specific ephemeral
        functions between parses to prevent memory bloating.
    =================================================================================
    """

    def __init__(self):
        self._globals: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def __getitem__(self, key: str) -> Any:
        with self._lock:
            return self._globals[key]

    def __setitem__(self, key: str, value: Any):
        """[ASCENSION 1]: Warded Registration."""
        with self._lock:
            self._globals[key] = value

    def __delitem__(self, key: str):
        with self._lock:
            del self._globals[key]

    def __iter__(self) -> Iterator[str]:
        """[ASCENSION 3]: Transparent Introspection."""
        with self._lock:
            yield from self._globals

    def __len__(self) -> int:
        with self._lock:
            return len(self._globals)

    def purge_ephemeral(self):
        """[ASCENSION 4]: Evaporates dynamically compiled logic."""
        with self._lock:
            keys_to_purge = [k for k, v in self._globals.items() if not k.startswith('_')]
            for k in keys_to_purge:
                del self._globals[k]
            Logger.debug(f"Globals Vault purified. {len(keys_to_purge)} souls returned to the void.")

    def __repr__(self) -> str:
        return f"<Ω_SGF_GLOBALS_VAULT size={len(self._globals)} status=RESONANT>"