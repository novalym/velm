# Path: core/lsp/scaffold_features/completion/__init__.py
# --------------------------------------------------------
from .engine import ScaffoldCompletionEngine
from .providers import (
    KeywordProphet,
    VariableProphet,
    PathProphet,
    InternalCompletionProvider,
)

__all__ = [
    "ScaffoldCompletionEngine",
    "KeywordProphet",
    "VariableProphet",
    "PathProphet",
    "InternalCompletionProvider",
]