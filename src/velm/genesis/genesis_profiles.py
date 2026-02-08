# Path: src/velm/genesis/genesis_profiles.py
# ------------------------------------------
# LIF: ∞ | ROLE: ARCHETYPE_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_REGISTRY_V550_SINGULARITY_FINALIS
# =================================================================================
import threading
import os
import json
import time
import hashlib
import collections
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Final, Set

# --- THE GNOSTIC UPLINKS ---
from .canon_dna import GnosticDNAOracle
from ..logger import Scribe, get_console
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# --- LOGGING PROCLAMATION ---
Logger = Scribe("GnosticRegistry")

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
    =============================================================================
    == THE OMEGA REGISTRY (V-Ω-TOTALITY-V550-SINGULARITY)                      ==
    =============================================================================
    The Singleton Mind of the Registry. Performs the Quadratic Fusion of all
    known architectural strata across the multiverse.
    """
    # --- INTERNAL STATE ---
    _cache: Dict[str, Dict[str, Any]] = {}
    _last_scan_time: float = 0.0
    _scan_ttl: float = 2.0  # Default metabolic cooldown
    _state_hash: str = "primordial_void"

    # [ASCENSION 8]: METABOLIC LOCK
    _lock = threading.RLock()

    @classmethod
    def refresh(cls, force: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        =============================================================================
        == THE RITE OF QUADRATIC FUSION (REFRESH)                                  ==
        =============================================================================
        LIF: ∞ | Scans all four strata and weaves them into the Unified Grimoire.
        [THE FIX]: Now correctly differentiates between Cache Hits and Fresh Scans.
        """
        now = time.time()

        # 1. THE CHRONO-PROBE (CACHE CHECK)
        if not force and cls._cache and (now - cls._last_scan_time < cls._scan_ttl):
            # [ASCENSION 1]: PROCLAIM THE ECHO
            if os.getenv("SCAFFOLD_VERBOSE") == "1":
                Logger.verbose(
                    f"Reality Echoed (Cached). {len(cls._cache)} shards resonant. Hash: {cls._state_hash[:8]}")
            return cls._cache

        with cls._lock:
            # Re-check cache inside lock (Double-Checked Locking Pattern)
            if not force and cls._cache and (now - cls._last_scan_time < cls._scan_ttl):
                return cls._cache

            start_time = time.perf_counter()
            new_registry: Dict[str, Dict[str, Any]] = {}

            # --- MOVEMENT I: STRATUM HYDRATION ---
            # Order of execution defines the Precedence Law (Celestial < System < Global < Local)

            # 1. STRATUM-3: THE CELESTIAL STREAM (Cloud Base)
            cls._hydrate_celestial_stratum(new_registry)

            # 2. STRATUM-2: THE SYSTEM CORE (Built-ins)
            cls._scan_physical_stratum(SYSTEM_DIR, "System", new_registry)

            # 3. STRATUM-1: THE GLOBAL FORGE (User Universal)
            if GLOBAL_DIR.exists():
                cls._scan_physical_stratum(GLOBAL_DIR, "Global", new_registry)

            # 4. STRATUM-0: THE LOCAL SANCTUM (Project Overrides)
            # Detect project root to scan local overrides
            try:
                # Use current working directory as default local anchor
                cls._scan_physical_stratum(LOCAL_DIR, "Local", new_registry)
            except Exception:
                pass

            # --- MOVEMENT II: STATE FINALIZATION ---
            cls._cache = new_registry
            cls._last_scan_time = now

            # [ASCENSION 2]: EVOLVE STATE HASH
            # Generate a Merkle-hash of the current consciousness
            serial_state = json.dumps(new_registry, sort_keys=True, default=str)
            cls._state_hash = hashlib.sha256(serial_state.encode()).hexdigest()

            duration = (time.perf_counter() - start_time) * 1000

            # [ASCENSION 1 - THE FIX]: THE LUMINOUS PROCLAMATION
            if duration > 10.0:  # Only log significant activity
                Logger.debug(f"Lattice Resonated. {len(new_registry)} shards manifest. Latency: {duration:.2f}ms")

            return new_registry

    @classmethod
    def _hydrate_celestial_stratum(cls, registry: Dict[str, Any]):
        """[FACULTY 3]: Celestial Index Siphoning."""
        if not CELESTIAL_CACHE.exists():
            return

        try:
            raw_data = CELESTIAL_CACHE.read_text(encoding='utf-8')
            index_scripture = json.loads(raw_data)

            archetypes = index_scripture.get("archetypes", [])
            if not isinstance(archetypes, list):
                return

            for dna in archetypes:
                name = dna.get("name")
                if name:
                    # Enforce Schema Completeness
                    dna["source_realm"] = "Celestial"
                    dna["path"] = dna.get("url", "void://")
                    dna["archetype_path"] = f"celestial:{name}"
                    # [ASCENSION 7]: UI Metadata Generation
                    dna["_ui_schema"] = cls._project_ui_schema(dna)
                    registry[name] = dna
        except Exception as e:
            Logger.warn(f"Celestial Cache Paradox: {e}. Cloud patterns obscured.")

    @staticmethod
    def _scan_physical_stratum(root: Path, realm: str, registry: Dict[str, Any]):
        """[THE ATOMIC SCAN]: Recursive Gaze into local matter."""
        if not root.exists() or not root.is_dir():
            return

        try:
            # [ASCENSION 3]: RECURSIVE KNOWLEDGE TREES
            for full_path in root.rglob("*.scaffold"):
                if "__pycache__" in str(full_path) or ".git" in str(full_path):
                    continue

                slug = full_path.stem

                try:
                    # [ASCENSION 4]: METABOLIC I/O VIGIL
                    # Micro-yield to OS if scanning massive hierarchies
                    time.sleep(0)

                    # [ASCENSION 5]: DNA ORACLEcommunion with NoneType Protection
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        header_content = f.read(8192)  # Increased buffer for deep metadata

                    dna = GnosticDNAOracle.divine(slug, header_content)
                    if not dna or not isinstance(dna, dict):
                        continue

                    # ENRICH PROFILE
                    dna["source_realm"] = realm
                    dna["path"] = str(full_path.resolve())
                    dna["archetype_path"] = dna["path"]
                    dna["last_modified"] = full_path.stat().st_mtime

                    # [ASCENSION 7]: UI Schema Projection
                    dna["_ui_schema"] = ArchetypeRegistry._project_ui_schema(dna)

                    # [ASCENSION 6]: PRECEDENCE ENFORCEMENT
                    # Higher strata (Local) overwrite lower (System)
                    registry[slug] = dna

                except Exception as e:
                    Logger.debug(f"Heresy in {realm} shard '{slug}': {e}")
                    continue
        except Exception as e:
            Logger.error(f"Sanctum scan failure at {root}: {e}")

    @staticmethod
    def _project_ui_schema(dna: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 7]: Generates JSON-Schema for Ocular UI forms."""
        # Future ascension: Deep introspection of variable types
        return {
            "title": dna.get("name", "Unknown"),
            "description": dna.get("description", ""),
            "type": "object",
            "properties": {
                k: {"type": "string", "default": v}
                for k, v in dna.get("variables", {}).items()
            }
        }


# =============================================================================
# == THE OMEGA INTERFACE (PUBLIC API)                                        ==
# =============================================================================

def list_profiles(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE OMEGA CENSUS (V-Ω-TOTALITY)                                         ==
    =============================================================================
    Proclaims the census of manifest and latent architectural patterns.
    """
    registry = ArchetypeRegistry.refresh()
    profiles = list(registry.values())

    if category and category.lower() != "all":
        profiles = [p for p in profiles if p.get("category", "").lower() == category.lower()]

    # [ASCENSION 7]: Rank-based Sorting
    def rank_stratum(p):
        r = p.get("source_realm", "Celestial")
        return {"Local": 0, "Global": 1, "System": 2, "Celestial": 3}.get(r, 4)

    return sorted(profiles, key=lambda x: (rank_stratum(x), x.get("category", ""), x["name"]))


