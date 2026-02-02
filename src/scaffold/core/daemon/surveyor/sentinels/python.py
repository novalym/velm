# Path: core/daemon/surveyor/sentinels/python.py
# ----------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_HINT, SEVERITY_ERROR, CODE_DEBT, CODE_SECURITY, CODE_BEST_PRACTICE, \
    CODE_PERFORMANCE


class PythonSentinel(BaseSentinel):
    """
    [THE SERPENT'S EYE]
    Scans Python scriptures for anti-patterns, security risks, and performance traps.
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'): continue

            # 1. THE SILENCE VOW (Print Check)
            # Detects 'print(' but ignores commented out lines or 'print' inside strings (roughly)
            if re.search(r'(^|[\s;])print\s*\(', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Production Silence Violation: 'print()' detected. Use 'Logger'.",
                    SEVERITY_WARNING, "Python Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Replace with `Logger.info(...)`"
                ))

            # 2. THE DEBT COLLECTOR (TODOs)
            if 'TODO' in line or 'FIXME' in line:
                diagnostics.append(self.forge_diagnostic(
                    i, "Technical Debt Marker Detected.",
                    SEVERITY_HINT, "Gnostic Debt Collector", CODE_DEBT
                ))

            # 3. UNIVERSAL SECRET SCAN
            secret_diag = self.scan_for_secrets(stripped, i, "Security Warden")
            if secret_diag: diagnostics.append(secret_diag)

            # 4. THE EXECUTIONER GUARD (eval/exec)
            if re.search(r'(^|[\s;])(eval|exec)\s*\(', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Unsafe Execution: 'eval/exec' is a pathway to injection heresies.",
                    SEVERITY_ERROR, "Security Warden", CODE_SECURITY
                ))

            # 5. THE DEBUGGER TRAP
            if 'pdb.set_trace()' in stripped or 'breakpoint()' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Debugger Breakpoint left in scripture.",
                    SEVERITY_WARNING, "Python Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Remove breakpoint."
                ))

            # 6. MUTABLE DEFAULT ARGUMENT (The Hydra Head)
            if re.search(r'def\s+\w+\s*\(.*=\s*(\[\]|\{\})', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Mutable Default Argument detected. Lists/Dicts as defaults persist across calls.",
                    SEVERITY_ERROR, "Python Sentinel", "LOGIC_BUG",
                    suggestion="Use `None` as default and initialize inside function."
                ))

            # 7. WILDCARD IMPORT (The Pollution)
            if re.search(r'from\s+.*\s+import\s+\*', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Wildcard Import detected. Namespace pollution risk.",
                    SEVERITY_WARNING, "Python Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Import specific symbols explicitly."
                ))

            # 8. BARE EXCEPT (The Blindfold)
            if re.match(r'^\s*except\s*:', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Bare 'except:' clause. This catches SystemExit and KeyboardInterrupt.",
                    SEVERITY_WARNING, "Python Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Use `except Exception:` or specific errors."
                ))

        return diagnostics