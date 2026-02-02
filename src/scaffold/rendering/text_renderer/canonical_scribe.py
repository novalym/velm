# Path: scaffold/rendering/text_renderer/canonical_scribe.py
# ----------------------------------------------------------
from typing import List, Iterator

from ...contracts.data_contracts import _GnosticNode
# [THE FIX] We import the new CanonicalSerializer from the modular blueprint_scribe
from ...core.blueprint_scribe import CanonicalSerializer


class CanonicalScribe:
    """
    [EVOLUTION 1] The Pure Syntax Adapter.

    This artisan adapts the stream-based `CanonicalSerializer` (from the Core)
    to the list-based requirements of the TextRenderer's interface.
    It ensures that 'Plain Text' output is perfectly valid `.scaffold` syntax.
    """

    def __init__(self, root: _GnosticNode):
        self.root = root
        # We summon the core serializer
        self._core_serializer = CanonicalSerializer()

    def transcribe(self) -> List[str]:
        """
        Proclaims the pure .scaffold syntax as a list of lines.
        """
        # The Core Serializer yields lines; we consume them into a list
        return list(self._core_serializer.serialize(self.root))