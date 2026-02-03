import subprocess
from typing import Tuple
from .base import BaseVowHandler


class GitVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE CHRONICLE OF VERSIONING (GIT)                                       ==
    =============================================================================
    Judges the state of the Source Control timeline.
    """

    def _run_git(self, args: list) -> Tuple[bool, str]:
        """Internal helper for Git commands."""
        if not (self.root / ".git").exists():
            return False, "Not a git repository."
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=self.root,
                capture_output=True,
                text=True
            )
            return res.returncode == 0, res.stdout.strip()
        except Exception as e:
            return False, str(e)

    def _vow_git_branch_is(self, branch_name: str) -> Tuple[bool, str]:
        """Asserts the current HEAD is on a specific branch."""
        ok, output = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if not ok: return False, output
        return output == branch_name, f"Current branch is '{output}'."

    def _vow_git_tag_exists(self, tag_name: str) -> Tuple[bool, str]:
        """Asserts a specific tag exists in the local repo."""
        ok, _ = self._run_git(["rev-parse", tag_name])
        return ok, f"Tag '{tag_name}' {'exists' if ok else 'missing'}."

    def _vow_git_is_clean(self) -> Tuple[bool, str]:
        """Asserts there are no uncommitted changes."""
        ok, output = self._run_git(["status", "--porcelain"])
        if not ok: return False, "Git check failed."
        return output == "", "Working tree is clean." if output == "" else "Working tree is dirty."

    def _vow_git_remote_exists(self, remote_name: str) -> Tuple[bool, str]:
        """Asserts a remote (e.g., 'origin') is configured."""
        ok, output = self._run_git(["remote"])
        remotes = output.splitlines()
        return remote_name in remotes, f"Remote '{remote_name}' {'found' if remote_name in remotes else 'missing'}."

    def _vow_git_has_commits(self) -> Tuple[bool, str]:
        """Asserts the repository is not empty."""
        ok, _ = self._run_git(["rev-parse", "HEAD"])
        return ok, "Repository has history." if ok else "Repository is empty."

    def _vow_git_ignore_check(self, path: str) -> Tuple[bool, str]:
        """Asserts a path is ignored by .gitignore."""
        ok, output = self._run_git(["check-ignore", path])
        return ok, f"'{path}' is ignored." if ok else f"'{path}' is tracked."



