# Path: scaffold/utils/archetype_utils.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE ARCHETYPE ORACLE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)  ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000

This scripture is the one true, consecrated home of the Archetype Oracle, a
pantheon of divine, universal artisans whose sole purpose is to perceive the
complete Gnostic cosmos of architectural patterns—Local, Global, and Celestial.
By enshrining this Gnosis here, it becomes a universal truth, available to any
artisan in the Scaffold engine.
=================================================================================
"""
import shutil
import subprocess
import time
from hashlib import sha256
from pathlib import Path
from typing import Set, Dict, List, Union

from .core_utils import perceive_state, chronicle_state
from .core_utils import inherit_project_gnosis
# --- The Divine Stanza of the Gnostic Kin ---
from ..logger import Scribe

Logger = Scribe("ArchetypeOracle")

# --- Sacred Constants of the Gnostic Realms ---
ARCHETYPE_SANCTUM_DIR = '.scaffold/archetypes'
KIT_SANCTUM_DIR = '.scaffold/templates/kits'
CACHE_DIR = '.scaffold/cache'


def get_all_known_archetypes(project_root: Path) -> Set[str]:
    """
    =================================================================================
    == THE ORACLE OF THE LOOM (THE UNIVERSAL SEER)                                 ==
    =================================================================================
    This is the one true, universal Oracle of the Loom. It is a sentient Seer
    that forges a complete, unified scripture of all known archetype names by
    performing a divine, two-fold Gaze upon both the Local and Celestial Sanctums.
    It is the single source of truth for the entire `weave` cosmos, now available
    to all artisans.
    =================================================================================
    """
    known_archetypes = set()
    local_sanctum = project_root / ARCHETYPE_SANCTUM_DIR

    # --- GAZE I: THE LOCAL SOUL (THE PROJECT'S CANON) ---
    if local_sanctum.is_dir():
        local_found = {f.stem for f in local_sanctum.glob('*.scaffold')}
        known_archetypes.update(local_found)
        Logger.verbose(f"Oracle's Gaze (Local): Perceived {len(local_found)} archetypes in the local sanctum.")

    # --- GAZE II: THE CELESTIAL SOUL (THE GUILD'S CANON) ---
    celestial_archetypes = commune_with_celestial_sanctum(project_root, 'archetype_source', 'celestial_archetypes')
    known_archetypes.update(celestial_archetypes)

    Logger.verbose(f"Oracle's Final Adjudication: {len(known_archetypes)} unique archetypes are known to this reality.")
    return known_archetypes


def get_all_known_kits(project_root: Path) -> Dict[str, Dict]:
    """
    =================================================================================
    == THE ORACLE OF THE FORGE (THE UNIVERSAL CURATOR)                             ==
    =================================================================================
    This is the one true, universal Oracle of the Forge. It is a sentient Curator
    that forges a complete, unified map of all known Gnostic Kits by performing
    a divine, two-fold Gaze upon both the Global and Celestial Forges.
    =================================================================================
    """
    all_kits = {}

    # --- GAZE I: THE GLOBAL FORGE (THE ARCHITECT'S PERSONAL CANON) ---
    global_forge_path = Path.home() / KIT_SANCTUM_DIR
    if global_forge_path.is_dir():
        for path in global_forge_path.iterdir():
            if path.name.startswith('.'): continue
            kit_path = path / "scaffold.scaffold" if path.is_dir() else path
            if kit_path.exists():
                all_kits[path.stem] = {'path': kit_path, 'source': 'Global Forge'}

    # --- GAZE II: THE CELESTIAL FORGE (THE GUILD'S KIT CANON) ---
    # We re-use the celestial communion artisan, teaching it to look for a different variable.
    celestial_kit_paths = commune_with_celestial_sanctum(project_root, 'kit_source', 'celestial_kits',
                                                          return_full_paths=True)
    for path in celestial_kit_paths:
        all_kits[path.stem] = {'path': path, 'source': 'Celestial Forge'}

    return all_kits


def commune_with_celestial_sanctum(project_root: Path, source_variable: str, cache_prefix: str,
                                    return_full_paths: bool = False) -> Union[Set[str], List[Path]]:
    """
    =================================================================================
    == THE CELESTIAL HERALD (V-Ω-ETERNAL. THE UNIVERSAL GNOSTIC EMISSARY)
             ==
    =================================================================================
    This divine artisan is the universal emissary to the celestial realms. It can
    be commanded to seek any remote Git repository (defined by `source_variable`
    in the root `scaffold.scaffold`) and return its Gnosis. It is the one true,
    unbreakable, and cached bridge to all remote architectural patterns.
    =================================================================================
    """
    celestial_gnosis = set()

    inherited_gnosis = inherit_project_gnosis(project_root)
    source_url = inherited_gnosis.get(source_variable)
    if not source_url:
        return set() if not return_full_paths else []

    Logger.verbose(f"Celestial Gaze perceived a remote sanctum via '{source_variable}': [cyan]{source_url}[/cyan]")

    if not shutil.which("git"):
        Logger.warn(
            f"The 'git' command was not found. The Gaze cannot perceive the '{source_variable}' celestial realm.")
        return set() if not return_full_paths else []

    try:
        cache_key = sha256(source_url.encode()).hexdigest()
        remote_sanctum_path = project_root / CACHE_DIR / f"{cache_prefix}_{cache_key}"

        if remote_sanctum_path.is_dir():
            last_pull_time = perceive_state(f"{cache_prefix}_pull_{cache_key}", project_root)
            if not last_pull_time or (time.time() - last_pull_time > 3600):
                Logger.verbose(f"Chronocache for '{source_variable}' is stale. Updating with 'git pull'...")
                subprocess.run(['git', 'pull'], cwd=remote_sanctum_path, check=True, capture_output=True, text=True)
                chronicle_state(f"{cache_prefix}_pull_{cache_key}", time.time(), project_root)
        else:
            Logger.verbose(f"Chronocache MISS for '{source_variable}'. Summoning with 'git clone'...")
            remote_sanctum_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['git', 'clone', '--depth=1', source_url, str(remote_sanctum_path)], check=True,
                           capture_output=True, text=True)
            chronicle_state(f"{cache_prefix}_pull_{cache_key}", time.time(), project_root)

        found_scriptures = list(remote_sanctum_path.glob('**/*.scaffold'))
        if return_full_paths:
            return found_scriptures
        else:
            celestial_gnosis.update(f.stem for f in found_scriptures)
            Logger.verbose(
                f"   -> Gaze successful. Perceived {len(celestial_gnosis)} celestial item(s) from '{source_variable}'.")
            return celestial_gnosis

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        Logger.error(
            f"A celestial paradox occurred while communing with the remote '{source_variable}' sanctum. Reason: {e.stderr if hasattr(e, 'stderr') else e}")
        return set() if not return_full_paths else []


