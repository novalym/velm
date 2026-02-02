# Path: core/lsp/scaffold_features/linter/rules/architecture_law.py
# -----------------------------------------------------------------
#IN THE FUTURE, REPLACE THIS LOGIC WITH INTEGRATION OF THE POWERFUL SENTINEL

import re
from typing import List
from .base import BaseLinterRule
from ....base.types import Diagnostic, DiagnosticSeverity


class LayerViolationLaw(BaseLinterRule):
    """
    =============================================================================
    == THE ARCHITECTURAL WARDEN (V-Ω-LAYER-ENFORCEMENT)                        ==
    =============================================================================
    LIF: INFINITY | ROLE: SPAGHETTI_PREVENTION

    Enforces strict dependency directionality based on folder semantics.
    1. UI cannot import DB/Infra.
    2. Models cannot import Controllers.
    3. Utils cannot import Domain Logic.
    """

    @property
    def code(self):
        return "ARCHITECTURAL_VIOLATION"

    @property
    def priority(self):
        return 90

    def validate(self, ctx) -> List[Diagnostic]:
        findings = []

        # 1. Divine Current Layer
        uri = str(ctx.doc.uri)
        is_ui = "/components/" in uri or "/views/" in uri or "/ui/" in uri
        is_model = "/models/" in uri or "/schemas/" in uri
        is_util = "/utils/" in uri or "/common/" in uri

        lines = ctx.doc.text.splitlines()

        for i, line in enumerate(lines):
            if self.is_suppressed(ctx, i): continue

            # Check Imports
            match = re.search(r'^\s*(?:import|from)\s+["\']?([^"\';\s]+)', line)
            if not match: continue

            target = match.group(1).lower()

            # RULE 1: UI Integrity
            if is_ui and ("database" in target or "sqlalchemy" in target or "boto3" in target):
                findings.append(self.forge_diagnostic(
                    line=i, start_col=match.start(1), end_col=match.end(1),
                    message=f"Layer Violation: UI Component is touching the Infrastructure ('{target}'). Use a Service/API layer.",
                    severity=DiagnosticSeverity.Error,
                    suggestion="Move logic to a Service and call it via API."
                ))

            # RULE 2: Model Purity
            if is_model and ("controller" in target or "view" in target):
                findings.append(self.forge_diagnostic(
                    line=i, start_col=match.start(1), end_col=match.end(1),
                    message=f"Dependency Inversion: Data Model importing upper layer ('{target}').",
                    severity=DiagnosticSeverity.Warning,
                    suggestion="Models should be pure. Use dependency injection."
                ))

            # RULE 3: Utility Isolation
            if is_util and ("models" in target or "services" in target):
                findings.append(self.forge_diagnostic(
                    line=i, start_col=match.start(1), end_col=match.end(1),
                    message=f"Entanglement: Low-level Utility importing High-level Domain ('{target}').",
                    severity=DiagnosticSeverity.Warning,
                    suggestion="Pass data as arguments instead of importing domain objects."
                ))

        return findings