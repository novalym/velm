# Path: core/lsp/scaffold_features/code_lens/providers/kinetic.py
# ---------------------------------------------------------------
import re
from typing import List
from ....base.features.code_lens.contracts import CodeLensProvider
from ....base.features.code_lens.models import CodeLens, Range, Position, Command


class KineticActionProvider(CodeLensProvider):
    """[THE MAESTRO'S HAND] Projects execution portals for >> and %%."""

    @property
    def name(self) -> str:
        return "KineticAction"

    @property
    def priority(self) -> int:
        return 90

    # Matches: >> command OR %% post-run
    PATTERN = re.compile(r'^\s*(>>|%%)\s*([\w\-\s]+)')

    def provide_lenses(self, doc) -> List[CodeLens]:
        lenses = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            match = self.PATTERN.match(line)
            if match:
                sigil = match.group(1)

                # Forge the Range (Top of the line)
                rng = Range(
                    start=Position(line=i, character=0),
                    end=Position(line=i, character=5)
                )

                if sigil == ">>":
                    lenses.append(CodeLens(
                        range=rng,
                        command=Command(
                            title="🚀 Run Command",
                            command="scaffold.runRite",
                            arguments=["shell_exec", {"cmd": line.strip().lstrip("> ")}]
                        )
                    ))
                elif "post-run" in line:
                    lenses.append(CodeLens(
                        range=rng,
                        command=Command(
                            title="🎼 Conduct Symphony",
                            command="scaffold.runRite",
                            arguments=["symphony", {"file": doc.uri}]
                        )
                    ))
        return lenses