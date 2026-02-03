# Path: core/lsp/scaffold_features/linter/rules/bond_law.py
# ------------------------------------------------

import re
from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity
from ....base import UriUtils


class GnosticBondLaw(BaseLinterRule):
    """
    [THE LAW OF BONDS]
    Ensures that referenced files (@include, <<, ->) actually exist in reality.
    Uses the Server's project_root to perform physical existence checks.
    """

    INCLUDE_PATTERN = re.compile(r'(@include|<<|->)\s*["\']?([^"\']+)["\']?')

    def __init__(self, server):
        self.server = server

    @property
    def code(self):
        return "BOND_BROKEN"

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []
        if not self.server.project_root: return []

        for i, line in enumerate(ctx.doc.text.splitlines()):
            if self.is_suppressed(ctx, i): continue

            match = self.INCLUDE_PATTERN.search(line)
            if match:
                operator = match.group(1)
                target_path = match.group(2).strip()

                # Resolve Absolute Path
                try:
                    full_path = (self.server.project_root / target_path).resolve()

                    if not full_path.exists():
                        start = match.start(2)
                        end = match.end(2)

                        findings.append(self.forge_diagnostic(
                            line=i, start_col=start, end_col=end,
                            message=f"Broken Gnostic Bond: Sanctum '{target_path}' does not exist.",
                            severity=DiagnosticSeverity.Error,
                            suggestion="Verify the path or create the missing file.",
                            data={"missing_path": str(full_path), "fix_command": f"scaffold create {target_path}"}
                        ))
                except Exception:
                    pass  # Invalid path syntax

        return findings