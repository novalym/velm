# Path: src/velm/core/maestro/proclamations/panel_scribe.py
# --------------------------------------------------------

from rich.panel import Panel
from rich.text import Text
from .base import ProclamationScribe


class PanelScribe(ProclamationScribe):
    """Renders high-status, boxed Imperial Decrees."""

    def proclaim(self, payload: str, metadata: dict):
        clean_msg = self._purify(payload or metadata.get("msg", ""))
        title = metadata.get("title", "Gnostic Decree")
        border = metadata.get("style", "cyan")

        panel = Panel(
            Text(clean_msg, justify="center"),
            title=f"[bold]{title}[/bold]",
            border_style=border,
            padding=(1, 2)
        )
        self.console.print(panel)