# Path: src/velm/genesis/genesis_profiles.py
# ------------------------------------------
"""
=================================================================================
== THE OMEGA REGISTRY (V-Ω-TOTALITY-V200-QUADRATIC-FUSION)                     ==
=================================================================================
LIF: ∞ | ROLE: ARCHETYPE_GOVERNOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_REGISTRY_V200_TOTALITY_FINALIS

The supreme conductor of Gnostic discovery. This artisan unifies four planes
of reality into a single, prioritized Grimoire, enabling the instantaneous
streaming and materialization of architectural patterns.
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Final

# --- THE GNOSTIC UPLINKS ---
from .canon_dna import GnosticDNAOracle

# --- LOGGING PROCLAMATION ---
try:
    from ..logger import Scribe

    Logger = Scribe("GnosticRegistry")
except ImportError:
    Logger = logging.getLogger("GnosticRegistry")

# =============================================================================
# == THE PHYSICAL ANCHORS (THE FOUR REALMS)                                  ==
# =============================================================================

# I. SYSTEM CORE (The Primordial Seeds)
SYSTEM_DIR: Final[Path] = Path(__file__).parent.parent / "archetypes"

# II. GLOBAL FORGE (The User's Universal Library)
GLOBAL_DIR: Final[Path] = Path.home() / ".scaffold" / "archetypes"

# III. LOCAL SANCTUM (The Project's Private Logic)
LOCAL_DIR: Final[Path] = Path.cwd() / ".scaffold" / "archetypes"

# IV. CELESTIAL CACHE (The Local Echo of the Cloud Index)
CELESTIAL_CACHE: Final[Path] = Path.home() / ".scaffold" / "celestial_index.json"

DEFAULT_PROFILE_NAME: Final[str] = "python-basic"


class ArchetypeRegistry:
    """
    The Singleton Mind of the Registry.
    Performs the Quadratic Fusion of all known architectural strata.
    """
    _cache: Dict[str, Dict[str, Any]] = {}
    _last_scan_time: float = 0.0
    _scan_ttl: float = 2.0  # Metabolic cooldown

    @classmethod
    def refresh(cls) -> Dict[str, Dict[str, Any]]:
        """
        =============================================================================
        == THE RITE OF QUADRATIC FUSION (REFRESH)                                  ==
        =============================================================================
        LIF: 100x | Scans all four strata and weaves them into the Unified Grimoire.
        """
        now = time.time()
        if cls._cache and (now - cls._last_scan_time < cls._scan_ttl):
            return cls._cache

        start_time = time.perf_counter()

        # Build the registry from LOWEST to HIGHEST precedence.
        # Celestial -> System -> Global -> Local
        new_registry: Dict[str, Dict[str, Any]] = {}

        # 1. STRATUM-3: THE CELESTIAL STREAM (Cloud Base)
        cls._hydrate_celestial_stratum(new_registry)

        # 2. STRATUM-2: THE SYSTEM CORE (Built-ins)
        cls._scan_physical_stratum(SYSTEM_DIR, "System", new_registry)

        # 3. STRATUM-1: THE GLOBAL FORGE (User Universal)
        if GLOBAL_DIR.exists():
            cls._scan_physical_stratum(GLOBAL_DIR, "Global", new_registry)

        # 4. STRATUM-0: THE LOCAL SANCTUM (Project Overrides)
        if LOCAL_DIR.exists():
            cls._scan_physical_stratum(LOCAL_DIR, "Local", new_registry)

        cls._cache = new_registry
        cls._last_scan_time = now

        duration = (time.perf_counter() - start_time) * 1000
        if duration > 50.0:  # Only log heavy metabolics
            Logger.debug(f"Registry Refused. {len(new_registry)} shards active. Latency: {duration:.2f}ms")

        return new_registry

    @classmethod
    def _hydrate_celestial_stratum(cls, registry: Dict[str, Any]):
        """[FACULTY 3]: Celestial Index Siphoning."""
        if not CELESTIAL_CACHE.exists():
            return

        try:
            raw_data = CELESTIAL_CACHE.read_text(encoding='utf-8')
            index_scripture = json.loads(raw_data)

            # Extract list regardless of V200 wrapper
            archetypes = index_scripture.get("archetypes", index_scripture)

            if isinstance(archetypes, list):
                for dna in archetypes:
                    name = dna.get("name")
                    if name:
                        dna["source_realm"] = "Celestial"
                        # We use the URL as the path for celestial items
                        dna["path"] = dna.get("url", "void://")
                        # For celestial items, 'archetype_path' is virtual
                        dna["archetype_path"] = f"celestial:{name}"
                        registry[name] = dna
        except Exception as e:
            Logger.warn(f"Celestial Cache Paradox: {e}. Cloud patterns may be obscured.")

    @staticmethod
    def _scan_physical_stratum(root: Path, realm: str, registry: Dict[str, Any]):
        """[THE ATOMIC SCAN]: Recursive Gaze into local matter."""
        try:
            if not root.exists(): return

            # Use rglob to find nested archetypes (e.g. genesis/python-basic.scaffold)
            for full_path in root.rglob("*.scaffold"):
                slug = full_path.stem

                try:
                    # [ASCENSION 3]: The DNA Oracle Communion
                    # Read only the first 4KB for header parsing to be fast
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        header_content = f.read(4096)

                    dna = GnosticDNAOracle.divine(slug, header_content)

                    dna["source_realm"] = realm
                    dna["path"] = str(full_path.resolve())
                    # Important: Add 'archetype_path' for compatibility with legacy consumers
                    dna["archetype_path"] = str(full_path.resolve())

                    # [ASCENSION 2]: Priority Overwrite (Precedence Law)
                    registry[slug] = dna

                except Exception as e:
                    Logger.warn(f"Heresy in {realm} archetype '{slug}': {e}")
        except Exception as e:
            Logger.error(f"Sanctum scan failure at {root}: {e}")


# =============================================================================
# == THE PUBLIC API (THE OMEGA INTERFACE)                                    ==
# =============================================================================

def list_profiles(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE OMEGA CENSUS                                                        ==
    =============================================================================
    Proclaims the complete list of manifest and latent architectural patterns.
    """
    registry = ArchetypeRegistry.refresh()
    profiles = list(registry.values())

    if category:
        profiles = [p for p in profiles if p.get("category", "").lower() == category.lower()]

    # [ASCENSION 7]: Sorted by Stratum Priority and Name
    # Priority: Local (0) > Global (1) > System (2) > Celestial (3)
    def rank_stratum(p):
        r = p.get("source_realm", "Celestial")
        return {"Local": 0, "Global": 1, "System": 2, "Celestial": 3}.get(r, 4)

    return sorted(profiles, key=lambda x: (rank_stratum(x), x.get("category", ""), x["name"]))


