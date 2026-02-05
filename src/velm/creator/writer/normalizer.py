# Path: scaffold/creator/writer/normalizer.py
# -------------------------------------------
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Final, Optional
from enum import Enum, auto


class LineEnding(Enum):
    """The Gnostic denominations of line termination."""
    LF = "\n"
    CRLF = "\r\n"


class TabPolicy(Enum):
    """The Sacred Laws governing indentation."""
    FORCE_TABS = auto()  # Makefiles, Go
    FORCE_SPACES = auto()  # Python, YAML
    PRESERVE = auto()  # Generic text


class ContentNormalizer:
    """
    =================================================================================
    == THE ALCHEMIST OF FORM (V-Ω-TEXT-NORMALIZER-ULTIMA)                          ==
    =================================================================================
    LIF: INFINITY | ROLE: FORM_PURIFIER | RANK: OMEGA_SUPREME

    The Sovereign Artisan responsible for the geometric and physical sanctification
    of content. It ensures that the 'Ink' of the code honors the 'Will' of the
    Architecture across all Operating System boundaries.
    """

    # [ASCENSION 1 & 8]: The Grimoire of Impurities
    # Strips BOMs, Nulls, and other profane characters.
    IMPURITY_REGEX: Final[re.Pattern] = re.compile(r"[\x00\ufeff\u200b\u200c\u200d]")

    # [ASCENSION 3]: The Trailing Space Scribe
    TRAILING_WHITESPACE_REGEX: Final[re.Pattern] = re.compile(r"[ \t]+$", re.MULTILINE)

    def __init__(self, is_windows: bool = False):
        """
        Initializes the Alchemist.
        :param is_windows: If True, the engine will adopt the CRLF denomination.
        """
        self.is_windows = is_windows
        self.target_eol = LineEnding.CRLF if is_windows else LineEnding.LF

    def sanctify(self, path: Path, content: str) -> str:
        """
        The Grand Rite of Normalization.
        Conducts the content through the Twelve Lustrations.
        """
        if not content:
            return ""

        # --- LUSTRATION I: THE VOW OF PURITY ---
        # Strip null bytes and BOMs that profane the scripture.
        purified = self.IMPURITY_REGEX.sub("", content)

        # --- LUSTRATION II: THE RITE OF THE UNIFIED EOL ---
        # First, normalize all endings to LF for internal processing.
        purified = purified.replace("\r\n", "\n").replace("\r", "\n")

        # --- LUSTRATION III: THE GEOMETRIC SCRUB ---
        # Remove trailing whitespace that creates metabolic noise.
        purified = self.TRAILING_WHITESPACE_REGEX.sub("", purified)

        # --- LUSTRATION IV: THE ADJUDICATION OF THE TONGUE ---
        # Determine the indentation policy based on the scripture's extension.
        policy = self._divine_tab_policy(path)

        if policy == TabPolicy.FORCE_TABS:
            purified = self._enforce_tabs(purified)
        elif policy == TabPolicy.FORCE_SPACES:
            purified = self._enforce_spaces(purified)

        # --- LUSTRATION V: THE FINALITY VOW ---
        # Ensure the scripture ends with exactly one newline.
        purified = purified.rstrip("\n") + "\n"

        # --- LUSTRATION VI: THE OS TRANSMUTATION ---
        # Convert to the target OS format (LF or CRLF).
        if self.target_eol == LineEnding.CRLF:
            purified = purified.replace("\n", "\r\n")

        return purified

    def _divine_tab_policy(self, path: Path) -> TabPolicy:
        """Determines the indentation law for the given path."""
        name = path.name.lower()
        ext = path.suffix.lower()

        # The Law of the Makefile
        if name == "makefile" or ext == ".mk":
            return TabPolicy.FORCE_TABS

        # The Law of Go
        if ext == ".go":
            return TabPolicy.FORCE_TABS

        # The Law of Python and YAML
        if ext in (".py", ".yaml", ".yml", ".json"):
            return TabPolicy.FORCE_SPACES

        return TabPolicy.PRESERVE

    def _enforce_tabs(self, content: str) -> str:
        """
        [ASCENSION 2] The Tabular Oracle.
        Forces Tabs for recipes, but respects leading spaces for prose.
        """
        lines = content.splitlines()
        out = []

        # Matches 2-8 spaces at start of line
        indent_regex = re.compile(r"^( {2,8})")

        for line in lines:
            if not line.strip():
                out.append("")
                continue

            # If it looks like a recipe (indented), force tab
            if indent_regex.match(line):
                out.append("\t" + line.lstrip(' '))
            else:
                out.append(line)

        return "\n".join(out)

    def _enforce_spaces(self, content: str, indent_size: int = 4) -> str:
        """
        [ASCENSION 7] The Space Alchemist.
        Transmutes illegal tabs into space-based indentation.
        """
        lines = content.splitlines()
        out = []

        spaces = " " * indent_size

        for line in lines:
            if "\t" in line:
                # We replace leading tabs specifically to preserve tabs inside strings
                # (though tabs inside strings are a stylistic heresy regardless).
                leading_tabs = len(line) - len(line.lstrip('\t'))
                if leading_tabs > 0:
                    line = (spaces * leading_tabs) + line.lstrip('\t')
            out.append(line)

        return "\n".join(out)

    def __repr__(self) -> str:
        return f"<AlchemistOfForm mode={'WINDOWS' if self.is_windows else 'POSIX'}>"