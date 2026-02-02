# Path: core/lsp/scaffold_features/linter/rules/geometry_law.py
# ----------------------------------------------------

from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity

class GeometricPurityLaw(BaseLinterRule):
    """
    [THE LAW OF GEOMETRY]
    Enforces whitespace purity (Spaces over Tabs, Trailing Whitespace).
    """
    @property
    def code(self): return "GEOMETRIC_DRIFT"

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []
        for i, line in enumerate(ctx.doc.text.splitlines()):
            if self.is_suppressed(ctx, i): continue

            # 1. TAB HERESY
            if "\t" in line:
                idx = line.find("\t")
                findings.append(self.forge_diagnostic(
                    line=i, start_col=idx, end_col=idx+1,
                    message="Tab detected. The God-Engine favors 4 spaces for universal harmony.",
                    severity=DiagnosticSeverity.Hint,
                    suggestion="Convert indentation to spaces.",
                    data={"fix_type": "convert_tabs"}
                ))

            # 2. TRAILING WHITESPACE
            if line.rstrip() != line:
                stripped = line.rstrip()
                start = len(stripped)
                if start < len(line):
                    findings.append(self.forge_diagnostic(
                        line=i, start_col=start, end_col=len(line),
                        message="Trailing whitespace detected.",
                        severity=DiagnosticSeverity.Information,
                        suggestion="Trim the line end.",
                        data={"fix_type": "trim_trailing"}
                    ))

        return findings