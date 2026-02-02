# Path: core/lsp/base/features/linter/engine.py
# ---------------------------------------------

import logging
import time
from typing import List, Any, Type
from .contracts import LinterRule
from ...types import Diagnostic

Logger = logging.getLogger("LinterEngine")


class LinterEngine:
    """
    =============================================================================
    == THE STATIC INQUISITOR (V-Ω-BASE-ENGINE)                                 ==
    =============================================================================
    LIF: 10,000,000 | ROLE: RULE_ORCHESTRATOR | RANK: SOVEREIGN

    The generic engine that manages a collection of LinterRules.
    It is the impartial judge. It accepts a Context, iterates through its
    consecrated Rules, and aggregates the resulting Diagnostics.

    [CAPABILITIES]:
    1. **Fault Isolation:** If a single rule crashes, it is logged and skipped;
       the Inquisition continues.
    2. **Priority Execution:** Rules are run in order of importance.
    3. **Telemetry:** Measures the execution time of the entire inquest.
    """

    def __init__(self, server: Any):
        """
        Initializes the Inquisitor.

        Args:
            server: The Language Server instance (for accessing global config/root).
        """
        self.server = server
        self.rules: List[LinterRule] = []
        self._is_sorted = True

    def register(self, rule: LinterRule):
        """
        [RITE: CONSECRATION]
        Adds a new Law to the engine's registry.
        """
        self.rules.append(rule)
        self._is_sorted = False
        # Logger.debug(f"Linter Rule Registered: {rule.code} (Priority {rule.priority})")

    def conduct_inquest(self, ctx: Any) -> List[Diagnostic]:
        """
        [THE RITE OF TOTAL PERCEPTION]
        Runs all registered rules against the provided context.

        Args:
            ctx: The AnalysisContext (Document + Metadata).

        Returns:
            List[Diagnostic]: The aggregated findings of all rules.
        """
        if not self._is_sorted:
            # Sort rules: Higher priority first
            self.rules.sort(key=lambda r: r.priority, reverse=True)
            self._is_sorted = True

        all_heresies: List[Diagnostic] = []
        start_time = time.perf_counter()

        for rule in self.rules:
            try:
                # Execute the specific law
                findings = rule.validate(ctx)

                if findings:
                    all_heresies.extend(findings)

            except Exception as e:
                # [ASCENSION]: FAULT TOLERANCE
                # A fracture in one law must not invalidate the entire legal system.
                Logger.error(f"Rule '{rule.code}' fractured during judgment: {e}", exc_info=True)

                # We optionally inject a meta-heresy to warn the user that a rule failed
                # (Commented out to reduce noise, enable for dev mode)
                # all_heresies.append(Diagnostic(...))

        duration = (time.perf_counter() - start_time) * 1000

        # [ASCENSION]: HEAVY INQUEST LOGGING
        # If the lint takes > 100ms, we log it for optimization.
        if duration > 100:
            Logger.debug(f"Heavy Inquest ({len(self.rules)} rules) took {duration:.2f}ms")

        return all_heresies