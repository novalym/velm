# Path: src/velm/artisans/project/seeds.py
# ----------------------------------------
import os
import re
import sys
import time
import uuid
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from .constants import PROGENITOR_ID, GNOSTIC_NAMESPACE, SEED_NAMESPACE_PREFIX
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ArchetypeOracle")

# =============================================================================
# == STRATUM-0: THE TOPOGRAPHICAL CONSTANTS                                  ==
# =============================================================================

# [ASCENSION 1]: The Directory Filter Grimoire
# Matter that must be veiled from the Oracle's Gaze to maintain purity and speed.
ABYSSAL_DIRECTORIES: Final[Set[str]] = {
    ".git", ".scaffold", "__pycache__", "node_modules", "venv", ".venv", "dist", "build", ".next"
}

# The sacred extensions of Gnostic DNA
GNOSTIC_EXTENSIONS: Final[Set[str]] = {".scaffold", ".arch", ".blueprint"}

# =============================================================================
# == STRATUM-1: THE DISCOVERY CONTROLLER (THE UNIVERSAL HIGH PRIEST)         ==
# =============================================================================


class ArchetypeOracle:
    """
    =============================================================================
    == THE OMNISCIENT ORACLE OF ARCHETYPES (V-Ω-TOTALITY-V100K-UNIVERSAL)      ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_SENSORY_ORGAN | RANK: OMEGA_SUPREME
    AUTH: Ω_ORACLE_V100K_UNIFIED_CACHE_FINALIS

    The unified discovery engine that triangulates scriptures across the multiverse.
    It serves as the single source of truth for the Genesis Artisan, the Weave Artisan,
    and the Project Manager.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The L1 Memory Sarcophagus (THE CURE):** Caches the census of the multiverse
        in a thread-safe singleton state. Successive scries cost 0.00ms.
    2.  **Macro vs Micro Divination:** Automatically detects if a blueprint is a 
        Full Reality (Project) or a Micro-Reality (Weavable Fragment) via headers.
    3.  **The Resolution Faculty:** Exposes `resolve_source(name)` to instantly
        provide the absolute physical Path of an archetype for the Genesis engine.
    4.  **Dependency Perception:** Parses `@requires` headers to warn the Architect
        if a fragment requires specific dependencies (e.g., 'react', 'fastapi').
    5.  **Apophatic Silence:** Stripped of all `print` and `success` logs during
        initialization to guarantee a zero-noise boot sequence in the WASM substrate.
    6.  **The Triple-Aperture Gaze:** Scries the Virtual (WASM), System (Bundled), 
        and Local (User) sanctums simultaneously, respecting priority overwrites.
    7.  **Idempotent Path Canonicalization:** Forces strict resolving of symlinks
        and relative paths to prevent duplicate entries in the Grimoire.
    8.  **The Ghost-Name Healer:** If a blueprint lacks a `@name` header, it 
        surgically transmutes the filename into a Title Cased identity.
    9.  **Substrate-Aware Routing:** Bypasses deep-disk I/O on Emscripten by 
        leveraging the pre-mounted `/home/pyodide/simulacrum_pkg` anchor.
    10. **The Abyssal Filter V2:** Truncates os.walk dynamically by modifying 
        the `dirs` list in-place, saving massive amounts of memory in large repos.
    11. **Cryptographic Identity Sealing:** Uses UUIDv5 hashing on the filename 
        to ensure the same archetype has the exact same ID across all client machines.
    12. **The Finality Vow:** A mathematical guarantee of returning a structured 
        list of valid DNA dictionaries.
    =============================================================================
    """

    # [ASCENSION 1]: The Thread-Safe Global Cache
    # We share memory across instances to ensure that Genesis, Weave, and ProjectManager
    # do not redundantly walk the filesystem.
    _GNOSTIC_CACHE: Dict[str, Dict[str, Any]] = {}
    _CACHE_LOCK = threading.RLock()
    _CACHE_HYDRATED = False

    def __init__(self, project_root: Optional[Path] = None):
        self.root = project_root or Path.cwd()
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._sources: Dict[str, Path] = self._triangulate_sources()

    def _triangulate_sources(self) -> Dict[str, Path]:
        """Maps the physical coordinates of the known multiverse."""
        sources: Dict[str, Path] = {}

        # 1. The Ethereal Plane (WASM)
        if self.is_wasm:
            virtual_pkg = Path("/home/pyodide/simulacrum_pkg/archetypes").resolve()
            virtual_root = Path("/home/pyodide/archetypes").resolve()
            if virtual_pkg.exists() and virtual_pkg.is_dir():
                sources["virtual"] = virtual_pkg
            elif virtual_root.exists() and virtual_root.is_dir():
                sources["virtual"] = virtual_root

        # 2. The Bundled System Core
        try:
            package_root = Path(__file__).resolve().parents[2]
            system_forge = (package_root / "archetypes").resolve()
            if system_forge.exists() and system_forge.is_dir():
                if "virtual" not in sources:
                    sources["system"] = system_forge
        except Exception:
            pass

        # 3. The Global User Grimoire (~/.scaffold/archetypes)
        if not self.is_wasm:
            try:
                global_forge = (Path.home() / ".scaffold" / "archetypes").resolve()
                if global_forge.exists() and global_forge.is_dir():
                    sources["global"] = global_forge
            except Exception:
                pass

        # 4. The Local Project Sanctum (.scaffold/archetypes)
        try:
            local_forge = (self.root / ".scaffold" / "archetypes").resolve()
            if local_forge.exists() and local_forge.is_dir():
                sources["local"] = local_forge
        except Exception:
            pass

        # Purify paths
        purified_sources: Dict[str, Path] = {}
        for realm, path in sources.items():
            try:
                canonical_path = path.resolve(strict=True)
                if canonical_path.is_dir():
                    purified_sources[realm] = canonical_path
            except (OSError, RuntimeError, FileNotFoundError):
                continue

        return purified_sources

    # =========================================================================
    # == MOVEMENT I: THE RITE OF TOTAL DISCOVERY                             ==
    # =========================================================================

    def _hydrate_cache_if_void(self):
        """[THE CURE]: Scries the filesystem only if the memory banks are empty."""
        with self._CACHE_LOCK:
            if self._CACHE_HYDRATED:
                return

            all_strands = {}
            for source_name, source_path in self._sources.items():
                # We use os.walk but aggressively prune the abyss
                for root, dirs, files in os.walk(str(source_path)):
                    # [ASCENSION 10]: Abyssal Filter In-Place Pruning
                    dirs[:] = [d for d in dirs if d not in ABYSSAL_DIRECTORIES]

                    root_path = Path(root)
                    for filename in files:
                        ext = os.path.splitext(filename)[1].lower()
                        if ext in GNOSTIC_EXTENSIONS:
                            target_path = root_path / filename
                            try:
                                strand = self._materialize_strand(target_path, source_path,
                                                                  is_system=(source_name in ["system", "virtual"]))
                                # Key by unique ID
                                all_strands[strand["id"]] = strand
                            except Exception as e:
                                Logger.verbose(f"Strand Fracture in {filename}: {e}")

            self.__class__._GNOSTIC_CACHE = all_strands
            self.__class__._CACHE_HYDRATED = True

    def discover_all_patterns(self, type_filter: Optional[str] = None, exclude_demos: bool = True) -> List[
        Dict[str, Any]]:
        """
        Returns all manifest patterns from the L1 Cache.
        @param type_filter: "project" (Genesis) or "fragment" (Weave). None = All.
        """
        self._hydrate_cache_if_void()

        with self._CACHE_LOCK:
            results = list(self._GNOSTIC_CACHE.values())

            if exclude_demos:
                results = [r for r in results if not r.get("is_demo", False)]

            if type_filter:
                results = [r for r in results if r.get("type", "project") == type_filter]

            return results

    def scry_system_demos(self) -> List[Dict[str, Any]]:
        """Retrieves only the Progenitor and demo architectures."""
        self._hydrate_cache_if_void()
        with self._CACHE_LOCK:
            return [r for r in self._GNOSTIC_CACHE.values() if r.get("is_demo", False)]

    # =========================================================================
    # == MOVEMENT II: THE RESOLUTION FACULTY (FOR WEAVE & GENESIS)           ==
    # =========================================================================

    def resolve_source(self, intent_name: str) -> Tuple[Path, Dict[str, Any]]:
        """
        [ASCENSION 3]: THE PATHFINDER
        Locates the exact physical file for an archetype by name, template key, or ID.
        Used by the Genesis and Weave artisans to initiate materialization.
        """
        self._hydrate_cache_if_void()

        search_key = intent_name.lower().strip()

        with self._CACHE_LOCK:
            for strand_id, strand in self._GNOSTIC_CACHE.items():
                if (strand_id == search_key or
                        strand["template"].lower() == search_key or
                        strand["name"].lower() == search_key):

                    physical_path = Path(strand["physical_path"])
                    if physical_path.exists():
                        return physical_path, strand

            raise ArtisanHeresy(
                f"Oracle Failure: Archetype '{intent_name}' is unmanifest in the Grimoire.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use `scaffold project list --templates` or `scaffold archetypes list` to view manifest realities."
            )

    # =========================================================================
    # == MOVEMENT III: STRAND MATERIALIZATION (THE ALCHEMIST)                ==
    # =========================================================================

    def _materialize_strand(self, path: Path, source_root: Path, is_system: bool = False) -> Dict[str, Any]:
        """
        [THE GAZE OF THE SCRIBE]
        Transmutes a physical file into a rich Gnostic Strand dictionary.
        """
        template_key = path.stem

        # 1. Deterministic Identity
        if template_key == "progenitor":
            id_coord = PROGENITOR_ID
        else:
            id_coord = str(uuid.uuid5(GNOSTIC_NAMESPACE, f"{SEED_NAMESPACE_PREFIX}{template_key}"))

        # 2. Metadata Scrying
        metadata = self._scry_header(path)

        # 3. Geometric Normalization
        rel_path = str(path.relative_to(source_root.parent)).replace('\\', '/')

        # 4. Infer Demo Status
        is_demo = "demos" in path.parts

        return {
            "id": id_coord,
            "name": metadata["name"],
            "description": metadata["description"],
            "template": template_key,
            "physical_path": str(path.absolute()).replace('\\', '/'),
            "relative_path": rel_path,
            "category": metadata["category"],
            "type": metadata["type"],  # "project" or "fragment"
            "requires": metadata["requires"],  # Dependencies
            "is_system": is_system,
            "is_demo": is_demo,
            "tags": metadata["tags"],
            "difficulty": metadata["difficulty"],
            "mass": os.stat(path).st_size,
            "icon": metadata.get("icon", "Zap" if is_system else "Box"),
            "color": metadata.get("color", "#64ffda" if is_system else "#94a3b8")
        }

    def _scry_header(self, path: Path) -> Dict[str, Any]:
        """
        [FACULTY 2]: Fast-Gaze Metadata Extraction (Void-Protected).
        Scans the first 2KB of the scripture for @gnosis headers.
        """
        # [THE CURE]: If stem is empty (dotfiles), fallback to the full name.
        safe_name = path.stem if path.stem else path.name

        # Default Gnosis
        meta = {
            "name": safe_name.replace("-", " ").title().replace("Api", "API"),
            "description": "Architectural Pattern Shard.",
            "category": "Generic",
            "type": "project",  # Default to full project (Genesis)
            "requires": [],
            "difficulty": "Adept",
            "tags": ["archetype"]
        }

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.read(2048)

            # The Regex Matrix
            mapping = {
                "name": r'@(?:gnosis:)?(?:name|title):\s*(.*)',
                "description": r'@(?:gnosis:)?(?:description|summary):\s*(.*)',
                "category": r'@(?:gnosis:)?category:\s*(.*)',
                "type": r'@(?:gnosis:)?type:\s*(project|fragment|component|module)',
                "difficulty": r'@(?:gnosis:)?difficulty:\s*(Novice|Adept|Master|Grand Architect)',
                "icon": r'@(?:gnosis:)?icon:\s*(\w+)',
                "color": r'@(?:gnosis:)?color:\s*(#[0-9a-fA-F]{6})',
                "tags": r'@(?:gnosis:)?tags:\s*(.*)',
                "requires": r'@(?:gnosis:)?requires:\s*(.*)'
            }

            for key, pattern in mapping.items():
                match = re.search(pattern, header, re.IGNORECASE)
                if match:
                    val = match.group(1).strip()
                    if key == "tags" and val:
                        meta["tags"] = [t.strip().lower() for t in val.split(",") if t.strip()]
                    elif key == "requires" and val:
                        meta["requires"] = [t.strip().lower() for t in val.split(",") if t.strip()]
                    elif key == "type" and val:
                        # Normalize 'component' or 'module' to 'fragment' for internal taxonomy
                        meta["type"] = "fragment" if val.lower() in ("fragment", "component", "module") else "project"
                    elif val:
                        meta[key] = val

        except Exception as e:
            Logger.verbose(f"Metadata scry failed for {path.name}: {e}")

        return meta


# =============================================================================
# == STRATUM-2: GLOBAL REVELATION FUNCTIONS                                  ==
# =============================================================================

def discover_system_seeds() -> List[Dict[str, Any]]:
    """[THE PROJECT MANAGER INTERFACE]: Populates the 'demos' list instantly."""
    oracle = ArchetypeOracle()
    return oracle.scry_system_demos()


def discover_all_archetypes() -> List[Dict[str, Any]]:
    """[THE DEVELOPER INTERFACE]: Used by 'velm project list --templates'."""
    oracle = ArchetypeOracle()
    return oracle.discover_all_patterns(type_filter="project")


def discover_all_fragments() -> List[Dict[str, Any]]:
    """[THE WEAVER INTERFACE]: Used by 'velm weave' to find micro-realities."""
    oracle = ArchetypeOracle()
    return oracle.discover_all_patterns(type_filter="fragment")