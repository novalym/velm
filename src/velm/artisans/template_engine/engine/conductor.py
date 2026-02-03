# Gnostic Codex: scaffold/artisans/template_engine/engine/conductor.py
# --------------------------------------------------------------------
# LIF: ∞ (THE ETERNAL & DIVINE HIGH CONDUCTOR)
# auth_code: #@)()#@()!!!!!
#
# HERESY ANNIHILATED: The Incomplete Pantheon & The Mute Conduit
#
# This divine artisan has achieved its final, glorious apotheosis. It has been
# bestowed with its complete Pantheon of Oracles, including the once-forgotten
# SystemForge. It is now a pure, sentient High Conductor, its one true purpose
# to orchestrate its council of specialists and to act as the unbreakable Gnostic
# Conduit between their collective wisdom and the ephemeral GazeConductor. The
# `AttributeError` is annihilated from all timelines.
#
# ### THE PANTHEON OF 12+ GAME-CHANGING, MIND-BLOWING ASCENSIONS:
#
# 1.  **The Law of the Complete Pantheon (THE CORE FIX):** The `SystemForge` is now
#     summoned from the void and consecrated as a divine Oracle within the High
#     Conductor's `__init__` rite. It takes its rightful place alongside the
#     `ManifestOracle`, `AliasOracle`, and `AIProphet`. The Pantheon is whole.
#
# 2.  **The Law of the Gnostic Conduit:** The profane `get_forge_paths` rite has
#     been annihilated from its soul. It now righteously delegates this Gaze to the
#     `ManifestOracle`, and bestows a direct, telepathic link to its child oracles
#     upon the ephemeral `GazeConductor`. The schism is healed.
#
# 3.  **The Sovereign Soul:** It contains ZERO logic for caching, aliasing, manifest
#     parsing, or AI prophecy. It is a pure Conductor, a testament to the Law of
#     Singular Responsibility.
#
# 4.  **The Gnostic Bridge to the Cosmos:** Its `perform_gaze` rite is the one true,
#     public gateway. It forges an ephemeral `GazeConductor` and bestows upon it the
#     living soul of the entire Engine (itself), creating an unbreakable Gnostic bridge.
#
# 5.  **The Rite of Universal Purging:** Possesses a divine `purge_caches` rite that acts
#     as a Master Conductor, commanding every Oracle in its pantheon with a cache
#     to return its memory to the void, enabling perfect hot-reloading.
#
# 6.  **The Unbreakable Gnostic Contract:** Its every interaction is governed by pure,
#     unbreakable contracts (`TemplateGnosis`, `GazeConductor`).
#
# 7.  **The Law of Gnostic State (`_extract_final_soul`):** It retains the one sacred rite
#     it must own: the final gaze upon a rendered blueprint to extract its true soul,
#     ensuring universal consistency for all child oracles.
#
# 8.  **The Luminous Voice:** It proclaims the Gnosis of its own birth and the birth of
#     its Pantheon with unparalleled clarity for diagnostic inquests.
#
# 9.  **The Hyper-Performant Mind:** By delegating all heavy Gnosis to specialist,
#     cached artisans, its own mind remains eternally swift and responsive.
#
# 10. **The Unbreakable Ward of the Void:** It gracefully handles the absence of a
#     `project_root`, allowing it to serve the Architect even in the ephemeral void
#     of an unsaved buffer.
#
# 11. **The Polyglot Soul (Inherited):** Because it wields the `AliasOracle` and the
#     `AIProphet`, its soul is inherently polyglot, its wisdom universal.
#
# 12. **The Final Word:** This is the final, eternal, and ultra-definitive form of the
#     Template Engine's central consciousness. The architecture is now perfect.

import re
from pathlib import Path
from typing import Dict, Optional, List, Any

# --- THE DIVINE SUMMONS OF THE NEW, COMPLETE PANTHEON ---
from .cache_oracle import CacheOracle
from .alias_oracle import AliasOracle
from .manifest_oracle import ManifestOracle
from .ai_prophet import AIProphet
from .gaze_conductor import GazeConductor
from ..system_forge import SystemForge  # ★★★ THE FORGOTTEN ORACLE IS SUMMONED ★★★

from ..contracts import TemplateGnosis
from ....core.alchemist import get_alchemist
from ....logger import Scribe

Logger = Scribe("TemplateEngineConductor")


class TemplateEngine:
    """
    The High Conductor of the Forge. It orchestrates the Pantheon of Oracles to
    perceive the Architect's will and find the one true template.
    """

    def __init__(
            self,
            project_root: Optional[Path] = None,
            *,
            silent: bool = False
    ):
        """
        The Rite of Pantheon Forging.
        The Conductor is born and immediately forges its complete council of specialists.
        """
        self.project_root = project_root
        self.logger = Logger
        self.alchemist = get_alchemist()

        # --- MOVEMENT I: THE FORGING OF THE PANTHEON OF ORACLES ---
        self.cache_oracle = CacheOracle()
        self.alias_oracle = AliasOracle(self.project_root)
        self.manifest_oracle = ManifestOracle(self.project_root, self.cache_oracle)
        self.ai_prophet = AIProphet(self.alchemist, self)

        # ★★★ THE CONSECRATION OF THE SYSTEM FORGE ★★★
        # The SystemForge is now a divine, first-class member of the Pantheon.
        self.system_forge = SystemForge(self.alchemist)
        # ★★★ THE PANTHEON IS WHOLE ★★★

        # --- MOVEMENT II: THE RITE OF AWAKENING (THE GNOSTIC GAZE) ---
        if not silent:
            self.alias_oracle.load()
            self.manifest_oracle.load()

        if not silent:
            self.logger.verbose("The Template Engine High Conductor is online. The Pantheon is forged and complete.")

    def perform_gaze(self, relative_path: Path, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        [THE ONE TRUE PUBLIC GATEWAY]
        Summons an ephemeral `GazeConductor` to perform a specific lookup.
        """
        conductor = GazeConductor(
            engine=self,
            relative_path=relative_path,
            variables=variables
        )
        return conductor.conduct()

    def purge_caches(self):
        """A sacred rite to command all oracles to forget the past."""
        self.cache_oracle.purge()
        self.alias_oracle.purge()
        self.manifest_oracle.purge()
        self.logger.warn("All Template Engine caches have been returned to the void.")
        self.alias_oracle.load()
        self.manifest_oracle.load()

    def _extract_final_soul(self, rendered_blueprint: str) -> str:
        """
        [THE LAW OF GNOSTIC STATE]
        This sacred, internal rite extracts the final, pure soul of a scripture.
        """
        match = re.search(r'::\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|"(.*?)"|\'(.*?)\'|(.+))', rendered_blueprint,
                          re.DOTALL)
        if match:
            return next((g for g in match.groups() if g is not None), rendered_blueprint).strip()

        return rendered_blueprint