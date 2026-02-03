# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_polyglot_scribe.py

import re
from textwrap import dedent
from typing import List, TYPE_CHECKING, Dict, Any, Tuple, Optional

from .symphony_block_scribe import SymphonyBlockScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy
from .....contracts.symphony_contracts import Edict, EdictType

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyPolyglotScribe(SymphonyBlockScribe):
    """
    =================================================================================
    == THE GNOSTIC AMBASSADOR (V-Ω-LEGENDARY. THE POLYGLOT INTERPRETER)            ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    This divine artisan is the bridge between the Symphony and the Foreign Tongues.
    It perceives blocks of code written in alien languages (Python, Node, Bash, Go)
    and transmutes them into a sacred `POLYGLOT_ACTION` Edict.

    It is not merely a copy-paste engine; it is a **Contextual Alchemist**.
    It extracts metadata, dependencies, and configuration from within the script's
    very soul (comments and headers), allowing the Conductor to prepare a perfect,
    sandboxed reality for the foreign rite.

    ### The Pantheon of Faculties:
    1.  **The Header Parser:** Decodes complex parameters like `py(filesystem='read-only', timeout=30):`.
    2.  **The Metadata Miner:** Digs into the script body for Gnostic directives like `# requirements: pandas, requests`.
    3.  **The Import resolver:** Recognizes `# import: ./utils.py` to weave external code into the ephemeral execution context.
    4.  **The Indented Consumer:** Flawlessly consumes indented blocks, preserving their relative structure while stripping the container's indentation.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        # We invoke the name of the base block scribe to register our identity
        super().__init__(parser)

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE GNOSTIC AMBASSADOR (V-Ω-DUAL-TONGUED. THE POLYGLOT TRIAGE)              ==
        =================================================================================
        LIF: 10,000,000,000,000

        This Scribe is a master of Gnostic Triage. It perceives the Architect's will
        and summons the correct internal artisan for either the modern Indented Soul
        or the ancient Delimited Soul.
        """
        # --- I. THE GNOSTIC TRIAGE ---
        raw_header = vessel.raw_scripture.strip()

        # PATH A: The Modern Rite (Indented Soul)
        # Gaze for the colon, which signals an indented block.
        if raw_header.endswith(':'):
            return self._conduct_indented_rite(lines, i, vessel)

        # PATH B: The Ancient Rite (Delimited Soul)
        # Gaze for the '>>' sigil, which signals a delimited block.
        elif '>>' in raw_header:
            return self._conduct_delimited_rite(lines, i, vessel)

        else:
            # A heresy that should be architecturally impossible.
            self.parser.heresies.append(ArtisanHeresy(
                "AMBIGUOUS_POLYGLOT_HERESY: The polyglot scripture is malformed.",
                line_num=vessel.line_num
            ))
            return i + 1

    def _conduct_indented_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Conducts the modern, Pythonic rite: `py:...`"""
        line_num = vessel.line_num
        language = vessel.language

        self.Logger.verbose(f"L{line_num}: Perceiving an Indented Soul for a '{language}' vessel.")

        # --- MOVEMENT I: THE ALCHEMY OF PARAMETERS ---
        params_str = ""
        match = re.match(r'^[a-z]{2,8}(?:\((.*)\))?:?$', vessel.command.strip())
        if match: params_str = match.group(1)

        parameters = self._parse_alchemical_parameters(params_str)
        if parameters: self.Logger.verbose(f"   -> Configuration perceived: {parameters}")

        # --- MOVEMENT II: THE CONSUMPTION OF THE BODY ---
        parent_indent = self.parser._calculate_original_indent(lines[i])
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # --- MOVEMENT III & IV: METADATA & ARGUMENT FORGING ---
        # (This logic is pure and shared, so we delegate to a common artisan)
        pure_script_block, directive_args = self._forge_final_gnosis(content_lines, parameters)

        # --- MOVEMENT V: THE FORGING OF THE EDICT ---
        full_raw_scripture = vessel.raw_scripture + "\n" + "\n".join(content_lines)
        edict = Edict(
            type=EdictType.POLYGLOT_ACTION,
            raw_scripture=full_raw_scripture,
            line_num=line_num,
            language=language,
            script_block=pure_script_block,
            directive_args=directive_args,
            command=vessel.command
        )

        self.parser.edicts.append(edict)
        self.Logger.verbose(f"   -> Polyglot Rite (Indented) recorded. Handing control back at line {end_index}.")

        return end_index

    def _conduct_delimited_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Conducts the ancient, shell-like rite: `py >> ... <<`"""
        line_num = vessel.line_num
        language = vessel.language

        self.Logger.verbose(f"L{line_num}: Perceiving a Delimited Soul for a '{language}' vessel.")

        # --- MOVEMENT I: THE CONSUMPTION OF THE BODY ---
        # The body starts on the next line and ends with '<<'
        content_lines = []
        j = i + 1
        found_end = False
        while j < len(lines):
            line = lines[j]
            if line.strip() == '<<':
                found_end = True
                j += 1  # Consume the '<<' line
                break
            content_lines.append(line)
            j += 1

        end_index = j

        if not found_end:
            raise ArtisanHeresy("UNCLOSED_POLYGLOT_HERESY: Delimited polyglot block was not closed with '<<'.",
                                line_num=line_num)

        # --- MOVEMENT II & III: METADATA & ARGUMENT FORGING ---
        pure_script_block, directive_args = self._forge_final_gnosis(content_lines, {})  # No params in header

        # --- MOVEMENT IV: THE FORGING OF THE EDICT ---
        full_raw_scripture = "\n".join(lines[i:end_index])
        edict = Edict(
            type=EdictType.POLYGLOT_ACTION,
            raw_scripture=full_raw_scripture,
            line_num=line_num,
            language=language,
            script_block=pure_script_block,
            directive_args=directive_args,
            command=vessel.command
        )

        self.parser.edicts.append(edict)
        self.Logger.verbose(f"   -> Polyglot Rite (Delimited) recorded. Handing control back at line {end_index}.")

        return end_index

    def _forge_final_gnosis(self, content_lines: List[str], parameters: Dict[str, Any]) -> Tuple[str, List[str]]:
        """
        [THE PURE ALCHEMIST] A universal helper that forges the final script and args
        from the raw content and header parameters.
        """
        # 1. The Mining of Metadata
        script_block_lines, dependencies, imports, return_type = self._consume_gnostic_metadata(content_lines)

        # 2. The Gnostic Purification (Dedent)
        # We must handle the case of an empty block gracefully
        if not script_block_lines:
            pure_script_block = ""
        else:
            pure_script_block = dedent("\n".join(script_block_lines))

        # 3. The Forging of the Arguments
        directive_args = [f"{k}={v}" for k, v in parameters.items()]
        if dependencies:
            directive_args.append(f"requirements={','.join(dependencies)}")
            self.Logger.verbose(f"   -> Dependencies mined: {dependencies}")
        if imports:
            directive_args.append(f"imports={','.join(imports)}")
            self.Logger.verbose(f"   -> Imports requested: {imports}")
        if return_type:
            directive_args.append(f"return={return_type}")

        return pure_script_block, directive_args

    def _parse_alchemical_parameters(self, params_str: Optional[str]) -> Dict[str, Any]:
        """
        [THE ALCHEMIST'S GAZE]
        A divine, sentient artisan for parsing key-value Gnosis from a parameter string.
        It handles:
        - Unquoted values: key=value
        - Quoted values: key="value with spaces"
        - Booleans: key=true (Case insensitive)
        - Integers: key=123
        """
        parameters: Dict[str, Any] = {}
        if not params_str: return parameters

        # The Regex of Extraction:
        # \s*(\w+)      -> Capture the Key (alphanumeric)
        # \s*=\s*       -> The Equals bridge
        # ( ... )       -> Capture the Value group
        # " ... "       -> Double quoted string (handling escaped quotes)
        # ' ... '       -> Single quoted string
        # \d+           -> Integers
        # true|false    -> Booleans
        # [\w.-]+       -> Simple strings (filenames, identifiers)
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

            # The Rite of Type Transmutation
            if value.lower() == 'true':
                parameters[key] = True
            elif value.lower() == 'false':
                parameters[key] = False
            elif value.isdigit():
                parameters[key] = int(value)
            elif (value.startswith("'") and value.endswith("'")) or \
                    (value.startswith('"') and value.endswith('"')):
                parameters[key] = value[1:-1]  # Unbox the string
            else:
                parameters[key] = value  # Raw string

        return parameters

    def _consume_gnostic_metadata(self, lines: List[str]) -> Tuple[List[str], List[str], List[str], Optional[str]]:
        """
        [THE SCRIBE OF THE INDENTED SOUL]
        Scans the raw lines of the block. If a line is a special Gnostic Comment,
        it extracts the metadata and removes the line from the final script.

        Supported Directives:
        - # requirements: package1, package2
        - # packages: package1 (alias for requirements)
        - # import: ./local/file.py
        - # return: json (Hints to the conductor how to parse stdout)
        """
        script_lines = []
        dependencies: List[str] = []
        imports: List[str] = []
        return_type: Optional[str] = None

        for line in lines:
            stripped = line.strip()

            # Dependency Injection
            if stripped.startswith(('# requirements:', '# packages:')):
                # Extract everything after the colon, split by comma
                try:
                    deps_str = stripped.split(':', 1)[1]
                    found_deps = [p.strip() for p in deps_str.split(',') if p.strip()]
                    dependencies.extend(found_deps)
                except IndexError:
                    pass # Malformed requirement line, ignore
                # We do NOT add this line to script_lines; it is consumed.

            # File Injections
            elif stripped.startswith('# import:'):
                try:
                    import_path = stripped.split(':', 1)[1].strip()
                    if import_path:
                        imports.append(import_path)
                except IndexError:
                    pass
                # Consumed.

            # Output Type Hinting
            elif stripped.startswith('# return:'):
                try:
                    return_type = stripped.split(':', 1)[1].strip()
                except IndexError:
                    pass
                # Consumed.

            else:
                # It is pure code. Preserve it.
                script_lines.append(line)

        return script_lines, dependencies, imports, return_type