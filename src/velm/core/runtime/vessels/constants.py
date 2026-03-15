# =========================================================================================
# Path: core/runtime/vessels/constants.py
# =========================================================================================
"""
=================================================================================
== THE IMMUTABLE LAWS OF DATA (V-Ω-TOTALITY)                                   ==
=================================================================================
"""
from typing import Final, Set

# [ASCENSION 1]: THE JINJALESS PURIFICATION.
# These keys represent the "Prefrontal Cortex" of the resolution engine.
SGF_SYSTEM_INVARIANTS: Final[Set[str]] = {
    'logic', 'math', 'os', 'time', 'str', 'sec', 'cloud', 'ui', 'ai', 'auth',
    'id', 'infra', 'integration', 'iris', 'mock', 'monitor', 'neuron',
    'ops', 'policy', 'pulse', 'shadow', 'sim', 'soul', 'stack', 'struct',
    'test', 'topo', 'veritas', 'aether', 'chronos', 'cortex', 'flux',
    'hive', 'iter', 'law', 'meta', 'pact', 'signal', 'path'
}

# =========================================================================================
# == [ASCENSION 2]: THE SYSTEM RESERVOIR SHIELD (THE MASTER CURE)                        ==
# =========================================================================================
# These keys are the "Physical Arteries" of the God-Engine. They must NEVER be
# recursively voided. They must return None if missing, triggering the correct
# Parent/Global fallback logic in the Resolver/Parser.
SGF_RESERVOIRS: Final[Set[str]] = {
    '__woven_matter__', '__woven_commands__', '__engine__', '__alchemist__',
    '__current_file__', '__current_dir__', '__import_anchor__', '__trace_id__',
    '__parse_depth__', '__spacetime_id__', '__start_time_ns__', '_start_time_ns',
    '__current_line_aura__'
}

# =========================================================================================
# == [ASCENSION 3]: THE TENSOR SHIELD (AI COMPATIBILITY)                                 ==
# =========================================================================================
# Prevents the GnosticSovereignDict from attempting to recursively wrap high-dimensional
# mathematical arrays, which would shatter the Engine during RAG/Embedding operations.
SGF_TENSOR_TYPES: Final[Set[str]] = {
    'ndarray', 'Tensor', 'SparseVector', 'Embedding'
}