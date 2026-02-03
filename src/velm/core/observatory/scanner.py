# Path: scaffold/core/observatory/scanner.py
# ------------------------------------------
import os
from pathlib import Path
from typing import List, Tuple, Optional
from .contracts import ProjectType


class PlanetaryScanner:
    """
    Scans the filesystem to discover unregistered realities.
    """

    IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'target', 'dist', 'build'}

    @staticmethod
    def scan(root: Path, max_depth: int = 2) -> List[Tuple[Path, ProjectType]]:
        """
        Recursively finds projects.
        Returns list of (Path, Type).
        """
        found = []
        root = root.resolve()

        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # Prune search
                dirnames[:] = [d for d in dirnames if d not in PlanetaryScanner.IGNORE_DIRS]

                current = Path(dirpath)
                try:
                    depth = len(current.relative_to(root).parts)
                except ValueError:
                    depth = 0

                if depth > max_depth:
                    continue

                # Heuristic Detection
                ptype = PlanetaryScanner._divine_type(current, filenames)
                if ptype:
                    found.append((current, ptype))
                    # Don't recurse into a project (monorepos handled separately in future)
                    dirnames[:] = []
        except PermissionError:
            pass

        return found

    @staticmethod
    def _divine_type(path: Path, files: List[str]) -> Optional[ProjectType]:
        if "scaffold.scaffold" in files or "scaffold.lock" in files:
            return ProjectType.GENERIC  # Explicitly managed
        if "pyproject.toml" in files or "requirements.txt" in files:
            return ProjectType.PYTHON
        if "package.json" in files:
            return ProjectType.NODE
        if "Cargo.toml" in files:
            return ProjectType.RUST
        if "go.mod" in files:
            return ProjectType.GO
        if ".git" in os.listdir(path):  # Check dir for git
            return ProjectType.GENERIC
        return None

