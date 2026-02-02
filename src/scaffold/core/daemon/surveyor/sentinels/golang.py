# Path: core/daemon/surveyor/sentinels/golang.py
# ----------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_HINT, CODE_BEST_PRACTICE


class GolangSentinel(BaseSentinel):
    """
    [THE CLOUD WALKER]
    Analyzes Go source code.
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'): continue

            # 1. FMT PRINTLN
            if 'fmt.Println(' in stripped or 'fmt.Printf(' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Direct usage of 'fmt' for logging. Prefer 'log' or structured logger.",
                    SEVERITY_HINT, "Go Sentinel", CODE_BEST_PRACTICE
                ))

            # 2. PANIC
            if 'panic(' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Panic detected. Ensure this is truly unrecoverable.",
                    SEVERITY_WARNING, "Go Sentinel", "SAFETY_PANIC"
                ))

            # 3. IGNORED ERRORS (_ =)
            if '_ =' in stripped and ('err' in stripped or 'Error' in stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Error suppression detected. Handle the error explicitly.",
                    SEVERITY_WARNING, "Go Sentinel", CODE_BEST_PRACTICE
                ))

        return diagnostics