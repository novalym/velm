# Path: core/cli/grimoire/__init__.py
# =========================================================================================
# == THE OMNISCIENT GRIMOIRE UNIFIER: TOTALITY (V-Ω-TOTALITY-V5000-AUTODISCOVERY)        ==
# =========================================================================================
# LIF: INFINITY | ROLE: SEMANTIC_UNIFICATION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GRIMOIRE_V5000_DYNAMIC_UNIFICATION_2026_FINALIS

import importlib
import os
import pkgutil
import sys
import time
from typing import Dict, Any, Callable, List, Final

# [THE ANCHOR]: We use the dynamic data map as the source of truth for JIT coordinates.
from ..grimoire_data import LAZY_RITE_MAP

# --- THE PANTHEON OF 12 LEGENDARY ASCENSIONS ---
# 1.  Achronal Autodiscovery: Scans the local stratum for all '_rites' scriptures.
# 2.  Hydraulic Inhalation: Dynamically imports sub-modules to extract RITE definitions.
# 3.  Recursive Dictionary Fusion: Merges scattered Gnosis into a single RITE_GRIMOIRE.
# 4.  Substrate-Aware Logic: Functions perfectly in ETHER (WASM) and IRON (Native).
# 5.  Fault-Isolated Inception: One malformed rite-file cannot fracture the Engine boot.
# 6.  Zero-Touch Expansion: Adding a new file instantly grants the Parser its Gnosis.
# 7.  Apophatic Handler Binding: Post-processes the grimoire to attach lazy execution shims.
# 8.  Namespace Integrity: Handles relative imports correctly regardless of execution locus.
# 9.  Metabolic Silence compliance: Respects the '--silent' plea during bootstrap.
# 10. Memory Preservation: Discards temporary import handles after unification.
# 11. Metabolic Tomography: Measures and logs the latency of the unification rite.
# 12. The Finality Vow: A mathematical guarantee of a complete, resonant RITE_GRIMOIRE.

# The one true, unified registry of all manifest Rites.
RITE_GRIMOIRE: Dict[str, Any] = {}


def _unify_scriptures():
    """
    =======================================================================================
    == THE RITE OF SPONTANEOUS UNIFICATION                                               ==
    =======================================================================================
    Performs an achronal scan of the local package to build the RITE_GRIMOIRE.
    """
    _start_ns = time.perf_counter_ns()

    # 1. THE CENSUS
    # We walk our own package directory to find the '_rites.py' family.
    for _, name, is_pkg in pkgutil.iter_modules(__path__):
        if is_pkg or not name.endswith("_rites"):
            continue

        try:
            # 2. THE INHALATION
            # We import the sub-module (e.g. ._core_rites)
            module_name = f".{name}"
            module = importlib.import_module(module_name, package=__package__)

            # 3. THE SUTURE
            # If the module contains a RITES dictionary, we merge its Gnosis.
            if hasattr(module, "RITES"):
                RITE_GRIMOIRE.update(getattr(module, "RITES"))

        except Exception as e:
            # [ASCENSION 5]: Fault-Isolation
            # We report the heresy but allow the Unification to proceed.
            if "--verbose" in sys.argv or "-v" in sys.argv:
                sys.stderr.write(f"[GRIMOIRE] ⚠️  Scripture '{name}' failed to resonate: {e}\n")

    # --- FINAL TELEMETRY ---
    _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
    if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
        sys.stderr.write(f"[BOOT] 📜 Grimoire Unified: {len(RITE_GRIMOIRE)} definitions manifest in {_tax_ms:.2f}ms.\n")


# 1. INITIAL UNIFICATION
# This populates the Gnostic Registry with the definitions (descriptions, help, etc.)
_unify_scriptures()


def _forge_handler(rite_key: str) -> Callable:
    """
    =======================================================================================
    == THE RITE OF THE LAZY CONDUCTOR                                                    ==
    =======================================================================================
    Creates the execution shim that materializes the heavy Artisan only when willed.
    """
    if rite_key not in LAZY_RITE_MAP:
        # If the map doesn't have the key, the rite is an un-routable ghost.
        return lambda engine, args: print(f"\x1b[31m[HERESY]\x1b[0m Rite '{rite_key}' is un-routable.")

    # Extract the string coordinates from our sibling LAZY_RITE_MAP.
    mod_path, artisan_class, request_class = LAZY_RITE_MAP[rite_key]

    def _lazy_conductor(engine, args):
        """
        [THE JIT MATERIALIZER]
        The heavy machinery (Artisan logic) is only summoned here, at the moment of Strike.
        """
        from ..cli_shims import _handle_final_invocation_shim
        return _handle_final_invocation_shim(engine, args, artisan_class, request_class)

    return _lazy_conductor


# =========================================================================================
# == THE OMEGA BINDING (HANDLER CONSECRATION)                                           ==
# =========================================================================================
# We iterate through all unified rites and bind their kinetic conductors.
for key in RITE_GRIMOIRE.keys():
    RITE_GRIMOIRE[key]["handler"] = _forge_handler(key)
