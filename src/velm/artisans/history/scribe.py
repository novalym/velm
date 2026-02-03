# Path: scaffold/artisans/history/scribe.py
# -----------------------------------------

from datetime import datetime, timezone
from typing import List, Optional

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .contracts import RiteGnosis
from ...utils import get_human_readable_size


class HistoryScribe:
    """
    =================================================================================
    == THE SCRIBE OF THE TIMELINE (V-Ω-LUMINOUS-HERALD)                            ==
    =================================================================================
    The dedicated renderer for the History Artisan. It transforms `RiteGnosis`
    vessels into beautiful, information-dense terminal displays.
    """

    def __init__(self, console: Console):
        self.console = console

    def _format_age(self, ts: datetime) -> str:
        """[FACULTY 11] The Chronometric Harmonizer's Voice."""
        now = datetime.now(timezone.utc)
        delta = now - ts
        seconds = delta.total_seconds()

        if seconds < 60: return "Just now"
        if seconds < 3600: return f"{int(seconds / 60)}m ago"
        if seconds < 86400: return f"{int(seconds / 3600)}h ago"
        return f"{delta.days}d ago"

    def proclaim_timeline(self, history: List[RiteGnosis]):
        """[FACULTY 3] The Luminous Timeline."""
        table = Table(title="[bold magenta]The Gnostic Timeline[/bold magenta]", box=None, expand=True)
        table.add_column("Rite ID", style="cyan", no_wrap=True, width=10)
        table.add_column("Age", style="dim", width=12)
        table.add_column("Rite Name", style="white")
        table.add_column("Impact", style="yellow", justify="right")
        table.add_column("Branch", style="green")
        table.add_column("Architect", style="dim italic")

        for i, entry in enumerate(history):
            age = "[bold]HEAD[/bold]" if entry.is_head else self._format_age(entry.timestamp)

            stats = entry.provenance.rite_stats
            c = stats.get('create', 0)
            u = stats.get('update', 0)
            d = stats.get('delete', 0)
            m = stats.get('move', 0)
            impact_parts = []
            if c > 0: impact_parts.append(f"[green]+{c}[/green]")
            if u > 0: impact_parts.append(f"[yellow]~{u}[/yellow]")
            if d > 0: impact_parts.append(f"[red]-{d}[/red]")
            if m > 0: impact_parts.append(f"[cyan]>>{m}[/cyan]")
            impact_str = " ".join(impact_parts) or f"{len(entry.manifest)} files"

            table.add_row(
                entry.rite_id[:8],
                age,
                entry.rite_name,
                impact_str,
                entry.provenance.git_branch or "detached",
                entry.provenance.architect
            )
        self.console.print(table)

    def proclaim_inspection(self, rite: RiteGnosis, diff_results: Optional[List] = None):
        """[FACULTY 2] The Forensic Inspector's Voice."""

        prov_table = Table(box=None, show_header=False, padding=(0, 2))
        prov_table.add_column(style="dim", justify="right");
        prov_table.add_column(style="white")
        prov_table.add_row("Rite Name:", f"[cyan]{rite.rite_name}[/cyan]")
        prov_table.add_row("Rite ID:", rite.rite_id)
        prov_table.add_row("Timestamp:", str(rite.timestamp))
        prov_table.add_row("Architect:",
                           f"[yellow]{rite.provenance.architect} on {rite.provenance.machine_id}[/yellow]")
        if rite.provenance.git_commit:
            prov_table.add_row("Git Context:", f"{rite.provenance.git_branch} @ {rite.provenance.git_commit[:7]}")

        detail_items = []
        if rite.gnosis_delta:
            delta_table = Table(title="[bold]Gnosis Delta[/bold]", box=None, show_header=False)
            delta_table.add_column(style="yellow");
            delta_table.add_column(style="white")
            for k, v in rite.gnosis_delta.items():
                delta_table.add_row(f"{k}:", str(v))
            detail_items.append(delta_table)

        if rite.edicts:
            edict_text = Text("\n".join([f"$ {e}" for e in rite.edicts]))
            detail_items.append(Panel(edict_text, title="[bold]Maestro's Edicts[/bold]", border_style="dim"))

        manifest_table = Table(title="[bold]Manifest of Reality[/bold]", show_lines=True)
        manifest_table.add_column("Path", style="white")
        manifest_table.add_column("Gnosis", style="dim")

        for path, meta in sorted(rite.manifest.items()):
            action = meta.get('action', 'ADOPTED')
            color = "green" if action == "CREATED" else "yellow" if "TRANS" in action else "cyan"
            gnosis_text = Text.assemble(
                (f"Action: ", "bold"), (f"[{color}]{action}[/{color}]\n"),
                (f"Size: {get_human_readable_size(meta.get('bytes', 0))}\n"),
                (f"Origin: [magenta]{meta.get('blueprint_origin', 'Unknown')}[/magenta]")
            )
            manifest_table.add_row(path, gnosis_text)

        main_group = [
            Panel(prov_table, title="[bold magenta]Gnostic Provenance[/bold magenta]", border_style="magenta")]
        if detail_items:
            main_group.append(Group(*detail_items))
        main_group.append(manifest_table)

        self.console.print(Group(*main_group))