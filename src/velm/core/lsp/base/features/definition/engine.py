# Path: core/lsp/features/definition/engine.py
# --------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Union, Optional, Any, Dict
from .contracts import DefinitionRule
from .models import Location, LocationLink, DefinitionParams
from ...utils.text import TextUtils

Logger = logging.getLogger("DefinitionEngine")


class DefinitionEngine:
    """
    =============================================================================
    == THE NAVIGATOR (V-Ω-TOPOLOGICAL-DISPATCHER-V12)                          ==
    =============================================================================
    LIF: 10,000,000 | ROLE: CAUSAL_TRACER | RANK: SOVEREIGN

    The central intelligence that traces the threads of symbolic causality.
    It orchestrates a prioritized Council of Rules to locate where a symbol
    was willed into existence.
    """

    def __init__(self, server: Any):
        self.server = server
        self.rules: List[DefinitionRule] = []

        # [ASCENSION 4]: KINETIC FOUNDRY
        # High-priority thread pool for navigation lookups
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="NavigatorWorker"
        )

    def register(self, rule: DefinitionRule):
        """Consecrates a new navigation strategy in the registry."""
        self.rules.append(rule)
        # Re-sort by priority descending (highest first)
        self.rules.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Navigation Rule Inscribed: {rule.name} (P:{rule.priority})")

    def compute(self, params: DefinitionParams) -> Optional[Union[Location, List[Location], List[LocationLink]]]:
        """
        [THE RITE OF ORIGIN]
        Orchestrates the search for the symbol's genesis.
        """
        start_time = time.perf_counter()
        trace_id = f"nav-{uuid.uuid4().hex[:6]}"

        # 1. RETRIEVE THE LIVING SCRIPTURE
        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc:
            return None

        # 2. DIVINE THE ATOM (Word Identification)
        # Extracts the word and its context kind (variable, directive, etc.)
        info = TextUtils.get_word_at_position(doc, params.position)
        if not info:
            return None

        # 3. [ASCENSION 1 & 9]: PRIORITIZED RULE POLLING
        # We iterate through rules by priority. Usually, local rules succeed first.
        for rule in self.rules:
            try:
                # [ASCENSION 7]: MATCHING WARD
                if not rule.matches(info):
                    continue

                # [ASCENSION 4]: RULE EXECUTION
                # We execute the rule. Note: High-order rules may use the executor internally.
                result = rule.resolve(doc, info)

                if result:
                    # [ASCENSION 8]: TELEMETRY LOGGING
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    Logger.debug(f"[{trace_id}] Jump resolved by '{rule.name}' in {duration_ms:.2f}ms")
                    return result

            except Exception as e:
                # [ASCENSION 7]: FAULT ISOLATION
                Logger.error(f"Navigation Rule '{rule.name}' fractured for '{info.text}': {e}", exc_info=True)

        # Final Proclamation of Void
        return None