# Path: artisans/ui/artisan.py
import os
import sys
import time
import uvicorn
import webbrowser
import threading
from pathlib import Path
from .contracts import UIRequest
from .gateway import forge_gateway
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan


@register_artisan("ui")
class UIArtisan(BaseArtisan[UIRequest]):
    """
    =============================================================================
    == THE OMEGA UI CONDUCTOR (V-Ω-TOTALITY-V8000-FINALIS)                     ==
    =============================================================================
    LIF: ∞ | ROLE: SOVEREIGN_HOST | RANK: OMEGA_SUPREME
    AUTH: Ω_UI_CONDUCTOR_V8000_FINALIS

    [ARCHITECTURAL CONSTITUTION]
    Materializes the Gnostic Workbench as a local utility.
    It bridges the WASM Mind in the browser with the IRON Hand of the host OS.
    """

    def execute(self, request: UIRequest) -> ScaffoldResult:
        # 1. GEOMETRIC TRIANGULATION
        # Resolve the location of the static Next.js shard
        base_pkg_dir = Path(__file__).parent.parent.parent
        static_dir = base_pkg_dir / "ui" / "static"

        # 2. VITALITY CHECK
        if not static_dir.exists():
            return self.failure(
                "UI Shard Unmanifest.",
                suggestion="Run 'python scripts/forge_sovereign.py' to bake the UI into the package."
            )

        # 3. GATEWAY INCEPTION
        self.logger.info(f"Forging Gnostic Gateway on {request.host}:{request.port}...")
        app = forge_gateway(self.engine, static_dir)

        # 4. ADRENALINE INJECTION
        if request.adrenaline:
            os.environ["SCAFFOLD_ADRENALINE"] = "1"

        # 5. THE OPENING OF THE APERTURE
        url = f"http://{request.host}:{request.port}/velm/workbench/"

        def _awaken_browser():
            time.sleep(1.5)  # Wait for Uvicorn to resonate
            if not request.no_browser:
                self.logger.verbose(f"Opening Aperture: {url}")
                webbrowser.open(url)

        threading.Thread(target=_awaken_browser, daemon=True).start()

        # 6. KINETIC IGNITION (UVicorn)
        self.console.print(f"\n[bold green]✨ VELM Sovereign Workbench Online[/bold green]")
        self.console.print(f"[dim]Locus:[/] [cyan]{url}[/]")
        self.console.print(f"[dim]Substrate:[/] IRON_LOCAL\n")

        try:
            uvicorn.run(
                app,
                host=request.host,
                port=request.port,
                log_level="warning",
                access_log=False
            )
        except KeyboardInterrupt:
            self.logger.system("Neural link severed. UI returning to void.")
        except Exception as e:
            return self.failure(f"Gateway Fracture: {e}")

        return self.success("Workbench session concluded.")