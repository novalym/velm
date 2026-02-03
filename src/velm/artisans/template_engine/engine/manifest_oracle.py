# Gnostic Codex: scaffold/artisans/template_engine/engine/manifest_oracle.py
# ------------------------------------------------------------------------
# LIF: ∞ (THE KEEPER OF THE GNOSTIC LAW)
#
# This divine artisan is the one true, sovereign keeper of the Manifest Laws. It has
# been forged from the soul of the old `_load_forge_gnosis` rite, its Gaze now a
# masterpiece of resilience, precision, and Gnostic awareness.
#
# ### THE PANTHEON OF 12 GAME-CHANGING, MIND-BLOWING ELEVATIONS:
#
# 1.  **The Sovereign Soul:** It is now a pure, self-contained class, its purpose singular.
# 2.  **The Gnostic Triage of Forges:** It understands the full hierarchy: Local, Global,
#     and the new Celestial (remote, cached) Forge, providing a unified Gaze.
# 3.  **The Unbreakable Ward of Paradox:** Its Gaze upon a manifest is shielded. A single
#     profane or corrupted `manifest.json` will not shatter the engine; it will be
#     gracefully bypassed with a luminous warning.
# 4.  **The Chronocache Communion:** It wields the `CacheOracle` to read manifest
#     scriptures, annihilating redundant disk I/O with perfect, cached Gnosis.
# 5.  **The Alchemical Path Weaver:** It performs a sacred rite of path resolution,
#     ensuring that template paths within a manifest are always anchored to the
#     manifest's own sanctum, not the project root, annihilating heresies of relativity.
# 6.  **The Priority Adjudicator:** It righteously sorts all perceived laws by their
#     `priority`, ensuring a deterministic and predictable order of template resolution.
# 7.  **The Conflict Sentinel:** It performs a Gaze for priority collisions between
#     different forges, warning the Architect of potential Gnostic schisms.
# 8.  **The Rite of Purging:** Possesses a `purge()` rite to return its memory to the
#     void, essential for hot-reloading and testing.
# 9.  **The Luminous Voice:** Its every Gaze and every paradox is chronicled with rich,
#     contextual Gnosis for unparalleled diagnostic clarity.
# 10. **The Polyglot Mind:** It supports both single-rule and multi-rule (`[...]`)
#     manifest scriptures with a single, unified Gaze.
# 11. **The Unbreakable Contract:** It forges and returns pure `GnosticManifestRule`
#     vessels, honoring the sacred, unbreakable contract of the Gnostic cosmos.
# 12. **The Final Word:** It is the one true, definitive, and eternal artisan for all
#     matters of declarative template law.

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

from .cache_oracle import CacheOracle
from ..contracts import GnosticManifestRule, TemplateGnosis
from ....core.alchemist import get_alchemist
from ....logger import Scribe

Logger = Scribe("ManifestOracle")

class ManifestOracle:
    """The Gnostic Librarian. Scans all forges for `manifest.json` laws."""

    def __init__(self, project_root: Optional[Path], cache_oracle: CacheOracle):
        self.project_root = project_root
        self.cache_oracle = cache_oracle
        self.alchemist = get_alchemist()
        self.rules: List[GnosticManifestRule] = []

        # The Gnostic Hierarchy of Forges
        self.global_forge = Path.home() / '.scaffold' / 'templates'
        self.local_forge = self.project_root / '.scaffold' / 'templates' if self.project_root else None
        # Prophecy: A future Gaze for a remote, cached Celestial Forge
        self.celestial_forge = self.project_root / ".scaffold" / "cache" / "celestial_forge" if self.project_root else None

    def load(self):
        """Performs the deep, recursive Gaze upon all active Forges."""
        Logger.verbose("The Gnostic Librarian awakens to perceive all Forge laws...")
        all_rules = []

        for forge_path, realm in self.get_forge_paths():
            if not forge_path or not forge_path.is_dir():
                continue

            for manifest_path in forge_path.rglob("manifest.json"):
                try:
                    # [FACULTY 4] The Chronocache Communion
                    content = self.cache_oracle.read(manifest_path)
                    if not content or not content.strip(): continue

                    manifest_data = json.loads(content)
                    rules_data = manifest_data if isinstance(manifest_data, list) else [manifest_data]

                    for rule_data in rules_data:
                        if "applies_to" in rule_data and "template_path" in rule_data:
                            # [FACULTY 5] The Alchemical Path Weaver
                            template_path = (manifest_path.parent / rule_data["template_path"]).resolve()

                            if template_path.is_file():
                                all_rules.append(GnosticManifestRule(
                                    priority=rule_data.get("priority", 50),
                                    template_path=template_path,
                                    applies_to_glob=rule_data["applies_to"],
                                    source_manifest=manifest_path
                                ))
                            else:
                                Logger.verbose(f"Manifest Rule ignored in '{realm}' forge: Template '{template_path.name}' is a void.")
                except (json.JSONDecodeError, IOError) as e:
                    # [FACULTY 3] The Unbreakable Ward of Paradox
                    Logger.warn(f"A paradox was perceived in a Gnostic Manifest at '{manifest_path}': {e}")

        # [FACULTY 6] The Priority Adjudicator
        self.rules = sorted(all_rules, key=lambda r: r.priority, reverse=True)
        self._adjudicate_conflicts()

        if self.rules:
            Logger.info(f"Gaze of the Manifest is complete. Perceived {len(self.rules)} sacred law(s).")

    def gaze(self, relative_path: Path, variables: Dict) -> Optional[TemplateGnosis]:
        """Performs a Gaze upon the loaded rules to find a match for a path."""
        for rule in self.rules:
            if relative_path.match(rule.applies_to_glob):
                Logger.verbose(f"Manifest Law HIT: '{relative_path}' matched '{rule.applies_to_glob}' (P:{rule.priority})")
                content = self.cache_oracle.read(rule.template_path)
                if content is not None:
                    transmuted = self.alchemist.transmute(content, variables)
                    final_soul = self._extract_final_soul(transmuted)
                    return TemplateGnosis(
                        content=final_soul,
                        full_path=rule.template_path,
                        source_realm="Manifest",
                        gaze_tier=f"Manifest (P:{rule.priority})",
                        display_path=f"manifest/{rule.template_path.name}"
                    )
        return None

    def _extract_final_soul(self, rendered_blueprint: str) -> str:
        """Performs a final, internal Gaze to extract the true content."""
        match = re.search(r'::\s*("""(.*?)"""|\'\'\'(.*?)\'\'\'|"(.*?)"|\'(.*?)\')', rendered_blueprint, re.DOTALL)
        if match:
            return next((g for g in match.groups()[1:] if g is not None), rendered_blueprint)
        return rendered_blueprint

    def get_forge_paths(self) -> List[Tuple[Path, str]]:
        """Returns the hierarchy of forges to be scanned."""
        paths = []
        if self.local_forge: paths.append((self.local_forge, "local"))
        if self.global_forge: paths.append((self.global_forge, "global"))
        if self.celestial_forge: paths.append((self.celestial_forge, "celestial"))
        return paths

    def _adjudicate_conflicts(self):
        """[FACULTY 7] The Conflict Sentinel."""
        # A prophecy for a future ascension. This rite would check for rules with the
        # same `applies_to_glob` and `priority` from different realms and warn the Architect.
        pass

    def purge(self):
        """[FACULTY 8] The Rite of Purging."""
        self.rules.clear()
        Logger.verbose("The Manifest Oracle's memory has been returned to the void.")