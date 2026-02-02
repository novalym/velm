# Path: artisans/neural_link/artisan.py
# -------------------------------------

import sys
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ObserveRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy

# Lazy load TUI
try:
    from .dashboard import NeuralDashboardApp

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


@register_artisan("observe")
class NeuralLinkArtisan(BaseArtisan[ObserveRequest]):
    """
    =================================================================================
    == THE NEURAL LINK (V-Ω-RUNTIME-XRAY)                                          ==
    =================================================================================
    LIF: 10,000,000,000

    A TUI Dashboard that visualizes the heartbeat of a running system.
    It perceives CPU/RAM vitals, tails logs with semantic highlighting, and
    visualizes HTTP traffic velocity.
    """

    def execute(self, request: ObserveRequest) -> ScaffoldResult:
        if not TEXTUAL_AVAILABLE:
            return self.failure("The Neural Link requires 'textual'. pip install textual")

        self.logger.info("Establishing Neural Link...")

        try:
            app = NeuralDashboardApp(
                target_pid=request.target_pid,
                log_file=request.log_stream,
                demo_mode=request.demo
            )
            app.run()
            return self.success("Neural Link disconnected.")
        except Exception as e:
            raise ArtisanHeresy(f"The Dashboard shattered: {e}", child_heresy=e)