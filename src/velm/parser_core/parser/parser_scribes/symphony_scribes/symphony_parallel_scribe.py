# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_parallel_scribe.py

import re
from typing import List, TYPE_CHECKING, Dict, Any, Optional

from .symphony_block_scribe import SymphonyBlockScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import Edict, EdictType

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyParallelScribe(SymphonyBlockScribe):
    """
    =================================================================================
    == THE WEAVER OF SPACETIME (V-Ω-LEGENDARY. THE CONCURRENT ARTISAN)             ==
    =================================================================================
    LIF: 10,000,000,000,000

    This artisan handles `parallel:` and `&&:` blocks. It parses the block body
    recursively but enforces strict Gnostic Laws to ensure concurrent safety.

    It forbids Vows (non-deterministic) and State Changes (race conditions) within
    the parallel reality.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser)  # Registers as "SymphonyParallelScribe" via base magic or manual override if needed

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        Conducts the Rite of Parallelism (V-Ω-TUPLE-CORRECTED).
        """
        line_num = vessel.line_num
        raw_header = vessel.raw_scripture.strip()

        # [ELEVATION 1 & 2: PARAMETER ALCHEMIST & SYNTAX UNIFIER]
        # We extract parameters from "parallel(workers=2):" or "&&:"
        # vessel.command holds the stripped line content (e.g. "parallel(workers=2)")
        params_str = ""
        match = re.match(r'^(?:parallel|&&|multiverse)(?:\((.*)\))?:?$', vessel.command)
        if match:
            params_str = match.group(1)

        parameters = self._parse_alchemical_parameters(params_str)
        if parameters:
            self.Logger.verbose(f"L{line_num}: Parallel configuration perceived: {parameters}")

        # [ELEVATION 9: THE INDENTATION NORMALIZER]
        # Consume the body using the base scribe's logic
        block_content, end_index = self._consume_block(lines, i)

        # [ELEVATION 3 & 8: EMPTY MULTIVERSE SENTINEL & COMMENT FILTER]
        if not block_content.strip():
            # We check if it was truly empty or just comments.
            # Since _consume_block returns raw text, we can't easily tell without parsing.
            pass

        # [ELEVATION 4: THE RECURSIVE MIND]
        # Summon a new parser to interpret the threads
        sub_parser = self.parser.__class__(grammar_key='symphony')

        # We parse the block content to get the sub-edicts (threads)
        # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
        # (parser, items, commands, edicts, vars, dossier)
        _, _, _, sub_edicts, _, _ = sub_parser.parse_string(
            block_content,
            self.parser.file_path,
            line_offset=line_num
        )

        if not sub_edicts:
            self.parser.heresies.append(ArtisanHeresy(
                "EMPTY_MULTIVERSE_HERESY: A parallel block must contain at least one thread of execution.",
                line_num=line_num,
                severity=HeresySeverity.WARNING
            ))

        # --- THE GNOSTIC INQUISITION OF THREADS ---
        for sub_edict in sub_edicts:
            # [ELEVATION 5: THE VOW SENTINEL]
            if sub_edict.type == EdictType.VOW:
                self.parser.heresies.append(ArtisanHeresy(
                    "VOW_IN_PARALLEL_HERESY: Vows (`??`) cannot be made inside a parallel block due to non-deterministic completion order.",
                    line_num=sub_edict.line_num
                ))

            # [ELEVATION 6: THE STATE GUARDIAN]
            elif sub_edict.type == EdictType.STATE:
                self.parser.heresies.append(ArtisanHeresy(
                    "STATE_IN_PARALLEL_HERESY: State changes (`%%`) are forbidden in parallel blocks to prevent race conditions.",
                    line_num=sub_edict.line_num
                ))

            # [ELEVATION 7: THE NESTED PARADOX WARD]
            elif sub_edict.type == EdictType.PARALLEL_RITE:
                self.parser.heresies.append(ArtisanHeresy(
                    "NESTED_MULTIVERSE_HERESY: Nested parallel blocks are forbidden to preserve sanity.",
                    line_num=sub_edict.line_num
                ))

        # [ELEVATION 10: THE RAW SCRIPTURE WEAVER]
        full_raw_scripture = f"{vessel.raw_scripture}\n{block_content}"

        # [ELEVATION 11: THE ARGUMENT PACKER]
        directive_args = [f"{k}={v}" for k, v in parameters.items()]

        # Forge the Edict
        edict = Edict(
            type=EdictType.PARALLEL_RITE,
            raw_scripture=full_raw_scripture,
            line_num=line_num,
            parallel_edicts=sub_edicts,
            directive_args=directive_args
        )

        self.parser.edicts.append(edict)

        # [ELEVATION 12: THE ATOMIC RETURN]
        return end_index

    def _parse_alchemical_parameters(self, params_str: Optional[str]) -> Dict[str, Any]:
        """
        [THE ALCHEMIST'S GAZE]
        Parses key=value parameters from the header string.
        """
        parameters: Dict[str, Any] = {}
        if not params_str: return parameters

        # Reusing the robust regex from Polyglot Scribe for consistency
        param_regex = re.compile(r"""
            \s* (\w+) \s* = \s* (
                " (?: \\. | [^"\\] )* " |
                ' (?: \\. | [^'\\] )* ' |
                \d+ |
                (?i:true|false) |
                [\w.-]+
            ) \s*
        """, re.VERBOSE)

        for match in param_regex.finditer(params_str):
            key, value = match.groups()
            if value.lower() == 'true':
                parameters[key] = True
            elif value.lower() == 'false':
                parameters[key] = False
            elif value.isdigit():
                parameters[key] = int(value)
            elif (value.startswith("'") and value.endswith("'")) or \
                    (value.startswith('"') and value.endswith('"')):
                parameters[key] = value[1:-1]
            else:
                parameters[key] = value
        return parameters