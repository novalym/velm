# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/node_strategy.py
# -------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Set

from .base_strategy import BaseStrategy
from ....utils import atomic_write
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class NodeStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE NODE BARREL WEAVER (V-Ω-SEMANTIC-EXPORTER)                          ==
    =============================================================================
    The Guardian of the JavaScript/TypeScript Cosmos.
    1. Enforces Boundary: Ensures we are inside a `package.json` sanctum.
    2. Enforces Barrels: Automatically injects `export * from './File';` into `index` files.
    """

    def __init__(self, language_name: str, index_filename: str):
        super().__init__(language_name)
        self.index_filename = index_filename
        self.manifest_file = "package.json"

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        # 1. The Boundary Check (Inherited Wisdom)
        # We must ensure we are inside a valid project before creating files.
        if not self._verify_boundary(file_path, project_root, transaction):
            return

        # 2. The Semantic Registration
        # If we just added/moved a file, we should export it in the directory's index.
        if not file_path.is_dir() and file_path.name != self.index_filename:
            self._perform_barrel_registration(file_path, project_root, transaction)

    def _verify_boundary(self, file_path: Path, project_root: Path,
                         transaction: Optional["GnosticTransaction"]) -> bool:
        """Ensures we are within a valid package."""
        current = file_path.parent
        # Search upwards
        while current.is_relative_to(project_root) or current == project_root:
            manifest = current / self.manifest_file

            physical_exists = manifest.exists()
            virtual_exists = False
            if transaction:
                try:
                    staged = transaction.get_staging_path(manifest.relative_to(project_root))
                    virtual_exists = staged.exists()
                except ValueError:
                    pass

            if physical_exists or virtual_exists:
                return True

            if current == current.parent: break
            current = current.parent

        self.logger.warn(
            f"Structural Heresy: {self.language_name} file '{file_path.name}' is orphaned outside a '{self.manifest_file}' sanctum.")
        return False

    def _perform_barrel_registration(self, file_path: Path, project_root: Path,
                                     transaction: Optional["GnosticTransaction"]):
        """
        Injects `export * from './Filename';` into the parent index file.
        """
        # 1. The Gaze of Prudence
        if self._should_stay_hand(file_path):
            return

        # 2. The Gnostic Gaze (Check for Exports)
        content = self._read_content(file_path, project_root, transaction)
        if not self._has_exports(content):
            self.logger.verbose(f"   -> No exports perceived in '{file_path.name}'. Skipping barrel registration.")
            return

        # 3. The Rite of Injection
        index_file = file_path.parent / self.index_filename
        self._inject_export(index_file, file_path.stem, project_root, transaction)

    def _should_stay_hand(self, file_path: Path) -> bool:
        """Decides if a file is worthy of the barrel."""
        name = file_path.name
        if name.endswith(('.test.ts', '.test.js', '.spec.ts', '.spec.js')): return True
        if name.startswith('.'): return True  # Config/Hidden
        if name == "setupTests.ts": return True
        if "d.ts" in name: return False  # Type definitions SHOULD be exported
        return False

    def _has_exports(self, content: str) -> bool:
        """
        Simple heuristic: does the file contain 'export'?
        A future ascension could use Tree-sitter for precision.
        """
        return "export" in content

    def _read_content(self, path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> str:
        if transaction:
            try:
                rel_path = path.relative_to(project_root)
                staged_path = transaction.get_staging_path(rel_path)
                if staged_path.exists():
                    return staged_path.read_text(encoding='utf-8')
            except Exception:
                pass
        if path.exists():
            return path.read_text(encoding='utf-8')
        return ""

    def _inject_export(self, index_path: Path, module_name: str, project_root: Path,
                       transaction: Optional["GnosticTransaction"]):
        """
        Appends the export statement idempotently.
        """
        current_content = self._read_content(index_path, project_root, transaction)

        # The Semantic Export Line
        export_line = f"export * from './{module_name}';\n"

        # Idempotency Check (Simple String Matching)
        # We check for the module name in quotes to catch variants like `export { Foo } from './module'`
        if f"'{module_name}'" in current_content or f'"{module_name}"' in current_content:
            self.logger.verbose(f"   -> Exports for '{module_name}' already present in {self.index_filename}.")
            return

        # Append
        new_content = current_content
        if new_content and not new_content.endswith('\n'):
            new_content += "\n"

        new_content += export_line

        self.logger.success(f"   -> Injecting Barrel Export: [green]{export_line.strip()}[/green]")

        try:
            write_result = atomic_write(
                target_path=index_path,
                content=new_content,
                logger=self.logger,
                sanctum=project_root,
                transaction=transaction,
                verbose=False
            )

            if transaction and write_result.success:
                try:
                    logical_path = index_path.relative_to(project_root)
                    write_result.path = logical_path
                    transaction.record(write_result)
                except ValueError:
                    pass
        except Exception as e:
            self.logger.error(f"   -> Failed to inject exports into {index_path.name}: {e}")