# Path: artisans/mimic/artisan.py
# -------------------------------

import time
import subprocess
import sys
import threading
from pathlib import Path
from rich.panel import Panel
from rich.live import Live

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import MimicRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write

from .reflector import TypeReflector
from .generator import MockServerForge


@register_artisan("mimic")
class MimicArtisan(BaseArtisan[MimicRequest]):
    """
    =================================================================================
    == THE SIMULACRUM (V-Ω-EPHEMERAL-REALITY-ENGINE)                               ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan is a Mirror. It gazes upon the static soul of a Type Definition
    (Pydantic/SQL/TS) and projects a living, breathing API into the mortal realm.
    """

    def execute(self, request: MimicRequest) -> ScaffoldResult:
        source_path = (self.project_root / request.source_path).resolve()
        if not source_path.exists():
            return self.failure(f"Source definition not found: {source_path}")

        self.logger.info(f"The Simulacrum awakens. Reflecting upon [cyan]{source_path.name}[/cyan]...")

        # 1. The Gnostic Reflection (Parse the Type)
        reflector = TypeReflector(source_path)
        schema_gnosis = reflector.reflect()

        if not schema_gnosis:
            raise ArtisanHeresy(f"The Simulacrum sees only void. Could not extract types from {source_path.name}.")

        self.logger.success(
            f"Perceived entity: [bold]{schema_gnosis['name']}[/bold] with {len(schema_gnosis['fields'])} fields.")

        # 2. The Materialization (Generate Server Code)
        forge = MockServerForge(framework=request.framework)
        server_code = forge.forge_server(schema_gnosis, request.port)

        # Write the ephemeral server
        mimic_dir = self.project_root / ".scaffold" / "mimic"
        mimic_dir.mkdir(parents=True, exist_ok=True)
        server_file = mimic_dir / f"mock_{schema_gnosis['name'].lower()}.py"

        atomic_write(server_file, server_code, self.logger, self.project_root)

        # 3. The Breathing of Life (Run Server)
        self.console.print(Panel(
            f"[bold green]Simulacrum Active[/bold green]\n"
            f"Endpoint: http://localhost:{request.port}/{schema_gnosis['name'].lower()}\n"
            f"Source:   {source_path.name}\n"
            f"Status:   Materialized",
            title="[magenta]The Ephemeral Mirror[/magenta]",
            border_style="magenta"
        ))

        # We run the server. If watch mode is on, we'd need a reloader.
        # For V1, we run the python script directly.
        try:
            # We use the current python executable to run the generated script
            # Ensure dependencies (fastapi, uvicorn, faker) are present.
            # We can use `scaffold run` logic here or subprocess.

            cmd = [sys.executable, str(server_file)]
            self.logger.info(f"Igniting process: {' '.join(cmd)}")

            # Allow the user to abort with Ctrl+C
            subprocess.run(cmd, check=True)

        except KeyboardInterrupt:
            self.logger.info("The Simulacrum fades into the ether.")
            return self.success("Simulation ended.")
        except Exception as e:
            raise ArtisanHeresy(f"The Simulacrum shattered: {e}")

        return self.success("Simulacrum cycle complete.")