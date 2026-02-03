# Path: artisans/tutorial/engine.py
# ---------------------------------

from pathlib import Path
from typing import Dict, List, Any
from ...core.cortex.engine import GnosticCortex


class ThePedagogue:
    """
    The AI Curriculum Designer.
    Identifies key components and generates 'broken' versions of them for training.
    """

    def __init__(self, root: Path):
        self.root = root
        self.cortex = GnosticCortex(root)

    def design_curriculum(self, topic: str, difficulty: str) -> Dict[str, Any]:
        """
        Uses the Dependency Graph to find the 'Golden Path' of the application.
        """
        memory = self.cortex.perceive()

        # Heuristic: Find files with high Centrality Score
        candidates = sorted(memory.inventory, key=lambda x: x.centrality_score, reverse=True)

        # Filter by topic if provided (e.g. 'auth' -> match path)
        if topic:
            candidates = [c for c in candidates if topic in str(c.path)]

        quests = []
        for i, cand in enumerate(candidates[:5]):  # Top 5 relevant files
            if cand.category != 'code': continue

            quests.append({
                "id": f"quest_{i + 1}",
                "title": f"Mastering {cand.name}",
                "target_file": str(cand.path),
                "description": f"This file is critical to the architecture (Score: {cand.centrality_score:.1f}). It has been sabotaged. Restore it.",
                "objective": "Make the tests pass.",
                "difficulty": difficulty,
                # In a real impl, we'd use AST to identify a function to break
                "sabotage_target": "function:main"
            })

        return {
            "title": f"The Path of {topic or 'Mastery'}",
            "difficulty": difficulty,
            "quests": quests
        }