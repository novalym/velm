# Path: src/velm/core/lsp/base/types/code_action.py
# -------------------------------------------------
# =========================================================================================
# == THE REDEMPTION VESSEL: OMEGA POINT (V-Ω-TOTALITY-V200-SEVERITY-SUTURED)             ==
# =========================================================================================
# LIF: INFINITY | ROLE: ACTION_ATOM_SCHEMA | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CODE_ACTION_V200_SEVERITY_EXORCISM_FINALIS
#
# [ARCHITECTURAL CONSTITUTION]
# 1.  **The Severity 8 Exorcism (THE CURE):** Instantiates an aggressive pre-validator
#     on the `CodeActionContext` to intercept and cleanse out-of-bounds diagnostic
#     severities leaked by Monaco's internal renderer, annihilating the Pydantic crash.
# 2.  **Absolute Pydantic Shielding:** Ensures all arrays and nested dictionaries are
#     safe for strict schema enforcement.
# =========================================================================================

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import Field, ConfigDict, model_validator
from .base import LspModel
from .primitives import Range, Command, TextDocumentIdentifier
from .workspace import WorkspaceEdit
from .diagnostics import Diagnostic


# =================================================================================
# == I. THE NATURE OF THE ACT                                                    ==
# =================================================================================

class CodeActionKind(str, Enum):
    """
    [THE NATURE OF THE ACT]
    Standardized categories of architectural transmutations.
    """
    QuickFix = "quickfix"
    Refactor = "refactor"
    RefactorExtract = "refactor.extract"
    RefactorInline = "refactor.inline"
    RefactorRewrite = "refactor.rewrite"
    Source = "source"
    SourceOrganizeImports = "source.organizeImports"
    SourceFixAll = "source.fixAll"


# =================================================================================
# == II. THE CIRCUMSTANCE (CONTEXT)                                              ==
# =================================================================================

class CodeActionContext(LspModel):
    """
    [THE CIRCUMSTANCE]
    Carries the environmental context (heresies/diagnostics) that triggered the
    call for redemption.
    """
    model_config = ConfigDict(populate_by_name=True)

    diagnostics: List[Diagnostic]
    only: Optional[List[CodeActionKind]] = None
    trigger_kind: Optional[int] = Field(None, alias="triggerKind")

    @model_validator(mode='before')
    @classmethod
    def sanitize_profane_diagnostics(cls, data: Any) -> Any:
        """
        =============================================================================
        == THE APOPHATIC EXORCIST (V-Ω-SEVERITY-CLAMP)                             ==
        =============================================================================
        [THE CURE]: Monaco occasionally leaks internal, non-standard severity codes
        (like 8 for semantic tokens) into the CodeActionContext. This validator
        intercepts the raw dictionary and forces all severities into the sacred
        1-4 bounds BEFORE Pydantic can shatter the request.
        """
        if isinstance(data, dict) and 'diagnostics' in data:
            raw_diags = data['diagnostics']
            if isinstance(raw_diags, list):
                for diag in raw_diags:
                    if isinstance(diag, dict) and 'severity' in diag:
                        sev = diag['severity']
                        try:
                            # LSP Standard requires Severity to be 1, 2, 3, or 4
                            val = int(sev)
                            if val not in (1, 2, 3, 4):
                                # Clamp out-of-bounds severity:
                                # Values > 4 (like 8) are usually benign semantic hints, so we clamp to 4 (Hint).
                                # Values < 1 are coerced to 1 (Error).
                                diag['severity'] = 4 if val > 4 else 1
                        except (ValueError, TypeError):
                            # If it's a string or void, force to 3 (Info)
                            diag['severity'] = 3
        return data


# =================================================================================
# == III. THE PLEA (REQUEST)                                                     ==
# =================================================================================

class CodeActionParams(LspModel):
    """
    [THE PLEA FOR INTERVENTION]
    Sent by the Client when the Architect requests a QuickFix or Refactor.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    range: Range
    context: CodeActionContext


# =================================================================================
# == IV. THE REDEMPTION (RESPONSE ITEM)                                          ==
# =================================================================================

class CodeAction(LspModel):
    """
    [THE REDEMPTION]
    A command or edit to fix a problem or refactor code.
    Returned as a list from the Server.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(..., description="A short, human-readable, title for this code action.")

    kind: Optional[CodeActionKind] = Field(None, description="The kind of the code action.")

    diagnostics: Optional[List[Diagnostic]] = Field(None, description="The diagnostics that this action resolves.")

    is_preferred: Optional[bool] = Field(None, alias="isPreferred", description="Marks this as a preferred action.")

    disabled: Optional[Dict[str, str]] = Field(None, description="Marks the action as disabled.")

    edit: Optional[WorkspaceEdit] = Field(None, description="The workspace edit this code action performs.")

    command: Optional[Command] = Field(None, description="A command this code action executes.")

    data: Optional[Any] = Field(
        None,
        description="A data holder that is preserved between a `textDocument/codeAction` and a `codeAction/resolve` request."
    )


# =================================================================================
# == V. THE CAPABILITY (OPTIONS)                                                 ==
# =================================================================================

class CodeActionOptions(LspModel):
    """
    [THE CAPABILITY]
    Defines the server's code action capabilities during the handshake.
    """
    model_config = ConfigDict(populate_by_name=True)

    code_action_kinds: Optional[List[CodeActionKind]] = Field(None, alias="codeActionKinds")
    resolve_provider: Optional[bool] = Field(None, alias="resolveProvider")
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")