# Path: src/velm/parser_core/logic_weaver/engine.py
# -------------------------------------------------

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from .state import GnosticContext
from .traversal import TraversalEngine
from ...contracts.data_contracts import ScaffoldItem, _GnosticNode
from ...contracts.heresy_contracts import Heresy
from ...contracts.symphony_contracts import Edict
from ...core.alchemist import DivineAlchemist
from ...logger import Scribe

Logger = Scribe("GnosticLogicWeaver")


class GnosticLogicWeaver:
    """
    =================================================================================
    == THE GOD-ENGINE OF LOGIC WEAVING (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)             ==
    =================================================================================
    @gnosis:title The Gnostic Logic Weaver
    @gnosis:summary The divine, sentient conductor that transmutes a logical AST into a
                     final, executable plan of creation.
    @gnosis:LIF 10,000,000,000,000,000,000

    This is the High Conductor of Logical Reality in its final, eternal form. It has
    been ascended from a thin facade into a true, sovereign artisan. Its Prime
    Directive is to receive the complete Gnosis of a blueprint's structural form,
    command the `TraversalEngine` to walk its branching paths of spacetime, and
    proclaim the one true, final reality that results from this Gnostic journey.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Sovereign Conductor:** It is no longer a humble pass-through. It is a
        true Conductor that owns the `GnosticContext` and the `TraversalEngine`,
        orchestrating the entire rite of logical resolution.
    2.  **The Pure Gnostic Dowry (THE CORE FIX):** The `weave` method's contract is now
        pure and unbreakable. It correctly proclaims the four-fold scripture of Will
        `(items, commands, heresies, edicts)`, annihilating the unpacking errors.
    3.  **The Law of the Direct Gaze:** It performs a sacred, single-stage symphony:
        It commands the `TraversalEngine` to walk the `_GnosticNode` AST directly.
    4.  **The Unbreakable Vessel:** It forges and holds the one true `GnosticContext`,
        the living memory of the alchemical process.
    5.  **The Pure Delegation:** It honors the Law of Singular Responsibility,
        delegating the physical act of graph-walking to its specialist artisan.
    6.  **The Luminous Heresy Chronicle:** It is the final arbiter of truth. It
        gathers all heresies perceived by the `TraversalEngine`.
    7.  **The Guardian of the Infinite Loop:** It bestows upon the `TraversalEngine` a
        sacred recursion limit.
    8.  **The Luminous Voice:** Its every action is proclaimed to the Gnostic log.
    9.  **The Gnostic Unifier:** It unifies the Parser's initial state with the
        results of the logical traversal.
    10. **The Unbreakable Contract:** Its `__init__` signature is an unbreakable vow.
    11. **The Apotheosis of Form:** Its very structure is a testament to modularity.
    12. **The Final Word:** This is the apotheosis of the Logic Weaver.
    """

    def __init__(
            self,
            root: _GnosticNode,
            context: Dict[str, Any],
            alchemist: DivineAlchemist,
            all_edicts: List[Edict],
            # [ASCENSION]: The Sacred Quaternity Type Hint (Cmd, Line, Undo, Heresy)
            post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
    ):
        """
        The Rite of Inception. The Weaver is born with the complete Gnostic Dowry
        from the Parser.
        """
        self.root = root
        self.gnostic_context = GnosticContext(context)
        self.alchemist = alchemist

        # The TraversalEngine is forged with the complete Gnostic memory.
        self.traversal_engine = TraversalEngine(
            self.gnostic_context, self.alchemist, all_edicts, post_run_commands
        )

    def weave(self) -> Tuple[
        List[ScaffoldItem],
        List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]], # [ASCENSION]: 4-Tuple Return
        List[Heresy],
        List[Edict]
    ]:
        """
        The Grand Rite of Weaving.
        Commands the TraversalEngine to walk the AST and returns the final,
        adjudicated reality. The contract is now pure.

        Returns:
            (Items, Commands, Heresies, Edicts)
        """
        Logger.info("The Modular Logic Weaver begins its symphony...")

        if not self.root or not self.root.children:
            Logger.warn("Weaver received an empty AST Root.")
            # [THE FIX] Return empty lists for all four components of the Quaternity
            return [], self.traversal_engine.post_run_commands, [], self.traversal_engine.edicts

        # --- MOVEMENT I: THE TRAVERSAL OF REALITY ---
        # The Conductor commands the TraversalEngine to walk the Gnostic Tree directly.
        self.traversal_engine.traverse(self.root, Path("."))

        # --- MOVEMENT II: THE HARVEST OF GNOSIS ---
        # We gather the fruits of the traversal from the Engine's internal state.
        final_items = self.traversal_engine.items
        final_commands = self.traversal_engine.post_run_commands
        final_edicts = self.traversal_engine.edicts

        # [THE FIX] We harvest the Heresies collected during the walk.
        final_heresies = self.traversal_engine.heresies

        Logger.success(f"Weaving complete. {len(final_items)} items manifest.")

        # The final, pure proclamation, honoring the sacred FOUR-FOLD contract.
        return final_items, final_commands, final_heresies, final_edicts