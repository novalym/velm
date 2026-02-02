import re
from typing import Tuple
from .base import BaseVowHandler


class ProcessVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF WILL (PROCESS EXECUTION)                                  ==
    =============================================================================
    Judges the outcome of the last Symphony Action (>>).
    """

    def _check_reality(self) -> Tuple[bool, str]:
        if not self.last_reality:
            return False, "No previous action to judge."
        return True, "Reality exists."

    def _vow_succeeds(self) -> Tuple[bool, str]:
        ok, msg = self._check_reality()
        if not ok: return False, msg
        code = self.last_reality.returncode
        return code == 0, f"Rite succeeded (Exit 0)." if code == 0 else f"Rite failed (Exit {code})."

    def _vow_fails(self) -> Tuple[bool, str]:
        ok, msg = self._check_reality()
        if not ok: return False, msg
        code = self.last_reality.returncode
        return code != 0, f"Rite failed as expected (Exit {code})." if code != 0 else "Rite succeeded unexpectedly."

    def _vow_stdout_contains(self, text: str) -> Tuple[bool, str]:
        ok, msg = self._check_reality()
        if not ok: return False, msg
        output = self.last_reality.output
        return text in output, f"Output contains '{text}'." if text in output else f"Output missing '{text}'."

    def _vow_stdout_matches(self, regex: str) -> Tuple[bool, str]:
        ok, msg = self._check_reality()
        if not ok: return False, msg
        return bool(re.search(regex, self.last_reality.output, re.MULTILINE)), f"Output matches /{regex}/."

    def _vow_process_exited_with(self, code: str) -> Tuple[bool, str]:
        ok, msg = self._check_reality()
        if not ok: return False, msg
        try:
            expected = int(code)
            actual = self.last_reality.returncode
            return actual == expected, f"Exit code {actual} == {expected}."
        except ValueError:
            return False, f"Invalid integer code: {code}"
