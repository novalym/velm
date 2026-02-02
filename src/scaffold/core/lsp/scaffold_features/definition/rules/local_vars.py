# Path: core/lsp/scaffold_features/definition/rules/local_vars.py
# --------------------------------------------------------------
import re
from typing import Optional, Union, List
from ....base.features.definition.contracts import DefinitionRule
from ....base.features.definition.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo


class LocalVariableRule(DefinitionRule):
    """[THE KEEPER OF NAMES] Resolves variables in the current buffer."""

    @property
    def name(self) -> str:
        return "LocalVariable"

    @property
    def priority(self) -> int:
        return 100

    def matches(self, info: WordInfo) -> bool:
        # Matches tokens that look like variables, even without sigils
        return info.kind in ('variable', 'generic') and not '/' in info.text

    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Location]:
        # Clean the name: {{ var }} -> var, $$ var -> var
        clean_name = info.text.replace("{{", "").replace("}}", "").replace("$$", "").strip()
        if not clean_name: return None

        # [ASCENSION 2]: Instant Lexical Sweep
        # Search for: $$ clean_name = ... or let clean_name = ...
        pattern = re.compile(rf'^\s*(?:\$\$|let|def|const)\s+{re.escape(clean_name)}\b')

        lines = doc.text.splitlines()
        for i, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                # [ASCENSION 8]: Geometric Precision
                return Location(
                    uri=doc.uri,
                    range=Range(
                        start=Position(line=i, character=match.start()),
                        end=Position(line=i, character=match.end())
                    )
                )
        return None