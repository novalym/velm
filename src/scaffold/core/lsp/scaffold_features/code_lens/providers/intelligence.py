# Path: core/lsp/scaffold_features/code_lens/providers/intelligence.py
# --------------------------------------------------------------------
import re
from typing import List
from ....base.features.code_lens.contracts import CodeLensProvider
from ....features.code_lens.models import CodeLens, Range, Position, Command


class IntelligenceProvider(CodeLensProvider):
    """[THE ORACLE] Projects AI and Reference insights."""

    @property
    def name(self) -> str:
        return "GnosticIntelligence"

    @property
    def priority(self) -> int:
        return 50

    # Matches: $$ var_name
    VAR_PATTERN = re.compile(r'^\s*\$\$\s*([a-zA-Z_]\w*)')

    def provide_lenses(self, doc) -> List[CodeLens]:
        lenses = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            # 1. Reference Counting for Variables
            match = self.VAR_PATTERN.match(line)
            if match:
                var_name = match.group(1)
                # [ASCENSION 11]: Fast local scry for usages
                usage_count = len(re.findall(rf'\{{\{{\s*{re.escape(var_name)}\b', doc.text))

                rng = Range(
                    start=Position(line=i, character=0),
                    end=Position(line=i, character=5)
                )

                lenses.append(CodeLens(
                    range=rng,
                    command=Command(
                        title=f"🔗 {usage_count} references",
                        command="editor.action.showReferences",
                        arguments=[doc.uri, Position(line=i, character=line.find(var_name)), []]
                    )
                ))

            # 2. [ASCENSION 10]: AI Muse Hook for complex blocks
            if "@if" in line or "@for" in line:
                rng = Range(start=Position(line=i, character=0), end=Position(line=i, character=1))
                lenses.append(CodeLens(
                    range=rng,
                    command=Command(title="🔮 Explain Logic", command="scaffold.muse.explain", arguments=[doc.uri, i])
                ))

        return lenses