# Path: core/lsp/scaffold_features/linter/rules/base.py
# --------------------------------------------

import re
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict

# --- GNOSTIC UPLINKS ---
from ....base.types import Diagnostic, DiagnosticSeverity, Range, Position
from ..context import AnalysisContext

class BaseLinterRule(ABC):
    """
    =============================================================================
    == THE COVENANT OF LAW (V-Ω-BASE)                                          ==
    =============================================================================
    The abstract ancestor of all internal Linters.
    Provides geometric utilities, suppression checking, and standardized reporting.
    """

    @property
    @abstractmethod
    def code(self) -> str:
        """The machine-readable heresy code (e.g., LINT_001)."""
        pass

    @abstractmethod
    def validate(self, ctx: AnalysisContext) -> List[Diagnostic]:
        """Performs the forensic scan and returns Heresies."""
        pass

    def forge_diagnostic(
        self,
        line: int,
        start_col: int,
        end_col: int,
        message: str,
        severity: DiagnosticSeverity,
        fix_command: Optional[str] = None,
        suggestion: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Diagnostic:
        """
        [THE RITE OF ACCUSATION]
        Creates a strict Pydantic Diagnostic object.
        Automatically injects the rule code and source.
        """
        # [ASCENSION 2]: DATA ENRICHMENT
        # We pack the cure into the heresy for the Healer to find.
        payload = data or {}
        if fix_command: payload['fix_command'] = fix_command
        if suggestion: payload['suggestion'] = suggestion
        payload['heresy_key'] = self.code

        return Diagnostic(
            range=Range(
                start=Position(line=line, character=start_col),
                end=Position(line=line, character=end_col)
            ),
            severity=severity,
            code=self.code,
            source=f"Gnostic Linter",
            message=message,
            data=payload
        )

    def is_suppressed(self, ctx: AnalysisContext, line_index: int) -> bool:
        """
        [THE GAZE OF MERCY]
        Checks if the line carries the Sigil of Silence.
        """
        return line_index in ctx.suppressed_lines

    def get_token_range(self, line_text: str, token: str, start_search: int = 0) -> tuple[int, int]:
        """Helper to find start/end columns of a token."""
        start = line_text.find(token, start_search)
        if start == -1:
            return 0, len(line_text)
        return start, start + len(token)