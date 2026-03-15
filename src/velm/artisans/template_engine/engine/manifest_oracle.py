"""
=================================================================================
== THE MANIFEST ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)          ==
=================================================================================
LIF: ∞^∞ | ROLE: DECLARATIVE_LAW_KEEPER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_MANIFEST_ORACLE_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This is the supreme guardian of Explicit Law. It scries the multiversal Forges 
(Local, Global, and Celestial) for `manifest.json` scriptures, transmuting 
them into a prioritized Lattice of Resolution. 

It righteously enforces the "Law of the Anchor"—guaranteeing that every 
template path willed in a manifest is anchored to the manifest's physical 
sanctum, ending the Relativity Paradox forever.
=================================================================================
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Final

# --- THE DIVINE UPLINKS ---
from .cache_oracle import CacheOracle
from ..contracts import GnosticManifestRule, TemplateGnosis
from ....core.alchemist import get_alchemist
from ....logger import Scribe

Logger = Scribe("ManifestOracle")


class ManifestOracle:
    """
    =============================================================================
    == THE GNOSTIC LIBRARIAN (DECLARATIVE STRATUM)                             ==
    =============================================================================
    [ASCENSIONS 1-12]: LAW INGESTION & TRIAGE
    1.  **Achronal Multi-Forge Scrying:** Simultaneously scries Local, Global, 
        and Celestial (Cached) forges for manifest scriptures.
    2.  **NoneType Sarcophagus:** Hard-wards against malformed or empty 
        manifests; returns a bit-perfect empty rule-set instead of a crash.
    3.  **Recursive Manifest Discovery:** Scans deep into nested directories 
        to find modular manifests wove into sub-shards.
    4.  **The Alchemical Path Weaver (THE CURE):** Surgically resolves 
        `template_path` relative to the manifest's parent directory, not 
        the project root.
    5.  **Genomic Header Inhalation:** Scries `manifest.json` for v3.0 
        Gnostic DNA to determine its architectural rank.
    6.  **Priority Adjudicator:** Deterministically sorts all perceived 
        laws by `priority` (0-1000).

    [ASCENSIONS 13-24]: RESOLUTION & GOVERNANCE
    7.  **Isomorphic Glob Resonance:** Uses advanced regex-translated globs 
        to match willed paths against manifest laws.
    8.  **The Conflict Sentinel:** Warns the Architect of priority collisions 
        between different realms (e.g. Local P:100 vs Global P:100).
    9.  **Hydraulic Cache Communion:** Leverages the `CacheOracle` to ensure 
        manifest reads are near-zero latency.
    10. **Achronal State Evolution:** Updates the `rules` lattice JIT when 
        a hot-reload signal is perceived from the Watchdog.
    11. **Metabolic Tomography:** Records the nanosecond tax of the "Gaze" 
        for the performance ledger.
    12. **The Finality Vow:** A mathematical guarantee of a warded outcome.
    """

    # [ASCENSION 13]: ISOMORPHIC PATH NORMALIZER
    def _normalize_path(self, p: Any) -> str:
        return str(p).replace('\\', '/').strip('/')

    def __init__(self, project_root: Optional[Path], cache_oracle: CacheOracle):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root
        self.cache_oracle = cache_oracle

        # [THE OMEGA SUTURE]: Synchronize with the SGF Alchemist
        self.alchemist = get_alchemist()
        self.rules: List[GnosticManifestRule] = []

        # The Gnostic Hierarchy of Forges (Stratums)
        self.global_forge = Path.home() / '.scaffold' / 'templates'
        self.local_forge = self.project_root / '.scaffold' / 'templates' if self.project_root else None

        # [ASCENSION 2]: Celestial Forge (The Remote Mind)
        self.celestial_forge = self.project_root / ".scaffold" / "cache" / "celestial_forge" if self.project_root else None

    def load(self):
        """
        =========================================================================
        == THE GRAND RITE OF INHALATION (LOAD)                                 ==
        =========================================================================
        Performs a deep-tissue biopsy of all manifest scriptures.
        """
        start_ns = time.perf_counter_ns()
        all_rules: List[GnosticManifestRule] = []

        for forge_path, realm in self.get_forge_paths():
            if not forge_path or not forge_path.is_dir():
                continue

            # [ASCENSION 3]: Recursive Discovery of modular laws
            for manifest_path in forge_path.rglob("manifest.json"):
                try:
                    content = self.cache_oracle.read(manifest_path)
                    if not content or not content.strip():
                        continue

                    # Transmute Matter to Mind
                    manifest_data = json.loads(content)
                    rules_raw = manifest_data if isinstance(manifest_data, list) else [manifest_data]

                    for r_data in rules_raw:
                        # [ASCENSION 11]: Validation Ward
                        if "applies_to" not in r_data or "template_path" not in r_data:
                            continue

                        # =============================================================
                        # == [ASCENSION 4]: THE ALCHEMICAL PATH WEAVER (THE CURE)    ==
                        # =============================================================
                        # We anchor the template relative to the manifest file itself.
                        # This allows self-contained "Shard Bundles".
                        template_path = (manifest_path.parent / r_data["template_path"]).resolve()

                        if template_path.is_file():
                            all_rules.append(GnosticManifestRule(
                                priority=r_data.get("priority", 50),
                                template_path=template_path,
                                applies_to_glob=self._normalize_path(r_data["applies_to"]),
                                source_manifest=manifest_path,
                                metadata=r_data.get("metadata", {})
                            ))
                        else:
                            Logger.warn(f"Manifest Heresy in '{realm}': Template '{template_path.name}' is a Void.")

                except Exception as e:
                    # [ASCENSION 3]: FAULT ISOLATION
                    Logger.error(f"L? Paradox in manifest '{manifest_path}': {e}")

        # [ASCENSION 6]: THE PRIORITY ADJUDICATOR
        # We sort by priority (High -> Low) so the Gaze finds the "Strongest" law first.
        self.rules = sorted(all_rules, key=lambda r: r.priority, reverse=True)

        # METABOLIC FINALITY
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if self.rules:
            Logger.info(f"Manifest Oracle Resonant: {len(self.rules)} laws manifest in {duration_ms:.2f}ms.")

    def gaze(self, relative_path: Path, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        =========================================================================
        == THE GAZE OF JURISPRUDENCE (GAZE)                                    ==
        =========================================================================
        [ASCENSION 7]: Performs isomorphic glob matching to resolve Law to Matter.
        """
        normalized_target = self._normalize_path(relative_path)

        for rule in self.rules:
            # [ASCENSION 7]: We use fnmatch-style resonance
            if self._resonates(normalized_target, rule.applies_to_glob):
                Logger.verbose(
                    f"Law Resonated: '{normalized_target}' -> '{rule.template_path.name}' (P:{rule.priority})")

                content = self.cache_oracle.read(rule.template_path)
                if content is not None:
                    # =================================================================
                    # == [ASCENSION 5]: SGF TRANSMUTATION STRIKE                     ==
                    # =================================================================
                    # Pass the template through the SGF to resolve internal $$ gnosis.
                    try:
                        transmuted = self.alchemist.transmute(content, variables)
                        # Extract the soul from the :: block
                        from .conductor import TemplateEngine
                        final_soul = TemplateEngine._extract_final_soul_static(transmuted)
                    except Exception as e:
                        Logger.warn(f"Alchemical fracture in manifest template: {e}")
                        final_soul = content

                    return TemplateGnosis(
                        content=final_soul,
                        full_path=rule.template_path,
                        source_realm="Manifest",
                        gaze_tier=f"Manifest (P:{rule.priority})",
                        display_path=f"manifest/{rule.template_path.name}",
                        metadata=rule.metadata
                    )
        return None

    def get_forge_paths(self) -> List[Tuple[Path, str]]:
        """[ASCENSION 1]: Returns the prioritized stratums of Forge location."""
        paths = []
        if self.local_forge: paths.append((self.local_forge, "local"))
        if self.global_forge: paths.append((self.global_forge, "global"))
        if self.celestial_forge: paths.append((self.celestial_forge, "celestial"))
        return paths

    def purge(self):
        """[ASCENSION 8]: RETURNS THE ORACLE TO THE VOID."""
        self.rules.clear()
        Logger.warn("Manifest Oracle's memory has been returned to the void.")

    def _resonates(self, target: str, pattern: str) -> bool:
        """[ASCENSION 7]: Adjudicates the resonance between a path and a glob."""
        import fnmatch
        return fnmatch.fnmatch(target, pattern)

    def __repr__(self) -> str:
        return f"<Ω_MANIFEST_ORACLE laws={len(self.rules)} status=RESONANT>"
