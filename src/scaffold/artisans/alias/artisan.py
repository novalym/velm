# Path: scaffold/artisans/alias/artisan.py
# ----------------------------------------

import shlex
from rich.table import Table
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import AliasRequest
from ...help_registry import register_artisan
from ...settings.manager import SettingsManager


@register_artisan("alias")
class AliasArtisan(BaseArtisan[AliasRequest]):
    """
    =============================================================================
    == THE SHORTCUT FORGE (V-Ω-MACRO-MANAGER)                                  ==
    =============================================================================
    LIF: 10,000,000,000

    Manages the 'aliases' dictionary in the global config.
    """

    def execute(self, request: AliasRequest) -> ScaffoldResult:
        settings = SettingsManager(self.project_root)
        aliases = settings.get("aliases", {})

        cmd = request.alias_command

        if cmd == "list":
            if not aliases:
                return self.success("No aliases defined.")

            table = Table(title="Gnostic Aliases")
            table.add_column("Alias", style="cyan")
            table.add_column("Expansion", style="yellow")

            for k, v in aliases.items():
                table.add_row(k, v)

            self.console.print(table)
            return self.success(f"Listed {len(aliases)} aliases.")

        if not request.name:
            return self.failure("Alias name is required.")

        if cmd == "add":
            if not request.expansion:
                return self.failure("Expansion string is required for 'add'.")

            # Validate expansion syntax
            try:
                shlex.split(request.expansion)
            except ValueError as e:
                return self.failure(f"Invalid expansion syntax: {e}")

            aliases[request.name] = request.expansion
            settings.set_global("aliases", aliases)
            return self.success(f"Alias '{request.name}' -> '{request.expansion}' inscribed.")

        elif cmd == "remove":
            if request.name not in aliases:
                return self.failure(f"Alias '{request.name}' not found.")

            del aliases[request.name]
            settings.set_global("aliases", aliases)
            return self.success(f"Alias '{request.name}' annihilated.")

        return self.failure(f"Unknown rite: {cmd}")