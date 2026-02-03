# Path: core/lsp/scaffold_features/code_action/providers/refactor_surgeon.py
# ---------------------------------------------------------------------------

import uuid
from typing import List, Optional
from ....base.features.code_action.contracts import CodeActionProvider
from ....base.features.code_action.models import CodeAction, CodeActionKind, Diagnostic
from ....base.document import TextDocument
from ....base.types.primitives import Range, Command

class RefactorSurgeonProvider(CodeActionProvider):
    """
    [THE SURGEON]
    Focuses on structural transmutations based on selections.
    """
    @property
    def name(self) -> str: return "RefactorSurgeon"
    @property
    def priority(self) -> int: return 70

    def provide_actions(self, doc: TextDocument, range: Range, diagnostics: List[Diagnostic]) -> List[CodeAction]:
        # Only offer refactoring if a range (block of code) is selected
        if range.start.line == range.end.line and range.start.character == range.end.character:
            return []

        return [
            # --- RITE 1: EXCISE TO FRAGMENT ---
            CodeAction(
                title="✨ Excise Gnosis to @include fragment",
                kind=CodeActionKind.RefactorExtract,
                command=Command(
                    title="Extract Fragment",
                    command="scaffold.refactor.extract",
                    arguments=[
                        doc.uri,
                        range.model_dump(),
                        {"strategy": "fragment", "auto_name": True}
                    ]
                )
            ),
            # --- RITE 2: CONVERT TO TRAIT ---
            CodeAction(
                title="🧬 Transmute selection to reusable %% trait",
                kind=CodeActionKind.RefactorRewrite,
                command=Command(
                    title="Convert to Trait",
                    command="scaffold.refactor.to_trait",
                    arguments=[
                        doc.uri,
                        range.model_dump()
                    ]
                )
            )
        ]

    def resolve_action(self, action: CodeAction) -> CodeAction: return action

