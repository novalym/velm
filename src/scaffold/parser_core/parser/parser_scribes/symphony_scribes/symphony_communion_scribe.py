# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_communion_scribe.py

from typing import List, TYPE_CHECKING, Tuple

from .....utils.core_utils import forge_edict_from_vessel
from .symphony_base_scribe import SymphonyBaseScribe


from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import EdictType

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyCommunionScribe(SymphonyBaseScribe):
    """
    =================================================================================
    == THE COMMUNION SCRIBE (V-Ω-ULTIMA. THE MASTER OF INPUT)                      ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    This artisan conducts the Rite of Communion, bestowing Gnosis (stdin) upon an
    Action. It masters both the **Indented Soul** (modern) and the **Legacy Scripture**
    (heredoc) with a pantheon of 12 elevations.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "SymphonyCommunionScribe")

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Executes the Gnostic Triage to select the correct path of Communion.
        """

        # [ELEVATION 1: THE DUAL-GAZE ROUTER]
        # Path A: The Indented Communion (Modern, Pythonic)
        if vessel.line_type == GnosticLineType.BLOCK_START and vessel.edict_type == EdictType.ACTION:
            return self._conduct_indented_communion(lines, i, vessel)

        # Path B: The Legacy Communion (Shell-style Heredoc)
        elif vessel.edict_type == EdictType.COMMUNION:
            return self._conduct_legacy_communion(lines, i, vessel)

        # Fallback (Should be architecturally impossible due to Inquisitor)
        return i + 1

    def _conduct_indented_communion(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Conducts the modern rite:
        >> command:
            input 1
            input 2
        """
        line_num = vessel.line_num

        # [ELEVATION 11: THE MAGIC COLON STRIPPER]
        # We strip the trailing colon only from the end, ensuring we don't mangle commands.
        raw_command_line = vessel.raw_scripture.strip()
        if raw_command_line.endswith(':'):
            raw_command_line = raw_command_line[:-1].strip()

        # Remove the '>>' sigil
        raw_command_line = raw_command_line.lstrip('>').strip()

        # Forge the Base Edict
        # [ELEVATION 9: ATOMIC RE-TYPING]
        edict = forge_edict_from_vessel(vessel)
        edict.type = EdictType.ACTION

        # [ELEVATION 2: THE METADATA ALCHEMIST]
        # We parse 'as <var>' and 'using <adj>' from the command header.
        self._parse_action_metadata(raw_command_line, edict)

        # [ELEVATION 3: THE INDENTATION NORMALIZER]
        # Calculate the baseline indentation of the parent line
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Consume the block
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # [ELEVATION 4: THE VOID SENTINEL]
        if not content_lines:
            self.parser.heresies.append(ArtisanHeresy(
                "MUTE_COMMUNION_HERESY: A Communion was proclaimed with ':', but no indented Gnosis followed.",
                line_num=line_num,
                severity=HeresySeverity.WARNING
            ))
            # We still append the edict (as a standard action) to prevent a crash
            self.parser.edicts.append(edict)
            return end_index

        # Process the inputs
        pure_inputs = self._purify_inputs(content_lines)
        edict.inputs = pure_inputs

        # [ELEVATION 8: THE RAW SCRIPTURE PRESERVER]
        # We append the block content to the raw_scripture so the chronicler sees the whole story.
        block_text = "\n".join(content_lines)
        edict.raw_scripture = f"{vessel.raw_scripture}\n{block_text}"

        self.parser.edicts.append(edict)
        self.Logger.verbose(f"   -> Indented Communion complete. {len(pure_inputs)} lines of Gnosis bound.")

        # [ELEVATION 12: THE TIMELINE GUARDIAN]
        return end_index

    def _conduct_legacy_communion(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Conducts the ancient rite:
        >> command
        << EOF
        input
        EOF
        """
        delimiter = vessel.delimiter
        if not delimiter:
            # [ELEVATION 6: THE DELIMITER GUARDIAN]
            self.parser.heresies.append(ArtisanHeresy(
                "MALFORMED_HEREDOC_HERESY: Legacy communion '<<' missing delimiter (e.g. '<< EOF').",
                line_num=vessel.line_num
            ))
            return i + 1

        # [ELEVATION 5: THE ORPHANED SOUL DETECTOR]
        # Legacy Communion must attach to the *previous* action in the timeline.
        if not self.parser.edicts or self.parser.edicts[-1].type != EdictType.ACTION:
            self.parser.heresies.append(ArtisanHeresy(
                "ORPHANED_COMMUNION_HERESY: A '<<' block must immediately follow an Action ('>>').",
                line_num=vessel.line_num
            ))
            # We must still consume the block to prevent parsing chaos downstream
            return self._consume_until_delimiter(lines, i, delimiter)[1]

        # Perform consumption
        inputs, end_index = self._consume_until_delimiter(lines, i, delimiter)

        # Attach Gnosis to the Ancestor
        target_edict = self.parser.edicts[-1]
        target_edict.inputs.extend(inputs)

        # Update Ancestor's Chronicle
        # Note: We append the heredoc to the PREVIOUS edict's raw_scripture for completeness
        heredoc_raw = "\n".join(lines[i:end_index])
        target_edict.raw_scripture += f"\n{heredoc_raw}"

        self.Logger.verbose(f"   -> Legacy Communion attached {len(inputs)} lines to previous Action.")
        return end_index

    def _consume_until_delimiter(self, lines: List[str], start_index: int, delimiter: str) -> Tuple[List[str], int]:
        """
        Consumes lines until the delimiter is found on its own line.
        """
        inputs = []
        j = start_index + 1
        found_end = False

        while j < len(lines):
            line = lines[j].strip()
            # delimiter check is exact match on stripped line
            if line == delimiter:
                found_end = True
                j += 1  # Consume delimiter line
                break

            # For legacy heredocs, we usually preserve the line as-is (minus newline)
            # or strip basic indentation if it looks consistent?
            # Standard heredoc behavior preserves internal indentation.
            # We will strip newline chars.
            inputs.append(lines[j].rstrip('\r\n'))
            j += 1

        if not found_end:
            self.parser.heresies.append(ArtisanHeresy(
                f"UNCLOSED_HEREDOC_HERESY: Expected closing delimiter '{delimiter}'.",
                line_num=start_index + 1
            ))

        return inputs, j

    def _purify_inputs(self, content_lines: List[str]) -> List[str]:
        """
        [ELEVATION 3, 7, 10: THE TRI-FOLD PURIFICATION]
        1. Strips common indentation (dedent).
        2. Trims trailing void lines.
        3. Normalizes line endings.
        """
        if not content_lines:
            return []

        # 1. Dedent logic (manual, to be safe with mixed content)
        # Find the indentation of the first line
        first_line = content_lines[0]
        base_indent_len = len(first_line) - len(first_line.lstrip())

        cleaned_lines = []
        for line in content_lines:
            # Remove base indent
            if len(line) >= base_indent_len:
                line = line[base_indent_len:]

            # [ELEVATION 10: INPUT SANITIZER]
            line = line.rstrip('\r\n')
            cleaned_lines.append(line)

        # [ELEVATION 7: THE TRAILING VOID ANNIHILATOR]
        # Remove empty lines from the END of the block only.
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()

        return cleaned_lines