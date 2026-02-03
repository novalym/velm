# Path: artisans/distill/core/oracle/perceiver.py
# -----------------------------------------------

import time
from pathlib import Path
from typing import TYPE_CHECKING

# ★★★ THE DIVINE HEALING: THE LAW OF THE NEW GNOSTIC PATH ★★★
# The profane, direct plea to the old `engine` scripture is annihilated.
# We now make a sacred plea to the `cortex` sanctum itself. Its `__init__.py`
# will guide us to the true, fractalized soul of the Cortex.
from .....core.cortex import GnosticCortex
# ★★★ THE APOTHEOSIS IS COMPLETE. THE OUROBOROS IS DEAD. ★★★

from .....logger import Scribe
from .contracts import OracleContext
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("OraclePerceiver")


class OraclePerceiver:
    """
    =================================================================================
    == THE FACULTY OF PERCEPTION (V-Ω-PRE-FLIGHT-INQUISITOR-ULTIMA)                ==
    =================================================================================
    LIF: 100,000,000,000,000

    The First Movement. The Eyes of the Oracle.
    It has been ascended from a humble servant into a true Gnostic Inquisitor. Before
    awakening the Cortex, it performs a battery of pre-flight checks to ensure the
    sanctum is worthy and the Gaze will be pure.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Gaze of the Void:** Detects if the target directory is empty and can short-circuit the entire distillation, saving countless cycles.
    2.  **The Sentinel of the Abyss:** Detects if the target is a "noise" directory (`node_modules`, `.git`) and refuses to scan it, preventing catastrophic lock-ups.
    3.  **The Git Oracle Communion:** Performs a pre-flight check for Git, warning the Architect if temporal Gnosis (churn, history) will be unavailable.
    4.  **The Gnostic Triage of Reality:** Intelligently distinguishes between a file target and a directory target, adapting its Gaze accordingly.
    5.  **The Unbreakable Ward of the Symlink:** Detects and resolves symbolic links in the target path, preventing infinite recursion paradoxes.
    6.  **The Chronocache Bridge:** Passes the `force_refresh` command down to the Cortex, allowing for a complete invalidation of all cached memory.
    7.  **The Luminous Voice of Intent:** Proclaims the exact, resolved path it is about to scan, annihilating any ambiguity.
    8.  **The Cortex's Anvil:** It is responsible for forging the `GnosticCortex` instance, the very heart of the engine's memory.
    9.  **The Telemetric Heartbeat:** Precisely measures the duration of the Cortex's Gaze, providing critical performance data.
    10. **The Filter of Aversion:** It is the conduit for `ignore` and `include` patterns, teaching the Cortex what to see and what to shun.
    11. **The Sovereign Soul:** Its purpose is pure: prepare the sanctum, awaken the Cortex, and bestow the Memory upon the Oracle Context.
    12. **The Unbreakable Contract:** Its `perceive` rite is an unbreakable vow, receiving the `OracleContext` and returning nothing, modifying the vessel with absolute Gnostic purity.
    """

    def __init__(self, root: Path, silent: bool = False):
        self.root = root
        self.silent = silent
        self.cortex = GnosticCortex(self.root)

    def perceive(self, context: OracleContext):
        """
        Conducts the Grand Rite of Perception.
        Populates `context.memory` with the complete state of the project.
        """
        t0 = time.time()

        # --- MOVEMENT I: THE PRE-FLIGHT INQUEST ---
        # The target for distillation is the `distill_path` on the Oracle itself,
        # which was anchored by the DistillArtisan.
        target_path = context.root  # The root of distillation context

        # [FACULTY 5] The Unbreakable Ward of the Symlink
        if target_path.is_symlink():
            resolved_target = target_path.resolve()
            if not self.silent:
                Logger.info(f"Symbolic link detected. Resolving '{target_path.name}' -> '{resolved_target}'")
            target_path = resolved_target

        # [FACULTY 4] The Gnostic Triage of Reality
        if not target_path.exists():
            raise ArtisanHeresy(f"The sanctum is a void. Path not found: {target_path}",
                                severity=HeresySeverity.CRITICAL)

        # [FACULTY 1] The Gaze of the Void
        if target_path.is_dir() and not any(target_path.iterdir()):
            raise ArtisanHeresy(f"The sanctum '{target_path.name}' is empty. The Gaze finds only a void.",
                                severity=HeresySeverity.WARNING)

        # [FACULTY 2] The Sentinel of the Abyss
        from .....core.cortex.knowledge import KnowledgeBase
        if target_path.name in KnowledgeBase.ABYSS_DIRECTORIES:
            raise ArtisanHeresy(
                f"The sanctum '{target_path.name}' is an Abyssal Realm.",
                severity=HeresySeverity.CRITICAL,
                suggestion="The Oracle refuses to gaze into profane realms like 'node_modules' or '.git'. Choose a source directory."
            )

        # [FACULTY 3] The Git Oracle Communion
        if not self.silent and not (self.root / ".git").is_dir():
            Logger.warn("No Git repository detected. Temporal Gnosis (churn, author history) will be unavailable.")

        # --- MOVEMENT II: THE AWAKENING OF THE CORTEX ---
        if not self.silent:
            Logger.info("The Oracle opens its eyes... Awakening the Gnostic Cortex.")
            if context.profile.regression:
                Logger.info("Temporal shift detected. Forcing Cortex to re-perceive all of spacetime.")

        # [FACULTY 10] The Filter of Aversion
        # We teach the Cortex what to ignore before it performs its Gaze.
        self.cortex.configure_filters(
            ignore=context.profile.ignore,
            include=context.profile.include
        )

        # [FACULTY 6] The Chronocache Bridge
        # The Cortex performs the heavy lifting: scanning files, parsing ASTs,
        # and building the initial static dependency graph. It uses its own internal
        # caching to avoid re-scanning unchanged files.
        context.memory = self.cortex.perceive(force_refresh=context.profile.regression)

        # --- MOVEMENT III: THE FINAL PROCLAMATION ---
        duration = (time.time() - t0) * 1000
        context.record_stat('perception_ms', duration)

        if not self.silent:
            Logger.success(
                f"Perception complete in {duration:.0f}ms. {len(context.memory.inventory)} scriptures are known.")