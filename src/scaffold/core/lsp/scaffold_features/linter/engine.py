# Path: core/lsp/scaffold_features/linter/engine.py
# ----------------------------------------

import logging
import time
from typing import List, Any
from .context import AnalysisContext
from .registry import LawRegistry
from ...base.document import TextDocument
from ...base.types import Diagnostic

Logger = logging.getLogger("LinterEngine")

class LinterEngine:
    """
    =============================================================================
    == THE HIGH INQUISITOR (V-Ω-ORCHESTRATOR)                                  ==
    =============================================================================
    LIF: 10,000,000 | ROLE: JUDGMENT_DISPATCHER

    Orchestrates the Council of Rules to adjudicate the scripture.
    It summons the LawRegistry to get applicable laws, creates the Context,
    and aggregates the findings.
    """

    def __init__(self, server: Any):
        self.server = server
        self.registry = LawRegistry(server)

    def conduct_inquest(self, doc: TextDocument) -> List[Diagnostic]:
        """
        [THE RITE OF TOTAL PERCEPTION]
        """
        start_time = time.perf_counter()

        # 1. Forge Context
        ctx = AnalysisContext(doc, self.server)

        # 2. Summon the Phalanx of Rules
        # We can filter laws based on file language (scaffold vs symphony)
        rules = self.registry.get_rules(doc.language_id)

        all_heresies: List[Diagnostic] = []

        # 3. Execute Adjudication
        for rule in rules:
            try:
                findings = rule.validate(ctx)
                if findings:
                    all_heresies.extend(findings)
            except Exception as e:
                # A single rule failure must not halt the Inquisition
                Logger.error(f"Rule {rule.code} fractured: {e}", exc_info=True)

        duration = (time.perf_counter() - start_time) * 1000
        if duration > 50:
            Logger.debug(f"Heavy Inquest: {doc.uri.split('/')[-1]} took {duration:.2f}ms")

        return all_heresies