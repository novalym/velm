# // scaffold/artisans/translocate_core/resolvers/cpp/pathfinder.py
# -----------------------------------------------------------------

import os
from pathlib import Path
from typing import Optional


class CppPathfinder:
    """
    Handles relative path algebra for C++ headers.
    Assumes standard "relative to current file" inclusion for local headers.
    """

    def __init__(self, root: Path):
        self.root = root
        self.include_dirs = [root / "include", root / "src"]

    def resolve_origin(self, include_path: str, context_file: Path, kind: str) -> Optional[Path]:
        if kind == 'system': return None

        # 1. Check relative to current file
        candidate = (context_file.parent / include_path).resolve()
        if candidate.exists() and candidate.is_file():
            return candidate

        # 2. Check include paths (Common convention)
        for inc_dir in self.include_dirs:
            candidate = (inc_dir / include_path).resolve()
            if candidate.exists() and candidate.is_file():
                return candidate

        return None

    def calculate_new_include(self, healee_path: Path, new_origin: Path) -> str:
        """
        Calculates path from healee (source file) to origin (header).
        Uses quotes for relative paths.
        """
        try:
            rel = os.path.relpath(new_origin, healee_path.parent)
            rel = rel.replace('\\', '/')
            # Quotes usually imply relative to file or include path.
            # We stick to relative to file for maximum safety in refactoring.
            return f'"{rel}"'
        except ValueError:
            return f'"{new_origin.name}"'  # Fallback