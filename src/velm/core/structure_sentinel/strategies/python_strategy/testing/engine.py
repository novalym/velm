# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/testing/engine.py
# ------------------------------------------------------------------------------------------------------------------

from pathlib import Path
from typing import Optional, TYPE_CHECKING
from ......utils import atomic_write
from .analyzer import SourceCodeAnatomist
from .generator import PytestArchitect

if TYPE_CHECKING:
    from ......core.kernel.transaction import GnosticTransaction
    from ......logger import Scribe


class TestingFaculty:
    """
    [THE ORCHESTRATOR OF ADJUDICATION]
    Coordinates the scanning of source code and the forging of test suites.
    """

    def __init__(self, logger: 'Scribe'):
        self.logger = logger
        self.anatomist = SourceCodeAnatomist()
        self.architect = PytestArchitect()

    def ensure_test_shadow(self, file_path: Path, root: Path, tx: Optional["GnosticTransaction"]):
        if self._should_ignore(file_path):
            return

        test_path = self._resolve_test_path(file_path, root)
        if not test_path or self._exists(test_path, root, tx):
            return

        source_content = self._read_content(file_path, root, tx)
        if not source_content:
            return

        # 1. Anatomize the Source
        blueprint = self.anatomist.analyze(file_path, source_content, root)
        if not blueprint:
            return

        # 2. Architect the Suite
        test_content = self.architect.forge_suite(blueprint)

        # 3. Inscribe
        self.logger.info(f"   -> Forging Smart Test Shadow: [cyan]{test_path.relative_to(root)}[/cyan]")
        self._write(test_path, test_content, root, tx)

    def _should_ignore(self, path: Path) -> bool:
        name = path.name
        parts = path.parts
        if "tests" in parts or "test" in parts or "migrations" in parts: return True
        if name.startswith("test_") or name.endswith("_test.py"): return True
        if name.startswith("_") and name != "__init__.py": return True
        if name in ["conftest.py", "setup.py", "manage.py", "wsgi.py", "asgi.py"]: return True
        return False

    def _resolve_test_path(self, source_path: Path, root: Path) -> Optional[Path]:
        try:
            rel_path = source_path.relative_to(root)
            parts = list(rel_path.parts)
            if parts[0] == "src": parts = parts[1:]

            parent_parts = parts[:-1]
            filename = parts[-1]

            test_rel_path = Path("tests") / Path(*parent_parts) / f"test_{filename}"
            return root / test_rel_path
        except ValueError:
            return None

    def _exists(self, path: Path, root: Path, tx) -> bool:
        if path.exists(): return True
        if tx:
            try:
                return tx.get_staging_path(path.relative_to(root)).exists()
            except:
                pass
        return False

    def _read_content(self, path: Path, root: Path, tx) -> str:
        if tx:
            try:
                staged = tx.get_staging_path(path.relative_to(root))
                if staged.exists(): return staged.read_text('utf-8')
            except:
                pass
        if path.exists(): return path.read_text('utf-8')
        return ""

    def _write(self, path: Path, content: str, root: Path, tx):
        path.parent.mkdir(parents=True, exist_ok=True)
        res = atomic_write(path, content, self.logger, root, transaction=tx, verbose=False)
        if tx and res.success:
            try:
                res.path = path.relative_to(root)
                tx.record(res)
            except:
                pass