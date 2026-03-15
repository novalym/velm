# Path: parser_core/parser/parser_scribes/scaffold_scribes/alchemical_scribe.py
# -----------------------------------------------------------------------------

import re
from typing import List, TYPE_CHECKING

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class AlchemicalScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE RITE OF THE ALCHEMICAL SCRIBE (V-Ω-TOTALITY-VMAX-GATE-SUTURE)           ==
    =================================================================================
    LIF: ∞^∞ | ROLE: SGF_LOGIC_ANCHOR | RANK: OMEGA_SOVEREIGN

    The Scribe's soul is pure SGF. It has been ascended to possess **Gate Clairvoyance**,
    surgically extracting SGF keywords (`if`, `for`, `try`) so the `LogicAdjudicator`
    can correctly traverse and hide AST branches without Jinja2.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "AlchemicalScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        line = lines[i]

        # The Scribe performs its one true duty: perfecting the vessel.
        vessel.is_sgf_construct = True
        vessel.sgf_expression = line.strip()
        vessel.name = line.strip()

        # =========================================================================
        # == [THE MASTER CURE]: PARSE SGF LOGIC GATES                            ==
        # =========================================================================
        # We extract the logic gate directly from the SGF block (`{% if foo %}`)
        # so the DimensionalWalker's Adjudicator knows how to navigate the tree.
        match = re.match(
            r'{%-?\s*(if|elif|else|endif|for|endfor|try|catch|finally|endtry)\b\s*(.*?)-?%}',
            line.strip(),
            re.IGNORECASE
        )

        if match:
            gate = match.group(1).upper()
            condition = match.group(2).strip()

            if gate in ('IF', 'ELIF', 'ELSE', 'ENDIF'):
                vessel.condition_type = f"CONDITIONALTYPE.{gate}"
            elif gate in ('FOR', 'ENDFOR'):
                vessel.condition_type = f"LOOPTYPE.{gate}"
            elif gate in ('TRY', 'CATCH', 'FINALLY', 'ENDTRY'):
                vessel.condition_type = f"RESILIENCETYPE.{gate}"

            vessel.condition = condition

        # The Scribe humbly returns control to the master parser, which will
        # forge a valid ScaffoldItem from this perfected vessel.
        self.parser._proclaim_final_item(vessel)

        self.Logger.verbose(f"L{vessel.line_num}: Chronicled Alchemical Logic: '{line.strip()}'")
        return i + 1