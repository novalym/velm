# Path: core/daemon/registry/consecrator.py
# -----------------------------------------
# LIF: INFINITY | ROLE: JIT_REALITY_CONDUCTOR | RANK: SOVEREIGN
# auth_code: Ω_GHOST_CONSECRATOR_V100

import importlib
import sys
import os
import time
import logging
from typing import Any, Dict, Type, Tuple

# --- CORE UPLINKS ---
from ...cli.grimoire_data import LAZY_RITE_MAP
from ....logger import Scribe

Logger = Scribe("PantheonConsecrator")


class PantheonConsecrator:
    """
    =================================================================================
    == THE GNOSTIC CONSECRATOR (V-Ω-HOT-SWAP-SINGULARITY)                          ==
    =================================================================================
    The High Priest of the Daemon's Skills.

    [THE APOTHEOSIS]: This version enforces the GHOST REGISTRY. It maps intents to
    string paths, allowing the Engine to perform JIT Re-Inception on every request.
    """

    @staticmethod
    def ignite(nexus: Any) -> int:
        """
        [THE RITE OF GHOST CONSECRATION]
        Populates the Nexus and Engine with string-based coordinates.
        """
        start_time = time.perf_counter()
        consecrated_count = 0

        # 1. Materialize the Interface Gateway (Lightweight Models)
        try:
            # We use string paths for the request models too to prevent eager imports
            req_gateway_path = "scaffold.interfaces.requests"
            req_gateway = importlib.import_module(req_gateway_path)
        except ImportError as e:
            Logger.critical(f"INTERFACE_VOID: {e}")
            return 0

        # 2. The Ghost Registration Loop
        for cmd_id, mapping in LAZY_RITE_MAP.items():
            normalized_key = cmd_id.split('/')[-1]

            mod_path = f"scaffold.{mapping[0]}"
            art_class_name = mapping[1]
            req_class_name = mapping[2]

            try:
                # 3. Request Model Acquisition (Required for Triage)
                if not hasattr(req_gateway, req_class_name):
                    continue
                RequestClass = getattr(req_gateway, req_class_name)

                # 4. [ASCENSION 1]: GHOST BINDING
                # We map the Command ID to the Request Class for the Dispatcher.
                nexus.REQUEST_MAP[normalized_key] = RequestClass

                # 5. [ASCENSION 2]: NEURAL COORDINATES
                # We register the Artisan as a TUPLE of (ModulePath, ClassName).
                # The Engine's dispatch logic will detect this and perform JIT loading.
                nexus.engine.register_artisan(
                    RequestClass,
                    (mod_path, art_class_name)
                )

                consecrated_count += 1

            except Exception as e:
                Logger.debug(f"Ghost Skill '{normalized_key}' deferred: {e}")

        duration = (time.perf_counter() - start_time) * 1000
        Logger.success(
            f"Ghost Registry Consecrated: {consecrated_count} Skills mapped in {duration:.2f}ms. "
            f"Hot-Swap: [ENABLED]"
        )

        return consecrated_count

    @staticmethod
    def materialize_jit(engine: Any, module_path: str, class_name: str) -> Any:
        """
        =============================================================================
        == THE RITE OF RE-INCEPTION (V-Ω-JIT-LOADER)                               ==
        =============================================================================
        [THE CURE]: This is the heart of the Hot-Swap. It purges the module cache
        and re-imports the code on every call.
        """
        # [ASCENSION 12]: HOT-SWAP TOGGLE
        # If we are not in dev mode, we could skip the reload for max speed.
        is_dev = os.environ.get("SCAFFOLD_HOT_SWAP") == "1"

        try:
            if is_dev:
                # 1. ATOMIC CACHE EXORCISM
                # Find the module and any sub-modules in the same package
                to_purge = [m for m in sys.modules if m.startswith(module_path)]
                for m in to_purge:
                    sys.modules.pop(m, None)

            # 2. NEURAL IMPORT
            module = importlib.import_module(module_path)

            # 3. SOUL EXTRACTION
            artisan_class = getattr(module, class_name)

            # 4. INSTANTIATION
            # Pass the living engine context to the new soul
            return artisan_class(engine)

        except Exception as fracture:
            Logger.error(f"JIT Re-Inception Fractured for {module_path}: {fracture}")
            # [ASCENSION 7]: FORENSIC TRACEBACK
            traceback.print_exc()
            raise fracture