# Path: scaffold/artisans/aether/analyzer.py
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Set
from ...core.cortex.engine import GnosticCortex
from ...logger import Scribe

Logger = Scribe("AetherAnalyzer")


class PatternAnalyzer:
    """
    =============================================================================
    == THE PATTERN ANALYZER (V-Ω-SEMANTIC-ABSTRACTOR)                          ==
    =============================================================================
    Extracts the 'Gnostic DNA' of a project. It finds repeating structures,
    common dependency chains, and architectural skeletons.
    """

    def __init__(self, root: Path):
        self.root = root
        self.cortex = GnosticCortex(root)

    def extract_dna(self, privacy_level: int = 1) -> Dict[str, Any]:
        """
        Transmutes local code into anonymized architectural patterns.
        Level 1: Structural only (No code content).
        Level 2: Semantic (Logic flows + signatures).
        Level 3: Full (Reusable fragments).
        """
        memory = self.cortex.perceive()
        patterns = []

        for item in memory.inventory:
            if item.category != 'code': continue

            # Extract high-level topology
            dna = {
                "ext": item.path.suffix,
                "imports": list(item.imported_symbols),
                "complexity": item.ast_metrics.get("cyclomatic_complexity", 0),
                "tags": item.semantic_tags
            }

            if privacy_level >= 2:
                # Include class/function signatures without body
                dna["structure"] = item.ast_metrics.get("functions", []) + item.ast_metrics.get("classes", [])

            patterns.append(dna)

        return {
            "fingerprint": hashlib.sha256(str(patterns).encode()).hexdigest(),
            "patterns": patterns,
            "project_type": memory.inventory[0].language if memory.inventory else "unknown"
        }