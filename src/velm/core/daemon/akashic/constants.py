# Path: core/daemon/akashic/constants.py
# --------------------------------------
# LIF: INFINITY | ROLE: CONFIGURATION_STONE
"""
The Immutable Laws governing the Akashic Record.
"""

# The maximum number of thoughts the Daemon retains in RAM.
# 5000 allows for deep forensic replay without consuming excessive heap.
MAX_HISTORY_DEPTH = 5000

# The maximum number of critical heresies (Errors) to keep PINNED in memory,
# ensuring they are never rotated out by spammy debug logs.
MAX_PINNED_HERESIES = 100

# Time (seconds) to wait for a client socket to accept data before
# considering it dead/slow and pruning it.
BROADCAST_TIMEOUT = 0.5

# Semantic Tags for Routing
TAG_HERESY = "HERESY"
TAG_KINETIC = "KINETIC"
TAG_INTERNAL = "INTERNAL_BRIDGE"

