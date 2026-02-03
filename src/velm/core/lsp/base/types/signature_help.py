# Path: core/lsp/base/types/signature_help.py
# -------------------------------------------

from enum import IntEnum
from typing import List, Optional, Union, Any, Dict
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import MarkupContent, TextDocumentIdentifier, Position, WorkDoneProgressOptions


# =================================================================================
# == I. THE ENUMS OF TRIGGERING                                                  ==
# =================================================================================

class SignatureHelpTriggerKind(IntEnum):
    """
    [THE CAUSE]
    How the signature help was invoked.
    """
    Invoked = 1
    TriggerCharacter = 2
    ContentChange = 3


# =================================================================================
# == II. THE ATOMS OF KNOWLEDGE                                                  ==
# =================================================================================

class ParameterInformation(LspModel):
    """
    [THE ARGUMENT]
    Represents a specific parameter within a callable signature.
    """
    # The label can be a simple string ("param: Type") or a substring range [start, end]
    label: Union[str, List[int]]
    documentation: Optional[Union[str, MarkupContent]] = None


class SignatureInformation(LspModel):
    """
    [THE SIGNATURE]
    Represents the signature of something callable (function, method, macro).
    """
    label: str = Field(..., description="The label of this signature. Will be shown in the UI.")
    documentation: Optional[Union[str, MarkupContent]] = None
    parameters: Optional[List[ParameterInformation]] = None
    active_parameter: Optional[int] = Field(None, alias="activeParameter",
                                            description="The index of the active parameter.")


class SignatureHelp(LspModel):
    """
    [THE REVELATION]
    The actual response sent to the client containing the list of signatures.
    """
    signatures: List[SignatureInformation]
    active_signature: Optional[int] = Field(0, alias="activeSignature",
                                            description="The active signature. If omitted or the value lies outside the range of `signatures` the value defaults to zero or is ignored if the `signatures.length` === 0.")
    active_parameter: Optional[int] = Field(0, alias="activeParameter",
                                            description="The active parameter of the active signature.")


# =================================================================================
# == III. THE CONTEXT & PLEA                                                     ==
# =================================================================================

class SignatureHelpContext(LspModel):
    """
    [THE SITUATION]
    Additional information about the context in which a signature help request was triggered.
    """
    trigger_kind: SignatureHelpTriggerKind = Field(..., alias="triggerKind")
    trigger_character: Optional[str] = Field(None, alias="triggerCharacter")
    is_retrigger: bool = Field(False, alias="isRetrigger")
    active_signature_help: Optional[SignatureHelp] = Field(None, alias="activeSignatureHelp")


class SignatureHelpParams(LspModel):
    """
    [THE PLEA]
    The parameters sent from the Client to the Server.
    """
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position
    context: Optional[SignatureHelpContext] = None
    work_done_token: Optional[Union[int, str]] = Field(None, alias="workDoneToken")


# =================================================================================
# == IV. THE CAPABILITY CONTRACT (THE MISSING LINK)                              ==
# =================================================================================

class SignatureHelpOptions(LspModel):
    """
    [THE ORACLE'S CONSTITUTION]
    LIF: 100x | ROLE: INVOCATION_SENTINEL

    Defines the server's capability to provide help during function or macro invocation.
    It tells the client which characters trigger the revelation of parameter gnosis.
    """

    trigger_characters: Optional[List[str]] = Field(
        None,
        alias="triggerCharacters",
        description="List of characters that trigger signature help automatically (e.g., '(', ',')."
    )

    retrigger_characters: Optional[List[str]] = Field(
        None,
        alias="retriggerCharacters",
        description="List of characters that re-trigger signature help while it is already active."
    )

    work_done_progress: Optional[bool] = Field(
        None,
        alias="workDoneProgress",
        description="Whether the server supports reporting progress for signature help."
    )

    @classmethod
    def default_gnostic(cls) -> "SignatureHelpOptions":
        """
        [FACTORY RITE]
        Forges a default instance tuned for Scaffold/Symphony/Python.
        Triggers on: '(', ',', and pipe '|' (for filters).
        """
        return cls(
            triggerCharacters=["(", ",", "|"],
            retriggerCharacters=[")"],
            workDoneProgress=False
        )