def get_profile(slug: str) -> Optional[Dict[str, Any]]:
    """[THE RITE OF RECALL] Instant O(1) metadata retrieval."""
    if not slug: return None

    # [ASCENSION 11]: GHOST-PATH BIOPSY
    profile = ArchetypeRegistry.refresh().get(slug)
    if profile and profile.get("source_realm") != "Celestial":
        p = Path(profile["path"])
        if not p.exists():
            Logger.warn(f"Ghost Shard detected: '{slug}' vanished from disk. Purging cache.")
            ArchetypeRegistry.refresh(force=True)
            return ArchetypeRegistry._cache.get(slug)

    return profile


def get_categories() -> List[str]:
    """Proclaims the unique strata taxonomies."""
    profiles = list_profiles()
    return sorted(list({p.get("category", "Unclassified") for p in profiles if p.get("category")}))


def search_canon(query: str) -> List[Dict[str, Any]]:
    """
    =============================================================================
    == THE SEMANTIC RESONANCE ORACLE                                           ==
    =============================================================================
    [ASCENSION 12]: Weighted keyword-density search.
    """
    if not query: return list_profiles()

    q_tokens = query.lower().split()
    all_profiles = list_profiles()
    scored_results = []

    for p in all_profiles:
        # Build weighted corpus
        # Name has 10x weight, Category 5x, Tags 3x, Description 1x
        name_part = (f"{p['name']} ") * 10
        cat_part = (f"{p.get('category', '')} ") * 5
        tag_part = (f"{' '.join(p.get('tags', []))} ") * 3
        desc_part = p.get("description", "")

        corpus = (name_part + cat_part + tag_part + desc_part).lower()

        # Calculate resonance
        resonance = sum(1 for token in q_tokens if token in corpus)
        if resonance == len(q_tokens):
            scored_results.append((resonance, p))

    # Return only fully resonant matches, sorted by name
    return [res[1] for res in scored_results]


# =============================================================================
# == THE LEGACY BRIDGE (PROFILES PROXY)                                      ==
# =============================================================================

class DynamicProfilesProxy(dict):
    """A magic dictionary that delegates to the live Singularity."""

    def __getitem__(self, key):
        return ArchetypeRegistry.refresh()[key]

    def get(self, key, default=None):
        return ArchetypeRegistry.refresh().get(key, default)

    def keys(self): return ArchetypeRegistry.refresh().keys()

    def values(self): return ArchetypeRegistry.refresh().values()

    def items(self): return ArchetypeRegistry.refresh().items()

    def __contains__(self, key): return key in ArchetypeRegistry.refresh()

    def __iter__(self): return iter(ArchetypeRegistry.refresh())

    def __len__(self): return len(ArchetypeRegistry.refresh())


# The Universal Constant for backward compatibility
PROFILES = DynamicProfilesProxy()

# == SCRIPTURE SEALED: THE REGISTRY HAS REACHED OMEGA TOTALITY ==