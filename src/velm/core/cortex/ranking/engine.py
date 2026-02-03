# Path: scaffold/artisans/distill/core/ranking/engine.py
# -----------------------------------------------------

import math
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Union
import re

# --- THE DIVINE SUMMONS ---
from ....core.cortex.contracts import FileGnosis, CortexMemory
from .strategies import MultiDimensionalStrategy, RankingWeights
from ....logger import Scribe

Logger = Scribe("SignificanceRanker")


class SignificanceRanker:
    """
    =================================================================================
    == THE HIGH PRIEST OF VALUE (V-Ω-ORPHAN-AMNESTY-ULTIMA)                        ==
    =================================================================================
    LIF: ∞ (THE ADJUDICATOR OF WORTH)

    This artisan judges the soul of every scripture. It assigns a `centrality_score`
    based on a multi-dimensional analysis of Topology, History, Semantics, and Intent.

    ### THE PANTHEON OF ASCENDED FACULTIES:

    1.  **The Orphan Amnesty:** Detects code files (`.py`, `.rs`) that have been
        disconnected from the graph and grants them a "Vitality Floor" score, ensuring
        they are never discarded as noise during the Governor's Census.
    2.  **The God-Ray (Focus):** If the Architect specifies `--focus`, those files
        receive an infinite score (10,000+), guaranteeing their `FULL` inclusion.
    3.  **The Gravity Wave:** Propagates value through the dependency graph. If a
        focused file imports X, then X gains mass.
    4.  **The Spatial Dampener:** Penalizes files if too many siblings from the same
        directory have already been ranked high, forcing the Governor to seek breadth
        (unless they are focused).
    5.  **The Keystone Recognition:** Automatically identifies and boosts critical
        project markers (`README`, `pyproject.toml`) regardless of graph connectivity.
    6.  **The Dynamic Persona:** Adjusts its weighting strategy based on the Architect's
        intent (e.g., "Bug Hunt" favors recency, "Onboarding" favors structure).
    """

    # The Grimoire of Vital Extensions (Files that inherently matter)
    VITAL_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java',
        '.cpp', '.c', '.h', '.rb', '.php', '.cs', '.swift', '.kt'
    }

    # The Grimoire of Vital Sanctums (Directories that imply code)
    VITAL_SANCTUMS = {'src', 'app', 'lib', 'core', 'internal', 'pkg', 'cmd'}

    def __init__(self, profile: Any, memory: CortexMemory, intent: str = "balanced"):
        self.profile = profile
        self.memory = memory
        # [FACULTY 6] The Dynamic Persona
        self.weights = self._divine_persona_by_name(intent) if isinstance(intent, str) else self._divine_persona(
            profile)
        self.strategy = MultiDimensionalStrategy(self.weights)

    def _divine_persona_by_name(self, intent: str) -> RankingWeights:
        """Selects the weighing logic based on the user's goal."""
        intent_lower = intent.lower()
        if 'bug' in intent_lower or 'debug' in intent_lower:
            return RankingWeights.FOR_BUG_HUNT()
        elif 'arch' in intent_lower or 'structure' in intent_lower:
            return RankingWeights.FOR_ARCHITECT()
        elif 'security' in intent_lower or 'audit' in intent_lower:
            return RankingWeights(semantic_match=10.0, complexity=2.0, recency=2.0)
        return RankingWeights()

    def _divine_persona(self, profile: Any) -> RankingWeights:
        """Extracts intent from the DistillationProfile."""
        return self._divine_persona_by_name(getattr(profile, 'name', 'balanced').lower())

    def rank(self, inventory: List[FileGnosis], context: Dict[str, Any] = None) -> List[FileGnosis]:
        """
        The Grand Rite of Valuation.
        """
        if context is None: context = {}
        ignore_terms = context.get('ignore', []) or []
        impact_scores = context.get('impact_scores', {})
        focus_terms = context.get('focus', [])

        scored_items: List[FileGnosis] = []
        scores: Dict[str, float] = {}

        # --- MOVEMENT I: THE BASE CALCULATION ---
        for file in inventory:
            path_str = file.path.as_posix()

            # 1. The Gaze of Aversion
            if any(term in path_str for term in ignore_terms):
                object.__setattr__(file, 'centrality_score', -1.0)
                continue

            # 2. The Algorithmic Assessment
            base_score = self.strategy.score(file, self.memory, context)

            # 3. The Keystone Boost
            # Docs and Configs that define the project get a static boost
            if file.name in ["README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "CONTEXT.md", "scaffold.lock"]:
                base_score += 20.0

            # 4. The Impact Injection (from Causal/Runtime analysis)
            if path_str in impact_scores:
                base_score += impact_scores[path_str]

            # 5. [FACULTY 1] THE ORPHAN AMNESTY
            # If the graph builder failed (orphans), code files usually drop to 0.
            # We enforce a "Vitality Floor" to ensure they are at least considered by the Governor.
            if base_score < 15.0:
                is_code = file.path.suffix.lower() in self.VITAL_EXTENSIONS
                in_core_dir = any(part in self.VITAL_SANCTUMS for part in file.path.parts)

                if is_code or in_core_dir:
                    base_score = 15.0  # Safe floor for "Summary" tier consideration
                    # self.logger.verbose(f"Amnesty granted to '{file.name}'")

            scores[path_str] = base_score

        # --- MOVEMENT II: THE PROPAGATION OF WAVES ---

        # 1. [FACULTY 3] The Gravity Wave (Topology)
        scores = self._apply_gravity_wave(scores)

        # 2. [FACULTY 2] The God-Ray (User Focus)
        if focus_terms:
            scores = self._apply_focus_boost(scores, focus_terms)

        # 3. [FACULTY 4] The Spatial Dampener (Diversity)
        scores = self._apply_spatial_diversity(scores)

        # --- MOVEMENT III: NORMALIZATION & ENSHRINEMENT ---

        max_score = max(scores.values()) if scores else 1.0
        if max_score == 0: max_score = 1.0

        for file in inventory:
            path_str = file.path.as_posix()
            raw_score = scores.get(path_str, 0.0)

            # If item matches focus exactly, force 100.0 (Absolute Priority)
            # Otherwise normalize relative to the max score found.
            is_focused = any(t in path_str for t in focus_terms)

            if is_focused:
                normalized = 100.0
            else:
                # We cap at 99.0 for non-focused items to preserve the sanctity of the 100.0 tier
                normalized = min(99.0, (raw_score / max_score) * 100.0)

            # Mutate the Immutable (Bypass Pydantic Freeze for Performance)
            object.__setattr__(file, 'centrality_score', normalized)

            # We include ALL non-ignored files. The Governor determines their fate (Tier).
            if raw_score >= 0:
                scored_items.append(file)

        # Sort: Highest Score First
        ranked = sorted(scored_items, key=lambda f: (-f.centrality_score, f.path.as_posix()))

        self._log_telemetry(ranked)
        return ranked

    def _apply_gravity_wave(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        [THE GRAVITY WAVE]
        If a file is important, the files it imports become important.
        """
        new_scores = scores.copy()
        for path, score in scores.items():
            if score <= 0: continue

            # Retrieve dependencies (files this path imports)
            deps = self.memory.get_dependencies_of(path)

            # Propagate 10% of the score to dependencies.
            # This ensures that if `main.py` is important, `utils.py` gets a boost.
            for dep in deps:
                if dep in new_scores:
                    new_scores[dep] += score * 0.10
        return new_scores

    def _apply_focus_boost(self, scores: Dict[str, float], focus_terms: List[str]) -> Dict[str, float]:
        """
        [THE GOD-RAY]
        Applies a massive, overriding boost to focused items and a strong ripple to their neighbors.
        """
        new_scores = scores.copy()

        # Pre-compile for speed
        # We check if the focus term is a substring of the path
        for path, score in scores.items():
            if any(term in path for term in focus_terms):
                # MASSIVE BOOST: This file is the center of the universe.
                # Base score set high enough to beat any normalization dampening.
                new_scores[path] = score + 10000.0

                # STRONG RIPPLE: Dependencies (What I need to work)
                for dep in self.memory.get_dependencies_of(path):
                    if dep in new_scores:
                        # +2000 is usually enough to guarantee SKELETON tier in the Governor
                        new_scores[dep] += 2000.0

                # MODERATE RIPPLE: Dependents (What uses me)
                for dept in self.memory.get_dependents_of(path):
                    if dept in new_scores:
                        new_scores[dept] += 500.0

        return new_scores

    def _apply_spatial_diversity(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        [THE SPATIAL DAMPENER]
        Prevents the context window from being flooded by 50 files from `utils/`.
        Reduces the score of files if their parent directory is already heavily represented.
        """
        dir_counts = defaultdict(int)
        new_scores = scores.copy()

        # Process high-scoring files first
        sorted_paths = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

        for path in sorted_paths:
            # Skip if score is massive (Focused items are immune to dampening)
            if scores[path] > 5000.0:
                continue

            directory = str(Path(path).parent)
            count = dir_counts[directory]

            # After 3 files from the same dir, decay the score by 10% for each subsequent file
            if count > 3:
                decay = 0.90 ** (count - 3)
                new_scores[path] *= decay

            dir_counts[directory] += 1

        return new_scores

    def _log_telemetry(self, ranked: List[FileGnosis]):
        if not ranked: return
        top = ranked[0]
        median_idx = len(ranked) // 2
        median = ranked[median_idx]

        Logger.info(
            f"Ranking Complete. "
            f"Top: [cyan]{top.path.name}[/] ({top.centrality_score:.1f}). "
            f"Median: [dim]{median.centrality_score:.1f}[/dim]"
        )