# Path: src/velm/core/kernel/transaction/volume_shifter/lazarus/engine.py
# -----------------------------------------------------------------------

import os
import sys
import shutil
from pathlib import Path

from ......logger import Scribe
from .scryer import LazarusScryer
from .resurrector import Resurrector
from .contracts import OrphanState

Logger = Scribe("VolumeShifter:Lazarus")


class LazarusRecovery:
    """
    =============================================================================
    == THE LAZARUS PROTOCOL (V-Ω-TOTALITY-V64-RESURRECTION-ENGINE)             ==
    =============================================================================
    LIF: ∞ | ROLE: SUPREME_SYSTEM_HEALER | RANK: OMEGA_PRIME

    The unified entry point for autonomic crash recovery. It evaluates the physical
    substrate, summons the Scryer to find temporal fractures, and unleashes the
    Resurrector to stitch reality back together.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Substrate Sensing:** Detects WASM environments and stays the hand, as
        persistent volume crashes are impossible in pure memory architectures.
    2.  **Zero-Latency Boot Hook:** Optimized to complete in < 5ms if the
        sanctum is pure, ensuring no metabolic tax on standard Engine boots.
    3.  **Abandoned Shadow Annihilation:** Automatically garbage-collects
        `green` volumes that failed to flip, reclaiming lost disk space.
    4.  **Bicameral Healing:** Perfectly handles both `commit.journal` forward-rolls
        and `blue_old` backward-rolls simultaneously.
    =============================================================================
    """

    @staticmethod
    def scry_and_heal(project_root: Path):
        """
        The Grand Rite of Resurrection.
        Usually invoked during Engine Bootstrap.
        """
        # 1. SUBSTRATE WARD
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        if is_wasm: return

        # 2. THE FAST PATH (ZERO-LATENCY)
        volumes_dir = project_root / ".scaffold" / "volumes"
        journal_path = project_root / ".scaffold" / "commit.journal"

        # If no debris exists, reality is pure. Exit immediately.
        if not volumes_dir.exists() and not journal_path.exists():
            return

        Logger.verbose("Lazarus Protocol active. Scrying for fractured realities...")

        # 3. SUMMON THE SPECIALISTS
        scryer = LazarusScryer(project_root)
        resurrector = Resurrector(is_windows=(os.name == 'nt'), is_wasm=False)

        # 4. CONDUCT THE INQUEST
        plans = scryer.divine_recovery_plans()

        if not plans:
            # Clean up empty volume root just in case
            if volumes_dir.exists() and not any(volumes_dir.iterdir()):
                try:
                    volumes_dir.rmdir()
                except OSError:
                    pass
            return

        # 5. EXECUTE THE HEALING
        for plan in plans:
            if plan.is_executable:
                resurrector.execute_plan(plan)
            elif plan.state == OrphanState.GREEN_ABANDONED:
                # Autonomous Garbage Collection for abandoned shadows
                Logger.verbose(f"[{plan.tx_id[:8]}] Evaporating abandoned Shadow Volume.")
                shutil.rmtree(plan.volume_dir, ignore_errors=True)