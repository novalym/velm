# scaffold/artisans/daemon_artisan/telemetry.py

import json
from pathlib import Path
import time
from typing import TYPE_CHECKING

import psutil
from rich.panel import Panel
from rich.table import Table

from .contracts import DaemonInfo
from ...interfaces.base import ScaffoldResult

if TYPE_CHECKING:
    from .conductor import DaemonArtisan


class TelemetryProvider:
    """The Oracle of Perception for the Daemon's state."""
    INFO_FILE = ".scaffold/daemon.json"

    def __init__(self, parent_artisan: 'DaemonArtisan'):
        self.parent = parent_artisan

    def proclaim_status(self, request) -> ScaffoldResult:
        """The Rite of Perception."""
        project_root = request.project_root or Path.cwd()
        info_file = project_root / self.INFO_FILE

        table = Table(title="[bold]Unified Gnostic Daemon Status[/bold]", box=None, show_header=False)
        table.add_column("Key", style="cyan");
        table.add_column("Value")

        if not info_file.exists():
            table.add_row("Status", "[dim]Offline[/dim]")
        else:
            try:
                info = DaemonInfo.model_validate_json(info_file.read_text())
                if psutil.pid_exists(info.pid):
                    proc = psutil.Process(info.pid)
                    uptime = time.time() - info.start_time
                    table.add_row("Status", f"[bold green]Online ({proc.status()})[/]")
                    table.add_row("PID", str(info.pid))
                    table.add_row("Uptime", f"{uptime / 60:.1f} mins")
                    table.add_row("Memory", f"{proc.memory_info().rss / 1024 ** 2:.1f} MB")
                    table.add_row("Nexus", f"{info.host}:{info.port}")
                    table.add_row("Mode", info.mode)
                    table.add_row("Project", info.project_root)
                else:
                    table.add_row("Status", "[bold red]Zombie Record[/bold red]")
                    info_file.unlink(missing_ok=True)
            except Exception as e:
                table.add_row("Status", "[bold red]Corrupted Gnosis[/bold red]")
                table.add_row("Heresy", str(e))

        self.parent.console.print(Panel(table, border_style="magenta"))
        return self.parent.success("Status proclaimed.")

    def stream_logs(self, request) -> ScaffoldResult:
        """The Prophecy of the Rite of Communion."""
        # Future: Implement logic to connect to daemon and stream logs
        return self.parent.success("Log streaming is a future ascension.")