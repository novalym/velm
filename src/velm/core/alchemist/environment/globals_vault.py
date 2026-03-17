# Path: core/alchemist/environment/globals_vault.py
# -------------------------------------------------

import os
import time
import uuid
import secrets
import threading
from collections.abc import MutableMapping
from typing import Dict, Any, Iterator

from ....logger import Scribe

Logger = Scribe("SGFGlobalsVault")

class CryptoProxy:
    """
    =============================================================================
    == THE CRYPTOGRAPHIC PROXY (V-Ω-TOTALITY-VMAX)                             ==
    =============================================================================
    LIF: ∞ | ROLE: ENTROPY_GENERATOR | RANK: MASTER

    Provides deterministic and high-entropy cryptographic generation natively
    within the SGF template context. Annihilates the 'crypto undefined' heresy.
    """
    def random(self, length: int = 32, fmt: str = 'hex') -> str:
        """Forges a secure token of willed length and format."""
        if fmt == 'hex':
            return secrets.token_hex(length // 2)
        if fmt == 'base64':
            import base64
            return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')
        return secrets.token_hex(length // 2)

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
    5.  **The Cryptographic Suture (THE MASTER CURE):** Pre-loads `crypto`, `env`,
        `uuid`, and `now` into the primordial state, mathematically guaranteeing
        that `{{ crypto.random(64) }}` never falls to the Void.
    =================================================================================
    """

    def __init__(self):
        # [ASCENSION 5]: THE PRIMORDIAL GNOSIS
        self._globals: Dict[str, Any] = {
            "env": lambda k, d="": os.getenv(k, d),
            "crypto": CryptoProxy(),
            "uuid": lambda: str(uuid.uuid4()),
            "uuid_v4": lambda: str(uuid.uuid4()),
            "now": lambda: time.time(),
        }
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
            # We preserve our primordial functions (crypto, env, etc.)
            keys_to_purge =[k for k in self._globals.keys() if not k.startswith('_') and k not in {"env", "crypto", "uuid", "uuid_v4", "now"}]
            for k in keys_to_purge:
                del self._globals[k]
            Logger.debug(f"Globals Vault purified. {len(keys_to_purge)} souls returned to the void.")

    def __repr__(self) -> str:
        return f"<Ω_SGF_GLOBALS_VAULT size={len(self._globals)} status=RESONANT>"