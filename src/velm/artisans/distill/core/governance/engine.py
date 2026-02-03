# Path: scaffold/artisans/distill/core/governance/engine.py
# ---------------------------------------------------------

import math
from typing import List, Dict, Optional, Any, Set, Union, Callable
from pathlib import Path

from .....logger import Scribe
from .....core.cortex.contracts import FileGnosis
from .contracts import RepresentationTier, GovernancePlan, GovernanceDecision
from .estimator import CostEstimator
from .policies import GovernancePolicy

Logger = Scribe("BudgetGovernor")


class BudgetGovernor:
    """
    =================================================================================
    == THE SOVEREIGN OF ALLOCATION (V-Ω-WATERLINE-PROTOCOL-ULTIMA)                 ==
    =================================================================================
    LIF: 10,000,000,000,000 (THE VORACIOUS MIND)

    This is not a simple counter. It is a **Gnostic Economist**.
    It treats the Context Window as a sacred vessel that must be filled to the brim
    with the highest-value Gnosis available.

    It implements the **Waterline Protocol**, a multi-pass strategy that layers fidelity
    onto the project structure like a painter applying glazes:
    1.  **Census:** Map the existence of everything.
    2.  **Vitality:** Grant full life to the Focus and Keystones.
    3.  **Context:** Grant summaries to the important.
    4.  **Structure:** Grant skeletons to the logic.
    5.  **Saturation:** Greedily upgrade everything else until the vessel overflows.
    """

    # We leave a small buffer for tokenizer variance (tokens are not always 4 chars)
    SAFETY_MARGIN = 0.02

    def __init__(self, budget_limit: int):
        self.raw_budget = budget_limit
        self.effective_budget = int(budget_limit * (1.0 - self.SAFETY_MARGIN))
        self.estimator = CostEstimator()
        self.current_spend = 0
        self.plan = GovernancePlan()

        # Internal tracking to prevent O(N^2) lookups
        self._allocation_map: Dict[Path, RepresentationTier] = {}

    def adjudicate_and_plan(self, ranked_inventory: List[FileGnosis]) -> Dict[Path, str]:
        """
        The Grand Rite of Budgeting.
        """
        Logger.info(
            f"The Governor awakens. Budget: [yellow]{self.effective_budget:,}[/yellow] tokens. "
            f"Candidates: {len(ranked_inventory)}"
        )

        self.plan = GovernancePlan()
        self.current_spend = 0
        self._allocation_map = {}

        # Sort by score descending. High value files get first dibs on upgrades.
        sorted_inventory = sorted(ranked_inventory, key=lambda x: x.centrality_score, reverse=True)

        # --- PHASE I: THE CENSUS (Map the Territory) ---
        # Minimal cost. We want *every* file to at least exist in the tree output.
        self._conduct_pass(
            sorted_inventory,
            target_tier=RepresentationTier.PATH_ONLY,
            reason_base="Census",
            force=True  # We force paths even if budget is tight (they are cheap)
        )

        # --- PHASE II: THE VITALITY PASS (Focus & Keystones) ---
        # Immediate promotion to maximum fidelity for critical files.
        for file in sorted_inventory:
            # 1. Explicit Focus (Score ~100)
            if file.centrality_score >= 99.0:
                self._try_upgrade(file, RepresentationTier.FULL, force=True, reason="Focus Target")
                continue

            # 2. Keystones (README, pyproject.toml, etc.)
            if GovernancePolicy.is_keystone(file):
                # Lockfiles are heavy. Keep them summarized unless explicitly focused.
                if GovernancePolicy.is_lockfile(file):
                    self._try_upgrade(file, RepresentationTier.SUMMARY, force=True, reason="Keystone Lockfile")
                else:
                    self._try_upgrade(file, RepresentationTier.FULL, force=True, reason="Keystone Artifact")

        # --- PHASE III: THE CONTEXT PASS (Broad Awareness) ---
        # Give the AI a summary of what high-ranking files *are*.
        # We target files with decent relevance (> 20.0).
        Logger.verbose("Governor entering Pass 3: Context Saturation (Summaries)...")
        context_candidates = [f for f in sorted_inventory if f.centrality_score > 20.0]
        self._conduct_pass(
            context_candidates,
            RepresentationTier.SUMMARY,
            reason_base="Context Layer"
        )

        # --- PHASE IV: THE STRUCTURAL PASS (Architecture) ---
        # Give the AI the AST/Definitions of the code.
        # We target code files with structural relevance (> 40.0).
        Logger.verbose("Governor entering Pass 4: Structural Saturation (Skeletons)...")
        structure_candidates = [f for f in sorted_inventory if f.centrality_score > 40.0 and f.category == 'code']
        self._conduct_pass(
            structure_candidates,
            RepresentationTier.SKELETON,
            reason_base="Structural Layer"
        )

        # --- PHASE V: THE SATURATION LOOP (The Voracious Fill) ---
        # Fill the remaining void with source code, starting from the most relevant.
        # We loop until we can't fit anything else.
        Logger.verbose("Governor entering Pass 5: Total Saturation (Greedy Fill)...")
        self._conduct_saturation_pass(sorted_inventory)

        # --- Finalize ---
        self._balance_books()
        return self.plan.allocations

    def _conduct_pass(
            self,
            inventory: List[FileGnosis],
            target_tier: RepresentationTier,
            reason_base: str,
            force: bool = False
    ):
        """
        Iterates through the inventory and attempts to upgrade files to the target tier.
        """
        for file in inventory:
            # Stop if budget exhausted (unless forcing)
            if self.current_spend >= self.effective_budget and not force:
                return

            # Check if file is already at a higher or equal tier
            current_tier = self._allocation_map.get(file.path, RepresentationTier.EXCLUDED)
            if self._is_tier_higher_or_equal(current_tier, target_tier):
                continue

            # Special Rule: Don't upgrade lockfiles to FULL in bulk passes
            if target_tier == RepresentationTier.FULL and GovernancePolicy.is_lockfile(file):
                continue

            # Attempt upgrade
            self._try_upgrade(file, target_tier, force=force, reason=reason_base)

    def _conduct_saturation_pass(self, inventory: List[FileGnosis]):
        """
        [THE VORACIOUS LOOP]
        Iterates through the inventory. If it can afford FULL, it buys it.
        If it can't afford FULL but can afford SKELETON, it buys that.
        If it can't afford SKELETON but can afford SUMMARY, it buys that.
        It squeezes every last drop of value into the window.
        """
        # We define the upgrade path: SUMMARY -> SKELETON -> FULL
        # We try the highest possible upgrade for each file.

        for file in inventory:
            if self.current_spend >= self.effective_budget:
                break

            current_tier = self._allocation_map.get(file.path, RepresentationTier.EXCLUDED)

            # Skip if already maxed out
            if current_tier == RepresentationTier.FULL:
                continue

            # Skip lockfiles for FULL saturation (too big, low value)
            if GovernancePolicy.is_lockfile(file):
                continue

            # Try FULL
            if self._try_upgrade(file, RepresentationTier.FULL, reason="Saturation (Full)"):
                continue

            # If FULL failed (too expensive), try SKELETON (if code)
            if file.category == 'code' and current_tier != RepresentationTier.SKELETON:
                if self._try_upgrade(file, RepresentationTier.SKELETON, reason="Saturation (Skeleton)"):
                    continue

            # If SKELETON failed, try SUMMARY
            if current_tier != RepresentationTier.SUMMARY:
                self._try_upgrade(file, RepresentationTier.SUMMARY, reason="Saturation (Summary)")

    def _try_upgrade(
            self,
            file: FileGnosis,
            target_tier: RepresentationTier,
            force: bool = False,
            reason: str = ""
    ) -> bool:
        """
        [THE ATOMIC TRANSACTION]
        Calculates the marginal cost. If affordable, commits the upgrade.
        Returns True if upgrade happened.
        """
        # Get current cost allocation
        current_decision = self.plan.decisions.get(file.path)
        current_cost = current_decision.cost if current_decision else 0

        # Estimate target cost
        target_cost = self.estimator.estimate(file, target_tier)

        # Marginal cost to upgrade
        marginal_cost = target_cost - current_cost

        # Adjudicate
        # Optimization: If marginal cost is <= 0 (downgrade or same), allow it always
        if force or marginal_cost <= 0 or (self.current_spend + marginal_cost <= self.effective_budget):
            self.current_spend += marginal_cost

            # Record the decision
            self.plan.decisions[file.path] = GovernanceDecision(
                tier=target_tier,
                cost=target_cost,
                reason=reason,
                score=file.centrality_score
            )
            # Update fast lookup maps
            self._allocation_map[file.path] = target_tier
            self.plan.allocations[file.path] = target_tier.value
            return True

        return False

    def _is_tier_higher_or_equal(self, current: Union[RepresentationTier, str], target: RepresentationTier) -> bool:
        """
        Hierarchy: FULL > SKELETON > SUMMARY > PATH_ONLY > EXCLUDED
        Note: SKELETON vs SUMMARY is subjective, but structurally SKELETON is usually 'more' code.
        """
        ranks = {
            RepresentationTier.EXCLUDED: 0,
            "excluded": 0,
            RepresentationTier.PATH_ONLY: 1,
            "path_only": 1,
            RepresentationTier.SUMMARY: 2,
            "summary": 2,
            RepresentationTier.INTERFACE: 3,  # Treat interface similar to skeleton
            "stub": 3,
            RepresentationTier.SKELETON: 4,
            "skeleton": 4,
            RepresentationTier.FULL: 5,
            "full": 5
        }

        curr_val = current if isinstance(current, RepresentationTier) else current
        return ranks.get(curr_val, 0) >= ranks.get(target, 0)

    def _balance_books(self):
        """Finalizes metrics and proclaims the allocation stats."""
        self.plan.total_cost = self.current_spend
        self.plan.utilization_percent = (self.current_spend / self.raw_budget) * 100

        # Reset and recount stats for accuracy
        self.plan.stats = {t.value: 0 for t in RepresentationTier}

        for decision in self.plan.decisions.values():
            self.plan.stats[decision.tier.value] += 1

        utilization_color = "green" if self.plan.utilization_percent > 80 else "yellow"
        if self.plan.utilization_percent < 10: utilization_color = "red"

        Logger.success(
            f"Governance Complete. Utilization: [{utilization_color}]{self.plan.utilization_percent:.1f}%[/] "
            f"({self.current_spend:,}/{self.raw_budget:,} tokens)\n"
            f"   [bold green]Full: {self.plan.stats['full']}[/] | "
            f"[bold yellow]Skel: {self.plan.stats['skeleton']}[/] | "
            f"[bold cyan]Sum: {self.plan.stats['summary']}[/] | "
            f"[dim]Path: {self.plan.stats['path_only']}[/]"
        )