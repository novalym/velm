# Path: scaffold/artisans/telepresence/url_projector.py
# ----------------------------------------------------
import os
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import hash_file

Logger = Scribe("URLProjector")


class URLProjector:
    """
    =================================================================================
    == THE CELESTIAL PROJECTOR (V-Ω-URL-INHABITATION-ULTIMA)                       ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: ()@#()#@()#@()

    This artisan manages the projection of remote realities into the local Gnostic
    context. It is the bridge to the Celestial Aether.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        # [FACULTY 1]: The Volatile RAM-Disk Sanctum
        self.mount_root = self.root / ".scaffold" / "mounts"
        self._active_mounts: Dict[str, Path] = {}
        self._lock = threading.Lock()

        if not self.mount_root.exists():
            self.mount_root.mkdir(parents=True, exist_ok=True)

    def mount(self, url: str) -> Dict[str, Any]:
        """
        [THE RITE OF INHABITATION]
        Transmutes a celestial URL into a local virtual project.
        """
        Logger.info(f"Projecting Celestial URL: [cyan]{url}[/cyan]")

        # 1. Divine the Target Name
        target_name = url.split('/')[-1].replace('.git', '')
        mount_point = self.mount_root / target_name

        with self._lock:
            # 2. Check for existing Inhabitation
            if mount_point.exists() and url in self._active_mounts:
                Logger.verbose(f"Re-attaching to existing projection: {target_name}")
                return {"success": True, "mount_point": str(mount_point), "status": "WARM"}

            # 3. [FACULTY 3]: Protocol Triage
            if url.startswith(('git@', 'https://github.com')):
                self._project_git_reality(url, mount_point)
            elif url.startswith(('http://', 'https://')):
                self._project_web_reality(url, mount_point)
            else:
                raise ArtisanHeresy(f"Protocol Heresy: Unsupported URL scheme in '{url}'")

            self._active_mounts[url] = mount_point

        return {
            "success": True,
            "mount_point": str(mount_point.relative_to(self.root)),
            "status": "INHABITED",
            "telemetry": {
                "size": self._calculate_mount_size(mount_point),
                "timestamp": time.time()
            }
        }

    def _project_git_reality(self, url: str, dest: Path):
        """
        [FACULTY 2]: Selective Shallow Proclivity.
        Clones only the structural skeleton of the Git soul.
        """
        Logger.verbose(f"   -> Forging Git Wormhole to {url}...")
        try:
            # Use --depth 1 and --filter to minimize I/O entropy
            cmd = [
                "git", "clone",
                "--depth", "1",
                "--single-branch",
                "--filter=blob:none",
                url, str(dest)
            ]

            # [FACULTY 11]: Telemetry Pulse
            # In a full implementation, we'd wrap this in a progress monitor
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)

            # [FACULTY 6]: Shadow-Branch Spawning
            # Forge an ephemeral branch for shadow prototype commits
            subprocess.run(
                ["git", "checkout", "-b", "scaffold-shadow-proto"],
                cwd=dest, check=True, capture_output=True
            )

        except subprocess.CalledProcessError as e:
            shutil.rmtree(dest, ignore_errors=True)
            raise ArtisanHeresy(f"Git Projection failed: {e.stderr.decode()}")

    def _project_web_reality(self, url: str, dest: Path):
        """
        [FACULTY 4]: Neural Web-Scraping Alchemy.
        Projects documentation or static sites as Gnostic trees.
        """
        Logger.verbose(f"   -> Scrying Web Reality at {url}...")
        dest.mkdir(parents=True, exist_ok=True)

        # This is a prophecy for the Neural Scraper.
        # For now, we forge a virtual README and project the landing page.
        try:
            import requests
            response = requests.get(url, timeout=10)
            (dest / "index.html").write_text(response.text, encoding='utf-8')
            (dest / "scaffold.remote").write_text(f"URL: {url}\nType: WebProjection", encoding='utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"Web Projection failed: {e}")

    def purge_mount(self, url: str):
        """[FACULTY 10]: Wormhole Cleanup Sentinel."""
        with self._lock:
            mount_point = self._active_mounts.pop(url, None)
            if mount_point and mount_point.exists():
                Logger.warn(f"Annihilating mount: {mount_point.name}")
                shutil.rmtree(mount_point, ignore_errors=True)

    def _calculate_mount_size(self, path: Path) -> int:
        """Heuristic Gaze of the mount's physical mass."""
        total = 0
        for f in path.rglob('*'):
            if f.is_file():
                total += f.stat().st_size
        return total

    def cleanup_all(self):
        """Final purification of the mount sanctum."""
        Logger.verbose("Purifying the Celestial mount sanctum...")
        shutil.rmtree(self.mount_root, ignore_errors=True)
        self.mount_root.mkdir()

# --- [ELEVATION: RUST INTEROP PROTOCOL] ---
# If the Rust Core (Iron Core) were to invoke this, it would use:
# scaffold_core_rs::telepresence::project_celestial_url(url)

