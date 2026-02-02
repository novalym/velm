# Gnostic Codex: scaffold/core/kernel/chronicle/provenance_scribe.py
# ------------------------------------------------------------------
# LIF: ∞ (ETERNAL & ABSOLUTE)
#
# HERESY ANNIHILATED: The Heresy of the Unborn Timeline
#
# The `_get_git_info` rite has been bestowed with its final, divine wisdom. It no
# longer merely checks for the existence of a `.git` directory; it now performs the
# sacred Gaze of the First Scripture, asking the Git Oracle if a timeline has
# actually been born (i.e., if any commits exist).
#
# ASCENSION:
# 1. It now uses `git rev-parse --verify HEAD` in a shielded subprocess call.
# 2. This is the canonical method to check for the existence of at least one commit.
# 3. If this sacred plea fails, the Scribe understands that the timeline is a void
#    and righteously stays its hand in SILENCE.
#
# The profane "Git Gaze faltered" warning during initial project creation is now
# annihilated from all timelines, for all eternity. The Gnosis is pure.

import getpass
import shutil
import platform
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

from .... import __version__
from ....contracts.heresy_contracts import Heresy
from ....logger import Scribe

Logger = Scribe("ProvenanceScribe")


class ProvenanceScribe:
    """
    =================================================================================
    == THE FORENSIC HISTORIAN (V-Ω-ETERNAL-APOTHEOSIS-WISE)                        ==
    =================================================================================
    The divine oracle for the "Who, What, When, Where, and Why" of every rite. It
    now possesses the Gaze of the First Scripture, understanding the difference
    between an empty sanctum and an unwritten history.
    =================================================================================
    """

    def __init__(self, rite_name: str, blueprint_path: Path, project_root: Path, **kwargs):
        self.rite_name = rite_name
        self.blueprint_path = blueprint_path
        self.project_root = project_root
        self.start_time = time.monotonic()

        self.edicts_executed: List[str] = kwargs.get("edicts_executed", [])
        self.heresies_perceived: List[Heresy] = kwargs.get("heresies_perceived", [])

    def _get_git_info(self) -> Tuple[Optional[str], Optional[str]]:
        """Ascension IV: The Gaze of the First Scripture."""
        # --- THE GAZE OF PRUDENCE (V2) ---
        # We first check if the .git directory and the git command exist.
        if not (self.project_root / ".git").is_dir() or not shutil.which("git"):
            return None, None

        try:
            # --- THE GAZE OF THE FIRST SCRIPTURE ---
            # We now ask the one true question: "Has any history been written?"
            # `git rev-parse --verify HEAD` will fail with a non-zero exit code if no commits exist.
            # We suppress its output entirely, caring only for its success or failure.
            subprocess.run(
                ['git', 'rev-parse', '--verify', 'HEAD'],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )

            # If we reach here, a commit exists. Now we can safely perceive the timeline.
            Logger.verbose("Gazing into the Git timeline...")
            commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
            ).strip()
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
            ).strip()
            Logger.verbose(f"Git Gnosis perceived: Branch='{branch}', Commit='{commit[:7]}'")
            return commit, branch
        except (subprocess.CalledProcessError, FileNotFoundError):
            # This path now correctly and silently handles two cases:
            # 1. A repo with `git init` but no commits.
            # 2. A true failure of the git command (e.g., corrupted repo).
            # In both cases, silence is the righteous path. We do not warn.
            return None, None

    def forge_dossier(self, rite_stats: Dict, gnosis_map: Dict, old_gnosis: Dict) -> Tuple[Dict, Dict]:
        """
        The Grand Rite of Provenance Forging.
        Returns the `provenance` and `gnosis_delta` dictionaries.
        """
        commit_hash, branch_name = self._get_git_info()
        duration = time.monotonic() - self.start_time

        variable_delta = {}
        for key, value in gnosis_map.items():
            if key not in old_gnosis or old_gnosis[key] != value:
                if any(s in key.lower() for s in ['secret', 'token', 'password', 'key']):
                    variable_delta[key] = "[REDACTED_BY_PROVENANCE_SCRIBE]"
                else:
                    variable_delta[key] = value

        provenance = {
            "scaffold_version": __version__,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "architect": getpass.getuser(),
            "machine_id": platform.node(),
            "rite_name": self.rite_name,
            "rite_duration_seconds": round(duration, 4),
            "rite_stats": rite_stats,
            "blueprint_path": self.blueprint_path.as_posix(),
            "rite_id": str(uuid.uuid4()),
            "git_commit": commit_hash,
            "git_branch": branch_name,
        }

        return provenance, variable_delta