# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
# ------------------------------------------------------------------------------------
# =========================================================================================
# == THE ORACLE OF ORCHESTRATION: TOTALITY (V-Ω-TOTALITY-V350.0-POLYGLOT-SUTURE)         ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_WILL_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_POSTRUN_V350_POLYGLOT_SUTURE_2026_FINALIS
# =========================================================================================

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
    == THE SCRIBE OF THE MAESTRO'S WILL: APOTHEOSIS                                ==
    =================================================================================
    The Supreme Conductor of Kinetic Intent. It has been Ascended to perceive
    'Foreign Tongues' (Python/JS) directly within the post-run symphony,
    annihilating the barrier between Shell and Logic.
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
        == THE GRAND SYMPHONY OF CONDUCT (V-Ω-TOTALITY-V3.5)                      ==
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
        == THE RITE OF THE BICAMERAL WILL (V-Ω-TOTALITY-V3.5)                     ==
        =============================================================================
        Consumes an orchestration block. It walks the block line-by-line, triggering
        'Sub-Block Fission' whenever a polyglot header is perceived.
        """
        line_num = vessel.line_num
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # This will hold our final quaternity set: (Cmd, Line, Undo, Heresy)
        commands_with_gnosis: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]] = []

        # --- MOVEMENT II: THE BICAMERAL SCAN ---
        current_idx = i + 1
        while current_idx < len(lines):
            line = lines[current_idx]
            stripped = line.strip()

            # Skip the Void and the Whispers
            if not stripped:
                current_idx += 1
                continue

            # [FACULTY 12]: THE BOUNDARY SENTINEL
            # If we hit a dedent (relative to the %% post-run header), the symphony ends.
            indent = self.parser._calculate_original_indent(line)
            if indent <= parent_indent and not stripped.startswith('#'):
                break

                # --- PHASE A: POLYGLOT BLOCK DETECTION (ASCENSION 1) ---
            poly_match = self.POLYGLOT_HEADER_PATTERN.match(line)
            if poly_match:
                # [ASCENSION 2]: ACHRONAL BLOCK FISSION
                lang = poly_match.group('lang')
                self.Logger.verbose(f"L{current_idx + 1:03d}: Polyglot Gaze detected [{lang}].")

                # We use the Parser's context to consume the indented code block
                # parent_indent is the indent of the 'py:' line
                poly_lines, next_idx = self.parser._consume_indented_block_with_context(
                    lines, current_idx + 1, indent
                )

                # We forge the "Fused Command": The lang tag followed by the code
                # The MaestroConductor will see "py:" at the start and know to interpret.
                full_poly_script = f"{lang}:\n" + "\n".join(poly_lines)

                # Inscribe the Quaternity
                commands_with_gnosis.append((full_poly_script, current_idx + 1, None, None))

                # Advance the cursor past the consumed block
                current_idx = next_idx
                continue

            # --- PHASE B: STANDARD KINETIC SCAN ---
            # If not a polyglot header, treat as a standard shell edict or filter.
            if not stripped.startswith('#') and not self.JINJA_CONTROL_PATTERN.match(stripped):
                if not self.STRUCTURAL_LOGIC_PATTERN.match(stripped):
                    commands_with_gnosis.append((stripped, current_idx + 1, None, None))
                else:
                    # Report structural leakage (e.g. @if inside post-run)
                    self._report_structural_heresy(stripped, current_idx + 1)

            current_idx += 1

        # --- MOVEMENT III: CAUSAL LOOKAHEAD (ON-UNDO/ON-HERESY) ---
        # [ASCENSION 9]: Bind redemption to the ENTIRE block of edicts.
        undo_block, next_i = self._peek_for_sub_block(lines, current_idx, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        # Conduct Adjudication and final Ledger Inscription
        self._adjudicate_and_chronicle(commands_with_gnosis, vessel, undo_block, heresy_block)

        return final_i

    def _conduct_single_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Handles single-line edicts: %% post-run <matter>."""
        parts = vessel.raw_scripture.strip().split(None, 2)
        if len(parts) < 3:
            return i + 1

        command_str = parts[2]
        if self.JINJA_CONTROL_PATTERN.match(command_str):
            return i + 1

        undo_block, next_i = self._peek_for_sub_block(lines, i + 1, "on-undo")
        heresy_block, final_i = self._peek_for_sub_block(lines, next_i, "on-heresy")

        self._adjudicate_and_chronicle(
            [(command_str, vessel.line_num, undo_block, heresy_block)],
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
            # [ASCENSION 10]: ATOMIC SIGNAL DECAPITATION
            # If it's a polyglot command, we bypass the shell sentry;
            # the PolyglotHandler handles its own security adjudication.
            if ":" in cmd_str.split('\n', 1)[0]:
                valid_commands.append((cmd_str, line, undo_block, heresy_block))
                continue

            try:
                # Clean leading sigils
                clean_intent = re.sub(r'^>+\s*', '', cmd_str)

                # [FACULTY 5]: THE SENTRY'S VOW
                self.sentry.adjudicate(clean_intent, self.parser.base_path, line)
                valid_commands.append((clean_intent, line, undo_block, heresy_block))

            except GuardianHeresy as e:
                self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=e.get_proclamation())

        if not valid_commands:
            return

        # 1. COMMIT TO MASTER EDICT STREAM
        # This is what the Maestro actually executes.
        self.parser.post_run_commands.extend(valid_commands)

        # 2. FORGE GNOSTIC ANCHORS (ASCENSION 6)
        # We record the line numbers in a JSON payload for the AST weaver.
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
        return "<Ω_POST_RUN_SCRIBE status=VIGILANT version=3.5-POLYGLOT>"
