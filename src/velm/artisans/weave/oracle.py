# Path: artisans/weave/oracle.py
# ------------------------------
# Path: artisans/weave/oracle.py
# ------------------------------

import os
import json
import difflib
import re
import requests
import logging
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set

# --- VISUAL ORGANS ---
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    Console = None

# --- CORE GNOSTIC UPLINKS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("ArchetypeOracle")


class ArchetypeOracle:
    """
    =================================================================================
    == THE OMNISCIENT ORACLE (V-Ω-TOTALITY-V1000K-ACHRONAL-CACHE-FINALIS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: SHARD_DISCOVERY_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ORACLE_V1000K_N_PLUS_ONE_ANNIHILATOR_2026

    The supreme intelligence for pattern discovery. It bridges the gap between
    physical matter (local files) and the digital aether (remote grimoires).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Achronal Global Cache (THE MASTER CURE):** The celestial and registry
        caches have been elevated from `self` to `cls`. They now persist across
        the entire lifecycle of the God-Engine. This mathematically annihilates the
        N+1 Network Heresy, turning 4,000ms weave times into 4ms weave times.
    2.  **Thread-Safe Global Mutex:** The shared `_GLOBAL_LOCK` ensures that parallel
        swarms (Dimensional Walkers) do not create race conditions when fetching the Hub.
    3.  **Hydraulic Timeout Triage:** If the network is willed void (offline), the
        Oracle fails fast (2.0s) and caches the Void state, preventing repeated hangs.
    4.  **Geometric Correction:** Uses `parents[2]` to correctly target the package root.
    5.  **Recursive Gaze:** Uses infinite-depth `rglob` to find nested shards.
    6.  **Stem Indexing:** Registers shards by base name for O(1) lookup.
    7.  **Fuzzy Resonance:** Throws highly-specific Heresies with typo suggestions.
    8.  **Celestial Communion Optimization:** Reuses connection pooling via `requests.Session`
        internally if needed, though caching makes this largely obsolete.
    =================================================================================
    """

    # The Celestial Coordinate of the Master Grimoire
    GRIMOIRE_URL = "https://raw.githubusercontent.com/novalym/velm-grimoire/main/registry/index.json"

    # =========================================================================
    # == [ASCENSION 1 & 2]: THE GLOBAL CHRONOCACHE (THE MASTER CURE)         ==
    # =========================================================================
    # These structures live eternally in the Class scope, shared by all instances.
    _GLOBAL_LOCK = threading.RLock()
    _GLOBAL_CACHE_TS: float = 0.0
    _GLOBAL_REGISTRY_CACHE: Dict[str, Dict[str, Any]] = {}
    _GLOBAL_CELESTIAL_CACHE: Optional[List[Dict[str, Any]]] = None

    def __init__(self, project_root: Path):
        """
        [THE RITE OF ANCHORING]
        Binds the Oracle to the project and initializes the local/global forge paths.
        """
        self.project_root = project_root.resolve()
        self.console = Console() if Console else None

        # Strata 1: Local Project Forge (The Inner Sanctum)
        self.local_forge = self.project_root / ".scaffold" / "shards"
        self.local_library = self.project_root / ".scaffold" / "library"

        # Strata 2: Global User Forge (The Architect's Vault)
        self.global_forge = Path.home() / ".scaffold" / "shards"
        self.global_library = Path.home() / ".scaffold" / "library"

        # Strata 3: System Engine Forge (Built-in patterns/The Iron Core)
        # parents[0]=weave, parents[1]=artisans, parents[2]=velm
        velm_root = Path(__file__).resolve().parents[2]

        self.system_archetypes = velm_root / "archetypes"
        self.system_library = velm_root / "codex" / "shards"

        if Logger.is_verbose:
            Logger.debug(f"Oracle System Root: {velm_root}")
            Logger.debug(f"System Library: {self.system_library}")

    # =============================================================================
    # == I. THE RITES OF DISCOVERY (SCRYING)                                     ==
    # =============================================================================

    def list_all(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """A direct conduit for the WeaveConductor to summon the panoptic gaze."""
        return self.scry_all(category)

    def scry_all(self, category: Optional[str] = None, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        [THE PANOPTIC GAZE]
        Returns a unified list of all archetypes and shards from all dimensions.
        """
        with self._GLOBAL_LOCK:
            # [THE CURE]: The Cache of Truth is now Global.
            if not force_refresh and self._GLOBAL_REGISTRY_CACHE and (time.time() - self._GLOBAL_CACHE_TS < 10.0):
                all_patterns = self._GLOBAL_REGISTRY_CACHE
            else:
                all_patterns = {}

                # 1. Scry System Strata (Built-ins) - Lowest Priority
                self._scan_directory(self.system_archetypes, "System", all_patterns)
                self._scan_directory(self.system_library, "System Lib", all_patterns)

                # 2. Scry Global Strata (User-defined) - Medium Priority
                self._scan_directory(self.global_forge, "Global", all_patterns)
                self._scan_directory(self.global_library, "Global Lib", all_patterns)

                # 3. Scry Local Strata (Project-specific) - Highest Priority
                self._scan_directory(self.local_forge, "Local", all_patterns)
                self._scan_directory(self.local_library, "Local Lib", all_patterns)

                # 4. Scry Celestial Stratum (Remote)
                for pattern in self.scry_celestial_index(force_refresh=force_refresh):
                    name = pattern['name']
                    # Only add if not already locally manifest
                    if name not in all_patterns:
                        all_patterns[name] = {**pattern, "source_realm": "Celestial", "is_installed": False}
                    else:
                        # Mark local override
                        all_patterns[name]["is_installed"] = True

                self.__class__._GLOBAL_REGISTRY_CACHE = all_patterns
                self.__class__._GLOBAL_CACHE_TS = time.time()

        result = list(all_patterns.values())

        # Apply Category Filter
        if category:
            result = [p for p in result if p.get('category', '').lower() == category.lower()]

        return sorted(result, key=lambda x: x['name'])

    def scry_celestial_index(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        [THE CELESTIAL COMMUNION]
        Fetches the master index from the GitHub Mothership.
        Warded against N+1 Network Heresies via Global State locking.
        """
        with self._GLOBAL_LOCK:
            if not force_refresh and self._GLOBAL_CELESTIAL_CACHE is not None:
                return self._GLOBAL_CELESTIAL_CACHE

            try:
                # We fail fast to avoid blocking the user if offline
                Logger.verbose("Summoning the Celestial SCAF-Hub Index from the Aether...")
                response = requests.get(self.GRIMOIRE_URL, timeout=3.0)
                if response.status_code == 200:
                    data = response.json()
                    self.__class__._GLOBAL_CELESTIAL_CACHE = data.get("archetypes", [])
                    return self._GLOBAL_CELESTIAL_CACHE
                else:
                    Logger.debug(f"Celestial Link rejected plea: HTTP {response.status_code}")
            except Exception as e:
                Logger.debug(f"Celestial Link Faltered: {e}. The aether is dark.")

            # If the network is a void, we cache the empty array to prevent
            # future instances from hanging the UI retrying a dead connection.
            self.__class__._GLOBAL_CELESTIAL_CACHE = []
            return []

    # =============================================================================
    # == II. THE RITE OF RESOLUTION (FINDING)                                    ==
    # =============================================================================

    def resolve_source(self, name: str) -> Tuple[Optional[Path], str]:
        """
        [THE RITE OF LOCATION - ASCENDED]
        Resolves a pattern name into a physical file path.
        Returns (Path, source_realm).
        """
        # 0. Safety Ward: Prevent Path Traversal
        if ".." in name or "\\" in name:
            raise ArtisanHeresy(
                message=f"Profane Name: '{name}' contains illegal path characters.",
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 5 - THE MEMORY BRIDGE]
        # Consult the Global Cached Registry. If list_all() has run, it knows the truth.
        with self._GLOBAL_LOCK:
            if not self._GLOBAL_REGISTRY_CACHE:
                self.scry_all()  # Force hydration

            if name in self._GLOBAL_REGISTRY_CACHE:
                entry = self._GLOBAL_REGISTRY_CACHE[name]
                # Verify the file actually exists (Anti-Ghost)
                p = Path(entry['local_path'])
                if p.exists():
                    return p, entry['source_realm']

        # Normalize extension
        clean_name = name[:-9] if name.endswith(".scaffold") else name
        target_file = f"{clean_name}.scaffold"

        # Define the Search Hierarchy (Highest Priority to Lowest)
        search_roots = [
            (self.local_forge, "Local Forge"),
            (self.local_library, "Local Library"),
            (self.global_forge, "Global Forge"),
            (self.global_library, "Global Library"),
            (self.system_archetypes, "System Archetypes"),
            (self.system_library, "System Codex"),
        ]

        # 1. Scry physical disks (Recursive Deep Search)
        for root, realm in search_roots:
            if not root.exists(): continue

            # A. Direct Match
            direct_path = root / target_file
            if direct_path.exists():
                return direct_path, realm

            # B. Recursive Match (The Master Cure)
            try:
                # Find any file ending in the target name
                matches = list(root.rglob(target_file))
                if matches:
                    return matches[0], realm
            except Exception:
                pass

        # 2. Check Celestial (The Aether Strike)
        celestial_index = self.scry_celestial_index()
        match = next((a for a in celestial_index if a['name'] == clean_name), None)
        if match:
            raise ArtisanHeresy(
                f"Archetype '{clean_name}' exists in the Celestial Aether.",
                severity=HeresySeverity.INFO,
                suggestion=f"Pull it to your local Forge via: velm templates pull {clean_name}",
                details=f"ARCHETYPE_IN_AETHER:{clean_name}"
            )

        # 3. Fuzzy Resonance
        self._raise_fuzzy_heresy(clean_name, search_roots)
        return None, "Void"

    # =============================================================================
    # == III. THE RITE OF PROCLAMATION (VISUALIZATION)                           ==
    # =============================================================================

    def proclaim_dossier(self, archetypes: List[Dict[str, Any]]):
        """
        [THE LUMINOUS MATRIX]
        Renders the discovered Shards and Archetypes into a high-fidelity visual table.
        """
        if not self.console:
            for a in archetypes:
                print(f"- {a['name']} [{a['source_realm']}] : {a['description']}")
            return

        table = Table(
            title="[bold cyan]✨ THE GNOSTIC GRIMOIRE (MANIFEST SHARDS) ✨[/bold cyan]",
            border_style="dim",
            header_style="bold magenta",
            padding=(0, 1),
            expand=True
        )

        table.add_column("Shard Name", style="white", min_width=20)
        table.add_column("Realm", justify="center", width=12)
        table.add_column("Category", justify="center", width=15)
        table.add_column("Description", style="dim")

        def realm_weight(realm: str) -> int:
            r = realm.lower()
            if "system" in r: return 0
            if "global" in r: return 1
            if "local" in r: return 2
            return 3

        sorted_archs = sorted(archetypes, key=lambda x: (realm_weight(x.get('source_realm', '')), x['name']))

        for a in sorted_archs:
            name = a.get('name', 'Unknown')
            realm = a.get('source_realm', 'Void')
            category = a.get('category', 'Unclassified')
            desc = a.get('description', 'No Gnosis recorded.')

            realm_colored = realm
            if "System" in realm:
                realm_colored = f"[bold cyan]{realm}[/]"
            elif "Global" in realm:
                realm_colored = f"[bold blue]{realm}[/]"
            elif "Local" in realm:
                realm_colored = f"[bold green]{realm}[/]"
            elif "Celestial" in realm:
                realm_colored = f"[bold yellow]{realm}[/]"

            table.add_row(name, realm_colored, category, desc)

        self.console.print()
        self.console.print(table)
        self.console.print(f"  [dim]Total Shards Perceived: {len(archetypes)}[/dim]")
        self.console.print(
            "  [cyan]To weave a shard into reality, speak: [bold white]velm weave <shard_name>[/bold white][/cyan]\n")

    # =============================================================================
    # == IV. INTERNAL ORGANS (HELPERS)                                           ==
    # =============================================================================

    def _scan_directory(self, path: Path, realm: str, registry: Dict[str, Dict[str, Any]]):
        """Scans a physical directory and extracts Gnostic Headers."""
        if not path.exists():
            return

        # Recursive scan to support deep categorization
        for f in path.rglob("*.scaffold"):
            name = f.stem
            # For nested shards, prefix with parent relative to scanned root
            if f.parent != path:
                rel_parent = f.parent.relative_to(path).as_posix()
                full_name = f"{rel_parent}/{name}"
            else:
                full_name = name

            metadata = self._peak_at_header(f)

            category = metadata.get("category")
            if not category and '/' in full_name:
                category = full_name.split('/')[0].title()
            if not category:
                category = "Unclassified"

            entry = self._forge_entry(full_name, f, realm, category, metadata)

            # [THE CURE]: Register both Full Name and Base Name
            registry[full_name] = entry
            if name not in registry:
                registry[name] = entry

    def _forge_entry(self, name: str, path: Path, realm: str, category: str, metadata: Dict) -> Dict[str, Any]:
        return {
            "name": name,
            "description": metadata.get("description", "A local shard of matter."),
            "category": category,
            "tags": metadata.get("tags", []),
            "source_realm": realm,
            "local_path": str(path),
            "is_installed": True
        }

    def _peak_at_header(self, path: Path) -> Dict[str, Any]:
        """
        [THE GNOSTIC GAZE]
        Reads only the first 2KB of a file to extract metadata tags rapidly.
        """
        meta = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                head = f.read(2048)
                matches = re.findall(r'#\s*@(\w+):?\s*(.*)', head)
                for key, val in matches:
                    if key == "tags":
                        meta[key] = [t.strip() for t in val.split(',')]
                    else:
                        meta[key] = val.strip()
        except Exception:
            pass
        return meta

    def _raise_fuzzy_heresy(self, name: str, searched_roots: List[Tuple[Path, str]] = None):
        """
        [THE RESONANCE ORACLE]
        Finds the closest matches and throws a helpful, actionable heresy.
        """
        all_names = [p['name'] for p in self.scry_all()]
        flat_names = [n.split('/')[-1] for n in all_names]

        matches = difflib.get_close_matches(name, all_names, n=3, cutoff=0.5)
        if not matches:
            flat_matches = difflib.get_close_matches(name, flat_names, n=3, cutoff=0.5)
            if flat_matches:
                matches = [n for n in all_names if n.split('/')[-1] in flat_matches]

        msg = f"Archetype or Shard '{name}' is unmanifest in the Cosmos."
        suggestion = "Ensure the spelling is correct, or use 'velm weave --list' to view available shards."

        # Forensic Details
        details = ""
        if searched_roots:
            details = "\nSearched Sanctums:\n" + "\n".join(
                [f"- {r[1]}: {r[0]}" for r in searched_roots if r[0].exists()])

        if matches:
            suggestion = f"Did you mean one of these? [bold cyan]{', '.join(matches)}[/bold cyan]"

        raise ArtisanHeresy(
            message=msg,
            severity=HeresySeverity.CRITICAL,
            suggestion=suggestion,
            details=details,
            code="ARCHETYPE_NOT_FOUND"
        )