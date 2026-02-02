# Path: core/lsp/features/semantic_tokens/__init__.py
# ---------------------------------------------------

"""
=================================================================================
== THE SPECTRAL SCRIPTORIUM (V-Ω-SEMANTIC-CORE-V12)                            ==
=================================================================================
The engine of semantic illumination.
Transmutes the soul of the code into a dense integer stream of meaning.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import SemanticTokensEngine
from .contracts import TokenProvider
from .legend import TokenLegend, get_default_legend
from .models import SemanticTokens, SemanticTokensParams

__all__ = ["SemanticTokensEngine", "TokenProvider", "TokenLegend", "get_default_legend", "SemanticTokens", "SemanticTokensParams"]