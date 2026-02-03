# scaffold/artisans/distill/core/inquisitor/temporal.py

import subprocess
import re
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel

from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("TemporalInquisitor")


class RegressionDossier(BaseModel):
    commit_hash: str
    author: str
    date: str
    message: str
    affected_files: list[str]
    diff: str


class TemporalInquisitor:
    """
    =============================================================================
    == THE TEMPORAL INQUISITOR (V-Ω-GIT-BISECT-AUTOMATOR)                      ==
    =============================================================================
    LIF: 10,000,000,000

    Automates the 'git bisect' rite to pinpoint the exact moment a heresy
    entered the timeline.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    def hunt(self, test_command: str, good_ref: str, bad_ref: str = "HEAD") -> Optional[RegressionDossier]:
        """
        Conducts the Bisect Rite.
        """
        Logger.info(f"Initiating Temporal Hunt between '{good_ref}' (Good) and '{bad_ref}' (Bad)...")

        try:
            # 1. Start Bisect
            self._git(["bisect", "start"])
            self._git(["bisect", "bad", bad_ref])
            self._git(["bisect", "good", good_ref])

            # 2. Run Automation
            # We use 'git bisect run' with the provided shell command
            Logger.info(f"Running automated inquest: [yellow]{test_command}[/yellow]")

            # git bisect run expects the command to return 0 for good, 1-127 for bad (except 125)
            # We wrap the command to ensure robust exit codes if needed,
            # but usually the user provided command works (e.g. pytest).

            proc = subprocess.run(
                ["git", "bisect", "run", "sh", "-c", test_command],
                cwd=self.root,
                capture_output=True,
                text=True
            )

            # 3. Analyze Result
            if "is the first bad commit" in proc.stdout:
                match = re.search(r"([a-f0-9]+) is the first bad commit", proc.stdout)
                if match:
                    bad_commit = match.group(1)
                    return self._forge_dossier(bad_commit)

            Logger.warn("The Temporal Inquest was inconclusive.")
            return None

        except Exception as e:
            Logger.error(f"Temporal Inquest failed: {e}")
            return None
        finally:
            self._git(["bisect", "reset"])

    def _git(self, args: list[str]) -> str:
        res = subprocess.run(["git"] + args, cwd=self.root, capture_output=True, text=True, check=True)
        return res.stdout.strip()

    def _forge_dossier(self, commit_hash: str) -> RegressionDossier:
        """Extracts the soul of the bad commit."""
        Logger.success(f"Regression identified at: [red]{commit_hash[:7]}[/red]")

        # Get Metadata
        info = self._git(["show", "-s", "--format=%an|%ad|%s", commit_hash]).split("|")

        # Get Changed Files
        files = self._git(["show", "--name-only", "--format=", commit_hash]).splitlines()

        # Get Diff
        diff = self._git(["show", commit_hash])

        return RegressionDossier(
            commit_hash=commit_hash,
            author=info[0],
            date=info[1],
            message=info[2],
            affected_files=[f.strip() for f in files if f.strip()],
            diff=diff
        )