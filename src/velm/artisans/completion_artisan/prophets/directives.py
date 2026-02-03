# Path: artisans/completion_artisan/prophets/directives.py
# --------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_DIRECTIVE_PROPHET_DYNAMIC_V24
# SYSTEM: OCULAR_PROPHET | ROLE: DYNAMIC_STRUCTURE_MAGE
# =================================================================================

import logging
import re
from typing import List, Dict, Any, Optional

# --- IRON CORE UPLINKS ---
from .base import BaseProphet
from ....core.lsp.base.features.completion.contracts import CompletionContext
from ....core.lsp.base.features.completion.models import CompletionItem, CompletionItemKind, InsertTextFormat

Logger = logging.getLogger("DirectiveProphet")


class DirectiveProphet(BaseProphet):
    """
    =============================================================================
    == THE LOGIC GATEKEEPER (V-Ω-DYNAMIC-STRUCTURE)                            ==
    =============================================================================
    Prophesies control flow, structural directives, and polyglot blocks.
    It consults the LIVING CANON to find plugins and extensions.

    [MODES]:
    1. SCAFFOLD: Suggests @directives (Core + Plugins).
    2. SYMPHONY: Suggests Edicts (>>), Vows (??), and Polyglot (py:).
    """

    def prophesy(self, ctx: CompletionContext) -> List[CompletionItem]:
        try:
            # [ASCENSION 1]: SAFETY CHECK
            # We need the Canon to speak.
            if not self.canon: return []

            # [ASCENSION 5]: CONTEXTUAL GATING
            # Directives live at the root or block level, never inside Jinja or Comments.
            if ctx.is_inside_jinja or ctx.is_inside_comment:
                return []

            # Identify the trigger
            token = ctx.partial_token
            suggestions = []

            # --- MODE A: SCAFFOLD (.scaffold, .arch) ---
            if ctx.language_id in ('scaffold', 'arch'):
                # Trigger: @
                if token.startswith('@') or not token:
                    suggestions.extend(self._prophesy_scaffold(token))

            # --- MODE B: SYMPHONY (.symphony) ---
            elif ctx.language_id in ('symphony'):
                # Trigger: >> (Action), ?? (Vow), % (State), [a-z]: (Polyglot)

                # 1. EDICTS (>>)
                if token.startswith('>') or not token:
                    suggestions.extend(self._prophesy_edicts(token))

                # 2. VOWS (??)
                if token.startswith('?') or not token:
                    suggestions.extend(self._prophesy_vows(token))

                # 3. POLYGLOT (py:, rs:)
                # If we are at the start of a line (indentation only), suggest languages
                if not token.startswith(('>', '?', '%', '@')):
                    suggestions.extend(self._prophesy_polyglot(token))

            return suggestions

        except Exception as e:
            Logger.error(f"Directive Prophecy Fractured: {e}")
            return []

    # =========================================================================
    # == SCYING RITES                                                        ==
    # =========================================================================

    def _prophesy_scaffold(self, token: str) -> List[CompletionItem]:
        """Scries the Canon for Scaffold Directives (@if, @aws/...)."""
        items = []

        # Pull dynamic directives from the Runtime
        directives = self.canon.scaffold_directives

        for d in directives:
            name = d.get("token") or d.get("name")
            if not name: continue

            # [ASCENSION 11]: CORE DEDUPLICATION
            # Skip core logic gates that KeywordProphet handles better (static is faster)
            if name in ['@if', '@else', '@elif', '@for', '@macro', '@call', '@include']:
                continue

            if token and not name.startswith(token): continue

            # [ASCENSION 2]: SNIPPET SYNTHESIS
            snippet = self._forge_snippet(name, d.get("args", []), d.get("has_body", False))

            items.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Module,  # Directives act like modules
                detail="Dynamic Directive",
                documentation={
                    "kind": "markdown",
                    "value": d.get("description", "Runtime Extension") + f"\n\n**Syntax:** `{snippet}`"
                },
                insertText=snippet,
                insertTextFormat=InsertTextFormat.Snippet,
                # [ASCENSION 8]: SORT STRATIFICATION
                # "03" places it after Core Keywords ("00") but before Generics
                sortText=f"03-live-{name}",
                filterText=name
            ))

        return items

    def _prophesy_edicts(self, token: str) -> List[CompletionItem]:
        """Scries the Canon for Symphony Edicts (>>)."""
        items = []
        edits = self.canon.symphony_edicts

        for e in edits:
            name = e.get("token")
            if not name: continue

            # Filter
            if token and not name.startswith(token): continue

            # For '>>', we usually just append a space
            snippet = f"{name} ${{1:command}}"

            items.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Keyword,
                detail="Kinetic Action",
                documentation=e.get("description", "Execute intent."),
                insertText=snippet,
                insertTextFormat=InsertTextFormat.Snippet,
                sortText=f"00-edict-{name}",
                filterText=name
            ))
        return items

    def _prophesy_vows(self, token: str) -> List[CompletionItem]:
        """Scries the Canon for Symphony Vows (??)."""
        items = []
        vows = self.canon.symphony_vows  # Flattened list from Canon

        for v in vows:
            name = f"?? {v.get('name')}"  # Canon usually stores name without sigil
            sigil_name = v.get('token', name)  # Or uses token "?? name"

            # Normalize to sigil format
            if not sigil_name.startswith('??'): sigil_name = f"?? {sigil_name}"

            if token and not sigil_name.startswith(token): continue

            # Construct snippet with args
            args = v.get("args", [])
            snippet = self._forge_vow_snippet(sigil_name, args)

            items.append(CompletionItem(
                label=sigil_name,
                kind=CompletionItemKind.Interface,  # Vows are contracts
                detail="Gnostic Vow",
                documentation=v.get("description", "Assert reality."),
                insertText=snippet,
                insertTextFormat=InsertTextFormat.Snippet,
                sortText=f"01-vow-{sigil_name}",
                filterText=sigil_name
            ))
        return items

    def _prophesy_polyglot(self, token: str) -> List[CompletionItem]:
        """Scries the Canon for Language Blocks."""
        items = []
        # Fallback list if Canon is empty
        langs = self.canon.symphony_polyglot or [
            {"name": "python", "token": "py:"},
            {"name": "javascript", "token": "js:"},
            {"name": "rust", "token": "rs:"},
            {"name": "go", "token": "go:"},
            {"name": "bash", "token": "sh:"}
        ]

        for l in langs:
            tag = l.get("token")
            name = l.get("name")

            if token and not tag.startswith(token): continue

            snippet = f"{tag}\n\t$0"

            items.append(CompletionItem(
                label=tag,
                kind=CompletionItemKind.Class,  # Languages are classes of thought
                detail=f"Embedded {name}",
                insertText=snippet,
                insertTextFormat=InsertTextFormat.Snippet,
                sortText=f"10-polyglot-{tag}",
                filterText=tag
            ))
        return items

    # =========================================================================
    # == THE FORGE HELPERS                                                   ==
    # =========================================================================

    def _forge_snippet(self, name: str, args: List[str], has_body: bool) -> str:
        """
        [ASCENSION 2]: SNIPPET SYNTHESIS
        Constructs a dynamic snippet: @directive(arg1, arg2)
        """
        snippet = name

        # Argument Injection
        if args:
            arg_list = []
            for i, arg in enumerate(args):
                # ${1:arg_name}
                arg_list.append(f"${{{i + 1}:{arg}}}")
            snippet += f"({', '.join(arg_list)})"

        # Body Injection
        if has_body:
            # $0 is final cursor position
            snippet += "\n\t$0\n@end"

        return snippet

    def _forge_vow_snippet(self, name: str, args: List[str]) -> str:
        """Constructs: ?? vow: arg1"""
        snippet = name
        if args:
            snippet += ": "
            arg_list = []
            for i, arg in enumerate(args):
                arg_list.append(f"${{{i + 1}:{arg}}}")
            snippet += ", ".join(arg_list)
        return snippet