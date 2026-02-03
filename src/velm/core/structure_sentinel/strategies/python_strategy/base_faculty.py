# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/base_faculty.py
# ----------------------------------------------------------------------------------------------------------------

from abc import ABC
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .....utils import atomic_write

if TYPE_CHECKING:
    from .contracts import SharedContext
    from .....logger import Scribe

class BaseFaculty(ABC):
    """
    The Ancestral Soul of all Python Faculties.
    Provides shared utilities and the unbreakable bond to the Logger.
    """
    def __init__(self, logger: "Scribe"):
        self.logger = logger

    def _read(self, path: Path, context: "SharedContext") -> str:
        """Reads content from Transaction Staging OR Disk."""
        if context.transaction:
            try:
                rel_path = path.relative_to(context.project_root)
                staged_path = context.transaction.get_staging_path(rel_path)
                if staged_path.exists():
                    return staged_path.read_text(encoding='utf-8')
            except Exception:
                pass
        if path.exists():
            return path.read_text(encoding='utf-8')
        return ""

    def _write(self, path: Path, content: str, context: "SharedContext"):
        """Performs a transactional write."""
        res = atomic_write(path, content, self.logger, context.project_root, transaction=context.transaction, verbose=False)
        if context.transaction and res.success:
            try:
                res.path = path.relative_to(context.project_root)
                context.transaction.record(res)
            except ValueError:
                pass