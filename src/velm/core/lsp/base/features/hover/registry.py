# Path: core/lsp/features/hover/registry.py
# ----------------------------------------
from .contracts import HoverProvider
from typing import List, Dict

class ProviderRegistry:
    """
    [THE TABLE OF SCHOLARS]
    Manages the prioritization of different wisdom sources.
    """
    def __init__(self):
        self._providers: List[HoverProvider] = []

    def add(self, provider: HoverProvider):
        self._providers.append(provider)

    def get_all(self) -> List[HoverProvider]:
        return sorted(self._providers, key=lambda x: x.priority, reverse=True)