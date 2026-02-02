# Path: core/lsp/base/features/completion/engine.py
# -------------------------------------------------

import time
import logging
import concurrent.futures
import sys
import uuid
from typing import List, Any, Dict, Optional
from .contracts import CompletionContext
from .models import CompletionList, CompletionItem, CompletionItemKind
from ...telemetry import forensic_log

Logger = logging.getLogger("CompletionEngine")


class CompletionEngine:
    """
    =============================================================================
    == THE MASTER PROPHET (V-Ω-HYPER-DIAGNOSTIC-V25-RESOLVER)                  ==
    =============================================================================
    LIF: 10,000,000 | ROLE: PRECOGNITION_DISPATCHER

    Orchestrates the Council of Providers.

    [ASCENSION 13]: RESOLUTION ROUTING
    Now tags every completion item with its creator's ID in `data._provider`.
    The `resolve` method uses this tag to route the item back to the specific
    Prophet for deep hydration (lazy documentation).
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers = []
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=8,
            thread_name_prefix="Prophet"
        )

    def register(self, provider):
        """Consecrates a new prophet in the council."""
        self.providers.append(provider)
        self.providers.sort(key=lambda x: x.priority, reverse=True)

    def prophesy(self, params: Any, trace_id: str = "0xVOID") -> CompletionList:
        """
        [THE RITE OF PROPHECY]
        Base Engine Implementation (V-Ω-STRING-AWARE)
        """
        start_time = time.perf_counter()

        # 1. RETRIEVE SCRIPTURE
        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)

        # [ASCENSION 1]: VOID GUARD
        if not doc:
            return CompletionList(isIncomplete=False, items=[])

        # 2. DIVINE CONTEXT
        pos = params.position
        line_text = doc.get_line(pos.line)
        line_prefix = line_text[:pos.character]

        # [ASCENSION 2]: HOLOGRAPHIC METADATA PASSTHROUGH
        # Allow middleware/client metadata to flow into the context
        metadata = getattr(params, 'metadata', {}) or {}
        if isinstance(metadata, dict) and 'current_line' in metadata:
            # If middleware injected truth, use it
            line_text = metadata['current_line']
            line_prefix = line_text[:pos.character]

        # [ASCENSION 3]: STRING CONTEXT DETECTION (HEURISTIC)
        # Counts unescaped quotes to determine if we are inside a string.
        # This prevents Prophets from speaking inside string literals.
        import re
        double_quotes = len(re.findall(r'(?<!\\)"', line_prefix))
        single_quotes = len(re.findall(r"(?<!\\)'", line_prefix))
        is_inside_string = (double_quotes % 2 == 1) or (single_quotes % 2 == 1)

        trigger_char = getattr(params.context, 'triggerCharacter', None)
        trigger_kind = getattr(params.context, 'triggerKind', 1)

        ctx = CompletionContext(
            uri=uri,
            project_root=str(self.server.project_root) if self.server.project_root else "",
            session_id=getattr(self.server, '_session_id', 'VOID'),
            line_text=line_text,
            line_prefix=line_prefix,
            full_content=doc.text,
            position={"line": pos.line, "character": pos.character},
            offset=0,
            trigger_character=trigger_char,
            trigger_kind=trigger_kind,
            language_id=doc.language_id,
            context_type='soul',
            # [ASCENSION 4]: LEXICAL AWARENESS
            is_inside_jinja='{{' in line_prefix and '}}' not in line_prefix,
            is_inside_comment=line_prefix.strip().startswith('#') or line_prefix.strip().startswith('//'),
            is_inside_string=is_inside_string,  # <--- [ASCENSION 3 INTEGRATED]
            trace_id=trace_id,
            client_info=metadata.get('client_info', {})
        )

        all_items: List[CompletionItem] = []

        # 3. [ASCENSION 5]: PARALLEL GATHERING
        futures = {self._executor.submit(p.provide, ctx): p for p in self.providers}

        # [ASCENSION 6]: METABOLIC THROTTLING (350ms)
        done, not_done = concurrent.futures.wait(futures, timeout=0.350)

        for future in done:
            provider = futures[future]
            try:
                items = future.result()
                if items:
                    for item in items:
                        # [ASCENSION 7]: DEFAULT KIND
                        if not item.kind: item.kind = CompletionItemKind.Text

                        # [ASCENSION 8]: PRIORITY SORTING (Zero-Padded)
                        prio_prefix = f"{100 - provider.priority:03d}"
                        if not item.sort_text: item.sort_text = f"{prio_prefix}-{item.label}"

                        # [ASCENSION 9]: PROVIDER ATTRIBUTION (The Cure)
                        if item.data is None: item.data = {}
                        if isinstance(item.data, dict):
                            item.data["_provider"] = provider.name
                            item.data["_trace_id"] = trace_id

                        all_items.append(item)

            except Exception as e:
                # [ASCENSION 10]: FAULT ISOLATION
                forensic_log(f"Prophet '{provider.name}' fractured: {e}", "ERROR", "COMPLETION", trace_id=trace_id)

        # 4. [ASCENSION 11]: DEDUPLICATION
        unique_map = {}
        for item in all_items:
            # Key by Label + Detail to merge similar items
            key = f"{item.label}:{item.detail or ''}"
            if key not in unique_map:
                unique_map[key] = item
            else:
                # Keep the one with better sort text (Higher priority)
                existing = unique_map[key]
                if (item.sort_text or "") < (existing.sort_text or ""):
                    unique_map[key] = item

        final_list = list(unique_map.values())

        # 5. [ASCENSION 12]: TELEMETRY
        duration = (time.perf_counter() - start_time) * 1000
        if duration > 100 or len(final_list) > 0:
            forensic_log(f"Prophecy: {len(final_list)} items in {duration:.2f}ms", "SUCCESS", "COMPLETION",
                         trace_id=trace_id)

        return CompletionList(isIncomplete=bool(not_done), items=final_list)

    def resolve(self, item: CompletionItem) -> CompletionItem:
        """
        [THE RITE OF RESOLUTION]
        Routes the item back to its creator for deep hydration (docs, details).
        """
        if not item.data or not isinstance(item.data, dict):
            return item

        provider_name = item.data.get("_provider")
        if not provider_name:
            return item

        # Find the Prophet
        provider = next((p for p in self.providers if p.name == provider_name), None)
        if not provider:
            return item

        try:
            # Delegate resolution
            return provider.resolve(item)
        except Exception as e:
            Logger.error(f"Resolution Fracture ({provider_name}): {e}")
            return item