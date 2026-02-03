# Path: core/lsp/base/features/folding_range/__init__.py
# ------------------------------------------------------

"""
=================================================================================
== THE GEOMETRIC COMPRESSOR (V-Ω-FOLDING-CORE-V12)                             ==
=================================================================================
The engine of spatial compression.
Identifies regions of the scripture that can be collapsed into singularities.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import FoldingRangeEngine
from .contracts import FoldingRangeProvider
from .models import FoldingRange, FoldingRangeParams, FoldingRangeKind

__all__ = [
    "FoldingRangeEngine",
    "FoldingRangeProvider",
    "FoldingRange",
    "FoldingRangeParams",
    "FoldingRangeKind"
]