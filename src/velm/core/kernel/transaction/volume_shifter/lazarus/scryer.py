# Path: src/velm/core/kernel/transaction/volume_shifter/lazarus/scryer.py
# -----------------------------------------------------------------------

import json
import os
import time
from pathlib import Path
from typing import List, Optional

from ......logger import Scribe
from .contracts import RecoveryPlan, OrphanState

Logger = Scribe("Lazarus:Scryer")


class LazarusScryer:
    """
    =================================================================================
    == THE NECROMANTIC SCRIER (V-Ω-FORENSIC-DIVINATION)                            ==
    =================================================================================
    LIF: 10,000x | ROLE: TEMPORAL_DETECTIVE | RANK: OMEGA_GUARDIAN

    This artisan possesses the 'Gaze of the Afterlife'. It scans the `.scaffold/volumes`
    and `.scaffold/commit.journal` to identify realities that were shattered mid-flip.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.volumes_dir = self.root / ".scaffold" / "volumes"
        self.journal_path = self.root / ".scaffold" / "commit.journal"

    def divine_recovery_plans(self) -> List[RecoveryPlan]:
        """
        Conducts a panoptic scan of all temporal debris and formulates exact
        mathematical plans for their restoration.
        """
        plans: List[RecoveryPlan] = []

        # --- MOVEMENT I: THE JOURNAL INQUEST ---
        journal_plan = self._scry_journal()
        if journal_plan:
            plans.append(journal_plan)

        # --- MOVEMENT II: THE VOLUME CENSUS ---
        if self.volumes_dir.exists() and self.volumes_dir.is_dir():
            for tx_dir in self.volumes_dir.iterdir():
                if tx_dir.is_dir():
                    plan = self._scry_transaction_volume(tx_dir)
                    if plan and plan.is_executable:
                        # Deduplicate against journal to prevent double-resurrection
                        if not any(p.tx_id == plan.tx_id for p in plans):
                            plans.append(plan)

        return plans

    def _scry_journal(self) -> Optional[RecoveryPlan]:
        """
        [ASCENSION 4]: The Journal Decryptor.
        Reads the `commit.journal` WAL (Write-Ahead Log) to find aborted flips.
        """
        if not self.journal_path.exists():
            return None

        try:
            data = json.loads(self.journal_path.read_text(encoding='utf-8'))
            tx_id = data.get("tx_id", "unknown_journal_tx")
            manifest = data.get("manifest", {})

            # If the journal exists, it means the Committer died during the physical move.
            plan = RecoveryPlan(
                tx_id=tx_id,
                state=OrphanState.JOURNAL_DEADLOCK,
                volume_dir=self.journal_path.parent,
                timestamp=data.get("timestamp", time.time())
            )

            # The manifest maps src (staging) -> dst (reality).
            # To recover, we just need to ensure dst got what it needed, but standard
            # Lazarus focuses on undoing the damage. If a journal exists, the move
            # was in progress. The safest bet is to execute the original journal intent
            # (Roll-forward recovery).
            for src_str, dst_str in manifest.items():
                plan.resurrection_targets.append({
                    "source": Path(src_str),
                    "destination": Path(dst_str)
                })

            return plan
        except Exception as e:
            Logger.warn(f"Journal Divination Fractured: {e}. The WAL is unreadable.")
            return None

    def _scry_transaction_volume(self, tx_dir: Path) -> Optional[RecoveryPlan]:
        """
        [ASCENSION 7]: The Legacy Biopsy.
        Examines a specific `.scaffold/volumes/<tx_id>` directory.
        """
        tx_id = tx_dir.name
        blue_old = tx_dir / "blue_old"
        green_shadow = tx_dir / "green"

        # CASE A: STRANDED LEGACY (The most critical failure)
        # The flip started, original files were moved to blue_old, but it crashed before
        # green was fully moved into place or before cleanup happened.
        if blue_old.exists() and any(blue_old.iterdir()):
            plan = RecoveryPlan(
                tx_id=tx_id,
                state=OrphanState.BLUE_OLD_STRANDED,
                volume_dir=tx_dir,
                timestamp=tx_dir.stat().st_mtime
            )

            # Map every root-level shard in blue_old back to its rightful place in the project root
            for shard in blue_old.iterdir():
                plan.resurrection_targets.append({
                    "source": shard,
                    "destination": self.root / shard.name
                })

            return plan

        # CASE B: ABANDONED SHADOW (Harmless but wasteful)
        # The shadow volume was forged, but the flip never initiated.
        if green_shadow.exists() and any(green_shadow.iterdir()):
            return RecoveryPlan(
                tx_id=tx_id,
                state=OrphanState.GREEN_ABANDONED,
                volume_dir=tx_dir,
                timestamp=tx_dir.stat().st_mtime,
                is_executable=False  # Abandoned shadows just need deletion, not restoration
            )

        return None