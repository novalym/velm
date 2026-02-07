# Path: src/velm/parser_core/lexer_core/inquisitor.py
# ---------------------------------------------------

import re
import traceback
from pathlib import Path
from typing import Optional, List, Union, Dict, Any, TYPE_CHECKING

# --- THE DIVINE IMPORTS ---
from .contracts import TokenType
from ...contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .deconstructor import DeconstructionScribe
from .lexer import GnosticLexer
from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy, Heresy
from ...contracts.symphony_contracts import EdictType
from ...logger import Scribe

if TYPE_CHECKING:
    from ..parser import ApotheosisParser


class GnosticLineInquisitor:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC PERCEPTION (V-Ω-ULTRA-DEFINITIVE-ASCENDED)        ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: LEXICAL_TRIAGE_MASTER | RANK: OMEGA

    This is the divine, sentient Inquisitor in its final, eternal form. Its Prime
    Directive is to gaze upon a raw line of scripture, perform a Gnostic Triage to
    perceive its one true purpose, and forge a GnosticVessel containing its soul.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Gnostic Triage (Declarative Mind):** The profane `if/elif` chain has been
        annihilated. Its mind is now a `PERCEPTION_GRIMOIRE`, a declarative map that
        binds a Gnostic `detector` rite to each `LineType`, making perception absolute.
    2.  **The Trait Seer:** Instantly recognizes `%% trait` and `%% use` signatures.
    3.  **The Lexer's Primacy:** It delegates the deepest Gaze to the `GnosticLexer` and
        `DeconstructionScribe`, purifying its own soul to be a pure Conductor.
    4.  **The Sovereign Soul (Unified Class):** The profane `_GnosticInquest` has been
        annihilated, its soul absorbed into this single, sovereign entity.
    5.  **The Unbreakable Ward of Paradox:** Its `inquire` rite is shielded. A paradox
        will not shatter the Parser; it will forge a luminous Heresy.
    6.  **The Polyglot Prophet:** The Grimoire architecture makes the Inquisitor a true
        Polyglot, ready for new languages.
    7.  **The Gnostic Purifier:** It retains the sacred rites for purifying paths and content.
    8.  **The Final Proclamation:** Its `inquire` rite's one true purpose is to return a
        single, pure `GnosticVessel`.
    9.  **The Luminous Heresy Forge:** It wields a universal `_proclaim_heresy` rite.
    10. **The Anointed Soul:** Its `_conduct_symphony_rite` is anointed with the
        `DeconstructionScribe` to perceive the full grammar of the Language of Will.
    11. **The Symlink Sentinel:** Detects `->` patterns to preemptively categorize links.
    12. **The Gaze of Redemption:** Explicitly recognizes `%% on-heresy` as a distinct
        metaphysical state, separating failure handling from standard execution.
    """

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

        # =========================================================================
        # == THE GRIMOIRE OF PERCEPTION (THE DECLARATIVE MIND)                   ==
        # =========================================================================
        # Order matters: Specific directives must be caught before generic variable assignments.
        self.PERCEPTION_GRIMOIRE = [
            # 1. The Void
            (lambda s: not s, GnosticLineType.VOID, "Void"),

            # 2. The Whispers (Comments)
            (lambda s: s.startswith(('#', '//')), GnosticLineType.COMMENT, "Comment"),

            # 3. The Logic of the Alchemist
            (lambda s: s.startswith(('{%', '{#')), GnosticLineType.JINJA_CONSTRUCT, "Jinja Construct"),

            # 4. The Contracts of Law
            (lambda s: s.startswith('%% contract'), GnosticLineType.CONTRACT_DEF, "Contract Definition"),

            # 5. The Traits (Mixins)
            (lambda s: s.startswith('%% trait'), GnosticLineType.TRAIT_DEF, "Trait Definition"),
            (lambda s: s.startswith('%% use'), GnosticLineType.TRAIT_USE, "Trait Usage"),

            # 6. [ASCENSION]: THE RITE OF REDEMPTION
            # Must precede generic POST_RUN to prevent the "False Equivalence" heresy.
            (lambda s: s.startswith('%% on-heresy'), GnosticLineType.ON_HERESY, "On-Heresy Block"),

            # 7. The Rite of Reversal
            # Must precede generic POST_RUN.
            (lambda s: s.startswith('%% on-undo'), GnosticLineType.ON_UNDO, "On-Undo Block"),

            # 8. The Generic State Change (post-run, pre-run, weave)
            (lambda s: s.startswith('%%'), GnosticLineType.POST_RUN, "Post-Run Block"),

            # 9. The Variables of State
            (lambda s: s.startswith(('$$', 'let ', 'def ', 'const ')), GnosticLineType.VARIABLE, "Variable Definition"),

            # 10. The Directives of Logic
            (lambda s: s.startswith('@'), GnosticLineType.LOGIC, "Logic Directive"),

            # 11. The Bare Assignments (Legacy Support)
            (lambda s: re.match(r"^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*(?::[^=]+)?\s*=", s), GnosticLineType.VARIABLE,
             "Bare Assignment"),
        ]

    def _proclaim_heresy(self, key: str, item: Union[GnosticVessel, ScaffoldItem, str], **kwargs):
        """Delegates the forging of the heresy vessel to the one true, universal rite."""
        from ...jurisprudence_core.jurisprudence import forge_heresy_vessel

        raw_scripture = getattr(item, 'raw_scripture', str(item))
        line_num = getattr(item, 'line_num', self.line_num)
        exception_obj = kwargs.get('exception_obj')
        details = kwargs.get('details', "")

        if exception_obj:
            # Forensic Traceback Extraction
            tb_list = traceback.extract_tb(exception_obj.__traceback__)
            scaffold_frames = [frame for frame in tb_list if 'scaffold' in frame.filename]
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
            self.vessel.is_valid = False
            self._proclaim_heresy(
                "META_HERESY_INQUISITOR_FRACTURED", self.vessel,
                details=f"Gaze shattered by unhandled paradox.", exception_obj=e
            )
            return self.vessel

    def _conduct_scaffold_rite(self):
        """The mind of the Gnostic Parser, utilizing the declarative Grimoire."""
        l_stripped_line = self.raw_line.lstrip()

        # 1. The Gnostic Triage
        for detector, line_type, name in self.PERCEPTION_GRIMOIRE:
            if detector(l_stripped_line):
                self.vessel.line_type = line_type

                # For simple types, we set the name to the raw line immediately
                if line_type in (
                        GnosticLineType.COMMENT,
                        GnosticLineType.JINJA_CONSTRUCT,
                        GnosticLineType.POST_RUN,
                        GnosticLineType.VARIABLE,
                        GnosticLineType.LOGIC,
                        GnosticLineType.CONTRACT_DEF,
                        GnosticLineType.TRAIT_DEF,
                        GnosticLineType.TRAIT_USE,
                        # [ASCENSION]: Redemption & Reversal
                        GnosticLineType.ON_HERESY,
                        GnosticLineType.ON_UNDO
                ):
                    self.vessel.name = self.raw_line.strip()

                    if line_type == GnosticLineType.JINJA_CONSTRUCT:
                        self.vessel.is_jinja_construct = True
                        self.vessel.jinja_expression = self.raw_line.strip()
                return

        # 2. Default to FORM (Structure)
        self.vessel.line_type = GnosticLineType.FORM

        # 3. Summon the Lexer for Deep Analysis
        lexer = GnosticLexer(grammar_key="scaffold")
        tokens = lexer.tokenize(self.raw_line)

        if not tokens:
            self.vessel.line_type = GnosticLineType.VOID
            return

        # 4. Summon the Deconstructor
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

        # 5. Merge Deconstructed Gnosis
        self.vessel.name = deconstructed_vessel.name
        self.vessel.path = deconstructed_vessel.path
        self.vessel.is_dir = deconstructed_vessel.is_dir
        self.vessel.content = deconstructed_vessel.content
        self.vessel.seed_path = deconstructed_vessel.seed_path
        self.vessel.permissions = deconstructed_vessel.permissions
        self.vessel.is_valid = deconstructed_vessel.is_valid
        self.vessel.mutation_op = deconstructed_vessel.mutation_op
        self.vessel.semantic_selector = deconstructed_vessel.semantic_selector

        # [NEW] Expansion V-Ω Fields
        self.vessel.is_symlink = deconstructed_vessel.is_symlink
        self.vessel.symlink_target = deconstructed_vessel.symlink_target
        self.vessel.expected_hash = deconstructed_vessel.expected_hash
        self.vessel.trait_name = deconstructed_vessel.trait_name
        self.vessel.trait_path = deconstructed_vessel.trait_path
        self.vessel.trait_args = deconstructed_vessel.trait_args

        # 6. Type Promotion (Traits)
        if deconstructed_vessel.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
            self.vessel.line_type = deconstructed_vessel.line_type

    def _conduct_symphony_rite(self):
        """The High Inquisitor of Will, now with the Anointed Soul."""
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

        # Transfer the Core Type Gnosis
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
        """The pure, stateless Conductor of the Gnostic Inquest."""
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
            heresy_vessel = GnosticVessel(
                raw_scripture=raw_line,
                line_num=line_num,
                is_valid=False,
                original_indent=original_indent
            )
            error_details = (
                f"High Inquisitor's soul fractured on line {line_num}.\n"
                f"Scripture: '{raw_line.strip()}'\n\n"
                f"[bold red]EXCEPTION:[/bold red] {type(e).__name__}: {e}\n"
                f"[dim]Traceback:\n{tb}[/dim]"
            )

            # We append directly to the parser if available, or raise if not.
            # In classmethod context, we rely on the parser passed in.
            parser.heresies.append(Heresy(
                message="META_HERESY_INQUISITOR_FRACTURED",
                line_num=line_num,
                line_content=raw_line,
                details=error_details,
                severity=HeresySeverity.CRITICAL
            ))
            return heresy_vessel