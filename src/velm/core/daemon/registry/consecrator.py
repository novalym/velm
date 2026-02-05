# Path: src/velm/core/daemon/registry/consecrator.py
# =========================================================================================
# == THE PANTHEON CONSECRATOR (V-Ω-TOTALITY-V26-SINGULARITY)                             ==
# =========================================================================================
# LIF: INFINITY | ROLE: SYSTEM_NEURAL_LINKER | RANK: OMEGA_SUPREME
# AUTH: Ω_REGISTRY_RECTIFICATION_2026_FINAL
# =========================================================================================

import importlib
import importlib.util
import sys
import os
import time
import logging
import traceback
from typing import Any, Dict, Type, Tuple, Optional

# --- CORE GNOSTIC UPLINKS ---
# We reach into the Grimoire Data to find the coordinates of the souls.
from ...cli.grimoire_data import LAZY_RITE_MAP
from ....logger import Scribe

Logger = Scribe("PantheonConsecrator")


class PantheonConsecrator:
    """
    =================================================================================
    == THE GNOSTIC CONSECRATOR (V-Ω-TOTALITY-HEALED-V26)                           ==
    =================================================================================
    LIF: 10,000,000,000 | auth_code: Ω_VELM_NATIVE_CORE

    The High Priest of the Daemon's Skills. This artisan is responsible for mapping
    Human Intent (Requests) to Kinetic Action (Artisans).

    [THE APOTHEOSIS]:
    This version physically enforces the 'velm' namespace. It has been purged of
    all legacy 'scaffold' references that caused the Import Paradox.
    =================================================================================
    """

    @staticmethod
    def ignite(nexus: Any) -> int:
        """
        =============================================================================
        == THE RITE OF GHOST CONSECRATION (IGNITION)                               ==
        =============================================================================
        Populates the Nexus and the Engine with the map of potential realities.
        """
        start_time = time.perf_counter()
        consecrated_count = 0
        heresy_count = 0

        # 1. MATERIALIZE THE INTERFACE GATEWAY (The Pydantic Contracts)
        # This is the Stratum-1 layer where the contracts reside.
        try:
            # [ASCENSION 1]: FORCE NATIVE NAMESPACE
            # We strictly enforce 'velm' to annihilate the ghost of 'scaffold'.
            req_gateway_path = "velm.interfaces.requests"
            req_gateway = importlib.import_module(req_gateway_path)
            Logger.verbose(f"Neural Gateway manifest at: {req_gateway.__file__}")
        except ImportError as e:
            Logger.critical(f"INTERFACE_VOID: The Gnostic Contracts are unmanifest. {e}")
            return 0

        # 2. THE GHOST REGISTRATION LOOP
        # We iterate through every Rite described in the Grimoire.
        for cmd_id, mapping in LAZY_RITE_MAP.items():
            # 'cmd_id' is the unique identifier (e.g., 'scaffold/analyze')
            # We extract the leaf intent.
            normalized_key = cmd_id.split('/')[-1]

            # [ASCENSION 1 & 5]: ASSEMBLY OF THE SOUL COORDINATES
            # Mapping is (module_path, artisan_class_name, request_class_name)
            # We prepend the 'velm.' prefix to ensure absolute resolution.
            mod_path = f"velm.{mapping[0]}"
            art_class_name = mapping[1]
            req_class_name = mapping[2]

            try:
                # 3. REQUEST CONTRACT ACQUISITION
                # We verify the Pydantic vessel exists before linking.
                if not hasattr(req_gateway, req_class_name):
                    Logger.warn(f"L{normalized_key}: Contract '{req_class_name}' is a void. Skipping.")
                    continue

                RequestClass = getattr(req_gateway, req_class_name)

                # 4. [ASCENSION 10]: NEXUS MAPPING
                # We update the Nexus's internal routing table so it knows
                # how to validate incoming JSON-RPC pleas.
                nexus.REQUEST_MAP[normalized_key] = RequestClass

                # 5. [ASCENSION 2]: GHOST BINDING
                # We register the Artisan with the Engine as a LATENT POTENTIAL (Tuple).
                # The Engine's dispatch logic will detect this tuple and call
                # materialize_jit() when the strike is willed.
                nexus.engine.register_artisan(
                    RequestClass,
                    (mod_path, art_class_name)
                )

                consecrated_count += 1
                # Logger.debug(f"Consecrated: {normalized_key} -> {art_class_name}")

            except Exception as e:
                # [ASCENSION 11]: FAULT ISOLATION
                Logger.error(f"Gnostic schism during {normalized_key} link: {e}")
                heresy_count += 1

        duration_ms = (time.perf_counter() - start_time) * 1000

        if consecrated_count > 0:
            Logger.success(
                f"Lattice Consecrated. {consecrated_count} Skills manifest in {duration_ms:.2f}ms."
            )

        if heresy_count > 0:
            Logger.warn(f"Perceived {heresy_count} fractures during consecration. Logic may be limited.")

        return consecrated_count

    @staticmethod
    def materialize_jit(engine: Any, module_path: str, class_name: str) -> Any:
        """
        =============================================================================
        == THE RITE OF RE-INCEPTION (V-Ω-JIT-LOADER)                               ==
        =============================================================================
        [ASCENSION 3 & 12]: THE DYNAMIC SOUL-LIFTER.
        This is the heart of the Hot-Swap. It purges the module cache and
        re-imports the code on every call to ensure the latest Will is manifest.
        """
        # Check environment for the Hot-Swap Will
        is_dev = os.environ.get("SCAFFOLD_HOT_SWAP") == "1"

        try:
            # [ASCENSION 3]: ATOMIC CACHE EXORCISM
            if is_dev:
                # Find the module and any sub-modules in the same package
                to_purge = [m for m in sys.modules if m.startswith(module_path)]
                for m in to_purge:
                    sys.modules.pop(m, None)

            # [ASCENSION 1]: THE PURE IMPORT
            # This will now correctly find 'velm.artisans...' because the
            # ignite() rite provided the absolute 'velm.' prefix.
            module = importlib.import_module(module_path)

            # Extract the Soul from the Matter
            artisan_class = getattr(module, class_name)

            # [ASCENSION 5]: THE INSTANTIATION
            # Pass the living engine context to the new artisan instance.
            return artisan_class(engine)

        except ImportError as ie:
            # [ASCENSION 7]: FORENSIC AUTOPSY
            Logger.critical(f"VOID_REALITY_HERESY: Module '{module_path}' could not be located.")
            raise ArtisanHeresy(
                f"Failed to lift Artisan '{class_name}' from the void.",
                details=f"Path '{module_path}' resolved to unknown location. Error: {ie}",
                suggestion="Check that the package is installed as 'velm' and not 'scaffold'."
            ) from ie

        except Exception as fracture:
            Logger.error(f"JIT Re-Inception Fractured for {module_path}: {fracture}")
            # Log full stack for post-mortem
            # traceback.print_exc()
            raise fracture

# == SCRIPTURE SEALED: THE CONSECRATOR IS NOW SOVEREIGN AND RECTIFIED ==