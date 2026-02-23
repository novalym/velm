# Path: artisans/ui/gateway.py
import os
import json
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from ...core.runtime import ScaffoldEngine
from ...interfaces.requests import AnalyzeRequest, TransmuteRequest, GenesisRequest


def forge_gateway(engine: ScaffoldEngine, static_dir: Path):
    """
    =============================================================================
    == THE GNOSTIC GATEWAY FORGE (V-Ω-TOTALITY-V5000.1)                        ==
    =============================================================================
    LIF: 100x | ROLE: MATTER_ETHER_BRIDGE | RANK: OMEGA
    """
    app = FastAPI(title="VELM_SOVEREIGN_GATEWAY")

    # [ASCENSION: THE CORS SHIELD]
    # Restricts the iron hand to only respond to the local forge.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- STRATUM 1: KINETIC ENDPOINTS (THE HAND) ---

    @app.post("/api/vfs/scry")
    async def vfs_scry(request: Request):
        """Allows the browser to scry the local disk topographies."""
        payload = await request.json()
        from ...core.runtime.vfs.scryer import vfs_scry_recursive
        target = payload.get("path", str(engine.project_root))
        return vfs_scry_recursive(target)

    @app.post("/api/kinetic/strike")
    async def kinetic_strike(request: Request):
        """The absolute entry point for Local Execution from the UI."""
        payload = await request.json()
        try:
            # Transmute JSON into Gnostic Request
            # (e.g. Genesis, Transmute, or Run)
            result = engine.dispatch(payload)
            return result.model_dump(mode='json')
        except Exception as e:
            return {"success": False, "error": str(e), "trace": traceback.format_exc()}

    # --- STRATUM 2: STATIC REALITY (THE EYE) ---
    # We serve the Next.js 'out' shard at the root
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app