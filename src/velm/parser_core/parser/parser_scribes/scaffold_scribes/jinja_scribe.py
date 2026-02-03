# scaffold/parser_core/parser_scribes/jinja_scribe.py
from typing import List, TYPE_CHECKING

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class JinjaScribe(ScaffoldBaseScribe):
    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "JinjaScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE RITE OF THE HUMBLE SCRIBE (V-Ω-ETERNAL-APOTHEOSIS)                      ==
        =================================================================================
        The Scribe's soul is now pure. It no longer usurps the Parser's authority. Its
        one true purpose is to bestow the Gnosis of Jinja upon the sacred vessel and
        then return control to its master. The heresy of the nameless soul is annihilated.
        =================================================================================
        """
        line = lines[i]

        # The Scribe performs its one true duty: perfecting the vessel.
        vessel.is_jinja_construct = True
        vessel.jinja_expression = line.strip()
        # It bestows a Gnostic Identity upon the logic, fulfilling the sacred law.
        vessel.name = line.strip()

        # The Scribe does NOT proclaim a final item. It humbly returns control to the
        # master parser, which will now always forge a valid ScaffoldItem from this
        # perfected vessel.
        self.parser._proclaim_final_item(vessel)

        self.Logger.verbose(f"L{vessel.line_num}: Chronicled Jinja Logic: '{line.strip()}'")
        return i + 1

