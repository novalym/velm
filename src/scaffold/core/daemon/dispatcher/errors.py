# Path: core/daemon/dispatcher/errors.py
# --------------------------------------
# LIF: INFINITY | ROLE: FORENSIC_ERROR_FACTORY
import time
import traceback
from typing import Dict, Any, Optional

class ErrorForge:
    """
    [THE FORENSIC SCRIPTORIUM]
    Transmutes chaos (Exceptions) into order (JSON-RPC Errors).
    """

    @staticmethod
    def forge(req_id: Any, 
              code: int, 
              message: str, 
              data: Optional[Dict] = None, 
              exc: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Creates a structured error response.
        If an exception is provided, extracts the traceback.
        """
        trace = None
        if exc:
            # Capture the stack trace of the fracture
            trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": code,
                "message": message,
                "data": {
                    "payload": data or {},
                    "traceback": trace,
                    "timestamp": time.time(),
                    "exception_type": type(exc).__name__ if exc else "GnosticError"
                }
            },
            "success": False
        }