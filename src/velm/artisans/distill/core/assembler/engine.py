# Path: artisans/distill/core/assembler/engine.py
# -----------------------------------------------

import time
from pathlib import Path
from typing import List, Dict, Set, Optional, Any

# --- THE DIVINE CONTRACTS ---
from .contracts import AssemblyContext, AssemblyStats
from .budget import TokenAccountant
from .header import HeaderForge
from .content import ContentWeaver

# --- THE GNOSTIC INSTRUMENTS ---
from .....core.cortex.contracts import  DistillationProfile
from ..skeletonizer import GnosticSkeletonizer
from .....core.cortex.contracts import FileGnosis
from .....core.cortex.tokenomics import TokenEconomist
from .....logger import Scribe

Logger = Scribe("BudgetWeaver")


class BudgetWeaver:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC ASSEMBLY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS)  ==
    =================================================================================
    @gnosis:title The Budget Weaver (The Sentient Loom)
    @gnosis:summary The final artisan that weaves the Gnostic Plan into textual reality,
                    managing the Token Budget with atomic precision.
    @gnosis:LIF 10,000,000,000,000
    @gnosis:auth_code #!@((#)

    This is the High Priest of the Output. It takes the **Plan** from the Governor,
    the **Symbols** from the Propagator, and the **Heat** from the Tracer, and weaves
    them into the final `scaffold-blueprint.scaffold` scripture.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Economist's Heart:** Instantiates its own `TokenEconomist` to
        perform precise, model-aware cost calculations, ensuring the context window
        is never breached.
    2.  **The Symbolic Bridge:** Correctly receives and passes the `active_symbols_map`
        to the `ContentWeaver`, enabling "Smart Skeletons" (Active: 5 | Dormant: 20).
    3.  **The Thermal Link:** Integrates the `heat_map` and `runtime_map` from the
        Runtime Wraith to annotate files with execution data (🔥) and variable states (👻).
    4.  **The Drift Inscriptor:** Injects the `architectural_drift_summary` into the
        header, preserving the wisdom of the `Verify` rite.
    5.  **The Fallback Safety Net:** Wraps every individual file weaving in a `try/except`
        block. If one file fails (encoding, permission), it is logged as a Heresy,
        but the Blueprint continues.
    6.  **The Path Normalizer:** Forces all output paths to be Relative POSIX strings,
        ensuring the AI sees a clean, consistent virtual filesystem.
    7.  **The Omission Scribe:** If a file is too expensive (budget exceeded), it
        automatically degrades it to a `PATH_ONLY` comment (`# [Omitted]`) rather
        than vanishing it entirely.
    8.  **The Telemetric Ledger:** Maintains detailed `AssemblyStats` (Files included,
        Files omitted, Breakdown by Tier) for the final Luminous Proclamation.
    9.  **The Header Forge:** Delegates system prompt generation to the `HeaderForge`,
        ensuring tech stack summaries and debt analysis are included.
    10. **The Dual-Weave Logic:** Intelligently switches between `weave()` and
        `weave_with_annotations()` depending on whether runtime data exists.
    11. **The Cost Simulator:** Provides a `calculate_cost()` method that allows the
        Governor to "dry run" the assembly math without generating the full string.
    12. **The Sovereign Context:** Encapsulates all state in `AssemblyContext`, making
        the Weaver stateless and reusable across different distillation passes.
    """

    def __init__(
            self,
            profile: DistillationProfile,
            root: Path,
            focus_keywords: Optional[List[str]] = None,
            active_symbols_map: Optional[Dict[Path, Set[str]]] = None,
            inventory: List[FileGnosis] = None,  # The Plan from the Governor
            heat_map: Optional[Dict[str, Set[int]]] = None,
            runtime_map: Optional[Dict[str, Dict[int, List[str]]]] = None,
            perf_stats: Optional[Dict[str, Dict[str, Any]]] = None,
            architectural_drift_summary: Optional[str] = None
    ):
        self.profile = profile
        self.root = root
        self.planned_inventory = inventory or []
        self.heat_map = heat_map or {}
        self.runtime_map = runtime_map or {}
        self.perf_stats = perf_stats or {}

        # [ASCENSION 1] The Economist's Heart
        self.economist = TokenEconomist()

        # [ASCENSION 2] The Symbolic Bridge
        self.context = AssemblyContext(
            token_budget=profile.token_budget,
            focus_keywords=focus_keywords or [],
            active_symbols_map=active_symbols_map or {}
        )

        # Budget Management
        self.accountant = TokenAccountant(
            max_tokens=float('inf') if profile.strategy == 'faithful' else profile.token_budget
        )

        # Sub-Artisans
        self.header_forge = HeaderForge(root, self.context, architectural_drift_summary=architectural_drift_summary)

        # [ASCENSION 6] The Skeletonizer Bridge
        skeletonizer = GnosticSkeletonizer(focus_keywords)

        self.content_weaver = ContentWeaver(
            profile, skeletonizer,
            heat_map=self.heat_map,
            runtime_values=self.runtime_map,
            perf_stats=self.perf_stats
        )

        self.stats = AssemblyStats()

    def assemble(self) -> str:
        """
        The Grand Rite of Assembly.
        Iterates through the plan, weaves content, checks budget, and produces the final scripture.
        """
        blueprint_lines = []

        # 1. Forge and Charge Header
        header = self.header_forge.forge(self.planned_inventory)
        self.accountant.charge(header)
        blueprint_lines.append(header)

        # 2. Iterate Inventory
        for gnosis in self.planned_inventory:
            # Normalize path key for map lookups
            path_key = str(gnosis.path).replace('\\', '/')

            # [ASCENSION 2] Retrieve Active Symbols for this file
            active_symbols = self.context.active_symbols_map.get(gnosis.path)

            # Retrieve Runtime Annotations
            file_heat = self.heat_map.get(path_key, set())
            file_runtime = self.runtime_map.get(path_key, {})

            entry = ""
            try:
                # [ASCENSION 10] Dual-Weave Logic
                # If we have runtime data and it's a full file, use the annotated weaver.
                if (file_heat or file_runtime) and gnosis.representation_method == 'full':
                    entry = self.content_weaver.weave_with_annotations(
                        gnosis, self.root, active_symbols, heat_lines=file_heat, runtime_notes=file_runtime
                    )
                else:
                    # Standard Weave (handles Full, Skeleton, Summary, Stub)
                    entry = self.content_weaver.weave(gnosis, self.root, active_symbols)

            except Exception as e:
                # [ASCENSION 5] The Fallback Safety Net
                Logger.warn(f"ContentWeaver faltered for '{gnosis.path.name}': {e}. Omitting from blueprint.")
                entry = f"# [HERESY] Failed to weave soul for {gnosis.path.name}. Reason: {e}"
                self.stats.files_omitted += 1
                blueprint_lines.append(entry)
                continue

            # [ASCENSION 11] The Budget Enforcer
            if self.accountant.can_afford(entry):
                self.accountant.charge(entry)
                blueprint_lines.append(entry)

                # Update Stats
                self.stats.files_included += 1
                self.stats.breakdown[gnosis.representation_method] = self.stats.breakdown.get(
                    gnosis.representation_method, 0) + 1
            else:
                # [ASCENSION 7] The Omission Scribe
                # If we can't afford the content, try to afford just the path
                path_entry = f"{path_key} # [Omitted: Budget Exceeded]"
                if self.accountant.can_afford(path_entry):
                    self.accountant.charge(path_entry)
                    blueprint_lines.append(path_entry)
                    self.stats.breakdown['path_only'] = self.stats.breakdown.get('path_only', 0) + 1

                self.stats.files_omitted += 1

        # Final Telemetry Log
        if not self.profile.strategy == 'faithful':
            Logger.info(
                f"Assembly Stats: {self.stats.breakdown} | "
                f"Utilization: {self.accountant.current_tokens}/{self.accountant.max_tokens}"
            )

        return "\n".join(blueprint_lines)

    def calculate_cost(self) -> int:
        """
        [ASCENSION 11] The Cost Simulator.
        Calculates the total token cost of the current plan without generating the full string.
        Used by the Governor for 'what-if' analysis.
        """
        # Base cost (Header)
        header = self.header_forge.forge(self.planned_inventory)
        total_cost = self.economist.estimate_cost(header)

        for gnosis in self.planned_inventory:
            # simulate weave
            active_symbols = self.context.active_symbols_map.get(gnosis.path)

            # We must actually run the weave logic to know the size of skeletons/summaries
            # because they are generated dynamically based on AST.
            # This is expensive but necessary for accurate budgeting.
            entry = self.content_weaver.weave(gnosis, self.root, active_symbols)
            total_cost += self.economist.estimate_cost(entry)

        return total_cost