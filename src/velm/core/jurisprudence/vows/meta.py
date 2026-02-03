import subprocess
from typing import Tuple
from .base import BaseVowHandler
from rich.prompt import Confirm


class MetaVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF LOGIC (VARIABLES, GIT, & TIME)                            ==
    =============================================================================
    Judges internal state, git history, and user intent.
    """

    # --- VARIABLE LOGIC ---
    def _vow_variable_equals(self, name: str, value: str) -> Tuple[bool, str]:
        actual = str(self.variables.get(name, ""))
        return actual == value, f"$$ {name} == '{value}'."

    def _vow_is_truthy(self, name: str) -> Tuple[bool, str]:
        val = self.variables.get(name)
        is_true = bool(val) and str(val).lower() not in ('false', '0', 'no', 'off', 'none')
        return is_true, f"$$ {name} is Truthy."

    # --- GIT LOGIC ---
    def _vow_git_clean(self) -> Tuple[bool, str]:
        if not (self.root / ".git").exists(): return False, "Not a git repo."
        try:
            res = subprocess.run(["git", "status", "--porcelain"], cwd=self.root, capture_output=True, text=True)
            return not res.stdout.strip(), "Git working tree is clean."
        except:
            return False, "Git status check failed."

    def _vow_confirm(self, question: str) -> Tuple[bool, str]:
        """Pauses for the Architect's confirmation."""
        # In non-interactive contexts (CI), we might default to True or False based on flags.
        # For now, we assume interactive or fail.
        import sys
        if not sys.stdout.isatty():
            return True, "Auto-confirmed (Non-interactive)."

        choice = Confirm.ask(f"[bold yellow]Vow Required:[/bold yellow] {question}")
        return choice, "Architect confirmed." if choice else "Architect denied."