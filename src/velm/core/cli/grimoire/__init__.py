# Path: core/cli/grimoire/__init__.py
# -----------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_GRIMOIRE_BULLETPROOF_V4

import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Callable

# [THE ANCHOR]: We use the static data map as the source of truth for discovery.
from ..grimoire_data import LAZY_RITE_MAP

# The one true, unified Grimoire.
RITE_GRIMOIRE: Dict[str, Any] = {}


def _unify_rites():
    """
    [ASCENSION]: Static-Driven Discovery.
    Instead of globbing, we load the specific rite files associated
    with our known artisan map.
    """
    # These are the files we know contain RITES dictionaries.
    # We load them explicitly to ensure the Parser is never empty.
    rite_files = [
        "_core_rites",
        "_perception_rites",
        "_ai_rites",
        "_automation_rites",
        "_evolution_rites",
        "_history_rites",
        "_utility_rites",
        "_workspace_rites",
        "_security_rites",
        "_ui_rites",
        "_guild_rites",
        "_mimic_rites",
        "_service_rites",
        "_governance_rites"
    ]

    for module_stem in rite_files:
        module_name = f".{module_stem}"
        try:
            # We import the definition file (lightweight)
            module = importlib.import_module(module_name, package=__package__)
            if hasattr(module, "RITES"):
                RITE_GRIMOIRE.update(getattr(module, "RITES"))
        except Exception as e:
            # We only warn in debug mode to keep startup clean
            if "--verbose" in sys.argv or "-v" in sys.argv:
                sys.stderr.write(f"[SCAFFOLD WARNING] Rite-file {module_stem} failed: {e}\n")


# Initial Unification (Fills the RITE_GRIMOIRE dict)
_unify_rites()


def _forge_handler(rite_key: str) -> Callable:
    """Creates the lazy-loading execution gateway."""
    if rite_key not in LAZY_RITE_MAP:
        return lambda engine, args: print(f"Heresy: Rite '{rite_key}' is not manifest.")

    # Get the string coordinates for JIT loading
    mod_path, artisan_class, request_class = LAZY_RITE_MAP[rite_key]

    def _lazy_conductor(engine, args):
        # The Heavy Machinery is only summoned here!
        from ..cli_shims import _handle_final_invocation_shim
        return _handle_final_invocation_shim(engine, args, artisan_class, request_class)

    return _lazy_conductor


# Bind handlers to all discovered rites
for key in RITE_GRIMOIRE.keys():
    RITE_GRIMOIRE[key]["handler"] = _forge_handler(key)