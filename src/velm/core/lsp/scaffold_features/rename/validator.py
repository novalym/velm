# Path: core/lsp/scaffold_features/rename/validator.py
# -----------------------------------------------------
from typing import Optional
from ...base.features.rename.contracts import RenameValidator
from ...base.features.rename.models import Range
from ...document import TextDocument
from ...utils.text import WordInfo


class ScaffoldRenameValidator(RenameValidator):
    """
    [THE GUARDIAN OF PRUDENCE]
    Adjudicates whether a symbol is worthy of transmutation.
    """

    # Fundamental particles that cannot be renamed
    SACRED_KEYWORDS = {
        '$$', '%%', '::', '<<', '->', '@if', '@else', '@elif',
        '@endif', '@for', '@endfor', '@include', '@macro', '@call'
    }

    def validate(self, doc: TextDocument, info: WordInfo) -> Optional[Range]:
        # 1. Block Keyword Profanation
        if info.text in self.SACRED_KEYWORDS or info.kind == 'directive':
            return None

        # 2. Block Logic Atoms
        if info.text in ('true', 'false', 'null', 'None'):
            return None

        # 3. Allow Variables, Paths, and Generic Identifiers
        return info.range