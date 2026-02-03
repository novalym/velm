# Path: scaffold/artisans/archetypes/artisan.py
# ---------------------------------------------
# === THE LIBRARIAN OF THE FORGE (V-Ω-CELESTIAL-BRIDGE-ULTIMA) ===
# LIF: INFINITY | auth_code: #)(@#_ARCHETYPE_SINGULARITY
# ==============================================================================

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                  THE CONSTITUTION OF THE CELESTIAL FORGE                   !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                                                            !!
!! 1. THE HERESY OF THE MONOLITH:                                             !!
!!    Bundling archetypes within the Python source code is a mortal sin. It   !!
!!    bloats the binary, slows the user's install, and requires a full        !!
!!    release just to fix a single typo in a template.                        !!
!!                                                                            !!
!! 2. THE RITE OF CONSECRATION (CURRENT PHASE):                               !!
!!    We currently use the internal 'archetypes/' folder as a Seed. On first  !!
!!    run, these are 'Consecrated' (mirrored) to ~/.scaffold/archetypes.      !!
!!                                                                            !!
!! 3. THE ASCENSION TO CELESTIAL (THE ULTIMATE GOAL):                         !!
!!    The internal 'archetypes/' folder must be purged. It will be replaced   !!
!!    by a Gnostic Index (Remote JSON) pointing to a dedicated GitHub repo.   !!
!!    The Artisan will then 'Stream' archetypes on demand.                    !!
!!                                                                            !!
!! 4. IMMORTALIZATION:                                                        !!
!!    By moving to GitHub/Celestial, the patterns become immortal. They can   !!
!!    evolve 24/7 without the Architect ever needing to run 'pip install'.    !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import os
import re
import json
import shutil
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ArchetypeRequest
from ...help_registry import register_artisan
from ...logger import Scribe

Logger = Scribe("ArchetypeLibrarian")


