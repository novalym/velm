# Path: core/lsp/scaffold_features/references/providers/inclusion.py
# ----------------------------------------------------------------------
import re
from pathlib import Path
from typing import List, Any
from ....base.features.references.contracts import ReferenceProvider
from ....base.features.references.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo
from ....base.utils.uri import UriUtils


class InclusionProvider(ReferenceProvider):
    """[THE MATTER TRACKER] Finds references to file paths."""

    @property
    def name(self) -> str:
        return "InclusionTracker"

    @property
    def priority(self) -> int:
        return 90

    def find_references(self, doc: TextDocument, info: WordInfo, context: Any) -> List[Location]:
        # Triage: Does the word look like a path?
        if info.kind != 'path' and '/' not in info.text: return []

        target_path_str = info.text.strip("\"'")
        if not target_path_str: return []

        # [ASCENSION 8]: SEARCH THE CURRENT FILE FOR PATH ECHOES
        # Find every line where this path is mentioned with an operator
        pattern = re.compile(rf'([\'"])({re.escape(target_path_str)})\1')

        locations = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            if any(op in line for op in ("::", "<<", "->", "@include")):
                for match in pattern.finditer(line):
                    locations.append(Location(
                        uri=doc.uri,
                        range=Range(
                            start=Position(line=i, character=match.start(2)),
                            end=Position(line=i, character=match.end(2))
                        )
                    ))

        return locations