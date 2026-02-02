# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/go_strategy.py
# -----------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy
from ....utils import atomic_write
from ....inquisitor import get_treesitter_gnosis

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class GoStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE GO GUARDIAN (V-Ω-WIRE-WEAVER)                                       ==
    =============================================================================
    1. Enforces `package <dirname>`.
    2. Scans for `// @scaffold:wire` markers to inject `New...` constructors.
    """

    def __init__(self):
        super().__init__("Go")
        self.marker = "@scaffold:wire"

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        if file_path.is_dir() or file_path.suffix != '.go':
            return

        content = self._read_content(file_path, project_root, transaction)
        if not content: return

        # 1. Package Consistency Check
        self._enforce_package_name(file_path, content, project_root, transaction)

        # 2. Dependency Injection Wiring
        self._perform_wire_injection(file_path, content, project_root, transaction)

    def _enforce_package_name(self, path: Path, content: str, root: Path, tx):
        """Ensures package name matches directory name (best practice)."""
        # Heuristic regex
        match = re.search(r"^package\s+(\w+)", content, re.MULTILINE)
        if match:
            pkg_name = match.group(1)
            dir_name = path.parent.name
            # Allow 'main' or matching name
            if pkg_name != "main" and pkg_name != dir_name:
                self.logger.warn(
                    f"Go Package Mismatch: '{path.name}' is in package '{pkg_name}', but directory is '{dir_name}'.")

    def _perform_wire_injection(self, source_file: Path, content: str, root: Path, tx):
        """
        Finds constructors (New...) and injects them into a marked wire set.
        """
        # A. Find Constructors in the new file
        # We use a simple regex heuristic for speed, or tree-sitter if available.
        # "func NewServiceName(...) *ServiceName"
        constructors = re.findall(r"func\s+(New[a-zA-Z0-9_]+)", content)
        if not constructors: return

        # B. Find the Wire File (in parent or root)
        # We look for a file containing the marker.
        wire_file = self._find_file_with_marker(source_file.parent, root, tx)
        if not wire_file:
            return

        # C. Inject
        self._inject_constructors(wire_file, constructors, root, tx)

    def _find_file_with_marker(self, start_dir: Path, root: Path, tx) -> Optional[Path]:
        current = start_dir
        while current.is_relative_to(root) or current == root:
            # Check files in this dir
            # Prioritize wire.go, main.go
            candidates = list(current.glob("*.go"))
            for cand in candidates:
                txt = self._read_content(cand, root, tx)
                if self.marker in txt:
                    return cand
            if current == root: break
            current = current.parent
        return None

    def _inject_constructors(self, target: Path, constructors: list[str], root: Path, tx):
        content = self._read_content(target, root, tx)

        new_content = content
        changes = 0

        for ctor in constructors:
            if ctor in content: continue

            # Injection Logic: Find the marker and append after it.
            # Marker: // @scaffold:wire
            # We assume the marker is inside a wire.NewSet(...) or similar list.

            replacement = f"{self.marker}\n\t{ctor},"
            # We assume it's in the same package scope or imported.
            # If different package, we'd need the package alias.
            # For V1, we assume simple injection.

            if self.marker in new_content:
                new_content = new_content.replace(self.marker, replacement)
                changes += 1

        if changes:
            self.logger.success(f"   -> Wired {changes} constructor(s) into {target.name}")
            self._write_file(target, new_content, root, tx)

    # ... Helper methods (_read_content, _write_file) duplicated from Rust/Python strategies for independence ...
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