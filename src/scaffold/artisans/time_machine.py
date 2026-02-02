# scaffold/artisans/time_machine.py

"""
=================================================================================
== THE KEEPER OF THE GATEWAY (V-Ω-ETERNAL-ALIAS)                               ==
=================================================================================
This divine artisan is a pure Gnostic Alias. Its one true purpose is to serve as
a luminous gateway, receiving the `time-machine` plea and immediately delegating
it to the ascended `HistoryArtisan`, the true master of the Altar of Time.
=================================================================================
"""
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import TimeMachineRequest, HistoryRequest
from ..help_registry import register_artisan


@register_artisan("time-machine")
class TimeMachineArtisan(BaseArtisan[TimeMachineRequest]):
    """The Gnostic gateway to the interactive timeline."""

    def execute(self, request: TimeMachineRequest) -> ScaffoldResult:
        """
        The Rite of Pure Delegation.
        Transmutes the plea and passes it to the Chronomancer.
        """
        self.logger.info("The Time Machine gateway opens. Delegating to the Chronomancer (`history`)...")

        # We forge a new HistoryRequest from the will of the TimeMachineRequest.
        # Since their souls are now identical, this is a pure transmutation.
        history_request = HistoryRequest.model_validate(request.model_dump())

        # We explicitly set the command to None to trigger the interactive TUI
        history_request.command = None

        # Summon the true artisan.
        from .history.artisan import HistoryArtisan
        return HistoryArtisan(self.engine).execute(history_request)