# path: scaffold/artisans/save_artisan.py

import subprocess
import time
from pathlib import Path

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import SaveRequest
from ..help_registry import register_artisan
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.ai.engine import AIEngine
from rich.prompt import Confirm


@register_artisan("save")
class SaveArtisan(BaseArtisan[SaveRequest]):
    """The Neural Scribe for intent-driven commits."""

    MAX_HEALING_ATTEMPTS = 3

    def execute(self, request: SaveRequest) -> ScaffoldResult:
        self.logger.info("The Neural Scribe awakens...")

        # 1. The Gaze of Change
        diff = self._get_diff()
        if not diff:
            return self.success("No changes to save. The timeline is pure.")

        # 2. The Gnostic Plea to the AI
        ai_engine = AIEngine.get_instance()
        prompt = (
            f"User Intent: \"{request.intent}\"\n\n"
            f"Git Diff:\n```diff\n{diff}\n```\n\n"
            "Generate a concise, conventional commit message for these changes."
        )
        system_prompt = "You are an expert at writing conventional commit messages (e.g., feat(scope): message)."

        with self.console.status("[magenta]The Neural Scribe is communing with the Cortex...[/magenta]"):
            commit_message = ai_engine.ignite(prompt, system_prompt, model="smart")

        # 3. The Rite of Adjudication
        self.console.print("[bold cyan]Neural Scribe's Prophecy:[/bold cyan]")
        self.console.print(f"[green]Commit Message:[/green] {commit_message}")
        if not request.force and not Confirm.ask("\n[bold question]Is this your will?[/bold question]", default=True):
            return self.success("Rite of Saving was stayed by the Architect.")

        # 4. The Self-Healing Loop
        for attempt in range(self.MAX_HEALING_ATTEMPTS):
            # A. Pre-Flight Inquest (Tests)
            self.logger.info(f"Conducting pre-flight inquest (Tests)... Attempt {attempt + 1}")
            test_ok, test_output = self._run_tests()
            if test_ok:
                self.logger.success("Tests are pure. Proceeding with final inscription.")
                self._git_commit_and_push(commit_message)
                return self.success("The Great Work has been inscribed into the eternal chronicle.")

            # B. Self-Healing
            self.logger.error(f"Test inquest failed. Awakening the Self-Healing Cortex...")
            self.console.print(f"[bold red]Test Failure:[/bold red]\n{test_output[-1000:]}")

            healing_prompt = (
                f"The tests failed with the following error:\n```\n{test_output}\n```\n\n"
                f"The original intent was: \"{request.intent}\"\n\n"
                f"Here is the code diff that caused the failure:\n```diff\n{diff}\n```\n\n"
                "Generate a patch in `diff` format to fix the code so the tests will pass. "
                "Output ONLY the raw patch content, starting with 'diff --git ...'."
            )

            with self.console.status("[magenta]The Healing Cortex is forging a cure...[/magenta]"):
                patch = ai_engine.ignite(healing_prompt, system="You are an expert debugger and code fixer.",
                                         model="smart")

            if not patch.strip().startswith("diff --git"):
                return self.failure("The Healing Cortex failed to forge a valid patch. Aborting.")

            self.logger.info("Applying the healing patch...")
            try:
                subprocess.run(['git', 'apply', '-'], input=patch, text=True, check=True, cwd=self.project_root)
                diff = self._get_diff()  # Recalculate diff after patch
            except subprocess.CalledProcessError:
                return self.failure("The healing patch was profane and could not be applied. Aborting.")

        return self.failure(
            f"Self-healing failed after {self.MAX_HEALING_ATTEMPTS} attempts. Please intervene manually.")

    def _get_diff(self) -> str:
        """Perceives staged changes, falling back to all changes."""
        try:
            staged_diff = subprocess.check_output(['git', 'diff', '--staged'], text=True, cwd=self.project_root)
            if staged_diff.strip():
                return staged_diff

            # If nothing is staged, stage everything and get the diff
            subprocess.run(['git', 'add', '.'], cwd=self.project_root, check=True)
            return subprocess.check_output(['git', 'diff', '--staged'], text=True, cwd=self.project_root)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ArtisanHeresy("Could not read Git state. Is this a Git repository?")

    def _run_tests(self) -> tuple[bool, str]:
        """A Gnostic Gaze to find and run the project's test suite."""
        # This would use the prophecy oracle in a real implementation
        if (self.project_root / "package.json").exists():
            cmd = "npm test"
        elif (self.project_root / "pyproject.toml").exists():
            cmd = "poetry run pytest"
        else:
            return True, "No known test suite found."  # Pass if no tests

        try:
            result = subprocess.run(shlex.split(cmd), cwd=self.project_root, check=True, capture_output=True, text=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stdout + e.stderr

    def _git_commit_and_push(self, message: str):
        subprocess.run(['git', 'commit', '-m', message], cwd=self.project_root, check=True)
        subprocess.run(['git', 'push'], cwd=self.project_root, check=True)