# Path: core/lsp/scaffold_features/rename/mutators/local.py
# ---------------------------------------------------------
import re
from typing import Optional, List, Dict
from ....base.features.rename.contracts import RenameMutator, RenameContext
from ....base.features.rename.models import WorkspaceEdit, TextEdit, Range, Position
from ....document import TextDocument


class LocalMutator(RenameMutator):
    """[THE SURGICAL SCRIBE] Renames symbols in the current buffer."""

    @property
    def name(self) -> str:
        return "LocalScribe"

    @property
    def priority(self) -> int:
        return 100

    def provide_edits(self, doc: TextDocument, ctx: RenameContext) -> Optional[WorkspaceEdit]:
        # Purify identities
        old = ctx.original_name.replace("{{", "").replace("}}", "").replace("$$", "").strip()
        new = ctx.new_name.replace("{{", "").replace("}}", "").replace("$$", "").strip()

        # [ASCENSION 5]: Sigil-Aware Identifier Logic
        # Matches $$ var, let var, or {{ var }}
        # Uses word boundaries to avoid 'id' matching 'user_id'
        pattern = re.compile(rf'(?<![\w]){re.escape(old)}(?![\w])')

        edits = []
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('#'): continue

            for match in pattern.finditer(line):
                # Verify Alchemical Aura: Is it a definition or inside braces?
                is_def = line.lstrip().startswith(('$$', 'let', 'def'))

                # Check for Jinja enclosure
                prefix = line[:match.start()]
                is_jinja = prefix.count("{{") > prefix.count("}}")

                if is_def or is_jinja:
                    edits.append(TextEdit(
                        range=Range(
                            start=Position(line=i, character=match.start()),
                            end=Position(line=i, character=match.end())
                        ),
                        newText=new
                    ))

        if not edits: return None
        return WorkspaceEdit(changes={doc.uri: edits})