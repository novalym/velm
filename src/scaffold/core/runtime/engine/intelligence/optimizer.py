# Path: core/runtime/engine/intelligence/optimizer.py
# ---------------------------------------------------

import os
import psutil
from typing import Any


class NeuroOptimizer:
    """
    =============================================================================
    == THE NEURO-OPTIMIZER (ADAPTIVE TUNING)                                   ==
    =============================================================================
    Adjusts runtime parameters based on hardware capabilities.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.cpu_count = os.cpu_count() or 1
        self.total_ram = psutil.virtual_memory().total

    def pre_dispatch_tuning(self):
        """
        Called before every dispatch to fine-tune environment.
        """
        # 1. Adjust Priority based on Load
        try:
            load = psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0

            if load > self.cpu_count:
                # System is stressed. Lower our priority.
                os.environ["SCAFFOLD_LOW_PRIORITY"] = "1"
            else:
                os.environ.pop("SCAFFOLD_LOW_PRIORITY", None)

            # 2. Memory Pressure Strategy
            mem_percent = psutil.virtual_memory().percent
            if mem_percent > 90:
                # Disable Caching to save RAM
                os.environ["SCAFFOLD_DISABLE_CACHE"] = "1"
            else:
                os.environ.pop("SCAFFOLD_DISABLE_CACHE", None)

        except Exception:
            pass

