# Path: scaffold/rendering/text_renderer/diagnostic_scribe.py
# -----------------------------------------------------------
from rich.table import Table
from rich.markup import escape
from typing import Dict, Any

from .config import RendererConfig

class DiagnosticScribe:
    """
    [EVOLUTION 2, 6, 7]
    Handles the Diagnostic Gaze (Variables, Commands).
    """
    def __init__(self, config: RendererConfig):
        self.config = config

    def forge_context_table(self) -> Table:
        """[EVOLUTION 6] The Context Table Forge."""
        vars_table = Table(
            title="[bold magenta]I. The Altar of Gnostic Truths (Context)[/bold magenta]",
            box=None, expand=True, title_style="bold magenta", show_lines=True
        )
        vars_table.add_column("Key", style="cyan", width=20)
        vars_table.add_column("Value", style="white")
        vars_table.add_column("Type", style="dim white", width=8)

        for k, v in sorted(self.config.variables.items()):
            type_name = type(v).__name__
            display_val = str(v)

            if any(s in k.lower() for s in ['secret', 'key', 'token', 'password']):
                display_val = "***"
            elif len(display_val) > 60:
                display_val = display_val[:57] + "..."

            type_color = "green" if type_name == "bool" else "blue" if type_name == "int" else "dim"
            vars_table.add_row(k, escape(display_val), f"[{type_color}]{type_name}[/{type_color}]")

        return vars_table

    def forge_maestro_scroll(self) -> Table:
        """[EVOLUTION 7] The Maestro Scroll."""
        will_table = Table(
            title="[bold yellow]III. The Scripture of Will (Commands)[/bold yellow]",
            box=None, show_header=False, expand=True, title_style="bold yellow"
        )
        will_table.add_column(style="yellow")

        if self.config.post_run_commands:
            for command in self.config.post_run_commands:
                will_table.add_row(f"$ {escape(str(command))}")
        else:
            will_table.add_row("[dim]The Maestro is silent.[/dim]")

        return will_table