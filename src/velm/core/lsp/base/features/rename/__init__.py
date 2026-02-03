# Path: core/lsp/features/rename/__init__.py
# ------------------------------------------

"""
=================================================================================
== THE HALL OF TRANSMUTATION (V-Ω-RENAME-CORE-V12)                             ==
=================================================================================
The engine responsible for safely rewriting reality.
It handles 'textDocument/rename' and 'textDocument/prepareRename'.

This is the PURE, language-agnostic foundation for reality shifting.
=================================================================================
"""

from .engine import RenameEngine
from .contracts import RenameMutator, RenameValidator
from .models import RenameParams, PrepareRenameParams, WorkspaceEdit, TextEdit

__all__ = [
    "RenameEngine",
    "RenameMutator",
    "RenameValidator",
    "RenameParams",
    "PrepareRenameParams",
    "WorkspaceEdit",
    "TextEdit"
]