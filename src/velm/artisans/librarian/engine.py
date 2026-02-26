# Path: artisans/librarian/engine.py
# ---------------------------------
import time
from pathlib import Path
from typing import Tuple, List, Dict, Any

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import LibrarianRequest, LustrationIntensity
from ...help_registry import register_artisan
from ...logger import Scribe

# INTERNAL ORGANS
from .purifiers.matter import MatterPurifier
from .purifiers.memory import MemoryPurifier
from .purifiers.process import ProcessPurifier

Logger = Scribe("Librarian")


@register_artisan("librarian")
class LibrarianArtisan(BaseArtisan[LibrarianRequest]):
    """
    =================================================================================
    == THE OMEGA LIBRARIAN (V-Ω-TOTALITY-V25000-SANCTUM)                           ==
    =================================================================================
    LIF: ∞ | ROLE: METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN

    The supreme conductor of the Engine's lustration rites. It coordinates the
    Matter, Memory, and Process purifiers to maintain homeostasis.
    =================================================================================
    """

    def execute(self, request: LibrarianRequest) -> ScaffoldResult:
        self._start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: SENSORY TOMOGRAPHY ---
        vitals = self.vitals  # Inherited from BaseArtisan
        system_ram_percent = vitals.get("load_percent", 0)

        # [ASCENSION 2]: SYSTEM-LOAD EMPATHY
        # If the whole machine is dying (>95% RAM), we must be extremely gentle.
        is_pandemic = system_ram_percent > 95.0

        self.logger.info(
            f"Librarian: Metabolism scried ({system_ram_percent}% load). Intensity: {request.intensity.value}")
        self.progress("Calibrating Solvents...", 10)

        # Initialize Purifiers
        matter = MatterPurifier(self.io, self.project_root, self.logger)
        memory = MemoryPurifier(self.engine, self.logger)
        process = ProcessPurifier(self.logger)

        stats = {"bytes_reclaimed": 0, "entities_purged": 0}

        # --- MOVEMENT I: MEMORY LUSTRATION (GENTLEST) ---
        # Always run, especially in 'Pandemic' mode.
        mem_stats = memory.lustrate()
        stats["entities_purged"] += mem_stats

        if is_pandemic and request.intensity != LustrationIntensity.CRITICAL:
            self.logger.warn("System Pandemic detected (Too many tabs?). Restricting to Memory Lustration.")
            return self.success("In-memory lustration complete. Disk-rites stayed for host stability.", data=stats)

        # --- MOVEMENT II: MATTER LUSTRATION ---
        # We only touch .scaffold/ - Never the user's source code.
        matter_stats = matter.lustrate(request.intensity, request.target_domains, request.preserve_latest_count)
        stats["bytes_reclaimed"] += matter_stats[0]
        stats["entities_purged"] += matter_stats[1]

        # --- MOVEMENT III: PROCESS REAPING (ZOMBIES) ---
        if "zombies" in request.target_domains or request.intensity == LustrationIntensity.CRITICAL:
            process_stats = process.reap_orphans()
            stats["entities_purged"] += process_stats

        # --- FINAL REVELATION ---
        from ...utils import get_human_readable_size
        mass_str = get_human_readable_size(stats["bytes_reclaimed"])

        self.logger.success(f"Engine Cooled: {mass_str} reclaimed across {stats['entities_purged']} shards.")

        return self.success(
            f"Lustration complete. Engine homeostasis restored.",
            data=stats,
            ui_hints={"vfx": "bloom_blue" if not is_pandemic else "pulse_blue"}
        )
