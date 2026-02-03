# Path: core/daemon/dispatcher/constants.py
# -----------------------------------------
# LIF: INFINITY | ROLE: CEREBRAL_CONSTANTS
"""
The Immutable Laws governing the Dispatcher's decision making.
"""

# [TEMPORAL BOUNDARIES]
TIMEOUT_CORTEX = 30.0    # Seconds for fast thoughts (LSP)
TIMEOUT_FOUNDRY = 300.0  # Seconds for heavy rites (Genesis)

# [CAPACITY LIMITS]
MAX_CORTEX_WORKERS = 12
MAX_FOUNDRY_WORKERS = 8
MAX_QUEUE_DEPTH = 64     # Backpressure threshold

# [IDENTIFIERS]
POOL_CORTEX = "CortexLens"
POOL_FOUNDRY = "ArtisanFoundry"

# [RITE CLASSIFICATION]
# Rites that must flow through the fast Cortex pool
FAST_RITES = {
    'initialize',     # The sacred handshake
    'shutdown',       # The final goodbye
    '$/heartbeat',    # Vitality pulse
    'status',         # Gaze status
    'completion',     # High-frequency intelligence
    'hover',
    'definition'
}