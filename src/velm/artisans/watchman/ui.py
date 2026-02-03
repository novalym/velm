# Path: scaffold/artisans/watchman/ui.py
# --------------------------------------
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from datetime import datetime


class SentinelUI:
    def __init__(self, console: Console):
        self.console = console
        self._live = None
        self._status_text = "Sentinel Standing By"
        self._last_trigger = "None"
        self._run_count = 0

    def header(self, target: str, command: str, profile_name: str = None):
        """Displays the Vigil's Charter."""
        self.console.clear()
        title = f"[bold cyan]The Watchman's Vigil[/bold cyan]"
        if profile_name:
            title += f" [bold magenta]({profile_name})[/bold magenta]"

        grid = f"""
[dim]Target:[/dim]  [yellow]{target}[/yellow]
[dim]Action:[/dim]  [green]{command}[/green]
"""
        self.console.print(Panel(grid.strip(), title=title, border_style="blue"))

    def on_trigger(self, path: str):
        """Updates the HUD when a change is detected."""
        self._run_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._last_trigger = f"{path} @ {timestamp}"

        # Clear screen for focus if desired (handled by logic, but UI prepares the space)
        self.console.print(f"\n[bold yellow]⚡ Change detected:[/bold yellow] {path}")
        self.console.rule(f"[bold]Run #{self._run_count}[/bold] ({timestamp})")

    def on_success(self, duration: float):
        self.console.print(f"\n[bold green]✔ Rite Completed[/bold green] in {duration:.2f}s")

    def on_failure(self, duration: float, code: int):
        self.console.print(f"\n[bold red]✘ Rite Failed[/bold red] (Exit {code}) in {duration:.2f}s")