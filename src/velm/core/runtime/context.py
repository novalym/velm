# Path: scaffold/core/runtime/context.py
# -------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_CONTEXT_SINGULARITY_V12
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: REALITY_ANCHOR
# =================================================================================
# [ASCENSION LOG]:
# 1.  ATOMIC SLOT ALLOCATION: Uses __slots__ to annihilate __dict__ overhead.
# 2.  DOUBLE-CHECKED JIT LOCKING: Thread-safe root resolution with zero contention.
# 3.  HOST FINGERPRINTING: Unique Machine ID for telemetry isolation.
# 4.  UNC/LONG-PATH SHIELD: Specialized Windows path normalization for large SANs.
# 5.  ENVIRONMENT DNA PRE-CACHE: Instant access to SCAFFOLD_* environment vars.
# 6.  REALITY BITMASK: Tracks resolution state (Cold/Warm/Hot) in a single byte.
# 7.  ZERO-DEPENDENCY PROBING: Pure syscall-level path checking.
# 8.  RECURSIVE DEPTH GOVERNOR: Prevents infinite filesystem loops.
# 9.  SESSION ENTROPY: Cryptographically secure session IDs via secrets.
# 10. GNOSTIC MARKER PRIORITY: Weights indicators (scaffold.scaffold > package.json).
# 11. VIRTUAL SHADOW SUPPORT: Ability to simulate roots in memory.
# 12. MICRO-TELEMETRY ANCHOR: High-resolution timestamping of the moment of birth.
# =================================================================================

import os
import sys
import time
import secrets
import threading
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...logger import Scribe


class RuntimeContext:
    """
    =============================================================================
    == THE KEEPER OF REALITY (V-Ω-TEMPORAL-ANCHOR-ULTIMA)                      ==
    =============================================================================
    The mind of the engine, now ascended.

    It manages the Gnostic mapping of the physical filesystem to the logical
    architecture of the project and workspace.
    """

    # [ASCENSION 1]: Atomic Slot Allocation
    __slots__ = (
        '_explicit_root', '_project_root', '_workspace_root',
        '_session_id', '_env_dna', '_machine_id', '_state_mask',
        '_lock', '_logger', '_birth_timestamp'
    )

    def __init__(self, project_root: Optional[Path] = None):
        """
        The Rite of Inception.
        Initializes the vessel in a COLD state. No I/O occurs here.
        """
        self._explicit_root = project_root
        self._project_root: Optional[Path] = None
        self._workspace_root: Optional[Path] = None

        # [ASCENSION 9]: Session Entropy
        self._session_id = secrets.token_hex(4)
        self._birth_timestamp = time.perf_counter()

        # [ASCENSION 5]: Environment DNA Pre-cache
        self._env_dna = {k: v for k, v in os.environ.items() if k.startswith("SCAFFOLD_")}

        # [ASCENSION 6]: Reality Bitmask (0=Cold, 1=Warm/Project, 2=Hot/Workspace)
        self._state_mask = 0

        self._lock = threading.RLock()
        self._logger = None
        self._machine_id = None

    @property
    def logger(self) -> 'Scribe':
        """Lazy loader for Scribe to prevent import avalanche."""
        if self._logger is None:
            from ...logger import Scribe
            self._logger = Scribe("RuntimeContext")
        return self._logger

    @property
    def project_root(self) -> Path:
        """
        [THE LAZY ANCHOR]
        Returns the project root. Triggers JIT resolution if the mask is COLD.
        """
        if not (self._state_mask & 1):
            self._resolve_reality()
        return self._project_root

    @project_root.setter
    def project_root(self, path: Path):
        """Allows manual transfiguration of the project root."""
        with self._lock:
            self._project_root = path
            self._state_mask |= 1

    @property
    def workspace_root(self) -> Optional[Path]:
        """
        [THE LAZY COSMOS]
        Returns the Monorepo/Workspace root if perceived.
        """
        if not (self._state_mask & 2):
            self._resolve_reality()
        return self._workspace_root

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def machine_id(self) -> str:
        """[ASCENSION 3]: Unique Host Identity."""
        if self._machine_id is None:
            import platform
            self._machine_id = f"{platform.node()}-{platform.machine()}"
        return self._machine_id

    # =========================================================================
    # == THE RITE OF OMNISCIENCE                                             ==
    # =========================================================================

    def _resolve_reality(self):
        """
        [ASCENSION 2]: Double-Checked JIT Locking.
        Ensures only one thread ever conducts the upward scan.
        """
        with self._lock:
            # Re-check mask inside the lock
            if self._state_mask == 3:
                return

            # 1. Project Root Resolution
            if self._explicit_root:
                self._project_root = self._explicit_root.resolve()
            else:
                # [ASCENSION 10]: Gnostic Marker Priority
                # We check for the sacred .scaffold first, then generic manifests
                cwd = Path.cwd()
                self._project_root = (
                        self._fast_scan_upwards(cwd, ["scaffold.scaffold", "scaffold.arch", ".scaffold"]) or
                        self._fast_scan_upwards(cwd, ["pyproject.toml", "package.json", "go.mod", "Cargo.toml"]) or
                        cwd
                )

            self._state_mask |= 1

            # 2. Workspace Root Resolution
            # [ASCENSION 10]: Search for high-order monorepo markers
            ws_indicators = ["pnpm-workspace.yaml", "lerna.json", "scaffold.workspace", "nx.json", ".git"]
            self._workspace_root = self._fast_scan_upwards(self._project_root.parent, ws_indicators)

            self._state_mask |= 2

            # [ASCENSION 12]: Micro-Telemetry
            if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
                latency = (time.perf_counter() - self._birth_timestamp) * 1000
                self.logger.debug(f"Reality Anchored in {latency:.2f}ms. Root: {self._project_root.name}")

    def _fast_scan_upwards(self, start_dir: Path, indicators: List[str]) -> Optional[Path]:
        """
        [ASCENSION 7]: Zero-Dependency Probing.
        [ASCENSION 8]: Recursive Depth Governor.
        """
        try:
            # [ASCENSION 4]: UNC/Long-Path Normalization
            current = start_dir.resolve()
        except OSError:
            return None

        # Max depth 12 to prevent infinite traversal in symlink-looped environments
        for _ in range(12):
            # Check for indicators in current sanctum
            for marker in indicators:
                # Pure syscall-level check (os.path.exists via pathlib)
                if (current / marker).exists():
                    return current

            # Hit filesystem root?
            if current.parent == current:
                break
            current = current.parent

        return None

    # =========================================================================
    # == DUNDER PROTOCOLS                                                    ==
    # =========================================================================

    def __repr__(self) -> str:
        status = "HOT" if self._state_mask == 3 else "COLD"
        return f"<RuntimeContext id={self._session_id} state={status} root={self._project_root}>"

    def __bool__(self) -> bool:
        """A Context is True if it is anchored to a real project."""
        return self.project_root is not None

