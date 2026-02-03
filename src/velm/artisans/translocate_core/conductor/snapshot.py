# Path: scaffold/artisans/translocate_core/conductor/snapshot.py
# --------------------------------------------------------------

import hashlib
import time
import json
import tarfile
import io
import getpass
import platform
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple, List, TYPE_CHECKING, Any, Optional

from rich.progress import Progress
from rich.prompt import Confirm

# --- THE DIVINE SUMMONS ---
import velm
from ....contracts.heresy_contracts import ArtisanHeresy
from ....utils import hash_file, get_human_readable_size
from ....logger import get_console, Scribe

if TYPE_CHECKING:
    from .engine import TranslocationConductor

Logger = Scribe("GnosticArchivist")


class SnapshotMixin:
    """
    =================================================================================
    == THE FACULTY OF PRESERVATION (V-Ω-FORENSIC-ARCHIVIST-ULTIMA)                 ==
    =================================================================================
    Handles the creation of Gnostic Snapshots (backups) before kinetic action.
    """

    def _forge_gnostic_snapshot(self: 'TranslocationConductor', progress: Progress, task_id) -> Path:
        """
        =================================================================================
        == THE GOD-ENGINE OF FORENSIC ARCHIVAL (V-Ω-ULTRA-DEFINITIVE-ASCENDED)         ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000

        This is not a function; it is a divine, sentient Guardian that forges a
        perfect, Gnostically-aware, and cryptographically verifiable Time Capsule of a
        reality before it is transfigured.
        """
        if not self.backup_root_path:
            raise ArtisanHeresy("A plea was made to forge a snapshot, but the sanctum is a void.")

        # Ensure the Sanctum exists
        self.backup_root_path.mkdir(parents=True, exist_ok=True)

        console = get_console()

        # [FACULTY 24] The Self-Aware Name
        # We hash the plan itself to create a unique fingerprint for this specific operation.
        plan_str = str(sorted([(str(k), str(v)) for k, v in self.translocation_map.moves.items()]))
        plan_hash = hashlib.sha256(plan_str.encode()).hexdigest()[:8]
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        archive_name = f"translocate-{timestamp}-{plan_hash}.tar.gz"
        tmp_archive_path = self.backup_root_path.resolve() / f".{archive_name}.tmp"
        final_archive_path = self.backup_root_path.resolve() / archive_name

        forensic_log: List[str] = [
            f"### Gnostic Forensic Log for Snapshot {archive_name} ###",
            f"Date: {datetime.now(timezone.utc).isoformat()}",
            f"Architect: {getpass.getuser()}",
            f"Plan Hash: {plan_hash}",
            "---"
        ]

        # --- MOVEMENT I: THE PRE-FLIGHT GAZE ---
        items_to_backup: List[Tuple[Path, str]] = []
        total_backup_size = 0
        heavyweights_detected = []
        ignored_count = 0

        progress.update(task_id, description="[yellow]Calculating snapshot cosmology...")

        # Sort origins by path length to ensure consistent ordering
        origins_to_scan = sorted(list(self.translocation_map.moves.keys()), key=lambda p: str(p))

        # [FACULTY 16] The Recursive Scanner
        processed_paths = set()

        for origin in origins_to_scan:
            if not origin.exists():
                forensic_log.append(f"MISSING: {origin} (Source vanished before snapshot)")
                continue

            # If it's a symlink, we treat it as a file (archive the link itself)
            if origin.is_symlink():
                paths_to_add = [origin]
            elif origin.is_file():
                paths_to_add = [origin]
            else:
                # It is a directory. We must recurse.
                paths_to_add = list(origin.rglob("*"))
                paths_to_add.append(origin)  # Include the dir itself for metadata

            for path in paths_to_add:
                # Deduplication Ward
                if path in processed_paths: continue
                processed_paths.add(path)

                # [FACULTY 18] The Smart Exclusion Heuristic
                # We do not archive the .git folder or internal scaffold cache during a move
                # unless explicitly requested.
                if ".git" in path.parts or "__pycache__" in path.parts:
                    ignored_count += 1
                    continue

                # We also skip the backup directory itself to prevent recursion loops
                if self.backup_root_path in path.parents or path == self.backup_root_path:
                    continue

                try:
                    rel_arcname = str(path.relative_to(self.project_root))
                except ValueError:
                    # If path is outside project root, store it under a specialized prefix
                    rel_arcname = f"__EXTERNAL__/{path.name}"

                if path.is_dir():
                    items_to_backup.append((path, rel_arcname))

                elif path.is_file() or path.is_symlink():
                    file_size = path.stat().st_size

                    # [FACULTY 19] The Heavyweight Sentinel
                    if file_size > 100 * 1024 * 1024:  # 100MB Limit
                        heavyweights_detected.append((path, file_size))
                        forensic_log.append(
                            f"HEAVYWEIGHT_EXCLUDED: {rel_arcname} ({get_human_readable_size(file_size)})")
                        continue

                    items_to_backup.append((path, rel_arcname))
                    total_backup_size += file_size

        # --- MOVEMENT II: THE RITE OF CONSENT ---
        if not self.non_interactive:
            if heavyweights_detected:
                console.print(
                    f"[bold yellow]⚠️  {len(heavyweights_detected)} heavyweight scripture(s) detected (>100MB).[/bold yellow]")
                if not Confirm.ask(
                        f"Exclude them to preserve spacetime integrity?",
                        default=True):
                    # Re-add them if the Architect insists
                    for path, size in heavyweights_detected:
                        try:
                            arc = str(path.relative_to(self.project_root))
                        except:
                            arc = f"__EXTERNAL__/{path.name}"
                        items_to_backup.append((path, arc))
                        total_backup_size += size
                        forensic_log.append(f"HEAVYWEIGHT_INCLUDED_BY_FIAT: {arc}")

            # Warn if backup is massive
            if total_backup_size > 500 * 1024 * 1024:  # 500MB
                console.print(
                    f"[bold red]⚠️  Snapshot size will be approx {get_human_readable_size(total_backup_size)}.[/bold red]")
                if not Confirm.ask("Proceed with archival?", default=True):
                    raise ArtisanHeresy("Snapshot rite stayed by Architect's prudence.", exit_code=0)

        # --- MOVEMENT III: THE FORGING OF THE GNOSTIC TARBALL ---
        progress.update(task_id, total=total_backup_size, description="[yellow]Forging Gnostic Snapshot...")

        # Determine Git State for the Manifest
        git_state = self._capture_git_state()
        gnosis_manifest = self._forge_manifest_header(git_state)

        try:
            # We open the tarfile in write mode with gzip compression
            with tarfile.open(tmp_archive_path, "w:gz") as tar:

                # [FACULTY 17 & 22] The Permission & Owner Chronicler
                buffer_size = 1024 * 1024  # 1MB Buffer for speed

                for path, arc_name in items_to_backup:
                    # Update progress visually
                    if path.is_file() and not path.is_symlink():
                        progress.update(task_id, advance=path.stat().st_size,
                                        description=f"[cyan]Archiving '{path.name}'...")

                    # Add to Tar
                    # We use 'recursive=False' because we flattened the list manually for control
                    tar.add(path, arcname=arc_name, recursive=False)

                    # Gather Metadata
                    if path.is_file() and not path.is_symlink():
                        file_hash = hash_file(path)
                        stat_info = path.stat()
                        entry = {
                            "sha256": file_hash,
                            "mode": oct(stat_info.st_mode)[-4:],
                            "size": stat_info.st_size,
                            "mtime": stat_info.st_mtime
                        }
                        # Capture ownership if on POSIX
                        if hasattr(stat_info, 'st_uid'):
                            entry["uid"] = stat_info.st_uid
                            entry["gid"] = stat_info.st_gid

                        gnosis_manifest["file_fingerprints"][arc_name] = entry

                # [FACULTY 21] The Forensic Log Stream
                forensic_log.append("--- End of Ledger ---")
                log_bytes = "\n".join(forensic_log).encode('utf-8')

                tarinfo_log = tarfile.TarInfo(name="__log__.txt")
                tarinfo_log.size = len(log_bytes)
                tarinfo_log.mtime = time.time()
                tar.addfile(tarinfo_log, fileobj=io.BytesIO(log_bytes))

                # [FACULTY 15] The Cryptographic Seal
                # We serialize the manifest to calculate its own hash before insertion
                manifest_str_for_hash = json.dumps(gnosis_manifest, sort_keys=True)
                manifest_hash = hashlib.sha256(manifest_str_for_hash.encode('utf-8')).hexdigest()
                gnosis_manifest["integrity"]["manifest_hash"] = manifest_hash

                manifest_bytes = json.dumps(gnosis_manifest, indent=2).encode('utf-8')

                tarinfo_gnosis = tarfile.TarInfo(name="__gnosis__.json")
                tarinfo_gnosis.size = len(manifest_bytes)
                tarinfo_gnosis.mtime = time.time()
                tar.addfile(tarinfo_gnosis, fileobj=io.BytesIO(manifest_bytes))

            # --- MOVEMENT IV: THE INTEGRITY INQUISITION ---
            # We verify the archive is valid GZIP structure before finalizing.
            if not tarfile.is_tarfile(tmp_archive_path):
                raise ArtisanHeresy("The forged archive is structurally profane (Invalid Tar/Gzip).")

            # --- MOVEMENT V: THE ATOMIC CONSECRATION ---
            # Rename .tmp to .tar.gz
            if final_archive_path.exists():
                final_archive_path.unlink()
            os.rename(tmp_archive_path, final_archive_path)

            final_size = final_archive_path.stat().st_size
            progress.update(task_id, completed=total_backup_size,
                            description=f"[green]Snapshot secured: [cyan]'{final_archive_path.name}'[/cyan] ({get_human_readable_size(final_size)})")

            return final_archive_path

        except Exception as e:
            # [FACULTY 23] The Self-Healing Forge
            # Clean up the partial artifact to prevent corruption confusion
            if tmp_archive_path.exists():
                try:
                    tmp_archive_path.unlink()
                except:
                    pass

            raise ArtisanHeresy("A catastrophic paradox shattered the snapshot forging rite.", child_heresy=e) from e

    def _capture_git_state(self) -> Dict[str, str]:
        """
        [FACULTY 25] The Git State Anchor.
        Captures the exact commit and status of the repo at snapshot time.
        """
        state = {"active": False}
        if (self.project_root / ".git").exists():
            try:
                commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.project_root, text=True,
                                                 stderr=subprocess.DEVNULL).strip()
                branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=self.project_root,
                                                 text=True, stderr=subprocess.DEVNULL).strip()
                status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=self.project_root, text=True,
                                                 stderr=subprocess.DEVNULL).strip()

                state.update({
                    "active": True,
                    "commit": commit,
                    "branch": branch,
                    "dirty": bool(status)
                })
            except Exception:
                pass
        return state

    def _get_system_vitality(self) -> Dict[str, Any]:
        """
        [FACULTY 26] The System Vitality Snapshot.
        Records load averages to understand environmental pressure.
        """
        vitals = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cpu_count": os.cpu_count()
        }
        try:
            # Load avg (Unix only)
            if hasattr(os, 'getloadavg'):
                vitals['load_avg'] = os.getloadavg()
        except:
            pass
        return vitals

    def _forge_manifest_header(self: 'TranslocationConductor', git_state: Dict[str, Any]) -> Dict:
        """A new, divine artisan to forge the header of the Gnostic manifest."""
        # [FACULTY 14] The Gnostic Change Vector
        return {
            "snapshot_version": "3.0-forensic",
            "provenance": {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "scaffold_version": velm.__version__,
                "architect": getpass.getuser(),
                "machine_id": platform.node(),
                "triggering_command": "scaffold translocate",
            },
            "environment": {
                "git": git_state,
                "system": self._get_system_vitality()
            },
            "change_vector": {
                "type": "translocation",
                # Serialize the move map for forensic replay
                "map": {str(k.relative_to(self.project_root)): str(v.relative_to(self.project_root))
                        for k, v in self.translocation_map.moves.items()}
            },
            "integrity": {
                "manifest_hash": None  # Placeholder for the final seal
            },
            "file_fingerprints": {}
        }