# // scaffold/artisans/translocate_core/resolvers/javascript/pathfinder.py
# ------------------------------------------------------------------------

import os
from pathlib import Path
from typing import Optional


class JSPathfinder:
    """
    The Geometrician of the Node Cosmos.
    """

    EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.json']

    def __init__(self, project_root: Path):
        self.root = project_root

    def is_node_module(self, specifier: str) -> bool:
        """
        Adjudicates if an import is a library (e.g. 'react') or local ('./utils').
        """
        if specifier.startswith('.'): return False
        if specifier.startswith('/'): return False  # Absolute path (rare but local)
        # Check for path aliases (e.g. @/ or ~/) - handled by TS subclass mostly
        if specifier.startswith('@/') or specifier.startswith('~/'): return False
        return True

    def resolve_absolute_path(self, context_file: Path, specifier: str) -> Optional[Path]:
        """
        Resolves a specifier to an absolute file path on disk.
        """
        # 1. Handle Relative
        base_dir = context_file.parent
        target_path = (base_dir / specifier).resolve()

        # 2. Probe for file existence (Exact, Extension, Index)
        return self._probe_file(target_path)

    def calculate_new_specifier(self, healee_path: Path, new_origin: Path) -> str:
        """
        Calculates the relative path from A to B.
        """
        try:
            rel = os.path.relpath(new_origin, healee_path.parent)
            # Normalize separators
            rel = rel.replace('\\', '/')

            # Ensure ./ prefix for siblings
            if not rel.startswith('.'):
                rel = f"./{rel}"

            # Strip extension if standard JS/TS
            base, ext = os.path.splitext(rel)
            if ext in self.EXTENSIONS:
                # Check for index
                if base.endswith('/index'):
                    return base[:-6] or '.'
                return base

            return rel
        except ValueError:
            return str(new_origin)  # Fallback

    def _probe_file(self, base_path: Path) -> Optional[Path]:
        # Exact match
        if base_path.is_file(): return base_path

        # Extensions
        for ext in self.EXTENSIONS:
            candidate = base_path.with_suffix(ext)
            if candidate.is_file(): return candidate

        # Index
        if base_path.is_dir():
            for ext in self.EXTENSIONS:
                candidate = base_path / f"index{ext}"
                if candidate.is_file(): return candidate

        return None