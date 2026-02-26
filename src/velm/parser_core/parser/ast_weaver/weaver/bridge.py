# Path: parser_core/parser/ast_weaver/weaver/bridge.py
# ------------------------------------------------------

from typing import List, Tuple, Optional, Any, TYPE_CHECKING

from .....contracts.data_contracts import _GnosticNode, ScaffoldItem
from .....contracts.heresy_contracts import Heresy
from .....contracts.symphony_contracts import Edict

if TYPE_CHECKING:
    from ...engine import ApotheosisParser

# [THE ASCENDED TYPE]: The Sacred Quaternity
Quaternity = Tuple[str, int, Optional[List[str]], Optional[List[str]]]


class DimensionalBridge:
    """
    =============================================================================
    == THE DIMENSIONAL BRIDGE (V-Ω-QUATERNITY-CAST-ULTIMA)                     ==
    =============================================================================
    The bridge to the LogicWeaver. It resolves the 'Type Schism' by performing
    a mathematically perfect cast of the command ledger before invocation.
    """

    @classmethod
    def resolve_paths_from_ast(
            cls,
            parser: 'ApotheosisParser',
            node: _GnosticNode
    ) -> Tuple[List[ScaffoldItem], List[Quaternity], List[Heresy], List[Edict]]:
        """
        [ASCENSION 1]: THE QUATERNITY CAST (THE CURE).
        Righteously ensures the master parser's `post_run_commands` conform exactly
        to the strict typing expected by the GnosticLogicWeaver.
        """
        from ....logic_weaver import GnosticLogicWeaver

        # --- MOVEMENT I: THE RITE OF PURIFICATION (TYPE CASTING) ---
        safe_commands: List[Quaternity] = []

        for cmd in parser.post_run_commands:
            # Pad the tuple to exactly 4 elements using None
            padded = list(cmd) + [None] * (4 - len(cmd))

            # Enforce the strict types of the Quaternity
            safe_cmd: Quaternity = (
                str(padded[0]),  # Command string
                int(padded[1]),  # Line number
                padded[2],  # Optional Undo block
                padded[3]  # Optional Heresy block
            )
            safe_commands.append(safe_cmd)

        # --- MOVEMENT II: BESTOW THE DOWRY ---
        # [ASCENSION 8]: The Gnostic Dowry Seal
        weaver = GnosticLogicWeaver(
            root=node,
            context=parser.variables,
            alchemist=parser.alchemist,
            all_edicts=parser.edicts,
            post_run_commands=safe_commands  # <--- HEALED AND PURIFIED
        )

        # --- MOVEMENT III: THE LOGIC STRIKE ---
        resolved_items, extra_commands_tuples, heresies, resolved_edicts = weaver.weave()

        # --- MOVEMENT IV: PERSISTENCE SYNC ---
        parser.post_run_commands = extra_commands_tuples

        # [ASCENSION 23 & 24]: The Quaternity Tuple Destructuring & Finality Vow
        return resolved_items, extra_commands_tuples, heresies, resolved_edicts