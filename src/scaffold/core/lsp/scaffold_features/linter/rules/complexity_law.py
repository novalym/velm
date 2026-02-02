# Path: core/lsp/scaffold_features/linter/rules/complexity_law.py
# ------------------------------------------------------

from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity

class ComplexityLaw(BaseLinterRule):
    """
    [THE LAW OF ENTROPY]
    Measures the cognitive weight of the scripture.
    """

    @property
    def code(self):
        return "HIGH_ENTROPY"

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []
        lines = ctx.doc.text.splitlines()

        # 1. MONOLITH DETECTION
        if len(lines) > 500:
            findings.append(self.forge_diagnostic(
                line=0, start_col=0, end_col=len(lines[0]),
                message=f"Monolithic Scripture Detected ({len(lines)} lines). Consider fission.",
                severity=DiagnosticSeverity.Information,
                suggestion="Split this blueprint into smaller fragments using @include."
            ))

        # 2. NESTING DEPTH
        for i, line in enumerate(lines):
            if self.is_suppressed(ctx, i): continue

            # Count leading spaces (4 spaces = 1 level)
            indent = ctx.indent_map.get(i, 0)
            depth = indent / 4

            if depth > 5:
                findings.append(self.forge_diagnostic(
                    line=i, start_col=0, end_col=indent,
                    message=f"Deep Nesting ({int(depth)} levels). Logic flow is becoming obscure.",
                    severity=DiagnosticSeverity.Warning,
                    suggestion="Refactor logic to flatten the structure."
                ))

        return findings