# Path: core/lsp/scaffold_features/completion/providers/__init__.py
# -----------------------------------------------------------------

"""
=================================================================================
== THE COUNCIL OF PROPHETS (V-Ω-COMPLETION-PROVIDERS)                          ==
=================================================================================
The assembly of specialized oracles that predict the Architect's intent.

[EXPORTS]:
- KeywordProphet: Static syntax (keywords, sigils).
- VariableProphet: Dynamic state ($$ variables).
- PathProphet: Filesystem topology.
- ArtisanBridgeProphet: Deep Daemon inference.
"""

from .keyword_prophet import KeywordProphet
from .variable_prophet import VariableProphet
from .path_prophet import PathProphet
from .internal import InternalCompletionProvider

__all__ = [
    "KeywordProphet",
    "VariableProphet",
    "PathProphet",
    "InternalCompletionProvider"
]