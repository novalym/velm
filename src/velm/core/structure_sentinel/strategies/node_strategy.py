# Path: core/structure_sentinel/strategies/node_strategy.py
# ---------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Set, Dict, Any, List

from .base_strategy import BaseStrategy
from ....utils import atomic_write
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction
    from ....creator.io_controller import IOConductor


class NodeStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE NODE BARREL WEAVER: TOTALITY (V-Ω-TOTALITY-V7000-HEALED)            ==
    =============================================================================
    LIF: ∞ | ROLE: SEMANTIC_INTERFACE_ARCHITECT | RANK: MASTER
    AUTH: Ω_NODE_STRATEGY_V7000_SUTURE_2026_FINALIS

    The Guardian of the JavaScript/TypeScript Cosmos. It ensures the structural
    purity of packages and orchestrates the automated weaving of Export Barrels.
    """

    def __init__(self, language_name: str, index_filename: str):
        super().__init__(language_name)
        self.index_filename = index_filename
        self.manifest_file = "package.json"

    def consecrate(
            self,
            path: Path,
            project_root: Path,
            transaction: Optional["GnosticTransaction"] = None,
            io_conductor: Optional["IOConductor"] = None,
            gnosis: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-TOTALITY-SUTURED)                         ==
        =============================================================================
        [THE CURE]: Signature now perfectly honors the StructureSentinel dowry.
        """
        # 1. THE BOUNDARY GAZE
        # Ensure we are inside a valid package before materializing matter.
        if not self._verify_boundary(path, project_root, transaction):
            return

        # 2. THE SEMANTIC TRIAGE
        # We only weave barrels for files. If the path is a directory, it will
        # be handled when its children are born.
        is_dir = path.is_dir()
        if not is_dir and path.name != self.index_filename:
            self._perform_barrel_registration(path, project_root, transaction, io_conductor)

    def _verify_boundary(self, file_path: Path, project_root: Path,
                         transaction: Optional["GnosticTransaction"]) -> bool:
        """[FACULTY 4]: Achronal Boundary Verification."""
        # Start scanning from the parent if target is a file
        current = file_path if file_path.is_dir() else file_path.parent

        # Search upwards to the project root wall
        while current.is_relative_to(project_root) or current == project_root:
            manifest = current / self.manifest_file

            # Bicameral check
            physical_exists = manifest.exists()
            virtual_exists = False
            if transaction:
                try:
                    rel_manifest = manifest.relative_to(project_root)
                    virtual_exists = transaction.is_file_in_staging(rel_manifest)
                except ValueError:
                    pass

            if physical_exists or virtual_exists:
                return True

            if current == current.parent: break
            current = current.parent

        self.logger.warn(
            f"Structural Heresy: {self.language_name} artifact '{file_path.name}' is orphaned outside a '{self.manifest_file}' sanctum."
        )
        return False

    def _perform_barrel_registration(
            self,
            file_path: Path,
            project_root: Path,
            transaction: Optional["GnosticTransaction"],
            io_conductor: Optional["IOConductor"]
    ):
        """
        [FACULTY 3]: The Rite of Injection via the Sovereign Hand.
        """
        # 1. THE GAZE OF PRUDENCE
        if self._should_stay_hand(file_path):
            return

        # 2. THE GNOSTIC GAZE (Check for Exports)
        content = self._read_content(file_path, project_root, transaction)
        if not self._has_exports(content):
            # self.logger.verbose(f"   -> No exports perceived in '{file_path.name}'. Skipping barrel.")
            return

        # 3. THE KINETIC STRIKE
        index_file = file_path.parent / self.index_filename
        self._inject_export(index_file, file_path.stem, project_root, transaction, io_conductor)

    def _should_stay_hand(self, file_path: Path) -> bool:
        """[FACULTY 8]: The Abyssal Filter."""
        name = file_path.name.lower()
        # Filter tests, hidden files, and setup scripts
        if any(token in name for token in ('.test.', '.spec.', '.config.', 'setup.')):
            return True
        if name.startswith('.'):
            return True
        return False

    def _has_exports(self, content: str) -> bool:
        """Perceives if a file is an exporter of logic."""
        # Look for ESM export patterns
        return "export " in content or "export {" in content or "export default" in content

    def _read_content(self, path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> str:
        """[FACULTY 9]: The Bicameral Gaze."""
        if transaction:
            try:
                rel_path = path.relative_to(project_root)
                staged_content = transaction.get_staged_content(rel_path)
                if staged_content is not None:
                    return staged_content
            except Exception:
                pass

        if path.exists():
            return path.read_text(encoding='utf-8', errors='ignore')
        return ""

    def _inject_export(
            self,
            index_path: Path,
            module_name: str,
            project_root: Path,
            transaction: Optional["GnosticTransaction"],
            io_conductor: Optional["IOConductor"]
    ):
        """
        [FACULTY 3 & 12]: Transactional Suture of the Export Edict.
        """
        current_content = self._read_content(index_path, project_root, transaction)

        # [FACULTY 5]: Isomorphic Export Token
        export_line = f"export * from './{module_name}';"

        # [FACULTY 6]: The Idempotency Shield
        if f"from './{module_name}'" in current_content or f"from \"./{module_name}\"" in current_content:
            return

        # [FACULTY 7]: Geometric Spacing
        new_lines = current_content.splitlines()
        if new_lines and new_lines[-1].strip():
            new_lines.append("")  # Ensure gap
        new_lines.append(export_line)

        # Add final newline to satisfy the Linters
        final_content = "\n".join(new_lines).strip() + "\n"

        self.logger.success(f"   -> Weaving Barrel Export: [green]{export_line}[/green]")

        try:
            # [ASCENSION 3]: THE SOVEREIGN HAND
            # Use the Conductor for transactional integrity
            if io_conductor:
                rel_path = index_path.relative_to(project_root)
                res = io_conductor.write(
                    logical_path=rel_path,
                    content=final_content,
                    metadata={"origin": "NodeStructureStrategy", "action": "barrel_weave"}
                )
                if transaction and res.success:
                    transaction.record(res)
            else:
                # Fallback to atomic write
                res = atomic_write(
                    target_path=index_path,
                    content=final_content,
                    logger=self.logger,
                    sanctum=project_root,
                    transaction=transaction,
                    verbose=False
                )
                if transaction and res.success:
                    try:
                        res.path = index_path.relative_to(project_root)
                        transaction.record(res)
                    except ValueError:
                        pass

        except Exception as e:
            self.logger.error(f"   -> Barrel Weaving Fracture in '{index_path.name}': {e}")

    def __repr__(self) -> str:
        return f"<Ω_NODE_STRATEGY name={self.language_name} index={self.index_filename} status=RESONANT>"