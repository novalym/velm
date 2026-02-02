# Path: core/lsp/base/features/inline_completion/__init__.py
# ----------------------------------------------------------

"""
=================================================================================
== THE HALL OF PROPHECY (V-Ω-INLINE-COMPLETION-CORE)                           ==
=================================================================================
The engine of Ghost Text.
Projects predictive text directly into the editor's future stream.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import InlineCompletionEngine
from .contracts import InlineCompletionProvider
from .models import InlineCompletionItem, InlineCompletionList

__all__ = ["InlineCompletionEngine", "InlineCompletionProvider", "InlineCompletionItem", "InlineCompletionList"]