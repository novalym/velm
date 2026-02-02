# Path: scaffold/artisans/gui/artisan.py
# --------------------------------------

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import GuiRequest
from ...help_registry import register_artisan

try:
    from .app import OmniBarApp

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


@register_artisan("gui")
class GuiArtisan(BaseArtisan[GuiRequest]):
    """
    =============================================================================
    == THE OMNI-BAR (V-Ω-META-UI)                                              ==
    =============================================================================
    LIF: 10,000,000,000

    Dynamically generates a TUI for every registered artisan in the system.
    """

    def execute(self, request: GuiRequest) -> ScaffoldResult:
        if not TEXTUAL_AVAILABLE:
            return self.failure("The Omni-Bar requires 'textual'. pip install textual")

        # 1. Harvest Gnosis (The Registry)
        # We pass the engine so the App can inspect the registry.
        app = OmniBarApp(self.engine, initial_filter=request.initial_filter)

        # 2. The Rite of Interface
        # The app returns a tuple: (command_name, request_object)
        result = app.run()

        if not result:
            return self.success("The Architect dismissed the Omni-Bar.")

        command_name, child_request = result

        self.console.rule(f"[bold magenta]Executing: {command_name}[/bold magenta]")

        # 3. The Divine Delegation
        # We dispatch the constructed request back to the engine.
        return self.engine.dispatch(child_request)