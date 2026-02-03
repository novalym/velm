# // scaffold/artisans/translocate_core/resolvers/rust/pathfinder.py
# ------------------------------------------------------------------

from pathlib import Path
from typing import Optional, Dict


class RustPathfinder:
    """
    Maps filesystem paths to Rust module paths (crate::...) and back.
    """

    def __init__(self, root: Path):
        self.root = root
        self.src = root / "src"

    def file_to_module(self, path: Path) -> Optional[str]:
        """
        src/main.rs -> crate
        src/lib.rs -> crate
        src/foo.rs -> crate::foo
        src/foo/mod.rs -> crate::foo
        """
        try:
            # Must be in src
            if not path.is_relative_to(self.src): return None

            rel = path.relative_to(self.src)
            parts = list(rel.with_suffix('').parts)

            # Normalize mod.rs
            if parts[-1] == 'mod': parts.pop()

            # Handle root files
            if not parts: return "crate"  # src/mod.rs? Rare.
            if parts == ['main'] or parts == ['lib']: return "crate"

            return "crate::" + "::".join(parts)

        except ValueError:
            return None

    def module_to_file(self, module_path: str) -> Optional[Path]:
        """
        crate::foo::bar -> src/foo/bar.rs OR src/foo/bar/mod.rs
        """
        if not module_path.startswith("crate"): return None

        if module_path == "crate":
            # Ambiguous: could be main.rs or lib.rs.
            # Resolvers usually don't import 'crate' directly like that in use statements.
            return None

        # crate::foo -> foo
        rel_mod = module_path.replace("crate::", "").replace("::", "/")

        # Check simple file
        candidate = self.src / f"{rel_mod}.rs"
        if candidate.exists(): return candidate

        # Check mod file
        candidate = self.src / rel_mod / "mod.rs"
        if candidate.exists(): return candidate

        return None

    def get_imported_module_path(self, use_path: str) -> str:
        """
        Extracts the module path from a use statement.
        use crate::foo::Bar -> crate::foo
        """
        # This is heuristic. We assume the last part is the Symbol, unless it's a module import.
        # Deep resolution requires AST analysis of the target file to see if it's a struct/func or mod.
        # For refactoring files (moving files), we mostly care about the prefix.
        return use_path  # simplified for V1