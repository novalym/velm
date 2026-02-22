# Path: src/velm/artisans/project/seeds.py
# ----------------------------------------
# LIF: ∞ | ROLE: MULTIVERSAL_DISCOVERY_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SEEDS_V300_SOURCE_TRIAGE_2026_FINALIS

import os
import re
import time
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
        """
        =============================================================================
        == THE TRIPLE-APERTURE GAZE: OMEGA POINT (V-Ω-TOTALITY-V20000.8-FINALIS)   ==
        =============================================================================
        LIF: ∞ | ROLE: SPATIAL_TRIANGULATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TRIANGULATE_V20000_WASM_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite scries the project multiverse to locate the sacred sanctums where
        architectural DNA resides. It has been ascended to its final form,
        implementing the "Virtual-First" priority to ensure the WASM mount is
        immediately resonant and unmanifested drift is annihilated.
        """
        start_ns = time.perf_counter_ns()
        sources: Dict[str, Path] = {}

        # =========================================================================
        # == MOVEMENT I: THE ETHEREAL PLANE (WASM_VIRTUAL)                      ==
        # =========================================================================
        # [ASCENSION 1]: THE CURE. In the browser, the Simulacrum mount is Supreme.
        # We scry the absolute mount point provided by the simulacrum_installer.
        if self.is_wasm:
            # Locus A: The Primary Package Mount
            virtual_pkg = Path("/home/pyodide/simulacrum_pkg/archetypes").resolve()
            # Locus B: Fallback for root-level unzips
            virtual_root = Path("/home/pyodide/archetypes").resolve()

            if virtual_pkg.exists() and virtual_pkg.is_dir():
                sources["virtual"] = virtual_pkg
                # Logger.verbose(f"VFS_RESONANCE: Sanctum manifest at {virtual_pkg}")
            elif virtual_root.exists() and virtual_root.is_dir():
                sources["virtual"] = virtual_root

        # =========================================================================
        # == MOVEMENT II: THE BUNDLED CORE (SYSTEM_GNOSIS)                       ==
        # =========================================================================
        # [ASCENSION 8]: DNA shipped within the Engine's own soul.
        try:
            # Navigate from seeds.py (Level 2) to the package root.
            package_root = Path(__file__).resolve().parents[2]
            system_forge = (package_root / "archetypes").resolve()

            if system_forge.exists() and system_forge.is_dir():
                # We do not overwrite "virtual" if it already claimed "system"
                if "virtual" not in sources:
                    sources["system"] = system_forge
        except Exception as e:
            Logger.debug(f"System Forge scry hindered: {e}")

        # =========================================================================
        # == MOVEMENT III: THE GLOBAL FORGE (USER_WILL)                          ==
        # =========================================================================
        # [ASCENSION 11]: The Architect's universal library (~/.scaffold/archetypes)
        if not self.is_wasm:
            try:
                global_forge = (Path.home() / ".scaffold" / "archetypes").resolve()
                if global_forge.exists() and global_forge.is_dir():
                    sources["global"] = global_forge
            except Exception:
                pass

        # =========================================================================
        # == MOVEMENT IV: THE PROJECT SANCTUM (LOCAL_MATTER)                      ==
        # =========================================================================
        # [ASCENSION 1]: Highest-order precedence: The local project's own Forge.
        try:
            local_forge = (self.root / ".scaffold" / "archetypes").resolve()
            if local_forge.exists() and local_forge.is_dir():
                sources["local"] = local_forge
        except Exception:
            pass

        # =========================================================================
        # == MOVEMENT V: VALIDATION & CANONIZATION                               ==
        # =========================================================================
        # [ASCENSION 4 & 5]: Final lustration of the spatial map.
        purified_sources: Dict[str, Path] = {}
        for realm, path in sources.items():
            try:
                # Force absolute normalization and verify physical resonance
                canonical_path = path.resolve(strict=True)
                if canonical_path.is_dir():
                    purified_sources[realm] = canonical_path
            except (OSError, RuntimeError, FileNotFoundError):
                # The sanctum is a ghost. We stay our hand.
                continue

        # --- FINAL TELEMETRY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if purified_sources:
            # self.logger.verbose(f"Triangulation RESONANT: {list(purified_sources.keys())} strata detected ({duration_ms:.2f}ms)")
            pass
        else:
            Logger.warn("TOTAL DISRESONANCE: No architectural DNA found in any strata.")

        # [ASCENSION 12]: THE FINALITY VOW
        return purified_sources

    # =========================================================================
    # == MOVEMENT I: SYSTEM DEMO CENSUS (The Specific Will)                  ==
    # =========================================================================

    def scry_system_demos(self) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE RITE OF DEMO DISCOVERY (V-Ω-TOTALITY-V2.0-WARDED)                  ==
        =============================================================================
        [THE CURE]: Implements multi-path scrying for the demos/ sanctum.
        """
        Logger.verbose("Scrying for System Demos (demos/ sanctums)...")
        demo_strands = []

        # [ASCENSION 1]: THE TRIPLE-GAZE
        # We scry: 1. Bundled (WASM), 2. Global (Home), 3. Local (.scaffold)
        for source_name, source_path in self._sources.items():
            # [THE FIX]: Check both 'demos' and 'archetypes/demos' for path-drift resilience
            candidates = [
                source_path / "demos",
                source_path / "archetypes" / "demos"
            ]

            for demo_dir in candidates:
                if not demo_dir.exists() or not demo_dir.is_dir():
                    continue

                Logger.verbose(f"   -> Perceiving Sanctum: {demo_dir}")
                for scripture in demo_dir.glob("*"):
                    if scripture.suffix in GNOSTIC_EXTENSIONS:
                        try:
                            strand = self._materialize_strand(scripture, source_path, is_system=True)
                            demo_strands.append(strand)
                            Logger.success(f"      [✓] Demo Manifest: {strand['name']}")
                        except Exception as e:
                            Logger.debug(f"      [!] Strand Fracture in {scripture.name}: {e}")

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
        """[FACULTY 2] Fast-Gaze Metadata Extraction (Void-Protected)."""
        # [THE CURE]: If stem is empty (dotfiles), fallback to the full name.
        safe_name = path.stem if path.stem else path.name

        meta = {
            "name": safe_name.replace("-", " ").title().replace("Api", "API"),
            "description": "Architectural Pattern Shard.",
            "category": "Generic",
            "difficulty": "Adept",
            "tags": ["archetype"]
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
                    val = match.group(1).strip()
                    if key == "tags" and val:
                        meta["tags"] = [t.strip().lower() for t in val.split(",") if t.strip()]
                    elif val:  # [THE CURE]: Ensure we don't overwrite with empty strings
                        meta[key] = val
        except Exception:
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