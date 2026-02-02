# Path: core/lsp/scaffold_features/code_action/providers/neural_healer.py
# ------------------------------------------------------------------------

from typing import List, Optional
from ....base.features.code_action.contracts import CodeActionProvider
from ....base.features.code_action.models import CodeAction, CodeActionKind, Diagnostic
from ....base.document import TextDocument
from ....base.types.primitives import Range, Command

class NeuralHealerProvider(CodeActionProvider):
    """
    [THE PROPHET]
    Summons the Neural Muse or AI Architect for generative healing of complex logic.
    """
    @property
    def name(self) -> str: return "NeuralHealer"
    @property
    def priority(self) -> int: return 40

    def provide_actions(self, doc: TextDocument, range: Range, diagnostics: List[Diagnostic]) -> List[CodeAction]:
        # If no diagnostics, we offer "Explanation" instead of "Healing"
        if not diagnostics:
            return [
                CodeAction(
                    title="🔮 Explain architectural logic (Neural Muse)",
                    kind=CodeActionKind.Refactor,
                    command=Command(
                        title="Neural Explanation",
                        command="scaffold.muse.explain",
                        arguments=[doc.uri, range.model_dump()]
                    )
                )
            ]

        # Offer Generative Healing for errors
        return [
            CodeAction(
                title="🧠 Conduct Neural Redemption on these heresies",
                kind=CodeActionKind.QuickFix,
                diagnostics=diagnostics,
                command=Command(
                    title="Neural Repair",
                    command="scaffold.architect.heal",
                    arguments=[
                        doc.uri,
                        [d.model_dump() for d in diagnostics]
                    ]
                )
            )
        ]

    def resolve_action(self, action: CodeAction) -> CodeAction: return action