# Path: scaffold/artisans/self_test.py
# ------------------------------------

import sys
import shutil
import subprocess
from pathlib import Path
from rich.panel import Panel
from rich.text import Text

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import BaseRequest
from ..help_registry import register_artisan


class SelfTestRequest(BaseRequest):
    """A plea for the Engine to examine its own soul."""
    pass


@register_artisan("self-test")
class SelfTestArtisan(BaseArtisan[SelfTestRequest]):
    """
    @gnosis:title The Mirror of introspection (`self-test`)
    @gnosis:summary Runs a battery of internal integrity tests to verify the Engine's physics.
    """

    def execute(self, request: SelfTestRequest) -> ScaffoldResult:
        self.console.rule("[bold magenta]The Rite of Self-Verification[/bold magenta]")

        sandbox = self.project_root / ".scaffold" / "proving_ground"
        if sandbox.exists():
            shutil.rmtree(sandbox)
        sandbox.mkdir(parents=True, exist_ok=True)

        tests = [
            self._test_genesis,
            self._test_append_mutation,
            self._test_regex_transfiguration
        ]

        success_count = 0

        for test in tests:
            test_name = test.__name__.replace("_test_", "").replace("_", " ").title()
            self.console.print(f"\n[bold cyan]Running Test: {test_name}...[/bold cyan]")
            try:
                test(sandbox)
                self.console.print(f"[green]✔ PASS[/green]")
                success_count += 1
            except Exception as e:
                self.console.print(f"[red]✘ FAIL: {e}[/red]")
                return self.failure(f"Self-Test failed at '{test_name}'")

        # Cleanup
        if sandbox.exists():
            shutil.rmtree(sandbox)

        return self.success(f"All {success_count} internal rites passed. The Engine is pure.")

    def _test_genesis(self, sandbox: Path):
        """Verifies we can create files."""
        blueprint = sandbox / "genesis.scaffold"
        blueprint.write_text('src/main.py :: "print(1)"', encoding='utf-8')

        self._invoke(["run", str(blueprint), "--root", str(sandbox), "--force"])

        if not (sandbox / "src" / "main.py").exists():
            raise Exception("Genesis failed to materialize file.")

    def _test_append_mutation(self, sandbox: Path):
        """Verifies the += operator."""
        # 1. Seed
        target = sandbox / "append_target.py"
        target.write_text("original\n", encoding='utf-8')

        # 2. Patch
        patch = sandbox / "append.patch.scaffold"
        patch.write_text('append_target.py += "appended"', encoding='utf-8')

        # 3. Execute
        self._invoke(["patch", str(patch), "--root", str(sandbox), "--force"])

        # 4. Verify
        content = target.read_text(encoding='utf-8')
        if "original" not in content or "appended" not in content:
            raise Exception(f"Append failed. Content: {content!r}")

    def _test_regex_transfiguration(self, sandbox: Path):
        """Verifies the ~= operator."""
        # 1. Seed
        target = sandbox / "transform_target.txt"
        target.write_text("Hello World", encoding='utf-8')

        # 2. Patch
        patch = sandbox / "transform.patch.scaffold"
        patch.write_text('transform_target.txt ~= s/World/Cosmos/', encoding='utf-8')

        # 3. Execute
        self._invoke(["patch", str(patch), "--root", str(sandbox), "--force"])

        # 4. Verify
        content = target.read_text(encoding='utf-8')
        if "Hello Cosmos" not in content:
            raise Exception(f"Transfiguration failed. Content: {content!r}")

    def _invoke(self, args: list):
        """Invokes the engine as a subprocess to ensure isolation."""
        # We rely on the current sys.executable to run the module
        cmd = [sys.executable, "-m", "scaffold"] + args
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        if res.returncode != 0:
            raise Exception(f"Subprocess failed:\n{res.stderr}")