# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/java_strategy.py
# -------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy
from ....utils import atomic_write

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class JavaStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE JAVA MAGISTRATE (V-Ω-PACKAGE-ENFORCER)                              ==
    =============================================================================
    The Guardian of the JVM.
    Enforces the Sacred Law: The `package` declaration must mirror the Sanctum's path.
    """

    def __init__(self):
        super().__init__("Java")
        # Common source roots to anchor the package calculation
        self.src_roots = ["src/main/java", "src/test/java", "src"]

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        if file_path.is_dir() or file_path.suffix != ".java":
            return

        # 1. Determine the expected package
        expected_package = self._calculate_package(file_path, project_root)
        if not expected_package:
            self.logger.verbose(
                f"   -> Could not determine source root for '{file_path.name}'. Skipping package enforcement.")
            return

        # 2. Read the Soul
        content = self._read_content(file_path, project_root, transaction)
        if not content: return

        # 3. Enforce the Law
        new_content = self._enforce_package_decl(content, expected_package)

        # 4. Inscribe changes if needed
        if new_content != content:
            self.logger.success(f"   -> Correcting Java Package: [green]{expected_package}[/green]")
            self._write_file(file_path, new_content, project_root, transaction)

    def _calculate_package(self, file_path: Path, project_root: Path) -> Optional[str]:
        """Calculates package name based on path relative to source root."""
        for root in self.src_roots:
            abs_root = project_root / root
            # Check if file is inside this root
            # We use str checks because is_relative_to implies existence in some python versions/contexts
            if str(file_path.resolve()).startswith(str(abs_root.resolve())):
                try:
                    rel_dir = file_path.parent.relative_to(abs_root)
                    if str(rel_dir) == ".": return ""
                    return str(rel_dir).replace("/", ".").replace("\\", ".")
                except ValueError:
                    continue
        return None

    def _enforce_package_decl(self, content: str, package_name: str) -> str:
        """Surgically updates or injects the package declaration."""
        package_decl = f"package {package_name};"

        # Regex to find existing package declaration
        # Matches: package com.example.foo;
        regex = re.compile(r"^\s*package\s+[\w.]+;", re.MULTILINE)

        if regex.search(content):
            # Replace existing
            return regex.sub(package_decl, content, count=1)
        else:
            # Prepend to top (preserving comments/license headers is hard without AST,
            # but we'll try to insert after comments if possible, or just at top)
            return f"{package_decl}\n\n{content}"

    def _read_content(self, path: Path, root: Path, tx) -> str:
        if tx:
            try:
                staged = tx.get_staging_path(path.relative_to(root))
                if staged.exists(): return staged.read_text('utf-8')
            except:
                pass
        if path.exists(): return path.read_text('utf-8')
        return ""

    def _write_file(self, path: Path, content: str, root: Path, tx):
        res = atomic_write(path, content, self.logger, root, transaction=tx, verbose=False)
        if tx and res.success:
            try:
                res.path = path.relative_to(root)
                tx.record(res)
            except:
                pass