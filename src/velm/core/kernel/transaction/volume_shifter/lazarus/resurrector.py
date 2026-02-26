# Path: src/velm/core/kernel/transaction/volume_shifter/lazarus/resurrector.py
# ----------------------------------------------------------------------------

import shutil
import os
from pathlib import Path

from ......logger import Scribe
from ..shifter.robust_rename import AtomicRenamer
from .contracts import RecoveryPlan, OrphanState

Logger = Scribe("Lazarus:Resurrector")


class Resurrector:
    """
    =================================================================================
    == THE GRAND RESURRECTOR (V-Ω-TOTALITY-V64-ATOMIC-HEALER)                      ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_SURGEON | RANK: OMEGA_SOVEREIGN

    Executes the Recovery Plan with absolute atomicity. It utilizes the same
    `AtomicRenamer` used by the KineticShifter to guarantee that the healing
    process itself does not fall victim to OS locks.
    """

    def __init__(self, is_windows: bool, is_wasm: bool):
        self.renamer = AtomicRenamer(Logger, is_windows, is_wasm)

    def execute_plan(self, plan: RecoveryPlan) -> bool:
        """
        [THE RITE OF RESURRECTION]
        Transmutes the fragmented debris back into a cohesive reality.
        """
        Logger.warn(f"[{plan.tx_id[:8]}] Lazarus Protocol Engaged. Diagnosis: {plan.state.name}")

        success_count = 0
        total_targets = len(plan.resurrection_targets)

        try:
            # --- MOVEMENT I: THE ROLLBACK (BLUE_OLD) ---
            if plan.state == OrphanState.BLUE_OLD_STRANDED:
                for target in plan.resurrection_targets:
                    src: Path = target["source"]
                    dst: Path = target["destination"]

                    if not src.exists(): continue

                    # If the destination already has corrupted/partial matter, we must displace it
                    if dst.exists():
                        if dst.is_dir() and not dst.is_symlink():
                            shutil.rmtree(dst, ignore_errors=True)
                        else:
                            dst.unlink(missing_ok=True)

                    # Atomic restoration
                    self.renamer.robust_rename(src, dst)
                    success_count += 1
                    Logger.verbose(f"   -> Resurrected: {dst.name}")

            # --- MOVEMENT II: THE ROLL-FORWARD (JOURNAL) ---
            elif plan.state == OrphanState.JOURNAL_DEADLOCK:
                for target in plan.resurrection_targets:
                    src: Path = target["source"]
                    dst: Path = target["destination"]

                    if src.exists():
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        self.renamer.robust_rename(src, dst)
                        success_count += 1
                        Logger.verbose(f"   -> Enforced Journal Mandate: {dst.name}")

            # --- MOVEMENT III: PURGATION OF THE GRAVE ---
            # Once the souls have been returned, we incinerate the empty tomb.
            if plan.volume_dir.exists() and plan.state != OrphanState.JOURNAL_DEADLOCK:
                shutil.rmtree(plan.volume_dir, ignore_errors=True)

            # If it was a journal lock, delete the journal
            if plan.state == OrphanState.JOURNAL_DEADLOCK and plan.volume_dir.is_file():
                plan.volume_dir.unlink(missing_ok=True)

            Logger.success(f"[{plan.tx_id[:8]}] Reality Stabilized. {success_count}/{total_targets} shards healed.")
            return True

        except Exception as e:
            Logger.critical(f"[{plan.tx_id[:8]}] FATAL LAZARUS FRACTURE: The resurrection failed: {e}")
            return False
        finally:
            # Clean up any ghost files created by the AtomicRenamer during healing
            self.renamer.evaporate_ghosts()