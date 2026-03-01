# Path: src/velm/artisans/ui/artisan.py
# -----------------------------------------------------------------------------------------
# == THE OMEGA UI CONDUCTOR (V-Ω-TOTALITY-V10000-PORT-HUNTER)                            ==
# =========================================================================================
# LIF: ∞ | ROLE: SOVEREIGN_HOST | RANK: OMEGA_SUPREME
# AUTH: Ω_UI_CONDUCTOR_V10000_FINALIS

import os
import sys
import time
import socket
import webbrowser
import threading
from pathlib import Path
from typing import Optional

from ...contracts.heresy_contracts import ArtisanHeresy

# [ASCENSION 1]: Lazy Imports for Zero-Latency CLI Boot
try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from fastapi.middleware.cors import CORSMiddleware

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

from .contracts import UIRequest
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan


@register_artisan("ui")
class UIArtisan(BaseArtisan[UIRequest]):
    """
    =============================================================================
    == THE OMEGA UI CONDUCTOR (V-Ω-TOTALITY-V10000-FINALIS)                    ==
    =============================================================================
    LIF: ∞ | ROLE: SOVEREIGN_HOST | RANK: OMEGA_SUPREME

    [ARCHITECTURAL CONSTITUTION]
    Materializes the Gnostic Workbench as a local, offline utility.
    It serves the static React shard forged by `forge_sovereign.py`.

    ### THE 12 ASCENSIONS:
    1.  **FastAPI SPA Routing:** Custom routing to ensure Next.js client-side
        routes do not return 404s when the browser is refreshed.
    2.  **Achronal Port Hunting:** Automatically scans for the next available TCP
        port if the willed port is occupied, annihilating 'Address in Use' crashes.
    3.  **Cross-Origin Resonance:** Injects CORS headers automatically so local
        extensions or scripts can commune with the UI if needed.
    4.  **Graceful Substrate Check:** Explicitly checks for FastAPI and provides
        the exact `pip install` command if missing.
    =============================================================================
    """

    def execute(self, request: UIRequest) -> ScaffoldResult:
        if not FASTAPI_AVAILABLE:
            return self.failure(
                "The UI Conductor requires the 'fastapi' and 'uvicorn' organs.",
                suggestion="Execute: `pip install fastapi uvicorn`"
            )

        # 1. GEOMETRIC TRIANGULATION
        # Resolve the location of the static Next.js shard
        base_pkg_dir = Path(__file__).resolve().parent.parent.parent
        static_dir = base_pkg_dir / "ui" / "static"

        # 2. VITALITY CHECK
        if not static_dir.exists() or not any(static_dir.iterdir()):
            return self.failure(
                "Ocular UI Shard Unmanifest.",
                suggestion="Run 'python scripts/forge_sovereign.py' to bake the React UI into the package."
            )

        # 3. ACHRONAL PORT HUNTING
        target_port = self._hunt_for_open_port(request.host, request.port)

        # 4. GATEWAY INCEPTION
        self.logger.info(f"Forging Gnostic Gateway on {request.host}:{target_port}...")
        app = self._forge_gateway(static_dir)

        # 5. ADRENALINE INJECTION
        if getattr(request, 'adrenaline', False):
            os.environ["SCAFFOLD_ADRENALINE"] = "1"

        # 6. THE OPENING OF THE APERTURE
        url = f"http://{'localhost' if request.host == '0.0.0.0' else request.host}:{target_port}"

        def _awaken_browser():
            time.sleep(1.5)  # Wait for Uvicorn to reach resonance
            if not getattr(request, 'no_browser', False):
                self.logger.verbose(f"Opening Aperture: {url}")
                webbrowser.open(url)

        threading.Thread(target=_awaken_browser, daemon=True).start()

        # 7. KINETIC IGNITION (UVicorn)
        self.console.print(f"\n[bold green]✨ VELM Sovereign Workbench Online[/bold green]")
        self.console.print(f"[dim]Locus:[/] [cyan]{url}[/]")
        self.console.print(f"[dim]Substrate:[/] IRON_LOCAL\n")
        self.console.print(f"[dim italic]Press Ctrl+C to collapse the reality and exit.[/dim italic]\n")

        try:
            uvicorn.run(
                app,
                host=request.host,
                port=target_port,
                log_level="warning",
                access_log=False
            )
        except KeyboardInterrupt:
            self.logger.system("Neural link severed. UI returning to void.")
        except Exception as e:
            return self.failure(f"Gateway Fracture: {e}")

        return self.success("Workbench session concluded gracefully.")

    def _hunt_for_open_port(self, host: str, start_port: int) -> int:
        """[ASCENSION 2]: Scries the network lattice for an open channel."""
        port = start_port
        while port < start_port + 100:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex((host, port)) != 0:
                    return port
            port += 1
        raise ArtisanHeresy("Metabolic Network Congestion: No open ports found.")

    def _forge_gateway(self, static_dir: Path) -> 'FastAPI':
        """
        [ASCENSION 1]: The Single Page Application (SPA) Router.
        Ensures that client-side routes (like /settings or /editor) resolve
        to the index.html file so React Router can take over.
        """
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from fastapi.middleware.cors import CORSMiddleware

        app = FastAPI(title="VELM Sovereign UI")

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Serve static assets (_next, css, js, wasm)
        app.mount("/_next", StaticFiles(directory=str(static_dir / "_next")), name="_next")

        if (static_dir / "wasm").exists():
            app.mount("/wasm", StaticFiles(directory=str(static_dir / "wasm")), name="wasm")

        # Catch-all Route for the React SPA
        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            # If the requested path is a real file (e.g. favicon.ico), serve it.
            requested_file = static_dir / full_path
            if requested_file.exists() and requested_file.is_file():
                return FileResponse(requested_file)

            # Otherwise, return the main React HTML shell
            return FileResponse(static_dir / "index.html")

        return app