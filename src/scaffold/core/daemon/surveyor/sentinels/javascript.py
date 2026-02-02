# Path: core/daemon/surveyor/sentinels/javascript.py
# --------------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_HINT, SEVERITY_ERROR, CODE_DEBT, CODE_SECURITY, CODE_BEST_PRACTICE


class JavaScriptSentinel(BaseSentinel):
    """
    [THE WEB WEAVER]
    Analyzes the chaotic energies of the JavaScript ecosystem (JS/JSX).
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'): continue

            # 1. CONSOLE LOGGING
            if re.search(r'console\.(log|debug|info)\s*\(', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Console log detected. Remove for production purity.",
                    SEVERITY_HINT, "JS Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Remove or wrap in debug flag."
                ))

            # 2. THE VAR HERESY
            if re.search(r'\bvar\s+\w+', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Usage of 'var' detected. Use 'let' or 'const' for block scoping.",
                    SEVERITY_WARNING, "JS Sentinel", CODE_BEST_PRACTICE,
                    suggestion="Replace `var` with `let` or `const`."
                ))

            # 3. LOOSE EQUALITY
            if re.search(r'[^=!]==[^=]', stripped):  # Matches == but not === or !==
                diagnostics.append(self.forge_diagnostic(
                    i, "Loose equality '==' used. Prefer strict '==='.",
                    SEVERITY_WARNING, "JS Sentinel", "TYPE_SAFETY",
                    suggestion="Use `===`."
                ))

            # 4. SECRET CHECK
            secret_diag = self.scan_for_secrets(stripped, i, "Security Warden")
            if secret_diag: diagnostics.append(secret_diag)

            # 5. ALERT/CONFIRM BLOCKING
            if re.search(r'(window\.)?(alert|confirm|prompt)\s*\(', stripped):
                diagnostics.append(self.forge_diagnostic(
                    i, "Blocking UI call detected. Use a Modal Interface.",
                    SEVERITY_WARNING, "UX Sentinel", CODE_BEST_PRACTICE
                ))

            # 6. DANGEROUS HTML
            if 'dangerouslySetInnerHTML' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Direct DOM Injection via dangerouslySetInnerHTML.",
                    SEVERITY_WARNING, "Security Warden", "SECURITY_XSS",
                    suggestion="Sanitize input before rendering."
                ))

        return diagnostics