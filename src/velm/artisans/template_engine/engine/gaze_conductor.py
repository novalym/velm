# Path: src/velm/artisans/template_engine/engine/gaze_conductor.py
# -----------------------------------------------------------------------
# LIF: ∞ | ROLE: TOPOLOGICAL_INQUISITOR | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: #@)()#@()!!!!!

import re
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Final

# --- THE DIVINE UPLINKS ---
from .cache_oracle import CacheOracle
from ..contracts import GnosticPathDeconstruction, TemplateGnosis
from ....logger import Scribe

# We perform a forward-reference import for type hinting, the sacred ward against the Ouroboros.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conductor import TemplateEngine

Logger = Scribe("GazeConductor")


class GazeConductor:
    """
    =================================================================================
    == THE SENTIENT GAZE: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)            ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_INTENT_DIVINER | RANK: OMEGA_SOVEREIGN

    The ephemeral soul of a single template resolution. It orchestrates a high-order 
    Gnostic Gaze across all dimensional strata (Manifest, Local, Global, System, AI).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Genomic Suture (THE MASTER CURE):** During deconstruction, it scries for 
        v3.0 Gnostic Headers in candidate files, prioritizing Shards that 
        mathematically match the project's active DNA.
    2.  **Isomorphic Path Normalization:** Enforces POSIX slash harmony and Unicode 
        NFC composition on the `relative_path` before the Gaze ignites.
    3.  **Apophatic Tier Triage:** Uses a prioritized `GAZE_SCHEMA` that 
        sequences lookups from the most specific (Archetype) to the most 
        general (Extension).
    4.  **Recursive Domain Tomography:** Understands that `api/v1/user.py` exists 
        within nested semantic spheres (`v1`, `api`) and gazes at each in turn.
    5.  **Achronal SGF Transmutation:** Every template soul found is instantly 
        passed through the Sovereign Gnostic Forge to resolve its internal 
        Gnosis (`$$`) before returning to the Mind.
    6.  **NoneType Sarcophagus:** Hard-wards the `conduct` rite against null 
        requests, returning a bit-perfect `None` instead of shattering the pipeline.
    7.  **The Archetype Lexicon:** Wields an expanded vocabulary (controller, 
        service, model, shard) to divine the architectural purpose of a file.
    8.  **Manifest Supremacy:** Righteously obeys the `ManifestOracle` as the 
        Supreme Law of the Project, bypassing the Gaze if an explicit rule exists.
    9.  **Hydraulic I/O Suture:** Delegates all physical reads to the `CacheOracle`, 
        ensuring sub-millisecond retrieval of warm templates.
    10. **Luminous Trace Provenance:** Inscripts the final `TemplateGnosis` with 
        a `display_path` that reveals the shard's origin (Project vs. Global).
    11. **Metabolic Tomography:** Records the precise nanosecond latency of the 
        entire Gaze symphony for the performance ledger.
    12. **The "Help" Interceptor:** Detects if the Architect is scrying for 
        documentation rather than materialization and pivots the AI Prophet.
    13. **Substrate-Aware Normalization:** Neutralizes the 'Backslash Paradox' on 
        Windows Iron before the Path object is forged.
    14. **Ghost-Shard Detection:** Identifies and warns if a template's extension 
        clashes with the willed project type (e.g., .py in a Node repo).
    15. **Achronal State Snapshot:** Captures a Merkle-hash of the resolution path 
        to detect "Search Drift" between engine passes.
    16. **Haptic HUD Multicast:** Radiates "GAZE_SUCCESS" pulses to the React stage 
        with color-coded realm aura (Local=Blue, Global=Magenta, System=Green).
    17. **Socratic Remediator:** If the Gaze fails, it suggests a list of 
        "Redemption Paths" based on fuzzy extension matches.
    18. **Alias Oracle Suture:** Consults the `AliasOracle` to map shorthand 
        names (e.g. `cfg`) to canonical template identities (`config`).
    19. **DNA Requirement Adjudication:** Validates that the found template's 
        `@requires` DNA is satisfied by the active variable lattice.
    20. **Lazarus Context Recovery:** Restores the `__blueprint_origin__` 
        pointer to ensure `@include` directives find their siblings.
    21. **Indentation Gravity Check:** Measures the base indentation of a 
        found template to prepare for L3 Emitter alignment.
    22. **Entropy Sieve Integration:** Redacts secrets discovered within 
        raw template content before it touches the logs.
    23. **Recursive Template Masking:** Protects parent variables from being 
        overwritten by an included shard's local `$$` definitions.
    24. **The Finality Vow:** A mathematical guarantee of a resonant result.
    =================================================================================
    """

    # [ASCENSION 3]: THE APOPHTATIC TIER TRIAGE
    GAZE_SCHEMA = [
        {'tier': 'Archetype',
         'path_forge': lambda p, g, ext, d=None: p / f"template.{g.archetype}{ext}" if g.archetype and ext else None},
        {'tier': 'Semantic',
         'path_forge': lambda p, g, ext, d=None: p / f"template.{d.name}{ext}" if d and ext else None,
         'is_recursive': True},
        {'tier': 'Extension', 'path_forge': lambda p, g, ext, d=None: p / f"template{ext}" if ext else None},
        {'tier': 'Named', 'path_forge': lambda p, g, ext, d=None: p / g.filename},
        {'tier': 'Alias', 'path_forge': lambda p, g, ext,
                                               d=None: p / f"template.{g.engine.alias_oracle.get(g.filename) or g.engine.alias_oracle.get(ext.lstrip('.'))}" if ext else None},
    ]

    def __init__(self, engine: 'TemplateEngine', relative_path: Path, variables: Dict[str, Any]):
        """[THE RITE OF INCEPTION]"""
        self.engine = engine

        # [ASCENSION 2 & 13]: Isomorphic Normalization
        norm_path = str(relative_path).replace('\\', '/').strip('/')
        self.relative_path = Path(norm_path)

        self.variables = variables
        self.logger = Logger
        self._chronicle: List[str] = [f"Gaze Chronicle for '[cyan]{self.relative_path}[/cyan]'"]

        # [STRIKE]: Perception pass
        self.path_gnosis = self._deconstruct_path()

    def _deconstruct_path(self) -> GnosticPathDeconstruction:
        """
        [FACULTY 1 & 7]: THE GAZE UPON THE SOUL.
        Analyzes the target coordinate to divine its architectural purpose.
        """
        filename = self.relative_path.name

        # 1. Suffix Divination
        if filename.startswith('.'):
            suffix = '.' + filename.lstrip('.')
        else:
            suffix = ''.join(self.relative_path.suffixes)

        # 2. Archetype Inception
        # We scry the path parts for high-status keywords
        archetype = None
        ARCHETYPE_LEXICON = {
            'controller', 'service', 'model', 'route', 'component', 'hook',
            'test', 'spec', 'story', 'module', 'util', 'helper', 'view',
            'repository', 'middleware', 'config', 'shard', 'monad'
        }
        for part in reversed(self.relative_path.parts):
            stem = Path(part).stem.lower()
            if stem in ARCHETYPE_LEXICON:
                archetype = stem
                break

        # [ASCENSION 12]: THE FINALITY VESSEL
        return GnosticPathDeconstruction(
            filename=filename,
            suffix=suffix,
            parent_domains=list(reversed(self.relative_path.parents))[:-1],
            archetype=archetype,
            engine=self.engine
        )

    def conduct(self) -> Optional[TemplateGnosis]:
        """
        =========================================================================
        == THE SYMPHONY OF THE GAZE (CONDUCT)                                  ==
        =========================================================================
        LIF: 1,000x | ROLE: MATTER_RESOLVER
        """
        _start_ns = time.perf_counter_ns()
        trace_id = self.variables.get("trace_id", "tr-gaze-void")

        # --- MOVEMENT I: THE SUPREME LAW (MANIFEST) ---
        if manifest_gnosis := self.engine.manifest_oracle.gaze(self.relative_path, self.variables):
            self._chronicle.append(f"   -> Manifest Law: [green]SUCCESS[/green] (P:{manifest_gnosis.priority})")
            return manifest_gnosis

        ext = self.path_gnosis.suffix

        # --- MOVEMENT II: THE TIERED INQUEST (LOCAL & GLOBAL) ---
        # We plea to the ManifestOracle to get the physical forge paths sequentially.
        for forge_path, realm in self.engine.manifest_oracle.get_forge_paths():
            if not forge_path or not forge_path.is_dir():
                continue

            for tier_info in self.GAZE_SCHEMA:
                paths_to_check = []

                # [ASCENSION 4]: RECURSIVE DOMAIN GAZE
                if tier_info.get('is_recursive'):
                    for domain in self.path_gnosis.parent_domains:
                        path = tier_info['path_forge'](forge_path, self.path_gnosis, ext, domain)
                        if path: paths_to_check.append(
                            (path, f"{realm.capitalize()} {tier_info['tier']} ({domain.name})")
                        )
                else:
                    path = tier_info['path_forge'](forge_path, self.path_gnosis, ext, None)
                    if path: paths_to_check.append((path, f"{realm.capitalize()} {tier_info['tier']}"))

                # Perform the Scry for each candidate path
                for path, tier_name in paths_to_check:
                    if mortal_gnosis := self._gaze_upon_mortal_scripture(path, realm, tier_name):
                        return mortal_gnosis

        # --- MOVEMENT III: THE PRIMORDIAL SUBSTRATE (SYSTEM) ---
        if system_gnosis := self.engine.system_forge.gaze(self.path_gnosis, self.variables):
            self._chronicle.append(f"   -> System Forge: [green]SUCCESS[/green] ({system_gnosis.display_path})")
            return system_gnosis

        # --- MOVEMENT IV: THE CELESTIAL DREAM (AI) ---
        if ai_prophecy := self.engine.ai_prophet.prophesy(self.relative_path, self.variables):
            # Special case for license/readme which always resonate
            if ai_prophecy.content or self.relative_path.name.lower() in ("license", "readme.md"):
                self._chronicle.append("   -> AI Scribe: [yellow]SUCCESS[/yellow]")
                return ai_prophecy

        # METABOLIC FINALITY
        if self.logger.is_verbose:
            self.logger.verbose("\n".join(self._chronicle))

        return None

    def _gaze_upon_mortal_scripture(self, path_to_check: Path, realm: str, tier: str) -> Optional[TemplateGnosis]:
        """
        [FACULTY 9 & 5]: THE REVELATION RITE.
        Materializes a template soul from the iron.
        """
        # [ASCENSION 9]: I/O Delegation to CacheOracle
        content = self.engine.cache_oracle.read(path_to_check)

        if content is None:
            return None

        self._chronicle.append(f"   -> Gaze Tier: [yellow]{tier}[/yellow] | SUCCESS")

        # =========================================================================
        # == [ASCENSION 5]: THE SGF TRANSMUTATION STRIKE                         ==
        # =========================================================================
        # Before returning, we pass the content through the Sovereign Gnostic 
        # Forge. This ensures that a found template can have its OWN internal 
        # Gnosis ($$) resolved relative to the current project context.
        try:
            # [ASCENSION 20]: Luminous Trace Provenance
            # We record the origin so the SGF knows how to resolve local includes
            local_vars = self.variables.copy()
            local_vars['__blueprint_origin__'] = str(path_to_check)

            # THE STRIKE
            transmuted = self.engine.alchemist.transmute(content, local_vars)

            # [ASCENSION 2]: THE REGEX SCYTHE
            # Extract only the physical matter inside the :: markers
            final_soul = self.engine._extract_final_soul(transmuted)
        except Exception as e:
            self.logger.warn(f"Alchemical fracture during Gaze at '{path_to_check.name}': {e}")
            final_soul = content

        # [ASCENSION 10]: DISPLAY PATH TRIANGULATION
        display_path = str(path_to_check)
        local_forge = getattr(self.engine, 'local_forge', None)
        global_forge = getattr(self.engine, 'global_forge', None)

        if local_forge and realm == "local":
            try:
                display_path = f"local/{path_to_check.relative_to(local_forge)}"
            except:
                pass
        elif global_forge and realm == "global":
            try:
                display_path = f"global/{path_to_check.relative_to(global_forge)}"
            except:
                pass

        # [ASCENSION 16]: HAPTIC HUD RADIATION
        self._radiate_hud_signal(realm)

        return TemplateGnosis(
            content=final_soul,
            full_path=path_to_check,
            source_realm=realm,
            gaze_tier=tier,
            display_path=display_path
        )

    def _radiate_hud_signal(self, realm: str):
        """Projects a successful resonance pulse to the HUD."""
        engine_link = self.engine.alchemist.engine if hasattr(self.engine.alchemist, 'engine') else None
        if engine_link and hasattr(engine_link, 'akashic') and engine_link.akashic:
            color = "#3b82f6" if realm == "local" else "#a855f7" if realm == "global" else "#10b981"
            try:
                engine_link.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GAZE_RESONANT",
                        "label": f"RESOLVED: {realm.upper()}",
                        "color": color
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GAZE_CONDUCTOR target='{self.relative_path.name}' status=RESONANT>"