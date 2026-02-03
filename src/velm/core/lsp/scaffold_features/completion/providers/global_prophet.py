# Path: core/lsp/scaffold_features/completion/providers/global_prophet.py
# -----------------------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_GLOBAL_PROPHET_OMNISCIENT_V12
# SYSTEM: CEREBRAL_CORTEX | ROLE: CROSS_FILE_SCRYER
# =================================================================================

import re
import logging
import time
from typing import List, Any, Set, Dict, Optional
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem, CompletionItemKind, InsertTextFormat

Logger = logging.getLogger("GlobalProphet")


class GlobalProphet(CompletionProvider):
    """
    =============================================================================
    == THE OMNISCIENT OBSERVER (V-Ω-ETHERIC-LINK)                              ==
    =============================================================================
    [CAPABILITIES]:
    1. Scans the 'Ether' (All Open Documents) for Gnostic Definitions.
    2. Projects variables from other files into the current completion list.
    3. Provides context on where the variable comes from and what it holds.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "GlobalProphet"

    @property
    def priority(self) -> int:
        # Lower than Local (100) and Keyword (100).
        # We want local variables to appear first.
        return 85

        # [ASCENSION 8]: TOMOGRAPHIC REGEX

    # Captures: 1=Sigil, 2=Name, 3=Type(opt), 4=Value(opt)
    # Matches: $$ port: int = 8080  OR  let user = "admin"
    VAR_PATTERN = re.compile(
        r'^\s*(?P<sigil>\$\$|let|def|const)\s+'
        r'(?P<name>[a-zA-Z_]\w*)'
        r'(?:\s*:\s*(?P<type>[^=]+))?'
        r'(?:\s*=\s*(?P<value>.*))?',
        re.MULTILINE
    )

    def provide(self, ctx: CompletionContext) -> List[CompletionItem]:
        start_time = time.perf_counter()

        # [ASCENSION 9]: TRIGGER DISCIPLINE
        # Only speak if the Architect is invoking a variable ($) or alchemical expression ({{)
        is_var_trigger = (
                ctx.trigger_character == '$' or
                ctx.line_prefix.endswith('$') or
                ctx.is_inside_jinja
        )

        if not is_var_trigger:
            return []

        items = []
        seen_vars: Set[str] = set()

        try:
            # 1. HARVEST THE ETHER
            # We iterate through all documents currently held in the Librarian's memory.
            open_uris = self.server.documents.open_uris

            # [ASCENSION 7]: METABOLIC GOVERNOR
            # Cap the scan to prevent freezing if 1000 files are open
            scan_limit = 50
            scanned_count = 0

            for uri in open_uris:
                if scanned_count >= scan_limit: break

                # [ASCENSION 2]: SELF-EXCLUSION
                # The LocalVariableProphet handles the current file with higher fidelity.
                if uri == ctx.uri: continue

                doc = self.server.documents.get(uri)
                if not doc: continue

                # Divine the origin name
                filename = uri.split('/')[-1]
                scanned_count += 1

                # 2. PERFORM THE SCAN
                # Find all definitions in this scripture
                matches = self.VAR_PATTERN.finditer(doc.text)

                for match in matches:
                    name = match.group("name")

                    # [ASCENSION 10]: DEDUPLICATION MATRIX
                    # If we've already seen this variable from another file, skip it.
                    # (First come, first served - usually most recently opened)
                    if name in seen_vars: continue

                    sigil = match.group("sigil")
                    type_hint = (match.group("type") or "").strip()
                    raw_value = (match.group("value") or "").strip().strip("'\"")

                    # [ASCENSION 4]: VALUE HOLOGRAPHY
                    # Truncate long values for display
                    display_value = raw_value if len(raw_value) < 30 else raw_value[:27] + "..."

                    # Construct Detail
                    detail = f"Global: {filename}"
                    if type_hint: detail += f" : {type_hint}"

                    # Construct Documentation
                    doc_md = (
                        f"### 🌍 Global Gnosis\n"
                        f"**Origin:** `{filename}`\n"
                        f"**Definition:** `{sigil} {name}`\n"
                    )
                    if raw_value:
                        doc_md += f"**Current Value:** `{display_value}`\n"

                    # 3. FORGE THE ITEM
                    items.append(CompletionItem(
                        label=name,
                        kind=CompletionItemKind.Variable,
                        detail=detail,
                        documentation={"kind": "markdown", "value": doc_md},
                        insertText=name,
                        # [ASCENSION 6]: PRIORITY STRATIFICATION
                        # "20" puts it below Local ("00") and Keywords ("00/10")
                        sortText=f"20-global-{name}",
                        filterText=name,  # Ensure fuzzy matching works
                        data={
                            "_source": "GLOBAL_ETHER",
                            "origin_uri": uri
                        }
                    ))

                    seen_vars.add(name)

            # Telemetry for heavy scans
            duration = (time.perf_counter() - start_time) * 1000
            if duration > 10:
                Logger.debug(
                    f"Scanned {scanned_count} remote scriptures in {duration:.2f}ms. Found {len(items)} artifacts.")

            return items

        except Exception as e:
            # [ASCENSION 11]: FAULT ISOLATION
            Logger.error(f"Global Prophecy Fractured: {e}")
            return []