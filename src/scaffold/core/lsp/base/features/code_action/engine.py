# Path: core/lsp/features/code_action/engine.py
# --------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Optional, Any, Dict, Union
from .contracts import CodeActionProvider
from .models import CodeAction, CodeActionParams, CodeActionKind

Logger = logging.getLogger("CodeActionEngine")


class CodeActionEngine:
    """
    =============================================================================
    == THE MASTER REDEEMER (V-Ω-ACTION-ORCHESTRATOR-V12)                       ==
    =============================================================================
    LIF: 10,000,000 | ROLE: JUDICIAL_DISPATCHER | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Physicians.
    It performs parallel scrying to offer immediate structural and syntactic
    redemption to the Architect.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[CodeActionProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="RedemptionWorker"
        )

    def register(self, provider: CodeActionProvider):
        """Consecrates a new provider of action."""
        self.providers.append(provider)
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Action Provider Registered: {provider.name}")

    def compute(self, params: CodeActionParams) -> List[CodeAction]:
        """
        [THE RITE OF DISCOVERY]
        Aggregates potential actions from all providers in parallel.
        """
        start_time = time.perf_counter()
        trace_id = f"act-{uuid.uuid4().hex[:6]}"

        uri_data = params.text_document
        uri = str(uri_data.get('uri', ''))

        doc = self.server.documents.get(uri)
        if not doc:
            return []

        # 1. ASSEMBLE REDEMPTION CONTEXT
        target_range = params.range
        diagnostics = params.context.diagnostics

        # 2. [ASCENSION 1]: PARALLEL GATHERING
        all_actions: List[CodeAction] = []

        # Poll all providers concurrently
        futures = {self._executor.submit(p.provide_actions, doc, target_range, diagnostics): p for p in self.providers}

        # 300ms threshold for the lightbulb to appear
        done, _ = concurrent.futures.wait(futures, timeout=0.3)

        for future in done:
            provider = futures[future]
            try:
                actions = future.result()
                if actions:
                    # [ASCENSION 8]: Trace & Identity Injection
                    for action in actions:
                        if action.data is None: action.data = {}
                        if isinstance(action.data, dict):
                            action.data['_provider'] = provider.name
                            action.data['_trace_id'] = trace_id
                    all_actions.extend(actions)
            except Exception as e:
                Logger.error(f"Action Provider '{provider.name}' fractured: {e}", exc_info=True)

        # [ASCENSION 5]: RANKED WEIGHTING
        # Preferred actions (high confidence) bubble to the absolute top
        return sorted(all_actions, key=lambda a: (a.isPreferred or False), reverse=True)

    def resolve(self, action: CodeAction) -> CodeAction:
        """
        [THE RITE OF RESOLUTION]
        Calculates heavy edits lazily when the Architect focuses on a suggestion.
        """
        if not action.data or not isinstance(action.data, dict):
            return action

        provider_name = action.data.get('_provider')
        provider = next((p for p in self.providers if p.name == provider_name), None)

        if not provider:
            return action

        try:
            return provider.resolve_action(action)
        except Exception as e:
            Logger.error(f"Action Resolution failed for {provider_name}: {e}")
            return action