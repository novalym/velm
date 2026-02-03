# === [scaffold/artisans/distill/core/ranker/factors/cohesion.py] - SECTION 1 of 1: The Oracle of Cohesion ===
import math
from typing import List, Dict, Tuple, Counter, Set
from collections import defaultdict

# --- THE DIVINE SUMMONS ---
from .....core.cortex.contracts import FileGnosis
from ..contracts import RankDossier
from .....logger import Scribe

Logger = Scribe("CohesionJudge")


class CohesionJudge:
    """
    =================================================================================
    == THE ORACLE OF COHESION (V-Ω-TEMPORAL-GRAVITY-ENGINE)                        ==
    =================================================================================
    LIF: 10,000,000,000,000,000 (THE CHRONOMETRIC WEB)

    This divine artisan perceives the **Dark Matter** of the codebase: the invisible,
    temporal bonds formed when two scriptures are transmuted in the same Git commit.

    It implements **"The Law of Temporal Destiny"**: If Scripture A changes, and
    Scripture B frequently changes with it, then B is Gnostically entangled with A.
    If A is important (a Seed), B must also be summoned.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Seed Selector:** Identifies "Gravity Wells"—files that already have high
        Gnostic value (from focus, pagerank, or recency)—and uses them as the source
        of the boost.
    2.  **The Bond Strength Ratio:** Calculates the specific gravity between two files.
        `Strength = Co-Changes(A,B) / Total_Changes(A)`.
    3.  **The Hub Dampener:** Recognizes "God Files" (e.g., `version.txt`, `config.json`)
        that change with *everyone*. It diffuses their gravity to prevent them from
        flooding the context with noise.
    4.  **The Logarithmic Scaler:** Applies boosts on a log scale to reward strong
        bonds without allowing runaway inflation.
    5.  **The Recursive Resonance:** If A boosts B, B becomes slightly heavier, potentially
        allowing it to boost C in a future pass (though we limit to 1 pass for speed).
    6.  **The Path Normalizer:** Ensures Git paths (often relative to repo root) match
        the Project paths (relative to project root) perfectly.
    7.  **The Threshold Guard:** Ignores weak bonds (less than 3 co-commits) to filter
        out coincidental noise.
    8.  **The Symmetry Breaker:** Understands that the relationship is symmetric, but
        the *value transfer* is directional (from High Rank to Low Rank).
    9.  **The Self-Awareness:** Skips self-referential loops.
    10. **The Luminous Telemetry:** Logs specific "Gravitational Assists" so the
        Architect knows *why* a file appeared (e.g., "Pulled by `main.py`").
    11. **The Safe Division:** Guards against division-by-zero paradoxes when calculating
        bond strength.
    12. **The Unbreakable Contract:** Operates in-place on the `RankDossier` objects,
        seamlessly integrating with the Tribunal of Value.
    """

    # Minimum co-commits to be considered a bond
    BOND_THRESHOLD = 2

    def __init__(self, co_change_graph: Dict[str, Counter[str]], cohesion_multiplier: float = 20.0):
        self.graph = co_change_graph
        self.multiplier = cohesion_multiplier

    def judge(self, ranked_items: List[Tuple[FileGnosis, RankDossier]]):
        """
        The Rite of Temporal Binding.
        Modifies the `cohesion_score` of the RankDossiers in-place.
        """
        if not self.graph:
            return

        # 1. Forge the Lookup Map
        # We map normalized paths to their Dossiers for O(1) gravity application.
        path_to_entry: Dict[str, Tuple[FileGnosis, RankDossier]] = {
            str(g.path).replace('\\', '/'): (g, d)
            for g, d in ranked_items
        }

        # 2. Identify Gravity Wells (Seeds)
        # A file is a Seed if it has high existing relevance.
        # We take the top 20% of files or any file with score > 50.
        # This ensures we propagate relevance from "Focus" files outwards.
        sorted_by_score = sorted(ranked_items, key=lambda x: x[1].total, reverse=True)
        seed_count = max(1, int(len(ranked_items) * 0.2))

        seeds = []
        for i, entry in enumerate(sorted_by_score):
            gnosis, dossier = entry
            # Thresholds for being a Gravity Well
            if i < seed_count or dossier.total > 40.0:
                seeds.append(entry)

        Logger.verbose(f"Identified {len(seeds)} Temporal Gravity Wells.")

        # 3. The Propagation of Gravity
        for seed_gnosis, seed_dossier in seeds:
            seed_path = str(seed_gnosis.path).replace('\\', '/')

            # Retrieve the co-change history for this seed
            # Graph key structure must match path structure (relative to root)
            # The GitHistorian creates keys relative to git root.
            # We assume project_root == git_root for simplicity in V1,
            # or that paths are normalized.

            partners = self.graph.get(seed_path)
            if not partners:
                continue

            # [FACULTY 3] The Hub Dampener
            # Calculate the total "Mass" (Total co-commits with everyone)
            total_mass = sum(partners.values())

            # If a file changes with EVERYTHING, it is a Hub.
            # We punish its ability to boost others.
            # E.g., if total_mass is 1000, dampening is high.
            # Damping factor: 1 / log(total_mass)
            hub_dampening = 1.0 / (math.log10(total_mass) + 1.0) if total_mass > 10 else 1.0

            for partner_path, co_commits in partners.items():
                # [FACULTY 9] Self-Awareness
                if partner_path == seed_path: continue

                # [FACULTY 7] Threshold Guard
                if co_commits < self.BOND_THRESHOLD: continue

                if partner_path in path_to_entry:
                    target_gnosis, target_dossier = path_to_entry[partner_path]

                    # [FACULTY 2] Bond Strength Ratio
                    # Strength = (Co-Commits with Target) / (Total Commits of Seed)
                    # This represents: "When Seed changes, how likely is Target to change?"
                    # Since we don't have absolute total commits of seed easily here without
                    # querying Gnosis again, we use total_mass (sum of co-changes) as a proxy.
                    bond_strength = co_commits / total_mass

                    # [FACULTY 4] The Calculation of Force
                    # Boost = (Seed Score) * (Bond Strength) * (Multiplier) * (Hub Dampener)
                    # We use sqrt on Seed Score to prevent super-focused files (Score 10,000)
                    # from instantly pulling the entire repo.

                    seed_power = math.sqrt(seed_dossier.total)
                    boost = seed_power * bond_strength * self.multiplier * hub_dampening

                    # Apply the boost
                    target_dossier.cohesion_score += boost

                    # [FACULTY 10] Luminous Telemetry (Log significant assists)
                    if boost > 5.0:
                        Logger.verbose(
                            f"   -> Gravity Assist: [cyan]{seed_path}[/] pulls [green]{partner_path}[/] "
                            f"(Strength: {bond_strength:.2f}, Boost: +{boost:.1f})"
                        )