# Path: scaffold/artisans/undo/artisan.py
# ---------------------------------------

import json
import shutil
from pathlib import Path
from typing import List, Optional

from rich.prompt import Confirm

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import UndoRequest  # <-- The new, specific vessel
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe
from ...core.state.contracts import LedgerEntry
from ...creator.io_controller.trash import TrashManager
from ...core.sanitization.ghost_buster import GhostBuster
from ..history.contracts import RiteGnosis  # <-- We now speak the language of the Historian
from .reverser import TemporalReverser

Logger = Scribe("Chronomancer")


class UndoArtisan(BaseArtisan[UndoRequest]):
    """
    =================================================================================
    == THE CHRONOMANCER (V-Ω-MULTI-RITE-REVERSAL-ENGINE)                           ==
    =================================================================================
    LIF: ∞ (THE MASTER OF THE TIMELINE)

    The ascended High Priest of Reversal. It is now a true Time Lord, capable of
    unwinding multiple strands of causality in a single, atomic symphony.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The N-Step Gaze:** Perceives the `steps` argument to understand the depth of
        the requested reversal (`undo 3`).
    2.  **The Chronicle Reader:** Summons the `_load_chronicle_timeline`, a divine rite to
        read the complete history of the cosmos from `.scaffold/chronicles/`.
    3.  **The Multi-Rite Symphony:** Its core logic is now a grand loop, conducting the
        reversal of multiple transactions in the correct, causally pure order (newest first).
    4.  **The Deep Time Rewind:** Its `_revert_lockfile_state` Gaze is now one of profound
        wisdom. It can find the exact state of reality from *before* the entire sequence
        of reversed rites.
    5.  **The Luminous Prophecy:** Before acting, it proclaims a detailed dossier of the
        rites it is about to annihilate from the timeline, awaiting the Architect's final vow.
    6.  **The Resilience Ward:** Gracefully handles missing ledgers within a multi-step
        reversal, warning the Architect but continuing the rite if `--force` is spoken.
    7.  **The Pure Delegation:** It remains a pure conductor, delegating all physical
        reversal to the `TemporalReverser`.
    8.  **The Final Exorcism:** The `GhostBuster` is summoned only once, at the very end
        of the multi-rite symphony, for maximum efficiency and purity.
    9.  **The Unbreakable Contract:** It speaks the new, pure `UndoRequest` contract.
    10. **The Atomic Heart:** The entire multi-step reversal is conceptually atomic. If
        one step fails without `--force`, the symphony halts.
    11. **The Silent Guardian:** Fully honors `--non-interactive` and `--force` vows for
        use in automated realities.
    12. **The Luminous Dossier:** Its final proclamation is a rich `ScaffoldResult`,
        chronicling the full extent of the temporal shift.
    """

    def execute(self, request: UndoRequest) -> ScaffoldResult:
        self.console.rule("[bold magenta]The Rite of Multi-Step Temporal Reversal[/bold magenta]")

        project_root = request.project_root or self.project_root
        trash_manager = TrashManager(project_root)

        # --- MOVEMENT I: THE GAZE UPON THE TIMELINE ---
        timeline = self._load_chronicle_timeline(project_root)
        if not timeline:
            return self.failure("The Gnostic Chronicle is a void. Time travel is impossible.")

        steps_to_reverse = request.steps
        if steps_to_reverse > len(timeline):
            return self.failure(
                f"Cannot reverse {steps_to_reverse} steps; only {len(timeline)} rites exist in the chronicle.")

        rites_to_undo = timeline[:steps_to_reverse]
        if not rites_to_undo:
            return self.success("No rites to undo.")

        # --- MOVEMENT II: THE LUMINOUS PROPHECY ---
        scribe = self.engine.registry.get(HistoryRequest)(self.engine).scribe
        self.console.print(Panel(
            f"The Chronomancer will reverse the following [bold red]{len(rites_to_undo)}[/bold red] rite(s):",
            title="[yellow]Prophecy of Reversal[/yellow]", border_style="yellow"
        ))
        scribe.proclaim_timeline(rites_to_undo)

        if not request.force and not request.non_interactive:
            if not Confirm.ask("\n[bold question]Is this your will?[/bold question]", default=False):
                return self.success("The Rite of Reversal was stayed by the Architect.")

        # --- MOVEMENT III: THE REVERSAL SYMPHONY ---
        reverser = TemporalReverser(trash_manager, project_root)
        total_success = 0
        total_failures = 0
        all_artifacts: List[Artifact] = []

        with self.console.status(f"[bold yellow]Reversing {len(rites_to_undo)} rite(s)...[/bold yellow]") as status:
            for i, rite in enumerate(rites_to_undo):
                status.update(
                    f"[bold yellow]Reversing '{rite.rite_name}' ({i + 1}/{len(rites_to_undo)})...[/bold yellow]")

                ledger = trash_manager.read_ledger(rite.rite_id)
                if not ledger:
                    msg = f"No Gnostic Ledger found for transaction {rite.rite_id[:8]} ('{rite.rite_name}')."
                    if not request.force:
                        raise ArtisanHeresy(msg,
                                            suggestion="This rite may be too ancient to undo. Use --force to skip.")
                    self.logger.warn(f"{msg} Skipping.")
                    continue

                # Reverse all entries for this specific rite
                for entry in reversed(ledger):
                    if not entry.inverse_action:
                        continue
                    try:
                        artifact = reverser.reverse(entry.inverse_action)
                        if artifact: all_artifacts.append(artifact)
                        total_success += 1
                    except Exception as e:
                        self.logger.error(f"Reversal failed for op {entry.operation} in rite {rite.rite_id[:8]}: {e}")
                        total_failures += 1
                        if not request.force:
                            raise ArtisanHeresy("The Timeline Fractured. The symphony is halted.", child_heresy=e)

        # --- MOVEMENT IV: THE FINAL EXORCISM & CHRONICLE REWIND ---
        self.logger.info("The symphony of reversal is complete. Summoning the final artisans...")

        ghost_buster = GhostBuster(project_root, protected_paths={project_root / ".scaffold", project_root / ".git"})
        purged = ghost_buster.exorcise()

        self._revert_lockfile_state(project_root, len(rites_to_undo))

        return self.success(
            f"Undo Complete. Reverted {len(rites_to_undo)} rite(s).",
            data={
                "operations_reversed": total_success,
                "failures": total_failures,
                "ghosts_busted": purged,
                "rites_reversed": [r.rite_id for r in rites_to_undo]
            },
            artifacts=all_artifacts
        )

    def _load_chronicle_timeline(self, project_root: Path) -> List[RiteGnosis]:
        """Performs a Gaze upon the full history to build a timeline of reversible rites."""
        chronicles_dir = project_root / ".scaffold" / "chronicles"
        if not chronicles_dir.exists():
            return []

        history = []
        # We also include the current lockfile as HEAD (the most recent state)
        all_locks = list(chronicles_dir.glob("*.lock")) + [project_root / "scaffold.lock"]

        processed_ids = set()
        for f in all_locks:
            if not f.exists(): continue
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                rite_id = data.get("provenance", {}).get("rite_id")
                if rite_id and rite_id not in processed_ids:
                    history.append(RiteGnosis.from_dict(data, f.name))
                    processed_ids.add(rite_id)
            except Exception:
                continue  # Skip corrupted chronicles

        # We must return a list of rites that *can* be undone, which are all but the current state.
        # So we sort by timestamp, newest first, and skip the first one (which is HEAD).
        sorted_history = sorted(history, key=lambda x: x.timestamp, reverse=True)
        return sorted_history[1:]

    def _revert_lockfile_state(self, root: Path, steps_reversed: int):
        """Restores the scaffold.lock to the state from N steps ago."""
        chronicles_dir = root / ".scaffold" / "chronicles"
        target_lock = root / "scaffold.lock"

        if not chronicles_dir.exists():
            return

        archives = sorted(chronicles_dir.glob("*.lock"), key=lambda f: f.stat().st_mtime, reverse=True)

        # The Nth most recent chronicle is the state we want to restore to.
        if len(archives) >= steps_reversed:
            target_state_file = archives[steps_reversed - 1]
            shutil.copy2(target_state_file, target_lock)
            self.logger.success(f"Gnostic Chronicle reverted to state from: [dim]{target_state_file.name}[/dim]")
        else:
            # We've undone all of history. The lockfile should be a void.
            if target_lock.exists():
                target_lock.unlink()
            self.logger.success("The Gnostic Chronicle has been returned to the void of Genesis.")