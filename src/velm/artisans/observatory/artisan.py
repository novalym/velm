# Path: scaffold/artisans/observatory/artisan.py
# ----------------------------------------------

import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.console import Group

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ObservatoryRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy

# --- THE DIVINE COMMUNION ---
# We summon the Singleton Logic from the Core. We do NOT reinvent it.
from ...core.observatory import Observatory
from ...core.observatory.contracts import ProjectHealth


@register_artisan("observatory")
class ObservatoryArtisan(BaseArtisan[ObservatoryRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF THE OBSERVATORY (V-Ω-CLI-ADAPTER)                        ==
    =================================================================================
    LIF: 10,000,000,000

    The Command-Line Interface for the Gnostic Observatory.
    It translates user intent into Core Observatory operations.
    """

    def execute(self, request: ObservatoryRequest) -> ScaffoldResult:
        command = request.obs_command

        # The Grimoire of Rites
        rite_map = {
            "list": self._conduct_list,
            "add": self._conduct_add,
            "register": self._conduct_add,  # Alias
            "switch": self._conduct_switch,
            "active": self._conduct_active,
            "discover": self._conduct_discover,
            "prune": self._conduct_prune,
            "health": self._conduct_health,
            "open": self._conduct_open,
        }

        handler = rite_map.get(command)
        if not handler:
            return self.failure(f"Unknown observatory rite: '{command}'")

        return handler(request)

    def _conduct_add(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 6] The Atomic Add."""
        if not request.target:
            return self.failure("The 'add' rite requires a target path.")

        # Resolve path relative to CWD (User Context)
        target_path = Path.cwd() / request.target
        if not target_path.exists():
            return self.failure(f"The path '{request.target}' is a void.")

        entry = Observatory.register(str(target_path), name=request.name)

        return self.success(
            f"Project '{entry.name}' registered.",
            data={"project_id": entry.id, "project": entry.model_dump()}
        )

    def _conduct_list(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 12] The Luminous Dossier."""
        projects = Observatory.list_projects()
        active = Observatory.get_active()

        # JSON Mode for Electron
        if request.json_mode:
            return self.success(
                "Projects listed.",
                data={"projects": [p.model_dump() for p in projects], "active_id": active.id if active else None}
            )

        # Rich UI Mode
        table = Table(title="[bold cyan]The Gnostic Observatory[/bold cyan]", border_style="cyan")
        table.add_column("*", style="bold green", width=3)
        table.add_column("ID", style="dim")
        table.add_column("Project Name", style="bold white")
        table.add_column("Path", style="blue")
        table.add_column("Health", justify="center")
        table.add_column("Tech Stack", style="magenta")

        for p in projects:
            is_active = active and active.id == p.id
            marker = "➤" if is_active else ""

            health_style = {
                ProjectHealth.HEALTHY: "green",
                ProjectHealth.DIRTY: "yellow",
                ProjectHealth.GHOST: "red",
                ProjectHealth.UNKNOWN: "dim"
            }.get(p.health, "white")

            stack = f"{p.metadata.language.value}"
            if p.metadata.frameworks:
                stack += f" ({', '.join(p.metadata.frameworks[:2])})"

            table.add_row(
                marker,
                p.id[:8],
                p.name,
                str(p.path),
                f"[{health_style}]{p.health.value}[/{health_style}]",
                stack
            )

        self.console.print(table)
        return self.success(f"Found {len(projects)} projects.")

    def _conduct_switch(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 2] The Interactive Switch."""
        target = request.target

        # Interactive Selection if no target
        if not target and not request.non_interactive:
            projects = Observatory.list_projects()
            if not projects:
                return self.failure("No projects to switch to.")

            options = {str(i + 1): p for i, p in enumerate(projects)}

            self.console.print("[bold]Select a reality:[/bold]")
            for i, p in enumerate(projects):
                self.console.print(f"  [cyan]{i + 1}.[/cyan] {p.name} [dim]({p.path})[/dim]")

            choice = Prompt.ask("Choice", choices=list(options.keys()))
            target = options[choice].id

        if not target:
            return self.failure("Target required for switch.")

        entry = Observatory.switch(target)
        if entry:
            return self.success(f"Switched to '{entry.name}'.", data=entry.model_dump())

        return self.failure(f"Could not find project matching '{target}'.")

    def _conduct_active(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 10] The Active Gaze."""
        entry = Observatory.get_active()
        if not entry:
            return self.failure("No active project.")

        if request.json_mode:
            return self.success("Active project retrieved.", data=entry.model_dump())

        self.console.print(Panel(
            f"Name: [bold cyan]{entry.name}[/bold cyan]\n"
            f"Path: {entry.path}\n"
            f"ID:   {entry.id}\n"
            f"Git:  {entry.metadata.git_branch or 'N/A'}",
            title="[bold]Active Reality[/bold]",
            border_style="green"
        ))
        return self.success(f"Active: {entry.name}")

    def _conduct_discover(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 4] The Planetary Scanner."""
        from ...core.observatory.scanner import PlanetaryScanner

        root = Path.cwd()
        if request.target:
            root = (Path.cwd() / request.target).resolve()

        self.logger.info(f"Scanning for unmanaged realities in [cyan]{root}[/cyan]...")
        candidates = PlanetaryScanner.scan(root, max_depth=1)

        if not candidates:
            return self.success("No new realities found.")

        added_count = 0
        for path, ptype in candidates:
            # Check if already registered
            # Optimization: Logic inside Observatory.register handles duplication gracefully/updates
            # But we want to confirm with user if interactive

            should_add = True
            if not request.force and not request.non_interactive:
                should_add = Confirm.ask(f"Adopt [bold]{path.name}[/bold] ({ptype.value})?", default=True)

            if should_add:
                Observatory.register(str(path))
                added_count += 1

        return self.success(f"Adopted {added_count} new projects.")

    def _conduct_prune(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 3] The Ghost Exorcist."""
        state = Observatory.store.load()
        ghosts = []

        for pid, proj in state.projects.items():
            if not proj.path.exists():
                ghosts.append(pid)

        if not ghosts:
            return self.success("The Observatory is free of ghosts.")

        if request.force or Confirm.ask(f"Exorcise {len(ghosts)} missing projects from the registry?"):
            for pid in ghosts:
                del state.projects[pid]

            if state.active_project_id in ghosts:
                state.active_project_id = None

            Observatory.store.save(state)
            return self.success(f"Exorcised {len(ghosts)} ghosts.")

        return self.success("Pruning stayed.")

    def _conduct_health(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 5] The Health Dashboard."""
        Observatory.pulse()  # Force update
        return self._conduct_list(request)

    def _conduct_open(self, request: ObservatoryRequest) -> ScaffoldResult:
        """[FACULTY 8] The Launchpad."""
        entry = Observatory.get_active()
        if request.target:
            # Try to resolve target to a project
            # (Assuming switch logic or fuzzy find)
            # For V1, only open active or fail
            pass

        if not entry:
            return self.failure("No active project to open.")

        editor = os.getenv("EDITOR", "code")
        if "code" in editor or shutil.which("code"):
            subprocess.Popen(["code", str(entry.path)], shell=True)
            return self.success(f"Opened '{entry.name}' in VS Code.")

        return self.failure("Could not determine editor. Set $EDITOR or install VS Code.")