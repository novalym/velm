# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/boundary_strategy.py
# -----------------------------------------------------------------------------------------------------

from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class BoundaryCheckStrategy(BaseStrategy):
    """
    =============================================================================
    == THE BOUNDARY GUARDIAN (V-Ω-GENERIC-SENTINEL)                            ==
    =============================================================================
    For languages that define their cosmos via a root-level manifest, this
    Guardian does not write files. Instead, it gazes upwards from a new scripture,
    ensuring it can perceive the project's sacred manifest. If not, it proclaims
    a heresy of orphanage.
    """

    def __init__(self, language_name: str, manifest_file: str):
        super().__init__(language_name)
        self.manifest_file = manifest_file

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        # [THE FIX] Handle directory targets correctly
        if file_path.is_dir():
            current = file_path
        else:
            current = file_path.parent

        found_manifest = False

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
                found_manifest = True
                break

            if current == current.parent: break
            current = current.parent

        if not found_manifest:
            # We warn, but do not halt. The Architect may be forging a new world.
            self.logger.warn(
                f"Structural Heresy: {self.language_name} file '{file_path.name}' is orphaned outside a '{self.manifest_file}' sanctum.")