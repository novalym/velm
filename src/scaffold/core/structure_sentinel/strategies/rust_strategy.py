# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/rust_strategy.py
# -------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy
from ....utils import atomic_write
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class RustStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE RUST FERRAN (V-Ω-SEMANTIC-MOD-WEAVER)                               ==
    =============================================================================
    The Guardian of the Rust Cosmos.
    1. Forges `mod.rs` if a directory is born void.
    2. Injects `pub mod <name>;` into the parent module file (lib.rs/main.rs/mod.rs).
    """

    def __init__(self):
        super().__init__("Rust")

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        # --- PHASE I: STRUCTURAL INTEGRITY ---
        # Ensure mod.rs exists for directories, etc. (Existing logic)

        if file_path.is_dir():
            current_dir = file_path
        else:
            current_dir = file_path.parent

        src_root = project_root / "src"
        if not current_dir.is_relative_to(src_root) and current_dir != src_root:
            # Allow src/ itself, or subdirs.
            if not str(current_dir).startswith(str(src_root)):
                return

        # 1. Recursive mod.rs creation (The existing logic)
        temp_dir = current_dir
        while temp_dir != src_root and temp_dir.is_relative_to(src_root):
            self._ensure_mod_file(temp_dir, project_root, transaction)
            if temp_dir.parent == temp_dir: break
            temp_dir = temp_dir.parent

        # --- PHASE II: SEMANTIC REGISTRATION ---
        # If we just added a file (foo.rs) or a module dir (foo/mod.rs),
        # we must tell the PARENT about it.

        if file_path.name in ("mod.rs", "lib.rs", "main.rs"):
            return  # These are structural files, not modules themselves (usually)

        # Name of the module being added
        module_name = file_path.stem
        if file_path.is_dir():
            # If it's a dir, the module name is the dir name
            module_name = file_path.name

        # Find the parent module file
        parent_dir = file_path.parent if not file_path.is_dir() else file_path.parent

        parent_mod_file = self._find_parent_module_file(parent_dir, src_root)

        if parent_mod_file:
            self._inject_mod_decl(parent_mod_file, module_name, project_root, transaction)

    def _ensure_mod_file(self, directory: Path, project_root: Path, transaction: Optional["GnosticTransaction"]):
        # Rust 2018+ prefers `directory.rs` sibling over `directory/mod.rs` nested,
        # BUT if `directory/` exists and has files, `mod.rs` is still the standard way to expose THEM.
        # Scaffold defaults to `mod.rs` for explicit directory structures.

        nested_mod = directory / "mod.rs"
        sibling_mod = directory.with_suffix(".rs")

        # Check existence
        if self._exists(sibling_mod, project_root, transaction): return
        if self._exists(nested_mod, project_root, transaction): return

        # If neither exists, create nested mod.rs
        self.logger.info(f"   -> Void detected. Forging: [cyan]{nested_mod.relative_to(project_root)}[/cyan]")
        self._write_file(nested_mod, "// Gnostically Consecrated Module\n", project_root, transaction)

    def _find_parent_module_file(self, directory: Path, src_root: Path) -> Optional[Path]:
        """
        Locates the file that owns the 'directory' scope.
        Priority:
        1. directory/mod.rs
        2. directory.rs (Sibling of directory? No, that would BE the module)
        Wait. If I create `src/models/user.rs`. Parent dir is `src/models`.
        I need to find the file that defines `mod models`. NO.
        I need to find the file that defines the CONTENTS of `src/models`.
        That is `src/models/mod.rs` OR `src/models.rs`.

        If I create `src/lib.rs`, I am root.
        If I create `src/main.rs`, I am root.
        """
        # Case 1: We are in root (src/)
        if directory == src_root:
            lib = directory / "lib.rs"
            if lib.exists(): return lib
            main = directory / "main.rs"
            if main.exists(): return main
            return None

        # Case 2: We are in a subdir (src/models/)
        # Look for mod.rs inside
        nested = directory / "mod.rs"
        if nested.exists(): return nested

        # Look for sibling (src/models.rs)
        sibling = directory.with_suffix(".rs")
        if sibling.exists(): return sibling

        return None

    def _inject_mod_decl(self, target_file: Path, module_name: str, project_root: Path,
                         transaction: Optional["GnosticTransaction"]):
        content = self._read_content(target_file, project_root, transaction)

        # Check if already declared
        # matches `mod name;` or `pub mod name;`
        regex = re.compile(rf"^\s*(pub\s+)?mod\s+{re.escape(module_name)}\s*;", re.MULTILINE)
        if regex.search(content):
            self.logger.verbose(f"   -> Module '{module_name}' already declared in {target_file.name}.")
            return

        # Append
        decl = f"pub mod {module_name};\n"

        # Try to insert alphabetically? Or at end?
        # Simple append for now.
        new_content = content
        if new_content and not new_content.endswith('\n'): new_content += "\n"
        new_content += decl

        self.logger.success(f"   -> Injecting Rust Module: [green]{decl.strip()}[/green] into {target_file.name}")
        self._write_file(target_file, new_content, project_root, transaction)

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