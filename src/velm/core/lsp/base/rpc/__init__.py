# Path: core/lsp/rpc/__init__.py
# ------------------------------

"""
=================================================================================
== THE RPC CITADEL (V-Ω-MESSAGE-CORE-V12-SUTURED)                              ==
=================================================================================
The definitions of the JSON-RPC 2.0 standard.

[THE CURE]: Aliases injected to resolve the 'JsonRpcRequest' name schism.
"""

from .messages import (
    Request, Response, Notification,
    Message, RequestId, ErrorPayload,
    JsonRpcMessage
)
from .errors import JsonRpcError
from .codes import ErrorCodes
from .converter import MessageConverter
from .serializer import GnosticSerializer, gnostic_serializer
from .filters import is_metabolic_noise

# =============================================================================
# == THE RITE OF ALIASING (BACKWARD COMPATIBILITY BRIDGE)                    ==
# =============================================================================
# We map the Ascended Names back to the Legacy Names to ensure the
# GnosticLSPServer and other artisans can still find their way.

JsonRpcRequest = Request
JsonRpcResponse = Response
JsonRpcNotification = Notification
TypeTransmuter = MessageConverter

__all__ = [
    # Ascended Names
    "Request", "Response", "Notification", "Message",
    "RequestId", "ErrorPayload", "JsonRpcMessage",
    "JsonRpcError", "ErrorCodes",
    "MessageConverter",
    "GnosticSerializer", "gnostic_serializer",
    "is_metabolic_noise",

    # Legacy Aliases
    "JsonRpcRequest",
    "JsonRpcResponse",
    "JsonRpcNotification",
    "TypeTransmuter"
]