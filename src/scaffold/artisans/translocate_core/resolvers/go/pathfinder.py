# // scaffold/artisans/translocate_core/resolvers/go/pathfinder.py
import re
from pathlib import Path
from typing import Optional


class GoPathfinder:
    def __init__(self, project_root: Path):
        self.root = project_root
        self.module_name = self._read_go_mod()

    def _read_go_mod(self) -> Optional[str]:
        """Extracts the module name from go.mod."""
        go_mod = self.root / "go.mod"
        if not go_mod.exists(): return None
        content = go_mod.read_text(encoding="utf-8")
        match = re.search(r"^module\s+(.*)$", content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def resolve_file_path(self, import_path: str) -> Optional[Path]:
        """
        Transmutes a Go import path into a physical file path (directory).
        """
        if not self.module_name: return None

        # If it doesn't start with our module name, it's external (std or 3rd party)
        if not import_path.startswith(self.module_name):
            return None

        # Determine relative path from module root
        # import: "example.com/proj/pkg/utils"
        # module: "example.com/proj"
        # rel:    "pkg/utils"
        rel_path = import_path[len(self.module_name):].lstrip("/")

        candidate = (self.root / rel_path).resolve()
        return candidate if candidate.is_dir() else None

    def calculate_import_path(self, file_path: Path) -> str:
        """
        Calculates the Go import path for a specific directory.
        Go imports point to PACKAGES (directories), not files.
        """
        if not self.module_name: return ""

        # Ensure we are pointing to the directory containing the file
        directory = file_path if file_path.is_dir() else file_path.parent

        try:
            rel = directory.relative_to(self.root).as_posix()
            if rel == ".": return self.module_name
            return f"{self.module_name}/{rel}"
        except ValueError:
            return ""