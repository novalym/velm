# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
# ------------------------------------------------------------------------------------

import re
from pathlib import Path
from textwrap import dedent
from typing import List, Tuple, TYPE_CHECKING, Optional

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....core.guardian import GnosticSentry
from .....contracts.heresy_contracts import GuardianHeresy, ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import EdictType

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser


class PostRunScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF ORCHESTRATION (V-Ω-QUATERNITY-ENFORCED)                       ==
    =================================================================================
    LIF: 10,000,000,000
    AUTH: Ω_POSTRUN_QUATERNITY_FIX

    The divine artisan that perceives, validates, and chronicles the Maestro's Will.
    It is the SOURCE of the Post-Run Commands list.

    [THE LEGENDARY ASCENSION]:
    This Scribe now enforces the Law of the Quaternity. Every command it inscribes
    into the `parser.post_run_commands` list is guaranteed to be a 4-tuple:
    `(command, line_num, undo_commands_list_or_none, heresy_commands_list_or_none)`.

    This enables the Engine to distinguish between Reversal (Undo) and Redemption (Heresy).
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "PostRunScribe")
        self.sentry = GnosticSentry()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """The Grand Symphony of Orchestrational Perception."""
        line_num = vessel.line_num
        self.Logger.verbose(
            f"L{line_num:03d}: The Oracle of Orchestration awakens for '{vessel.raw_scripture.strip()}'...")

        try:
            # --- MOVEMENT I: THE GNOSTIC TRIAGE ---
            # A block is signified by a trailing colon OR if the next line is indented.
            parent_indent = self.parser._calculate_original_indent(lines[i])
            stripped_header = lines[i].strip()
            is_explicit_block = stripped_header.endswith(':')

            is_implicit_block = False
            # Peek ahead to see if the next non-empty line is indented
            if (i + 1) < len(lines):
                next_line_idx = i + 1
                while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                    next_line_idx += 1

                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx]
                    next_indent = self.parser._calculate_original_indent(next_line)
                    if next_indent > parent_indent:
                        is_implicit_block = True

            if is_explicit_block or is_implicit_block:
                return self._conduct_block_rite(lines, i, vessel)
            else:
                return self._conduct_single_rite(lines, i, vessel)

        except Exception as e:
            self.parser._proclaim_heresy(
                "META_HERESY_POSTRUN_SCRIBE_FRACTURED", vessel,
                details=f"A catastrophic paradox occurred in the Oracle of Orchestration: {e}",
                exception_obj=e
            )
            return i + 1

    def _conduct_single_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Handles a single-line command like `%% git init`."""
        line_num = vessel.line_num
        # Strip `%%` and the directive name (e.g., `post-run`) to get the command
        parts = vessel.raw_scripture.strip().split(None, 2)
        if len(parts) < 3:
            # Case: `%% post-run` with no command and no block -> Empty/Void
            return i + 1

        command_str = parts[2]  # %% post-run <command>

        # We must peek for BOTH undo and heresy blocks
        # The order might vary, so we check sequentially and update the index

        # Check 1
        undo_block, next_i = self._peek_for_sub_block(lines, i + 1, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        # Check 2 (If order was flipped or first check missed)
        if not undo_block:
            # Try getting heresy first
            heresy_block_alt, next_i_alt = self._peek_for_sub_block(lines, i + 1, "on-heresy")
            if heresy_block_alt:
                heresy_block = heresy_block_alt
                # Then check for undo after heresy
                undo_block, final_i = self._peek_for_sub_block(lines, next_i_alt, "on-undo")
            else:
                # Neither found in alt check, stick with first check results (both None)
                pass

        # Pass as a list of 4-tuples
        self._adjudicate_and_chronicle([(command_str, line_num, undo_block, heresy_block)], vessel)

        return final_i

    def _conduct_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Handles multi-line blocks, now with causal `on-undo` and `on-heresy` linkage."""
        line_num = vessel.line_num
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Consume the main block of commands
        raw_block_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        if not raw_block_lines:
            self.Logger.warn(f"L{line_num:03d}: The '{vessel.raw_scripture.strip()}' block is a void.")
            return end_index

        # Peek for attached blocks
        undo_block, next_i = self._peek_for_sub_block(lines, end_index, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        # Flip check
        if not undo_block:
            heresy_block_alt, next_i_alt = self._peek_for_sub_block(lines, end_index, "on-heresy")
            if heresy_block_alt:
                heresy_block = heresy_block_alt
                undo_block, final_i = self._peek_for_sub_block(lines, next_i_alt, "on-undo")

        dedented_block = dedent("\n".join(raw_block_lines))
        commands_lines = dedented_block.splitlines()

        # The causal link: the undo/heresy blocks apply to ALL commands in the preceding block
        # (Though kinetically, heresy usually handles the failure of the block as a unit)
        commands_with_gnosis: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        for idx, command_str in enumerate(commands_lines):
            clean_cmd = command_str.strip()
            if clean_cmd and not clean_cmd.startswith('#'):
                current_cmd_line = line_num + 1 + idx  # Approximate line number
                # [THE FIX]: Forge the 4-Tuple here
                commands_with_gnosis.append((clean_cmd, current_cmd_line, undo_block, heresy_block))

                # OPTIMIZATION: We attach the blocks to every command.
                # The QuantumCPU will execute them if *that specific command* fails.
                # For a block, if the first fails, its heresy block runs. The rest are skipped.
                # This is correct behavior.

        self._adjudicate_and_chronicle(commands_with_gnosis, vessel)

        return final_i

    def _peek_for_sub_block(self, lines: List[str], start_index: int, key: str) -> Tuple[Optional[List[str]], int]:
        """Looks ahead for a specific block (on-undo, on-heresy) and consumes it if found."""
        if start_index >= len(lines):
            return None, start_index

        next_i = start_index
        # Skip blank lines and comments to find the next directive
        while next_i < len(lines):
            line = lines[next_i].strip()
            if not line or line.startswith(('#', '//')):
                next_i += 1
                continue
            break

        if next_i >= len(lines):
            return None, start_index

        if lines[next_i].strip().startswith(f"%% {key}"):
            parent_indent = self.parser._calculate_original_indent(lines[next_i])
            sub_lines, end_index = self.parser._consume_indented_block_with_context(lines, next_i + 1, parent_indent)

            # If sub_lines exist, dedent and return.
            # If not, it might be a single line directive (though less common for these blocks).
            # We assume indented block for now.
            if sub_lines:
                dedented = dedent("\n".join(sub_lines))
                return dedented.splitlines(), end_index

            # If header exists but no body, consume header line
            return [], next_i + 1

        return None, start_index  # Return original start_index (before skipping blanks) or next_i?
        # We should return the index where we STOPPED looking.
        # Actually, if we didn't find the block, we should return the index BEFORE we skipped blanks/comments
        # so the main loop can consume them or the next scribe can see them?
        # NO. The main loop calls this. If we return start_index, the main loop continues from there.
        return None, start_index

    def _adjudicate_and_chronicle(self,
                                  commands_with_gnosis: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
                                  vessel: GnosticVessel):
        """
        =================================================================================
        == THE RITE OF GNOSTIC ASSOCIATION (V-Ω-QUATERNITY-ENFORCED)                   ==
        =================================================================================
        [THE CURE]: This method guarantees that what enters `self.parser.post_run_commands`
        is strictly a list of 4-Tuples: (command, line_num, undo_stack, heresy_stack).
        """
        if not commands_with_gnosis:
            return

        self.Logger.verbose(f"   -> Adjudicating {len(commands_with_gnosis)} edict(s)...")

        valid_commands = []
        for command, cmd_line_num, undo_cmds, heresy_cmds in commands_with_gnosis:
            try:
                # [ASCENSION 1]: SIGIL DECAPITATION
                # We strip leading '>>' or '>' so the Maestro receives pure kinetic matter.
                clean_command = re.sub(r'^>+\s*', '', command)

                self.sentry.adjudicate(clean_command, self.parser.base_path, cmd_line_num)

                # [ASCENSION 2]: THE QUATERNITY SEAL
                final_undo = undo_cmds if undo_cmds else None
                final_heresy = heresy_cmds if heresy_cmds else None

                # Append the Sacred Quaternity
                valid_commands.append((clean_command, cmd_line_num, final_undo, final_heresy))

            except GuardianHeresy as e:
                self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=e.get_proclamation())

        if not valid_commands:
            return

        # Commit to the parser's master edict stream
        self.parser.post_run_commands.extend(valid_commands)

        # Inscribe the Gnostic Map for the LogicWeaver (Line Number Reference)
        import json
        # We only store line numbers in the content payload for mapping
        command_line_numbers = [cmd_line_num for _, cmd_line_num, _, _ in valid_commands]
        content_payload = json.dumps(command_line_numbers)

        maestro_item = ScaffoldItem(
            path=Path(vessel.raw_scripture.strip()), is_dir=False,
            content=content_payload,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=GnosticLineType.POST_RUN
        )
        self.parser.raw_items.append(maestro_item)