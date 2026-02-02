# Path: core/lsp/scaffold_features/rename/mutators/cortex.py
# ----------------------------------------------------------
from typing import Optional, Dict, List
from pathlib import Path
from ....base.features.rename.contracts import RenameMutator, RenameContext
from ....base.features.rename.models import WorkspaceEdit, TextEdit, Range, Position
from ....document import TextDocument
from ....base.utils.uri import UriUtils


class CortexMutator(RenameMutator):
    """[THE CAUSAL WEAVER] Propagates renames across the monorepo."""

    @property
    def name(self) -> str:
        return "CortexWeaver"

    @property
    def priority(self) -> int:
        return 50

    def provide_edits(self, doc: TextDocument, ctx: RenameContext) -> Optional[WorkspaceEdit]:
        # [ASCENSION 4]: THE ADRENALINE BRIDGE
        if not hasattr(self.server, 'relay_request'): return None

        # Request the Daemon to find all cross-file references
        # This uses the 'References' engine logic in the Daemon
        params = {
            "file_path": str(UriUtils.to_fs_path(ctx.uri)),
            "symbol": ctx.original_name.replace("{", "").replace("}", "").replace("$", "").strip(),
            "new_name": ctx.new_name.replace("{", "").replace("}", "").replace("$", "").strip(),
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_RENAME", "trace_id": ctx.trace_id}
        }

        try:
            # Synchronous plea across the Silver Cord
            response = self.server.relay_request("rename", params)
            if response and response.get('success'):
                # Transmute Daemon response to WorkspaceEdit
                return WorkspaceEdit.model_validate(response.get('data'))
        except:
            pass

        return None