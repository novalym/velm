# === [scaffold/artisans/translocate_core/conductor/execution.py] ===
import shutil
import os
from pathlib import Path
from typing import TYPE_CHECKING, Set, List

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.console import Group
from rich.traceback import Traceback
from rich.text import Text

from ....logger import get_console, Scribe
from ....contracts.data_contracts import InscriptionAction
from ....contracts.heresy_contracts import ArtisanHeresy
from ..resolvers import PythonImportResolver
from ....interfaces.base import ScaffoldResult, Artifact

if TYPE_CHECKING:
    from .engine import TranslocationConductor

Logger = Scribe("TranslocationExecution")


class ExecutionMixin:
    """
    =================================================================================
    == THE FACULTY OF EXECUTION (V-Ω-KINETIC-HAND-ULTIMA-INSTRUMENTED)             ==
    =================================================================================
    Handles the `conduct` rite.

    [INSTRUMENTED]: Now returns a ScaffoldResult for Gnostic Contract compliance.
    """

    def conduct(self: 'TranslocationConductor') -> ScaffoldResult:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC EVOLUTION (V-Ω-ANCESTRAL-GAZE-ASCENDED)           ==
        =================================================================================
        """
        console = get_console()
        artifacts: List[Artifact] = []  # [ASCENSION] Track manifest artifacts

        if not self.translocation_map or not self.translocation_map.moves:
            self.logger.info(
                "Guardian of the Void: The translocation plan is empty. The symphony is gracefully stayed.")
            return ScaffoldResult.forge_success("No translocation required.", data={"moved": 0})

        # [SELF-HEALING] Ensure StructureSentinel exists
        if not hasattr(self, 'structure_sentinel') or self.structure_sentinel is None:
            self.logger.warn("Structure Sentinel missing from Engine. Summoning it JIT...")
            from ....core.structure_sentinel import StructureSentinel
            tx = getattr(self, 'transaction', None)
            self.structure_sentinel = StructureSentinel(self.project_root, tx)

        # [[[ THE DIVINE HEALING: THE GAZE OF CONTAINMENT ]]]
        all_files_in_scope: Set[Path] = set()
        for origin in self.translocation_map.moves.keys():
            if origin.is_file():
                all_files_in_scope.add(origin)
            elif origin.is_dir():
                for file_gnosis in self.cortex._memory.inventory:
                    try:
                        if file_gnosis.path.resolve().is_relative_to(origin.resolve()):
                            all_files_in_scope.add(file_gnosis.path.resolve())
                    except ValueError:
                        if str(file_gnosis.path.resolve()).startswith(str(origin.resolve())):
                            all_files_in_scope.add(file_gnosis.path.resolve())

        self.logger.verbose(f"Gaze of Containment perceived {len(all_files_in_scope)} total scriptures in scope.")

        # --- MOVEMENT I: THE PROPHECY (THE COMMUNION WITH THE CORTEX) ---
        self.logger.info("Movement I: The Prophecy. Communing with the Gnostic Cortex...")
        self.all_healing_plans = self.cortex.prophesy_healing_plan(self.translocation_map.moves)
        self.logger.success("Cortex has spoken. The Prophecy of Healing is complete.")

        # --- THE GNOSTIC TRIAGE OF WILL ---
        if self.preview:
            non_python_files = [f for f in all_files_in_scope if f.suffix != '.py']
            self._proclaim_prophetic_dossier(self.all_healing_plans, non_python_files)
            return ScaffoldResult.forge_success("Prophecy Revealed (Dry Run).",
                                                data={"plan": str(self.all_healing_plans)})

        # --- THE PATH OF MANIFESTATION: THE CINEMATIC SYMPHONY ---
        console.rule("[bold magenta]The Grand Symphony of Gnostic Evolution Begins[/bold magenta]")

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                      TimeElapsedColumn(), console=console) as progress:
            try:
                # --- MOVEMENT II: THE VOW OF REASSURANCE (THE GNOSTIC SNAPSHOT) ---
                if self.backup_root_path:
                    backup_task = progress.add_task("[yellow]Movement II: Forging Gnostic Snapshot...",
                                                    total=len(self.translocation_map.moves))
                    snapshot_dir = self._forge_gnostic_snapshot(progress, backup_task)
                    progress.update(backup_task, completed=len(self.translocation_map.moves),
                                    description=f"[green]Snapshot forged at [cyan]'{snapshot_dir.name}'[/cyan].")

                # --- MOVEMENT III: THE TRANSLOCATION (THE FORGING OF THE 'AFTER') ---
                move_task = progress.add_task("[cyan]Movement III: Translocating scriptures...",
                                              total=len(self.translocation_map.moves))
                moved_origins = set()

                sorted_moves = sorted(self.translocation_map.moves.items(), key=lambda x: len(x[0].parts))

                for origin, dest in sorted_moves:
                    progress.update(move_task, advance=1, description=f"[cyan]Moving [red]'{origin.name}'[/red]...")

                    if not origin.exists():
                        Logger.warn(f"Cannot translocate a void: '{origin.relative_to(self.project_root)}' not found.")
                        continue

                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(origin), str(dest))
                    moved_origins.add(origin)

                    # [ASCENSION]: Record Artifact
                    artifacts.append(Artifact(
                        path=dest,
                        action="TRANSLOCATED",
                        size_bytes=dest.stat().st_size if dest.exists() else 0
                    ))

                    # [ELEVATION 13] THE RITE OF STRUCTURAL CONSECRATION
                    self.logger.verbose(f"Summoning Structure Sentinel for '{dest.name}'...")
                    self.structure_sentinel.ensure_structure(dest)

                progress.update(move_task, description="[green]Movement III: Translocation Complete.")

                # --- MOVEMENT IV: THE GNOSTIC HEALING (PURIFICATION) ---
                if not self.all_healing_plans:
                    Logger.info("Cortex Gaze is serene. No Gnostic bonds require healing.")
                else:
                    healer = PythonImportResolver(self.project_root, {}, {})

                    heal_task = progress.add_task("[magenta]Movement IV: Healing Gnostic connections...",
                                                  total=len(self.all_healing_plans))
                    all_rites_were_pure = True

                    for original_file_path, plan in self.all_healing_plans.items():
                        current_file_path = self._resolve_destination_path(original_file_path)

                        progress.update(heal_task, advance=1,
                                        description=f"[magenta]Healing '{current_file_path.name}'...")

                        if not current_file_path.exists():
                            Logger.error(
                                f"Healing Paradox: The patient '{current_file_path}' has vanished from reality. (Orig: {original_file_path})")
                            all_rites_were_pure = False
                            continue

                        if not healer.conduct_healing_rite(current_file_path, plan):
                            all_rites_were_pure = False

                        # [ASCENSION]: Record Healing
                        artifacts.append(Artifact(
                            path=current_file_path,
                            action="HEALED",
                            size_bytes=current_file_path.stat().st_size,
                            metadata={"healed_imports": len(plan)}
                        ))

                    progress.update(heal_task, description="[green]Movement IV: Gnostic Healing Complete.")
                    if not all_rites_were_pure:
                        raise ArtisanHeresy("The Symphony of Healing was marred by paradox.")

                # --- MOVEMENT V: THE PURIFICATION OF THE VOID ---
                purge_task = progress.add_task("[blue]Movement V: Purifying empty sanctums...", total=1)
                parents_of_moved_files = {p.parent for p in moved_origins}
                purged_count = 0
                for parent in sorted(list(parents_of_moved_files), key=lambda p: len(p.parts), reverse=True):
                    if parent.is_dir() and not any(parent.iterdir()) and parent != self.project_root:
                        Logger.verbose(f"Purifying empty sanctum: '{parent.relative_to(self.project_root)}'")
                        try:
                            parent.rmdir()
                            purged_count += 1
                        except OSError:
                            pass
                progress.update(purge_task, completed=1,
                                description=f"[green]Movement V: Purification Complete ({purged_count} void(s) purged).")

                console.rule("[bold green]The Grand Symphony of Gnostic Evolution is Complete[/bold green]")

                # [ASCENSION]: RETURN THE GNOSTIC RESULT
                return ScaffoldResult.forge_success(
                    message=f"Translocated {len(moved_origins)} scriptures and healed {len(self.all_healing_plans)} bonds.",
                    data={
                        "moved": len(moved_origins),
                        "healed": len(self.all_healing_plans),
                        "purged": purged_count
                    },
                    artifacts=artifacts
                )

            except (ArtisanHeresy, Exception) as e:
                progress.stop()
                console.print(Panel(
                    Group(Text.from_markup(f"[bold red]A catastrophic paradox shattered the symphony.[/bold red]"),
                          Traceback.from_exception(type(e), e, e.__traceback__, show_locals=False)),
                    title="[red]Dossier of the Fallen Symphony[/red]", border_style="red"
                ))
                if self.backup_root_path:
                    console.print(
                        f"[yellow]Your reality has been preserved in the Gnostic Snapshot at: [cyan]{self.backup_root_path}[/cyan][/yellow]")

                # Re-raise to let the Nexus catch it and wrap it in the Heresy response
                raise ArtisanHeresy("The Grand Symphony was halted by a paradox.", child_heresy=e)

    def _resolve_destination_path(self: 'TranslocationConductor', original_path: Path) -> Path:
        """
        [THE ROBUST PATHFINDER]
        Locates the current location of a file that might have moved.
        """
        resolved_orig = original_path.resolve()

        # 1. Direct Move Check
        if resolved_orig in self.translocation_map.moves:
            return self.translocation_map.moves[resolved_orig]

        # 2. Ancestral Move Check
        best_parent = None
        best_dest = None

        for source, dest in self.translocation_map.moves.items():
            source_res = source.resolve()
            # We assume anything in the move map is a valid source
            try:
                if resolved_orig.is_relative_to(source_res):
                    if resolved_orig == source_res: continue

                    if best_parent is None or len(source_res.parts) > len(best_parent.parts):
                        best_parent = source_res
                        best_dest = dest.resolve()
            except ValueError:
                continue

        if best_parent and best_dest:
            rel_path = resolved_orig.relative_to(best_parent)
            return best_dest / rel_path

        return original_path