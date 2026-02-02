# Path: scaffold/artisans/time_branch.py

import subprocess
import shutil
from pathlib import Path

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import TimeBranchRequest
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.kernel.hologram import HolographicEngine
from ..help_registry import register_artisan

@register_artisan("time-branch")
class TimeBranchArtisan(BaseArtisan[TimeBranchRequest]):
    """
    =================================================================================
    == THE FORGER OF TIMELINES (V-Ω-GNOSIC-BRANCHER)                               ==
    =================================================================================
    Conducts the sacred rite of `time-branch`, creating a new reality from an echo
    of the past.
    """

    def execute(self, request: TimeBranchRequest) -> ScaffoldResult:
        self.logger.info(f"The Forger of Timelines awakens. Creating branch '{request.new_branch_name}' from rite '{request.from_rite}'...")

        hologram_engine = HolographicEngine(self.project_root)

        # 1. Gaze upon Git
        if not (self.project_root / ".git").is_dir():
            raise ArtisanHeresy("This rite requires a Git sanctum.")

        # 2. Forge the New Branch
        try:
            subprocess.run(["git", "checkout", "-b", request.new_branch_name], cwd=self.project_root, check=True, capture_output=True)
            self.logger.success(f"New timeline '{request.new_branch_name}' has been forged.")
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"Could not forge new branch: {e.stderr.decode()}", child_heresy=e)

        # 3. Materialize the Past
        self.logger.info("Materializing the past reality onto the new timeline...")
        # This new method on the HologramEngine will handle the full materialization.
        files_materialized = hologram_engine.materialize_to_path(request.from_rite, self.project_root)

        if files_materialized == 0:
            return self.failure("No files were materialized from the past rite. The new branch is a reflection of the void.")

        # 4. Commit the New Genesis
        self.logger.info("Committing the resurrected reality as the first scripture of the new timeline...")
        try:
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True)
            commit_msg = f"feat: Gnostic branch from rite '{request.from_rite}'"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.project_root, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
             raise ArtisanHeresy(f"Failed to commit the new genesis: {e.stderr.decode()}", child_heresy=e)

        return self.success(
            f"Gnostic Branching complete. Timeline '{request.new_branch_name}' is now active.",
            data={"files_materialized": files_materialized}
        )