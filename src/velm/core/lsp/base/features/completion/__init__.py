# Path: core/lsp/features/completion/__init__.py
# ----------------------------------------------

"""
=================================================================================
== THE HALL OF PROPHECY (V-Ω-COMPLETION-CORE)                                  ==
=================================================================================
The engine of precognition.
It anticipates the Architect's intent and offers Gnostic suggestions.

This is the language-agnostic foundation.
=================================================================================
"""

from .engine import CompletionEngine
from .contracts import CompletionProvider, CompletionContext
from .models import CompletionItem, CompletionList

__all__ = ["CompletionEngine", "CompletionProvider", "CompletionContext", "CompletionList"]