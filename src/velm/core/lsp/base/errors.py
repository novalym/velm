# Path: core/lsp/base/errors.py
# ----------------------------
import traceback
from typing import Any, Optional, Dict
from .rpc import JsonRpcError, ErrorCodes


class ErrorForge:
    """
    =============================================================================
    == THE ERROR FORGE (V-Ω-FORENSIC-ADJUDICATOR)                             ==
    =============================================================================
    Transmutes chaotic Python exceptions into structured Gnostic Heresies.
    """

    @staticmethod
    def forge(exc: Exception, method: str) -> JsonRpcError:
        """Divines the correct protocol error based on exception type."""
        tb = traceback.format_exc()

        if isinstance(exc, TypeError):
            return JsonRpcError.invalid_params(f"Parameter Paradox in {method}: {str(exc)}")

        if isinstance(exc, NotImplementedError):
            return JsonRpcError.method_not_found(method)

        # [ASCENSION 12]: Default to InternalError with full Forensic Autopsy
        return JsonRpcError.internal_error(
            details=f"{type(exc).__name__}: {str(exc)}",
            data={"traceback": tb}
        )