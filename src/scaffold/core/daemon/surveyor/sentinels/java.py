# Path: core/daemon/surveyor/sentinels/java.py
# --------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_HINT, SEVERITY_ERROR, CODE_BEST_PRACTICE, CODE_PERFORMANCE


class JavaSentinel(BaseSentinel):
    """
    [THE ENTERPRISE MONOLITH]
    Analyzes Java source code for legacy patterns and performance traps.
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'): continue

            # 1. SYSTEM OUT
            if 'System.out.print' in stripped or 'System.err.print' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "System.out/err usage. Use a Logger (SLF4J/Log4j).",
                    SEVERITY_HINT, "Java Sentinel", CODE_BEST_PRACTICE
                ))

            # 2. PRINT STACK TRACE
            if '.printStackTrace()' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "printStackTrace() detected. Log the exception properly.",
                    SEVERITY_WARNING, "Java Sentinel", CODE_BEST_PRACTICE
                ))

            # 3. THREAD STOP (Deprecated/Unsafe)
            if '.stop()' in stripped and 'Thread' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Thread.stop() is deprecated and unsafe.",
                    SEVERITY_ERROR, "Java Sentinel", "SAFETY_CONCURRENCY"
                ))

            # 4. EMPTY CATCH BLOCK
            if re.search(r'catch\s*\(.*?\)\s*\{\s*\}', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Empty Catch Block. Errors must not be silenced.",
                    SEVERITY_WARNING, "Java Sentinel", CODE_BEST_PRACTICE
                ))

        return diagnostics