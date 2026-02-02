# Path: scaffold/artisans/weave/oracle.py
# ---------------------------------------

import importlib.resources as pkg_resources
from pathlib import Path
from typing import Set, Tuple, List, Dict

from rich.table import Table
from rich.panel import Panel

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe, get_console

Logger = Scribe("ArchetypeOracle")


class ArchetypeOracle:
    """
    The Seer of Archetypes. It performs the Tri-Fold Gaze to find the one true
    source of an architectural pattern.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        # The Three Sacred Sanctums
        self.local_forge = project_root / ".scaffold/archetypes"
        self.global_forge = Path.home() / ".scaffold/archetypes"
        self.system_forge_package = "scaffold.archetypes.genesis"

    def resolve_source(self, fragment_name: str) -> Tuple[Path, str]:
        """
        The Tri-Fold Gaze. Seeks the archetype in Local, then Global, then System.
        Returns (absolute_path, source_realm_name).
        """
        # Gaze 1: The Local Forge (Highest Precedence)
        local_path = self.local_forge / f"{fragment_name}.scaffold"
        if local_path.is_file():
            return local_path, "Local"

        # Gaze 2: The Global Forge
        global_path = self.global_forge / f"{fragment_name}.scaffold"
        if global_path.is_file():
            return global_path, "Global"

        # Gaze 3: The System Forge (The Engine's Soul)
        try:
            if pkg_resources.is_resource(self.system_forge_package, f"{fragment_name}.scaffold"):
                # We must materialize this ephemeral soul to a temporary file for the parser.
                # A future ascension could teach the parser to read from memory.
                with pkg_resources.path(self.system_forge_package, f"{fragment_name}.scaffold") as p:
                    return p, "System"
        except (ModuleNotFoundError, FileNotFoundError):
            pass  # The Gaze continues if the package is a void.

        raise ArtisanHeresy(f"Archetype '{fragment_name}' not found in any known Forge (Local, Global, System).")

    def list_all(self) -> Dict[str, str]:
        """Performs a Gaze upon all three realms and returns a unified map."""
        archetypes = {}
        # System
        try:
            for resource in pkg_resources.files(self.system_forge_package).iterdir():
                if resource.is_file() and resource.name.endswith('.scaffold'):
                    archetypes[resource.name.replace('.scaffold', '')] = "System"
        except (ModuleNotFoundError, FileNotFoundError):
            pass
        # Global (overwrites System if name collides)
        if self.global_forge.is_dir():
            for f in self.global_forge.glob("*.scaffold"):
                archetypes[f.stem] = "Global"
        # Local (highest precedence)
        if self.local_forge.is_dir():
            for f in self.local_forge.glob("*.scaffold"):
                archetypes[f.stem] = "Local"
        return archetypes

    def proclaim_dossier(self, archetypes: Dict[str, str]):
        """Forges the luminous Table of all known archetypes."""
        console = get_console()
        table = Table(title="[bold magenta]The Luminous Loom: Available Archetypes[/bold magenta]", box=None)
        table.add_column("Name", style="cyan")
        table.add_column("Source Realm", style="dim")

        for name, source in sorted(archetypes.items()):
            color = "white"
            if source == "Local": color = "bold green"
            if source == "Global": color = "yellow"
            table.add_row(name, f"[{color}]{source}[/{color}]")

        console.print(Panel(table, border_style="magenta"))