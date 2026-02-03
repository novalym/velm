# Path: core/lsp/features/workspace/folders/__init__.py
# ------------------------------------------------------
"""
=================================================================================
== THE MAP ROOM (V-Ω-WORKSPACE-FOLDERS-V12)                                    ==
=================================================================================
The sovereign authority for spatial reality.
Orchestrates the anchoring and severance of project sanctums.
"""
from .manager import FolderManager
from .models import WorkspaceFolder, FolderMetadata
from .scryer import RealityScryer

__all__ = ["FolderManager", "WorkspaceFolder", "FolderMetadata", "RealityScryer"]