# Path: scaffold/parser_core/parser_scribes/makefile_scribe.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE MAKEFILE SCRIBE (V-Ω-GENESIS)                     ==
=================================================================================
This scripture contains the living soul of the MakefileScribe, a divine
artisan that teaches the God-Engine to perceive the Gnostic grammar of Makefiles.
=================================================================================
"""
import re
from typing import List, TYPE_CHECKING

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class MakefileScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF THE MAKEFILE TONGUE (THE CONTEXTUAL GAZE)                       ==
    =================================================================================
    LIF: 100,000,000,000

    This divine artisan is a master of context. Its Gaze is not blind; it is
    Gnostic. It awakens only when its master, the Parser, proclaims that it is
    within the sacred reality of a `Makefile`. It then perceives the grammar of
    targets and recipes, righteously consuming them to prevent the
    StructuralScribe from misinterpreting them as files.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "MakefileScribe")
        # A Gaze for a valid Makefile target (e.g., "install:", ".PHONY: help").
        # It must start at the beginning of the line and not be preceded by whitespace.
        self.TARGET_REGEX = re.compile(r"^[.A-Za-z0-9_-]+:.*")

    def gaze(self, vessel: GnosticVessel) -> bool:
        """
        Its Gaze is two-fold: Is this a Makefile? And does this line look like a target?
        """
        # Gaze 1: The Gaze of Context
        # The Scribe gazes upon the Parser's memory of the current path.
        parent_node_path = self.parser.path_stack[-1][0] if self.parser.path_stack else ""
        is_in_makefile = "Makefile" in str(parent_node_path)

        if not is_in_makefile:
            return False

        # Gaze 2: The Gaze of Form
        # The Gaze is upon the raw scripture, stripped of only leading whitespace
        # to correctly perceive the target at the start of the line.
        return self.TARGET_REGEX.match(vessel.raw_scripture.lstrip()) is not None

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Scribe perceives the target and consumes its indented recipes. It does not
        forge a new item, but instructs the master Parser to treat this entire
        block as a single unit of content for the parent `Makefile` item.
        This is a rite of temporal manipulation.
        """
        line_num = i + 1 + self.parser.line_offset
        self.Logger.verbose(f"L{line_num:03d}: The MakefileScribe awakens for target '{vessel.raw_scripture.strip()}'.")

        # This Scribe's purpose is to prevent other scribes from acting.
        # It tells the main loop to simply advance past this line, allowing the
        # StructuralScribe's `_conduct_indented_content_rite` to correctly
        # consume it as part of the Makefile's soul.

        # To do this, we simply advance the timeline without creating a new item.
        # This is a Gnostic signal that this line has been "handled" and is not
        # a structural element to be parsed on its own.
        return i + 1