# Path: core/lsp/features/signature_help/engine.py
# ------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
import re
from typing import List, Optional, Any, Dict, Tuple

from .contracts import SignatureProvider, InvocationContext
from .models import SignatureHelp, SignatureHelpParams, SignatureInformation

Logger = logging.getLogger("SignatureHelpEngine")


class SignatureHelpEngine:
    """
    =============================================================================
    == THE HIGH CHRONICLER (V-Ω-ORCHESTRATOR-V12)                             ==
    =============================================================================
    LIF: 10,000,000 | ROLE: INVOCATION_DISPATCHER | RANK: SOVEREIGN

    The central intelligence that traces back the cursor to find the call site,
    calculates argument indices, and polls the council of prophets.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[SignatureProvider] = []

        # [ASCENSION 5]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="SignatureOracleWorker"
        )

    def register(self, provider: SignatureProvider):
        """Consecrates a new signature prophet."""
        self.providers.append(provider)
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Signature Prophet Registered: {provider.name}")

    def compute(self, params: SignatureHelpParams) -> Optional[SignatureHelp]:
        """
        [THE RITE OF SIGNATURE REVELATION]
        """
        start_time = time.perf_counter()
        trace_id = f"sig-{uuid.uuid4().hex[:6]}"

        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return None

        # 1. DIVINE INVOCATION CONTEXT (The Heavy Lifting)
        # We walk back from the cursor to find the unclosed '(' and the symbol preceding it.
        invoc_ctx = self._divine_context(doc, params.position, trace_id)
        if not invoc_ctx:
            return None

        # 2. [ASCENSION 5]: PARALLEL POLLING
        all_sigs: List[SignatureInformation] = []
        futures = {self._executor.submit(p.provide_signatures, invoc_ctx): p for p in self.providers}

        done, _ = concurrent.futures.wait(futures, timeout=0.400)

        for future in done:
            provider = futures[future]
            try:
                sigs = future.result()
                if sigs:
                    all_sigs.extend(sigs)
            except Exception as e:
                Logger.error(f"Prophet '{provider.name}' fractured for '{invoc_ctx.symbol_name}': {e}")

        if not all_sigs:
            return None

        # 3. ASSEMBLY
        duration = (time.perf_counter() - start_time) * 1000
        Logger.debug(f"[{trace_id}] Signature revealed in {duration:.2f}ms. Sigs: {len(all_sigs)}")

        return SignatureHelp(
            signatures=all_sigs,
            activeSignature=0,
            activeParameter=invoc_ctx.active_parameter
        )

    def _divine_context(self, doc: Any, pos: Any, trace_id: str) -> Optional[InvocationContext]:
        """
        [ASCENSION 1 & 3]: THE GEOMETRIC DIVINER
        Walks backward from the cursor to find the nearest '(' and comma count.
        """
        line_text = doc.get_line(pos.line)
        prefix = line_text[:pos.character]

        # 1. Find the nearest unclosed '('
        paren_balance = 0
        arg_index = 0
        call_site_idx = -1

        # We walk backwards from the character before the cursor
        for i in range(len(prefix) - 1, -1, -1):
            char = prefix[i]

            if char == ')':
                paren_balance += 1
            elif char == '(':
                if paren_balance == 0:
                    call_site_idx = i
                    break
                else:
                    paren_balance -= 1
            elif char == ',' and paren_balance == 0:
                # [ASCENSION 3]: Parameter Calculus
                arg_index += 1

        if call_site_idx == -1:
            return None

        # 2. Extract the symbol name preceding the '('
        # Matches alphanumeric tokens including @ (for directives)
        before_call = prefix[:call_site_idx].rstrip()
        name_match = re.search(r'([a-zA-Z0-9_\$@%\-]+)$', before_call)

        if not name_match:
            return None

        symbol_name = name_match.group(1)

        return InvocationContext(
            uri=doc.uri,
            symbol_name=symbol_name,
            active_parameter=arg_index,
            full_line=line_text,
            prefix=prefix,
            trace_id=trace_id
        )