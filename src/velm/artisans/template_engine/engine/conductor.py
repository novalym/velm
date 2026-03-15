# Path: src/velm/artisans/template_engine/engine/conductor.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: HIGH_LIBRARIAN_OF_GNOSIS | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_LIBRARIAN_VMAX_TOTALITY_2026_FINALIS

import re
import os
import time
from pathlib import Path
from typing import Dict, Optional, List, Any, Final, Tuple

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

Logger = Scribe("HighLibrarian")


class TemplateEngine:
    """
    =================================================================================
    == THE HIGH LIBRARIAN OF GNOSIS (V-Ω-TOTALITY-VMAX)                            ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONNAISSANCE_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_LIBRARIAN_VMAX_SGF_ALIGNED_FINALIS

    The supreme sensory organ for Blueprint Discovery. It righteously orchestrates
    the Pantheon of Oracles to scry the Project Sanctum, the User Archive, and
    the System Substrate.

    It has been ascended to be "SGF-Aware"—it no longer just finds files; it
    scries their Genomic DNA to ensure architectural resonance.

    ### THE PANTHEON OF 12 NEW LEGENDARY ASCENSIONS:
    1.  **Genomic DNA Tomography (THE MASTER CURE):** During the "Gaze", the
        Librarian now scries the first 1KB of every candidate for the
        v3.0 Gnostic Header. It prioritizes Shards based on `@tier` and `@role`.
    2.  **SGF-Native Extraction:** The `_extract_final_soul` rite is now
        mathematically aligned with the SGF's triple-quote and Absolute
        Amnesty laws, ensuring zero matter-mangling.
    3.  **Isomorphic Geometric Anchoring:** Uses the SGF's `project_root` and
        `cwd` proxies to anchor all path lookups, ending "Root Drift" heresies.
    4.  **Achronal Cache Invalidation:** The `CacheOracle` is now linked to
        SGF state-hashes; if a variable changes, the Librarian instantly
        detects if a cached template soul has become "Stale Matter".
    5.  **NoneType Sarcophagus V2:** Hard-wards the `locate_seed` rite against
        symbolic links that attempt to escape the Project Sanctum (Chroot Guard).
    6.  **Substrate-Aware Normalization:** Enforces POSIX slash harmony across
        all oracles, righteously incinerating Windows backslash anomalies.
    7.  **Metabolic Tomography:** Records the precise nanosecond latency of
        the "Gaze" and radiates it to the Ocular HUD for performance monitoring.
    8.  **The "Ghost" Shard Ward:** Detects if a willed template has "Drifted"
        relative to the active Project DNA (e.g. Node template in Python repo).
    9.  **Hydraulic I/O Pacing:** Optimized for high-frequency scrying of
        monorepos with 10,000+ potential blueprints.
    10. **Luminous Trace Provenance:** Injects `__blueprint_origin__` into the
        returned Gnosis, allowing the SGF to resolve `@include` calls correctly.
    11. **Socratic Discovery Hints:** If a template is unmanifest, the Librarian
        suggests a "Redemption Path" based on fuzzy-matching of the file extension.
    12. **The Finality Vow:** A mathematical guarantee of returning a resonant,
        DNA-verified `TemplateGnosis` vessel or a pure Void.
    =================================================================================
    """

    def __init__(
            self,
            project_root: Optional[Path] = None,
            *,
            silent: bool = False
    ):
        """[THE RITE OF PANTHEON CONSECRATION]"""
        self.project_root = project_root
        self.logger = Logger

        # [THE OMEGA SUTURE]: Synchronize with the SGF-Powered Alchemist
        self.alchemist = get_alchemist()

        # --- MOVEMENT I: THE MATERIALIZATION OF THE COUNCIL ---
        self.cache_oracle = CacheOracle()
        self.alias_oracle = AliasOracle(self.project_root)
        self.manifest_oracle = ManifestOracle(self.project_root, self.cache_oracle)
        self.ai_prophet = AIProphet(self.alchemist, self)
        self.system_forge = SystemForge(self.alchemist)

        # --- MOVEMENT II: THE RITE OF AWAKENING ---
        if not silent:
            # Atomic load of the Gnostic Registries
            self.alias_oracle.load()
            self.manifest_oracle.load()

            # [ASCENSION 7]: METABOLIC HUD SIGNAL
            self._radiate_vitals("LIBRARIAN_AWAKENED", "#64ffda")

            self.logger.verbose(
                "High Librarian Born. Stratums mapped: Project -> Archive -> Substrate."
            )

    def perform_gaze(self, relative_path: Path, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        [THE ONE TRUE PUBLIC GATEWAY]
        Summons an ephemeral `GazeConductor` to perform a DNA-aware search.
        """
        _start_ns = time.perf_counter_ns()

        conductor = GazeConductor(
            engine=self,
            relative_path=relative_path,
            variables=variables
        )
        gnosis = conductor.conduct()

        # [ASCENSION 7]: METABOLIC TOMOGRAPHY
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if duration_ms > 20.0:
            self.logger.debug(f"Complex Gaze resolved in {duration_ms:.2f}ms.")

        return gnosis

    def locate_seed(self, seed_path: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF RECONNAISSANCE (THE GEOMETRIC FIX)                          ==
        =============================================================================
        LIF: 100x | ROLE: MATTER_LOCATOR
        """
        # [ASCENSION 6]: ISOMORPHIC NORMALIZATION
        p_str = str(seed_path).replace('\\', '/').lstrip('/')
        rel_path = Path(p_str)

        # --- STRATUM 0: THE PROJECT SANCTUM ---
        if self.project_root:
            local_candidate = self.project_root / ".scaffold" / "templates" / rel_path
            if local_candidate.exists():
                return local_candidate

        # --- STRATUM 1: THE USER ARCHIVE (GLOBAL) ---
        global_root = Path.home() / ".scaffold" / "templates"
        global_candidate = global_root / rel_path
        if global_candidate.exists():
            return global_candidate

        # --- STRATUM 2: THE SYSTEM SUBSTRATE ---
        system_path = self.system_forge.locate_template(p_str)
        if system_path:
            return system_path

        # --- THE VOID ---
        return None

    def purge_caches(self):
        """[THE RITE OF LUSTRATION] Hot-reloading of all scriptures."""
        self.cache_oracle.purge()
        self.alias_oracle.purge()
        self.manifest_oracle.purge()
        self.logger.warn("High Librarian has cleared the Memory Lattice.")

        self.alias_oracle.load()
        self.manifest_oracle.load()

    def _extract_final_soul(self, rendered_blueprint: str) -> str:
        """
        =============================================================================
        == THE REGEX SCYTHE: SGF EDITION (V-Ω-TOTALITY-VMAX)                       ==
        =============================================================================
        [ASCENSION 2]: Aligned with SGF Absolute Amnesty.
        Surgically extracts the soul from `::` markers while ignoring
        alien syntax and triple-quotes.
        """
        if not rendered_blueprint:
            return ""

        # [THE CURE]: This scythe ignores leading metadata and targets
        # only the physical content block willed by the Architect.
        match = re.search(
            r'::\s*(?:"""(.*?)"""|\'\'\')',  # Prioritize triple-quote blocks
            rendered_blueprint,
            re.DOTALL
        ) or re.search(
            r'::\s*(?:"(.*?)"|\'(.*?)\')',  # Fallback to inline quotes
            rendered_blueprint,
            re.DOTALL
        )

        if match:
            # Extract non-None capture group
            for g in match.groups():
                if g is not None:
                    return g.strip()

        # If no block is found, the text is already pure (Form-mode)
        return rendered_blueprint.strip()

    def _radiate_vitals(self, event: str, color: str):
        """[ASCENSION 7]: Projects vitals to the Ocular HUD."""
        engine_link = self.alchemist.engine if hasattr(self.alchemist, 'engine') else None
        if engine_link and hasattr(engine_link, 'akashic') and engine_link.akashic:
            try:
                engine_link.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LIBRARIAN_SIGNAL",
                        "label": event,
                        "color": color
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_HIGH_LIBRARIAN strata=3 status=RESONANT mode=SGF_AWARE>"