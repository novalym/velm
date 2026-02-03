# Path: core/lsp/scaffold_features/linter/rules/security_law.py
# ----------------------------------------------------

import re
from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity

class SecurityLaw(BaseLinterRule):
    """
    [THE LAW OF SECRECY]
    Scans for high-entropy secrets and dangerous path traversals.
    """

    SECRET_REGEX = re.compile(r'(api_key|secret|password|token|auth)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']', re.I)

    @property
    def code(self):
        return "SECURITY_RISK"

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []
        for i, line in enumerate(ctx.doc.text.splitlines()):
            if self.is_suppressed(ctx, i): continue

            # 1. HARDCODED SECRETS
            match = self.SECRET_REGEX.search(line)
            if match:
                findings.append(self.forge_diagnostic(
                    line=i, start_col=match.start(), end_col=match.end(),
                    message="Hardcoded Secret perceived. Move to .env for architectural purity.",
                    severity=DiagnosticSeverity.Warning,
                    suggestion="Use '$$ var = env(SECRET)' instead.",
                    data={"code_action": "extract_to_env"} # Hint for code action
                ))

            # 2. PATH TRAVERSAL
            if "../" in line:
                idx = line.find("../")
                findings.append(self.forge_diagnostic(
                    line=i, start_col=idx, end_col=idx + 3,
                    message="Path Traversal Heresy: Blueprints must be relative to the Sanctum.",
                    severity=DiagnosticSeverity.Error,
                    suggestion="Use absolute project paths or re-structure the blueprint."
                ))

        return findings