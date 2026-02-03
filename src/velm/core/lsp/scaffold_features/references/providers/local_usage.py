# Path: core/lsp/scaffold_features/references/providers/local_usage.py
# ----------------------------------------------------------------------
import re
from typing import List, Any
from ....base.features.references.contracts import ReferenceProvider
from ....base.features.references.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo


class LocalUsageProvider(ReferenceProvider):
    """[THE LOCAL RESONATOR] Finds all usages within the current buffer."""

    @property
    def name(self) -> str:
        return "LocalUsage"

    @property
    def priority(self) -> int:
        return 100

    def find_references(self, doc: TextDocument, info: WordInfo, context: Any) -> List[Location]:
        # 1. Purify Target
        # {{ var }} -> var | $$ var -> var
        target = info.text.replace("{", "").replace("}", "").replace("$", "").strip()
        if not target: return []

        # [ASCENSION 7]: Precise Regex for Gnostic Particles
        # Matches the variable name surrounded by word boundaries or Jinja braces
        pattern = re.compile(rf'(?<![\w]){re.escape(target)}(?![\w])')

        locations = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            # Skip comments to avoid noise
            if line.strip().startswith('#'): continue

            for match in pattern.finditer(line):
                # Context Check: Ensure we are either at a definition site or in a Jinja block
                is_def = line.lstrip().startswith(('$$', 'let', 'def', 'const'))

                # Check for Jinja enclosure
                prefix = line[:match.start()]
                is_jinja = prefix.count("{{") > prefix.count("}}")

                if is_def or is_jinja:
                    locations.append(Location(
                        uri=doc.uri,
                        range=Range(
                            start=Position(line=i, character=match.start()),
                            end=Position(line=i, character=match.end())
                        )
                    ))

        return locations