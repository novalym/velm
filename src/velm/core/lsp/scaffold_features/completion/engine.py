# Path: core/lsp/scaffold_features/completion/engine.py
# -----------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_COMPLETION_ENGINE_GOD_TIER_V200
# SYSTEM: CEREBRAL_CORTEX | ROLE: FORESIGHT_ORCHESTRATOR | RANK: SOVEREIGN
# =================================================================================

import logging
import time
import concurrent.futures
import uuid
import re
import sys
from typing import List, Any, Dict, Optional, Set

# --- IRON CORE UPLINKS ---
from ...base.features.completion.engine import CompletionEngine
from ...base.features.completion.contracts import CompletionContext
from ...base.features.completion.models import CompletionList, CompletionItem, CompletionItemKind
from ...base.types import Range, Position, TextEdit
from ...base.telemetry import forensic_log
from ...base.utils.uri import UriUtils

# --- THE PROPHET REGISTRY ---
from .providers.internal import InternalCompletionProvider
from .providers.keyword_prophet import KeywordProphet
from .providers.variable_prophet import VariableProphet
from .providers.path_prophet import PathProphet
from .providers.global_prophet import GlobalProphet

Logger = logging.getLogger("ScaffoldCompletionEngine")

# [ASCENSION 1]: THE GEOMETRIC LAW
TOKEN_PATTERN = re.compile(r'([^\s]+)$')

# [ASCENSION 2]: THE SINGLETON SIGILS
# Items matching these filterTexts are considered "The Same Thing" regardless of Label.
# We do NOT include '%' here because '%% post-run' and '%% trait' are distinct items sharing a prefix.
SINGLETON_SIGILS = {'$$', '::', '<<', '->', '@if', '@elif', '@else', '@for', '@include', '@macro', '@call'}


class ScaffoldCompletionEngine:
    """
    =============================================================================
    == THE SCAFFOLD COMPLETION FACTORY (V-Ω-SINGULARITY)                       ==
    =============================================================================
    """

    @staticmethod
    def forge(server: Any) -> 'CompletionEngine':
        engine = SingularityCompletionEngine(server)

        # [ASCENSION 3]: CONSTITUTIONAL HANDSHAKE (Fixing the % Trigger)
        server.register_capability(lambda caps: setattr(caps, 'completion_provider', {
            "triggerCharacters": ['.', '@', '$', ':', '/', '%', '?', '!', '>', '|', '{', '<', '-', '"', "'"],
            "resolveProvider": True,
            "completionItem": {
                "labelDetailsSupport": True,
                "documentationFormat": ["markdown", "plaintext"],
                "snippetSupport": True,
                "commitCharactersSupport": True
            }
        }))

        # Consecrate the Council of Prophets (Priority Order)
        engine.register(KeywordProphet(server))  # 100: Static Laws
        engine.register(InternalCompletionProvider(server))  # 95: Deep Logic
        engine.register(VariableProphet(server))  # 90: Local Reality
        engine.register(GlobalProphet(server))  # 85: Global Ether
        engine.register(PathProphet(server))  # 80: Topology

        return engine


