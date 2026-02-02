# Path: core/lsp/features/code_lens/__init__.py
# ----------------------------------------------

"""
=================================================================================
== THE GUTTER SCRIPTORIUM (V-Ω-CODE-LENS-CORE-V12)                             ==
=================================================================================
The engine of interactive annotation.
Projects actionable commands and metadata directly above lines of code.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import CodeLensEngine
from .contracts import CodeLensProvider
from .models import CodeLens, CodeLensParams

__all__ = ["CodeLensEngine", "CodeLensProvider", "CodeLens", "CodeLensParams"]