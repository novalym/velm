# path: scaffold/artisans/holograph_artisan.py

import os
import sys
import json
import platform
import shutil
import subprocess
from pathlib import Path

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import HolographRequest
from ..help_registry import register_artisan
from ..utils import atomic_write
from .. import __version__


@register_artisan("holograph")
class HolographArtisan(BaseArtisan[HolographRequest]):
    """
    =================================================================================
    == THE KEEPER OF THE HOLOGRAM (V-Ω-ENVIRONMENT-IMPRINT)                        ==
    =================================================================================
    Captures the complete Gnostic signature of the current reality for perfect
    reproducibility and forensic analysis.
    """

    def execute(self, request: HolographRequest) -> ScaffoldResult:
        self.logger.info("The Keeper of the Hologram awakens its Gaze...")

        hologram = {
            "schema_version": "1.0",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "scaffold_version": __version__,
            "environment": self._get_env_vars(),
            "platform": self._get_platform_info(),
            "tools": self._get_tool_versions(),
            "libraries": self._get_library_versions()
        }

        output_path = self.project_root / (request.output or "hologram.json")
        atomic_write(output_path, json.dumps(hologram, indent=2), self.logger, self.project_root)

        return self.success(f"Environment Hologram inscribed at '{output_path.name}'.")

    def _get_env_vars(self) -> dict:
        """Captures relevant environment variables."""
        return {
            key: val for key, val in os.environ.items()
            if key.startswith("SCAFFOLD_") or key in ["PATH", "PYTHONPATH"]
        }

    def _get_platform_info(self) -> dict:
        """Captures OS details."""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
        }

    def _get_tool_versions(self) -> dict:
        """Captures versions of critical CLI tools."""
        tools = ["git", "docker", "node", "npm", "python", "poetry", "go", "rustc"]
        versions = {}
        for tool in tools:
            if shutil.which(tool):
                try:
                    version_flag = "--version"
                    if tool == "go": version_flag = "version"

                    output = subprocess.check_output([tool, version_flag], text=True, stderr=subprocess.STDOUT)
                    # Extract first line for cleaner output
                    versions[tool] = output.splitlines()[0].strip()
                except Exception:
                    versions[tool] = "present_but_unversioned"
        return versions

    def _get_library_versions(self) -> dict:
        """Captures project-specific library versions."""
        libs = {}
        # Pip
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            libs["pip"] = req_file.read_text().splitlines()

        # Npm
        pkg_lock = self.project_root / "package-lock.json"
        if pkg_lock.exists():
            try:
                data = json.loads(pkg_lock.read_text())
                libs["npm"] = {name: info.get("version") for name, info in data.get("packages", {}).items() if name}
            except:
                pass

        return libs