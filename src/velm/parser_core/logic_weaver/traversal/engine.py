# Path: parser_core/logic_weaver/traversal/engine.py
# --------------------------------------------------

import time
import gc
from pathlib import Path
from typing import List, Tuple, Optional

from .context import SpacetimeContext
from .walker import DimensionalWalker
from ..state import GnosticContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....contracts.symphony_contracts import Edict
from ....core.alchemist import DivineAlchemist
from ....logger import Scribe

Logger = Scribe("GnosticTraversal")


class TraversalEngine:
    """
    =================================================================================
    == THE ENGINE OF DIMENSIONAL TRAVERSAL (V-Ω-TOTALITY-FACADE)                   ==
    =================================================================================
    LIF: ∞ | ROLE: CORTEX_ORCHESTRATOR | RANK: OMEGA_SINGULARITY

    The unified public gateway to the newly ascended Directory Sanctum.
    It orchestrates the `SpacetimeContext` and the `DimensionalWalker` to generate
    the final executable Quaternity.
    """

    def __init__(
            self,
            context: GnosticContext,
            alchemist: DivineAlchemist,
            parser_edicts: List[Edict],
            # [ASCENSION]: The Sacred 4-Tuple Input Type
            parser_post_run: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """The Rite of Memory Allocation."""

        # Transmute lists into O(1) Lookup Maps
        edict_map = {e.line_num: e for e in parser_edicts}
        post_run_map = {cmd_tuple[1]: cmd_tuple for cmd_tuple in parser_post_run}

        self.ctx = SpacetimeContext(context, alchemist, edict_map, post_run_map)
        self.walker = DimensionalWalker(self.ctx)

    def traverse(self, node: _GnosticNode, current_path: Path):
        """
        [THE RITE OF THE GRAND WALK]
        Ignites the Dimensional Walker, traversing the entire AST and harvesting reality.
        """
        self.walker.walk(node, current_path, self.ctx)

    @property
    def items(self) -> List[ScaffoldItem]:
        return self.ctx.items

    @property
    def post_run_commands(self) -> List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]:
        return self.ctx.post_run_commands

    @property
    def edicts(self) -> List[Edict]:
        return self.ctx.edicts

    @property
    def heresies(self) -> List[Heresy]:
        return self.ctx.heresies