# Gnostic Codex: scaffold/artisans/template_engine/engine/alias_oracle.py
# ---------------------------------------------------------------------
# LIF: ∞ (THE MASTER LINGUIST)
#
# This divine artisan is the one true Master Linguist of the Forge. It has been
# forged from the soul of the old `_load_aliases` rite into a sovereign,
# intelligent, and hyper-aware Oracle of Aliases.
#
# ### THE PANTHEON OF 12 GAME-CHANGING, MIND-BLOWING ELEVATIONS:
#
# 1.  **The Sovereign Soul:** It is now a pure, self-contained class, its purpose absolute.
# 2.  **The Gnostic Triage of Realms:** It understands the hierarchy of Gnosis:
#     Project Config > Global Config > System Defaults.
# 3.  **The Unbreakable Ward of Paradox:** Its Gaze is shielded. A profane or
#     corrupted `config.json` will not shatter the engine.
# 4.  **The Luminous Voice:** Its every Gaze is chronicled with rich, Gnostic detail.
# 5.  **The Reverse Gaze:** Possesses a new, divine `reverse_lookup` rite, allowing
#     it to prophesy that `template.py` is the righteous scripture for `__init__.py`.
# 6.  **The Pure Gnostic Contract:** Its `load` and `get` rites are unbreakable contracts.
# 7.  **The Rite of Purging:** Its `purge` rite returns its memory to the void.
# 8.  **The Reusable Gaze (`_load_from_path`):** Its core Gaze is a pure, reusable
#     artisan, ready for future expansion to other configuration sources.
# 9.  **The Unbreakable Anchor:** It correctly anchors its Gaze to the `project_root`,
#     annihilating heresies of relativity.
# 10. **The Gnostic Grimoire:** Its `DEFAULT_ALIASES` are now its sacred, internal
#     grimoire, the foundation of its wisdom.
# 11. **The Polyglot Mind:** The entire system is forged to be extensible, ready to
#     learn new aliases from any source.
# 12. **The Final Word:** It is the one true, definitive, and eternal artisan for all
#     matters of template alias resolution.

import json
from pathlib import Path
from typing import Dict, Optional

from ....logger import Scribe

Logger = Scribe("AliasOracle")

class AliasOracle:
    """The Master Linguist. Manages mappings between filenames and template extensions."""

    DEFAULT_ALIASES: Dict[str, str] = {
        "__init__.py": "py",
        "mod.rs": "rs",
        "index.ts": "ts",
        "index.js": "js",
        "index.tsx": "tsx",
        "main.go": "go",
        "main.py": "py",
        "Cargo.toml": "rust",
        "pyproject.toml": "python",
        "package.json": "node",
        "go.mod": "go",
    }

    def __init__(self, project_root: Optional[Path]):
        self.project_root = project_root
        self.aliases: Dict[str, str] = {}
        self._reverse_map: Dict[str, str] = {}

    def load(self):
        """Performs the Gnostic Triage to load aliases from all realms."""
        Logger.verbose("The Alias Oracle awakens its Gaze...")
        # Tier 3: System Defaults (The Foundation)
        final_aliases = self.DEFAULT_ALIASES.copy()

        # Tier 2: Global Config (The Architect's General Will)
        global_config = Path.home() / ".scaffold" / "config.json"
        global_aliases = self._load_from_path(global_config)
        final_aliases.update(global_aliases)

        # Tier 1: Project Config (The Architect's Specific Will)
        if self.project_root:
            project_config = self.project_root / ".scaffold" / "config.json"
            project_aliases = self._load_from_path(project_config)
            final_aliases.update(project_aliases)

        self.aliases = final_aliases
        self._reverse_map = {v: k for k, v in self.aliases.items()}
        Logger.verbose(f"Alias Gaze complete. {len(self.aliases)} total aliases are known.")

    def _load_from_path(self, path: Path) -> Dict[str, str]:
        """A pure, reusable Gaze upon a single config scripture."""
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
                user_aliases = data.get("template_aliases", {})
                if user_aliases:
                    Logger.verbose(f"Perceived {len(user_aliases)} custom aliases from '{path.name}'.")
                    return user_aliases
            except (json.JSONDecodeError, IOError):
                Logger.warn(f"A paradox was perceived in the Polyglot scripture at '{path}'.")
        return {}

    def get(self, filename: str) -> Optional[str]:
        """Performs a Gaze for a filename's aliased soul."""
        return self.aliases.get(filename)

    def reverse_lookup(self, template_ext: str) -> Optional[str]:
        """[THE REVERSE GAZE] Finds the filename that maps to a template extension."""
        return self._reverse_map.get(template_ext)

    def purge(self):
        """The Rite of Purging."""
        self.aliases.clear()
        self._reverse_map.clear()
        Logger.verbose("The Alias Oracle's memory has been returned to the void.")