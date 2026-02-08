# Path: src/velm/artisans/weave/oracle.py
# ----------------------------------------
# =========================================================================================
# == THE ARCHETYPE ORACLE (V-Ω-TOTALITY-V100.0-CELESTIAL-AWARE)                          ==
# =========================================================================================
# LIF: INFINITY | ROLE: PATTERN_DISCOVERY_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ORACLE_V100_TOTALITY_FINALIS
# =========================================================================================

import os
import json
import difflib
import requests
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set

# --- CORE GNOSTIC UPLINKS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ArchetypeOracle")


class ArchetypeOracle:
    """
    =================================================================================
    == THE OMNISCIENT ORACLE                                                       ==
    =================================================================================
    The supreme intelligence for pattern discovery. It bridges the gap between
    physical matter (local files) and the digital aether (remote grimoires).
    """

    # The Celestial Coordinate of the Master Grimoire
    GRIMOIRE_URL = "https://raw.githubusercontent.com/novalym/velm-grimoire/main/index.json"

    def __init__(self, project_root: Path):
        """
        [THE RITE OF ANCHORING]
        Binds the Oracle to the project and initializes the local/global forge paths.
        """
        self.project_root = project_root.resolve()

        # Strata 1: Local Project Forge
        self.local_forge = self.project_root / ".scaffold" / "archetypes"

        # Strata 2: Global User Forge
        self.global_forge = Path.home() / ".scaffold" / "archetypes"

        # Strata 3: System Engine Forge (Built-in patterns)
        self.system_forge = Path(__file__).parent.parent.parent / "archetypes"

        # Strata 4: The Celestial Cache
        self._celestial_cache: Optional[List[Dict[str, Any]]] = None

    # =============================================================================
    # == I. THE RITE OF DISCOVERY (SCRYING)                                      ==
    # =============================================================================

    def scry_all(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        [THE PANOPTIC GAZE]
        Returns a unified list of all archetypes from all four dimensions.
        """
        all_patterns: Dict[str, Dict[str, Any]] = {}

        # 1. Scry System Stratum (Built-ins)
        self._scan_directory(self.system_forge, "System", all_patterns)

        # 2. Scry Global Stratum (User-defined)
        self._scan_directory(self.global_forge, "Global", all_patterns)

        # 3. Scry Local Stratum (Project-specific)
        self._scan_directory(self.local_forge, "Local", all_patterns)

        # 4. Scry Celestial Stratum (Remote)
        for pattern in self.scry_celestial_index():
            name = pattern['name']
            if name not in all_patterns:
                all_patterns[name] = {**pattern, "source_realm": "Celestial", "is_installed": False}
            else:
                # If already local, mark it as installed
                all_patterns[name]["is_installed"] = True

        result = list(all_patterns.values())

        # Apply Category Filter
        if category:
            result = [p for p in result if p.get('category', '').lower() == category.lower()]

        return sorted(result, key=lambda x: x['name'])

    def scry_celestial_index(self) -> List[Dict[str, Any]]:
        """
        [THE CELESTIAL COMMUNION]
        Fetches the master index from the GitHub Mothership.
        """
        if self._celestial_cache is not None:
            return self._celestial_cache

        try:
            Logger.verbose(f"Scrying the Celestial Grimoire at {self.GRIMOIRE_URL}...")
            response = requests.get(self.GRIMOIRE_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self._celestial_cache = data.get("archetypes", [])
                return self._celestial_cache
        except Exception as e:
            Logger.warn(f"Celestial Link Faltered: {e}. The aether is dark.")

        self._celestial_cache = []
        return []

    # =============================================================================
    # == II. THE RITE OF RESOLUTION (FINDING)                                    ==
    # =============================================================================

    def resolve_source(self, name: str) -> Tuple[Path, str]:
        """
        [THE RITE OF LOCATION]
        Resolves a pattern name into a physical file path.
        Returns (Path, source_realm).
        """
        # 0. Safety Ward: Prevent Path Traversal
        if ".." in name or "/" in name or "\\" in name:
            raise ArtisanHeresy(f"Profane Name: '{name}' contains illegal path characters.")

        # 1. Check Local (Highest Priority)
        local_path = self.local_forge / f"{name}.scaffold"
        if local_path.exists():
            return local_path, "Local"

        # 2. Check Global
        global_path = self.global_forge / f"{name}.scaffold"
        if global_path.exists():
            return global_path, "Global"

        # 3. Check System
        system_path = self.system_forge / f"{name}.scaffold"
        if system_path.exists():
            return system_path, "System"

        # 4. Check Celestial (The Aether Strike)
        celestial_index = self.scry_celestial_index()
        match = next((a for a in celestial_index if a['name'] == name), None)
        if match:
            # We raise a specific code to tell the Conductor to pull the matter
            raise ArtisanHeresy(
                f"Archetype '{name}' exists in the Celestial Aether.",
                severity=HeresySeverity.INFO,
                fix_command=f"velm archetypes pull {name}",
                # CUSTOM_SIGNAL used by the Conductor
                details=f"ARCHETYPE_IN_AETHER:{name}"
            )

        # 5. Fuzzy Resonance (If all else fails)
        self._raise_fuzzy_heresy(name)

    # =============================================================================
    # == III. INTERNAL ORGANS (HELPERS)                                          ==
    # =============================================================================

    def _scan_directory(self, path: Path, realm: str, registry: Dict[str, Dict[str, Any]]):
        """Scans a physical directory and extracts Gnostic Headers."""
        if not path.exists():
            return

        for f in path.glob("*.scaffold"):
            name = f.stem
            metadata = self._peak_at_header(f)
            registry[name] = {
                "name": name,
                "description": metadata.get("description", "Local Artifact"),
                "category": metadata.get("category", "Unclassified"),
                "tags": metadata.get("tags", []),
                "source_realm": realm,
                "local_path": str(f),
                "is_installed": True
            }

    def _peak_at_header(self, path: Path) -> Dict[str, Any]:
        """
        [THE GNOSTIC GAZE]
        Reads only the first 2KB of a file to extract metadata tags.
        """
        meta = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                head = f.read(2048)
                # Look for # @key: value
                matches = re.findall(r'#\s*@(\w+):\s*(.*)', head)
                for key, val in matches:
                    if key == "tags":
                        meta[key] = [t.strip() for t in val.split(',')]
                    else:
                        meta[key] = val.strip()
        except Exception:
            pass
        return meta

    def _raise_fuzzy_heresy(self, name: str):
        """
        [THE RESONANCE ORACLE]
        Finds the closest matches and throws a helpful heresy.
        """
        all_names = [p['name'] for p in self.scry_all()]
        matches = difflib.get_close_matches(name, all_names, n=3, cutoff=0.6)

        msg = f"Archetype '{name}' is unknown in this galaxy."
        suggestion = "Check the spelling or run `velm archetypes sync`."

        if matches:
            suggestion = f"Did you mean one of these? [bold cyan]{', '.join(matches)}[/bold cyan]"

        raise ArtisanHeresy(
            msg,
            severity=HeresySeverity.CRITICAL,
            suggestion=suggestion,
            code="ARCHETYPE_NOT_FOUND"
        )

# == SCRIPTURE SEALED: THE ARCHETYPE ORACLE IS OMNIPOTENT ==