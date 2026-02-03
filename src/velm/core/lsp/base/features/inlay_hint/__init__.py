# Path: core/lsp/features/inlay_hint/__init__.py
# ----------------------------------------------

"""
=================================================================================
== THE GHOST SCRIPTORIUM (V-Ω-INLAY-HINT-CORE-V12)                             ==
=================================================================================
The engine of spectral annotation.
Projects non-textual information directly into the editor's visual lattice.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import InlayHintEngine
from .contracts import InlayHintProvider
from .models import InlayHint, InlayHintParams, InlayHintKind

__all__ = ["InlayHintEngine", "InlayHintProvider", "InlayHint", "InlayHintParams", "InlayHintKind"]