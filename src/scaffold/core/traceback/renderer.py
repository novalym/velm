# scaffold/core/traceback/renderer.py

from typing import List
from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.box import ROUNDED, HEAVY

from .contracts import GnosticError, GnosticFrame


class GnosticRenderer:
    """
    =================================================================================
    == THE LUMINOUS HERALD OF PARADOX (V-Ω-VISUALIZER)                             ==
    =================================================================================
    Renders the Gnostic Error Dossier into a beautiful, interactive terminal interface.
    """

    def render(self, error: GnosticError) -> Panel:

        # --- 1. THE HEADER OF CATASTROPHE ---
        header_text = Text.assemble(
            ("⚡ GNOSTIC HERESY: ", "bold red"),
            (f"{error.exc_type}", "bold white on red"),
            ("\n"),
            (f"{error.exc_value}", "bold white")
        )

        # --- 2. THE CONTEXTUAL GRID ---
        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(style="dim white", justify="right")
        grid.add_column(style="cyan")

        if error.active_rite and error.active_rite != "Unknown":
            grid.add_row("Active Rite:", error.active_rite)
        if error.project_root:
            grid.add_row("Sanctum:", error.project_root)

        # --- 3. THE STACK SYMPHONY ---
        stack_renderables = []

        # We iterate in reverse (most recent call last is standard Python,
        # but we want the crash site at the bottom, visible).
        # Rich Traceback does this well. We mimic it but with Gnostic data.

        for i, frame in enumerate(error.frames):
            is_last = (i == len(error.frames) - 1)

            # Filter: Collapse System Libraries unless verbose?
            # For now, we render them DIMMED.
            style_color = "white" if frame.is_scaffold_code else "dim white"
            border_style = "red" if is_last else ("blue" if frame.is_scaffold_code else "dim")

            # Frame Header: File Path (Link) + Function
            file_link = f"[link={frame.editor_link}]{frame.filename}[/link]"

            frame_title = Text.assemble(
                (f"#{i} ", "dim"),
                (f"{frame.component_type} " if frame.component_type != "System" else "", "magenta"),
                (f"{frame.name}", "bold " + style_color),
                (" in ", "dim"),
                Text.from_markup(file_link),
                (f":{frame.lineno}", "cyan")
            )

            # Source Code Window
            code_content = "".join(frame.context_lines).rstrip()

            # Determine syntax lexer based on extension
            lexer = "python"
            if frame.filename.endswith(".ts"): lexer = "typescript"

            code_syntax = Syntax(
                code_content,
                lexer,
                theme="monokai",
                line_numbers=True,
                start_line=frame.context_start_lineno,
                highlight_lines={frame.lineno},
                word_wrap=False
            )

            # Local Variables (The Altar)
            locals_group = None
            if frame.locals:
                locals_table = Table(box=None, show_header=False, padding=(0, 1), expand=True)
                locals_table.add_column(style="cyan", ratio=1)
                locals_table.add_column(style="yellow", ratio=3)

                for k, v in frame.locals.items():
                    locals_table.add_row(k, v)

                locals_group = Panel(
                    locals_table,
                    title="[dim]Local Gnosis[/dim]",
                    border_style="dim",
                    padding=(0, 1)
                )

            # Assemble the Frame Panel
            frame_content = [code_syntax]
            if is_last and locals_group:
                frame_content.append(locals_group)

            stack_renderables.append(
                Panel(
                    Group(*frame_content),
                    title=frame_title,
                    title_align="left",
                    border_style=border_style,
                    padding=(0, 1)
                )
            )

        # --- 4. THE PROPHECY OF REDEMPTION ---
        # If the error has a suggestion (from ArtisanHeresy), display it.
        # We check if the exception string contains a suggestion or if we can infer one.
        suggestion_panel = None
        # (This relies on the Inspector capturing the suggestion, which we'll add to GnosticError in future)

        # --- 5. FINAL ASSEMBLY ---
        final_group = [
            grid,
            Text("\nTraceback (Most Recent Call Last):", style="bold underline"),
            *stack_renderables
        ]

        return Panel(
            Group(*final_group),
            title=header_text,
            border_style="red",
            box=HEAVY,
            padding=(1, 2)
        )