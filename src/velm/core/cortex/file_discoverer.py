# Path: core/cortex/file_discoverer.py
# ------------------------------------


import os
from pathlib import Path
from typing import List, Set, Optional

from .knowledge import KnowledgeBase
from .contracts import GnosticPath
from ...logger import Scribe
from ...utils import get_ignore_spec

try:
    from pathspec import PathSpec

    PATHSPEC_AVAILABLE = True
except ImportError:
    PATHSPEC_AVAILABLE = False

try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    scaffold_core_rs = None
    RUST_AVAILABLE = False

Logger = Scribe("GnosticPathfinder")


class FileDiscoverer:
    """
    =================================================================================
    == THE GNOSTIC PATHFINDER (V-Ω-DISCIPLINED-GAZE)                               ==
    =================================================================================
    LIF: 100,000,000,000,000

    The All-Seeing Eye of the Filesystem.
    It has been healed of the "Greedy Ancestor" heresy. It now gazes upwards only
    for specific, sacred scriptures, ignoring the noise of documentation libraries.
    """

    _iron_core_disabled = False

    def __init__(self, root: Path, ignore_patterns: Optional[List[str]] = None,
                 include_patterns: Optional[List[str]] = None):
        self.root = root.resolve()
        self.ignore_spec = get_ignore_spec(self.root, extra_patterns=ignore_patterns or [])
        self.visited_inodes: Set[int] = set()
        self.use_iron_core = RUST_AVAILABLE and not FileDiscoverer._iron_core_disabled
        self.include_spec = None
        if include_patterns:
            if PATHSPEC_AVAILABLE:
                self.include_spec = PathSpec.from_lines("gitwildmatch", include_patterns)
            else:
                self.simple_include_patterns = include_patterns

    def discover(self) -> List[Path]:
        """The Grand Rite of Discovery."""
        Logger.verbose(f"The Gnostic Pathfinder awakens its Gaze... (Iron Core: {self.use_iron_core})")

        if self.use_iron_core:
            discovered_files = self._discover_with_iron_core()
        else:
            discovered_files = self._discover_with_python_legacy()

        # [PILLAR II] The Ancestral Gaze
        ancestral_scriptures = self._gaze_upon_ancestry()

        # Unify and ensure uniqueness
        final_paths = {p.resolve(): p for p in discovered_files}
        for scripture in ancestral_scriptures:
            if scripture.resolve() not in final_paths:
                final_paths[scripture.resolve()] = scripture

        return list(final_paths.values())

    def _gaze_upon_ancestry(self) -> Set[Path]:
        """
        [PILLAR II: THE ORACLE OF ANCESTRAL WISDOM - HEALED]
        Performs a Gaze upwards to find Keystone Scriptures.

        THE FIX: It no longer recurses into directories. It only picks up
        explicit files defined in `KEYSTONES`.
        """
        ancestors = set()
        current = self.root

        # Stop at git root or 2 levels up
        git_root = None
        temp = current
        for _ in range(3):  # Search limit
            if (temp / ".git").is_dir():
                git_root = temp
                break
            if temp.parent == temp: break
            temp = temp.parent

        limit = git_root or current.parent.parent

        # The Sacred List of Ancestors
        KEYSTONES = {"README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "LICENSE"}

        while current != limit and current.parent != current:
            current = current.parent

            for name in KEYSTONES:
                candidate = current / name

                # We only accept FILES. We do not look into directories.
                if candidate.is_file() and candidate.exists():
                    if self._is_file_included(candidate):
                        ancestors.add(candidate)

        return ancestors

    def _discover_with_iron_core(self) -> List[Path]:
        try:
            records = scaffold_core_rs.scan_directory(str(self.root), False)
            files_to_process = []

            for record in records:
                path_str = record.path
                path = GnosticPath(path_str)
                path.init_gnosis(size=record.size, mtime=record.mtime, is_binary=record.is_binary)

                try:
                    rel = path.relative_to(self.root)
                    if any(part in KnowledgeBase.ABYSS_DIRECTORIES for part in rel.parts):
                        continue
                except ValueError:
                    pass

                if self._is_file_ignored(path): continue
                if not self._is_file_included(path): continue

                files_to_process.append(path)

            return files_to_process
        except Exception as e:
            Logger.error(f"The Iron Core faltered: {e}. Disabling Rust acceleration for this session.")
            FileDiscoverer._iron_core_disabled = True
            self.use_iron_core = False
            return self._discover_with_python_legacy()

    def _discover_with_python_legacy(self) -> List[Path]:
        files_to_process: List[Path] = []
        try:
            for current_root, dirs, files in os.walk(self.root, topdown=True):
                current_path = Path(current_root)

                try:
                    # Symlink loop protection
                    inode = current_path.stat().st_ino
                    if inode and inode in self.visited_inodes:
                        del dirs[:]
                        continue
                    self.visited_inodes.add(inode)
                except Exception:
                    pass

                # Prune the Abyss
                dirs[:] = [d for d in dirs if not self._is_dir_ignored(current_path, d)]

                for f_name in files:
                    file_path = current_path / f_name
                    if self._is_file_ignored(file_path): continue
                    if not self._is_file_included(file_path): continue
                    files_to_process.append(file_path)
        except PermissionError as e:
            Logger.warn(f"Pathfinder's Gaze averted by Permission Heresy: {e}")
        return files_to_process

    def _is_dir_ignored(self, parent: Path, dir_name: str) -> bool:
        if dir_name in KnowledgeBase.ABYSS_DIRECTORIES: return True
        if self.ignore_spec:
            full_path = parent / dir_name
            try:
                rel = str(full_path.relative_to(self.root)) + "/"
                if self.ignore_spec.match_file(rel): return True
            except ValueError:
                pass
        return False

    def _is_file_ignored(self, path: Path) -> bool:
        if path.name in KnowledgeBase.ABYSS_DIRECTORIES: return True
        try:
            rel_path = path.relative_to(self.root)
            if self.ignore_spec and self.ignore_spec.match_file(str(rel_path)): return True
        except ValueError:
            # If it's not relative (ancestral), we check its name against the abyss list only
            if any(part in KnowledgeBase.ABYSS_DIRECTORIES for part in path.parts):
                return True
        return False

    def _is_file_included(self, path: Path) -> bool:
        if not self.include_spec and not hasattr(self, 'simple_include_patterns'): return True
        try:
            rel_path_str = str(path.relative_to(self.root))
            if self.include_spec: return self.include_spec.match_file(rel_path_str)
            for pat in self.simple_include_patterns:
                if fnmatch.fnmatch(rel_path_str, pat): return True
            return False
        except ValueError:
            # For ancestral paths, check against the name as a fallback
            return any(fnmatch.fnmatch(path.name, pat) for pat in getattr(self, 'simple_include_patterns', []))