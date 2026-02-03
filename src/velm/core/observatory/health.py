# Path: scaffold/core/observatory/health.py
# -----------------------------------------
import os
import subprocess
import shutil
from pathlib import Path
from typing import Tuple
from .contracts import ProjectHealth, ProjectMetadata, ProjectType

class VitalityMonitor:
    """
    Diagnoses the health and metadata of a project.
    """

    @staticmethod
    def check_pulse(path: Path) -> Tuple[ProjectHealth, ProjectMetadata]:
        meta = ProjectMetadata()

        # 1. Existence Check
        if not path.exists():
            return ProjectHealth.GHOST, meta

        # 2. Git Gaze
        if (path / ".git").exists() and shutil.which("git"):
            try:
                # Get Branch
                branch = subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=path, text=True, stderr=subprocess.DEVNULL
                ).strip()
                meta.git_branch = branch

                # Get Remote
                try:
                    remote = subprocess.check_output(
                        ["git", "config", "--get", "remote.origin.url"],
                        cwd=path, text=True, stderr=subprocess.DEVNULL
                    ).strip()
                    meta.git_remote = remote
                except:
                    pass

                # Check Status
                status = subprocess.check_output(
                    ["git", "status", "--porcelain"],
                    cwd=path, text=True, stderr=subprocess.DEVNULL
                ).strip()
                health = ProjectHealth.DIRTY if status else ProjectHealth.HEALTHY
            except:
                health = ProjectHealth.HEALTHY  # Git exists but maybe no commits yet
        else:
            health = ProjectHealth.HEALTHY

        # 3. Deep Metadata Extraction
        # (Here we could parse pyproject.toml for version, etc.)

        return health, meta