# Path: src/velm/genesis/genesis_profiles.py
# ------------------------------------------
# LIF: ∞ | ROLE: ARCHETYPE_GOVERNOR
# AUTH: Ω_REGISTRY_V550_SINGULARITY_FINALIS
# ------------------------------------------

import threading
import os
import json
import time
import hashlib
import collections
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Final, Set

# --- Core Interfaces ---
from .canon_dna import GnosticDNAOracle
from ..logger import Scribe, get_console
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ArchetypeRegistry")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"

# =============================================================================
# == PHYSICAL ANCHORS (THE FOUR REALMS)                                      ==
# =============================================================================

# I. System Core (Bundled with the package)
SYSTEM_DIR: Final[Path] = Path(__file__).parent.parent / "archetypes"

# II. Global Scope (User's Universal Library)
GLOBAL_DIR: Final[Path] = Path.home() / ".scaffold" / "archetypes"

# III. Local Scope (Project Overrides)
LOCAL_DIR: Final[Path] = Path.cwd() / ".scaffold" / "archetypes"

# IV. Cloud Cache (Local mirror of the remote index)
CELESTIAL_CACHE: Final[Path] = Path.home() / ".scaffold" / "celestial_index.json"

DEFAULT_PROFILE_NAME: Final[str] = "python-basic"


