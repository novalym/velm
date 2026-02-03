# Path: scaffold/artisans/muse/analyst.py
# ---------------------------------------

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter

from ...core.state.gnostic_db import GnosticDatabase, RiteModel, ScriptureModel
from ...logger import Scribe

Logger = Scribe("BehavioralAnalyst")


class BehavioralAnalyst:
    """
    =============================================================================
    == THE BEHAVIORAL ANALYST (V-Ω-MARKOV-CHAIN)                               ==
    =============================================================================
    LIF: 10,000,000,000

    Analyzes the causality of creation.
    "When the Architect creates A, they usually create B next."
    """

    def __init__(self, project_root: Path):
        self.db = GnosticDatabase(project_root)

    def prophesy_next(self, current_file: str, threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Predicts the next file creation based on the current context.
        """
        session = self.db.session
        try:
            # 1. Gather Creation Events
            # We look for all rites that involved creation.
            # We sort them by time to establish a causal sequence.
            all_rites = session.query(RiteModel).order_by(RiteModel.timestamp.asc()).all()

            creation_sequence = []
            for rite in all_rites:
                # Get files created in this rite
                created = [s.path for s in rite.scriptures_created]
                if created:
                    creation_sequence.extend(created)

            # 2. Build Markov Chain (Order 1)
            # Map: Context_Pattern -> Counter(Next_Pattern)
            # We use "patterns" (suffixes/stems) rather than exact paths to generalize.
            # e.g., "models.py" -> "service.py"
            transitions = defaultdict(Counter)

            for i in range(len(creation_sequence) - 1):
                current = self._abstract_path(creation_sequence[i])
                next_item = self._abstract_path(creation_sequence[i + 1])

                # Filter out self-loops (creating same type twice)
                if current != next_item:
                    transitions[current][next_item] += 1

            # 3. Query the Oracle
            context_pattern = self._abstract_path(current_file)
            Logger.verbose(f"Muse Context: '{current_file}' abstracted to '{context_pattern}'")

            candidates = transitions.get(context_pattern, Counter())
            total = sum(candidates.values())

            predictions = []
            for pattern, count in candidates.items():
                probability = count / total
                if probability >= threshold:
                    predictions.append({
                        "pattern": pattern,
                        "probability": probability,
                        "reason": f"Observed {count} times after '{context_pattern}'"
                    })

            return sorted(predictions, key=lambda x: x['probability'], reverse=True)

        finally:
            session.close()

    def _abstract_path(self, path_str: str) -> str:
        """
        Transmutes a concrete path into a semantic pattern.
        src/domain/user/model.py -> model.py
        src/api/auth.py -> api.py (if generic) or just suffix
        """
        # Heuristic 1: The Stem Suffix (e.g., _service.py, .controller.ts)
        p = Path(path_str)
        name = p.name

        # Check for common architectural suffixes
        suffixes = ['service', 'controller', 'repository', 'model', 'schema', 'dto', 'test', 'spec']
        for s in suffixes:
            if s in name.lower():
                return f"*{s}{p.suffix}"

        # Fallback: Just the extension or generic name
        if name in ['main.py', 'index.ts', 'App.tsx']:
            return name

        return f"*{p.suffix}"

