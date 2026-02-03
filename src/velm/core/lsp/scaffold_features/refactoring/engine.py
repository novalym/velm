# Path: core/lsp/scaffold_features/refactoring/engine.py
# ------------------------------------------------------

from typing import Any
from .handlers.rename_files import AutoImportHealer


class RefactoringEngine:
    """
    =============================================================================
    == THE REFACTORING ENGINE (V-Ω-KINETIC-MUTATOR)                            ==
    =============================================================================
    LIF: 10,000,000 | ROLE: FILE_SYSTEM_OVERSEER

    Manages the physical mutation of the project structure and the healing of
    references (Imports) when files are moved or renamed.
    """

    @staticmethod
    def forge(server: Any) -> 'RefactoringEngine':
        engine = RefactoringEngine(server)

        # [ASCENSION]: CONSECRATION
        # We tell the client we care about file operations
        server.register_capability(lambda caps: setattr(caps.workspace, 'fileOperations', {
            "willRename": {
                "filters": [{
                    "pattern": {"glob": "**/*"}
                }]
            }
        }))

        return engine

    def __init__(self, server: Any):
        self.server = server
        self.import_healer = AutoImportHealer(server)

    def on_will_rename_files(self, params: Any):
        """[RITE]: PRE-EMPTIVE HEALING"""
        return self.import_healer.calculate_edits(params.files)