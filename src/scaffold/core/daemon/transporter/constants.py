# Path: scaffold/core/daemon/transporter/constants.py
# ---------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_PY_CONSTANTS_BINARY_V999
# SYSTEM: KINETIC_PHYSICS | ROLE: IMMUTABLE_LAWS
# =================================================================================
# == THE LAWS OF KINETIC TRANSFER (PYTHON: BINARY EDITION)                       ==
# =================================================================================

import re

# [PROTOCOL PHYSICS]
# The dimensional barrier between Meta-Data (Header) and Gnosis (Body).
# [CRITICAL]: Must be bytes (b'') to interact with socket data.
HEADER_TERMINATOR = b'\r\n\r\n'

# The Regex to divine the mass of the payload from the header.
# Compiled once at module level for O(1) access.
# [CRITICAL]: Pattern must be bytes (rb'') to search bytearrays.
HEADER_REGEX = re.compile(rb'Content-Length: (\d+)', re.IGNORECASE)

# [MEMORY ALLOCATION]
# 64KB - Aligns with L1 CPU Cache pages for max throughput.
DEFAULT_CHUNK_SIZE = 65536

# 64MB - The maximum allowed thought size.
MAX_PAYLOAD_SIZE = 64 * 1024 * 1024

# Safety Valve: 1.2x Max Payload. If buffer exceeds this without header, PURGE.
BUFFER_SAFETY_CAP = int(MAX_PAYLOAD_SIZE * 1.2)

# [SOCKET PHYSICS]
# Kernel buffer size target (1MB) to prevent syscall blocking.
KERNEL_BUFFER_SIZE = 1048576

# [FORENSICS]
# Toggle this to True to flood stdout with hex dumps on error (Use with caution)
PARANOID_LOGGING = True