import re
from typing import Tuple
from .base import BaseVowHandler


class QualityVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE GUARDIAN OF HYGIENE (V-Ω-CODE-QUALITY)                              ==
    =============================================================================
    Enforces architectural purity, brevity, and cleanliness within source code.
    """

    def _vow_no_todos(self, path: str) -> Tuple[bool, str]:
        """
        Asserts a scripture contains no 'TODO' or 'FIXME' markers.
        Use this to prevent unfinished thoughts from entering production.
        """
        target = self._resolve(path)
        if not target.is_file(): return False, "Void path."

        content = target.read_text(encoding='utf-8', errors='ignore')
        matches = re.findall(r'(TODO|FIXME|XXX):?', content)

        if matches:
            return False, f"Heresy: Found {len(matches)} unfinished thought(s) ({matches[0]})."
        return True, "Scripture is complete (No TODOs)."

    def _vow_encoding_is_utf8(self, path: str) -> Tuple[bool, str]:
        """Asserts the file is valid UTF-8 without BOM."""
        target = self._resolve(path)
        try:
            raw = target.read_bytes()
            raw.decode('utf-8', errors='strict')
            if raw.startswith(b'\xef\xbb\xbf'):
                return False, "Heresy: UTF-8 BOM detected."
            return True, "Soul is pure UTF-8."
        except UnicodeDecodeError:
            return False, "Heresy: Invalid UTF-8 sequence."

    def _vow_line_count_lt(self, path: str, limit: str) -> Tuple[bool, str]:
        """
        Asserts the file is not a monolith.
        """
        target = self._resolve(path)
        lines = 0
        try:
            with open(target, 'rb') as f:
                lines = sum(1 for _ in f)

            limit_int = int(limit)
            return lines < limit_int, f"Line count {lines} < {limit_int}."
        except Exception:
            return False, "Could not count lines."

    def _vow_indentation_is_spaces(self, path: str) -> Tuple[bool, str]:
        """
        [THE TAB CRUSADE]
        Asserts the file does not contain tab characters for indentation.
        """
        target = self._resolve(path)
        content = target.read_text(encoding='utf-8', errors='ignore')
        if '\t' in content:
            return False, "Heresy: Tab characters detected."
        return True, "Indentation is pure (Spaces)."

    def _vow_has_shebang(self, path: str, interpreter: str) -> Tuple[bool, str]:
        """Asserts the file starts with a specific shebang."""
        target = self._resolve(path)
        with open(target, 'r') as f:
            first_line = f.readline().strip()

        expected = f"#!{interpreter}"
        if first_line.startswith(expected) or expected in first_line:
            return True, f"Shebang '{first_line}' detected."
        return False, f"Shebang missing or incorrect. Found: '{first_line}'"