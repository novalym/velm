# Path: core/lsp/base/rpc/messages.py
# -----------------------------------


from __future__ import annotations
import time
import uuid
from typing import Union, Optional, Dict, Any, List, Literal
from pydantic import Field, model_validator
from .base import RpcModel

# JSON-RPC 2.0 ID: String, Integer, or Null
RequestId = Union[int, str, None]


# =================================================================================
# == I. THE VESSEL OF HERESY (ERROR PAYLOAD)                                     ==
# =================================================================================

class ErrorPayload(RpcModel):
    """
    [THE MARK OF FAILURE]
    Represents the 'error' object inside a Response.
    """
    code: int
    message: str
    data: Optional[Any] = None

    def __str__(self) -> str:
        return f"[Code {self.code}] {self.message}"


# =================================================================================
# == II. THE VESSEL OF INTENT (REQUEST)                                          ==
# =================================================================================

class Request(RpcModel):
    """
    [THE PLEA]
    A method call that demands an answer.
    """
    jsonrpc: Literal["2.0"] = "2.0"
    id: RequestId
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None

    # [ASCENSION 1]: CAUSAL TRACING
    trace_id: str = Field(
        default_factory=lambda: f"req-{uuid.uuid4().hex[:8]}",
        alias="traceId"
    )
    timestamp: float = Field(default_factory=time.time)

    @property
    def is_notification(self) -> bool:
        return False


# =================================================================================
# == III. THE VESSEL OF SIGNAL (NOTIFICATION)                                    ==
# =================================================================================

class Notification(RpcModel):
    """
    [THE SIGNAL]
    A fire-and-forget message. No ID, No Response.
    """
    jsonrpc: Literal["2.0"] = "2.0"
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None

    trace_id: str = Field(
        default_factory=lambda: f"not-{uuid.uuid4().hex[:8]}",
        alias="traceId"
    )
    timestamp: float = Field(default_factory=time.time)

    @property
    def is_notification(self) -> bool:
        return True


# =================================================================================
# == IV. THE VESSEL OF REVELATION (RESPONSE)                                     ==
# =================================================================================

class Response(RpcModel):
    """
    [THE ANSWER]
    The result of a Request.
    """
    jsonrpc: Literal["2.0"] = "2.0"
    id: RequestId

    # The Gnosis (Success)
    result: Optional[Any] = None

    # The Heresy (Failure)
    error: Optional[ErrorPayload] = None

    # [ASCENSION 4]: THE META-CHANNEL
    meta: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="_meta")

    @property
    def is_error(self) -> bool:
        return self.error is not None

    @property
    def is_success(self) -> bool:
        return self.error is None

    # --- FACTORY RITES ---
    # [THE FIX]: Renamed to avoid collision with 'error' field and 'success' property concepts.

    @classmethod
    def build_success(cls, req_id: RequestId, result: Any, trace_id: Optional[str] = None) -> 'Response':
        r = cls(id=req_id, result=result)
        if trace_id:
            if not r.meta: r.meta = {}
            r.meta['trace_id'] = trace_id
        return r

    @classmethod
    def build_error(cls, req_id: RequestId, code: int, message: str, data: Any = None) -> 'Response':
        return cls(
            id=req_id,
            error=ErrorPayload(code=code, message=message, data=data)
        )


# =================================================================================
# == V. THE UNION OF MATTER                                                      ==
# =================================================================================

Message = Union[Request, Notification, Response]
JsonRpcMessage = Union[Message, List[Message]]