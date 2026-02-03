# Path: scaffold/artisans/weave/ci_weaver.py
# ------------------------------------------

import yaml
from pathlib import Path
from typing import Optional

from ...core.runtime import ScaffoldEngine
from ...interfaces.base import Artifact
from ...utils import atomic_write, get_human_readable_size
from ...contracts.heresy_contracts import ArtisanHeresy


class CIWeaver:
    """
    =============================================================================
    == THE SCRIBE OF CELESTIAL SYMPHONIES                                      ==
    =============================================================================
    A specialist artisan that forges CI/CD pipeline scriptures.
    """

    def __init__(self, engine: ScaffoldEngine):
        self.engine = engine
        self.logger = engine.logger
        self.project_root = engine.project_root

    def weave(self, provider: str, project_type: Optional[str], force: bool) -> Artifact:
        if provider.lower() != 'github':
            raise ArtisanHeresy("Only 'github' is a known celestial realm for CI.")

        # 1. Gnostic Gaze
        if not project_type:
            # Prophecy: A future ascension would auto-detect this.
            # For now, we fall back to a generic template.
            self.logger.warn("No project type specified. Forging a generic CI scripture.")
            project_type = 'generic'

        # 2. Forge Scripture
        workflow_content = self._get_github_workflow(project_type)

        # 3. Inscribe
        workflow_dir = self.project_root / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        target_path = workflow_dir / "scaffold-ci.yml"

        if target_path.exists() and not force:
            raise ArtisanHeresy(
                f"A CI scripture already exists at '{target_path}'.",
                suggestion="Use --force to overwrite."
            )

        write_result = atomic_write(target_path, workflow_content, self.logger, self.project_root)

        return Artifact(
            path=target_path,
            type='file',
            action=write_result.action_taken.value,
            size_bytes=write_result.bytes_written
        )

    def _get_github_workflow(self, project_type: str) -> str:
        """Contains the templates for different pipelines."""
        # This is a simplified version. A full impl would use Jinja templates.

        base_workflow = {
            "name": "Scaffold CI/CD",
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {"build-and-test": {"runs-on": "ubuntu-latest", "steps": []}}
        }

        steps = base_workflow['jobs']['build-and-test']['steps']
        steps.append({"name": "Checkout code", "uses": "actions/checkout@v4"})

        if 'python' in project_type:
            steps.extend([
                {"name": "Set up Python", "uses": "actions/setup-python@v5", "with": {"python-version": "3.11"}},
                {"name": "Install Poetry", "run": "pip install poetry"},
                {"name": "Install dependencies", "run": "poetry install"},
                {"name": "Run tests", "run": "poetry run pytest"}
            ])
        elif 'node' in project_type:
            steps.extend([
                {"name": "Set up Node.js", "uses": "actions/setup-node@v4", "with": {"node-version": "20"}},
                {"name": "Install dependencies", "run": "npm ci"},
                {"name": "Run tests", "run": "npm test"}
            ])
        else:  # Generic
            steps.append({"name": "Echo Build", "run": "echo 'Build and test steps go here'"})

        return yaml.dump(base_workflow, sort_keys=False)