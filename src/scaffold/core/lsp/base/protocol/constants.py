# Path: core/lsp/protocol/constants.py
# ------------------------------------

import re

# [PHYSICS: FRAMING]
# The dimensional barrier between Meta-Data (Header) and Gnosis (Body).
HEADER_TERMINATOR = b"\r\n\r\n"

# The Regex to divine the mass of the payload from the header.
# Compiled as bytes (rb) for zero-copy scanning.
CONTENT_LENGTH_RE = re.compile(rb"Content-Length: (\d+)", re.IGNORECASE)

# [PHYSICS: LIMITS]
# 256KB - Aligns with L2 Cache on modern CPUs for optimal throughput.
DEFAULT_CHUNK_SIZE = 256 * 1024

# 100MB - The maximum allowed thought size. Larger packets are treated as DoS/Heresy.
MAX_PAYLOAD_SIZE = 100 * 1024 * 1024

# [PHYSICS: TIMING]
# How long to wait for a socket write before considering it a blockage (Seconds).
SOCKET_WRITE_TIMEOUT = 5.0

# [METABOLIC NOISE]
# Messages to filter out from high-verbosity logs to prevent console flooding.
SILENT_METHODS = {
    '$/heartbeat',
    'heartbeat',
    'scaffold/progress',
    'textDocument/publishDiagnostics',
    'window/logMessage'
}
