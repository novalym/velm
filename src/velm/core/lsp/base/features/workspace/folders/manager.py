# Path: core/lsp/features/workspace/folders/manager.py
# ----------------------------------------------------
import logging
import threading
from typing import List, Dict, Optional, Any
from pathlib import Path

from .models import WorkspaceFolder, RootAura, FolderMetadata
from .scryer import RealityScryer
from ....utils.uri import UriUtils

Logger = logging.getLogger("FolderManager")


class FolderManager:
    """
    =============================================================================
    == THE CARTOGRAPHER (V-Ω-TOTALITY-V12)                                     ==
    =============================================================================
    LIF: 10,000,000 | ROLE: TOPOLOGICAL_GOVERNOR | RANK: SOVEREIGN

    Manages the multiple roots of reality.
    It is the absolute authority on which project "owns" a specific file.
    """

    def __init__(self, server: Any):
        self.server = server
        self._active_roots: Dict[str, WorkspaceFolder] = {}
        self._lock = threading.RLock()
        self.scryer = RealityScryer()

    def initialize(self, folders: List[Dict[str, Any]]):
        """
        [THE RITE OF INCEPTION]
        Mass-anchors reality during the server handshake.
        """
        if not folders: return

        with self._lock:
            # Transmute dicts to models
            added = [WorkspaceFolder.model_validate(f) for f in folders]
            self.update(added, [])

    def update(self, added: List[WorkspaceFolder], removed: List[WorkspaceFolder]):
        """
        [THE RITE OF SHIFTING]
        Surgically adds or prunes roots from the active constellation.
        """
        with self._lock:
            # 1. ANNIHILATION
            for folder in removed:
                norm_uri = UriUtils.normalize_uri(folder.uri)
                if norm_uri in self._active_roots:
                    del self._active_roots[norm_uri]
                    Logger.info(f"Reality Severed: {folder.name} (v{norm_uri})")

            # 2. GENESIS
            for folder in added:
                norm_uri = UriUtils.normalize_uri(folder.uri)

                # [ASCENSION 3 & 11]: SCRY FOR IDENTITY
                # If name is missing or generic, we scry the disk for the truth.
                fs_path = UriUtils.to_fs_path(norm_uri)
                if fs_path.exists():
                    folder.metadata.aura = self.scryer.divine_aura(fs_path)
                    if not folder.name or folder.name.startswith("Untitled"):
                        folder.name = self.scryer.divine_name(fs_path) or folder.name

                self._active_roots[norm_uri] = folder
                Logger.info(f"Reality Anchored: [{folder.metadata.aura.upper()}] {folder.name}")

    def get_owner(self, uri: str) -> Optional[WorkspaceFolder]:
        """
        [ASCENSION 2]: TOPOLOGICAL TRIAGE
        Finds the deepest root that contains the target URI.
        """
        norm_uri = UriUtils.normalize_uri(uri)

        with self._lock:
            # Collect all roots that are ancestors of this URI
            matches = [
                root for r_uri, root in self._active_roots.items()
                if norm_uri.startswith(r_uri)
            ]

            if not matches:
                return None

            # The deepest match (longest URI) is the true owner
            return max(matches, key=lambda r: len(r.uri))

    def resolve_primary_root(self) -> Optional[Path]:
        """
        [ASCENSION 4]: PRIMARY ANCHOR
        Returns the first root as the default project authority.
        """
        with self._lock:
            if not self._active_roots: return None
            # Return first as Path
            first_uri = next(iter(self._active_roots.keys()))
            return UriUtils.to_fs_path(first_uri)

    def list_folders(self) -> List[WorkspaceFolder]:
        """Returns the roster of all manifest realities."""
        with self._lock:
            return list(self._active_roots.values())

    def __len__(self) -> int:
        with self._lock:
            return len(self._active_roots)