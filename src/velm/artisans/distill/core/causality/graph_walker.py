# === [scaffold/artisans/distill/core/causality/graph_walker.py] - SECTION 1 of 1: The Graph Walker ===
import math
from collections import deque
from typing import Dict, Set, List, Tuple

from .....core.cortex.contracts import CortexMemory
from .....logger import Scribe
from .contracts import CausalityProfile, PropagationDirection, CausalNode, ImpactReport
from .constants import HUB_DEGREE_THRESHOLD, HUB_DAMPENING_FACTOR

Logger = Scribe("CausalGraphWalker")


class GraphWalker:
    """
    =================================================================================
    == THE WALKER OF WEBS (V-Ω-BFS-ALCHEMIST)                                      ==
    =================================================================================
    LIF: 100,000,000,000

    A stateless artisan that performs a Breadth-First Search (BFS) over the
    Gnostic Graph. It implements "Max-Pooling Logic": if a node is reached via
    multiple paths, it retains the highest relevance score.
    """

    def __init__(self, memory: CortexMemory, profile: CausalityProfile):
        self.memory = memory
        self.profile = profile

    def walk(self, seeds: List[str], base_scores: Dict[str, int]) -> ImpactReport:
        """
        The Grand Rite of Traversal.
        """
        # Map: Path -> CausalNode
        # Holds the state of the universe during the walk.
        universe: Dict[str, CausalNode] = {}
        hubs_found = set()

        # 1. Initialize the Queue with Seeds
        # Queue Item: (current_path, current_score, depth, direction)
        queue = deque()

        for seed in seeds:
            initial_score = base_scores.get(seed, 100)
            universe[seed] = CausalNode(path=seed, score=initial_score, depth=0, sources={seed})

            # We treat the seed as the center. We look both Up and Down.
            queue.append((seed, initial_score, 0, PropagationDirection.SEED))

        max_depth_reached = 0

        # 2. The BFS Loop
        while queue:
            curr_path, curr_score, depth, direction = queue.popleft()
            max_depth_reached = max(max_depth_reached, depth)

            if depth >= self.profile.max_depth:
                continue

            # Determine Neighbors based on Direction
            # If we are at a Seed, we look BOTH ways (if permitted).
            # If we are traveling Downstream (Dependencies), we usually keep going Downstream.
            # If we are traveling Upstream (Dependents), we usually keep going Upstream.

            next_steps: List[Tuple[str, PropagationDirection]] = []

            if direction == PropagationDirection.SEED:
                # [THE FIX] Check flags before exploding in directions
                if self.profile.include_dependencies:
                    for dep in self.memory.get_dependencies_of(curr_path):
                        next_steps.append((dep, PropagationDirection.DOWNSTREAM))

                if self.profile.include_dependents:
                    for dep in self.memory.get_dependents_of(curr_path):
                        next_steps.append((dep, PropagationDirection.UPSTREAM))

            elif direction == PropagationDirection.DOWNSTREAM:
                # Continue tracing dependencies (What does this need?)
                if self.profile.include_dependencies:
                    for dep in self.memory.get_dependencies_of(curr_path):
                        next_steps.append((dep, PropagationDirection.DOWNSTREAM))

            elif direction == PropagationDirection.UPSTREAM:
                # Continue tracing dependents (Who needs this?)
                if self.profile.include_dependents:
                    for dep in self.memory.get_dependents_of(curr_path):
                        next_steps.append((dep, PropagationDirection.UPSTREAM))

            # Process Neighbors
            for neighbor_path, next_dir in next_steps:
                neighbor_key = neighbor_path.replace('\\', '/')

                # Calculate Decay based on direction
                decay = (self.profile.dependency_decay
                         if next_dir == PropagationDirection.DOWNSTREAM
                         else self.profile.dependent_decay)

                # Hub Adjudication
                is_hub = self._is_hub(neighbor_key)
                if is_hub:
                    hubs_found.add(neighbor_key)
                    if self.profile.dampen_hubs:
                        decay *= HUB_DAMPENING_FACTOR

                new_score = int(curr_score * decay)

                # The Threshold of Existence
                if new_score < self.profile.min_threshold:
                    continue

                # The Max-Pooling Adjudication
                # If we've seen this neighbor before, only process if we found a STRONGER path.
                if neighbor_key in universe:
                    if new_score > universe[neighbor_key].score:
                        universe[neighbor_key].score = new_score
                        universe[neighbor_key].depth = min(universe[neighbor_key].depth, depth + 1)
                        # Re-queue to propagate the stronger signal
                        queue.append((neighbor_key, new_score, depth + 1, next_dir))
                else:
                    # New Discovery
                    universe[neighbor_key] = CausalNode(path=neighbor_key, score=new_score, depth=depth + 1)
                    queue.append((neighbor_key, new_score, depth + 1, next_dir))

        # 3. Forge the Report
        final_scores = {k: v.score for k, v in universe.items()}
        return ImpactReport(
            scores=final_scores,
            visited_count=len(universe),
            max_depth_reached=max_depth_reached,
            hubs_encountered=list(hubs_found)
        )

    def _is_hub(self, path: str) -> bool:
        """Decides if a node is a chaotic hub based on degree centrality."""
        # Check cached dependency graph degree
        # In-degree (Dependents) is usually the sign of a hub/utility.
        dependents = self.memory.get_dependents_of(path)
        return len(dependents) >= HUB_DEGREE_THRESHOLD