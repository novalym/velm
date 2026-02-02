# Path: core/lsp/scaffold_features/definition/rules/file_links.py
# --------------------------------------------------------------
import re
from pathlib import Path
from typing import Optional, Union, List
from ....base.features.definition.contracts import DefinitionRule
from ....base.features.definition.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo
from ....base.utils.uri import UriUtils


class FileLinkRule(DefinitionRule):
    """[THE MATTER MIGRATOR] Resolves file paths to their physical origins."""

    @property
    def name(self) -> str:
        return "FileLink"

    @property
    def priority(self) -> int:
        return 90

    def matches(self, info: WordInfo) -> bool:
        # Only relevant for paths or lines with file operators
        return info.kind == 'path' or any(op in info.line_text for op in ("::", "<<", "->", "@include"))

    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Location]:
        # Clean the path string
        path_str = info.text.strip("\"'")
        if not path_str: return None

        # [ASCENSION 1]: ISOMORPHIC ANCHORING
        project_root = self.server.project_root
        if not project_root: return None

        try:
            # Resolve the candidate path
            target_path = (project_root / path_str).resolve()

            # [ASCENSION 7]: SHADOW VAULT AWARENESS
            # If not on disk, check the staging area
            if not target_path.exists():
                shadow = project_root / ".scaffold" / "staging" / path_str
                if shadow.exists(): target_path = shadow

            if target_path.exists():
                return Location(
                    uri=UriUtils.to_uri(target_path),
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=0, character=0)
                    )
                )
        except:
            pass
        return None