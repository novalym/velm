# Path: core/runtime/engine/constants.py
# --------------------------------------
"""
The Immutable Laws governing the Engine's reality.
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
SACRED_RITES = {'initialize', 'shutdown', 'ping', 'status', '$/heartbeat'}
FAST_RITES = SACRED_RITES.union({'hover', 'completion', 'definition', 'signature'})