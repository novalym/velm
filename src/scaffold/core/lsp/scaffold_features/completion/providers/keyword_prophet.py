# Path: core/lsp/scaffold_features/completion/providers/keyword_prophet.py
# ------------------------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_KEYWORD_PROPHET_APOTHEOSIS_V24
# SYSTEM: OCULAR_PROPHET | ROLE: SYNTAX_LAW_KEEPER | RANK: SOVEREIGN
# =================================================================================

import logging
import re
import time
from typing import List, Any, Optional, Dict
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem, CompletionItemKind, InsertTextFormat

Logger = logging.getLogger("KeywordProphet")

# =================================================================================
# == I. THE SACRED GRIMOIRE (IMMUTABLE SYNTAX PROTOTYPES)                        ==
# =================================================================================

SIGILS = [
    CompletionItem(
        label="$$", kind=CompletionItemKind.Keyword, detail="Define Variable",
        insertText="$$ ${1:name}: ${2|str,int,bool,list,dict,any|} = ${3:\"value\"}",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 10x**\nInscribes a unit of Gnostic memory into the project scope.",
        sortText="00-sigil-var", filterText="$$"
    ),
    CompletionItem(
        label="::", kind=CompletionItemKind.Operator, detail="Inline Content",
        insertText=":: \"${1:content}\"",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 1x**\nBinds textual soul directly to a physical path.",
        sortText="00-sigil-content", filterText="::"
    ),
    CompletionItem(
        label="<<", kind=CompletionItemKind.Operator, detail="Celestial Seed",
        insertText="<< ${1:./path/to/template}",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 50x**\nClones the soul of an external archetype.",
        sortText="00-sigil-seed", filterText="<<"
    ),
    CompletionItem(
        label="->", kind=CompletionItemKind.Operator, detail="Symbolic Link",
        insertText="-> ${1:target_path}",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 5x**\nForges a persistent link between two points in spacetime.",
        sortText="00-sigil-link", filterText="->"
    )
]

ROOT_DIRECTIVES = [
    CompletionItem(
        label="@if", kind=CompletionItemKind.Snippet, detail="Logic Gate",
        insertText="@if {{ ${1:condition} }}\n\t$0\n@endif",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 100x**\nBranches reality based on alchemical truth.",
        sortText="10-dir-if", filterText="@if"
    ),
    CompletionItem(
        label="@for", kind=CompletionItemKind.Snippet, detail="Iteration",
        insertText="@for ${1:item} in ${2:list}\n\t$0\n@endfor",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 100x**\nRepeats a structural pattern across a collection.",
        sortText="13-dir-for", filterText="@for"
    ),
    CompletionItem(
        label="@include", kind=CompletionItemKind.Module, detail="Composition",
        insertText="@include \"${1:path/to/fragment}\"",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**LIF: 20x**\nWeaves an external blueprint into this reality.",
        sortText="14-dir-include", filterText="@include"
    ),
    CompletionItem(
        label="@macro", kind=CompletionItemKind.Function, detail="Pattern Forge",
        insertText="@macro ${1:name}(${2:params})\n\t$0\n@endmacro",
        insertTextFormat=InsertTextFormat.Snippet,
        sortText="15-dir-macro", filterText="@macro"
    ),
    CompletionItem(
        label="@call", kind=CompletionItemKind.Function, detail="Invocation",
        insertText="@call ${1:name}(${2:args})",
        insertTextFormat=InsertTextFormat.Snippet,
        sortText="16-dir-call", filterText="@call"
    )
]

CONDITIONAL_DIRECTIVES = [
    CompletionItem(label="@elif", kind=CompletionItemKind.Snippet, detail="Branch",
                   insertText="@elif {{ ${1:condition} }}", insertTextFormat=InsertTextFormat.Snippet,
                   sortText="11-dir-elif", filterText="@elif"),
    CompletionItem(label="@else", kind=CompletionItemKind.Snippet, detail="Fallback", insertText="@else",
                   insertTextFormat=InsertTextFormat.Snippet, sortText="12-dir-else", filterText="@else"),
    CompletionItem(label="@endif", kind=CompletionItemKind.Snippet, detail="Seal", insertText="@endif",
                   insertTextFormat=InsertTextFormat.Snippet, sortText="12-dir-endif", filterText="@endif"),
]

MAESTRO_EXPANSIONS = [
    CompletionItem(
        label="%% post-run", kind=CompletionItemKind.Class, detail="After Manifest",
        insertText="%% post-run\n\t>> ${1:command}\n\t?? succeeds",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**Will: After**\nCommands to conduct once the matter is physically stable.",
        sortText="20-maestro-post", filterText="%%"
    ),
    CompletionItem(
        label="%% pre-run", kind=CompletionItemKind.Class, detail="Before Manifest",
        insertText="%% pre-run\n\t>> ${1:command}",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**Will: Before**\nCommands to conduct before matter is touched.",
        sortText="20-maestro-pre", filterText="%%"
    ),
    CompletionItem(
        label="%% trait", kind=CompletionItemKind.Struct, detail="Define Trait",
        insertText="%% trait ${1:Name}\n\t$0",
        insertTextFormat=InsertTextFormat.Snippet,
        documentation="**Form: Trait**\nDefines a reusable architectural gene.",
        sortText="20-maestro-trait", filterText="%%"
    )
]