def get_profile(slug: str) -> Optional[Dict[str, Any]]:
    """[THE RITE OF RECALL] Instant O(1) metadata retrieval."""
    if not slug: return None
    registry = ArchetypeRegistry.refresh()
    return registry.get(slug)


def get_categories() -> List[str]:
    """[ASCENSION 7] Proclaims the unique strata taxonomies."""
    profiles = list_profiles()
    return sorted(list({p.get("category", "Unclassified") for p in profiles}))


def search_canon(query: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE FUZZY RESONANCE ORACLE                                              ==
    =============================================================================
    Searches the Gnostic Corpus (Names, Tags, Descriptions) for intent.
    """
    if not query: return list_profiles()

    q_tokens = query.lower().split()
    results = []
    all_profiles = list_profiles()

    for p in all_profiles:
        # Build the Semantic Corpus for this shard
        corpus = (
            f"{p['name']} "
            f"{p.get('description', '')} "
            f"{' '.join(p.get('tags', []))} "
            f"{p.get('category', '')} "
            f"{p.get('source_realm', '')}"
        ).lower()

        # The Gnostic Match: All query tokens must resonate within the corpus.
        if all(token in corpus for token in q_tokens):
            results.append(p)

    return results


# =============================================================================
# == THE LEGACY BRIDGE (PROFILES PROXY)                                      ==
# =============================================================================
# [THE CURE]: This class behaves like a Dictionary but calls ArchetypeRegistry.refresh()
# on access. This allows legacy code (like communion.py) that imports PROFILES
# to work seamlessly with the new dynamic engine.

class DynamicProfilesProxy(dict):
    """
    A magic dictionary that delegates lookup to the live Registry.
    Heals the 'NameError: profiles' and 'PROFILES not found' heresies.
    """

    def __getitem__(self, key):
        registry = ArchetypeRegistry.refresh()
        return registry[key]

    def get(self, key, default=None):
        registry = ArchetypeRegistry.refresh()
        return registry.get(key, default)

    def keys(self):
        return ArchetypeRegistry.refresh().keys()

    def values(self):
        return ArchetypeRegistry.refresh().values()

    def items(self):
        return ArchetypeRegistry.refresh().items()

    def __contains__(self, key):
        return key in ArchetypeRegistry.refresh()

    def __iter__(self):
        return iter(ArchetypeRegistry.refresh())

    def __len__(self):
        return len(ArchetypeRegistry.refresh())


# The Global Constant expected by communion.py and others
PROFILES = DynamicProfilesProxy()