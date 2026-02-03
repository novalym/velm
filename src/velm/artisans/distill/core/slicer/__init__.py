# Path: scaffold/artisans/distill/core/slicer/__init__.py
# -------------------------------------------------------

"""
=================================================================================
== THE SANCTUM OF SURGICAL PERCEPTION (V-Ω-MODULAR)                            ==
=================================================================================
This sanctum houses the Causal Slicer, the artisan responsible for the atomic
dissection of source code based on semantic relevance.
"""

from .engine import CausalSlicer
from .contracts import SliceProfile

__all__ = ["CausalSlicer", "SliceProfile"]