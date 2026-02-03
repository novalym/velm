# Path: scaffold/core/jurisprudence/vows/base.py
# ----------------------------------------------

import os
from pathlib import Path
from typing import Any, Dict, Optional, List

from ..contracts import AdjudicationContext
from ....logger import Scribe

Logger = Scribe("BaseVowHandler")


class BaseVowHandler:
    """
    =============================================================================
    == THE GNOSTIC ADAPTER (V-Ω-SANCTUM-AWARE-ULTIMA)                          ==
    =============================================================================
    LIF: 10,000,000,000,000

    The Ancestral Soul of all Vow Handlers. It is now a master of Gnostic
    relativity, understanding that Truth is dependent on Location.
    """

    def __init__(self, context: AdjudicationContext):
        self.context = context

    @property
    def root(self) -> Path:
        """The immutable, physical root of the project sanctum."""
        return self.context.project_root

    @property
    def active_sanctum(self) -> Path:
        """
        [THE CORE FIX] The Gaze of the Active Sanctum.
        This property now correctly perceives the Symphony's current working
        directory from the Adjudication Context, which was bestowed by the
        GnosticContextManager. This is the one true source of location.
        """
        # AdjudicationContext now carries the cwd.
        return self.context.cwd

    @property
    def variables(self) -> Dict[str, Any]:
        return self.context.variables

    @property
    def last_reality(self) -> Optional[Any]:
        return self.context.last_process_result

    def _resolve(self, path_str: str) -> Path:
        """
        [FACULTY 2] The Forensic Path Gaze.
        Resolves a relative path string against the **Active Sanctum**.
        """
        p = Path(path_str)
        if p.is_absolute():
            resolved_path = p.resolve()
        else:
            resolved_path = (self.active_sanctum / path_str).resolve()

        Logger.verbose(
            f"Vow Path Gaze: '{path_str}' + Active Sanctum '{self.active_sanctum.name}' -> Resolved to '{resolved_path}'")
        return resolved_path

    def _check_virtual_existence(self, path_str: str) -> bool:
        """
        [FACULTY 3] The Virtual Reality Engine.
        Checks if the file exists in the Architect's Plan (Virtual Manifest).
        """
        virtual_manifest: List[str] = self.context.generated_manifest
        if not virtual_manifest:
            return False

        # We must resolve the path relative to the active sanctum to check it
        target_path = self._resolve(path_str)
        try:
            target_clean = str(target_path.relative_to(self.root)).replace('\\', '/')
        except ValueError:
            return False  # Path is outside the project root

        if target_clean in virtual_manifest:
            return True

        for virtual_path_str in virtual_manifest:
            if virtual_path_str.endswith(target_clean):
                return True

        return False

    def _read_gnostic_content(self, path: Path) -> Optional[str]:
        """
        [FACULTY 4] The Dual-Gaze of the Soul.
        Reads from the in-memory buffer (for patch/transmute) or disk.
        """
        # 1. Check Virtual Reality (Patch Buffer)
        if self.context.target_file_path and path.resolve() == self.context.target_file_path.resolve():
            if self.context.file_content_buffer is not None:
                return self.context.file_content_buffer

        # 2. Check Physical Reality (Disk)
        if path.exists() and path.is_file():
            try:
                return path.read_text(encoding='utf-8', errors='replace')
            except Exception:
                return None  # The Unbreakable Ward of Grace
        return None