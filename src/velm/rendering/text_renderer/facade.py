# Path: scaffold/rendering/text_renderer/facade.py
# ------------------------------------------------
from typing import List, Union, Any, Optional
from rich.console import Group as RenderableGroup

from .config import RendererConfig
from .luminous_scribe import LuminousScribe
from .canonical_scribe import CanonicalScribe
from ..base_renderer import GnosticTreeRenderer
from ..theme import GnosticTheme
from ...contracts.data_contracts import ScaffoldItem


class TextRenderer(GnosticTreeRenderer):
    """
    =================================================================================
    == THE PURE CONDUCTOR (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++. THE UNIFIED VOICE)     ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Public API for text rendering.
    It performs the Gnostic Triage using the new modular scribes.
    """

    def __init__(self,
                 items: List[ScaffoldItem],
                 use_markup: bool = True,
                 app_state: Optional[Any] = None,
                 **kwargs: Any):

        enabled_inquisitors = kwargs.pop('enabled_inquisitors', None)

        # Forge the Config Vessel
        self.config = RendererConfig(
            theme=GnosticTheme(),
            variables=kwargs.pop('variables', {}),
            post_run_commands=kwargs.pop('post_run_commands', []),
            verbose=kwargs.pop('verbose', False),
            pure_structure=kwargs.pop('pure', False),
            app_state=app_state
        )

        self.use_markup = use_markup

        super().__init__(items, enabled_inquisitors=enabled_inquisitors, **kwargs)

    def render(self) -> Union[str, RenderableGroup]:
        """
        The one true Rite of Proclamation.
        """
        target_node = self.root

        if self.use_markup:
            # Path 1: Luminous Revelation (Rich Markup)
            scribe = LuminousScribe(target_node, self.config)
            return RenderableGroup(*scribe.transcribe())
        else:
            # Path 2: Gnostic Purity (Canonical Syntax)
            scribe = CanonicalScribe(target_node)
            return "\n".join(scribe.transcribe())