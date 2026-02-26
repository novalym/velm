# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/engine.py
# ----------------------------------------------------------------------------

import os
import sys
import time
import gc
import shutil
from pathlib import Path
from typing import Dict, Any

from ......logger import Scribe
from ......utils import get_human_readable_size
from ......contracts.heresy_contracts import ArtisanHeresy

from .contracts import ForgeMetrics
from .replicator import AtomicReplicator
from .strategies import KineticStrategies

Logger = Scribe("VolumeShifter:Forge")


class ShadowForge:
    """
    =================================================================================
    == THE OMEGA SHADOW FORGE (V-Ω-TOTALITY-V64-DECAPITATED)                       ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_REPLICATOR_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME

    The unified facade for the hyper-modular Shadow Forge Sanctum.
    It orchestrates the Sieve, the Replicator, and the Substrate Strategies to
    forge a perfect, non-destructive clone of Reality in nanoseconds.
    =================================================================================
    """

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self.Logger = Logger
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.is_windows = os.name == 'nt'

    def materialize(self, source: Path, destination: Path) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF HOLOGRAPHIC PROJECTION                                      ==
        =============================================================================
        Clones the universe from Source to Destination with absolute verification.
        """
        metrics = ForgeMetrics()

        # [ASCENSION 14]: The Zombie Handle Exorcist
        gc.collect(2)

        if not source.exists():
            destination.mkdir(parents=True, exist_ok=True)
            return metrics.snapshot()

        self.Logger.verbose(f"Forge: Materializing Shadow Volume at [dim]{destination.name}[/dim]")
        start_ns = time.perf_counter_ns()

        try:
            # --- MOVEMENT I: PRE-FLIGHT GEOMETRY ---
            src_abs = source.resolve()
            dst_abs = destination.resolve()

            if self.is_windows:
                src_abs = Path(self._win_long_path(str(src_abs)))
                dst_abs = Path(self._win_long_path(str(dst_abs)))

            # The Shadow Lock
            if dst_abs.exists():
                shutil.rmtree(str(dst_abs), ignore_errors=True)
            dst_abs.mkdir(parents=True, exist_ok=True)

            # --- MOVEMENT II: CROSS-DEVICE SUTURE ---
            cross_device = False
            try:
                cross_device = (src_abs.stat().st_dev != dst_abs.stat().st_dev)
            except OSError:
                cross_device = True  # Assume worst case

            if cross_device:
                self.Logger.verbose("Cross-Device Boundary Detected. Hardlinks disabled. Engaging Block Copy.")

            # Materialize the Substrate-Aware Replicator
            replicator = AtomicReplicator(self.Logger, metrics, cross_device)

            # --- MOVEMENT III: THE KINETIC WALK ---
            if self.is_wasm:
                self.Logger.verbose("Substrate: ETHER. Engaging Sequential Flow.")
                KineticStrategies.ether_flow(src_abs, dst_abs, replicator, metrics, self.Logger)
            else:
                self.Logger.verbose("Substrate: IRON. Engaging Parallel Hurricane.")
                KineticStrategies.iron_hurricane(src_abs, dst_abs, replicator, metrics, self.Logger)

            # --- MOVEMENT IV: INTEGRITY & FINALITY ---
            self._verify_integrity_sample(dst_abs)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            final_stats = metrics.snapshot()

            self.Logger.debug(
                f"Shadow forged in {duration_ms:.2f}ms. "
                f"Links: {final_stats['hardlinks']} | Copies: {final_stats['copies']} | "
                f"Mass: {get_human_readable_size(final_stats['bytes'])}"
            )

            if final_stats["errors"] > 0:
                self.Logger.warn(f"Shadow Forge encountered {final_stats['errors']} non-fatal fractures.")

            return final_stats

        except Exception as e:
            self.Logger.error(f"Forge Fracture: {e}")
            raise e

    def _verify_integrity_sample(self, root: Path):
        """[ASCENSION 19]: Paranoid Sampling."""
        count = 0
        for f in root.rglob('*'):
            if f.is_file():
                if f.stat().st_size == 0:
                    if not f.exists():
                        self.Logger.error(f"Ghost File Detected: {f}")
                count += 1
                if count > 5: break

    def _win_long_path(self, path: str) -> str:
        """[ASCENSION 9]: Windows Long Path Prefix."""
        if self.is_windows and len(path) > 240 and not path.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(path)
        return path


