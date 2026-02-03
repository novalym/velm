# Path: artisans/distill/core/inquisitor/architectural.py
# -------------------------------------------------------

import re
from typing import List, Dict

from .....core.cortex.contracts import FileGnosis
from ...codex_of_anti_patterns import ARCHITECTURAL_GRIMOIRE


class ArchitecturalInquisitor:
    """
    =================================================================================
    == THE ARCHITECTURAL INQUISITOR (THE GUARDIAN OF PURITY)                       ==
    =================================================================================
    This divine artisan is summoned during the `distill` rite. It walks the complete,
    polyglot dependency graph forged by the Cortex and adjudicates it against the
    sacred laws inscribed in the `ARCHITECTURAL_GRIMOIRE`.

    Any scripture found committing a heresy (a forbidden import) will receive a
    massive relevance boost, and its `FileGnosis` vessel will be inscribed with a
    `heresy` tag. This ensures that architectural drift and anti-patterns are
    immediately brought to the Architect's attention in the final blueprint.
    =================================================================================
    """

    def __init__(self, dependency_graph: Dict[str, List[str]]):
        """
        The Inquisitor is born with the complete map of the cosmos.
        """
        self.graph = dependency_graph
        self.laws = [(key, re.compile(pattern), desc) for key, pattern, desc in ARCHITECTURAL_GRIMOIRE]

    def conduct_inquest(self, inventory_map: Dict[str, FileGnosis], file_scores: Dict[str, int]):
        """
        The Grand Rite of Adjudication.

        Walks the graph, applies the laws, and updates file scores and tags in-place.
        """
        for source_path, dependencies in self.graph.items():
            for target_path in dependencies:
                # We forge a string representing the bond for the regex to adjudicate.
                bond_string = f"{source_path} -> {target_path}"

                for key, pattern, description in self.laws:
                    if pattern.search(bond_string):
                        # A heresy has been perceived!
                        if source_path in inventory_map:
                            # Mark the sinner with a heresy tag.
                            sinner_gnosis = inventory_map[source_path]
                            if "heresy" not in sinner_gnosis.semantic_tags:
                                sinner_gnosis.semantic_tags.append("heresy")
                            if key not in sinner_gnosis.semantic_tags:
                                sinner_gnosis.semantic_tags.append(key)

                            # Bestow a massive relevance boost to draw the Architect's Gaze.
                            file_scores[source_path] = file_scores.get(source_path, 0) + 5000

