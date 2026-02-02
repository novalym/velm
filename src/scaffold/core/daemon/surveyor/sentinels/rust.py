# Path: core/daemon/surveyor/sentinels/rust.py
# --------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_INFO, SEVERITY_ERROR, CODE_BEST_PRACTICE, CODE_DEBT


class RustSentinel(BaseSentinel):
    """
    [THE IRON CORE]
    Enforces discipline in Rust scriptures.
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'): continue

            # 1. THE PANIC BUTTON (unwrap)
            if '.unwrap()' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Usage of '.unwrap()' detected. Handle the Result gracefully or use 'expect()'.",
                    SEVERITY_WARNING, "Rust Sentinel", "SAFETY_PANIC",
                    suggestion="Replace with `match`, `if let`, or `?` operator."
                ))

            # 2. THE UNSAFE REALM
            if 'unsafe {' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Entering Unsafe Block. Verify invariants manually.",
                    SEVERITY_INFO, "Rust Sentinel", "SAFETY_UNSAFE"
                ))

            # 3. PRINTLN DEBUGGING
            if 'println!(' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Standard Output macro detected. Use 'log' or 'tracing' crates.",
                    SEVERITY_HINT, "Rust Sentinel", CODE_BEST_PRACTICE
                ))

            # 4. PANIC MACRO
            if 'panic!(' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Explicit Panic. Ensure this state is truly unrecoverable.",
                    SEVERITY_WARNING, "Rust Sentinel", "SAFETY_PANIC"
                ))

            # 5. TODO MACRO
            if 'todo!(' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Unimplemented Logic (todo!).",
                    SEVERITY_HINT, "Rust Sentinel", CODE_DEBT
                ))

        return diagnostics