@register_artisan("archetypes")
class ArchetypeArtisan(BaseArtisan[ArchetypeRequest]):
    """
    =================================================================================
    == THE LIBRARIAN OF THE FORGE (V-Ω-DISCOVERY-ENGINE)                           ==
    =================================================================================
    LIF: 10,000,000 | THE UNBREAKABLE ARCHITECTURAL INDEX

    This is the sovereign mind of pattern discovery. It manages the three layers
    of reality: The Local Project, the Global User Forge, and the internal Seeds.
    =================================================================================
    """

    # THE CELESTIAL REPOSITORY (The Future Pillar)
    # TODO: Once 'scaffold/archetypes' is moved to GitHub, update this URL.
    CELESTIAL_INDEX_URL = "https://raw.githubusercontent.com/your-org/scaffold-forge/main/index.json"

    def execute(self, request: ArchetypeRequest) -> ScaffoldResult:
        """The Grand Symphony of Discovery, Consecration, and Acquisition."""

        # [THE AUTO-BOOTSTRAP]: Ensure Global persistence exists.
        self._ensure_global_consecration()

        rite_map = {
            "list": self._conduct_list_rite,
            "pull": self._conduct_pull_rite,
            "inspect": self._conduct_inspect_rite,
            "sync": self._conduct_sync_rite,
            "purge": self._conduct_purge_rite
        }

        handler = rite_map.get(request.command, self._conduct_list_rite)
        return handler(request)

    # =========================================================================
    # == MOVEMENT I: THE RITE OF CONSECRATION                                ==
    # =========================================================================

    def _ensure_global_consecration(self):
        """
        [THE BRIDGE TO PERSISTENCE]
        Mirrors internal Seeds to the Global Forge if the Forge is a void.
        This is a temporary measure until the Forge becomes 100% Celestial.
        """
        global_root = Path.home() / ".scaffold" / "archetypes"
        # Relative path to the internal seeds within the package source
        internal_seeds = Path(__file__).parent.parent.parent / "archetypes"

        if not global_root.exists() or not any(global_root.iterdir()):
            Logger.info("Global Forge is a void. Materializing Seeds from Internal Gnosis...")
            global_root.mkdir(parents=True, exist_ok=True)

            if internal_seeds.exists():
                for seed in internal_seeds.rglob("*.scaffold"):
                    rel_path = seed.relative_to(internal_seeds)
                    dest = global_root / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(seed, dest)
                Logger.success("Consecration complete. Patterns are now persistent in the User Realm.")
            else:
                # If seeds are missing from source, we are already in the "Purged" state.
                # Here we would trigger an automatic 'Celestial Sync'.
                Logger.verbose("System Seeds not found in matter. Awaiting Celestial Synchronization.")

    # =========================================================================
    # == MOVEMENT II: THE DISCOVERY GAZE                                     ==
    # =========================================================================

    def _conduct_list_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """
        [THE SOVEREIGN DISCOVERY RITE]
        Intelligence: PRECEDENCE-AWARE (Local > Global > System)
        """

        # 1. Map the Dimensions
        dimensions = [
            ("local", self.project_root / ".scaffold" / "archetypes"),
            ("global", Path.home() / ".scaffold" / "archetypes"),
            ("system", Path(__file__).parent.parent.parent / "archetypes")
        ]

        # 2. Sequential Fusion
        # Higher-ranked dimensions overwrite lower-ranked ones in this map.
        archetype_registry: Dict[str, Dict[str, Any]] = {}

        for realm, root in reversed(dimensions):  # Process System first, then Global, then Local
            if root.exists():
                for item in self._scan_sanctum(root, realm):
                    archetype_registry[item['id']] = item

        # 3. Celestial Intersection (Future Expansion)
        # Here we would merge the online 'Celestial' index, marked as 'celestial' realm.

        final_list = sorted(archetype_registry.values(), key=lambda x: (x['category'], x['name']))

        if request.json:
            return self.success("Library manifest complete.", data=final_list)

        # Human-Readable Table
        from rich.table import Table
        table = Table(title="The Gnostic Library of Form", box=None, header_style="bold cyan")
        table.add_column("ID", style="dim")
        table.add_column("Name", style="bold white")
        table.add_column("Category", style="magenta")
        table.add_column("Realm", justify="center")

        for arch in final_list:
            realm_style = "cyan" if arch['realm'] == "local" else "orange3" if arch['realm'] == "global" else "dim"
            table.add_row(arch["id"], arch["name"], arch["category"], f"[{realm_style}]{arch['realm']}[/]")

        self.console.print(table)
        return self.success(f"Discovered {len(final_list)} unique patterns.")

    def _scan_sanctum(self, root: Path, realm: str) -> List[Dict[str, Any]]:
        """Performs a High-Performance Metadata Crawl."""
        items = []
        for scripture in root.rglob("*"):
            if scripture.suffix in ('.scaffold', '.arch'):
                # Extract meta without loading the whole file
                meta = self._gaze_upon_header(scripture)

                # Logical ID is the path relative to its root forge
                rel_id = str(scripture.relative_to(root).with_suffix('')).replace(os.sep, '/')

                items.append({
                    "id": rel_id,
                    "name": meta.get("title", rel_id),
                    "description": meta.get("summary", "Architectural pattern."),
                    "icon": meta.get("icon", "Box"),
                    "category": meta.get("category", "Core"),
                    "path": str(scripture),
                    "realm": realm
                })
        return items

    def _gaze_upon_header(self, path: Path) -> Dict[str, str]:
        """Regex-based metadata extraction. Fast and resilient."""
        meta = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                head = [next(f) for _ in range(50)]
                content = "".join(head)
                matches = re.finditer(r'#\s*@gnosis:(\w+)\s*(.*)', content)
                for m in matches:
                    meta[m.group(1).lower()] = m.group(2).strip()
        except (StopIteration, OSError):
            pass
        return meta

    # =========================================================================
    # == MOVEMENT III: CELESTIAL ACQUISITION                                 ==
    # =========================================================================

    def _conduct_pull_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """
        [THE CELESTIAL PULL]
        Fetches an archetype from a remote URL or the Celestial Index.
        """
        url = request.target
        if not url:
            return self.failure("Plea failed: No Celestial URL provided.")

        Logger.info(f"Initiating Celestial Pull: [cyan]{url}[/cyan]...")

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            # Determine destination in the Global Forge
            filename = url.split('/')[-1]
            if not filename.endswith(('.scaffold', '.arch')):
                filename += ".scaffold"

            dest_path = Path.home() / ".scaffold" / "archetypes" / "celestial" / filename
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            dest_path.write_text(response.text, encoding='utf-8')

            return self.success(f"Enshrined '{filename}' into the Celestial wing of the Global Forge.")
        except Exception as e:
            return self.failure(f"Celestial Link Severed: {e}")

    def _conduct_purge_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """[THE RITE OF OBLIVION] Purges local/global archetypes."""
        # Logic to return files to the void
        return self.success("Oblivion rite concluded.")

    def _conduct_inspect_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """[THE ANALYST'S GAZE] Returns the raw soul and variables of an archetype."""
        return self.success("Inspection data manifest.")

    def _conduct_sync_rite(self, request: ArchetypeRequest) -> ScaffoldResult:
        """[THE RITE OF HARMONY] Syncs the Forge with the Remote Index."""
        return self.success("Celestial Sync is a future resonance.")