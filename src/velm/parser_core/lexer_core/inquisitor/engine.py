# Path: parser_core/lexer_core/inquisitor/engine.py
# -------------------------------------------------

import re
import unicodedata
import traceback
from typing import TYPE_CHECKING, Optional

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import GnosticVessel, GnosticLineType
from ....contracts.heresy_contracts import HeresySeverity, ArtisanHeresy
from ..lexer import GnosticLexer
from ..deconstructor import DeconstructionScribe

# --- THE ORGANS ---
from .forensics import TriageForensics
from .sentinel import CodeSentinel
from .geometry import GeometricValidator
from .triage import LexicalTriage
from .radiation import InquisitorRadiator

from ....logger import Scribe

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser

Logger = Scribe("GnosticInquisitor")


class GnosticLineInquisitor:
    """
    =============================================================================
    == THE OMEGA INQUISITOR FACADE (V-Ω-TOTALITY-VMAX)                         ==
    =============================================================================
    LIF: ∞^∞ | ROLE: LEXICAL_TRIAGE_MASTER | RANK: OMEGA_SOVEREIGN_PRIME

    [THE MANIFESTO]
    The monolithic era is over. The Inquisitor delegates perception to specialized
    stateless organs. It righteously supports the Semantic Suture (*=) and
    dynamic Topography ({{ var }}).
    """

    __slots__ = ('raw_line', 'line_num', 'parser', 'grammar_codex_key', 'vessel')

    def __init__(
            self,
            raw_line: str,
            line_num: int,
            parser: 'ApotheosisParser',
            grammar_codex_key: str,
            original_indent: int
    ):
        """[THE RITE OF INCEPTION]"""
        # [ASCENSION 4]: ZERO-WIDTH EXORCISM
        purified_raw = re.sub(r'[\ufeff\u200b\u200c\u200d\u2060]', '', raw_line)
        self.raw_line = purified_raw
        self.line_num = line_num
        self.parser = parser
        self.grammar_codex_key = grammar_codex_key

        self.vessel = GnosticVessel(
            raw_scripture=self.raw_line,
            line_num=line_num,
            original_indent=original_indent
        )

    def _conduct_inquest(self) -> GnosticVessel:
        """The God-Engine of Gnostic Perception."""
        try:
            # [ASCENSION 10]: NFC NORMALIZATION
            self.raw_line = unicodedata.normalize('NFC', self.raw_line)

            if self.grammar_codex_key == "scaffold":
                self._conduct_scaffold_rite()
            elif self.grammar_codex_key == "symphony":
                self._conduct_symphony_rite()
            else:
                raise ArtisanHeresy(f"META-HERESY: Unknown grammar key '{self.grammar_codex_key}'")

            return self.vessel

        except Exception as e:
            self.vessel.is_valid = False
            TriageForensics.proclaim_heresy(
                self.parser,
                "META_HERESY_INQUISITOR_FRACTURED",
                self.vessel,
                details=f"Gaze shattered by unhandled paradox.",
                exception_obj=e,
                severity=HeresySeverity.CRITICAL
            )
            return self.vessel

    def _conduct_scaffold_rite(self):
        """
        =========================================================================
        == THE SUPREME CONDUCTOR: TOTALITY (V-Ω-VMAX-SIGIL-PRIMACY-FINALIS)    ==
        =========================================================================
        """
        raw_line_content = self.raw_line.strip()
        l_stripped_line = self.raw_line.lstrip()

        # =====================================================================
        # == MOVEMENT 0: [THE MASTER CURE] - PRIMARY MATTER ESCALATION       ==
        # =====================================================================
        if GeometricValidator.is_explicit_form(raw_line_content) or GeometricValidator.is_sanctum(raw_line_content):
            self.vessel.line_type = GnosticLineType.FORM
            self._execute_deep_inquest()
            return

        # =====================================================================
        # == MOVEMENT I: THE NAKED DIRECTIVE WARD                            ==
        # =====================================================================
        if l_stripped_line.startswith('@'):
            match = re.match(r'^@(?P<verb>\w+)\s*(?P<args>.*)', l_stripped_line)
            if match:
                self.vessel.line_type = GnosticLineType.LOGIC
                self.vessel.directive_type = match.group('verb').lower()
                self.vessel.name = match.group('args').strip()
                InquisitorRadiator.radiate(self.parser, GnosticLineType.LOGIC)
                return

        # =====================================================================
        # == MOVEMENT II: THE GNOSTIC CENSUS (THE GRIMOIRE)                  ==
        # =====================================================================
        for detector, line_type in LexicalTriage.get_grimoire():
            if detector(self.raw_line):
                self.vessel.line_type = line_type

                if line_type in (
                        GnosticLineType.COMMENT, GnosticLineType.SGF_CONSTRUCT,
                        GnosticLineType.POST_RUN, GnosticLineType.VARIABLE,
                        GnosticLineType.LOGIC, GnosticLineType.CONTRACT_DEF,
                        GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE,
                        GnosticLineType.ON_HERESY, GnosticLineType.ON_UNDO,
                        GnosticLineType.VOW
                ):
                    self.vessel.name = raw_line_content
                    if line_type == GnosticLineType.SGF_CONSTRUCT:
                        self.vessel.is_sgf_construct = True
                        self.vessel.sgf_expression = raw_line_content

                InquisitorRadiator.radiate(self.parser, line_type)
                return

        # =====================================================================
        # == MOVEMENT III: THE FALLBACK REALITY (FORM)                       ==
        # =====================================================================
        self.vessel.line_type = GnosticLineType.FORM
        self._execute_deep_inquest()

    def _execute_deep_inquest(self):
        """[THE RITE OF ATOMIC ASSEMBLY]"""
        InquisitorRadiator.radiate(self.parser, GnosticLineType.FORM)

        lexer = GnosticLexer(grammar_key="scaffold")
        tokens = lexer.tokenize(self.raw_line)

        if not tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return

        scribe = DeconstructionScribe(
            raw_scripture=self.raw_line,
            line_num=self.line_num,
            tokens=tokens,
            logger=Logger,
            original_indent=self.vessel.original_indent,
            variables=self.parser.variables,
            parser=self.parser
        )
        deconstructed = scribe.inquire()

        # [THE CURE]: Absolute Suture of attributes across the deconstruction rift.
        attrs = ['name', 'path', 'is_dir', 'content', 'seed_path', 'permissions',
                 'is_valid', 'mutation_op', 'semantic_selector', 'is_symlink',
                 'symlink_target', 'expected_hash', 'trait_name', 'trait_path', 'trait_args']

        for attr in attrs:
            setattr(self.vessel, attr, getattr(deconstructed, attr))

        if deconstructed.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
            self.vessel.line_type = deconstructed.line_type

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
            logger=Logger,
            original_indent=self.vessel.original_indent,
            variables=self.parser.variables,
            parser=self.parser
        )
        deconstructed = scribe.inquire()

        self.vessel.line_type = deconstructed.line_type
        self.vessel.edict_type = deconstructed.edict_type
        self.vessel.command = deconstructed.command
        self.vessel.language = deconstructed.language
        self.vessel.delimiter = deconstructed.delimiter
        self.vessel.directive_type = deconstructed.directive_type

    @classmethod
    def inquire(
            cls,
            raw_line: str,
            line_num: int,
            parser: 'ApotheosisParser',
            grammar_codex_key: str,
            original_indent: int
    ) -> GnosticVessel:
        """The supreme dispatcher for retinal perception."""
        inquest = cls(raw_line, line_num, parser, grammar_codex_key, original_indent)
        return inquest._conduct_inquest()

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_INQUISITOR session={self.parser.parse_session_id[:8]} status=RESONANT>"