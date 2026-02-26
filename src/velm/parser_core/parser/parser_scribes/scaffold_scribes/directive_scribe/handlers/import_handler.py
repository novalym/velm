# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/import_handler.py
# ---------------------------------------------------------------------------------------------------------------------
import shlex
from typing import List
from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class ImportHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MULTIVERSAL GATEKEEPER (V-Ω-TOTALITY-V41-DECAPITATED)                   ==
    =================================================================================
    LIF: 10,000 | ROLE: INHALATION_DISPATCHER

    [ASCENSION 41]: THE DECAPITATION.
    This artisan has been purified. It contains NO parsing logic. It exists solely to
    parse the shell-like arguments of the `@import` directive and delegate the heavy
    lifting to the `GnosticImportManager` organ.

    Handles:
    - @import <path> [as <alias>]
    - @from <path> import <atoms>

    [FEATURES]:
    1.  **Shlex Argument Parsing:** Handles quoted paths with spaces correctly.
    2.  **JIT Manager Summons:** Materializes the Import Manager only when needed.
    3.  **Strict Syntax Validation:** Rejects malformed import pleas before delegation.
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Rite of Inhalation.
        """
        raw_line = vessel.raw_scripture.strip()

        try:
            # [ASCENSION 1]: SHELL-SAFE LEXING
            # We use shlex to split the line, preserving quoted strings.
            # Example: @import "my folder/script.scaffold" as my_script
            tokens = shlex.split(raw_line)
        except ValueError as e:
            raise ArtisanHeresy(
                f"Lexical Fracture in import statement: {e}",
                details="Unbalanced quotes detected.",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # Validation: Must have at least @import and a target
        if len(tokens) < 2:
            raise ArtisanHeresy(
                "Incomplete Inhalation Plea.",
                details="Usage: @import <path> [as alias] OR @from <path> import <items>",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 41]: THE DELEGATION
        # We perform a late-bound import to avoid circular dependency at module load time.
        from ......logic_weaver.import_manager.engine import GnosticImportManager

        # Summon the Manager, binding it to the current Parser state
        manager = GnosticImportManager(self.parser)

        # Strike: Command the Manager to inhale the foreign reality.
        # It returns the new line index (the time coordinate after inhalation).
        # We pass `tokens[1:]` (arguments without the directive) and the full raw line for context.
        next_i = manager.conduct_inhalation(i, tokens[1:], raw_line)

        return next_i