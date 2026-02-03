# Path: core/lsp/scaffold_features/hover/providers/__init__.py
# ------------------------------------------------------------

"""
=================================================================================
== THE COUNCIL OF SCHOLARS (V-Ω-HOVER-PROVIDERS)                               ==
=================================================================================
The assembly of specialized oracles that reveal the hidden truth of symbols.

[EXPORTS]:
- LexiconProvider: Explains static keywords ($$, @if).
- AlchemyProvider: Reveals dynamic variable values.
- MatterProvider: Confirms file existence.
- BridgeProvider: Queries the Daemon for deep Gnosis.
- MentorProvider: Offers Socratic architectural advice.
"""


from .alchemy import AlchemyProvider
from .matter import MatterProvider
from .internal import InternalHoverProvider
from .mentor import MentorProvider

__all__ = [
    "AlchemyProvider",
    "MatterProvider",
    "InternalHoverProvider",
    "MentorProvider"
]