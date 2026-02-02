# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/ruby_strategy.py
# -------------------------------------------------------------------------------------------------

import re
import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy
from ....utils import atomic_write

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class RubyStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE RUBY GEM SMITH (V-Ω-REQUIRE-WEAVER)                                 ==
    =============================================================================
    The Guardian of the Ruby Cosmos.
    1. Enforces `lib/` structure.
    2. Auto-injects `require_relative` into parent modules.
    """

    def __init__(self):
        super().__init__("Ruby")

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        if file_path.is_dir() or file_path.suffix != '.rb':
            return

        lib_root = project_root / "lib"
        if not file_path.is_relative_to(lib_root):
            return

        # If we added `lib/my_gem/utils.rb`, we need to require it in `lib/my_gem.rb`
        # or the parent directory's main file.

        # 1. Identify Parent Module File
        parent_dir = file_path.parent
        # The convention is that `lib/foo/bar.rb` is required by `lib/foo.rb`
        parent_module_file = parent_dir.with_suffix(".rb")

        # Also check for `lib/foo/bar/baz.rb` -> `lib/foo/bar.rb`

        if not self._exists(parent_module_file, project_root, transaction):
            # If the parent module file doesn't exist, we might need to create it?
            # Or perhaps we are at the root `lib/my_gem.rb` and we don't require ourselves.
            return

        self._inject_require(parent_module_file, file_path, project_root, transaction)

    def _inject_require(self, target_file: Path, source_file: Path, project_root: Path, tx):
        content = self._read_content(target_file, project_root, tx)

        # Calculate relative path for require
        # from lib/my_gem.rb to lib/my_gem/utils.rb is 'my_gem/utils'
        try:
            rel_path = source_file.relative_to(target_file.parent)
            require_path = str(rel_path.with_suffix(''))
        except ValueError:
            return

        # Check if already required
        if f"require_relative '{require_path}'" in content or f'require_relative "{require_path}"' in content:
            return

        # Append
        new_content = content
        if new_content and not new_content.endswith('\n'): new_content += "\n"

        req_stmt = f"require_relative '{require_path}'"
        new_content += f"{req_stmt}\n"

        self.logger.success(f"   -> Injecting Ruby Require: [green]{req_stmt}[/green]")
        self._write_file(target_file, new_content, project_root, tx)

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

    def _write_file(self, path: Path, content: str, root: Path, tx):
        res = atomic_write(path, content, self.logger, root, transaction=tx, verbose=False)
        if tx and res.success:
            try:
                res.path = path.relative_to(root)
                tx.record(res)
            except:
                pass