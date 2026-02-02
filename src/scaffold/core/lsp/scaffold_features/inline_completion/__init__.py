# Path: core/lsp/scaffold_features/inline_completion/__init__.py
# --------------------------------------------------------------

from .engine import ScaffoldInlineCompletionEngine
from .providers.muse import MuseProphet
from .providers.snippet import SnippetProphet

__all__ = ["ScaffoldInlineCompletionEngine", "MuseProphet", "SnippetProphet"]