# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/cpp_strategy.py
# ------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from .base_strategy import BaseStrategy
from ....utils import atomic_write

if TYPE_CHECKING:
    from ....core.kernel.transaction import GnosticTransaction


class CppStructureStrategy(BaseStrategy):
    """
    =============================================================================
    == THE C++ MASON (V-Ω-HEADER-GUARD-WEAVER)                                 ==
    =============================================================================
    The Guardian of the C/C++ Cosmos.
    1. Enforces Include Guards (`#pragma once` or `#ifndef`) in headers.
    2. Suggests CMake registration for new implementation files.
    """

    def __init__(self):
        super().__init__("C++")

    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        if file_path.is_dir(): return

        ext = file_path.suffix.lower()

        # 1. Header Guard Enforcement
        if ext in ('.h', '.hpp', '.hh', '.hxx'):
            self._enforce_header_guard(file_path, project_root, transaction)

        # 2. CMake Awareness (Passive Log)
        if ext in ('.cpp', '.c', '.cc', '.cxx'):
            self._check_cmake_registration(file_path, project_root, transaction)

    def _enforce_header_guard(self, file_path: Path, root: Path, tx):
        content = self._read_content(file_path, root, tx)
        if not content: return

        # Check for #pragma once
        if "#pragma once" in content:
            return

        # Check for standard ifndef guard
        guard_name = self._forge_guard_name(file_path, root)
        if f"#ifndef {guard_name}" in content:
            return

        # Inject #pragma once (Modern Convention)
        self.logger.info(f"   -> Injecting '#pragma once' into {file_path.name}")
        new_content = f"#pragma once\n\n{content}"
        self._write_file(file_path, new_content, root, tx)

    def _forge_guard_name(self, path: Path, root: Path) -> str:
        """Forges a unique guard name like PROJECT_SRC_UTILS_H"""
        try:
            rel = path.relative_to(root)
            slug = str(rel).upper().replace("/", "_").replace("\\", "_").replace(".", "_")
            return slug
        except ValueError:
            return path.name.upper().replace(".", "_")

    def _check_cmake_registration(self, file_path: Path, root: Path, tx):
        """
        Walks up to find CMakeLists.txt and warns if the file might be orphaned.
        Does not auto-edit CMakeLists as that is a high-entropy operation.
        """
        current = file_path.parent
        found_cmake = False
        while current.is_relative_to(root) or current == root:
            cmake = current / "CMakeLists.txt"

            # Check physical or virtual existence
            if cmake.exists():
                found_cmake = True
            elif tx:
                try:
                    if tx.get_staging_path(cmake.relative_to(root)).exists(): found_cmake = True
                except:
                    pass

            if found_cmake:
                # We found the build manifest.
                # In a future ascension, we could grep it for the filename.
                break

            if current == current.parent: break
            current = current.parent

        if not found_cmake:
            self.logger.verbose(f"   -> Note: No CMakeLists.txt found in parent hierarchy for '{file_path.name}'.")

    # ... Helper methods ...
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