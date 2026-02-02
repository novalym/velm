# scaffold/symphony/conductor_core/context/manager.py

from __future__ import annotations

import time
import os
import threading
import copy
import json
import sys
from pathlib import Path, WindowsPath, PosixPath
from typing import Dict, Any, MutableMapping, Iterator, Optional, TYPE_CHECKING, List, Union, Callable, Set
from contextlib import contextmanager

from .vault import GnosticVault
from .scope import EphemeralScope
from ....logger import Scribe
from ....contracts.symphony_contracts import SecretSource, ActionResult
from .... import __version__ as SCAFFOLD_VERSION

if TYPE_CHECKING:
    from ...conductor import SymphonyConductor
    from ....interfaces.requests import SymphonyRequest

Logger = Scribe('GnosticContextManager')

# Dynamically inherit from the correct concrete Path class for this OS.
_PathBase = WindowsPath if os.name == 'nt' else PosixPath


class GnosticPath(_PathBase):
    """
    [FACULTY 12] The Callable Path.
    Heals the 'Path object is not callable' heresy if a template tries to invoke a path
    as a function. It returns itself as a string, preserving sanity.
    """

    def __call__(self, *args, **kwargs):
        return self.as_posix()


class GnosticContextManager(MutableMapping[str, Any]):
    """
    =================================================================================
    == THE SENTIENT STATE ENGINE (V-Ω-SINGULARITY-ULTIMA-DEFINITIVE)               ==
    =================================================================================
    LIF: 10,000,000,000,000 (THE UNBREAKABLE HEART OF GNOSIS)

    The central repository of truth for the Symphony.
    It manages Variables, Secrets (Vault), and the physical location of reality (Sanctum).

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Sovereign Link:** Explicitly exposes `self.conductor` to allow
        subordinate artisans to query the Symphony's global state.
    2.  **The Raw Revelation:** Restores the `raw()` method as the authoritative
        accessor for the internal variable dictionary.
    3.  **The Thread-Safe Heart:** All state mutations are guarded by a `threading.RLock`.
    4.  **The Gnostic Vault:** Integrates `GnosticVault` for secret management.
    5.  **The History Ledger:** Records every variable change with a timestamp.
    6.  **The Reactive Mind:** Implements an Observer pattern for UI updates.
    7.  **The Ephemeral Fork:** Can `fork()` into a detached child context.
    8.  **The Scoped Mutation:** Provides a `temporary_context` manager.
    9.  **The Path Alchemist:** Transmutes `Path` -> `GnosticPath` for template safety.
    10. **The Environment Hydrator:** Absorbs `SC_*` environment variables on birth.
    11. **The Serializable Face:** Provides `snapshot()`/`restore()` for checkpoints.
    12. **The Replication Rite (THE FIX):** Implements `copy()` to satisfy the
        Divine Alchemist's need for context isolation.
    """

    def __init__(
            self,
            conductor: 'SymphonyConductor',
            request: 'SymphonyRequest',
            execution_root: Path,
            parent_context: Optional['GnosticContextManager'] = None
    ):
        self._conductor = conductor
        self._project_root = execution_root

        # [FACULTY 3] The Thread-Safe Heart
        self._lock = threading.RLock()

        # [FACULTY 4] The Gnostic Vault
        self._vault = GnosticVault()

        # [FACULTY 5] The History Ledger
        self._history: List[Dict[str, Any]] = []

        # [FACULTY 6] The Reactive Mind
        self._listeners: List[Callable[[str, Any], None]] = []

        # Internal State Storage
        # If forking, we copy the parent's soul.
        if parent_context:
            with parent_context._lock:
                self._context = copy.deepcopy(parent_context.raw())
                # Inherit Vault reference (shared secrets)
                self._vault = parent_context._vault
        else:
            self._context: Dict[str, Any] = {}
            self.hydrate()

        # Initialize core variables
        self._context['project_root'] = self._project_root
        self._context['scaffold_version'] = SCAFFOLD_VERSION

        # Merge Request Variables (CLI overrides)
        if request and request.variables:
            for k, v in request.variables.items():
                self[k] = v

    @property
    def conductor(self) -> 'SymphonyConductor':
        """[FACULTY 1] The Sovereign Link."""
        return self._conductor

    def raw(self) -> Dict[str, Any]:
        """
        [FACULTY 2] The Raw Revelation.
        Returns a direct reference to the internal dictionary.
        Use with caution; bypasses locks/listeners.
        """
        return self._context

    @property
    def variables(self) -> Dict[str, Any]:
        """Thread-safe copy of variables."""
        with self._lock:
            return self._context.copy()

    @property
    def cwd(self) -> Path:
        """The current working directory of the Symphony."""
        return self._context.get('cwd', self._project_root)

    @property
    def project_root(self) -> Path:
        return self._project_root

    @property
    def vault(self) -> GnosticVault:
        """[FACULTY 4] Access to the Secret Keeper."""
        return self._vault

    def get_vault(self) -> GnosticVault:
        """Alias for compatibility."""
        return self._vault

    @property
    def last_process_result(self) -> Optional[ActionResult]:
        """[FACULTY 12] The Last Reality Memory."""
        return self._context.get('_last_result')

    @last_process_result.setter
    def last_process_result(self, result: ActionResult):
        with self._lock:
            self._context['_last_result'] = result

    def update_variable(self, key: str, value: Any):
        """Thread-safe setter with notifications."""
        self[key] = value

    def set_sanctum(self, path_str: str):
        """Updates the CWD (Current Sanctum)."""
        new_path = Path(path_str).resolve()
        if not new_path.is_absolute():
            new_path = (self.cwd / path_str).resolve()
        self['cwd'] = new_path
        self['sanctum'] = new_path

    def resolve_secret(self, source: SecretSource) -> str:
        """Resolves a secret using the Vault."""
        return self._vault.resolve_source(source)

    def subscribe(self, callback: Callable[[str, Any], None]):
        """[FACULTY 6] The Reactive Mind."""
        with self._lock:
            self._listeners.append(callback)

    def _notify_listeners(self, key: str, value: Any):
        for callback in self._listeners:
            try:
                callback(key, value)
            except Exception:
                pass  # Listeners must not crash the Engine

    def fork(self) -> 'GnosticContextManager':
        """[FACULTY 7] The Ephemeral Fork."""
        with self._lock:
            return GnosticContextManager(
                self._conductor,
                None,  # No new request
                self._project_root,
                parent_context=self
            )

    @contextmanager
    def temporary_context(self, overrides: Dict[str, Any]):
        """[FACULTY 8] The Scoped Mutation."""
        # Snapshot current state
        with self._lock:
            snapshot = self.variables

        # Apply overrides
        scope = EphemeralScope(self, overrides)
        try:
            with scope:
                yield self
        finally:
            # Restore state (handled by EphemeralScope logic, but double check)
            pass

    def snapshot(self) -> Dict[str, Any]:
        """[FACULTY 11] The Serializable Face."""
        with self._lock:
            # We filter out non-serializable objects for the dump
            safe_data = {}
            for k, v in self._context.items():
                if self._ensure_serializable(v):
                    safe_data[k] = v
                else:
                    safe_data[k] = str(v)
            return safe_data

    def restore(self, snapshot: Dict[str, Any]):
        """Restores state from a snapshot."""
        with self._lock:
            self._context.update(snapshot)

    def hydrate(self):
        """[FACULTY 10] The Environment Hydrator."""
        for k, v in os.environ.items():
            if k.startswith("SC_"):
                key_name = k[3:].lower()
                self._context[key_name] = v

    def _record_history(self, event: str, key: str, value: Any):
        """[FACULTY 5] The History Ledger."""
        self._history.append({
            "timestamp": time.time(),
            "event": event,
            "key": key,
            "value_type": type(value).__name__
        })

    def _recursive_transmute(self, value: Any, depth: int = 0) -> Any:
        """[FACULTY 9] The Path Alchemist (Recursive)."""
        if depth > 10: return value

        if isinstance(value, Path) and not isinstance(value, GnosticPath):
            return GnosticPath(value)
        elif isinstance(value, dict):
            return {k: self._recursive_transmute(v, depth + 1) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._recursive_transmute(v, depth + 1) for v in value]
        return value

    def _ensure_serializable(self, value: Any) -> bool:
        try:
            json.dumps(value)
            return True
        except:
            return False

    # --- MutableMapping Implementation ---

    def __getitem__(self, key: str) -> Any:
        with self._lock:
            return self._context[key]

    def __setitem__(self, key: str, value: Any):
        with self._lock:
            transmuted_value = self._recursive_transmute(value)
            self._context[key] = transmuted_value
            self._record_history("SET", key, transmuted_value)
            self._notify_listeners(key, transmuted_value)

    def _gnostic_update(self, key: str, value: Any):
        """Direct update bypassing alchemy (internal use)."""
        self._context[key] = value

    def __delitem__(self, key: str):
        with self._lock:
            del self._context[key]
            self._record_history("DELETE", key, None)

    def __iter__(self) -> Iterator[str]:
        with self._lock:
            return iter(self._context)

    def __len__(self) -> int:
        with self._lock:
            return len(self._context)

    # --- [FACULTY 12] THE RITE OF REPLICATION (THE FIX) ---
    def copy(self) -> Dict[str, Any]:
        """
        Creates a shallow copy of the internal dictionary.
        This satisfies the 'DivineAlchemist' when it attempts to isolate
        the render context for Jinja2 templates.
        """
        with self._lock:
            return self._context.copy()

    def __repr__(self):
        return f"<GnosticContextManager keys={len(self)} root={self._project_root}>"