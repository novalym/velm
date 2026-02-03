# scaffold/artisans/distill/core/analyzer/architectural.py

from typing import List, Dict, Set
from .....core.cortex.contracts import CortexMemory
from .....logger import Scribe

Logger = Scribe("ArchitecturalAnalyzer")


class ArchitecturalAnalyzer:
    """
    =============================================================================
    == THE GNOSTIC CARTOGRAPHER (V-Ω-ARCHITECTURAL-SUMMARIZER)                 ==
    =============================================================================
    Analyzes the Cortex Memory to produce a high-level summary of the project's
    architecture, patterns, and topology.
    """

    def __init__(self, memory: CortexMemory):
        self.memory = memory

    def summarize(self) -> str:
        """Produces a human-readable architectural summary."""
        lines = []

        # 1. Component Detection
        components = self._detect_components()
        if components:
            lines.append("# [Detected Components]")
            for name, desc in components.items():
                lines.append(f"# - {name}: {desc}")
            lines.append("")

        # 2. Dependency Flow
        layers = self._analyze_layers()
        if layers:
            lines.append("# [Dependency Flow]")
            lines.append(f"# {' -> '.join(layers)}")
            lines.append("")

        # 3. Key Entry Points
        entry_points = self._find_entry_points()
        if entry_points:
            lines.append("# [Entry Points]")
            for ep in entry_points:
                lines.append(f"# - {ep}")
            lines.append("")

        return "\n".join(lines)

    def _detect_components(self) -> Dict[str, str]:
        """Heuristic detection of architectural components."""
        components = {}
        # Naive implementation for V1
        for item in self.memory.inventory:
            path_str = str(item.path).lower()
            if "controller" in path_str: components["Controllers"] = "Handles incoming requests."
            if "service" in path_str: components["Services"] = "Business logic layer."
            if "model" in path_str or "entity" in path_str: components[
                "Models"] = "Data structures and database schema."
            if "repository" in path_str: components["Repositories"] = "Data access layer."
            if "view" in path_str or "component" in path_str: components["Views"] = "UI components."
        return components

    def _analyze_layers(self) -> List[str]:
        """Guesses the layering strategy."""
        # Simple check for common layered architecture names
        layers = []
        known_layers = ["api", "service", "core", "data", "db"]

        # Check which exist
        found_layers = set()
        for item in self.memory.inventory:
            for part in item.path.parts:
                if part.lower() in known_layers:
                    found_layers.add(part.lower())

        # Order them logically
        if "api" in found_layers: layers.append("API")
        if "service" in found_layers: layers.append("Service")
        if "core" in found_layers: layers.append("Core")
        if "data" in found_layers or "db" in found_layers: layers.append("Data")

        return layers

    def _find_entry_points(self) -> List[str]:
        """Finds likely entry points (main.py, index.ts, etc)."""
        candidates = ["main.py", "app.py", "index.ts", "index.js", "server.go", "main.rs"]
        found = []
        for item in self.memory.inventory:
            if item.path.name in candidates:
                found.append(str(item.path))
        return found