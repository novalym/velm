# scaffold/parser_core/parser_scribes/scaffold_scribes/comment_scribe.py
import re
from pathlib import Path
from typing import List, TYPE_CHECKING

# --- CHANGED IMPORT ---
from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticLineType, GnosticVessel, ScaffoldItem

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser

class CommentScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF META-GNOSIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                  ==
    =================================================================================
    This is not a Scribe of Silence. This is a divine, polyglot God-Engine whose
    Gaze perceives not just comments, but the very meta-Gnosis of the Architect's
    will, transforming a simple text file into a living, self-aware architectural
    program.
    =================================================================================
    """
    # FACULTY #1 & #10: THE POLYGLOT SOUL & THE HIERARCHICAL GAZE
    INTENT_REGEX = re.compile(
        r"^\s*("
        r"(?P<SHEBANG>#!/.*)|"
        r"(?P<MARKDOWN_HEADER>##+.*)|"
        r"(?P<DESCRIPTION>#\s*@description:.*)|"
        r"(?P<PRAGMA>#\s*@scaffold-[\w:]+.*)|"
        r"(?P<TODO>#\s*TODO\(.*?\):.*)|"
        r"(?P<JINJA_COMMENT>\{#.*#\})|"
        r"(?P<SQL_COMMENT>--.*)|"
        r"(?P<C_STYLE_COMMENT>//.*)|"
        r"(?P<HASH_COMMENT>#.*)"
        r")"
    )

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "CommentScribe")

    # FACULTY #1: The Annihilation of the Gaze
    # def gaze(...) is ANNIHILATED.

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE GRAND CONDUCTOR OF META-GNOSIS (THE GNOSTIC TRIAGE)                     ==
        =================================================================================
        This rite is a divine symphony. It perceives the nature of a comment or void
        and summons the correct specialist artisan to chronicle its Gnosis or
        righteously annihilate it from the timeline.
        =================================================================================
        """
        line_num = i + 1 + self.parser.line_offset
        stripped = vessel.raw_scripture.strip()

        try:
            # --- THE GNOSTIC TRIAGE (FACULTY #11 & #12) ---
            if not stripped:
                self.Logger.verbose(f"L{line_num:03d}: Gaze of Silence perceived a pure void. Annihilating.")
                return i + 1

            # The deep Gaze to find the comment's true soul.
            intent_match = self.INTENT_REGEX.match(stripped)

            if intent_match:
                intent = intent_match.lastgroup
                # FACULTY #5: The Gaze of the Gnostic Shebang
                if intent == 'SHEBANG':
                    return self._conduct_shebang_rite(vessel, lines, i)
                # FACULTY #4: The Gnostic Pragma
                if intent == 'PRAGMA':
                    pragma_match = re.match(r'^\s*#\s*@scaffold-([\w:]+)(.*)', stripped)
                    if pragma_match:
                        return self._conduct_pragma_rite(pragma_match, vessel)
                # FACULTY #6 & #7: Sentient Docs & Gnostic TODOs
                if intent in ('MARKDOWN_HEADER', 'DESCRIPTION', 'TODO'):
                    return self._conduct_meta_gnosis_rite(vessel)

            # Default: It is a simple, humble comment to be annihilated.
            self.Logger.verbose(f"L{line_num:03d}: Annihilated a humble comment: '{stripped[:60]}...'")
            return i + 1

        except Exception as e:
            # FACULTY #8: THE UNBREAKABLE WARD OF GRACE
            self.Logger.error(f"A catastrophic paradox occurred within the Oracle of Meta-Gnosis on line {line_num}.", ex=e)
            return i + 1

    def _conduct_pragma_rite(self, match: re.Match, vessel: GnosticVessel) -> int:
        """A divine, specialist artisan for perceiving and acting upon Gnostic Pragmas."""
        key, value = match.groups()
        # FACULTY #9: The Luminous Voice
        self.Logger.info(
            f"L{vessel.line_num:03d}: Perceived Gnostic Pragma: [cyan]@{key.strip()}[/cyan] with value [yellow]'{value.strip()}'[/yellow]")

        # A prophecy for a future ascension where this forges a PRAGMA item.
        # For now, it is annihilated to prevent paradoxes.
        return vessel.line_num - self.parser.line_offset

    def _conduct_shebang_rite(self, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        """A divine, specialist artisan for bestowing executable will."""
        line_num = vessel.line_num
        self.Logger.info(
            f"L{line_num:03d}: Perceived a Gnostic Shebang. Bestowing executable will upon the next scripture.")

        # This rite performs a "lookahead" Gaze into the future of the timeline.
        for j in range(i + 1, len(lines)):
            # We must summon the master Inquisitor to perceive the next line's true soul.
            next_vessel = self.parser.inquisitor.inquire(lines[j], j + 1, self.parser, "scaffold", self.parser._calculate_original_indent(lines[j]))

            if next_vessel.line_type in (GnosticLineType.COMMENT, GnosticLineType.VOID):
                continue # Skip comments/voids

            # A true scripture of Form has been found. The will is bestowed upon the master Parser.
            if next_vessel.line_type == GnosticLineType.FORM:
                self.parser.pending_permissions = "755"
                self.Logger.verbose("   -> The will for '%% 755' has been bestowed upon the Parser's memory.")
            break
        else:
            self.Logger.warn(f"L{line_num:03d}: A Shebang was perceived, but no subsequent scripture of Form was found.")

        return i + 1

    def _conduct_meta_gnosis_rite(self, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE SCRIBE OF SENTIENT DOCUMENTATION (THE GNOSTIC VESSEL PROCLAMATION)      ==
        =================================================================================
        This divine artisan no longer annihilates valuable meta-gnosis. It forges a
        special `ScaffoldItem` of type `COMMENT`, preserving the Architect's thoughts
        for future artisans like the BlueprintScribe.
        =================================================================================
        """
        self.Logger.verbose(
            f"L{vessel.line_num:03d}: Chronicling a scripture of Meta-Gnosis: '{vessel.raw_scripture.strip()[:60]}...'")

        # FACULTY #6: THE GNOSTIC VESSEL PROCLAMATION
        meta_item = ScaffoldItem(
            path=Path(f"COMMENT:{vessel.line_num}"),
            is_dir=False,
            content=vessel.raw_scripture,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            line_type=GnosticLineType.COMMENT,
            original_indent=vessel.original_indent
        )
        self.parser.raw_items.append(meta_item)

        return vessel.line_num - self.parser.line_offset