class SingularityCompletionEngine(CompletionEngine):
    """
    =============================================================================
    == THE SINGULARITY COMPLETION ENGINE (V-Ω-HOLOGRAPHIC-DEDUPLICATED)        ==
    =============================================================================
    Integrates Virtual Injection for speed and Semantic Deduplication for purity.
    """

    def prophesy(self, params: Any, trace_id: str = "0xVOID") -> CompletionList:
        """
        [THE RITE OF FORESIGHT]
        """
        start_time = time.perf_counter()
        tid = trace_id or f"pred-{uuid.uuid4().hex[:6].upper()}"

        try:
            # 1. ACQUIRE SCRIPTURE
            uri = self.server._extract_uri(params)
            doc = self.server.documents.get(uri)

            if not doc:
                return CompletionList(isIncomplete=False, items=[])

            # 2. ATOMIC SNAPSHOT
            pos_dict = self.server._extract_position(params)
            line_idx = pos_dict['line']
            char_idx = pos_dict['character']

            # --- HOLOGRAPHIC OVERRIDE ---
            metadata = getattr(params, 'metadata', {}) or {}

            if isinstance(metadata, dict) and 'current_line' in metadata:
                line_text = metadata['current_line']
            else:
                line_text = doc.get_line(line_idx)

            safe_char_idx = min(char_idx, len(line_text))
            line_prefix = line_text[:safe_char_idx]

            # --- VIRTUAL INJECTION (FAIL-SAFE) ---
            trigger_char = getattr(params.context, 'triggerCharacter', None)

            if trigger_char and not line_prefix.endswith(trigger_char):
                line_prefix = line_prefix + trigger_char
                safe_char_idx += len(trigger_char)

            # --- STRING CONTEXT ---
            double_quotes = len(re.findall(r'(?<!\\)"', line_prefix))
            single_quotes = len(re.findall(r"(?<!\\)'", line_prefix))
            is_inside_string = (double_quotes % 2 == 1) or (single_quotes % 2 == 1)

            # 3. ASSEMBLE CONTEXT
            ctx = CompletionContext(
                uri=uri,
                project_root=str(self.server.project_root),
                session_id=getattr(self.server, '_session_id', 'VOID'),
                trace_id=tid,
                full_content=doc.text,
                line_text=line_text,
                line_prefix=line_prefix,
                position=pos_dict,
                offset=0,
                trigger_character=trigger_char,
                trigger_kind=getattr(params.context, 'triggerKind', 1),
                language_id=doc.language_id,
                context_type='soul',
                is_inside_jinja='{{' in line_prefix and '}}' not in line_prefix,
                is_inside_comment=line_prefix.strip().startswith('#'),
                is_inside_string=is_inside_string,
                client_info=metadata.get('client_info', {})
            )

            all_items: List[CompletionItem] = []

            # 4. MULTITHREADED GATHERING
            futures = {
                self.server.foundry.submit(f"pred-{p.name}", p.provide, ctx): p
                for p in self.providers
            }

            done, not_done = concurrent.futures.wait(futures, timeout=0.350)

            for future in done:
                provider = futures[future]
                try:
                    p_start = time.perf_counter()
                    items = future.result()
                    p_dur = (time.perf_counter() - p_start) * 1000

                    if items:
                        for item in items:
                            # SORT NORMALIZATION
                            prio = f"{100 - provider.priority:03d}"
                            if not item.sort_text:
                                item.sort_text = f"{prio}-{item.label}"

                            # METADATA SUTURE
                            if item.data is None: item.data = {}
                            if isinstance(item.data, dict):
                                item.data["_provider"] = provider.name
                                item.data["_trace_id"] = tid
                                item.data["_latency"] = p_dur

                            all_items.append(item)
                except Exception as e:
                    forensic_log(f"Prophet '{provider.name}' fractured: {e}", "ERROR", "PRED", trace_id=tid)

            # 5. GEOMETRIC SUTURE (RANGE CORRECTION)
            match = TOKEN_PATTERN.search(line_prefix)
            partial_token = match.group(1) if match else ""
            token_len = len(partial_token)

            start_char = safe_char_idx - token_len
            if start_char < 0: start_char = 0

            current_range = Range(
                start=Position(line=line_idx, character=start_char),
                end=Position(line=line_idx, character=safe_char_idx)
            )

            for item in all_items:
                item.text_edit = TextEdit(range=current_range, newText=item.insert_text or item.label)
                if not item.filter_text:
                    item.filter_text = item.label
                if '/' in item.label or item.kind in (17, 19):
                    item.commit_characters = []

                    # 6. [ASCENSION 11]: CONTENT-ADDRESSABLE DEDUPLICATION
            unique_map: Dict[str, CompletionItem] = {}

            for item in all_items:
                # Calculate Dedupe Key
                key = self._get_dedupe_key(item)

                if key not in unique_map:
                    unique_map[key] = item
                else:
                    existing = unique_map[key]

                    # CONFLICT RESOLUTION
                    # 1. Prefer Higher Priority (Lower SortText value)
                    if (item.sort_text or "") < (existing.sort_text or ""):
                        # Item wins. Inherit docs if missing.
                        if not item.documentation and existing.documentation:
                            item.documentation = existing.documentation
                        unique_map[key] = item
                    else:
                        # Existing wins. Inherit docs if missing.
                        if not existing.documentation and item.documentation:
                            existing.documentation = item.documentation

            final_list = sorted(unique_map.values(), key=lambda x: x.sort_text or x.label)

            # 7. TELEMETRY
            duration_ms = (time.perf_counter() - start_time) * 1000
            if duration_ms > 100:
                forensic_log(f"Prophecy Achieved: {len(final_list)} items in {duration_ms:.2f}ms", "SUCCESS", "PRED",
                             trace_id=tid)

            return CompletionList(
                isIncomplete=bool(not_done),
                items=final_list
            )

        except Exception as catastrophic_fracture:
            import traceback
            forensic_log(f"Prophecy Engine Collapse: {catastrophic_fracture}\n{traceback.format_exc()}", "CRIT", "PRED",
                         trace_id=tid)
            return CompletionList(isIncomplete=False, items=[])

    def _get_dedupe_key(self, item: CompletionItem) -> str:
        """
        [ASCENSION 2]: SEMANTIC KEY GENERATION
        Normalizes identity to merge "Sigil: Variable" with "$$".
        """
        # 1. Check FilterText against Singletons
        # The KeywordProphet sets filterText="$$" for "$$"
        # The SnippetProphet sets filterText="$$" for "Sigil: Variable Definition"
        # If they match a singleton, we return that singleton as the key.
        ft = item.filter_text or item.label
        if ft in SINGLETON_SIGILS:
            return f"SIGIL::{ft}"

        # 2. Check InsertText Identity
        # If insert texts are identical, they are the same item.
        # We strip snippet syntax for comparison (${1:foo} -> foo)? No, too risky.
        # Just direct comparison.
        if item.insert_text:
            return f"INSERT::{item.insert_text}"

        # 3. Fallback to Label
        return f"LABEL::{item.label}"

    def resolve(self, item: CompletionItem) -> CompletionItem:
        if not item.data or not isinstance(item.data, dict): return item
        provider_name = item.data.get("_provider")
        if not provider_name: return item

        provider = next((p for p in self.providers if p.name == provider_name), None)
        if not provider: return item

        try:
            return provider.resolve(item)
        except Exception:
            return item