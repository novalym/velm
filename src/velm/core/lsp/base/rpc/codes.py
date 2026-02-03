# Path: core/lsp/rpc/codes.py
# ---------------------------

from enum import IntEnum


class ErrorCodes(IntEnum):
    """
    [THE TABLETS OF LAW]
    Standard JSON-RPC 2.0 Error Codes and LSP extensions.
    """
    # --- Standard JSON-RPC 2.0 ---
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    # --- LSP Reserved Range (-32099 to -32000) ---
    SERVER_NOT_INITIALIZED = -32002
    UNKNOWN_ERROR_CODE = -32001
    REQUEST_CANCELLED = -32800
    CONTENT_MODIFIED = -32801
    REQUEST_FAILED = -32803

    # --- Gnostic Custom (-32099 start) ---
    HERESY_DETECTED = -32099
    DAEMON_UNREACHABLE = -32098
    PROTOCOL_VIOLATION = -32097
    TIMEOUT = -32096