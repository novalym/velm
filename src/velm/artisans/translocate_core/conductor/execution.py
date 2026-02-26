# Path: artisans/translocate_core/conductor/execution.py
# ------------------------------------------------------

from __future__ import annotations
import shutil
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Set, List, Dict, Optional, Tuple

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.console import Group
from rich.traceback import Traceback
from rich.text import Text

# --- THE DIVINE UPLINKS ---
from ....logger import get_console, Scribe
from ....contracts.data_contracts import InscriptionAction
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..resolvers import PythonImportResolver
from ....interfaces.base import ScaffoldResult, Artifact

if TYPE_CHECKING:
    from .engine import TranslocationConductor

Logger = Scribe("TranslocationExecution")


class ExecutionMixin:
    """
    =================================================================================
    == THE OMEGA FACULTY OF EXECUTION (V-Ω-KINETIC-SUTURE-V1100)                   ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_EVOLUTION_CONDUCTOR | RANK: OMEGA_SUPREME
    AUTH: Ω_CONDUCT_V1100_IO_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    This is the final, evolved heart of the Translocation Symphony. It has been
    stripped of physical anxiety and sutured to the Sovereign Hand (IOConductor).
    It manages the transition of matter and bonds through Five Sacred Movements.
    =================================================================================
    """

    def conduct(self: 'TranslocationConductor') -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EVOLUTION (CONDUCT)                               ==
        =============================================================================
        LIF: ∞ | The supreme rite of reality transfiguration.
        """
        console = get_console()
        final_artifacts: List[Artifact] = []
        start_ns = time.perf_counter_ns()

        # --- PRE-FLIGHT ADJUDICATION ---
        if not self.translocation_map or not self.translocation_map.moves:
            self.logger.info("Guardian of the Void: The plan is empty. The symphony is gracefully stayed.")
            return ScaffoldResult.forge_success("No translocation required.", data={"moved": 0})

        # [FACULTY 12]: THE HEARTBEAT SIGNAL
        self._project_hud_pulse("EVOLUTION_START", "#a855f7")

        # [[[ THE GAZE OF CONTAINMENT: COLLECTIVE INQUEST ]]]
        all_files_in_scope: Set[Path] = self._scry_total_scope()
        self.logger.verbose(f"Gaze of Containment perceived {len(all_files_in_scope)} total scriptures in scope.")

        # =========================================================================
        # == MOVEMENT I: THE PROPHECY (CORTEX COMMUNION)                         ==
        # =========================================================================
        # Scry the Gnostic Graph to predict which bonds will shatter when matter moves.
        self.logger.info("Movement I: The Prophecy. Communing with the Gnostic Cortex...")
        self.all_healing_plans = self.cortex.prophesy_healing_plan(self.translocation_map.moves)
        self.logger.success("Cortex has spoken. The Prophecy of Healing is complete.")

        # --- THE GNOSTIC TRIAGE OF WILL ---
        if self.preview:
            # [ASCENSION 4]: Holographic Preview
            non_python_files = [f for f in all_files_in_scope if f.suffix != '.py']
            self._proclaim_prophetic_dossier(self.all_healing_plans, non_python_files)
            return ScaffoldResult.forge_success(
                "Prophecy Revealed (Simulation).",
                data={"plan": str(self.all_healing_plans)},
                ui_hints={"vfx": "pulse_blue", "icon": "eye"}
            )

        # =========================================================================
        # == THE PATH OF MANIFESTATION: THE CINEMATIC SYMPHONY                   ==
        # =========================================================================
        console.rule("[bold magenta]The Grand Symphony of Gnostic Evolution Begins[/bold magenta]")

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console
        ) as progress:
            try:
                # =========================================================================
                # == MOVEMENT II: THE VOW OF REASSURANCE (GNOSTIC SNAPSHOT)              ==
                # =========================================================================
                if self.backup_root_path:
                    backup_task = progress.add_task("[yellow]Movement II: Forging Gnostic Snapshot...",
                                                    total=len(self.translocation_map.moves))
                    snapshot_dir = self._forge_gnostic_snapshot(progress, backup_task)
                    progress.update(backup_task, completed=len(self.translocation_map.moves),
                                    description=f"[green]Snapshot forged at [cyan]'{snapshot_dir.name}'[/cyan].")

                # =========================================================================
                # == MOVEMENT III: THE TRANSLOCATION (THE KINETIC STRIKE)                ==
                # =========================================================================
                # [THE CURE]: Delegating to the Sovereign Hand (IOConductor).
                move_task = progress.add_task("[cyan]Movement III: Translocating scriptures...",
                                              total=len(self.translocation_map.moves))
                moved_origins = set()

                # [ASCENSION 6]: Topological Depth Sorting
                sorted_moves = sorted(self.translocation_map.moves.items(), key=lambda x: len(x[0].parts))

                for origin, dest in sorted_moves:
                    progress.update(move_task, advance=1, description=f"[cyan]Moving [red]'{origin.name}'[/red]...")

                    # [ASCENSION 1]: THE ATOMIC STRIKE
                    # self.io (IOConductor) handles staging, ledger, and inverse-ops.
                    success = self.io.move(origin, dest)

                    if success:
                        moved_origins.add(origin)
                        # [ASCENSION 3]: RE-CONSECRATION
                        # The Sentinel blesses the new coordinate immediately.
                        self.structure_sentinel.ensure_structure(dest)

                        # [ASCENSION 7]: Artifact Inscription
                        final_artifacts.append(Artifact(
                            path=dest,
                            action="TRANSLOCATED",
                            size_bytes=dest.stat().st_size if dest.exists() else 0
                        ))
                    elif not self.preview:
                        # [ASCENSION 11]: Socratic Failure
                        raise ArtisanHeresy(
                            f"Translocation Fracture: Failed to manifest '{origin.name}' at new coordinate.",
                            severity=HeresySeverity.CRITICAL,
                            details=f"Target: {dest}",
                            suggestion="Check for OS-level file locks or substrate permissions."
                        )

                progress.update(move_task, description="[green]Movement III: Translocation Complete.")

                # =========================================================================
                # == MOVEMENT IV: THE GNOSTIC HEALING (BOND MENDING)                     ==
                # =========================================================================
                if not self.all_healing_plans:
                    Logger.info("Cortex Gaze is serene. No Gnostic bonds require healing.")
                else:
                    # [ASCENSION 13]: Import Shift Calculus
                    healer = PythonImportResolver(self.project_root, {}, {})
                    heal_task = progress.add_task("[magenta]Movement IV: Healing Gnostic connections...",
                                                  total=len(self.all_healing_plans))

                    for original_file_path, plan in self.all_healing_plans.items():
                        # Resolve the actual current locus of the file (it might have moved!)
                        current_file_path = self._resolve_destination_path(original_file_path)

                        progress.update(heal_task, advance=1,
                                        description=f"[magenta]Healing '{current_file_path.name}'...")

                        # [FACULTY 10]: Ghost-Locus Ward
                        if not current_file_path.exists():
                            # Check if it exists in the transaction's staging world
                            if not self.io.router.resolve(
                                    str(current_file_path.relative_to(self.project_root))).exists():
                                Logger.error(
                                    f"Healing Paradox: The patient '{current_file_path.name}' is unmanifest in all dimensions.")
                                continue

                        # Conduct the AST surgery
                        if healer.conduct_healing_rite(current_file_path, plan):
                            final_artifacts.append(Artifact(
                                path=current_file_path,
                                action="HEALED",
                                metadata={"bonds_mended": len(plan)}
                            ))

                    progress.update(heal_task, description="[green]Movement IV: Gnostic Healing Complete.")

                # =========================================================================
                # == MOVEMENT V: THE PURIFICATION (VOID RECLAMATION)                    ==
                # =========================================================================
                # [ASCENSION 12]: Reclaim empty sanctums left behind by the strike.
                purge_task = progress.add_task("[blue]Movement V: Purifying empty sanctums...", total=1)

                purged_count = 0
                parents_of_moved_files = {p.parent for p in moved_origins}

                # Sort deepest first to ensure recursive cleanup
                for parent in sorted(list(parents_of_moved_files), key=lambda p: len(p.parts), reverse=True):
                    # NEVER purge the Project Root or anything outside it
                    if parent.is_dir() and parent != self.project_root and parent.is_relative_to(self.project_root):
                        try:
                            # Only delete if actually empty
                            if not any(parent.iterdir()):
                                Logger.verbose(f"Purifying empty sanctum: '{parent.relative_to(self.project_root)}'")
                                parent.rmdir()
                                purged_count += 1
                        except OSError:
                            pass  # Parent is warded or not empty

                progress.update(purge_task, completed=1,
                                description=f"[green]Movement V: Purification Complete ({purged_count} void(s) purged).")

                # --- THE FINAL REVELATION ---
                console.rule("[bold green]The Grand Symphony of Gnostic Evolution is Complete[/bold green]")

                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                return ScaffoldResult.forge_success(
                    message=f"Translocated {len(moved_origins)} scriptures and healed {len(self.all_healing_plans)} bonds.",
                    data={
                        "moved_count": len(moved_origins),
                        "healed_count": len(self.all_healing_plans),
                        "purged_count": purged_count,
                        "latency_ms": duration_ms
                    },
                    artifacts=final_artifacts,
                    ui_hints={"vfx": "bloom", "sound": "success_chime"}
                )

            except Exception as catastrophic_paradox:
                # [ASCENSION 15]: THE FINALITY VOW (ROLLBACK SUTURE)
                progress.stop()
                self._project_hud_pulse("EVOLUTION_FRACTURED", "#ef4444")

                # Proclaim the tragedy
                console.print(Panel(
                    Group(
                        Text.from_markup(f"[bold red]A catastrophic paradox shattered the symphony.[/bold red]"),
                        Traceback.from_exception(type(catastrophic_paradox), catastrophic_paradox,
                                                 catastrophic_paradox.__traceback__, show_locals=False)
                    ),
                    title="[red]Dossier of the Fallen Symphony[/red]",
                    border_style="red"
                ))

                if self.backup_root_path:
                    console.print(
                        f"[yellow]Your reality is warded in the Gnostic Snapshot: [cyan]{self.backup_root_path.name}[/cyan][/yellow]")

                # Raise to the Engine's Healer
                raise ArtisanHeresy("The Grand Symphony was halted by a paradox.", child_heresy=catastrophic_paradox)

    def _scry_total_scope(self: 'TranslocationConductor') -> Set[Path]:
        """Perceives every physical scripture impacted by the willed moves."""
        scope = set()
        for origin in self.translocation_map.moves.keys():
            if origin.is_file():
                scope.add(origin.resolve())
            elif origin.is_dir():
                # Directory expansion
                for f in origin.rglob("*"):
                    if f.is_file(): scope.add(f.resolve())
        return scope

    def _resolve_destination_path(self: 'TranslocationConductor', original_path: Path) -> Path:
        """
        [FACULTY 2]: THE ROBUST PATHFINDER.
        Locates the new coordinate of a scripture that has moved during the strike.
        """
        resolved_orig = original_path.resolve()

        # 1. Direct Hit (The file itself moved)
        if resolved_orig in self.translocation_map.moves:
            return self.translocation_map.moves[resolved_orig]

        # 2. Ancestral Hit (The file's parent moved)
        best_parent, best_dest = None, None
        for source, dest in self.translocation_map.moves.items():
            source_res = source.resolve()
            try:
                if resolved_orig.is_relative_to(source_res) and resolved_orig != source_res:
                    # Choose the deepest matching parent for maximum precision
                    if best_parent is None or len(source_res.parts) > len(best_parent.parts):
                        best_parent = source_res
                        best_dest = dest.resolve()
            except ValueError:
                continue

        if best_parent and best_dest:
            rel_path = resolved_orig.relative_to(best_parent)
            return best_dest / rel_path

        return original_path

    def _project_hud_pulse(self: 'TranslocationConductor', type_label: str, color: str):
        """Radiates a kinetic signal to the Ocular interface."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "KINETIC_EVOLUTION",
                        "color": color,
                        "trace": getattr(self, "trace_id", "tr-void")
                    }
                })
            except:
                pass