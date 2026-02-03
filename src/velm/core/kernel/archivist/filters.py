# Path: scaffold/core/kernel/archivist/filters.py
# -----------------------------------------------

import os
import tarfile
from pathlib import Path
from typing import Optional, List, TYPE_CHECKING

from ...cortex.knowledge import KnowledgeBase

if TYPE_CHECKING:
    from . import ArchiveConfig

try:
    import pathspec

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False


class GnosticFilter:
    """
    =============================================================================
    == THE GAZE OF AVERSION (V-Ω-INTELLIGENT-FILTER)                           ==
    =============================================================================
    Decides what is worthy of preservation and what is mere entropy.
    It reads .gitignore and .scaffoldignore to maintain purity.
    """

    def __init__(self, root: Path, config: 'ArchiveConfig'):
        self.root = root
        self.config = config
        self.skipped_log: List[str] = []
        self.ignore_spec = self._load_ignore_specs()

    def _load_ignore_specs(self):
        """Loads and combines .gitignore and .scaffoldignore."""
        if not PATHSPEC_AVAILABLE:
            return None

        patterns = []

        # 1. Base Knowledge (Always ignore these)
        patterns.extend(KnowledgeBase.ABYSS_GLOBS)
        # We handle directories separately in filter_tarinfo, but globs help too

        # 2. .gitignore
        git_ignore = self.root / ".gitignore"
        if git_ignore.exists():
            try:
                with open(git_ignore, "r") as f:
                    patterns.extend(f.readlines())
            except:
                pass

        # 3. .scaffoldignore (Overrides)
        scaffold_ignore = self.root / ".scaffoldignore"
        if scaffold_ignore.exists():
            try:
                with open(scaffold_ignore, "r") as f:
                    patterns.extend(f.readlines())
            except:
                pass

        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)

    def filter_tarinfo(self, tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
        """The Atomic Judgment."""
        name = os.path.basename(tarinfo.name)
        # In tarfile filter, 'name' is the relative path inside the archive
        # We need to check if it matches our ignore patterns relative to root
        rel_path = tarinfo.name

        # 1. The Abyss Ward (Directories)
        if tarinfo.isdir():
            if name in KnowledgeBase.ABYSS_DIRECTORIES:
                return None
            if not self.config.include_git and name == ".git":
                return None
            if name in ['.scaffold', '__pycache__', 'node_modules', 'venv', '.venv', 'target', 'dist', 'build']:
                return None

        # 2. The Artifact Ward (Files)
        else:
            if name == "scaffold.lock": return None  # Prevent recursion
            if name.endswith(('.pyc', '.pyo', '.pyd', '.DS_Store', 'Thumbs.db')):
                return None

            # 3. The Heavyweight Gaze
            # Convert MB to bytes
            max_bytes = self.config.max_file_size_mb * 1024 * 1024
            if tarinfo.size > max_bytes:
                self.skipped_log.append(f"HEAVYWEIGHT: {rel_path} ({tarinfo.size} bytes)")
                return None

        # 4. The Gitignore Gaze
        if self.ignore_spec:
            if self.ignore_spec.match_file(rel_path):
                return None

        return tarinfo