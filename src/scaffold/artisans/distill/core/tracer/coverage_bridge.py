# === [scaffold/artisans/distill/core/tracer/coverage_bridge.py] - SECTION 1 of 1: The Coverage Wraith ===
import json
import shutil
import subprocess
import os
from pathlib import Path
from typing import Dict, Set, Optional

from .....contracts.heresy_contracts import ArtisanHeresy
from .....logger import Scribe

Logger = Scribe("CoverageWraith")


class CoverageBridge:
    """
    =============================================================================
    == THE DYNAMIC HOLOGRAM (V-Ω-COVERAGE-TRACER)                              ==
    =============================================================================
    Executes a command under the gaze of `coverage.py` and extracts the
    set of executed lines for every file.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self._coverage_cmd = shutil.which("coverage")

    def conduct_rite(self, command: str) -> Dict[str, Set[int]]:
        """
        Executes the command and returns {filepath: {line_numbers}}.
        """
        if not self._coverage_cmd:
            raise ArtisanHeresy(
                "The Coverage Wraith requires 'coverage'.",
                suggestion="pip install coverage"
            )

        Logger.info(f"Initiating Dynamic Hologram Rite: [yellow]{command}[/yellow]")

        # 1. Prepare Sanctum
        # We need a clean coverage file
        cov_file = self.root / ".coverage.scaffold"
        if cov_file.exists(): cov_file.unlink()

        # 2. Execute with Coverage
        # We split the command. e.g. "pytest" -> ["run", "-m", "pytest"]
        # or "python main.py" -> ["run", "main.py"]

        # Heuristic: wrapping the command
        full_cmd = [self._coverage_cmd, "run", f"--data-file={cov_file}"]
        if command.startswith("pytest"):
            full_cmd.extend(["-m", "pytest"] + command.split()[1:])
        elif command.startswith("python"):
            full_cmd.extend(command.split()[1:])
        else:
            # Generic shell command? Hard to wrap.
            raise ArtisanHeresy("Dynamic Focus currently only supports 'python' or 'pytest' commands.")

        try:
            env = os.environ.copy()
            subprocess.run(full_cmd, cwd=self.root, check=True, env=env)
        except subprocess.CalledProcessError as e:
            Logger.warn(f"The test command faltered (Exit {e.returncode}), but we shall harvest the echoes.")

        # 3. Harvest Gnosis (Export to JSON)
        json_report = self.root / ".coverage.json"
        try:
            subprocess.run(
                [self._coverage_cmd, "json", f"--data-file={cov_file}", "-o", str(json_report)],
                cwd=self.root, check=True, stdout=subprocess.DEVNULL
            )

            data = json.loads(json_report.read_text())
            return self._parse_coverage_json(data)

        except Exception as e:
            raise ArtisanHeresy(f"Failed to harvest coverage gnosis: {e}")
        finally:
            # Cleanup
            if cov_file.exists(): cov_file.unlink()
            if json_report.exists(): json_report.unlink()

    def _parse_coverage_json(self, data: Dict) -> Dict[str, Set[int]]:
        """Transmutes raw coverage JSON into the Gnostic Map."""
        mapping = {}
        files = data.get("files", {})

        for filename, info in files.items():
            # Normalize path relative to root
            try:
                # coverage report might have absolute paths
                abs_path = Path(filename)
                if abs_path.is_absolute():
                    rel_path = str(abs_path.relative_to(self.root)).replace('\\', '/')
                else:
                    rel_path = filename

                # "executed_lines" is the key
                lines = set(info.get("executed_lines", []))
                if lines:
                    mapping[rel_path] = lines
            except ValueError:
                continue  # File outside root

        return mapping