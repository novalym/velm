# Path: src/velm/artisans/template_engine/engine/conductor.py
# =========================================================================================
# == THE HIGH CONDUCTOR: OMEGA POINT (V-Ω-TOTALITY-V12.0-FINALIS)                        ==
# =========================================================================================
# LIF: INFINITY | ROLE: TEMPLATE_ORCHESTRATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_TEMPLATE_ENGINE_CONDUCTOR_2026_FINALIS
# =========================================================================================

import re
from pathlib import Path
from typing import Dict, Optional, List, Any

# --- THE DIVINE SUMMONS OF THE COMPLETE PANTHEON ---
from .cache_oracle import CacheOracle
from .alias_oracle import AliasOracle
from .manifest_oracle import ManifestOracle
from .ai_prophet import AIProphet
from .gaze_conductor import GazeConductor
from ..system_forge import SystemForge

from ..contracts import TemplateGnosis
from ....core.alchemist import get_alchemist
from ....logger import Scribe


Logger = Scribe("TemplateEngineConductor")


class TemplateEngine:
    """
    =================================================================================
    == THE GOD-ENGINE OF TEMPLATE ORCHESTRATION (V-Ω-TOTALITY-V12)                 ==
    =================================================================================
    The Supreme Conductor of the Forge. It orchestrates the Pantheon of Oracles to
    perceive the Architect's will and find the one true template across all
    dimensional strata.
    """

    def __init__(
            self,
            project_root: Optional[Path] = None,
            *,
            silent: bool = False
    ):
        """
        The Rite of Pantheon Forging.
        The Conductor is born and immediately materializes its complete council of specialists.
        """
        self.project_root = project_root
        self.logger = Logger
        self.alchemist = get_alchemist()

        # --- MOVEMENT I: THE FORGING OF THE PANTHEON OF ORACLES ---
        self.cache_oracle = CacheOracle()
        self.alias_oracle = AliasOracle(self.project_root)
        self.manifest_oracle = ManifestOracle(self.project_root, self.cache_oracle)
        self.ai_prophet = AIProphet(self.alchemist, self)

        # [ASCENSION 2]: THE CONSECRATION OF THE SYSTEM FORGE
        # The SystemForge is now a divine, first-class member of the Pantheon.
        self.system_forge = SystemForge(self.alchemist)
        # ★★★ THE PANTHEON IS WHOLE ★★★

        # --- MOVEMENT II: THE RITE OF AWAKENING (THE GNOSTIC GAZE) ---
        if not silent:
            self.alias_oracle.load()
            self.manifest_oracle.load()

        if not silent:
            self.logger.verbose(
                "The Template Engine High Conductor is online. The Pantheon is forged and complete."
            )

    def perform_gaze(self, relative_path: Path, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        [THE ONE TRUE PUBLIC GATEWAY]
        Summons an ephemeral `GazeConductor` to perform a specific, thread-safe lookup.
        """
        conductor = GazeConductor(
            engine=self,
            relative_path=relative_path,
            variables=variables
        )
        return conductor.conduct()

    def locate_seed(self, seed_path: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF RECONNAISSANCE (THE CORE FIX)                               ==
        =============================================================================
        LIF: 100x | ROLE: MATTER_LOCATOR

        [THE CURE]: This rite annihilates the AttributeError by providing a
        multi-strata path discovery engine. It gazes through three layers of
        reality to find the physical matter of a template.
        """
        # [ASCENSION 4]: GEOMETRIC PURIFICATION
        # Ensure we are working with a pure relative Path object
        p_str = str(seed_path).replace('\\', '/').lstrip('/')
        rel_path = Path(p_str)

        # --- STRATUM 0: THE PROJECT SANCTUM ---
        # Look within the local project structure first.
        if self.project_root:
            local_candidate = self.project_root / ".scaffold" / "templates" / rel_path
            if local_candidate.exists():
                self.logger.verbose(f"Lattice: Seed found in Project Sanctum: [dim]{rel_path}[/]")
                return local_candidate

        # --- STRATUM 1: THE USER ARCHIVE (GLOBAL) ---
        # Look within the Architect's global collection.
        global_root = Path.home() / ".scaffold" / "templates"
        global_candidate = global_root / rel_path
        if global_candidate.exists():
            self.logger.verbose(f"Lattice: Seed found in User Archive: [dim]{rel_path}[/]")
            return global_candidate

        # --- STRATUM 2: THE SYSTEM SUBSTRATE ---
        # [ASCENSION 3]: Delegate to the newly consecrated SystemForge
        # This reaches into the package's internal default_templates.
        system_path = self.system_forge.locate_template(p_str)
        if system_path:
            self.logger.verbose(f"Lattice: Seed found in System Substrate: [dim]{rel_path}[/]")
            return system_path

        # --- THE VOID ---
        return None

    def purge_caches(self):
        """
        [ASCENSION 5]: THE RITE OF UNIVERSAL PURGING
        Commands all oracles to return their memory to the void, enabling hot-reloading.
        """
        self.cache_oracle.purge()
        self.alias_oracle.purge()
        self.manifest_oracle.purge()

        self.logger.warn("All Template Engine caches have been returned to the void.")

        # Re-initialize to ensure fresh state
        self.alias_oracle.load()
        self.manifest_oracle.load()

    def _extract_final_soul(self, rendered_blueprint: str) -> str:
        """
        [THE LAW OF GNOSTIC STATE]
        This sacred, internal rite extracts the final, pure soul of a scripture
        by removing sigil markers and quotes.
        """
        match = re.search(
            r'::\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|"(.*?)"|\'(.*?)\'|(.+))',
            rendered_blueprint,
            re.DOTALL
        )
        if match:
            # We return the first non-None group found
            return next((g for g in match.groups() if g is not None), rendered_blueprint).strip()

        return rendered_blueprint

# == SCRIPTURE SEALED: THE HIGH CONDUCTOR HAS ACHIEVED TOTALITY ==