# Path: artisans/completion_artisan/prophets/alchemist.py
# -------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ALCHEMIST_DYNAMIC_V24
# SYSTEM: OCULAR_PROPHET | ROLE: JINJA_RUNTIME_SEER
# =================================================================================

import re
import logging
from typing import List, Dict, Any, Optional, Tuple

# --- IRON CORE UPLINKS ---
from .base import BaseProphet
from ....core.lsp.base.features.completion.contracts import CompletionContext
from ....core.lsp.base.features.completion.models import CompletionItem, CompletionItemKind, InsertTextFormat

Logger = logging.getLogger("AlchemistProphet")


class AlchemistProphet(BaseProphet):
    """
    =============================================================================
    == THE TRANSMUTATION SEER (V-Ω-DYNAMIC-RUNTIME-LINK)                       ==
    =============================================================================
    Prophesies Jinja2 variables, filters, and functions from the LIVE Runtime.
    It perceives the difference between a Source (Variable) and a Transformation (Filter).
    """

    # Matches: $$ name: type = value OR let name = value
    VAR_PATTERN = re.compile(
        r'^\s*(?:\$\$|let|def|const)\s+(?P<name>[a-zA-Z_]\w*)(?:\s*:\s*(?P<type>[^=]+))?',
        re.MULTILINE
    )

    # Matches a pipe not inside quotes
    PIPE_PATTERN = re.compile(r'\|(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)\s*$')

    def prophesy(self, ctx: CompletionContext) -> List[CompletionItem]:
        try:
            # [ASCENSION 1]: CONTEXTUAL GATING
            # Only speak if inside {{ ... }}
            if not ctx.is_inside_jinja:
                return []

            # [ASCENSION 11]: STRING GUARD
            # If we are inside a string *within* the Jinja block, silence.
            # (Note: ctx.is_inside_string usually tracks global state, but Jinja has internal strings)
            # Simple heuristic: count quotes in the jinja fragment
            jinja_frag = ctx.line_prefix.split('{{')[-1]
            if (jinja_frag.count('"') % 2 != 0) or (jinja_frag.count("'") % 2 != 0):
                return []

            suggestions = []

            # Check for Pipe Context (Filter Mode)
            is_filter_mode = bool(self.PIPE_PATTERN.search(jinja_frag))

            if is_filter_mode:
                # --- MODE A: FILTERS ---
                suggestions.extend(self._prophesy_filters())
            else:
                # --- MODE B: SOURCES (Functions & Variables) ---
                suggestions.extend(self._prophesy_functions())
                suggestions.extend(self._prophesy_local_variables(ctx.full_content))
                suggestions.extend(self._prophesy_jinja_keywords())

            return suggestions

        except Exception as e:
            # [ASCENSION 12]: FAULT ISOLATION
            Logger.error(f"Alchemical Prophecy Fractured: {e}")
            return []

    # =========================================================================
    # == RITES OF SCRYING                                                    ==
    # =========================================================================

    def _prophesy_filters(self) -> List[CompletionItem]:
        """Scries the Canon for registered Filters."""
        if not self.canon: return []

        items = []
        for filt in self.canon.alchemist_filters:
            name = filt.get("name")
            desc = filt.get("description", "Alchemical Filter")

            # [ASCENSION 9]: PRIORITY
            # Filters are Tier 00 when after a pipe.

            items.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Method,  # Filters act like methods
                detail="Filter",
                documentation={"kind": "markdown", "value": f"**Filter: {name}**\n{desc}"},
                insertText=f"{name} ",  # Add space for flow
                sortText=f"00-filter-{name}",
                filterText=name
            ))
        return items

    def _prophesy_functions(self) -> List[CompletionItem]:
        """Scries the Canon for registered Globals."""
        if not self.canon: return []

        items = []
        for func in self.canon.alchemist_functions:
            name = func.get("name")
            desc = func.get("description", "Global Function")
            syntax = func.get("syntax", f"{name}()")  # e.g. "env(key, default=None)"

            # [ASCENSION 4]: SNIPPET SYNTHESIS
            snippet = self._forge_signature_snippet(name, syntax)

            items.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Function,
                detail="Global Function",
                documentation={"kind": "markdown", "value": f"**Function: {name}**\n{desc}\n\n`{syntax}`"},
                insertText=snippet,
                insertTextFormat=InsertTextFormat.Snippet,
                sortText=f"01-func-{name}",  # Tier 01 (After variables)
                filterText=name
            ))
        return items

    def _prophesy_local_variables(self, content: str) -> List[CompletionItem]:
        """
        [ASCENSION 5]: LOCAL SCAN
        Scans the current buffer for `$$` definitions to offer immediate access.
        """
        items = []
        seen = set()

        for match in self.VAR_PATTERN.finditer(content):
            name = match.group("name")
            if name in seen: continue

            type_hint = (match.group("type") or "").strip()
            detail = "Local Variable"
            if type_hint: detail += f" : {type_hint}"  # [ASCENSION 6]: TYPE HOLOGRAPHY

            items.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Variable,
                detail=detail,
                insertText=name,
                sortText=f"00-var-{name}",  # Tier 00 (Highest Priority)
                filterText=name,
                documentation=f"Variable defined in current scripture."
            ))
            seen.add(name)

        return items

    def _prophesy_jinja_keywords(self) -> List[CompletionItem]:
        """[ASCENSION 7]: JINJA CONSTANTS"""
        keywords = [
            ("true", "Boolean True"),
            ("false", "Boolean False"),
            ("none", "Null Value"),
            ("loop", "Iteration Context"),
            ("self", "Template Context")
        ]
        return [
            CompletionItem(
                label=k,
                kind=CompletionItemKind.Keyword,
                detail=d,
                insertText=k,
                sortText=f"10-kw-{k}",
                filterText=k
            ) for k, d in keywords
        ]

    # =========================================================================
    # == ALCHEMICAL UTILITIES                                                ==
    # =========================================================================

    def _forge_signature_snippet(self, name: str, syntax: str) -> str:
        """
        Transmutes a Python signature string into a VS Code Snippet.
        Input: "env(key, default=None)"
        Output: "env(${1:key}, ${2:default})"
        """
        if "(" not in syntax: return f"{name}()"

        # Extract args string: "key, default=None"
        try:
            args_str = syntax.split("(", 1)[1].rsplit(")", 1)[0]
            if not args_str.strip(): return f"{name}()"

            # Split by comma, respecting nested parens (naive split ok for simple sigs)
            args = [a.strip() for a in args_str.split(",")]

            snippet_parts = []
            for i, arg in enumerate(args):
                # Clean arg (remove type hints or defaults for the label)
                # "key: str" -> "key"
                # "default=None" -> "default"
                clean_arg = arg.split(":")[0].split("=")[0].strip()
                snippet_parts.append(f"${{{i + 1}:{clean_arg}}}")

            return f"{name}({', '.join(snippet_parts)})"
        except:
            # Fallback if parsing fails
            return f"{name}($1)"