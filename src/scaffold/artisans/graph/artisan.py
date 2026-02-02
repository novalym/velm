# Path: scaffold/artisans/graph/artisan.py
# ----------------------------------------
from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.requests import GraphRequest
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan
from .cartographer import GnosticCartographer
from .architect import GnosticArchitect


@register_artisan("graph")
class GraphArtisan(BaseArtisan[GraphRequest]):
    """
    =================================================================================
    == THE TOPOLOGICAL CONDUCTOR (V-Ω-SINGULARITY)                                 ==
    =================================================================================
    The one true gateway for all Graph-based operations.
    It unifies Ingestion (Reading) and Manifestation (Writing).
    """

    def execute(self, request: GraphRequest) -> ScaffoldResult:
        project_root = Path(request.project_root or ".")

        # DECISION: ARE WE WRITING OR READING?
        if request.graph_data:
            # MOVEMENT I: THE HAND OF WILL (MANIFEST)
            # Transmute the Graph JSON back into files and directory structures.
            architect = GnosticArchitect(self.engine, project_root)
            return architect.manifest(request.graph_data, request.dry_run)

        # MOVEMENT II: THE OMNISCIENT GAZE (INGEST)
        # Scan the disk and build the JSON graph for the Cockpit.
        cartographer = GnosticCartographer(project_root)
        return cartographer.gaze(
            focus=request.focus,
            format=request.format,
            include_orphans=request.include_orphans
        )