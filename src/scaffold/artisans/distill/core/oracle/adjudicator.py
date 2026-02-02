# === [scaffold/artisans/distill/core/oracle/adjudicator.py] - SECTION 1 of 1: The Adjudicator of Value ===
import time
from typing import Any, List
from .....logger import Scribe
from .contracts import OracleContext
from .....core.cortex.ranking.engine import SignificanceRanker
from ..governance import BudgetGovernor
from ..consts import DEFAULT_BUDGET

Logger = Scribe("OracleAdjudicator")


class OracleAdjudicator:
    """
    =================================================================================
    == THE FACULTY OF JUDGMENT (V-Ω-GNOSTIC-TRIBUNAL-ULTIMA)                        ==
    =================================================================================
    LIF: 100,000,000,000,000,000

    The Fourth Movement. The High Judge of the Oracle.
    It presides over the Tribunal of Value, orchestrating the Ranker and the Governor.

    ### THE ASCENSION OF THE BRIDGE:
    It now correctly bridges the gap between Divination and Ranking. It takes the
    **Resolved Seed Paths** from the Diviner and passes them as the **Focus** for the
    Ranker, ensuring the God-Ray Boost is applied to the files found, not just the
    keywords requested.
    """

    def __init__(self, silent: bool = False):
        self.silent = silent

    def adjudicate(self, context: OracleContext):
        """
        Conducts the Rite of Adjudication.
        Populates `context.ranked_inventory` and `context.governance_plan`.
        """
        t0 = time.time()

        # --- PHASE A: VALUATION (THE RANKER'S JUDGMENT) ---

        # [FACULTY 1] The Law of Dynamic Personas
        persona_intent = context.query_intent.get('type', 'balanced') if context.query_intent else 'balanced'
        if not self.silent:
            Logger.info(f"Adjudicator summons the Ranker with Persona: [magenta]{persona_intent}[/magenta]")

        # [FACULTY 2 & 3] The Gnostic Triage of Value

        # [THE FIX] The Bridge of Seeds
        # The Ranker expects 'focus' to contain the strings to match against file paths.
        # The Diviner has already resolved the abstract 'GnosticLogicWeaver' into concrete paths in 'seed_files'.
        # We must pass these concrete paths as the focus targets to ensure the God-Ray Boost (+10000) strikes them.

        # We combine raw keywords (for loose matching) and resolved paths (for exact matching)
        combined_focus = list(context.seed_files) + (context.profile.focus_keywords or [])

        ranking_context = {
            "query": context.profile.feature or "",
            "intent": persona_intent,
            "seeds": list(context.seed_files),
            "traced": list(context.traced_files),
            "impact_scores": context.impact_scores,
            "reasons": context.context_reasons,
            "ignore": context.profile.ignore or [],
            # [THE FIX] Inject resolved paths as focus
            "focus": combined_focus
        }

        # The Ranker assigns a 0-100 score to every file in the inventory.
        ranker = SignificanceRanker(context.profile, context.memory, intent=persona_intent)

        context.ranked_inventory = ranker.rank(context.memory.inventory, ranking_context)

        t1 = time.time()
        context.record_stat('ranking_ms', (t1 - t0) * 1000)

        # --- PHASE B: GOVERNANCE (THE TREASURER'S DECREE) ---

        # [FACULTY 4] The Polyglot Budgeteer
        context.budget_limit = self._parse_budget(context.profile.token_budget)
        if not self.silent:
            Logger.info(f"The Treasury is set. Budget: [yellow]{context.budget_limit:,}[/yellow] tokens.")

        governor = BudgetGovernor(context.budget_limit)

        # The Governor generates the Plan (Map of File -> Tier).
        context.governance_plan = governor.adjudicate_and_plan(context.ranked_inventory)

        t2 = time.time()
        context.record_stat('governance_ms', (t2 - t1) * 1000)

    def _parse_budget(self, budget: Any) -> int:
        """Parses human-readable budget strings (e.g. '800k', '1m')."""
        if isinstance(budget, int):
            return budget
        if not budget:
            return DEFAULT_BUDGET

        s = str(budget).lower().strip()
        multiplier = 1

        if s.endswith('k'):
            multiplier = 1000
            s = s[:-1]
        elif s.endswith('m'):
            multiplier = 1000000
            s = s[:-1]

        try:
            return int(float(s) * multiplier)
        except ValueError:
            Logger.warn(f"Invalid budget format '{budget}'. Defaulting to {DEFAULT_BUDGET}.")
            return DEFAULT_BUDGET