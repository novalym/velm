# src/velm/parser_core/lexer_core/inquisitor.py
# ---------------------------------------------------

import os
import re
import sys
import traceback
from pathlib import Path
from typing import Optional, List, Union, Dict, Any, TYPE_CHECKING, Final, Tuple

# --- THE DIVINE IMPORTS ---
from .contracts import TokenType
from ...contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .deconstructor import DeconstructionScribe
from .lexer import GnosticLexer
from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy, Heresy
from ...contracts.symphony_contracts import EdictType
from ...logger import Scribe

if TYPE_CHECKING:
    from ..parser.engine import ApotheosisParser


class GnosticLineInquisitor:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC PERCEPTION (V-Ω-HYPER-DIAGNOSTIC-ULTIMA)          ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: LEXICAL_TRIAGE_MASTER | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_INQUISITOR_DIAGNOSTIC_VMAX
    """

    # [THE CURE]: THE INVINCIBLE VOW PHALANX
    VOW_PATTERN: Final[re.Pattern] = re.compile(
        r'^(?:->\s*)?'  # Optional Arrow (from inline @if)
        r'(?:retry\([^)]*\):\s*)?'  # Optional Retry Wrapper
        r'(?:'  # Core Sigils:
        r'>>|\?\?|!!|'  # - Shell, Vow, Breakpoint
        r'proclaim:|echo\s|allow_fail:|'  # - Proclamations & Modifiers
        r'(?:py|python|js|node|rs|rust|sh|bash|go):\s*$'  # - Polyglot Heads (Strictly End of Line)
        r')',
        re.IGNORECASE
    )

    def __init__(
            self,
            raw_line: str,
            line_num: int,
            parser: 'ApotheosisParser',
            grammar_codex_key: str,
            original_indent: int
    ):
        self.raw_line = raw_line
        self.line_num = line_num
        self.Logger = Scribe("GnosticInquisitor")
        self.parser = parser
        self.grammar_codex_key = grammar_codex_key
        self.vessel = GnosticVessel(
            raw_scripture=raw_line,
            line_num=line_num,
            original_indent=original_indent
        )

        self.PERCEPTION_GRIMOIRE = [
            (lambda s: not s, GnosticLineType.VOID, "Void"),
            (lambda s: s.startswith(('#', '//')), GnosticLineType.COMMENT, "Comment"),
            (lambda s: s.startswith(('{%', '{#')), GnosticLineType.JINJA_CONSTRUCT, "Jinja Construct"),
            (lambda s: s.startswith('%% contract'), GnosticLineType.CONTRACT_DEF, "Contract Definition"),
            (lambda s: s.startswith('%% trait'), GnosticLineType.TRAIT_DEF, "Trait Definition"),
            (lambda s: s.startswith('%% use'), GnosticLineType.TRAIT_USE, "Trait Usage"),
            (lambda s: s.startswith('%% on-heresy'), GnosticLineType.ON_HERESY, "On-Heresy Block"),
            (lambda s: s.startswith('%% on-undo'), GnosticLineType.ON_UNDO, "On-Undo Block"),
            (lambda s: s.startswith('%%'), GnosticLineType.POST_RUN, "Post-Run Block"),
            (lambda s: bool(self.VOW_PATTERN.match(s)), GnosticLineType.VOW, "Atomic Edict"),
            (lambda s: s.startswith(('$$', 'let ', 'def ', 'const ')), GnosticLineType.VARIABLE, "Variable Definition"),
            (lambda s: s.startswith('@'), GnosticLineType.LOGIC, "Logic Directive"),
            (lambda s: bool(re.match(r"^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*(?::[^=]+)?\s*=", s)), GnosticLineType.VARIABLE,
             "Bare Assignment"),
        ]

    def _proclaim_heresy(self, key: str, item: Union[GnosticVessel, ScaffoldItem, str], **kwargs):
        """Delegates the forging of the heresy vessel to the one true, universal rite."""
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel

        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', self.line_num)
        exception_obj = kwargs.get('exception_obj')
        details = kwargs.get('details', "")

        # [ASCENSION]: HYPER-DIAGNOSTIC TRACEBACK DUMP
        if exception_obj:
            sys.stderr.write(f"\n[INQUISITOR:FATAL] Heresy on L{line_num}: {key}\n")
            traceback.print_exc(file=sys.stderr)

            # Formatting for the internal log
            tb_list = traceback.extract_tb(exception_obj.__traceback__)
            scaffold_frames = [frame for frame in tb_list if 'scaffold' in frame.filename or 'velm' in frame.filename]
            last_frame = scaffold_frames[-1] if scaffold_frames else tb_list[-1]

            forensic_report = (
                f"Paradox Soul: {type(exception_obj).__name__}: {str(exception_obj)}\n"
                f"Locus: {Path(last_frame.filename).name}:{last_frame.lineno} in `{last_frame.name}`"
            )
            details = f"{details}\n{forensic_report}"

        heresy = forge_heresy_vessel(
            key=key,
            line_num=line_num,
            line_content=raw_scripture,
            details=details
        )

        if severity_override := kwargs.get('severity'):
            heresy.severity = severity_override

        self.parser.heresies.append(heresy)

        if hasattr(item, 'is_valid'):
            item.is_valid = False

        if heresy.severity == HeresySeverity.CRITICAL:
            self.parser.all_rites_are_pure = False

    def _conduct_inquest(self) -> GnosticVessel:
        """
        The God-Engine of Gnostic Perception.
        Determines the grammar and dispatches the specialized inquest.
        """
        try:
            if self.grammar_codex_key == "scaffold":
                self._conduct_scaffold_rite()
            elif self.grammar_codex_key == "symphony":
                self._conduct_symphony_rite()
            else:
                raise ArtisanHeresy(f"META-HERESY: Unknown grammar key '{self.grammar_codex_key}'")

            return self.vessel


        except Exception as e:

            # [ASCENSION]: FORCE TRACEBACK CAPTURE

            tb_str = traceback.format_exc()

            # Print to stderr for immediate visibility in simulation logs

            sys.stderr.write(f"\n[INQUISITOR:CRASH] Exception in inquire() at L{self.line_num}: {e}\n")

            self.vessel.is_valid = False

            self._proclaim_heresy(

                "META_HERESY_INQUISITOR_FRACTURED", self.vessel,

                details=f"Gaze shattered by unhandled paradox.\n\nTraceback:\n{tb_str}",  # <--- THE FIX

                exception_obj=e,

                severity=HeresySeverity.CRITICAL

            )

            return self.vessel

    def _conduct_scaffold_rite(self):
        """
        =============================================================================
        == THE SUPREME CONDUCTOR: TOTALITY (V-Ω-TOTALITY-V150000.0-NAKED-WARDED)   ==
        =============================================================================
        """
        # --- STRATUM 0: THE SENSORY PROBE ---
        raw_line_content = self.raw_line.strip()
        l_stripped_line = self.raw_line.lstrip()

        # =========================================================================
        # == MOVEMENT I: [THE CURE] - THE NAKED DIRECTIVE WARD (ASCENSION 13)    ==
        # =========================================================================
        if l_stripped_line.startswith('@'):
            match = re.match(r'^@(?P<verb>\w+)\s*(?P<args>.*)', l_stripped_line)
            if match:
                verb = match.group('verb').lower()
                naked_args = match.group('args').strip()

                self.vessel.line_type = GnosticLineType.LOGIC
                self.vessel.directive_type = verb
                self.vessel.name = naked_args
                return

        # =========================================================================
        # == MOVEMENT II: THE GNOSTIC TRIAGE (THE CENSUS)                        ==
        # =========================================================================
        for detector, line_type, semantic_label in self.PERCEPTION_GRIMOIRE:
            if detector(l_stripped_line):
                self.vessel.line_type = line_type

                if line_type in (
                        GnosticLineType.COMMENT,
                        GnosticLineType.JINJA_CONSTRUCT,
                        GnosticLineType.POST_RUN,
                        GnosticLineType.VARIABLE,
                        GnosticLineType.LOGIC,
                        GnosticLineType.CONTRACT_DEF,
                        GnosticLineType.TRAIT_DEF,
                        GnosticLineType.TRAIT_USE,
                        GnosticLineType.ON_HERESY,
                        GnosticLineType.ON_UNDO,
                        GnosticLineType.VOW
                ):
                    self.vessel.name = raw_line_content

                    if line_type == GnosticLineType.JINJA_CONSTRUCT:
                        self.vessel.is_jinja_construct = True
                        self.vessel.jinja_expression = raw_line_content

                return

        # =========================================================================
        # == MOVEMENT III: THE DEEP INQUEST (LEXICAL ATOMIZATION)                ==
        # =========================================================================
        self.vessel.line_type = GnosticLineType.FORM

        from ..lexer_core.lexer import GnosticLexer
        from ..lexer_core.deconstructor import DeconstructionScribe

        lexer = GnosticLexer(grammar_key="scaffold")
        tokens = lexer.tokenize(self.raw_line)

        if not tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return

        # =========================================================================
        # == MOVEMENT IV: THE RITE OF DECONSTRUCTION (ASSEMBLY)                  ==
        # =========================================================================
        scribe = DeconstructionScribe(
            raw_scripture=self.raw_line,
            line_num=self.line_num,
            tokens=tokens,
            logger=self.Logger,
            original_indent=self.vessel.original_indent,
            variables=self.parser.variables,
            parser=self.parser
        )
        deconstructed_vessel = scribe.inquire()

        # =========================================================================
        # == MOVEMENT V: THE GNOSTIC SUTURE (MERGE)                              ==
        # =========================================================================
        self.vessel.name = deconstructed_vessel.name
        self.vessel.path = deconstructed_vessel.path
        self.vessel.is_dir = deconstructed_vessel.is_dir
        self.vessel.content = deconstructed_vessel.content
        self.vessel.seed_path = deconstructed_vessel.seed_path
        self.vessel.permissions = deconstructed_vessel.permissions
        self.vessel.is_valid = deconstructed_vessel.is_valid
        self.vessel.mutation_op = deconstructed_vessel.mutation_op
        self.vessel.semantic_selector = deconstructed_vessel.semantic_selector
        self.vessel.is_symlink = deconstructed_vessel.is_symlink
        self.vessel.symlink_target = deconstructed_vessel.symlink_target
        self.vessel.expected_hash = deconstructed_vessel.expected_hash
        self.vessel.trait_name = deconstructed_vessel.trait_name
        self.vessel.trait_path = deconstructed_vessel.trait_path
        self.vessel.trait_args = deconstructed_vessel.trait_args

        if deconstructed_vessel.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
            self.vessel.line_type = deconstructed_vessel.line_type

    def _conduct_symphony_rite(self):
        """The High Inquisitor of Will."""
        lexer = GnosticLexer(grammar_key="symphony")
        tokens = lexer.tokenize(self.raw_line)

        if not tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return

        scribe = DeconstructionScribe(
            raw_scripture=self.raw_line,
            line_num=self.line_num,
            tokens=tokens,
            logger=self.Logger,
            original_indent=self.vessel.original_indent,
            variables=self.parser.variables,
            parser=self.parser
        )
        deconstructed_vessel = scribe.inquire()

        self.vessel.line_type = deconstructed_vessel.line_type
        self.vessel.edict_type = deconstructed_vessel.edict_type
        self.vessel.command = deconstructed_vessel.command
        self.vessel.language = deconstructed_vessel.language
        self.vessel.delimiter = deconstructed_vessel.delimiter
        self.vessel.directive_type = deconstructed_vessel.directive_type

    @classmethod
    def inquire(
            cls,
            raw_line: str,
            line_num: int,
            parser: 'ApotheosisParser',
            grammar_codex_key: str,
            original_indent: int
    ) -> GnosticVessel:
        """The pure, stateless Conductor."""
        try:
            inquest = cls(
                raw_line=raw_line,
                line_num=line_num,
                parser=parser,
                grammar_codex_key=grammar_codex_key,
                original_indent=original_indent
            )
            return inquest._conduct_inquest()

        except Exception as e:
            tb = traceback.format_exc()
            sys.stderr.write(f"\n[INQUISITOR:CRASH] Exception in inquire() at L{line_num}: {e}\n{tb}\n")

            heresy_vessel = GnosticVessel(
                raw_scripture=raw_line,
                line_num=line_num,
                is_valid=False,
                original_indent=original_indent
            )

            parser.heresies.append(Heresy(
                message="META_HERESY_INQUISITOR_FRACTURED",
                line_num=line_num,
                line_content=raw_line,
                details=f"The Inquisitor collapsed. See stderr for traceback.",
                severity=HeresySeverity.CRITICAL
            ))
            return heresy_vessel