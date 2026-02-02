# Path: core/lsp/scaffold_features/refactoring/handlers/rename_files.py
# ---------------------------------------------------------------------

import logging
from typing import List, Dict, Any
from pathlib import Path
from ....base.types import WorkspaceEdit, TextEdit, Range, Position
from ....base.utils.uri import UriUtils

Logger = logging.getLogger("AutoImportHealer")


class AutoImportHealer:
    """
    [THE BINDING MENDER]
    When a file moves, this artisan updates the cosmic web of imports.
    """

    def __init__(self, server: Any):
        self.server = server

    def calculate_edits(self, files: List[Any]) -> WorkspaceEdit:
        """
        Calculates the WorkspaceEdit required to fix imports.
        files: List of { oldUri, newUri }
        """
        if not hasattr(self.server, 'relay_request'):
            return WorkspaceEdit()

        all_changes: Dict[str, List[TextEdit]] = {}

        for file_op in files:
            old_uri = file_op.oldUri
            new_uri = file_op.newUri

            # [ASCENSION 1]: ASK THE DAEMON
            # "Who is importing this file?"
            try:
                # We reuse the 'references' rite but target the FILE PATH
                fs_path = str(UriUtils.to_fs_path(old_uri))

                params = {
                    "file_path": fs_path,
                    "symbol": "__FILE_REFERENCE__",  # Special signal
                    "project_root": str(self.server.project_root),
                    "metadata": {"source": "LSP_AUTO_IMPORT"}
                }

                response = self.server.relay_request("references", params)

                if not response or not response.get('success'):
                    continue

                # The Daemon returns locations of imports.
                # We must calculate the NEW relative path for each location.
                references = response.get('data', [])

                new_path_obj = UriUtils.to_fs_path(new_uri)

                for ref in references:
                    ref_uri = ref['uri']
                    # Don't update the file itself (it's moving)
                    if ref_uri == old_uri: continue

                    ref_file_path = UriUtils.to_fs_path(ref_uri)

                    # Calculate new relative import path
                    # From: ref_file_path.parent
                    # To: new_path_obj
                    # New Import: os.path.relpath(new_path_obj, ref_file_path.parent)
                    try:
                        new_rel_path = "./" + str(new_path_obj.relative_to(ref_file_path.parent)).replace('\\', '/')
                        # Strip extension for JS/TS/Py usually
                        new_rel_path = new_rel_path.rsplit('.', 1)[0]
                    except ValueError:
                        continue  # Cannot calculate relative path

                    # Forge Text Edit
                    if ref_uri not in all_changes: all_changes[ref_uri] = []

                    all_changes[ref_uri].append(TextEdit(
                        range=Range.model_validate(ref['range']),
                        newText=new_rel_path
                    ))

            except Exception as e:
                Logger.error(f"Import Healing Fractured: {e}")
                continue

        return WorkspaceEdit(changes=all_changes)