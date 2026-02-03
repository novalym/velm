# Path: core/lsp/utils/text.py
# ----------------------------
# LIF: INFINITY | AUTH_CODE: Ω_TEXT_UTILS_V9000
# SYSTEM: GNOSTIC_KERNEL | ROLE: LINGUISTIC_ALCHEMIST
# =================================================================================

import re
from typing import NamedTuple, Optional, List, Union, Any, Callable
from ..types import Position, Range

# =================================================================================
# == SECTION I: THE ANSI EXORCIST                                                ==
# =================================================================================

# Pre-compiled pattern for 7-bit and 8-bit C1 ANSI sequences
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi(text: str) -> str:
    """
    [THE PURIFIER]
    Removes all ANSI escape codes from a string.
    Essential for cleaning Daemon logs before sending them to the UI.
    """
    if not text:
        return ""
    return ANSI_ESCAPE_PATTERN.sub('', text)


# =================================================================================
# == SECTION II: THE SEMANTIC GEOMETER                                           ==
# =================================================================================

class WordInfo(NamedTuple):
    """The atom of meaning found under the cursor."""
    text: str
    range: Range
    line_text: str
    position: Position
    kind: str  # 'variable', 'path', 'directive', 'maestro', 'generic'


class TextUtils:
    """
    [THE SCRIBE]
    A library of static methods for analyzing the sacred geometry of text.
    """

    # --- THE GRIMOIRE OF REGEX ---
    # Captures $$variable
    RE_VARIABLE = re.compile(r'\$\$[\w_]+')
    # Captures @directive
    RE_DIRECTIVE = re.compile(r'@[\w]+')
    # Captures %% maestro_block
    RE_MAESTRO = re.compile(r'%%[\w\-]+')
    # Captures file paths (naive)
    RE_PATH = re.compile(r'[\w\.\-\/_\\\:]+')
    # Captures generic words (fallback)
    RE_GENERIC = re.compile(r'[\w$@%\.\/\-]+')

    @staticmethod
    def get_word_at_position(doc: Any, pos: Position) -> Optional[WordInfo]:
        """
        Divines the symbol under the cursor.
        It attempts to find the most specific match first (Variable/Directive),
        falling back to generic words.

        Args:
            doc: TextDocument instance (duck-typed for import safety)
            pos: Position object
        """
        line_text = doc.get_line(pos.line)
        char = pos.character

        # Clamp character position to line length
        if char > len(line_text):
            char = len(line_text)

        # 1. Check for specific Gnostic constructs first (High Priority)
        priority_patterns = [
            ('variable', TextUtils.RE_VARIABLE),
            ('directive', TextUtils.RE_DIRECTIVE),
            ('maestro', TextUtils.RE_MAESTRO),
            # Paths are tricky because they overlap with generics.
            # We treat them as specific if they contain slashes.
            ('path', re.compile(r'[\w\.\-\_]+\/[\w\.\-\/_]+'))
        ]

        for kind, pattern in priority_patterns:
            for match in pattern.finditer(line_text):
                if match.start() <= char <= match.end():
                    return WordInfo(
                        text=match.group(0),
                        range=Range(
                            start=Position(line=pos.line, character=match.start()),
                            end=Position(line=pos.line, character=match.end())
                        ),
                        line_text=line_text,
                        position=pos,
                        kind=kind
                    )

        # 2. Fallback to Generic Word
        for match in TextUtils.RE_GENERIC.finditer(line_text):
            if match.start() <= char <= match.end():
                return WordInfo(
                    text=match.group(0),
                    range=Range(
                        start=Position(line=pos.line, character=match.start()),
                        end=Position(line=pos.line, character=match.end())
                    ),
                    line_text=line_text,
                    position=pos,
                    kind='generic'
                )

        return None

    @staticmethod
    def extract_range(doc: Any, rng: Range) -> str:
        """
        Extracts the text contained within a Range.
        """
        # Single Line
        if rng.start.line == rng.end.line:
            line = doc.get_line(rng.start.line)
            return line[rng.start.character: rng.end.character]

        # Multi Line
        lines = []
        # First line partial
        lines.append(doc.get_line(rng.start.line)[rng.start.character:])

        # Middle lines full
        for i in range(rng.start.line + 1, rng.end.line):
            lines.append(doc.get_line(i))

        # Last line partial
        lines.append(doc.get_line(rng.end.line)[:rng.end.character])

        return "\n".join(lines)

    @staticmethod
    def is_position_in_range(pos: Position, rng: Range) -> bool:
        """Checks if a position falls within a range."""
        if pos.line < rng.start.line or pos.line > rng.end.line:
            return False
        if pos.line == rng.start.line and pos.character < rng.start.character:
            return False
        if pos.line == rng.end.line and pos.character > rng.end.character:
            return False
        return True

    @staticmethod
    def get_indentation(line: str) -> str:
        """Returns the leading whitespace of a line."""
        return line[:len(line) - len(line.lstrip())]

    @staticmethod
    def normalize_newlines(text: str) -> str:
        """Unifies line endings to \n."""
        return text.replace('\r\n', '\n').replace('\r', '\n')

    @staticmethod
    def to_snake_case(text: str) -> str:
        """Transmutes CamelCase to snake_case."""
        name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def to_camel_case(text: str) -> str:
        """Transmutes snake_case to CamelCase."""
        return ''.join(word.title() for word in text.split('_'))

    @staticmethod
    def sanitize_path(path_str: str) -> str:
        """Strips quotes and whitespace from a path string."""
        return path_str.strip().strip("'").strip('"')


# =================================================================================
# == SECTION III: THE STRING ALCHEMIST                                           ==
# =================================================================================

def truncate_middle(text: str, max_len: int) -> str:
    """Intelligently shortens a string by collapsing the center."""
    if len(text) <= max_len:
        return text
    side = (max_len - 3) // 2
    return text[:side] + "..." + text[-side:]


def safe_decode(data: bytes) -> str:
    """
    [THE UNIVERSAL DECODER]
    Attempts UTF-8, falls back to Latin-1. Never fails.
    """
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('latin-1', errors='replace')