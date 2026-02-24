# Path: parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
# ---------------------------------------------------------------------------


import re
import json
from pathlib import Path
from textwrap import dedent
from typing import List, Tuple, TYPE_CHECKING, Optional, Set, Final

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....core.guardian import GnosticSentry
from .....contracts.heresy_contracts import GuardianHeresy, ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import EdictType
from .....logger import Scribe

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser

Logger = Scribe("PostRunScribe")


class PostRunScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF THE MAESTRO'S WILL: APOTHEOSIS (V-Ω-TOTALITY-V5000-JINJA-PURE) ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_INTENT_PURIFIER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_POST_RUN_V5000_LOGIC_FILTER_FINALIS

    The Supreme Conductor of Kinetic Intent. It perceives 'Foreign Tongues' (Python/JS)
    directly within the post-run symphony, transmutes `@if` logic into pure Jinja2,
    and assigns **Virtual Line IDs** to prevent the "Dictionary Collision Heresy."

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **Virtual Chronometry (THE CURE):** Assigns a unique synthetic ID (`Line * 10000 + Index`)
        to every command in a block, preventing Dictionary Overwrites in the LogicWeaver.
    2.  **Jinja Logic Transmutation:** Converts `@if` logic into `{% if %}` templates and
        renders them immediately.
    3.  **Strict Logic Filtering (THE FIX):** Uses `JINJA_CONTROL_PATTERN` to aggressively
        ignore any lines that resemble Jinja control flow (`{% ... %}`) after rendering,
        preventing dead branches (like `@else -> proclaim heresy`) from leaking into the queue.
    4.  **Polyglot Block Fission:** Detects `py:` or `js:` headers and fuses the entire
        indented body into a single `POLYGLOT_ACTION` edict.
    5.  **Universal Sigil Exorcism:** Recursively strips `->`, `>>`, and `!!` prefixes,
        ensuring only the pure executable matter reaches the shell.
    6.  **Causal Lookahead:** Peeks into the future to bind `%% on-undo` and `%% on-heresy`
        blocks to their parent kinetic edicts.
    7.  **Structural Heresy Ward:** Detects if `@if` is used incorrectly outside of
        Jinja blocks and issues Socratic guidance.
    8.  **Implicit Proclamation:** Maps `echo ` to the high-status `proclaim:` logic.
    9.  **Navigation Alchemy:** Maps `cd ` to `sanctum:` state changes.
    10. **Metadata Peeling:** Extracts `as <var>` and `retry()` modifiers from commands.
    11. **Gnostic Anchoring:** Forges `ScaffoldItem` anchors for every edict, allowing
        the AST Weaver to place kinetic actions correctly in the timeline.
    12. **The Finality Vow:** A mathematical guarantee that every willed command is
        uniquely identified and sequentially preserved.
    =================================================================================
    """

    # [FACULTY 1]: THE ALCHEMICAL SIEVE PATTERNS
    JINJA_CONTROL_PATTERN: Final[re.Pattern] = re.compile(r'^\s*\{%')
    STRUCTURAL_LOGIC_PATTERN: Final[re.Pattern] = re.compile(r'^\s*@')

    # [ASCENSION 3]: THE POLYGLOT HEADER PHALANX
    # Recognizes the transition from Shell matter to Language soul.
    POLYGLOT_HEADER_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*(?P<lang>py|python|js|node|rs|rust|sh|bash|go):\s*$'
    )

    def __init__(self, parser: 'ApotheosisParser'):
        """The Rite of Inception."""
        super().__init__(parser, "PostRunScribe")
        self.sentry = GnosticSentry()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF CONDUCT (V-Ω-TOTALITY-V5000)                      ==
        =============================================================================
        The entry point for kinetic perception. Adjudicates block vs single-line rites.
        """
        line_num = vessel.line_num
        self.Logger.verbose(f"L{line_num:03d}: The Oracle of Orchestration awakens.")

        try:
            # --- MOVEMENT I: THE TOPOGRAPHICAL TRIAGE ---
            parent_indent = self.parser._calculate_original_indent(lines[i])
            header = lines[i].strip()

            # Adjudicate block nature: Explicit (:) or Implicit (Indented Child)
            is_explicit = header.endswith(':')
            is_implicit = False

            if not is_explicit and (i + 1) < len(lines):
                # Gaze into the future to perceive the "Indentation Shift"
                for next_idx in range(i + 1, len(lines)):
                    next_line = lines[next_idx]
                    if not next_line.strip() or next_line.strip().startswith('#'):
                        continue
                    if self.parser._calculate_original_indent(next_line) > parent_indent:
                        is_implicit = True
                    break

            if is_explicit or is_implicit:
                return self._conduct_block_rite(lines, i, vessel)
            else:
                return self._conduct_single_rite(lines, i, vessel)

        except Exception as e:
            self.parser._proclaim_heresy(
                "META_HERESY_POSTRUN_SCRIBE_FRACTURED",
                vessel,
                details=f"The Orchestrator's mind shattered on line {line_num}: {e}",
                exception_obj=e
            )
            return i + 1

    def _conduct_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE RITE OF THE BICAMERAL WILL (V-Ω-TOTALITY-V5000-VIRTUAL-TIME)        ==
        =============================================================================
        Consumes an orchestration block. It transmutes `@if` logic into pure Jinja2,
        evaluates the block against the current Gnostic Truth, and then safely
        extracts the resonant shell commands.

        [THE CURE]: It assigns a unique **Virtual Line ID** to every command to
        prevent dictionary collisions in the LogicWeaver's memory map.
        """
        line_num = vessel.line_num
        parent_indent = self.parser._calculate_original_indent(lines[i])

        commands_with_gnosis: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        # --- MOVEMENT II: THE CONSUMPTION OF THE RAW BLOCK ---
        content_lines, current_idx = self.parser._consume_indented_block_with_context(
            lines, i + 1, parent_indent
        )

        # --- MOVEMENT III: CAUSAL LOOKAHEAD (ON-UNDO/ON-HERESY) ---
        undo_block, next_i = self._peek_for_sub_block(lines, current_idx, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        if not content_lines:
            return final_i

        # --- MOVEMENT IV: JINJA TRANSMUTATION (THE CURE FOR @IF) ---
        jinja_lines = []
        for line in content_lines:
            stripped = line.strip()
            indent = line[:len(line) - len(line.lstrip())]

            if stripped.startswith('@if '):
                cond = stripped[4:].replace('{{', '').replace('}}', '').strip()
                jinja_lines.append(f"{indent}{{% if {cond} %}}")
            elif stripped.startswith('@elif '):
                cond = stripped[6:].replace('{{', '').replace('}}', '').strip()
                jinja_lines.append(f"{indent}{{% elif {cond} %}}")
            elif stripped == '@else':
                jinja_lines.append(f"{indent}{{% else %}}")
            elif stripped == '@endif':
                jinja_lines.append(f"{indent}{{% endif %}}")
            else:
                jinja_lines.append(line)

        raw_block = "\n".join(jinja_lines)

        # Resolve the conditions immediately using the Alchemist
        try:
            rendered_block = self.parser.alchemist.transmute(raw_block, self.parser.variables)
        except Exception as e:
            self.Logger.warn(f"L{line_num}: Alchemical fracture in post-run block: {e}")
            rendered_block = raw_block

        # --- MOVEMENT V: THE BICAMERAL SCAN ---
        rendered_lines = rendered_block.splitlines()

        r_idx = 0
        command_sequence = 0  # [ASCENSION 1]: Virtual Clock

        while r_idx < len(rendered_lines):
            line = rendered_lines[r_idx]
            stripped = line.strip()

            # [THE FIX]: AGGRESSIVE CONTROL FLOW SIEVE
            # We skip lines that are empty, comments, OR look like Jinja control flow remnants.
            # This ensures that an @else block which Jinja rendered as empty space or
            # partial tags is not interpreted as a command.
            if not stripped or stripped.startswith('#') or self.JINJA_CONTROL_PATTERN.match(stripped):
                r_idx += 1
                continue

            # [ASCENSION 1]: FORGE VIRTUAL TIME
            # We shift the line number by 10,000 for each command in the block.
            # This ensures uniqueness in the LogicWeaver's Dict map.
            virtual_line_num = (line_num * 10000) + command_sequence
            command_sequence += 1

            # Phase A: Polyglot Block Detection
            poly_match = self.POLYGLOT_HEADER_PATTERN.match(line)
            if poly_match:
                lang = poly_match.group('lang')
                poly_indent = self.parser._calculate_original_indent(line)

                # Consume lines that are indented further
                poly_body = []
                r_idx += 1
                while r_idx < len(rendered_lines):
                    p_line = rendered_lines[r_idx]
                    if not p_line.strip():
                        poly_body.append(p_line)
                        r_idx += 1
                        continue
                    if self.parser._calculate_original_indent(p_line) <= poly_indent:
                        break
                    poly_body.append(p_line)
                    r_idx += 1

                full_poly_script = f"{lang}:\n" + "\n".join(poly_body)
                commands_with_gnosis.append((full_poly_script, virtual_line_num, None, None))
                continue

            # Phase B: Standard Kinetic Scan
            # Because we already resolved @if to Jinja and rendered it, any remaining
            # structural logic (@for) is a strict heresy here.
            if not self.STRUCTURAL_LOGIC_PATTERN.match(stripped):
                commands_with_gnosis.append((stripped, virtual_line_num, None, None))
            else:
                self._report_structural_heresy(stripped, line_num)

            r_idx += 1

        # Conduct Adjudication and final Ledger Inscription
        self._adjudicate_and_chronicle(commands_with_gnosis, vessel, undo_block, heresy_block)

        return final_i

    def _conduct_single_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE SUPREME ATOMIC CONDUCTOR (V-Ω-TOTALITY-V500.5-SIGIL-PURE)           ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ATOMIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONDUCT_SINGLE_RITE_V500_SIGIL_EXORCISM_FINALIS
        """
        line_num = vessel.line_num
        raw_scripture = vessel.raw_scripture.strip()

        # --- MOVEMENT I: THE ATOMIC EXTRACTION ---
        parts = raw_scripture.split(None, 2)
        if len(parts) < 3:
            return i + 1

        # The raw, unpurified command body
        potential_intent = parts[2].strip()

        # [THE CURE]: THE SIGIL EXORCISM
        command_str = potential_intent.strip()
        command_str = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', command_str).strip()

        # --- MOVEMENT II: THE JINJA CONTROL GUARD ---
        if self.JINJA_CONTROL_PATTERN.match(command_str):
            self.Logger.verbose(f"L{line_num}: Pure logic perceived. Deferring to Alchemist.")
            return i + 1

        # --- MOVEMENT III: THE VOID GUARD ---
        if not command_str:
            self.parser._proclaim_heresy(
                "VOID_ACTION_HERESY",
                vessel,
                details="The kinetic edict contains sigils but no executable matter.",
                severity=HeresySeverity.WARNING
            )
            return i + 1

        # --- MOVEMENT IV: METADATA WEAVING ---
        from .....utils.core_utils import forge_edict_from_vessel
        temp_edict = forge_edict_from_vessel(vessel)
        final_command_body = self._parse_command_metadata_and_capture(command_str, temp_edict)

        # --- MOVEMENT V: CAUSAL PEEKING ---
        undo_block, next_i = self._peek_for_sub_block(lines, i + 1, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        # --- MOVEMENT VI: CHRONICLE ---
        self._adjudicate_and_chronicle(
            [(final_command_body, line_num, undo_block, heresy_block)],
            vessel
        )

        return final_i

    def _adjudicate_and_chronicle(
            self,
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
            vessel: GnosticVessel,
            undo_block: Optional[List[str]] = None,
            heresy_block: Optional[List[str]] = None
    ):
        """
        =============================================================================
        == THE RITE OF GNOSTIC ASSOCIATION (V-Ω-TOTALITY)                         ==
        =============================================================================
        Validates kinetic matter and weaves the Final Ledger.
        """
        if not commands:
            return

        valid_commands = []
        for cmd_str, line, _, _ in commands:
            first_line = cmd_str.split('\n', 1)[0].strip()

            if self.POLYGLOT_HEADER_PATTERN.match(first_line):
                valid_commands.append((cmd_str, line, undo_block, heresy_block))
                continue

            try:
                # Clean leading sigils (again, robustly, to handle array items)
                clean_intent = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', cmd_str).strip()

                self.sentry.adjudicate(clean_intent, self.parser.base_path, line)
                valid_commands.append((clean_intent, line, undo_block, heresy_block))

            except GuardianHeresy as e:
                self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=e.get_proclamation())

        if not valid_commands:
            return

        # 1. COMMIT TO MASTER EDICT STREAM
        self.parser.post_run_commands.extend(valid_commands)

        # 2. FORGE GNOSTIC ANCHORS (ASCENSION 6)
        # We record the VIRTUAL line numbers in the JSON payload.
        # The AST Weaver will use these unique IDs to retrieve the commands later.
        import json
        anchor_payload = json.dumps([c[1] for c in valid_commands])

        maestro_item = ScaffoldItem(
            path=Path(vessel.raw_scripture.strip()),
            is_dir=False,
            content=anchor_payload,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=GnosticLineType.POST_RUN
        )
        self.parser.raw_items.append(maestro_item)

        self.Logger.verbose(f"   -> Enshrined {len(valid_commands)} edict(s) in the Gnostic Ledger.")

    def _peek_for_sub_block(self, lines: List[str], start_index: int, key: str) -> Tuple[Optional[List[str]], int]:
        """[FACULTY 4]: THE CAUSAL PROBE peeking for associated blocks."""
        if start_index >= len(lines):
            return None, start_index

        next_i = start_index
        while next_i < len(lines):
            line = lines[next_i].strip()
            if not line or line.startswith(('#', '//')):
                next_i += 1
                continue
            break

        if next_i >= len(lines):
            return None, start_index

        if lines[next_i].strip().startswith(f"%% {key}"):
            p_indent = self.parser._calculate_original_indent(lines[next_i])
            sub_lines, end_index = self.parser._consume_indented_block_with_context(
                lines, next_i + 1, p_indent
            )
            if sub_lines:
                return [l.strip() for l in sub_lines if l.strip()], end_index
            return [], next_i + 1

        return None, start_index

    def _report_structural_heresy(self, clean_line: str, line_num: int):
        """[FACULTY 7]: SOCRATIC SUGGESTION FOR STRUCTURAL LEAKS."""
        self.parser._proclaim_heresy(
            "SYNTAX_HERESY_LOGIC_IN_KINETIC_BLOCK",
            ScaffoldItem(path=Path("LOGIC_LEAK"), line_num=line_num, raw_scripture=clean_line, is_dir=False),
            details="Structural directives (@if, @for) are forbidden in kinetic blocks.",
            suggestion="Use Jinja2 logic ({% if ... %}) for conditional edicts.",
            severity=HeresySeverity.CRITICAL
        )

    def __repr__(self) -> str:
        return "<Ω_POST_RUN_SCRIBE status=VIGILANT version=5000.0-JINJA-PURE>"