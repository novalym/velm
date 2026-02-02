# Path: scaffold/artisans/mri/artisan.py
# --------------------------------------

from typing import Dict, List, Set, Tuple
from pathlib import Path

from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import MRIRequest
from ...core.cortex.engine import GnosticCortex
from ...help_registry import register_artisan
from ...logger import Scribe

Logger = Scribe("ArchitecturalMRI")


@register_artisan("mri")
class MRIArtisan(BaseArtisan[MRIRequest]):
    """
    =============================================================================
    == THE ARCHITECTURAL MRI (V-Ω-STRUCTURAL-TOMOGRAPHY)                       ==
    =============================================================================
    Scans the dependency graph for Layer Violations.
    Enforces the One-Way Flow of Dependencies (The Onion Rule).
    """

    # The Default Clean Architecture Topography
    # Inner layers (0) cannot import Outer layers (3).
    # Outer layers MUST import Inner layers.
    DEFAULT_TOPOGRAPHY = {
        "domain": 0,  # Entities, Rules (Pure)
        "core": 1,  # Use Cases, Interfaces
        "service": 2,  # Application Logic
        "infra": 3,  # Database, API Clients, File I/O
        "api": 4,  # Controllers, Views
        "cmd": 4  # Entrypoints
    }

    def execute(self, request: MRIRequest) -> ScaffoldResult:
        self.logger.info("The MRI Machine spins up. Scanning structural integrity...")

        # 1. Perception
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()
        graph = memory.dependency_graph.get('dependency_graph', {})

        # 2. Topography Configuration
        # (Future: Load from .scaffold/mri.json)
        layers = self.DEFAULT_TOPOGRAPHY

        heresies: List[Dict] = []

        # 3. The Gaze of Structural Purity
        for source_file, dependencies in graph.items():
            source_layer = self._divine_layer(source_file, layers)
            if source_layer is None: continue

            for dep_file in dependencies:
                # Skip external imports (not in our file list usually, but graph might track them)
                if not dep_file.startswith(tuple(layers.keys())) and "src" not in dep_file:
                    continue

                dep_layer = self._divine_layer(dep_file, layers)
                if dep_layer is None: continue

                # THE LAW: Depend Inwards (Higher Layer -> Lower Layer) or Sideways (Same Layer).
                # Heresy: Lower Layer imports Higher Layer.
                if source_layer < dep_layer:
                    heresies.append({
                        "sinner": source_file,
                        "sin": dep_file,
                        "sinner_layer": self._get_layer_name(source_layer, layers),
                        "sin_layer": self._get_layer_name(dep_layer, layers)
                    })

        # 4. The Proclamation
        if not heresies:
            return self.success("The Architecture is Pure. No layer violations detected.")

        table = Table(title="[bold red]Structural Heresies Detected[/bold red]", border_style="red")
        table.add_column("Sinner (File)", style="cyan")
        table.add_column("Violation", style="white")
        table.add_column("Nature", style="red")

        for h in heresies:
            table.add_row(
                h['sinner'],
                f"Imports {h['sin']}",
                f"{h['sinner_layer']} (Inner) -> {h['sin_layer']} (Outer)"
            )

        self.console.print(table)

        return self.failure(
            f"MRI detected {len(heresies)} structural violations.",
            data={"heresies": heresies}
        )

    def _divine_layer(self, path: str, layers: Dict[str, int]) -> int:
        """Determines the layer of a file based on its path components."""
        parts = path.split('/')
        # Look for layer names in the path
        for part in parts:
            if part in layers:
                return layers[part]

        # Fallback mappings for common structures
        if "models" in parts or "entities" in parts: return 0  # Domain
        if "use_cases" in parts: return 1  # Core
        if "repositories" in parts: return 3  # Infra

        return None

    def _get_layer_name(self, rank: int, layers: Dict[str, int]) -> str:
        for name, r in layers.items():
            if r == rank: return name.upper()
        return "UNKNOWN"