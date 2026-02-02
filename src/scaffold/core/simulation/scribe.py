# scaffold/core/simulation/scribe.py

from rich.console import Group
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.box import ROUNDED, HEAVY

from .prophecy import Prophecy
from ...logger import get_console


class ProphecyScribe:
    """
    =================================================================================
    == THE LUMINOUS HERALD OF THE FUTURE (V-Ω-VISUALIZER-ULTIMA)                   ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Scribe of the Simulation. It transmutes the `Prophecy` vessel into a
    rich, interactive terminal dashboard.

    ### THE PANTHEON OF FACULTIES:
    1.  **The Gaze of Purity:** If the simulation results in no changes, it proclaims
        a serene "Green Panel" of harmony, ensuring the Architect knows the system
        is healthy, not just silent.
    2.  **The Altar of Context:** Renders the injected variables (Gnosis) that drove
        the simulation, filtering out internal system noise.
    3.  **The Differential Cinema:** Renders file changes as a high-level summary table
        followed by syntax-highlighted diff panels.
    4.  **The Limit Ward:** Intelligently caps the number of detailed diff panels
        displayed to prevent flooding the terminal on massive refactors.
    5.  **The Maestro's Scroll:** Displays simulated shell commands in a dedicated
        execution table.
    6.  **The Heresy Chronicle:** Renders simulated errors with the full gravity of
        a red alert.
    """

    def __init__(self, prophecy: Prophecy):
        self.prophecy = prophecy
        self.console = get_console()

    def proclaim(self):
        """The Grand Rite of Visual Revelation."""
        dossier_items = []

        # --- MOVEMENT I: THE GAZE OF PURITY ---
        # If nothing happened, we must still speak, lest the Architect thinks we are dead.
        is_empty_run = (
                not self.prophecy.diffs and
                not self.prophecy.heresies and
                not self.prophecy.simulated_commands
        )

        if is_empty_run:
            self.console.print(Panel(
                "[bold green]The Prophecy is Serene.[/bold green]\n"
                "The Gnostic Gaze perceived no divergence between Intent and Reality.\n"
                "[dim]No files created, modified, or deleted. No edicts spoken.[/dim]",
                title="[green]Quantum Simulation: Harmony[/green]",
                border_style="green",
                box=HEAVY,
                padding=(1, 2)
            ))
            return

        # --- MOVEMENT II: THE ALTAR OF VARIABLES ---
        # We show the Gnostic Context that fueled this simulation.
        if self.prophecy.final_variables:
            var_table = Table(
                box=None,
                show_header=True,
                expand=True,
                show_edge=False,
                padding=(0, 2)
            )
            var_table.add_column("Gnostic Variable", style="cyan", width=25)
            var_table.add_column("Resolved Value", style="green")

            has_vars = False
            # Sort for deterministic beauty
            for k, v in sorted(self.prophecy.final_variables.items()):
                # Filter internal scaffold variables to reduce noise
                if k.startswith("SCAFFOLD_"): continue
                if k in ["project_root", "template_path"]: continue

                val_str = str(v)
                # Truncate long values
                if len(val_str) > 100: val_str = val_str[:97] + "..."

                var_table.add_row(f"$$ {k}", escape(val_str))
                has_vars = True

            if has_vars:
                dossier_items.append(Panel(
                    var_table,
                    title="[bold magenta]I. Alchemical Context[/bold magenta]",
                    border_style="dim magenta",
                    padding=(0, 1)
                ))

        # --- MOVEMENT III: THE DIFFERENTIAL CINEMA ---
        if self.prophecy.diffs:
            # A. The High-Level Summary Table
            diff_table = Table(
                box=ROUNDED,
                expand=True,
                show_edge=True,
                header_style="bold white"
            )
            diff_table.add_column("Status", width=12, justify="center")
            diff_table.add_column("Scripture (Path)", style="cyan")
            diff_table.add_column("Nature", style="dim")

            for d in self.prophecy.diffs:
                status_style = "bold green" if d.status == "CREATED" else "bold yellow" if d.status == "MODIFIED" else "bold red"
                icon = "✨" if d.status == "CREATED" else "⚡" if d.status == "MODIFIED" else "💀"

                # Heuristic for nature
                nature = "Binary" if "[Binary" in (d.diff or "") else "Text"
                if d.path == "scaffold.lock": nature = "Chronicle"

                diff_table.add_row(
                    f"[{status_style}]{icon} {d.status}[/]",
                    d.path,
                    nature
                )

            dossier_items.append(Panel(
                diff_table,
                title="[bold yellow]II. Prophesied Transfigurations (Summary)[/bold yellow]",
                border_style="yellow",
                padding=(0, 0)
            ))

            # B. The Detailed Diffs (The Zoom)
            # We show the top 5 diffs to avoid console flooding
            MAX_DIFFS_TO_SHOW = 5
            shown_diffs = 0

            detailed_panels = []

            for d in self.prophecy.diffs:
                if shown_diffs >= MAX_DIFFS_TO_SHOW:
                    remaining = len(self.prophecy.diffs) - shown_diffs
                    detailed_panels.append(
                        Panel(f"[dim italic]... and {remaining} more scripture(s) modified.[/dim italic]",
                              border_style="dim")
                    )
                    break

                # Only show diff content if it exists and isn't the lockfile (noise)
                if d.diff and "Gnostic Chronicle" not in d.diff:
                    syntax_theme = "monokai"
                    lang = "diff"

                    # If it's a new file, show it as code, not diff
                    if d.status == "CREATED":
                        lang = d.path.split('.')[-1] if '.' in d.path else "text"
                        # Normalize lang for Rich
                        if lang not in ['js', 'ts', 'py', 'rs', 'go', 'json', 'yaml', 'md', 'css', 'html']:
                            lang = 'text'

                    # Clean up the diff/content
                    display_content = d.diff.strip()
                    if not display_content: continue

                    panel_title = Text.assemble(
                        (f"{d.status}: ", "bold " + ("green" if d.status == "CREATED" else "yellow")),
                        (d.path, "cyan")
                    )

                    detailed_panels.append(
                        Panel(
                            Syntax(display_content, lang, theme=syntax_theme, word_wrap=True),
                            title=panel_title,
                            border_style="dim"
                        )
                    )
                    shown_diffs += 1

            if detailed_panels:
                dossier_items.append(Group(*detailed_panels))

        # --- MOVEMENT IV: THE MAESTRO'S WILL ---
        if self.prophecy.simulated_commands:
            cmd_table = Table(box=None, expand=True, show_edge=False, padding=(0, 2))
            cmd_table.add_column("Edict", style="bold white")
            cmd_table.add_column("Simulation Output", style="dim")

            for cmd in self.prophecy.simulated_commands:
                cmd_table.add_row(f"$ {cmd.command}", cmd.output)

            dossier_items.append(Panel(
                cmd_table,
                title="[bold blue]III. Maestro's Edicts (Simulated)[/bold blue]",
                border_style="blue"
            ))

        # --- MOVEMENT V: THE HERESY LOG ---
        if self.prophecy.heresies:
            heresy_group = []
            for h in self.prophecy.heresies:
                heresy_group.append(Panel(
                    f"[bold red]{h.message}[/bold red]\n[dim]{h.details or ''}[/dim]",
                    title=f"[red]Simulated Heresy ({h.severity.name})[/red]",
                    border_style="red"
                ))
            dossier_items.append(Group(*heresy_group))

        # --- FINAL ASSEMBLY: THE MASTER PANEL ---
        # Determine overall style
        rite_name = self.prophecy.rite_name.replace("Request", "").upper()
        is_success = self.prophecy.is_pure and not self.prophecy.heresies

        title_text = f"QUANTUM SIMULATION: {rite_name}"
        border_style = "green" if is_success else "red"

        if not is_success:
            title_text += " (TAINTED)"

        self.console.print(Panel(
            Group(*dossier_items),
            title=f"[bold {border_style}]{title_text}[/]",
            subtitle=f"[dim]{self.prophecy.summary}[/dim]",
            expand=True,
            border_style=border_style,
            box=HEAVY
        ))