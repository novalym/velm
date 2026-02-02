# Path: core/lsp/base/rpc/errors.py
# ---------------------------------


from typing import Optional, Any
from .messages import Response, RequestId
from .codes import ErrorCodes


class JsonRpcError(Exception):
    """
    [THE HERESY EXCEPTION]
    Standard Python exception that carries RPC error data.
    Used to bubble errors up from Artisans to the Dispatcher.
    """

    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)

    def to_response(self, req_id: RequestId) -> Response:
        """Transmutes the exception into a JSON-RPC Response."""
        # [THE FIX]: Use build_error instead of error
        return Response.build_error(req_id, self.code, self.message, self.data)

    # --- FACTORY METHODS ---

    @classmethod
    def parse_error(cls, data: Any = None) -> 'JsonRpcError':
        return cls(ErrorCodes.PARSE_ERROR, "Parse error", data)

    @classmethod
    def invalid_request(cls, data: Any = None) -> 'JsonRpcError':
        return cls(ErrorCodes.INVALID_REQUEST, "Invalid Request", data)

    @classmethod
    def method_not_found(cls, method: str, data: Any = None) -> 'JsonRpcError':
        return cls(ErrorCodes.METHOD_NOT_FOUND, f"Method '{method}' not found", data)

    @classmethod
    def invalid_params(cls, details: str) -> 'JsonRpcError':
        return cls(ErrorCodes.INVALID_PARAMS, f"Invalid params: {details}")

    @classmethod
    def internal_error(cls, details: str) -> 'JsonRpcError':
        return cls(ErrorCodes.INTERNAL_ERROR, "Internal error", data=details)

    @classmethod
    def server_not_initialized(cls) -> 'JsonRpcError':
        return cls(ErrorCodes.SERVER_NOT_INITIALIZED, "Server not initialized")

    @classmethod
    def request_cancelled(cls) -> 'JsonRpcError':
        return cls(ErrorCodes.REQUEST_CANCELLED, "Request cancelled")