class ArchetypeRegistry:
    """
    The centralized, thread-safe memory bank for all available architecture patterns.

    Responsibilities:
    1. Hierarchical Resolution: Merges templates from System, Global, and Local scopes,
       ensuring local project overrides take precedence.
    2. Dynamic Caching: Prevents repetitive filesystem scanning via time-based invalidation.
    3. Metadata Extraction: Leverages the GnosticDNAOracle to parse template headers
       and generate dynamic JSON schemas for the UI.
    """
    # Internal State
    _cache: Dict[str, Dict[str, Any]] = {}
    _last_scan_time: float = 0.0
    _scan_ttl: float = 2.0  # Seconds before cache invalidation
    _state_hash: str = "void"

    # Concurrency Guard
    _lock = threading.RLock()

    @classmethod
    def _sys_log(cls, msg: str, color_code: str = "36"):
        """Internal tracing for performance and discovery diagnostics."""
        if _DEBUG_MODE:
            import sys
            sys.stderr.write(f"\x1b[{color_code};1m[DEBUG: Registry]\x1b[0m {msg}\n")
            sys.stderr.flush()

    @classmethod
    def refresh(cls, force: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Refreshes the registry index by scanning all available archetype sources.
        Implements the Double-Checked Locking pattern for maximum concurrency safety.
        """
        now = time.time()

        # 1. Fast-Path Cache Return
        if not force and cls._cache and (now - cls._last_scan_time < cls._scan_ttl):
            cls._sys_log(f"Cache hit. Serving {len(cls._cache)} templates. Hash: {cls._state_hash[:8]}")
            return cls._cache

        with cls._lock:
            # 2. Re-verify cache inside lock to prevent race conditions
            if not force and cls._cache and (now - cls._last_scan_time < cls._scan_ttl):
                return cls._cache

            start_time = time.perf_counter()
            new_registry: Dict[str, Dict[str, Any]] = {}

            # --- Source Hydration Hierarchy ---
            # Execution order defines override precedence (Local > Global > System > Cloud)

            # 1. Cloud Base
            cls._hydrate_celestial_stratum(new_registry)

            # 2. System Core
            cls._scan_physical_stratum(SYSTEM_DIR, "System", new_registry)

            # 3. Global User Overrides
            if GLOBAL_DIR.exists():
                cls._scan_physical_stratum(GLOBAL_DIR, "Global", new_registry)

            # 4. Local Project Overrides
            try:
                cls._scan_physical_stratum(LOCAL_DIR, "Local", new_registry)
            except Exception:
                pass

            # --- Finalize State ---
            cls._cache = new_registry
            cls._last_scan_time = now

            # Generate Merkle-hash for UI state verification
            serial_state = json.dumps(new_registry, sort_keys=True, default=str)
            cls._state_hash = hashlib.sha256(serial_state.encode()).hexdigest()

            duration = (time.perf_counter() - start_time) * 1000

            if duration > 10.0:
                Logger.debug(
                    f"Archetype Registry synchronized. {len(new_registry)} templates loaded in {duration:.2f}ms")

            return new_registry

    @classmethod
    def _hydrate_celestial_stratum(cls, registry: Dict[str, Any]):
        """Injects remote cloud templates from the local cache file."""
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
                    dna["source_realm"] = "Celestial"
                    dna["path"] = dna.get("url", "void://")
                    dna["archetype_path"] = f"celestial:{name}"
                    dna["_ui_schema"] = cls._project_ui_schema(dna)
                    registry[name] = dna
        except Exception as e:
            Logger.warn(f"Failed to load remote template cache: {e}")

    @staticmethod
    def _scan_physical_stratum(root: Path, realm: str, registry: Dict[str, Any]):
        """Recursively scans a local directory for .scaffold files and extracts their metadata."""
        if not root.exists() or not root.is_dir():
            return

        try:
            for full_path in root.rglob("*.scaffold"):
                # Prune noise directories
                if "__pycache__" in str(full_path) or ".git" in str(full_path):
                    continue

                slug = full_path.stem

                try:
                    # Yield to OS scheduler to prevent UI blocking on massive repositories
                    time.sleep(0)

                    # Extract metadata from file headers (Max 8KB to avoid loading huge templates into memory)
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        header_content = f.read(8192)

                    dna = GnosticDNAOracle.divine(slug, header_content)
                    if not dna or not isinstance(dna, dict):
                        continue

                    # Enrich metadata payload
                    dna["source_realm"] = realm
                    dna["path"] = str(full_path.resolve())
                    dna["archetype_path"] = dna["path"]
                    dna["last_modified"] = full_path.stat().st_mtime
                    dna["_ui_schema"] = ArchetypeRegistry._project_ui_schema(dna)

                    # Register (Overwrites lower-priority templates with the same name)
                    registry[slug] = dna

                except Exception as e:
                    ArchetypeRegistry._sys_log(f"Failed to parse metadata for {slug} in {realm}: {e}", "33")
                    continue
        except Exception as e:
            Logger.error(f"Directory scan failed at {root}: {e}")

    @staticmethod
    def _project_ui_schema(dna: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a JSON-Schema representation of the template's required variables for frontend rendering."""
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
# == PUBLIC API INTERFACES                                                   ==
# =============================================================================

def list_profiles(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns a formatted list of all available templates."""
    registry = ArchetypeRegistry.refresh()
    profiles = list(registry.values())

    if category and category.lower() != "all":
        profiles = [p for p in profiles if p.get("category", "").lower() == category.lower()]

    # Sort hierarchy: Local > Global > System > Cloud, then by Category, then alphabetically
    def rank_stratum(p):
        r = p.get("source_realm", "Celestial")
        return {"Local": 0, "Global": 1, "System": 2, "Celestial": 3}.get(r, 4)

    return sorted(profiles, key=lambda x: (rank_stratum(x), x.get("category", ""), x["name"]))


def get_profile(slug: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific template's metadata by its ID."""
    if not slug: return None

    # Handle the case where a physical file was deleted while the cache was active
    profile = ArchetypeRegistry.refresh().get(slug)
    if profile and profile.get("source_realm") != "Celestial":
        p = Path(profile["path"])
        if not p.exists():
            Logger.warn(f"Template '{slug}' was deleted from disk. Purging cache.")
            ArchetypeRegistry.refresh(force=True)
            return ArchetypeRegistry._cache.get(slug)

    return profile


def get_categories() -> List[str]:
    """Returns a list of all unique template categories for UI filtering."""
    profiles = list_profiles()
    return sorted(list({p.get("category", "Unclassified") for p in profiles if p.get("category")}))


def search_canon(query: str) -> List[Dict[str, Any]]:
    """
    Executes a weighted keyword-density search across all available templates.
    Useful for AI routing or fuzzy CLI searches.
    """
    if not query: return list_profiles()

    q_tokens = query.lower().split()
    all_profiles = list_profiles()
    scored_results = []

    for p in all_profiles:
        # Build search corpus with defined weighting priorities
        name_part = (f"{p['name']} ") * 10
        cat_part = (f"{p.get('category', '')} ") * 5
        tag_part = (f"{' '.join(p.get('tags', []))} ") * 3
        desc_part = p.get("description", "")

        corpus = (name_part + cat_part + tag_part + desc_part).lower()

        # Score matching token count
        resonance = sum(1 for token in q_tokens if token in corpus)

        # Only return results that match ALL provided search tokens
        if resonance == len(q_tokens):
            scored_results.append((resonance, p))

    return [res[1] for res in scored_results]


# =============================================================================
# == BACKWARD COMPATIBILITY LAYER                                            ==
# =============================================================================

class DynamicProfilesProxy(dict):
    """
    A transparent dictionary proxy that delegates standard dictionary operations
    to the live, continuously refreshed ArchetypeRegistry. Ensures older modules
    don't cache stale data.
    """

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


# The Universal Export
PROFILES = DynamicProfilesProxy()