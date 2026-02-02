# Path: core/lsp/scaffold_features/selection_range/__init__.py
# ------------------------------------------------------------
from .engine import ScaffoldSelectionRangeEngine
from .providers.semantic_expander import SemanticExpanderProvider

__all__ = ["ScaffoldSelectionRangeEngine", "SemanticExpanderProvider"]