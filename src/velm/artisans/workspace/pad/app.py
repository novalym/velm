# Path: scaffold/artisans/workspace/pad/app.py
# --------------------------------------------
import os
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any

import yaml
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, DataTable, Static, Log, Button, Checkbox, Collapsible

from ..contracts import WorkspaceConfig, WorkspaceProject
from ....utils.workspace_utils import find_workspace_root
from ....logger import Scribe


# ===============================================================
# == I. THE SACRED VESSELS & ENUMS                             ==
# ===============================================================

class ProjectStatus(Enum):
    """The Gnostic state of a single reality in the cosmos."""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    HEALTHY = "HEALTHY"
    DRIFT = "DRIFT"
    UNKNOWN = "UNKNOWN"
    HERESY = "HERESY"


@dataclass
class ProjectEntry:
    """The complete Gnostic Dossier for a project in the UI."""
    path: str
    managed: bool
    status: ProjectStatus = ProjectStatus.UNKNOWN
    details: str = "Awaiting Gaze..."
    config: Optional[WorkspaceProject] = None


# ===============================================================
# == II. THE GOD-ENGINE OF THE GNOSTIC COCKPIT                 ==
# ===============================================================

class WorkspacePadApp(App[None]):
    """The Gnostic Observatory - A Sentient Cockpit for your entire development cosmos."""

    TITLE = "Scaffold Gnostic Observatory"
    CSS = """
    Screen { layout: vertical; }
    #main_view { layout: horizontal; height: 1fr; }
    #project_list_container { width: 40%; border-right: solid $accent; }
    #detail_pane { width: 1fr; padding: 1; }
    #log_container { height: 30%; dock: bottom; border-top: wide $accent; }
    Log { padding: 1; }
    DataTable { height: 1fr; }
    #detail_table { border: none; }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("a", "add_unmanaged", "Adopt"),
        Binding("e", "exec_command", "Exec"),
        Binding("h", "run_health_check", "Health"),
        Binding("s", "sync_workspace", "Sync"),
        Binding("l", "toggle_log", "Logs"),
    ]

    def __init__(self, project_root: Path, **kwargs):
        super().__init__(**kwargs)
        self.scribe = Scribe("WorkspacePad")
        self.project_root = project_root
        self.workspace_root: Optional[Path] = None
        self.workspace_config: Optional[WorkspaceConfig] = None
        self.projects: Dict[str, ProjectEntry] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main_view"):
            with Vertical(id="project_list_container"):
                yield DataTable(cursor_type="row", id="project_table")
            yield Static("Select a project to see its Gnosis.", id="detail_pane")
        with Collapsible(title="Gnostic Chronicle", collapsed=True, id="log_container"):
            yield Log()
        yield Footer()

    def on_mount(self):
        self.sub_title = "Scanning the cosmos..."
        self.run_initial_scan()

    # ===============================================================
    # == ELEVATION 1: THE GNOSTIC RADAR & ZERO-CONFIG GENESIS      ==
    # ===============================================================
    @work(exclusive=True, thread=True, group="scan")
    def run_initial_scan(self):
        """Discovers the workspace or initiates the adoption prophecy."""
        try:
            self.workspace_root = find_workspace_root(self.project_root)

            # [ELEVATION 11] Zero-Config Genesis
            if not self.workspace_root:
                # Annihilation of the Profane Plea: Use reactive var assignment
                self.sub_title = "[yellow]No workspace found. Conducting Gnostic Radar...[/yellow]"
                potential_paths = []
                for item in self.project_root.iterdir():
                    if item.is_dir() and (item / ".git").exists():
                        potential_paths.append(f"./{item.name}")

                # We must use call_from_thread for methods
                self.call_from_thread(self.action_add_unmanaged, potential_paths, is_genesis=True)
                return

            self.sub_title = f"Observatory Online: {self.workspace_root.name}"
            ws_path = self.workspace_root / ".scaffold-workspace"
            config_data = yaml.safe_load(ws_path.read_text(encoding='utf-8'))
            self.workspace_config = WorkspaceConfig(**config_data)

            managed_paths = {p.path for p in self.workspace_config.projects}
            for p in self.workspace_config.projects:
                self.projects[p.path] = ProjectEntry(path=p.path, managed=True, config=p)

            # Discover unmanaged projects
            for item in self.workspace_root.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    rel_path = f"./{item.name}"
                    if rel_path not in managed_paths:
                        self.projects[rel_path] = ProjectEntry(path=rel_path, managed=False)

            self.call_from_thread(self._update_table)
            self.call_from_thread(self.run_health_check)  # Auto-run health on load

        except Exception as e:
            self.call_from_thread(self.notify, f"Error loading workspace: {e}", severity="error")

    def _update_table(self):
        """[ELEVATION 10] Renders the project list with Gnostic Sigils of State."""
        table = self.query_one("#project_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Status", "Project", "Tags")

        # Sort for consistency: managed first, then by path
        sorted_projects = sorted(self.projects.values(), key=lambda p: (not p.managed, p.path))

        for proj in sorted_projects:
            status_map = {
                ProjectStatus.ONLINE: ("[bold green]●[/]", "Online"),
                ProjectStatus.OFFLINE: ("[bold red]●[/]", "Offline"),
                ProjectStatus.HEALTHY: ("[bold green]✅[/]", "Pure"),
                ProjectStatus.DRIFT: ("[bold yellow]⚡[/]", "Drift"),
                ProjectStatus.HERESY: ("[bold red]💀[/]", "Heresy"),
                ProjectStatus.UNKNOWN: ("[dim]?[/]", "Unknown"),
            }
            sigil, _ = status_map.get(proj.status, ("[dim]?[/]", "Unknown"))

            # Differentiate managed vs unmanaged
            path_style = "cyan" if proj.managed else "dim cyan"
            tags = ", ".join(proj.config.tags) if proj.config else ""

            table.add_row(Text.from_markup(sigil), Text(proj.path, style=path_style), tags, key=proj.path)

    # ===============================================================
    # == ELEVATION 4 & 6: THE LUMINOUS DOSSIER & GIT INTEGRATION   ==
    # ===============================================================
    @on(DataTable.RowSelected, "#project_table")
    def on_project_selected(self, event: DataTable.RowSelected):
        """Displays a rich, Gnostic Dossier for the selected project."""
        proj_path_str = event.row_key.value
        proj_entry = self.projects.get(proj_path_str)
        if not proj_entry: return

        proj_path = (self.workspace_root or self.project_root) / proj_path_str

        dossier = Table.grid(expand=True)
        dossier.add_column(style="bold cyan", width=12)
        dossier.add_column()

        dossier.add_row("Path:", proj_path_str)
        dossier.add_row("Managed:", "Yes" if proj_entry.managed else "No (Adopt with 'a')")

        if not proj_path.is_dir():
            dossier.add_row("Status:", "[bold red]OFFLINE[/]")
        else:
            try:
                branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=proj_path, text=True,
                                                 stderr=subprocess.DEVNULL).strip()
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=proj_path, text=True,
                                                 stderr=subprocess.DEVNULL).strip()
                dossier.add_row("Branch:", branch)
                dossier.add_row("Git Status:", '[bold green]CLEAN[/]' if not status else '[bold yellow]DIRTY[/]')
            except Exception:
                dossier.add_row("Git Status:", "[dim]Not a Git repository.[/dim]")

        self.query_one("#detail_pane").update(Panel(dossier, title=f"Gnosis: {proj_path.name}"))

    # ===============================================================
    # == ELEVATION 5, 7, 8: ACTIONS & THE RITE OF INSCRIPTION      ==
    # ===============================================================
    def action_add_unmanaged(self, potential_paths: Optional[List[str]] = None, is_genesis: bool = False):
        """[ELEVATION 7] The Interactive Adoption Altar."""
        # A full modal screen for adopting unmanaged projects
        pass  # Placeholder for a new ModalScreen

    @work(thread=True)
    def action_run_health_check(self):
        """[ELEVATION 4 & 6] The Panoptic Health Inquest."""
        # ... logic to run 'scaffold verify' on projects and update their status ...
        pass

    @work(thread=True)
    def action_sync_workspace(self):
        """[ELEVATION 8] The Rite of Gnostic Replication."""
        # ... logic to run 'scaffold workspace sync' ...
        pass

    def action_exec_command(self):
        """[ELEVATION 5] The Universal Edict Terminal."""
        # ... logic to open a prompt and run 'scaffold workspace exec' ...
        pass

    def action_toggle_log(self):
        """Toggles the visibility of the log pane."""
        log_pane = self.query_one("#log_pane")
        log_pane.display = not log_pane.display