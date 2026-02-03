# Path: core/lsp/protocol/__init__.py
# -----------------------------------

"""
=================================================================================
== THE PROTOCOL FORTRESS (V-Ω-PHYSICS-LAYER)                                   ==
=================================================================================
The IO handling layer of the Gnostic LSP.
Decouples Framing, Transport, and Message Routing from the Logic.

[EXPORTS]:
- JsonRpcEndpoint: The high-level controller (The Governor).
- LspStream: The abstract base for IO.
- StdioStream: Standard Input/Output transport.
- SocketStream: TCP/IP transport.
- MemoryStream: In-memory buffer for testing/simulation.
- ProtocolTelemetry: The vital signs monitor.
"""

from .endpoint import JsonRpcEndpoint
from .streams import LspStream, StdioStream, SocketStream, MemoryStream
from .telemetry import ProtocolTelemetry

__all__ = [
    "JsonRpcEndpoint",
    "LspStream",
    "StdioStream",
    "SocketStream",
    "MemoryStream",
    "ProtocolTelemetry"
]