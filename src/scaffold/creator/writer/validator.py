# Path: scaffold/creator/writer/validator.py
# ------------------------------------------
import re
from pathlib import Path
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class PathValidator:
    """
    =============================================================================
    == THE WARD OF FORM (V-Ω-PATH-SANITIZER)                                   ==
    =============================================================================
    A paranoid sentinel that inspects paths for lexical heresies.
    It catches 'Parser Leaks' (code passed as paths) before they touch the OS.
    """

    # Windows-hostile characters + newlines (universal heresy)
    # We explicitly ban quotes because they indicate a parser failure
    PROFANE_CHARS = re.compile(r'[<>:"|?*\n\r]')

    # Code signatures that should never be in a filename
    CODE_SIGNATURES = [
        "def ", "class ", "import ", "return ", "if ", "else", "for ", "while ",
        "{{", "}}", "{%", "%}", "=="
    ]

    @classmethod
    def adjudicate(cls, path: Path) -> None:
        """
        Performs the Gaze of Validity. Raises ArtisanHeresy if the path is profane.
        """
        path_str = str(path)

        # 1. The Gaze of the Forbidden Glyph
        if cls.PROFANE_CHARS.search(path_str):
            raise ArtisanHeresy(
                f"Path Syntax Heresy: The path '{path_str}' contains illegal characters.",
                details="This usually indicates a Parser Leak where content was mistaken for a filename.",
                severity=HeresySeverity.CRITICAL
            )

        # 2. The Gaze of the Hidden Code
        # If the path looks like Python code, the Parser has failed us.
        if any(sig in path_str for sig in cls.CODE_SIGNATURES):
            raise ArtisanHeresy(
                f"Semantic Path Heresy: The path '{path_str}' appears to be source code.",
                details="The Gnostic Parser likely failed to close a block, interpreting code as a file path.",
                severity=HeresySeverity.CRITICAL
            )

        # 3. The Gaze of the Void
        if not path_str or path_str.strip() == ".":
            raise ArtisanHeresy("Void Path Heresy: Cannot write to an empty path.")