# Path: scaffold/artisans/distill/celestial.py
# --------------------------------------------

import requests
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional
from ...logger import Scribe

Logger = Scribe("CelestialFetcher")

class CelestialMaterializer:
    """
    =============================================================================
    == THE CELESTIAL MATERIALIZER (V-Ω-REMOTE-FETCHER)                         ==
    =============================================================================
    Downloads and extracts remote scriptures (GitHub, Gists) into an ephemeral sanctum.
    """

    @staticmethod
    def materialize(url: str, ephemeral_root: Path) -> Path:
        """Downloads the soul from the URL."""
        is_repo = "github.com" in url or url.endswith((".zip", ".git"))

        if is_repo:
            repo_url = url
            if "github.com" in repo_url and not repo_url.endswith(
                    ("/archive/refs/heads/main.zip", "/archive/refs/heads/master.zip")):
                # Heuristic: Default to main branch zip
                repo_url = repo_url.rstrip('/') + "/archive/refs/heads/main.zip"

            Logger.verbose(f"Downloading celestial archive from: {repo_url}")
            response = requests.get(repo_url, stream=True, timeout=60)
            response.raise_for_status()

            with zipfile.ZipFile(BytesIO(response.content)) as zf:
                zf.extractall(ephemeral_root)

            # Find the inner directory
            extracted_contents = list(ephemeral_root.iterdir())
            if len(extracted_contents) == 1 and extracted_contents[0].is_dir():
                source_path = extracted_contents[0]
                Logger.success(f"Celestial archive materialized at: {source_path.name}")
                return source_path
            return ephemeral_root
        else:
            # Single file (Gist raw or similar)
            filename = Path(url).name or "celestial_scripture.scaffold"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            target_path = ephemeral_root / filename
            target_path.write_text(response.text, encoding='utf-8')
            Logger.success(f"Celestial scripture '{filename}' materialized.")
            return target_path