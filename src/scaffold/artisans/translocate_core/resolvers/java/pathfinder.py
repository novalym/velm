# // scaffold/artisans/translocate_core/resolvers/java/pathfinder.py
# ------------------------------------------------------------------

from pathlib import Path
from typing import Optional


class JavaPathfinder:
    """
    The Geometrician of the JVM.
    Maps file paths to package names based on source roots.
    """

    # Common Java Source Roots
    SRC_ROOTS = ["src/main/java", "src/test/java", "src"]

    def __init__(self, project_root: Path):
        self.root = project_root

    def file_to_package(self, path: Path) -> Optional[str]:
        """
        src/main/java/com/example/App.java -> com.example.App
        """
        # Try to find which source root contains this file
        for src in self.SRC_ROOTS:
            root_path = self.root / src
            if path.is_relative_to(root_path):
                rel = path.relative_to(root_path)
                # Remove extension and replace / with .
                return str(rel.with_suffix('')).replace('/', '.')

        return None

    def package_to_file(self, package_path: str) -> Optional[Path]:
        """
        com.example.App -> src/main/java/com/example/App.java
        """
        rel_path = package_path.replace('.', '/') + ".java"

        # Check all roots
        for src in self.SRC_ROOTS:
            candidate = self.root / src / rel_path
            if candidate.exists():
                return candidate
        return None