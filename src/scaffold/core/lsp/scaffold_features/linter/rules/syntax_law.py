# Path: core/lsp/scaffold_features/linter/rules/syntax_law.py
# --------------------------------------------------

from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity

class SyntaxLaw(BaseLinterRule):
    """
    [THE LAW OF FORM]
    Enforces the grammar of the Scaffold tongue ($$, {{, %%).
    """
    @property
    def code(self): return "SYNTAX_SIGIL"

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []
        lines = ctx.doc.text.splitlines()

        for i, line in enumerate(lines):
            stripped = ctx.clean_lines[i]
            if not stripped or stripped.startswith("#"): continue
            if self.is_suppressed(ctx, i): continue

            # 1. VARIABLE DEFINITION ($ vs $$)
            # Incorrect: $ name = val
            # Correct: $$ name = val
            if stripped.startswith("$") and not stripped.startswith("$$"):
                start, end = self.get_token_range(line, "$")
                findings.append(self.forge_diagnostic(
                    line=i, start_col=start, end_col=end,
                    message="Malformed Variable Sigil. Gnostic variables require double-dollar '$$'.",
                    severity=DiagnosticSeverity.Error,
                    suggestion="Replace '$' with '$$'",
                    # Note: We pass raw text for simple replacements in data if needed
                    data={"fix_type": "replace_text", "old": "$", "new": "$$"}
                ))

            # 2. JINJA BALANCE
            open_count = line.count("{{")
            close_count = line.count("}}")
            if open_count != close_count:
                # Find the unbalanced brace
                target = "{{" if open_count > close_count else "}}"
                start, end = self.get_token_range(line, target)
                findings.append(self.forge_diagnostic(
                    line=i, start_col=start, end_col=end,
                    message="Unbalanced Alchemical Vessel. Check your '{{' and '}}' pairs.",
                    severity=DiagnosticSeverity.Error,
                    suggestion="Ensure every opening brace has a closing partner."
                ))

        return findings