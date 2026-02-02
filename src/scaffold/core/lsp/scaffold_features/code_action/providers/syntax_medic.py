# Path: core/lsp/scaffold_features/code_action/providers/syntax_medic.py
# -----------------------------------------------------------------------

import re
from typing import List, Optional
from ....base.features.code_action.contracts import CodeActionProvider
from ....base.features.code_action.models import CodeAction, CodeActionKind, Diagnostic, WorkspaceEdit, TextEdit
from ....base.document import TextDocument
from ....base.types.primitives import Range


class SyntaxMedicProvider(CodeActionProvider):
    """
    [THE MEDIC]
    Provides instant local skin-grafts for common grammar typos.
    Handles fixes that can be derived purely from the current text.
    """

    @property
    def name(self) -> str:
        return "SyntaxMedic"

    @property
    def priority(self) -> int:
        return 100

    def provide_actions(self, doc: TextDocument, range: Range, diagnostics: List[Diagnostic]) -> List[CodeAction]:
        actions = []
        for heresy in diagnostics:
            # --- FIX 1: Sigil Correction ($ -> $$) ---
            if heresy.code == "SYNTAX_SIGIL" and "$" in heresy.message:
                edit = TextEdit(range=heresy.range, newText="$$")
                actions.append(CodeAction(
                    title="Consecrate Sigil (Change '$' to '$$')",
                    kind=CodeActionKind.QuickFix,
                    diagnostics=[heresy],
                    isPreferred=True,
                    edit=WorkspaceEdit(changes={doc.uri: [edit]})
                ))

            # --- FIX 2: Jinja Spacing ({{var}} -> {{ var }}) ---
            if "spacing" in heresy.message.lower() and "{{" in doc.get_line(heresy.range.start.line):
                line = doc.get_line(heresy.range.start.line)
                # Naive spacing fix
                fixed_line = re.sub(r'\{\{\s*(.*?)\s*\}\}', r'{{ \1 }}', line)
                if fixed_line != line:
                    edit = TextEdit(
                        range=Range(
                            start=heresy.range.start,
                            end=heresy.range.end
                        ),
                        newText=fixed_line.strip()
                    )
                    actions.append(CodeAction(
                        title="Normalize Alchemical Spacing",
                        kind=CodeActionKind.QuickFix,
                        diagnostics=[heresy],
                        edit=WorkspaceEdit(changes={doc.uri: [edit]})
                    ))

        return actions

    def resolve_action(self, action: CodeAction) -> CodeAction:
        return action
