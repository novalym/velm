# Path: elara/vis/forensic_ocular_scribe.py
# ----------------------------------------
from typing import Any

from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.syntax import Syntax


class ForensicOcularScribe:
    """
    =============================================================================
    == THE FORENSIC OCULAR SCRIBE (V-Ω-TOTALITY)                               ==
    =============================================================================
    Specialist artisan for rendering complex logical fractures into
    human-readable, high-status HUD panels.
    """

    @classmethod
    def forge_heresy_panel(cls, heresy: Any) -> Panel:
        """Forges a bit-perfect Rich panel for an ELARA Heresy."""

        content = Group(
            Text(f"L{heresy.line_num}: {heresy.message}", style="bold white"),
            Text(f"\n{heresy.details}", style="dim yellow"),
            Text(f"\n💡 Cure: {heresy.suggestion}", style="bold green")
        )

        return Panel(
            content,
            title="[bold red]Ω_LOGIC_FRACTURE[/bold red]",
            border_style="red",
            padding=(1, 2)
        )