# Path: core/lsp/scaffold_features/code_lens/providers/blueprint.py
# -----------------------------------------------------------------
import re
from typing import List
from ....base.features.code_lens.contracts import CodeLensProvider
from ....base.features.code_lens.models import CodeLens, Range, Position, Command


class BlueprintHealerProvider(CodeLensProvider):
    """[THE MEDIC] Projects redemption portals over Heresies."""

    @property
    def name(self) -> str:
        return "BlueprintHealer"

    @property
    def priority(self) -> int:
        return 100

    def provide_lenses(self, doc) -> List[CodeLens]:
        lenses = []
        # [ASCENSION 7]: Access the server's diagnostic ledger
        # This allows the lens to appear EXACTLY where the linter found a bug.
        diagnostics = self.server.diagnostics.ledger.get_merged(doc.uri)

        # Track lines already lensed to prevent clutter
        seen_lines = set()

        for diag in diagnostics:
            if diag.severity == 1:  # Critical
                line = diag.range.start.line
                if line in seen_lines: continue

                rng = Range(
                    start=Position(line=line, character=0),
                    end=Position(line=line, character=5)
                )

                lenses.append(CodeLens(
                    range=rng,
                    command=Command(
                        title="✨ Heal Heresy",
                        command="scaffold.heal",
                        arguments=[doc.uri, diag.model_dump()]
                    )
                ))
                seen_lines.add(line)

        # [ASCENSION 3]: Global Survey Lens
        lenses.append(CodeLens(
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=1)),
            command=Command(title="🔍 Survey Sanctum", command="scaffold.runRite", arguments=["survey", {}])
        ))

        return lenses