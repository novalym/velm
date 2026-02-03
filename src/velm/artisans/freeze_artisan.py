# path: scaffold/artisans/freeze_artisan.py

import os
import shutil
import subprocess
from pathlib import Path
from typing import List

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import FreezeRequest
from ..help_registry import register_artisan
from ..contracts.heresy_contracts import ArtisanHeresy


@register_artisan("freeze")
class FreezeArtisan(BaseArtisan[FreezeRequest]):
    """
    =================================================================================
    == THE KEEPER OF THE VAULT (V-Ω-DEPENDENCY-TIME-CAPSULE)                         ==
    =================================================================================
    Forges a self-contained, offline-buildable snapshot of all project dependencies.
    """

    def execute(self, request: FreezeRequest) -> ScaffoldResult:
        self.logger.info("The Keeper of the Vault awakens to forge the Time-Capsule...")

        vendor_dir = self.project_root / ".scaffold" / "vendor"
        if vendor_dir.exists() and not request.force:
            raise ArtisanHeresy(
                "A dependency vault already exists.",
                suggestion=f"Purge the existing vault at '{vendor_dir}' or use --force to overwrite."
            )

        vendor_dir.mkdir(parents=True, exist_ok=True)

        self._freeze_pip(vendor_dir)
        self._freeze_npm(vendor_dir)
        # Future ascensions: _freeze_go, _freeze_cargo

        return self.success(f"Dependency Time-Capsule forged at '{vendor_dir}'.")

    def _freeze_pip(self, vendor_dir: Path):
        """Vendors Python dependencies."""
        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            return

        self.logger.info("Freezing Python dependencies...")
        pip_dir = vendor_dir / "pip"
        pip_dir.mkdir(exist_ok=True)

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "download", "-r", str(req_file), "-d", str(pip_dir)],
                check=True, capture_output=True, text=True
            )
            self.logger.success("Python souls have been enshrined.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to freeze pip dependencies: {e.stderr}")

    def _freeze_npm(self, vendor_dir: Path):
        """Vendors Node.js dependencies."""
        pkg_lock = self.project_root / "package-lock.json"
        if not pkg_lock.exists() or not shutil.which("npm"):
            return

        self.logger.info("Freezing Node.js dependencies...")
        npm_dir = vendor_dir / "npm"
        npm_dir.mkdir(exist_ok=True)

        try:
            # npm pack creates .tgz files for all dependencies in the CWD
            subprocess.run(
                ["npm", "pack"],
                cwd=npm_dir,  # Run pack inside the target dir
                check=True, capture_output=True, text=True,
                env={**os.environ, "npm_config_prefix": str(self.project_root)}
            )
            self.logger.success("Node.js souls have been enshrined.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to freeze npm dependencies: {e.stderr}")