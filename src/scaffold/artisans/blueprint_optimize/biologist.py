# Path: scaffold/artisans/blueprint_optimize/biologist.py
# -------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import Counter

from ...core.state.gnostic_db import GnosticDatabase, RiteModel, ScriptureModel
from ...logger import Scribe

Logger = Scribe("EvolutionaryBiologist")


class EvolutionaryBiologist:
    """
    =============================================================================
    == THE GENETICIST (V-Ω-STATISTICAL-INFERENCE)                              ==
    =============================================================================
    LIF: 10,000,000,000

    Analyzes the Gnostic Genome (History) to find dominant traits.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.db = GnosticDatabase(project_root)

    def analyze_evolution(self, blueprint_name: str, threshold: float) -> List[Dict[str, Any]]:
        """
        Scans history for a specific blueprint. Returns suggested mutations.
        """
        session = self.db.session
        suggestions = []

        try:
            # 1. Gather Genomes (Past Rites)
            # We look for rites where the blueprint_path matches.
            # Since RiteModel stores `blueprint_path` in provenance (inside JSON),
            # we must iterate or use a JSON query if supported.
            # For SQLite, we iterate python-side for flexibility.

            all_rites = session.query(RiteModel).all()
            relevant_rites = []

            for rite in all_rites:
                # Check provenance for blueprint match
                # (Assuming context_snapshot or a provenance field holds this)
                # In our schema, RiteModel has context_snapshot.
                # We also need to check if the rite actually used this blueprint.
                # Heuristic: We check if the rite created files that point to this blueprint origin.

                # Faster path: Check if we stored blueprint path in rite metadata
                # (We did in ProvenanceScribe).

                # Hack for V1: Just check if context has 'blueprint_path' matching
                ctx = rite.context_snapshot or {}
                if ctx.get("blueprint_path") == blueprint_name:
                    relevant_rites.append(rite)

            total_samples = len(relevant_rites)
            if total_samples < 3:
                Logger.info(f"Insufficient history ({total_samples} rites) for evolution. The species is too young.")
                return []

            # 2. Extract Alleles (Variable Values)
            variable_history: Dict[str, List[Any]] = {}

            for rite in relevant_rites:
                ctx = rite.context_snapshot or {}
                for key, val in ctx.items():
                    # Ignore internal system variables
                    if key.startswith("scaffold_") or key in ["project_root", "blueprint_path"]:
                        continue
                    # Ignore timestamps/dynamic values (heuristic)
                    if isinstance(val, (int, float)) and val > 1700000000:  # Timestamp check
                        continue

                    if key not in variable_history: variable_history[key] = []
                    variable_history[key].append(val)

            # 3. Adjudicate Dominance
            for key, values in variable_history.items():
                if len(values) < total_samples * 0.8:
                    # Variable wasn't present in enough runs to judge
                    continue

                # Serialize for counting (handle dicts/lists)
                str_values = [json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else str(v) for v in values]
                counts = Counter(str_values)
                most_common_val_str, count = counts.most_common(1)[0]
                frequency = count / len(values)

                if frequency >= threshold:
                    # We found a dominant trait!
                    # Deserialize back to python object
                    try:
                        suggestion_val = json.loads(most_common_val_str)
                    except:
                        suggestion_val = most_common_val_str
                        # Handle bools stored as strings
                        if suggestion_val == "True": suggestion_val = True
                        if suggestion_val == "False": suggestion_val = False

                    suggestions.append({
                        "key": key,
                        "current_dominance": frequency,
                        "suggested_default": suggestion_val,
                        "sample_size": len(values)
                    })

            return suggestions

        finally:
            session.close()