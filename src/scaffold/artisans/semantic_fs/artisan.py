# Path: scaffold/artisans/semantic_fs/artisan.py
# ----------------------------------------------


import os
import sys
from pathlib import Path
import threading
import time

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import MountRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy

# --- THE DIVINE SUMMONS (WITH THE GNOSTIC WARD) ---
# We perform a controlled, Gnostic Gaze for the FUSE artisan.
try:
    from fuse import FUSE
    from .operations import GnosticOperations

    FUSE_AVAILABLE = True
except ImportError:
    FUSE_AVAILABLE = False
    FUSE = object
    GnosticOperations = object


@register_artisan("mount")
class SemanticMountArtisan(BaseArtisan[MountRequest]):
    """
    =============================================================================
    == THE REALITY BINDER (V-Ω-FUSE-MOUNT-POLYGLOT)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Mounts the Gnostic Cortex's memory as a virtual filesystem.
    This artisan is now a Polyglot of Realms, understanding the Gnostic schism
    between POSIX and Windows realities and providing a path to unification.
    """

    def _check_winfsp_bridge(self) -> bool:
        """
        [THE GAZE FOR THE GNOSTIC BRIDGE]
        On Windows, this rite gazes into the system's soul to see if the
        WinFsp bridge has been forged.
        """
        if sys.platform != "win32":
            return True  # Not needed on non-windows

        system32 = Path(os.environ.get("SystemRoot", "C:\\Windows")) / "System32"
        # Check for the core DLL of WinFsp
        return (system32 / "winfsp-x64.dll").exists() or (system32 / "winfsp-x86.dll").exists()

    def execute(self, request: MountRequest) -> ScaffoldResult:
        # --- THE GNOSTIC TRIAGE OF REALMS ---
        if sys.platform == "win32" and not self._check_winfsp_bridge():
            raise ArtisanHeresy(
                "Windows Heresy: The Gnostic Bridge (WinFsp) is not manifest.",
                suggestion="To mount filesystems on Windows, you must first install WinFsp. See https://winfsp.dev/rel/"
            )

        if not FUSE_AVAILABLE:
            # This heresy is now proclaimed only after we've confirmed the environment is not the issue.
            return self.failure(
                "The 'fusepy' artisan is required for mounting.",
                suggestion="Speak the sacred plea: `pip install fusepy`"
            )

        mount_point = Path(request.mount_point).resolve()

        if not mount_point.exists():
            mount_point.mkdir(parents=True, exist_ok=True)

        if not mount_point.is_dir():
            return self.failure(f"Mount point '{mount_point}' is not a directory.")

        if any(mount_point.iterdir()):
            self.logger.warn(f"The mount sanctum '{mount_point.name}' is not empty. Its contents will be obscured.")

        self.logger.info(f"Mounting the Gnostic Cortex at [cyan]{mount_point}[/cyan]...")
        self.console.print("[dim]Press Ctrl+C to unmount and return to the mortal realm.[/dim]")

        # We must initialize the Cortex if it hasn't been already
        if not self.engine.cortex:
            from ...core.cortex.engine import GnosticCortex
            self.engine.cortex = GnosticCortex(self.project_root)

        # Ensure the cortex has perceived reality
        self.engine.cortex.perceive()

        try:
            # FUSE runs in the foreground by default
            FUSE(GnosticOperations(self.engine.cortex), str(mount_point), foreground=True, allow_other=False)
        except Exception as e:
            # Check for a common Windows heresy
            if "WinFsp-FUSE cannot be loaded" in str(e):
                raise ArtisanHeresy(
                    "The WinFsp Bridge is present, but `fusepy` cannot commune with it.",
                    suggestion="Ensure you have installed `fusepy` in the same Python environment AFTER installing WinFsp.",
                    child_heresy=e
                )
            raise ArtisanHeresy(f"Failed to mount Gnostic Filesystem: {e}", child_heresy=e)

        return self.success("Gnostic Filesystem unmounted.")