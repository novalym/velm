# Path: scaffold/artisans/translocate_core/conductor/proclamation.py
# ------------------------------------------------------------------


from typing import Dict, List, Any, TYPE_CHECKING
from pathlib import Path
import json

from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.box import ROUNDED
from ....logger import get_console

if TYPE_CHECKING:
    from .engine import TranslocationConductor


class ProclamationMixin:
    """
    =================================================================================
    == THE FACULTY OF PROCLAMATION (V-Ω-LUMINOUS-SCRIBE)                           ==
    =================================================================================
    Handles the `_proclaim_prophetic_dossier` rite, rendering the plan to the UI.
    """

    def _proclaim_prophetic_dossier(self: 'TranslocationConductor', healing_plans: Dict[Path, List[Dict]],
                                    non_python_files: List[Path]):
        """
        =================================================================================
        == THE GOD-ENGINE OF PROPHETIC REVELATION (V-Ω-ULTRA-DEFINITIVE)               ==
        =================================================================================
        LIF: 10,000,000,000,000

        Forges a luminous, multi-part, and cinematic Dossier of the entire prophesied
        reality.
        """
        console = get_console()

        # [FACULTY 1] The Gnostic Triage of Will
        has_moves = bool(self.translocation_map and self.translocation_map.moves)
        has_heals = bool(healing_plans)
        has_warnings = bool(non_python_files)

        if not has_moves and not has_heals and not has_warnings:
            console.print(Panel(
                "[bold green]The Prophet's Gaze is serene. The current reality is already a perfect reflection of your will.[/bold green]",
                title="[green]Dossier of Purity[/green]",
                border_style="green"
            ))
            return

        # [FACULTY 2] The Cinematic Symphony - The Vessel is Forged
        prophecy_group_items: List[Any] = []

        # --- MOVEMENT I: THE TRANSLOCATION CARTOGRAPHER ---
        if has_moves:
            translocation_table = Table(
                title="[bold]➡️ Movement I: Prophesied Translocations[/bold]",
                box=ROUNDED, show_header=True, header_style="bold magenta"
            )
            translocation_table.add_column("Origin (Old Reality)", style="red", overflow="fold")
            translocation_table.add_column("Destination (New Reality)", style="green", overflow="fold")

            for origin, dest in self.translocation_map.moves.items():
                translocation_table.add_row(
                    str(origin.relative_to(self.project_root)),
                    str(dest.relative_to(self.project_root))
                )
            prophecy_group_items.append(translocation_table)

        # --- MOVEMENT II: THE GNOSTIC HEALER'S SCRIPTURE ---
        if has_heals:
            healing_table = Table(
                title="[bold]⚕️ Movement II: Prophesied Gnostic Healings[/bold]",
                box=ROUNDED, show_header=True, header_style="bold bright_cyan"
            )
            healing_table.add_column("Scripture to be Healed", style="cyan", overflow="fold")
            healing_table.add_column("L#", style="magenta", justify="right")
            healing_table.add_column("Profane Import", style="dim", overflow="fold")
            healing_table.add_column("Pure Import", style="bright_cyan", overflow="fold")

            for original_file_path, plan in sorted(healing_plans.items()):
                current_file_path = self.translocation_map.moves.get(original_file_path.resolve(),
                                                                     original_file_path)
                for i, edict in enumerate(plan):
                    # For a clean table, only show the filename on the first entry for that file
                    try:
                        file_display = str(current_file_path.relative_to(self.project_root)) if i == 0 else ""
                    except ValueError:
                        file_display = current_file_path.name if i == 0 else ""

                    # [THE FIX] Polyglot Awareness & Schema Healing
                    # We inspect the edict keys to determine the language and format.

                    if 'original_module' in edict and 'symbol_name' in edict:
                        # Python HealingEdict
                        original_str = f"from {edict['original_module']} import {edict['symbol_name']}"
                        healed_str = f"from {edict['new_module_path']} import {edict['symbol_name']}"

                    elif 'original_specifier' in edict:
                        # JS/TS/React HealingEdict
                        original_str = f"import ... from '{edict['original_specifier']}'"
                        healed_str = f"import ... from '{edict['new_specifier']}'"

                    elif 'original_import' in edict:
                        # Legacy Python Format (Fallback)
                        original_imp = edict['original_import']
                        original_str = f"from {original_imp.get('module') or '.' * original_imp.get('level', 0)} import {original_imp.get('name')}"
                        healed_str = f"from {edict['new_module_path']} import {edict['symbol_name']}"

                    else:
                        # Unknown Format (Display Raw Data)
                        original_str = "Unknown Import"
                        healed_str = json.dumps(edict, indent=None)

                    healing_table.add_row(
                        file_display,
                        str(edict.get('line_num', '?')),
                        original_str,
                        healed_str
                    )
            prophecy_group_items.append(healing_table)

        # --- MOVEMENT III: THE POLYGLOT MENTOR ---
        if has_warnings:
            polyglot_warning_table = Table(
                title="[bold]⚠️ Movement III: Polyglot Mentor's Guidance[/bold]",
                box=ROUNDED, show_header=False, header_style="bold yellow"
            )
            polyglot_warning_table.add_column("Gnostic Prophecy", style="yellow")

            polyglot_warning_table.add_row(
                "The following scriptures will be translocated, but their internal Gnostic connections (imports/requires) "
                "will NOT be healed. This artisan awaits its Tree-sitter ascension for these tongues."
            )
            for file_path in non_python_files:
                try:
                    rel_path = file_path.relative_to(self.project_root)
                except ValueError:
                    rel_path = file_path.name
                polyglot_warning_table.add_row(f"  - [cyan]{rel_path}[/cyan]")

            prophecy_group_items.append(polyglot_warning_table)

        # --- THE FINAL PROCLAMATION ---
        console.print(Panel(
            Group(*prophecy_group_items),
            title="[bold yellow]Dossier of Prophetic Transfiguration[/bold yellow]",
            subtitle="[dim]This is a Quantum Simulation. No reality has been altered.[/dim]",
            border_style="yellow"
        ))