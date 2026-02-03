# Path: scaffold/artisans/biome/analyst.py
# ----------------------------------------

import math
from pathlib import Path
from typing import List, Dict, Any

from ...core.cortex.engine import GnosticCortex
from ...core.cortex.knowledge import KnowledgeBase
from ...logger import Scribe

Logger = Scribe("GnosticBiologist")


class BiomeAnalyst:
    """
    =============================================================================
    == THE GNOSTIC BIOLOGIST (V-Ω-DATA-SYNTHESIZER)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Transmutes raw project data into Topographical Gnosis for 3D rendering.
    Calculates:
    - Mass (File Size) -> Footprint
    - Complexity (AST Nodes) -> Elevation
    - Churn (Git History) -> Temperature (Color)
    """

    def __init__(self, root: Path):
        self.root = root
        self.cortex = GnosticCortex(root)

    def analyze(self) -> Dict[str, Any]:
        """
        The Rite of Topography.
        Returns a hierarchical JSON structure ready for the Prismatic Lens.
        """
        Logger.info("Scanning the terrain of the sanctum...")

        # 1. Perceive Reality (Files & AST)
        memory = self.cortex.perceive()

        # 2. Perceive Time (Git History)
        # Ensure the Historian has gazed upon the timeline
        self.cortex.git_historian.inquire_all()

        biome_data = []
        max_complexity = 1
        max_churn = 1

        for item in memory.inventory:
            # We only map code, not binary artifacts
            if item.category not in ('code', 'config', 'doc_critical'):
                continue

            path_str = str(item.path).replace("\\", "/")

            # --- CALCULATE ELEVATION (Complexity) ---
            # Default to 1. If AST data exists, use cyclomatic complexity.
            complexity = 1
            if item.ast_metrics:
                complexity = item.ast_metrics.get("cyclomatic_complexity", 1)
                # Boost height for "God Files" (high function/class count)
                func_count = item.ast_metrics.get("function_count", 0)
                complexity += (func_count * 0.5)

            # --- CALCULATE TEMPERATURE (Churn) ---
            # Retrieve temporal gnosis from the Historian
            temporal = self.cortex.git_historian.inquire(item.path)
            churn = temporal.churn_score

            # Update global max for normalization
            max_complexity = max(max_complexity, complexity)
            max_churn = max(max_churn, churn)

            # --- FORGE THE CELL ---
            cell = {
                "path": path_str,
                "name": item.name,
                "folder": str(item.path.parent).replace("\\", "/"),
                "metrics": {
                    "complexity": complexity,
                    "churn": churn,
                    "size": item.original_size,
                    "age_days": temporal.age_days if hasattr(temporal, 'age_days') else 0,
                    "last_author": temporal.primary_author or "Unknown"
                },
                "language": item.language
            }
            biome_data.append(cell)

        Logger.success(f"Topography mapped. {len(biome_data)} structures identified.")

        return {
            "project": self.root.name,
            "stats": {
                "max_complexity": max_complexity,
                "max_churn": max_churn,
                "total_files": len(biome_data)
            },
            "cells": biome_data
        }