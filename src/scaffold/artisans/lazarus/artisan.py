# Path: artisans/lazarus/artisan.py
# ---------------------------------

import subprocess
from rich.panel import Panel
from rich.prompt import Confirm

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import LazarusRequest
from ...help_registry import register_artisan
from ...core.ai.engine import AIEngine
from ...utils import atomic_write
from ...contracts.heresy_contracts import ArtisanHeresy


@register_artisan("resurrect")
class LazarusArtisan(BaseArtisan[LazarusRequest]):
    """
    =================================================================================
    == THE LAZARUS PROTOCOL (V-Ω-SELF-HEALING)                                     ==
    =================================================================================
    LIF: 100,000,000,000

    Iteratively runs code, captures crashes, diagnoses the soul, and patches the body.
    """

    def execute(self, request: LazarusRequest) -> ScaffoldResult:
        if not request.command:
            return self.failure("The Rite of Resurrection requires a command to test (e.g., 'pytest').")

        self.logger.info(f"Initiating Lazarus Protocol for: [yellow]{request.command}[/yellow]")

        # 1. The Diagnosis (Run and Catch)
        exit_code, stdout, stderr = self._run_command(request.command)

        if exit_code == 0:
            return self.success("The patient is healthy. No resurrection needed.")

        self.logger.warn("Crash detected. Analyzing wounds...")
        error_log = stderr + "\n" + stdout

        # 2. The Communion (Ask AI for a Cure)
        ai = AIEngine.get_instance()

        # We need the source code context. We assume the stack trace points to files.
        # For V1, we just pass the error. V2 would parse trace and fetch file content.

        prompt = f"""
        The command `{request.command}` failed with the following output:
        ```
        {error_log[-2000:]} # Last 2000 chars
        ```

        Analyze the error. 
        1. Explain the root cause.
        2. Provide a `diff` patch to fix the code.
        """

        system = "You are an Expert Debugger. You output only the analysis and a valid git diff."

        with self.console.status("[bold magenta]Forging a Cure...[/bold magenta]"):
            diagnosis = ai.ignite(prompt, system, model="smart")

        self.console.print(Panel(diagnosis, title="[green]The Prophecy of Healing[/green]", border_style="green"))

        # 3. The Miracle (Apply Patch)
        # Extract diff block
        import re
        diff_match = re.search(r"```diff\n(.*?)```", diagnosis, re.DOTALL)

        if diff_match:
            diff_content = diff_match.group(1)
            patch_path = self.project_root / ".scaffold" / "lazarus.patch"
            atomic_write(patch_path, diff_content, self.logger, self.project_root)

            if request.auto_apply or Confirm.ask("[bold yellow]Apply this patch?[/bold yellow]"):
                try:
                    subprocess.run(["git", "apply", str(patch_path)], cwd=self.project_root, check=True)
                    self.logger.success("Patch applied.")

                    # Verify
                    code, _, _ = self._run_command(request.command)
                    if code == 0:
                        return self.success("Resurrection Complete. The code lives.",
                                            artifacts=[Artifact(path=patch_path, type="file", action="created")])
                    else:
                        return self.failure("The cure was insufficient. The patient still suffers.")

                except subprocess.CalledProcessError:
                    return self.failure("Failed to apply the patch physically.")

        return self.success("Diagnosis provided.")

    def _run_command(self, cmd: str):
        res = subprocess.run(cmd, shell=True, cwd=self.project_root, capture_output=True, text=True)
        return res.returncode, res.stdout, res.stderr