class KeywordProphet(CompletionProvider):
    """
    =============================================================================
    == THE OMNISCIENT KEYWORD PROPHET (V-Ω-TOTALITY)                           ==
    =============================================================================
    """
    __slots__ = ['server']

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "KeywordProphet"

    @property
    def priority(self) -> int:
        return 100

    def provide(self, ctx: CompletionContext) -> List[CompletionItem]:
        try:
            # [ASCENSION 6]: CONTEXTUAL SILENCE
            if ctx.is_inside_comment or (ctx.is_inside_string and not ctx.is_inside_jinja):
                return []

            # [ASCENSION 1]: PERCENT-RESONANCE FIX
            # Extract the last non-whitespace atom using the virtual prefix
            token = ctx.line_prefix.strip().split()[-1] if ctx.line_prefix.strip() else ""

            # [ASCENSION 12]: IMMUTABLE CLONING RITE
            # Ensures we never profane the static Grimoire prototypes
            def _clone_and_align(items: List[CompletionItem]) -> List[CompletionItem]:
                results = []
                for item in items:
                    # [ASCENSION 2]: INDENTATION PHYSICS
                    # If snippet is multi-line, inject the current indentation
                    cloned = item.model_copy()
                    if '\n' in cloned.insert_text:
                        lines = cloned.insert_text.split('\n')
                        cloned.insert_text = lines[0] + '\n' + '\n'.join([f"{ctx.indent_str}{l}" for l in lines[1:]])
                    results.append(cloned)
                return results

            # =========================================================================
            # == INTELLIGENT ROUTING MATRIX                                          ==
            # =========================================================================

            # 1. SIGIL: '$' → '$$'
            if token.startswith('$'):
                return _clone_and_align([i for i in SIGILS if i.label == '$$'])

            # 2. SIGIL: '%' → THE MAESTRO EXPANSIONS (FIXED)
            if token.startswith('%'):
                # We return specific edicts if they start with % or %%.
                # This ensures first-keystroke resonance.
                return _clone_and_align(MAESTRO_EXPANSIONS)

            # 3. DIRECTIVE: '@' → THE LOGIC COUNCIL
            if token.startswith('@'):
                candidates = ROOT_DIRECTIVES[:]
                # [ASCENSION 8]: CONTEXTUAL FILTERING
                if self._scry_logic_anchor(ctx):
                    candidates.extend(CONDITIONAL_DIRECTIVES)

                if len(token) > 1:
                    return _clone_and_align([i for i in candidates if i.label.startswith(token)])
                return _clone_and_align(candidates)

            # 4. OPERATORS & FALLBACKS
            if any(token.startswith(c) for c in [':', '<', '-', '+', '^', '~']):
                # We scry the Operator Tier
                from .keyword_prophet import OPERATORS  # Reference to sibling list if needed
                # For brevity, assuming SIGILS + OPERATORS combined check
                return _clone_and_align(
                    [i for i in SIGILS + (OPERATORS if 'OPERATORS' in globals() else []) if i.label.startswith(token)])

            # 5. [ASCENSION 13]: KINETIC SEQUENCING (Vows)
            # If the current line is an Action (>>), suggest Vows (??)
            if ctx.line_prefix.strip().startswith('>>'):
                # (Assuming Vows are defined or we offer the generic sigil)
                vow_sigil = CompletionItem(
                    label="??", kind=CompletionItemKind.Keyword, detail="Assert Reality",
                    insertText="?? ${1|succeeds,file_exists,port_open|}",
                    insertTextFormat=InsertTextFormat.Snippet, sortText="00-vow"
                )
                return _clone_and_align([vow_sigil])

            # 6. ROOT GAZE (Empty Line)
            if not token:
                # Proclaim the Totality
                return _clone_and_align(SIGILS + ROOT_DIRECTIVES + MAESTRO_EXPANSIONS)

            return []

        except Exception as e:
            Logger.error(f"Keyword Prophecy Fractured: {e}")
            return []

    def _scry_logic_anchor(self, ctx: CompletionContext) -> bool:
        """
        [ASCENSION 3]: RECURSIVE SCOPE GAZE
        Checks if an @if or @for block is currently open at this indentation.
        """
        current_indent = len(ctx.indent_str.replace('\t', '    '))
        lines = ctx.full_content.splitlines()

        # [ASCENSION 22]: METABOLIC THRIFT
        # Limit lookback to preserve nanosecond interaction speeds
        lookback = 50

        for i in range(ctx.line_idx - 1, max(-1, ctx.line_idx - lookback), -1):
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith('#'): continue

            line_indent = len(line[:len(line) - len(stripped)].replace('\t', '    '))

            if line_indent < current_indent:
                return False  # We exited the scope of the parent

            if line_indent == current_indent:
                if stripped.startswith(('@if', '@elif')): return True
                if stripped.startswith(('@else', '@endif', '@endfor')): return False

        return False