# Path: src/velm/artisans/project/seeds.py
# ----------------------------------------
# LIF: ∞ | ROLE: MULTIVERSAL_DISCOVERY_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SEEDS_V300_SOURCE_TRIAGE_2026_FINALIS

import os
import re
import uuid
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Final

from ...logger import Scribe
from .constants import PROGENITOR_ID, GNOSTIC_NAMESPACE, SEED_NAMESPACE_PREFIX

Logger = Scribe("ArchetypeOracle")

# =============================================================================
# == STRATUM-0: THE TOPOGRAPHICAL CONSTANTS                                 ==
# =============================================================================

# [ASCENSION 1]: The Directory Filter Grimoire
# Matter that must be veiled from the Oracle's Gaze to maintain purity.
ABYSSAL_DIRECTORIES: Final[Set[str]] = {
    ".git", ".scaffold", "__pycache__", "node_modules", "venv", ".venv", "dist", "build"
}

# The sacred extensions of Gnostic DNA
GNOSTIC_EXTENSIONS: Final[Set[str]] = {".scaffold", ".arch", ".blueprint"}


# =============================================================================
# == STRATUM-1: THE DISCOVERY CONTROLLER (THE HIGH PRIEST)                  ==
# =============================================================================

class ArchetypeOracle:
    """
    =============================================================================
    == THE OMNISCIENT ORACLE OF ARCHETYPES (V-Ω-TOTALITY-V300)                 ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_SENSORY_ORGAN | RANK: OMEGA

    A hyper-versatile discovery engine that triangulates scriptures across
    multiple physical and virtual substrates.
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.root = project_root or Path.cwd()
        # [ASCENSION 2]: Substrate Sensing
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        # --- THE LATTICE REGISTRY ---
        # Maps Category -> List[Path]
        self._sources: Dict[str, Path] = self._triangulate_sources()

    def _triangulate_sources(self) -> Dict[str, Path]:
        """[FACULTY 1] Triangulates the physical sanctums of DNA."""
        sources = {}

        # 1. BUNDLED CORE (The shipped library)
        try:
            # We climb from artisans/project/seeds.py to the package root
            pkg_root = Path(__file__).resolve().parents[2]
            bundled_root = pkg_root / "archetypes"
            if bundled_root.exists():
                sources["bundled"] = bundled_root
        except Exception:
            pass

        # 2. VIRTUAL SANCTUM (WASM Fallback)
        if self.is_wasm:
            sources["virtual"] = Path("/home/pyodide/simulacrum_pkg/archetypes")

        # 3. GLOBAL FORGE (User's home directory)
        global_forge = Path.home() / ".scaffold" / "archetypes"
        if global_forge.exists():
            sources["global"] = global_forge

        # 4. LOCAL FORGE (Project-specific)
        local_forge = self.root / ".scaffold" / "archetypes"
        if local_forge.exists():
            sources["local"] = local_forge

        return sources

    # =========================================================================
    # == MOVEMENT I: SYSTEM DEMO CENSUS (The Specific Will)                  ==
    # =========================================================================

    def scry_system_demos(self) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE RITE OF DEMO DISCOVERY                                              ==
        =============================================================================
        [THE CURE]: Specifically targets the 'demos/' subfolder within any
        manifest source to identify 'System Demos' for the Multiverse Registry.
        """
        Logger.verbose("Scrying for System Demos (demos/ sanctums)...")
        demo_strands = []

        for source_name, source_path in self._sources.items():
            demo_dir = source_path / "demos"
            if not demo_dir.exists():
                continue

            # We perform a shallow scan of the demos folder
            for scripture in demo_dir.glob("*"):
                if scripture.suffix in GNOSTIC_EXTENSIONS:
                    strand = self._materialize_strand(scripture, source_path, is_system=True)
                    demo_strands.append(strand)

        return demo_strands

    # =========================================================================
    # == MOVEMENT II: PATTERN DISCOVERY (The General Will)                   ==
    # =========================================================================

    def discover_all_patterns(self, exclude_demos: bool = True) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE RITE OF TOTAL PERCEPTION                                            ==
        =============================================================================
        Recursively scans all manifest sources for every known Gnostic pattern.
        """
        all_strands = []
        for source_name, source_path in self._sources.items():
            Logger.verbose(f"Oracle scrying source: [cyan]{source_name}[/] at {source_path}")

            for root, dirs, files in os.walk(str(source_path)):
                # [ASCENSION 3]: ABYSSAL FILTERING
                # Prune non-Gnostic noise directories in-place
                dirs[:] = [d for d in dirs if d not in ABYSSAL_DIRECTORIES]

                # [ASCENSION 1]: DEMO ISOLATION
                # If willed, we skip the 'demos' folder during general pattern discovery
                if exclude_demos and "demos" in root:
                    continue

                root_path = Path(root)
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in GNOSTIC_EXTENSIONS:
                        strand = self._materialize_strand(root_path / filename, source_path)
                        all_strands.append(strand)

        return all_strands

    # =========================================================================
    # == MOVEMENT III: STRAND MATERIALIZATION (THE ALCHEMIST)                ==
    # =========================================================================

    def _materialize_strand(self, path: Path, source_root: Path, is_system: bool = False) -> Dict[str, Any]:
        """
        [THE GAZE OF THE SCRIBE]
        Transmutes a physical file into a rich Gnostic Strand.
        """
        # 1. Deterministic Identity
        template_key = path.stem
        if template_key == "progenitor":
            id_coord = PROGENITOR_ID
        else:
            # ID is tied to the filename to ensure cross-substrate resonance
            id_coord = str(uuid.uuid5(GNOSTIC_NAMESPACE, f"{SEED_NAMESPACE_PREFIX}{template_key}"))

        # 2. Metadata Scrying
        metadata = self._scry_header(path)

        # 3. Geometric Normalization
        rel_path = str(path.relative_to(source_root.parent)).replace('\\', '/')

        return {
            "id": id_coord,
            "name": metadata["name"],
            "description": metadata["description"],
            "template": template_key,
            "physical_path": str(path.absolute()).replace('\\', '/'),
            "relative_path": rel_path,
            "category": metadata["category"],
            "is_system": is_system,
            "tags": metadata["tags"],
            "difficulty": metadata["difficulty"],
            "mass": os.stat(path).st_size,
            "icon": metadata.get("icon", "Zap" if is_system else "Box"),
            "color": metadata.get("color", "#64ffda" if is_system else "#94a3b8")
        }

    def _scry_header(self, path: Path) -> Dict[str, Any]:
        """[FACULTY 2] Fast-Gaze Metadata Extraction."""
        meta = {
            "name": path.stem.replace("-", " ").title().replace("Api", "API"),
            "description": "Architectural Pattern Shard.",
            "category": "Generic",
            "difficulty": "Adept",
            "tags": []
        }

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.read(2048)  # Scry first 2KB only

            mapping = {
                "name": r"@name:\s*(.*)",
                "description": r"@description:\s*(.*)",
                "category": r"@category:\s*(.*)",
                "difficulty": r"@difficulty:\s*(Novice|Adept|Master|Grand Architect)",
                "icon": r"@icon:\s*(\w+)",
                "color": r"@color:\s*(#[0-9a-fA-F]{6})",
                "tags": r"@tags:\s*(.*)"
            }

            for key, pattern in mapping.items():
                match = re.search(pattern, header, re.IGNORECASE)
                if match:
                    if key == "tags":
                        meta["tags"] = [t.strip().lower() for t in match.group(1).split(",")]
                    else:
                        meta[key] = match.group(1).strip()
        except:
            pass

        return meta


# =============================================================================
# == STRATUM-2: GLOBAL REVELATION FUNCTIONS                                 ==
# =============================================================================

def discover_system_seeds() -> List[Dict[str, Any]]:
    """
    [THE PROJECT MANAGER INTERFACE]
    Used during bootstrap to populate the 'demos' list.
    """
    oracle = ArchetypeOracle()
    return oracle.scry_system_demos()


def discover_all_archetypes() -> List[Dict[str, Any]]:
    """
    [THE DEVELOPER INTERFACE]
    Used by 'velm project list --templates' or the Forge UI.
    """
    oracle = ArchetypeOracle()
    return oracle.discover_all_patterns()

# =============================================================================
# == THE FINALITY VOW                                                        ==
# =============================================================================
# The Oracle has spoken. The DNA of the Multiverse is now a queryable reality.