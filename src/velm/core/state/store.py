# Path: scaffold/core/state/store.py
# ----------------------------------
# LIF: INFINITY | ROLE: AKASHIC_MEMORY_CONTROLLER | RANK: SOVEREIGN
# auth_code: Ω_STORE_TOTALITY_V12_SINGULARITY

import threading
import time
import logging
from typing import Any, Dict, List, Optional, Set, Callable, Union, Iterable
from difflib import get_close_matches

# --- GNOSTIC LOGGING ---
Logger = logging.getLogger("GnosticStore")


class _GnosticStore:
    """
    =================================================================================
    == THE GNOSTIC STORE (V-Ω-TOTALITY-V12-ASCENDED)                               ==
    =================================================================================
    The Sovereign God-Engine for memory management. It serves as the single source
    of truth for all variables, states, and alchemical constants in the Cosmos.
    """

    def __init__(self):
        # The variables container
        self._variables: Dict[str, Any] = {}
        # Metadata storage for forensic audit
        self._meta: Dict[str, Dict[str, Any]] = {}
        # Subscribers for the Observer pattern
        self._subscribers: List[Callable[[str, Any], None]] = []

        # [ASCENSION 12]: Re-entrant lock for high-concurrency safety
        self._lock = threading.RLock()

        # Start the clock
        self._birth_ts = time.time()

    # =============================================================================
    # == I. INSCRIPTION RITES (WRITING)                                          ==
    # =============================================================================

    def set(self, key: str, value: Any, cast_as: Optional[type] = None):
        """
        [THE RITE OF INSCRIPTION]
        Inscribes a unit of data into the memory.
        """
        with self._lock:
            # [ASCENSION 5]: Type-Strict Inscription
            if cast_as:
                try:
                    value = cast_as(value)
                except (ValueError, TypeError) as e:
                    Logger.error(f"Type Heresy: Cannot cast {key} to {cast_as}. {e}")

            # [ASCENSION 6]: Metadata Scribing
            is_new = key not in self._variables
            self._variables[key] = value

            self._meta[key] = {
                "last_modified": time.time(),
                "mutation_count": self._meta.get(key, {}).get("mutation_count", 0) + 1,
                "is_system": key.startswith("scaffold_")
            }

            # [ASCENSION 4]: Notify the faithful
            self._notify(key, value)

    def update(self, data: Dict[str, Any]):
        """[RITE]: BULK_REALITY_MERGE"""
        with self._lock:
            for k, v in data.items():
                self.set(k, v)

    def remove(self, key: str):
        """[RITE]: ANNIHILATION"""
        with self._lock:
            if key in self._variables:
                del self._variables[key]
                del self._meta[key]
                self._notify(key, None)

    def clear(self):
        """[RITE]: TABULA_RASA"""
        with self._lock:
            self._variables.clear()
            self._meta.clear()
            Logger.warning("Gnostic Memory has returned to the Void.")

    # =============================================================================
    # == II. PERCEPTION RITES (READING)                                          ==
    # =============================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        [THE RITE OF PERCEPTION]
        Retrieves a variable. Handles recursive pointers natively.
        """
        with self._lock:
            val = self._variables.get(key, default)

            # [ASCENSION 10]: Pointer Unwinding
            # If the value is another key reference (e.g. "$$ other_var")
            if isinstance(val, str) and val.startswith("$$"):
                ptr = val.replace("$$", "").strip()
                return self.get(ptr, default)

            return val

    def get_all(self, include_hidden: bool = False) -> Dict[str, Any]:
        """[RITE]: TOTAL_RECALL"""
        with self._lock:
            if include_hidden:
                return self._variables.copy()
            # [ASCENSION 7]: Namespace Partitioning
            return {k: v for k, v in self._variables.items() if not k.startswith("_")}

    def has(self, key: str) -> bool:
        """[THE GAZE OF EXISTENCE]"""
        with self._lock:
            return key in self._variables

    def __contains__(self, key: str) -> bool:
        return self.has(key)

    def all_keys(self) -> Set[str]:
        """
        =========================================================================
        == [ASCENSION 1]: THE KEY ORACLE (FIX)                                 ==
        =========================================================================
        Returns the absolute set of all manifest identifiers.
        """
        with self._lock:
            return set(self._variables.keys())

    # =============================================================================
    # == III. DIVINATION RITES (DISCOVERY)                                       ==
    # =============================================================================

    def search(self, query: str, limit: int = 5, cutoff: float = 0.6) -> List[str]:
        """
        [THE FUZZY ORACLE]
        Finds keys similar to the query string using Levenshtein physics.
        """
        with self._lock:
            return get_close_matches(query, self._variables.keys(), n=limit, cutoff=cutoff)

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """[THE FORENSIC RECORD]"""
        with self._lock:
            return self._meta.get(key)

    # =============================================================================
    # == IV. LATTICE RITES (INTEGRATION)                                         ==
    # =============================================================================

    def subscribe(self, callback: Callable[[str, Any], None]):
        """[THE COVENANT OF THE OBSERVER]"""
        with self._lock:
            self._subscribers.append(callback)

    def _notify(self, key: str, value: Any):
        """[INTERNAL BROADCAST]"""
        for callback in self._subscribers:
            try:
                callback(key, value)
            except Exception as e:
                pass  # Prevent fractured listeners from killing the store

    def load_snapshot(self, state: Dict[str, Any]):
        """[RITE]: RESURRECTION"""
        with self._lock:
            self.clear()
            self.update(state)

    def capture_snapshot(self) -> Dict[str, Any]:
        """[RITE]: IMMUTABLE_FREEZE"""
        return self.get_all(include_hidden=True)

    def __iter__(self) -> Iterable[str]:
        """[ASCENSION 10]: Safe Iteration"""
        with self._lock:
            keys = list(self._variables.keys())
        for key in keys:
            yield key

    @property
    def vitals(self) -> Dict[str, Any]:
        """[THE PULSE]"""
        with self._lock:
            return {
                "uptime": time.time() - self._birth_ts,
                "variable_count": len(self._variables),
                "subscriber_count": len(self._subscribers),
                "total_mutations": sum(m["mutation_count"] for m in self._meta.values())
            }


# =============================================================================
# == THE SOVEREIGN INSTANCE                                                  ==
# =============================================================================
# The one true, sacred instance of the Gnostic Memory.
Store = _GnosticStore()

# === SCRIPTURE SEALED: THE MEMORY IS TITANIUM ===