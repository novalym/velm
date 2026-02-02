# Path: scaffold/parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
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
    == THE ORACLE OF ORCHESTRATION (V-Ω-ETERNAL-APOTHEOSIS)                        ==
    =================================================================================
    @gnosis:title The Oracle of Orchestration (`%% post-run`, `%% on-undo`, etc.)
    @gnosis:summary The divine artisan that perceives, validates, and chronicles the
                     Maestro's Will and its Gnostic inverse.
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

        # We must still check for an on-undo block immediately following
        undo_block, next_i = self._peek_for_undo_block(lines, i + 1)

        self._adjudicate_and_chronicle([(command_str, line_num, undo_block)], vessel)

        return next_i

    def _conduct_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Handles multi-line blocks, now with causal `on-undo` linkage."""
        line_num = vessel.line_num
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Consume the main block of commands
        raw_block_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # [THE FIX] If we detected a block intent but consumed nothing, it's a void block.
        # We must advance the index to prevent the main loop from re-consuming the header.
        if not raw_block_lines:
            self.Logger.warn(f"L{line_num:03d}: The '{vessel.raw_scripture.strip()}' block is a void.")
            # If we didn't consume anything, end_index is i+1.
            # We return this so the parser moves to the next line.
            return end_index

        # Now, check if the VERY NEXT block is an `on-undo` block
        undo_block, final_end_index = self._peek_for_undo_block(lines, end_index)

        dedented_block = dedent("\n".join(raw_block_lines))
        commands_lines = dedented_block.splitlines()

        # The causal link: the undo block applies to ALL commands in the preceding block
        # (This is a simplification; ideally we'd map 1:1, but block-level undo is safer for now)
        commands_with_gnosis: List[Tuple[str, int, Optional[List[str]]]] = []
        for idx, command_str in enumerate(commands_lines):
            clean_cmd = command_str.strip()
            if clean_cmd and not clean_cmd.startswith('#'):
                current_cmd_line = line_num + 1 + idx  # Approximate line number
                commands_with_gnosis.append((clean_cmd, current_cmd_line, undo_block))
                # The undo block is consumed only once by the whole block to avoid duplicate execution on undo
                undo_block = None

        self._adjudicate_and_chronicle(commands_with_gnosis, vessel)

        return final_end_index

    def _peek_for_undo_block(self, lines: List[str], start_index: int) -> Tuple[Optional[List[str]], int]:
        """Looks ahead for an `%% on-undo:` block and consumes it if found."""
        if start_index >= len(lines):
            return None, start_index

        next_i = start_index
        # Skip blank lines
        while next_i < len(lines) and not lines[next_i].strip():
            next_i += 1

        if next_i < len(lines) and lines[next_i].strip().startswith("%% on-undo"):
            parent_indent = self.parser._calculate_original_indent(lines[next_i])
            undo_lines, end_index = self.parser._consume_indented_block_with_context(lines, next_i + 1, parent_indent)
            if undo_lines:
                dedented_undo = dedent("\n".join(undo_lines))
                return dedented_undo.splitlines(), end_index
            # If header exists but no body, consume header line
            return [], next_i + 1

        return None, start_index

    def _adjudicate_and_chronicle(self, commands_with_gnosis: List[Tuple[str, int, Optional[List[str]]]],
                                  vessel: GnosticVessel):
        """
        =================================================================================
        == THE RITE OF GNOSTIC ASSOCIATION (V-Ω-ETERNAL)                               ==
        =================================================================================
        This rite now forges an unbreakable Gnostic link. It inscribes a sacred map
        of line numbers into the AST anchor, ensuring the LogicWeaver's Gaze will be
        one of absolute certainty.
        =================================================================================
        """
        if not commands_with_gnosis:
            return

        self.Logger.verbose(f"   -> Summoning Gnostic Sentinel to adjudicate {len(commands_with_gnosis)} edict(s)...")

        valid_commands = []
        for command, cmd_line_num, undo_cmds in commands_with_gnosis:
            try:
                self.sentry.adjudicate(command, self.parser.base_path, cmd_line_num)
                valid_commands.append((command, cmd_line_num, undo_cmds))
            except GuardianHeresy as e:
                self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=e.get_proclamation())

        if not valid_commands:
            return

        self.parser.post_run_commands.extend(valid_commands)

        # === THE DIVINE HEALING: THE FORGING OF THE SACRED MAP ===
        # We extract the line numbers from the pure, validated commands.
        # This list of integers is the one true Gnostic key.
        command_line_numbers = [cmd_line_num for _, cmd_line_num, _ in valid_commands]

        # We transmute this Gnosis into a JSON scripture.
        import json
        content_payload = json.dumps(command_line_numbers)
        # === THE APOTHEOSIS IS COMPLETE ===

        maestro_item = ScaffoldItem(
            path=Path(vessel.raw_scripture.strip()), is_dir=False,
            content=content_payload, # The content is now a map, not a script.
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=GnosticLineType.POST_RUN
        )
        self.parser.raw_items.append(maestro_item)