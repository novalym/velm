# // scaffold/artisans/translocate_core/resolvers/ruby/pathfinder.py
# ------------------------------------------------------------------

import os
from pathlib import Path
from typing import Optional


class RubyPathfinder:
    """
    The Geometrician of Gems.
    Understands the convention of `lib/` as the root for `require`.
    """

    def __init__(self, root: Path):
        self.root = root
        self.lib_root = root / "lib"  # Standard Ruby convention

    def resolve_origin(self, path_str: str, context_file: Path, kind: str) -> Optional[Path]:
        """
        Resolves the require string to a physical file.
        """
        target = None

        if kind == 'relative':
            # Relative to the file itself
            base_dir = context_file.parent
            target = (base_dir / path_str).resolve()

        elif kind == 'absolute':
            # Relative to lib/ (Load Path)
            target = (self.lib_root / path_str).resolve()

        if target:
            # Ruby files often omit extension in require
            if not target.exists() and not target.suffix:
                target = target.with_suffix(".rb")

            if target.exists() and target.is_file():
                return target

        return None

    def calculate_new_require(self, healee_path: Path, new_origin: Path, kind: str) -> str:
        """
        Calculates the new string based on the import type.
        """
        # Strategy 1: If it was absolute (in lib/), try to keep it absolute
        if kind == 'absolute':
            try:
                rel_to_lib = new_origin.relative_to(self.lib_root)
                # Strip .rb extension
                return os.path.splitext(str(rel_to_lib))[0]
            except ValueError:
                # It moved out of lib! Must switch to relative.
                kind = 'relative'

        # Strategy 2: Relative
        if kind == 'relative':
            try:
                rel = os.path.relpath(new_origin, healee_path.parent)
                rel = rel.replace('\\', '/')
                # require_relative does NOT need ./ prefix, but it's safe.
                # However, idiomatic ruby usually omits ./ for require_relative 'subdir/file'
                # but needs it for siblings if not careful?
                # Actually require_relative 'sibling' works.
                # We'll normalize to standard posix path.
                if rel.startswith('.'):
                    # Keep ./ or ../
                    pass
                else:
                    rel = f"./{rel}"

                    # Strip extension
                return os.path.splitext(rel)[0]
            except ValueError:
                return str(new_origin)  # Fallback

        return ""