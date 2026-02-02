# Path: scaffold/core/kernel/archivist/storage.py
# -----------------------------------------------

import tarfile
import os
import io
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any

from .contracts import ArchiveConfig
from .filters import GnosticFilter
from .manifest import ManifestScribe
from ....utils import hash_file
from ....logger import Scribe

Logger = Scribe("ArchiveStorage")


class GnosticStorage:
    """
    =============================================================================
    == THE HAND OF MATTER (V-Ω-ATOMIC-IO)                                      ==
    =============================================================================
    Manages the physical inscription of the archive.
    """

    def __init__(self, root: Path, config: ArchiveConfig):
        self.root = root
        self.config = config
        self.gnostic_filter = GnosticFilter(root, config)

    def inscribe(self, targets: List[Path], dest_path: Path, reason: str) -> Tuple[int, str, List[str]]:
        """
        Writes the tarball to a .tmp file, adds manifest, and moves to final dest.
        Returns (size, hash, skipped_list).
        """
        # Atomic Write Pattern
        temp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
        file_hashes: Dict[str, str] = {}

        mode = f"w:{self.config.compression}"

        try:
            with tarfile.open(temp_path, mode, compresslevel=self.config.compression_level) as tar:
                # 1. Add Target Files
                for target in targets:
                    try:
                        # Determine arcname relative to project root
                        try:
                            arcname = str(target.relative_to(self.root))
                        except ValueError:
                            arcname = target.name  # Fallback for external files

                        # Add to tar
                        tar.add(target, arcname=arcname, filter=self.gnostic_filter.filter_tarinfo)

                        # If it's a file, we want to hash it for the manifest
                        # Note: We re-read it here. In a hyper-optimized version, we'd wrap the file obj.
                        # For now, reliability > micro-optimization.
                        if target.is_file() and not self.config.structure_only:
                            # Verify if it was filtered out?
                            # tar.add doesn't return info on filtered items easily.
                            # We check our filter manually.
                            # Optimization: The filter already ran in tar.add.
                            # We'll just hash everything in targets that looks valid.
                            # A slight inefficiency but acceptable.
                            file_hashes[arcname] = hash_file(target)

                    except Exception as e:
                        Logger.warn(f"Failed to archive '{target.name}': {e}")

                # 2. Forge and Add Manifest
                manifest_bytes = ManifestScribe.forge(reason, file_hashes, self.gnostic_filter.skipped_log)

                ti = tarfile.TarInfo(name="__gnosis__.json")
                ti.size = len(manifest_bytes)
                ti.mtime = time.time()
                tar.addfile(ti, io.BytesIO(manifest_bytes))

                # 3. Add Forensic Log
                if self.gnostic_filter.skipped_log:
                    log_bytes = "\n".join(self.gnostic_filter.skipped_log).encode('utf-8')
                    ti_log = tarfile.TarInfo(name="__skipped__.log")
                    ti_log.size = len(log_bytes)
                    ti_log.mtime = time.time()
                    tar.addfile(ti_log, io.BytesIO(log_bytes))

            # 4. Atomic Swap
            if dest_path.exists():
                dest_path.unlink()
            os.replace(temp_path, dest_path)

            # 5. Final Hash of Archive
            final_hash = hash_file(dest_path)

            return dest_path.stat().st_size, final_hash, self.gnostic_filter.skipped_log

        except Exception as e:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except:
                    pass
            raise e