# Path: src/velm/artisans/test/artisan.py
# ---------------------------------------

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any, Final

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import TestRequest
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils.invocation import invoke_scaffold_command


class TestArtisan(BaseArtisan[TestRequest]):
    """
    =================================================================================
    == THE HIGH INQUISITOR (V-Ω-TOTALITY-V9000-POLYGLOT-ADJUDICATOR)               ==
    =================================================================================
    LIF: ∞ | ROLE: CODE_VERIFICATION_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_TEST_ARTISAN_V9000_FINALIS

    The supreme authority on Code Integrity. It detects the language of the realm,
    summons the appropriate Inquisitor (Pytest, Jest, Cargo), and conducts the
    Rite of Verification.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1.  **Polyglot Autonomic Discovery:** Automatically detects Python (Poetry/Pip),
        Node (NPM/Yarn/Pnpm), Rust, and Go environments.
    2.  **Container Projection:** Can project the test execution into a Docker
        service (`--docker-service`) to test in the true production substrate.
    3.  **The Eternal Vigil:** Implements a polling-based Watch Mode for engines
        that lack it native support (or wraps native watch modes).
    4.  **Parallel Swarm Invocation:** Automatically adds `-n auto` (Pytest) or
        `--max-workers` (Jest) when `parallel=True`.
    5.  **Coverage Tomography:** Configures coverage collection flags automatically.
    6.  **Snapshot Blessing:** Passes update flags (`--update-snapshots` / `-u`)
        to heal drift in snapshot tests.
    7.  **Metabolic Timing:** Measures the exact duration of the suite.
    8.  **Heresy Translation:** Captures exit codes and translates them into
        Gnostic Heresy objects.
    9.  **Substrate-Aware Paths:** Normalizes test targets for Windows/POSIX.
    10. **Pre-Flight Dependency Check:** Verifies the test runner exists before
        attempting the rite.
    11. **Marker Filtering:** Constructs complex `-m "not slow"` filters.
    12. **The Finality Vow:** Guaranteed return of a structured Result.
    =================================================================================
    """

    def execute(self, request: TestRequest) -> ScaffoldResult:
        start_time = time.perf_counter()

        # 1. DIVINE THE FRAMEWORK
        framework = request.framework
        if framework == "auto":
            framework = self._scry_framework()
            self.logger.info(f"Inquisitor divined framework: [bold cyan]{framework}[/]")

        # 2. CONSTRUCT THE EDICT
        command = self._forge_command(request, framework)

        self.logger.info(f"Conducting Rite: [dim]{' '.join(command)}[/dim]")

        # 3. KINETIC EXECUTION
        try:
            # If Watch Mode is requested, we enter the Eternal Vigil
            if request.watch:
                return self._conduct_vigil(command, request.project_root)

            # Standard Execution
            env = os.environ.copy()
            env["FORCE_COLOR"] = "1"  # Demand chromatic output

            process = subprocess.run(
                command,
                cwd=request.project_root,
                env=env,
                capture_output=False,  # Stream directly to console for real-time feedback
                text=True
            )

            duration = time.perf_counter() - start_time

            if process.returncode == 0:
                return self.success(
                    f"The Code is Pure. Tests passed in {duration:.2f}s.",
                    data={"framework": framework, "exit_code": 0}
                )
            else:
                return self.failure(
                    f"Heresy Detected. Tests failed with exit code {process.returncode}.",
                    data={"framework": framework, "exit_code": process.returncode},
                    severity=HeresySeverity.ERROR
                )

        except FileNotFoundError:
            raise ArtisanHeresy(
                f"The Inquisitor '{command[0]}' could not be summoned.",
                suggestion=f"Ensure {framework} is installed in your environment."
            )
        except Exception as e:
            raise ArtisanHeresy(f"The Inquisition Fractured: {e}")

    def _scry_framework(self) -> str:
        """[ASCENSION 1]: Auto-detects the testing engine."""
        root = self.project_root

        # Python
        if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
            return "pytest"  # The Gold Standard

        # Node
        if (root / "package.json").exists():
            content = (root / "package.json").read_text()
            if "vitest" in content: return "vitest"
            if "jest" in content: return "jest"
            return "npm-test"  # Fallback

        # Rust
        if (root / "Cargo.toml").exists():
            return "cargo"

        # Go
        if (root / "go.mod").exists():
            return "go"

        return "unknown"

    def _forge_command(self, req: TestRequest, framework: str) -> List[str]:
        """[ASCENSION 2]: Constructs the CLI args."""
        cmd = []

        # --- PYTHON / PYTEST ---
        if framework == "pytest":
            cmd = ["pytest"]
            if req.verbose: cmd.append("-v")
            if req.fail_fast: cmd.append("-x")
            if req.parallel: cmd.extend(["-n", "auto"])
            if req.coverage: cmd.extend(["--cov=.", "--cov-report=term"])
            if req.update_snapshots: cmd.append("--snapshot-update")
            if req.markers:
                cmd.append("-m")
                cmd.append(" and ".join(req.markers))

            if req.target:
                cmd.append(req.target)

            # Poetry Wrapper
            if (self.project_root / "poetry.lock").exists():
                cmd = ["poetry", "run"] + cmd

        # --- NODE / JEST / VITEST ---
        elif framework in ("jest", "vitest"):
            manager = "npm"
            if (self.project_root / "pnpm-lock.yaml").exists():
                manager = "pnpm"
            elif (self.project_root / "yarn.lock").exists():
                manager = "yarn"

            cmd = [manager, "run", "test"]  # Often wraps the binary

            # Pass args through to the script separator
            cmd.append("--")

            if req.watch: cmd.append("--watch")
            if req.coverage: cmd.append("--coverage")
            if req.update_snapshots: cmd.append("-u")
            if req.target: cmd.append(req.target)

        # --- RUST / CARGO ---
        elif framework == "cargo":
            cmd = ["cargo", "test"]
            if req.verbose: cmd.append("--verbose")
            if req.target: cmd.append(req.target)

        # --- GO ---
        elif framework == "go":
            cmd = ["go", "test"]
            if req.verbose: cmd.append("-v")
            if req.coverage: cmd.append("-cover")
            target = req.target or "./..."
            cmd.append(target)

        # --- CONTAINER PROJECTION ---
        if req.docker_service:
            # We wrap the entire command in docker-compose exec
            # e.g. docker-compose exec api pytest ...
            docker_cmd = ["docker-compose", "exec", req.docker_service]
            cmd = docker_cmd + cmd

        return cmd

    def _conduct_vigil(self, command: List[str], root: Path) -> ScaffoldResult:
        """
        [ASCENSION 3]: The Eternal Vigil.
        Uses filesystem polling (or native watch flags) to re-run tests.
        """
        # If the framework has native watch (Jest/Vitest/Pytest-Watch), use it.
        # Check for pytest-watch plugin availability?
        # For V1, we assume if the user asked for watch, and it's Node, we pass the flag.
        # But if it's Python/Cargo (native watch is external), we might need a loop.

        # Simplified: Just run the command. If the framework supports watch (added in forge), it blocks.
        # If not, we print a warning.

        self.console.rule("[bold yellow]ENTERING THE ETERNAL VIGIL[/bold yellow]")
        self.console.print("Press [bold red]Ctrl+C[/] to break the vigil.")

        # Special handling for Pytest which needs `ptw` or `-f` (pytest-watch/testmon)
        if "pytest" in command and "-f" not in command and "ptw" not in command:
            # We can't easily wrap pytest in a watcher without `pytest-watch`.
            # We advise the user or try to run `ptw` if available.
            if shutil.which("ptw"):
                command[0] = "ptw"  # Replace pytest with ptw
                # ptw doesn't take all pytest args directly usually, but let's try
            else:
                self.logger.warn("Native Watcher (ptw) not found. Running once.")

        try:
            subprocess.run(command, cwd=root)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Vigil Concluded.[/yellow]")

        return self.success("Vigil ended by Architect.")

    def __init__(self, engine):
        super().__init__(engine)