# Path: core/lsp/scaffold_features/completion/providers/variable_prophet.py
# -------------------------------------------------------------------------

import re
import logging
from typing import List, Any
from ....base.features.completion.contracts import CompletionProvider, CompletionContext
from ....base.features.completion.models import CompletionItem, CompletionItemKind

Logger = logging.getLogger("VariableProphet")


class VariableProphet(CompletionProvider):
    """
    =============================================================================
    == THE KEEPER OF NAMES (V-Ω-LOCAL-SCRYER-V12)                              ==
    =============================================================================
    [CAPABILITIES]:
    1. Scans the current buffer for `$$ var` definitions.
    2. Provides system built-ins (`now`, `env`, `project_root`).
    3. Triggered by `$` or inside `{{ }}`.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "VariableProphet"

    @property
    def priority(self) -> int:
        return 90

    def provide(self, ctx: CompletionContext) -> List[CompletionItem]:
        try:
            # [ASCENSION 1]: TRIGGER LOGIC
            # Trigger on '$' or inside Jinja blocks '{{ '
            is_jinja = "{{" in ctx.line_prefix and "}}" not in ctx.line_prefix
            is_var_sigil = ctx.trigger_character == '$' or ctx.line_prefix.endswith('$')

            if not (is_var_sigil or is_jinja):
                return []

            items = []

            # 1. LOCAL BUFFER SCAN (Regex Scry)
            # Find all: $$ var, let var, def var, const var
            var_pattern = re.compile(r'^\s*(?:\$\$|let|def|const)\s+([a-zA-Z_]\w*)', re.MULTILINE)
            local_vars = set(
                var_pattern.findall(ctx.line_text))  # Optimization: check current line first? No, full content needed.

            # [THE FIX]: We need full content, but ctx only gives line.
            # We must access the document from the server.
            doc = self.server.documents.get(ctx.uri)
            if doc:
                local_vars = set(var_pattern.findall(doc.text))

            for var in local_vars:
                items.append(CompletionItem(
                    label=var,
                    kind=CompletionItemKind.Variable,
                    detail="Local Gnosis",
                    insertText=var,
                    sortText=f"0-{var}",
                    documentation=f"Variable defined in {doc.uri.split('/')[-1]}"
                ))

            # 2. SYSTEM BUILT-INS
            builtins = [
                ("project_root", "Absolute path to the project anchor."),
                ("now", "Current timestamp."),
                ("env", "Access environment variables."),
                ("secret", "Generate cryptographic entropy."),
                ("scaffold_version", "The version of the God-Engine.")
            ]

            for name, doc in builtins:
                items.append(CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Constant,
                    detail="System Gnosis",
                    insertText=name,
                    sortText=f"1-{name}",
                    documentation=doc
                ))

            return items

        except Exception as e:
            Logger.error(f"Variable Prophecy Fractured: {e}")
            return []