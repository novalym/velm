# Path: parser_core/logic_weaver/traversal/context.py
# ---------------------------------------------------

import threading
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path

from ....contracts.data_contracts import ScaffoldItem
from ....contracts.heresy_contracts import Heresy
from ....contracts.symphony_contracts import Edict
from ..state import GnosticContext
from ....core.alchemist import DivineAlchemist


class SpacetimeContext:
    """
    =============================================================================
    == THE VESSEL OF SPACETIME (V-Ω-SHARED-MEMORY-LATTICE)                     ==
    =============================================================================
    A unified memory vessel passed by reference through the recursive walk.
    It holds the harvested matter (items) and kinetic will (commands).

    [THE CURE]: It enables 'Isolated Timelines', allowing the Reaper to spawn a
    sub-context to evaluate @if logic natively inside ON_HERESY blocks!
    """

    def __init__(
            self,
            gnostic_context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: Dict[int, Edict],
            parser_post_run: Dict[int, Tuple]
    ):
        self.gnostic_context = gnostic_context
        self.alchemist = alchemist
        self.parser_edicts = parser_edicts
        self.parser_post_run = parser_post_run

        # --- The Harvested Reality ---
        self.items: List[ScaffoldItem] = []

        # The Sacred Quaternity: (Cmd, Line, Undo, Heresy)
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        self.edicts: List[Edict] = []
        self.heresies: List[Heresy] = []

        # Topological Tracking
        self.visibility_map: Dict[int, bool] = {}
        self.materialized_paths: Dict[str, int] = {}

    def spawn_isolated_timeline(self) -> 'SpacetimeContext':
        """
        [ASCENSION 1]: THE ISOLATED TIMELINE SUTURE.
        Forges a child context to capture commands within a localized block
        (e.g., ON_HERESY) without polluting the global command stream.
        """
        child = SpacetimeContext(
            self.gnostic_context,
            self.alchemist,
            self.parser_edicts,
            self.parser_post_run
        )
        # We share the topological state to prevent duplicate path warnings,
        # but the harvested lists (items, commands) remain strictly isolated!
        child.materialized_paths = self.materialized_paths
        child.visibility_map = self.visibility_map
        return child