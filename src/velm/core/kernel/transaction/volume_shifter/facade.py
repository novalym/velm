# Path: src/velm/core/kernel/transaction/volume_shifter/facade.py
# ---------------------------------------------------------------
# LIF: INFINITY // ROLE: ATOMIC_DIRECTORY_SWAP_MANAGER
# AUTH: Ω_SHIFTER_V3500_GEOMETRIC_ISOLATION_FINALIS
# ---------------------------------------------------------------

import time
import shutil
import os
import threading
from pathlib import Path
from typing import Optional, Any, Dict

from .contracts import VolumeState, FlipStrategy
from .shadow_forge import ShadowForge
from .shifter import KineticShifter
from .....contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from .....logger import Scribe

Logger = Scribe("VolumeShifter")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class VolumeShifter:
    """
    Orchestrates the Blue-Green materialization sequence for the filesystem.

    This class is responsible for ensuring that physical reality is only updated
    when the newly forged project structure is completely verified. It achieves this
    through a strict state machine and an atomic directory swap (The Flip).

    Key Capabilities:
    1.  Geometric Isolation: Decouples the internal `.scaffold/volumes` directory
        from the target mutation zone, preventing recursive mirroring loops.
    2.  Surgical Sub-Volume Flipping: Allows isolated atomic updates to specific
        subdirectories within a project rather than replacing the entire root.
    3.  Robust Cleanup: Implements exponential backoff for directory deletion to
        handle transient OS-level file locks (Windows Search/Defender).
    4.  Dynamic Strategy Resolution: Gracefully degrades from atomic RENAME
        to recursive COPY operations based on cross-device boundary constraints.
    5.  Thread-Safe Mutex Envelopment: Shields critical I/O operations with RLock.
    """

    def __init__(self, project_root: Path, tx_id: str, base_path: Optional[Path] = None):
        """
        Initializes the Volume Shifter and maps the required spatial geometries.
        """
        self.root = project_root.resolve()
        self.tx_id = tx_id

        # Thread-Safety Shield for multi-threaded worker pools
        self._lock = threading.RLock()

        # Establish the absolute boundary for internal metadata to prevent corruption
        self.base_path = (base_path or project_root).resolve()

        # The Triple-Strata Geometry for Blue-Green Deployments
        self.sanctum = self.base_path / ".scaffold" / "volumes" / self.tx_id
        self.shadow_root = self.sanctum / "green"
        self.legacy_root = self.sanctum / "blue_old"

        self.forge = ShadowForge()

        # Bind the underlying file operation handler to the target root
        self.kinetic = KineticShifter(self.root)

        self.state = VolumeState.VOID
        self.force = False
        self._flip_latency_ms: float = 0.0

    def _sys_log(self, msg: str, color: str = "36"):
        """Internal tracing for I/O diagnostics."""
        if _DEBUG_MODE:
            import sys
            sys.stderr.write(f"\x1b[{color};1m[DEBUG: VolumeShifter]\x1b[0m {msg}\n")
            sys.stderr.flush()

    def prepare(self, strategy: FlipStrategy = FlipStrategy.RENAME):
        """
        Phase 1: Shadow Forging.

        Clones the existing directory structure into the isolated 'green' staging volume.
        This provides the baseline upon which the current transaction will apply its modifications.
        """
        with self._lock:
            if self.state in (VolumeState.RESONANT, VolumeState.FORGING):
                self._sys_log(f"[{self.tx_id[:8]}] Shadow Volume already prepared or forging. Bypassing.")
                return

            self.state = VolumeState.FORGING

            try:
                self.sanctum.mkdir(parents=True, exist_ok=True)

                # Delegate physical cloning to the Forge
                self.forge.materialize(self.root, self.shadow_root)

                self.state = VolumeState.RESONANT
                self._sys_log(f"[{self.tx_id[:8]}] Shadow Volume Prepared [RESONANT].")

            except Exception as e:
                self.state = VolumeState.FRACTURED
                Logger.error(f"[{self.tx_id[:8]}] Shadow Forge Initialization Failed: {e}")
                raise ArtisanHeresy(
                    f"Volumetric Shadow Forge Failed: {e}",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Target: {self.shadow_root}",
                    child_heresy=e
                )

    def flip(self, target_dir: Optional[Path] = None, strategy: FlipStrategy = FlipStrategy.RENAME):
        """
        Phase 2: The Atomic Swap (The Flip).

        Performs the microsecond pointer-swap that replaces the live 'blue' environment
        with the newly finalized 'green' shadow volume.
        """
        with self._lock:
            if self.state != VolumeState.RESONANT:
                raise RuntimeError(
                    f"Cannot perform Directory Swap. Volume state is {self.state.name}, expected RESONANT.")

            # Synchronize override flags to the physical layer
            self.kinetic.force = getattr(self, 'force', False)

            # Support surgical replacement of subdirectories
            active_target = target_dir or self.root
            self.state = VolumeState.FLIPPING

            start_time = time.perf_counter()

            try:
                # Calculate relative offset to locate the correct staging payload
                try:
                    rel_path = active_target.relative_to(self.root)
                    source_in_shadow = self.shadow_root / rel_path
                except ValueError:
                    # Target matches root directly
                    source_in_shadow = self.shadow_root

                # Execute the OS-level directory manipulation
                if strategy == FlipStrategy.SYMLINK:
                    self.kinetic.perform_symlink_flip(active_target, source_in_shadow, self.legacy_root)
                else:
                    self.kinetic.perform_rename_flip(active_target, source_in_shadow, self.legacy_root, self.tx_id)

                self.state = VolumeState.ACTIVE

                self._flip_latency_ms = (time.perf_counter() - start_time) * 1000
                Logger.success(f"Atomic Directory Swap complete in {self._flip_latency_ms:.2f}ms.")

            except Exception as failure:
                self.state = VolumeState.FRACTURED
                Logger.critical(f"Atomic Directory Swap Failed: {failure}")
                raise failure

    def cleanup(self):
        """
        Phase 3: Teardown and Rollback Preservation.

        Removes temporary volumes. If the transaction failed, the original data
        (blue_old) is preserved to allow manual recovery or forensic analysis.
        """
        with self._lock:
            if not self.sanctum.exists():
                return

            try:
                # Always remove the 'green' (Shadow) volume as it represents uncommitted state
                if self.shadow_root.exists():
                    self._robust_rmtree(self.shadow_root)

                if self.state == VolumeState.ACTIVE:
                    # Success Path: The previous reality is obsolete, clean up the entire volume cache
                    self._robust_rmtree(self.sanctum)
                    self.state = VolumeState.VOID
                    self._sys_log(f"[{self.tx_id[:8]}] Transactional shards purified.")

                elif self.state == HeresySeverity.CRITICAL or self.state == VolumeState.FRACTURED:
                    # Failure Path: Preserve the legacy volume ('blue_old') for recovery
                    Logger.warn(
                        f"[{self.tx_id[:8]}] Rollback execution halted. "
                        f"Original state preserved in [cyan]{self.legacy_root.relative_to(self.root)}[/cyan]"
                    )

                    # Only purge the root container if blue_old is already empty
                    if not any(self.legacy_root.iterdir()) if self.legacy_root.exists() else True:
                        self._robust_rmtree(self.sanctum)
                        self.state = VolumeState.VOID
                else:
                    # Passive/Incomplete state: Clean everything
                    self._robust_rmtree(self.sanctum)
                    self.state = VolumeState.VOID

            except Exception as e:
                self._sys_log(f"Cleanup encountered friction: {e}", "33")

    def _robust_rmtree(self, path: Path):
        """
        Bypasses 'Directory not empty' OS-level locking errors during heavy I/O cleanup
        by applying an exponential backoff retry loop. Essential for Windows stability.
        """
        if not path.exists():
            return

        for attempt in range(5):
            try:
                shutil.rmtree(path, ignore_errors=False)
                break
            except Exception:
                time.sleep(0.15 * (attempt + 1))
        else:
            # Final attempt silently ignores errors to prevent crashing the orchestrator
            shutil.rmtree(path, ignore_errors=True)

    def __repr__(self):
        return f"<VolumeShifter state={self.state.name} tx={self.tx_id[:8]}>"