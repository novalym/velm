# Path: core/daemon/surveyor/sentinels/scaffold.py
# ------------------------------------------------

import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_ERROR, SEVERITY_WARNING, SEVERITY_INFO, CODE_SYNTAX


class ScaffoldSentinel(BaseSentinel):
    """
    [THE FORM GUARDIAN]
    Enforces the syntax of Gnostic Blueprints (.scaffold, .arch).
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'): continue

            # 1. VARIABLE DEFINITION CHECK
            if stripped.startswith('$$'):
                match = re.match(r'\$\$\s*([a-zA-Z0-9_]+)\s*(:|=)', stripped)
                if not match:
                    diagnostics.append(self.forge_diagnostic(
                        i, "Malformed Variable: Must follow '$$ name = value' or '$$ name: type'",
                        SEVERITY_ERROR, "Scaffold Sentinel", CODE_SYNTAX
                    ))
                else:
                    # [ASCENSION]: Emit Info for Valid Variables (Proof of Life)
                    diagnostics.append(self.forge_diagnostic(
                        i, f"Gnostic Variable Defined: {match.group(1)}",
                        SEVERITY_INFO, "Scaffold Sentinel", "GNOSTIC_VAR"
                    ))

            # 2. DIRECTIVE SYNTAX CHECK
            if stripped.startswith('@if') or stripped.startswith('@elif'):
                if '{{' not in stripped or '}}' not in stripped:
                    diagnostics.append(self.forge_diagnostic(
                        i, "Logic Directive missing Jinja2 brackets '{{ }}'",
                        SEVERITY_ERROR, "Scaffold Sentinel", CODE_SYNTAX
                    ))

            # 3. FILE OPERATION CHECK
            if '::' in stripped:
                parts = stripped.split('::')
                if len(parts) > 1 and not (parts[1].strip().startswith('"') or parts[1].strip().startswith('"""')):
                    diagnostics.append(self.forge_diagnostic(
                        i, "Inline content must be wrapped in quotes.",
                        SEVERITY_WARNING, "Scaffold Sentinel", CODE_SYNTAX
                    ))

        return diagnostics