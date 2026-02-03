# Path: scaffold/artisans/distill/core/causality/constants.py
# -----------------------------------------------------------

"""
=================================================================================
== THE LAWS OF PHYSICS (V-Ω-CONSTANTS)                                         ==
=================================================================================
Immutable constants governing the propagation of relevance through the ether.
"""

# The minimal spark of relevance required to keep a file in the context.
# Scores below this are rounded down to the Void.
MIN_RELEVANCE_THRESHOLD = 5.0

# The absolute horizon. No signal travels further than this many hops.
MAX_PROPAGATION_DEPTH = 4

# The standard decay for looking at what a file *needs* (Dependencies).
# We assume dependencies are highly relevant to understanding the seed.
DEFAULT_DEPENDENCY_DECAY = 0.7  # Strong signal

# The standard decay for looking at what *uses* a file (Dependents).
# We assume usage examples are useful but less critical than definitions.
DEFAULT_DEPENDENT_DECAY = 0.4  # Weaker signal

# Hub Definitions:
# If a node has > 20 connections, it is a "Hub" (e.g. utils.py, shared.ts).
# Signals passing through hubs are dampened to prevent exploding the context.
HUB_DEGREE_THRESHOLD = 20
HUB_DAMPENING_FACTOR = 0.3