

from typing import List, Optional
from rich.panel import Panel
from rich.text import Text

class SecurityScribe:
    """Forges the 'Sentinel's Verdict' panel for security warnings."""

    def __init__(self, warnings: Optional[List[str]]):
        self.warnings = warnings

    def forge(self) -> Optional[Panel]:
        """The one true rite of forging for this Scribe."""
        if not self.warnings:
            return None

        content = Text("The Sentinel's Gaze has perceived profane artifacts within the newly forged reality:\n", style="white")
        for warning in self.warnings:
            content.append(f"\n  • {warning}", style="bold")

        return Panel(
            content,
            title="[bold white on red] 💀 CRITICAL HERESY: Sentinel's Verdict [/bold white on red]",
            border_style="red",
            padding=(1, 2)
        )