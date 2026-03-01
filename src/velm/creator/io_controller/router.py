# Path: src/velm/creator/io_controller/router.py
# ----------------------------------------------

import os
import sys
import threading
import hashlib
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Dict, Tuple, Optional, Any, Final

from ...core.sanctum.base import SanctumInterface
from ...core.sanctum.factory import SanctumFactory
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("IORouter")


class IORouter:
    """
    Universal Protocol Multiplexer.

    Maps diverse connection strings (file://, s3://, memory://, ssh://) to their
    respective I/O drivers (Sanctums). Handles connection pooling, thread-safe access,
    and environment-aware fallbacks.
    """

    def __init__(self, project_root: Optional[Path] = None, force_memory: bool = False):
        self.project_root = (project_root or Path.cwd()).resolve()

        # Enables the redirection of all physical file writes to the RAM disk for dry-runs
        self.force_memory = force_memory

        # Detect WebAssembly environment to apply proper IDBFS behaviors
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Connection Pool Cache to reuse authenticated cloud drivers
        self._active_sanctums: Dict[str, SanctumInterface] = {}
        self._lock = threading.RLock()

        # In WASM environments, 'file' maps to the persistent IDBFS layer rather than an ephemeral void.
        self._default_scheme = "memory" if self.force_memory else "file"

    def resolve(self, uri_or_path: str) -> Tuple[SanctumInterface, str]:
        """
        Parses a URI and returns an initialized connection driver and relative path.
        """
        if not uri_or_path:
            raise ArtisanHeresy("Cannot resolve an empty URI string.")

        uri_str = str(uri_or_path).strip()

        # Normalize Windows local drive letters to prevent scheme parsing errors (C:/ -> file:///C:/)
        if os.name == 'nt' and len(uri_str) > 1 and uri_str[1] == ":" and "://" not in uri_str:
            uri_str = f"file:///{uri_str.replace('\\', '/')}"

        # If no protocol is specified, attach the default fallback
        if "://" not in uri_str:
            if self.force_memory:
                uri_str = f"memory://{uri_str.lstrip('/')}"
            else:
                abs_path = os.path.abspath(os.path.join(str(self.project_root), uri_str))
                uri_str = f"file://{abs_path.replace('\\', '/')}"

        try:
            parsed = urlparse(uri_str)
            scheme = parsed.scheme.lower()

            # Extract query parameters to pass as configuration dictionary to drivers
            driver_config = {}
            if parsed.query:
                query_params = parse_qs(parsed.query)
                driver_config = {k: v[0] for k, v in query_params.items()}

            if scheme == "s3":
                internal_path = parsed.path.lstrip('/')
            elif scheme in ("file", "local"):
                internal_path = parsed.path
                if os.name == 'nt' and internal_path.startswith('/') and len(internal_path) > 2 and internal_path[
                    2] == ':':
                    internal_path = internal_path.lstrip('/')
            else:
                internal_path = parsed.path.lstrip('/')

        except Exception as e:
            raise ArtisanHeresy(
                f"Failed to parse URI: '{uri_str}'.",
                details=str(e),
                severity=HeresySeverity.CRITICAL
            )

        with self._lock:
            # Cache keys are generated per remote endpoint to pool connections
            cache_key = f"{scheme}://{parsed.netloc}"

            if cache_key not in self._active_sanctums:
                try:
                    sanctum = SanctumFactory.forge(uri_str, config=driver_config)
                    self._active_sanctums[cache_key] = sanctum
                except Exception as e:
                    raise ArtisanHeresy(
                        f"Failed to initialize driver for protocol '{scheme}://'.",
                        details=str(e),
                        severity=HeresySeverity.CRITICAL
                    )

            return self._active_sanctums[cache_key], internal_path

    def get_default_driver(self) -> SanctumInterface:
        """Returns the active driver mapped to the current working directory."""
        driver, _ = self.resolve(".")
        return driver

    def close_all(self):
        """Flushes and cleanly closes all active file descriptors and network sockets."""
        with self._lock:
            for key, sanctum in list(self._active_sanctums.items()):
                try:
                    if hasattr(sanctum, 'close'):
                        sanctum.close()
                except Exception:
                    pass

            self._active_sanctums.clear()


    def __repr__(self) -> str:
        return f"<IORouter substrate={'ETHER' if self.is_wasm else 'IRON'} bridges={len(self._active_sanctums)}>"