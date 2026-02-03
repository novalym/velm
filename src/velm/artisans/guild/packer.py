# Path: artisans/guild/packer.py
# ------------------------------

import shutil
import tarfile
from pathlib import Path
from typing import Optional


class GuildPacker:
    """The Scribe that bundles Gnosis for transport."""

    def __init__(self, project_root: Path):
        self.local_forge = project_root / ".scaffold" / "archetypes"
        self.global_forge = Path.home() / ".scaffold" / "archetypes"
        self.dist_dir = Path.home() / ".scaffold" / "dist"
        self.dist_dir.mkdir(parents=True, exist_ok=True)

    def pack_archetype(self, name: str) -> Optional[Path]:
        """Finds an archetype and zips it."""
        # Find Source
        source = (self.local_forge / f"{name}.scaffold")
        if not source.exists():
            source = (self.global_forge / f"{name}.scaffold")

        if not source.exists(): return None

        # Pack
        target_zip = self.dist_dir / f"{name}.tar.gz"
        with tarfile.open(target_zip, "w:gz") as tar:
            tar.add(source, arcname=source.name)

        return target_zip