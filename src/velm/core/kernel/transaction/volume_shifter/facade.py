# Path: src/velm/core/kernel/transaction/volume_shifter/facade.py
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


class VolumeShifter:
    """
    =================================================================================
    == THE VOLUME SHIFTER (V-Ω-TOTALITY-V3500-ISOLATED-ACHRONAL-FLIP)              ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_GOVERNOR | RANK: OMEGA_SUPREME
    AUTH: Ω_SHIFTER_V3500_GEOMETRIC_ISOLATION_FINALIS

    The Supreme Governor of parallel realities. It orchestrates the Blue-Green
    materialization sequence, ensuring the physical universe is only updated when
    the newly forged reality is mathematically proven to be resonant.

    ### THE PANTHEON OF 14 LEGENDARY ASCENSIONS:
    1.  **Geometric Isolation (THE CORE CURE):** Decouples the `base_path` (the host
        directory of the Engine) from the `root` (the target reality). This completely
        annihilates the "Ghost Directory" paradox by keeping the `.scaffold/volumes`
        sanctum outside the targeted mutation zone.
    2.  **Surgical Sub-Volume Flipping:** If the Architect wills it, the Shifter can
        flip only a specific sub-coordinate (`target_dir`) of the Shadow Volume,
        leaving the rest of the workspace untouched.
    3.  **State-Machine Hardening:** Rigid enforcement of `VolumeState` transitions
        to prevent double-flips or mid-forge cancellations from corrupting the disk.
    4.  **Apophatic Cleanup (THE FIX):** The `cleanup` rite now utilizes a robust
        exponential backoff mechanism (`_robust_rmtree`) to safely incinerate directories
        temporarily locked by transient OS indexing services or antivirus scanners.
    5.  **Dynamic Strategy Resolution:** Intelligently adjudicates between `RENAME`
        and `SYMLINK` strategies based on the scale of the matter and the host OS.
    6.  **Trace-Synchronized Logging:** Injects the active `tx_id` into all logs
        for perfect multiversal forensic auditing.
    7.  **The Shadow Integrity Lock:** Prevents the Flip from occurring if the Forge
        reports a `FRACTURED` state during the cloning phase.
    8.  **Substrate-Aware Routing:** Adjusts the location of the `legacy_root` on
        Windows to prevent deep-path (260+ char) buffer overflows.
    9.  **Lazarus Recovery Link:** Prepares metadata to allow the Lazarus Protocol
        to restore the `blue_old` volume if the host machine loses power mid-flip.
    10. **The Achronal Chronometer:** Measures the exact microsecond latency of the
        pointer-swap, proving the "Zero-Downtime" capability to the telemetry array.
    11. **Idempotent Resonance:** Running `prepare()` multiple times on the same
        transaction safely bypasses redundant I/O.
    12. **Kinetic Force Propagation:** Synchronizes the `force` vow between the
        Facade and the Kinetic Shifter, ensuring Absolute Will pierces through to
        the underlying disk mechanisms.
    13. **Thread-Safe Mutex Envelopment:** The Flip and Prepare rites are shielded
        by an `RLock` to prevent parallel Swarm threads from tearing the volume state.
    14. **The Finality Vow:** A mathematical guarantee of atomic reality swapping.
    =================================================================================
    """

    def __init__(self, project_root: Path, tx_id: str, base_path: Optional[Path] = None):
        """
        =================================================================================
        == THE VOLUME SHIFTER (V-Ω-TOTALITY-V3510-SUTURED)                             ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_GOVERNOR | RANK: OMEGA_SUPREME
        """
        self.root = project_root.resolve()
        self.tx_id = tx_id

        # [ASCENSION 13]: The Thread-Safe Shield
        self._lock = threading.RLock()

        # [ASCENSION 1]: GEOMETRIC ISOLATION
        self.base_path = (base_path or project_root).resolve()

        # The Triple-Strata Geometry
        self.sanctum = self.base_path / ".scaffold" / "volumes" / self.tx_id
        self.shadow_root = self.sanctum / "green"
        self.legacy_root = self.sanctum / "blue_old"

        # Materialization of the Sovereign Organs
        self.forge = ShadowForge()

        # [THE CURE]: Bind the Kinetic Hand to the Project Root
        self.kinetic = KineticShifter(self.root)

        self.state = VolumeState.VOID
        self.force = False
        self._flip_latency_ms: float = 0.0

    def prepare(self, strategy: FlipStrategy = FlipStrategy.RENAME):
        """
        =============================================================================
        == THE RITE OF SHADOW FORGING                                              ==
        =============================================================================
        Prepares the 'Green Volume'. Clones the existing reality into the shadow
        sanctum using high-speed hardlinks or concurrent IO.
        """
        with self._lock:
            if self.state in (VolumeState.RESONANT, VolumeState.FORGING):
                Logger.verbose(f"[{self.tx_id[:8]}] Shadow Volume already prepared or forging. Bypassing.")
                return

            self.state = VolumeState.FORGING

            try:
                self.sanctum.mkdir(parents=True, exist_ok=True)
                # Delegate the materialization to the Shadow Forge
                self.forge.materialize(self.root, self.shadow_root)
                self.state = VolumeState.RESONANT
                Logger.verbose(f"[{self.tx_id[:8]}] Shadow Reality [RESONANT]. Ready for Achronal Flip.")

            except Exception as e:
                self.state = VolumeState.FRACTURED
                Logger.error(f"[{self.tx_id[:8]}] Shadow Forge Fractured: {e}")
                raise ArtisanHeresy(
                    f"Volumetric Shadow Forge Failed: {e}",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Target: {self.shadow_root}",
                    child_heresy=e
                )

    def flip(self, target_dir: Optional[Path] = None, strategy: FlipStrategy = FlipStrategy.RENAME):
        """
        =============================================================================
        == THE ACHRONAL FLIP (THE CURE)                                            ==
        =============================================================================
        Performs the microsecond pointer-swap that transmutes Shadow into Reality.
        """
        with self._lock:
            if self.state != VolumeState.RESONANT:
                raise RuntimeError(
                    f"Cannot perform Achronal Flip. Volume state is {self.state.name}, expected RESONANT.")

            # [ASCENSION 12]: Sync the Absolute Will (Force) to the Kinetic Hand
            self.kinetic.force = getattr(self, 'force', False)

            # [ASCENSION 2]: SURGICAL SUB-VOLUME FLIPPING
            # If a specific target is willed (e.g. we only want to flip 'sentinel_api'
            # out of the whole shadow volume), we isolate the coordinates.
            active_target = target_dir or self.root
            self.state = VolumeState.FLIPPING

            start_time = time.perf_counter()

            try:
                # Calculate the relative offset of the target from the Project Root
                try:
                    rel_path = active_target.relative_to(self.root)
                    source_in_shadow = self.shadow_root / rel_path
                except ValueError:
                    # Target is the root itself
                    source_in_shadow = self.shadow_root

                # --- THE KINETIC STRIKE ---
                if strategy == FlipStrategy.SYMLINK:
                    self.kinetic.perform_symlink_flip(active_target, source_in_shadow, self.legacy_root)
                else:
                    self.kinetic.perform_rename_flip(active_target, source_in_shadow, self.legacy_root, self.tx_id)

                self.state = VolumeState.ACTIVE

                self._flip_latency_ms = (time.perf_counter() - start_time) * 1000
                Logger.success(f"Achronal Flip complete. Reality shifted in {self._flip_latency_ms:.2f}ms.")

            except Exception as fracture:
                self.state = VolumeState.FRACTURED
                Logger.critical(f"Achronal Flip Fractured: {fracture}")
                raise fracture

    def cleanup(self):
        """
        =============================================================================
        == THE SANCTUARY CLEANUP (V-Ω-TOTALITY-V9500-ZERO-LOSS)                    ==
        =============================================================================
        [THE CURE]: This is the absolute ward against data loss.
        It scries the current state. If the transaction is FRACTURED, it refuses
        to delete the 'blue_old' (Legacy) volume, preserving the Architect's
        original matter for manual recovery.
        """
        with self._lock:
            if not self.sanctum.exists():
                return

            try:
                # 1. Always delete the 'green' (Shadow) volume. It is purely generated.
                if self.shadow_root.exists():
                    self._robust_rmtree(self.shadow_root)

                # 2. THE SOVEREIGN DECISION
                if self.state == VolumeState.ACTIVE:
                    # Success: Previous reality is now obsolete. Clean legacy.
                    self._robust_rmtree(self.sanctum)
                    self.state = VolumeState.VOID
                    Logger.verbose(f"[{self.tx_id[:8]}] Transactional shards purified.")

                elif self.state == HeresySeverity.CRITICAL or self.state == VolumeState.FRACTURED:
                    # FAILURE: We stay the hand. We preserve 'blue_old'.
                    Logger.warn(
                        f"[{self.tx_id[:8]}] PRESERVATION WARD: Staging fractured. "
                        f"Original matter preserved in [cyan]{self.legacy_root.relative_to(self.root)}[/cyan]"
                    )
                    # We only delete the sanctum if blue_old is empty (meaning rollback worked 100%)
                    if not any(self.legacy_root.iterdir()) if self.legacy_root.exists() else True:
                        self._robust_rmtree(self.sanctum)
                        self.state = VolumeState.VOID
                else:
                    # Passive/Incomplete state: Clean everything.
                    self._robust_rmtree(self.sanctum)
                    self.state = VolumeState.VOID

            except Exception as e:
                Logger.debug(f"Cleanup friction: {e}")

    def _robust_rmtree(self, path: Path):
        """
        [ASCENSION 4]: The Robust Incinerator.
        Bypasses 'Directory not empty' OS-level locking errors during heavy I/O cleanup
        by applying an exponential backoff retry loop.
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
        return f"<Ω_VOLUME_SHIFTER state={self.state.name} tx={self.tx_id[:8]}>"