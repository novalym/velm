# Path: src/velm/core/daemon/registry/resolver.py
# =========================================================================================
# == THE REGISTRY RESOLVER (V-Ω-TOTALITY-V27-SINGULARITY)                                ==
# =========================================================================================
# LIF: INFINITY | ROLE: SPATIAL_SOUL_RESOLVER | RANK: OMEGA_SUPREME
# AUTH: Ω_RESOLVER_RECTIFICATION_2026_FINALIS
# =========================================================================================

import importlib
import importlib.util
import sys
import os
import logging
from typing import Tuple, Any, Type, Optional, Set
from pathlib import Path

# --- CORE GNOSTIC UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("RegistryResolver")


class PathSeer:
    """
    =================================================================================
    == THE GNOSTIC PATH-SEER (V-Ω-TOTALITY-HEALED-V27)                             ==
    =================================================================================
    LIF: 10,000,000,000 | auth_code: Ω_VELM_RESOLVER_ULTIMA

    The divine specialist responsible for translating string coordinates into living
    Python souls. This artisan performs the high-stakes transition from the Grimoire's
    declarative text to the Engine's executable logic.

    [THE RECTIFICATION]:
    All legacy 'scaffold' namespaces have been surgically excised. The Gaze is now
    permanently fixed on the 'velm' frequency.
    =================================================================================
    """

    _RESOLUTION_STACK: Set[str] = set()
    _LOCK = threading.RLock() if 'threading' in sys.modules else None

    @staticmethod
    def resolve(mod_path: str, art_name: str, req_name: str) -> Tuple[Type[Any], Type[Any]]:
        """
        =============================================================================
        == THE RITE OF SOUL RESOLUTION (RESOLVE)                                   ==
        =============================================================================
        LIF: ∞ | ROLE: GNOSTIC_TRANSLATOR

        Transmutes string-based coordinates into a pair of (ArtisanClass, RequestClass).
        """
        # [ASCENSION 1]: FORCE NATIVE NAMESPACE
        # We prepend 'velm.' to the incoming relative path to ensure absolute resolution.
        full_mod_path = f"velm.{mod_path}"
        req_gateway = "velm.interfaces.requests"

        # [ASCENSION 6]: CIRCULARITY WARD
        resolution_id = f"{full_mod_path}:{art_name}"
        if resolution_id in PathSeer._RESOLUTION_STACK:
            raise ArtisanHeresy(
                f"Ouroboros Loop Detected: Circular resolution of {resolution_id}",
                severity=HeresySeverity.CRITICAL
            )

        PathSeer._RESOLUTION_STACK.add(resolution_id)

        try:
            Logger.verbose(f"Seer gazing upon: [cyan]{full_mod_path}[/cyan] ...")

            # [ASCENSION 2]: SPECULATIVE SCRYING
            # We verify the module exists in the Aether before we attempt the heavy lift.
            spec = importlib.util.find_spec(full_mod_path)
            if spec is None:
                # [ASCENSION 7]: SOCRATIC ERROR TOMOGRAPHY
                PathSeer._conduct_path_autopsy(full_mod_path)
                raise ImportError(f"Module '{full_mod_path}' is a void in the current Python path.")

            # [ASCENSION 8]: THE DYNAMIC IMPORT RITE
            # Materialize the Artisan's home module
            art_module = importlib.import_module(full_mod_path)

            # Materialize the Request Gateway
            req_module = importlib.import_module(req_gateway)

            # [ASCENSION 3]: BIOMETRIC SOUL VALIDATION
            # 1. Extract and Verify Artisan
            if not hasattr(art_module, art_name):
                raise AttributeError(f"Artisan soul '{art_name}' not found in matter '{full_mod_path}'.")

            artisan_class = getattr(art_module, art_name)

            # 2. Extract and Verify Request Contract
            if not hasattr(req_module, req_name):
                raise AttributeError(f"Request contract '{req_name}' not found in the Neural Gateway.")

            request_class = getattr(req_module, req_name)

            # [ASCENSION 5]: FORENSIC LINEAGE TRACKING
            origin_file = getattr(art_module, "__file__", "unknown")
            Logger.debug(f"Resolved [green]{art_name}[/green] from {origin_file}")

            return artisan_class, request_class

        except ImportError as ie:
            Logger.critical(f"VOID_REALITY_HERESY: The Seer is blind to '{full_mod_path}'.")
            raise ArtisanHeresy(
                f"Linguistic Schism: Failed to resolve logic path.",
                details=f"The namespace '{full_mod_path}' is unreachable. Verify that 'velm' is installed and your PYTHONPATH is pure.",
                suggestion="Execute 'pip show velm' to verify the physical installation location.",
                severity=HeresySeverity.CRITICAL
            ) from ie

        except Exception as fracture:
            Logger.error(f"Resolution Paradox: A catastrophic event shattered the Gaze.")
            raise fracture

        finally:
            PathSeer._RESOLUTION_STACK.discard(resolution_id)

    @staticmethod
    def _conduct_path_autopsy(target_mod: str):
        """
        [FACULTY]: Performs a forensic analysis of the environment to find out
        why a module resolution failed.
        """
        Logger.warn(f"Conducting autopsy on failed resolution of '{target_mod}'...")

        # Log the state of the Python path for the Architect's gaze
        for i, p in enumerate(sys.path):
            Logger.debug(f"  [PATH_STRATA_{i}]: {p}")

        # Check for the old 'scaffold' ghost in the same location
        ghost_mod = target_mod.replace("velm.", "scaffold.")
        ghost_spec = importlib.util.find_spec(ghost_mod)
        if ghost_spec:
            Logger.critical(
                f"🚨 GHOST DETECTED: Found legacy '{ghost_mod}' at {ghost_spec.origin}. This is the source of the schism!")

    @staticmethod
    def get_version_info(obj: Any) -> str:
        """[FACULTY]: Scries the version metadata from a resolved soul."""
        module = importlib.import_module(obj.__module__)
        return getattr(module, "__version__", "UNKNOWN_VERSION")

# == SCRIPTURE SEALED: THE SEER'S GAZE IS NOW ABSOLUTE AND OMEGA ==