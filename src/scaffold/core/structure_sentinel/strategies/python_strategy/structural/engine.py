# Path: scaffold/core/structure_sentinel/strategies/python_strategy/structural/engine.py
# --------------------------------------------------------------------------------------

from pathlib import Path
from typing import Optional, Set, TYPE_CHECKING, Dict, Any
from ......utils import atomic_write
from .layout import LayoutGeometer
from .content import ContentScribe

if TYPE_CHECKING:
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class StructuralFaculty:
    """
    =================================================================================
    == THE STRUCTURAL FACULTY (V-Ω-LOGICAL-IDENTITY-ASCENDED)                      ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The Sovereign of Structure. It orchestrates the consecration of directories
    into Python packages.

    It has been healed of the "Ephemeral Name Heresy". It now distinguishes between
    the **Effective Path** (where we write/scan) and the **Logical Path** (what we name it).
    """

    def __init__(self, logger: 'Scribe'):
        self.logger = logger
        self.geometer = LayoutGeometer()
        self.scribe = ContentScribe()
        self._init_cache: Set[Path] = set()
        self._py_typed_cache: Set[Path] = set()
        self._license_header_cache: Optional[str] = None

    def ensure_structure(
            self,
            file_path: Path,
            project_root: Path,
            transaction: Optional["GnosticTransaction"],
            gnosis: Optional[Dict[str, Any]] = None
    ):
        """
        The Rite of Consecration.
        Ensures every directory from the file up to the root is a valid Python package.

        Args:
            file_path: The target file triggering the structural check.
            project_root: The root of the project.
            transaction: The active transaction (if any).
            gnosis: Global context variables (author, email, etc.) for metadata injection.
        """
        # Resolve to absolute paths for robust comparisons
        abs_file_path = file_path.resolve()
        abs_project_root = project_root.resolve()
        gnosis = gnosis or {}

        if abs_file_path.is_dir():
            current_dir = abs_file_path
        else:
            current_dir = abs_file_path.parent

        # [FACULTY 8] Lazy load the license header
        if self._license_header_cache is None:
            self._license_header_cache = self.scribe.get_license_header(abs_project_root)

        # [FACULTY 5] The Recursive Ascent
        while True:
            # Safety: Stop if we ascend past the project root
            if not current_dir.is_relative_to(abs_project_root) and current_dir != abs_project_root:
                break

            # [FACULTY 3] Resolve the Effective Path (Staging vs Disk) for INSPECTION
            effective_dir = self._resolve_effective_directory(current_dir, abs_project_root, transaction)

            # If the geometer marks it as an abyss (e.g. .git, __pycache__), skip it.
            if self.geometer.is_abyss(current_dir):
                if current_dir == abs_project_root: break
                current_dir = current_dir.parent
                continue

            # [FACULTY 6] Namespace Sentinel
            if self.geometer.is_namespace_package(current_dir):
                self.logger.verbose(f"   -> Namespace '{current_dir.name}' detected. Skipping __init__.py.")
            else:
                # [FACULTY 1] We pass the Logical Directory (current_dir) for naming/paths
                # and the Effective Directory (effective_dir) for content scanning.
                self._forge_init(current_dir, effective_dir, abs_project_root, transaction, gnosis)

            # [FACULTY 9] Marker Forge
            if self.geometer.should_be_typed(current_dir, abs_project_root):
                self._forge_marker(current_dir / "py.typed", abs_project_root, transaction)

            # Stop AFTER processing the project root (to handle flat layouts)
            if current_dir == abs_project_root:
                break

            # Stop if we hit the filesystem root
            if current_dir.parent == current_dir:
                break

            current_dir = current_dir.parent

    def _resolve_effective_directory(self, logical_dir: Path, root: Path, tx: Optional["GnosticTransaction"]) -> Path:
        """
        [FACULTY 3 & 4] THE EFFECTIVE PATH RESOLVER & MATERIALIZER.
        Returns the path where the directory contents ACTUALLY reside (Staging or Disk).
        """
        if not tx:
            return logical_dir

        try:
            rel_path = logical_dir.relative_to(root)
            staging_path = tx.get_staging_path(rel_path)

            # [FACULTY 4] The Ephemeral Materializer
            # Ensure the directory exists in staging so iterdir() works
            if not staging_path.exists():
                staging_path.mkdir(parents=True, exist_ok=True)

            return staging_path
        except ValueError:
            return logical_dir

    def _forge_init(self, logical_dir: Path, effective_dir: Path, root: Path, tx, gnosis: Dict[str, Any]):
        """
        Forges the __init__.py.
        """
        init_file_target = logical_dir / "__init__.py"

        # [FACULTY 10] Caching & Idempotency
        if init_file_target in self._init_cache: return
        self._init_cache.add(init_file_target)

        if not self._exists(init_file_target, root, tx):
            # [FACULTY 7] Root Divination
            is_root = self.geometer.is_root_package(logical_dir, root)

            # [FACULTY 1] The Law of Logical Identity
            # We pass `logical_dir.name` as the package_name.
            # This ensures "The `billing` package" instead of "The `f8a...` package".
            content = self.scribe.forge_init(
                directory=effective_dir,  # Scan here
                is_root=is_root,
                license_header=self._license_header_cache,
                package_name=logical_dir.name,  # Name this
                gnosis=gnosis  # [FACULTY 2] Inject Metadata
            )

            self.logger.info(f"   -> Forging Structure: [cyan]{init_file_target.relative_to(root)}[/cyan]")
            self._write(init_file_target, content, root, tx)

    def _forge_marker(self, path: Path, root: Path, tx):
        if path in self._py_typed_cache: return
        self._py_typed_cache.add(path)

        if not self._exists(path, root, tx):
            content = self.scribe.forge_marker()
            self.logger.verbose(f"   -> Marking library: {path.relative_to(root)}")
            self._write(path, content, root, tx)

    def _exists(self, path: Path, root: Path, tx) -> bool:
        """Checks existence in Reality OR Staging."""
        if path.exists(): return True
        if tx:
            try:
                rel = path.relative_to(root)
                return tx.get_staging_path(rel).exists()
            except ValueError:
                pass
        return False

    def _write(self, path: Path, content: str, root: Path, tx):
        """[FACULTY 8 & 11] The Atomic Inscription & Recording."""
        try:
            if path.exists() and not tx:
                try:
                    if path.read_text(encoding='utf-8') == content: return
                except:
                    pass

            res = atomic_write(path, content, self.logger, root, transaction=tx, verbose=False)

            if tx and res.success:
                try:
                    res.path = path.relative_to(root)
                    tx.record(res)
                except ValueError:
                    pass
        except Exception as e:
            self.logger.error(f"   -> Failed to write {path.name}: {e}")