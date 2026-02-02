# Path: core/lsp/scaffold_features/definition/rules/stdlib.py
# -----------------------------------------------------------

from typing import Optional
from ....base.features.definition.contracts import DefinitionRule
from ....base.features.definition.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo


class StandardLibraryRule(DefinitionRule):
    """
    [THE ANCESTRAL ARCHIVE]
    Resolves navigation for built-in Alchemist functions.
    """
    STDLIB_ATOMS = {"env", "now", "secret", "shell", "read_file", "uuid"}

    @property
    def name(self) -> str: return "StdLib"

    @property
    def priority(self) -> int: return 10  # Low priority - let user variables shadow built-ins

    def matches(self, info: WordInfo) -> bool:
        # Strip braces to check if it's a built-in function name
        clean = info.text.replace("{{", "").replace("}}", "").strip().split('(')[0]
        return clean in self.STDLIB_ATOMS

    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Location]:
        # [ASCENSION 12]: VIRTUAL REALITY REDIRECTION
        # We jump to a virtual URI that Monaco can handle via a custom provider
        # to show documentation rather than a raw file.
        clean = info.text.replace("{{", "").replace("}}", "").strip().split('(')[0]

        return Location(
            uri=f"scaffold-docs://stdlib/{clean}",
            range=Range(start=Position(line=0, character=0), end=Position(line=0, character=0))
        )