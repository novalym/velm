# Path: core/lsp/base/types/window.py
# -----------------------------------

from enum import IntEnum
from typing import Optional, List, Union
from pydantic import Field, field_validator
from .base import LspModel


# =================================================================================
# == I. THE ENUM OF GRAVITY                                                      ==
# =================================================================================

class MessageType(IntEnum):
    """
    [THE SPECTRUM OF URGENCY]
    Defines the gravity of a message sent to the User Interface.
    Inherits from IntEnum to ensure JSON serialization creates integers (1-4), not strings.
    """
    Error = 1
    Warning = 2
    Info = 3
    Log = 4

    # [ASCENSION 1]: AUTO-RESOLVER
    # Allows safe transmutation from raw integers back to Enums
    @classmethod
    def from_value(cls, value: Union[int, str, 'MessageType']) -> 'MessageType':
        try:
            if isinstance(value, cls):
                return value
            return cls(int(value))
        except (ValueError, TypeError):
            return cls.Log  # Default to lowest severity on heresy


# =================================================================================
# == II. THE VESSEL OF PROCLAMATION (SHOW MESSAGE)                               ==
# =================================================================================

class ShowMessageParams(LspModel):
    """
    [THE TOAST]
    Params for `window/showMessage`. Displays a transient notification.
    """
    # [ASCENSION 2]: THE DUALITY UNION (THE FIX)
    # We explicitly accept Union[MessageType, int] to silence static type checkers
    # who complain when you pass raw integers (e.g. 1) to this field.
    type: Union[MessageType, int]
    message: str

    @field_validator('type', mode='before')
    def validate_type(cls, v):
        """Ensures the integer matches the Gnostic Enum."""
        return MessageType.from_value(v)


# =================================================================================
# == III. THE VESSEL OF WHISPERS (LOG MESSAGE)                                   ==
# =================================================================================

class LogMessageParams(LspModel):
    """
    [THE CONSOLE LOG]
    Params for `window/logMessage`. Writes to the Output panel without disturbing the user.
    """
    type: Union[MessageType, int]
    message: str

    @field_validator('type', mode='before')
    def validate_type(cls, v):
        return MessageType.from_value(v)


# =================================================================================
# == IV. THE VESSEL OF INTERCESSION (REQUEST MESSAGE)                            ==
# =================================================================================

class MessageActionItem(LspModel):
    """
    [THE CHOICE]
    A clickable button presented in a Message Request.
    """
    title: str


class ShowMessageRequestParams(LspModel):
    """
    [THE PLEA FOR INTERVENTION]
    Params for `window/showMessageRequest`. Blocks/waits for user action.
    """
    type: Union[MessageType, int]
    message: str
    actions: Optional[List[MessageActionItem]] = None

    @field_validator('type', mode='before')
    def validate_type(cls, v):
        return MessageType.from_value(v)