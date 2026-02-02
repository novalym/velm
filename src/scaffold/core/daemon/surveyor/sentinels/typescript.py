# Path: core/daemon/surveyor/sentinels/typescript.py
# --------------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .javascript import JavaScriptSentinel
from ..constants import SEVERITY_WARNING, CODE_TYPE_SAFETY

class TypeScriptSentinel(JavaScriptSentinel):
    """
    [THE STRICT TYPIST]
    Extends the Web Weaver with strict type enforcement.
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        # Inherit JS checks first
        diagnostics = super().analyze(content, file_path, root_path)
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'): continue

            # 1. THE ANY HERESY
            # Matches ': any' or 'as any', ignoring eslint-disable lines
            if re.search(r'(\:\s*any\b|\bas\s+any\b)', stripped) and 'eslint-disable' not in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "The 'any' type is a void of meaning. Define a Schema or use 'unknown'.",
                    SEVERITY_WARNING, "TS Sentinel", CODE_TYPE_SAFETY
                ))

            # 2. BANGLING (Non-Null Assertion)
            if re.search(r'\w+!\.', stripped):
                 diagnostics.append(self.forge_diagnostic(
                    i, "Non-null assertion (!) used. Safety guarantee bypassing detected.",
                    SEVERITY_WARNING, "TS Sentinel", CODE_TYPE_SAFETY,
                    suggestion="Use optional chaining `?.` or explicit checks."
                ))

        return diagnostics