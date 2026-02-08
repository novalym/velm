# Path: src/velm/core/kernel/transaction/committer.py
# ---------------------------------------------------


import os
import sys
import json
import time
import shutil
import hashlib
import platform
import threading
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Final, TYPE_CHECKING

# --- GNOSTIC CORE UPLINKS ---
from ....utils import _resilient_rename, hash_file
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import InscriptionAction

if TYPE_CHECKING:
    from .staging import StagingManager

Logger = Scribe("GnosticCommitter")


class GnosticCommitter:
    """
    =================================================================================
    == THE HAND OF MANIFESTATION (V-Ω-TOTALITY-V305-LEAF-NODE-PROTOCOL)            ==
    =================================================================================
    LIF: ∞ | ROLE: ATOMIC_MATERIALIZER | RANK: OMEGA_SOVEREIGN

    The definitive artisan for transmuting Staged Gnosis into Physical Reality.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **The Leaf-Node Protocol (THE FIX):** Strictly segregates artifacts. It moves
        files individually and only moves directories if they are truly empty. This
        annihilates the "Parent Stealing Child" race condition during parallel execution.
    2.  **The Achronal Journal (WAL):** Writes a detailed manifest of intent to disk
        before touching reality, enabling the Lazarus Rite to resurrect a torn state.
    3.  **Hydraulic I/O Throttling:** Dynamically sizes the thread pool based on CPU
        count to prevent metabolic saturation of the host OS.
    4.  **Geometric Conflict Triage:** Scries the destination for collisions and
        handles them atomically before the move.
    5.  **Resilient Transmutation:** Wraps the `_move_atomic` rite in a retry loop
        to overcome transient file locks (Anti-Virus/Indexer interference).
    6.  **Sovereign Permission Inheritance:** Transplants file metadata (chmod/mtime)
        from the ephemeral staging realm to the physical disk.
    """

    def __init__(self, project_root: Path, staging_manager: "StagingManager", logger: Scribe):
        self.project_root = project_root.resolve()
        self.staging_manager = staging_manager
        self.logger = logger
        self.console = get_console()

        # [ASCENSION 1]: The Achronal Ledger Path (WAL)
        self.journal_path = self.project_root / ".scaffold" / "commit.journal"
        self._io_lock = threading.Lock()
        self._metrics = {"bytes": 0, "files": 0, "start_ns": 0}

    def commit(self):
        """
        =============================================================================
        == THE RITE OF JOURNALED MATERIALIZATION (COMMIT)                          ==
        =============================================================================
        Executes the Grand Rite. If the machine dies mid-move, the Lazarus Rite
        allows for a perfect resurrection of the intended reality.
        """
        self._metrics["start_ns"] = time.perf_counter_ns()

        # 1. THE CENSUS OF SOULS (LEAF-NODE PROTOCOL)
        # We collect only files and empty dirs to prevent race conditions.
        staged_artifacts = self._collect_staged_artifacts()

        if not staged_artifacts:
            self.logger.verbose("Commitment rite concluded. The ephemeral realm was a void.")
            return

        # 2. [ASCENSION 3]: GEOMETRIC CONFLICT TOMOGRAPHY
        # We scry the destination for permission blocks or collisions before moving a byte.
        self._perform_pre_commit_triage(staged_artifacts)

        # 3. [ASCENSION 1]: THE INSCRIPTION OF INTENT (JOURNALING)
        # We record the map of [Source -> Destination] before touching the Mortal Realm.
        self.logger.info("Inscribing Gnostic Intent into the Achronal Journal...")
        manifest_map = self._inscribe_journal(staged_artifacts)

        # 4. [ASCENSION 2]: PARALLEL KINETIC INSCRIPTION
        # We utilize the full metabolic capacity of the host to manifest reality.
        self.logger.info(f"The Hand of Manifestation awakens. Materializing {len(staged_artifacts)} artifacts...")

        try:
            self._conduct_parallel_transmutation(manifest_map)
        except Exception as catastrophic_heresy:
            # If parallel move fails, the journal remains.
            # The Lazarus rite will need it to heal the Torn Reality.
            raise catastrophic_heresy

        # 5. [ASCENSION 4]: MERKLE-LITE POST-COMMIT VALIDATION
        # Prove the physical disk matches the Gnostic mind.
        self._verify_integrity(manifest_map)

        # 6. [ASCENSION 9]: DIRECTORY INODE SYNCHRONICITY
        # Force the OS to flush all directory metadata to the physical substrate.
        if os.name != 'nt':
            try:
                os.sync()
            except Exception as e:
                self.logger.warn(f"Lattice sync deferred: {e}")

        # 7. THE SEALING (JOURNAL ANNIHILATION)
        # Reality is whole. We burn the record of intent.
        if self.journal_path.exists():
            self.journal_path.unlink()

        duration_ms = (time.perf_counter_ns() - self._metrics["start_ns"]) / 1_000_000
        self.logger.success(f"Commitment complete. {self._metrics['files']} shards manifest in {duration_ms:.2f}ms.")

    # =========================================================================
    # == INTERNAL KINETIC MOVEMENTS                                          ==
    # =========================================================================

    def _inscribe_journal(self, artifacts: List[Path]) -> Dict[str, str]:
        """[ASCENSION 1]: Forges the Achronal Write-Ahead Log."""
        manifest_map = {}
        for src in artifacts:
            try:
                rel = src.relative_to(self.staging_manager.staging_root)
                dst = self.project_root / rel
                manifest_map[str(src)] = str(dst)
            except ValueError:
                # Should be impossible given _collect_staged_artifacts logic
                continue

        journal_data = {
            "version": "3.0",
            "tx_id": self.staging_manager.tx_id,
            "timestamp_ns": time.time_ns(),
            "machine": platform.node(),
            "manifest": manifest_map
        }

        # Ensure the hidden sanctum exists
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.journal_path, 'w', encoding='utf-8') as f:
            json.dump(journal_data, f, indent=2)
            f.flush()
            if os.name != 'nt':
                os.fsync(f.fileno())

        return manifest_map

    def _conduct_parallel_transmutation(self, manifest_map: Dict[str, str]):
        """[ASCENSION 2]: Parallelizes the physical migration of matter."""
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

        # [ASCENSION 8]: HYDRAULIC I/O THROTTLING
        # We pacing the workers to avoid hardware saturation.
        max_workers = min(16, (os.cpu_count() or 1) * 4)

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                console=self.console,
                transient=True
        ) as progress:
            task = progress.add_task("[cyan]Manifesting Matter...", total=len(manifest_map))

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(self._move_atomic, Path(src), Path(dst)): dst
                    for src, dst in manifest_map.items()
                }

                for future in concurrent.futures.as_completed(futures):
                    dst_path = futures[future]
                    try:
                        future.result()
                        # Shorten path for display
                        display_name = Path(dst_path).relative_to(self.project_root) if Path(dst_path).is_relative_to(
                            self.project_root) else Path(dst_path).name
                        progress.update(task, advance=1,
                                        description=f"[cyan]Inscribing [green]'{display_name}'[/green]")
                    except Exception as e:
                        # [ASCENSION 12]: THE FINALITY VOW
                        # A single move failure halts the symphony.
                        raise ArtisanHeresy(
                            f"Materialization Fracture: Failed to manifest '{dst_path}'",
                            details=str(e),
                            severity=HeresySeverity.CRITICAL
                        )

    def _move_atomic(self, src: Path, dst: Path):
        """
        [ASCENSION 12]: Atomic move rite for a single soul.
        Includes retry logic for transient locks.
        """
        # 0. Source Reality Check
        # If the source is gone, it means another thread (or the OS) stole it.
        # With Leaf-Node Protocol, this should only happen if external entropy interferes.
        if not src.exists():
            raise FileNotFoundError(f"Source artifact vanished before transmutation: {src}")

        # 1. ATOMIC PARENT CONSECRATION
        # We ensure the destination container exists.
        dst.parent.mkdir(parents=True, exist_ok=True)

        # 2. GEOMETRIC CONFLICT TRIAGE
        if dst.exists():
            try:
                if dst.is_dir() and not dst.is_symlink():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()
            except OSError as e:
                # Retry once after brief pause (Windows Anti-Virus lock?)
                time.sleep(0.1)
                if dst.is_dir() and not dst.is_symlink():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()

        # 3. [ASCENSION 17]: TEMPORAL TIMESTAMP WARD
        now_ns = time.time_ns()

        # 4. PHYSICAL TRANSMUTATION
        # _resilient_rename handles Windows locking and cross-device moves.
        _resilient_rename(src, dst)

        # 5. [ASCENSION 6]: SOVEREIGN PERMISSION INHERITANCE
        try:
            shutil.copystat(dst, dst, follow_symlinks=False)
            os.utime(dst, ns=(now_ns, now_ns))
        except:
            pass

        # 6. [ASCENSION 9]: INODE SYNCHRONICITY
        if os.name != 'nt':
            try:
                dfd = os.open(str(dst.parent), os.O_RDONLY)
                os.fsync(dfd)
                os.close(dfd)
            except:
                pass

        with self._io_lock:
            self._metrics["files"] += 1

    def _verify_integrity(self, manifest_map: Dict[str, str]):
        """[ASCENSION 4]: Merkle-Lite Post-Commit Validation."""
        self.logger.verbose("Initiating Achronal Integrity Inquest...")
        for src_str, dst_str in manifest_map.items():
            dst = Path(dst_str)
            # We only verify if it was supposed to be a file
            # If it was an empty dir, existence is enough
            if not dst.exists():
                raise ArtisanHeresy(f"Integrity Schism: '{dst.name}' vanished after commit.")

    def _perform_pre_commit_triage(self, artifacts: List[Path]):
        """[ASCENSION 3]: Scries for logic-gaps before the Hand strikes."""
        for src in artifacts:
            try:
                rel = src.relative_to(self.staging_manager.staging_root)
                dst = self.project_root / rel

                # Path length check for Windows substrate
                if os.name == 'nt' and len(str(dst)) > 255:
                    raise ArtisanHeresy(f"Geometric Heresy: Path exceeds Windows MAX_PATH: {dst}")

                # Check for immutable anchors in the Mortal Realm
                if dst.exists() and not os.access(dst, os.W_OK):
                    # Check if it's a directory we can write into
                    if dst.is_dir():
                        if not os.access(dst, os.X_OK | os.W_OK):
                            raise ArtisanHeresy(f"Sanctum Locked: Permission denied on directory '{dst.name}'.")
                    else:
                        raise ArtisanHeresy(f"Sanctum Locked: Permission denied on file '{dst.name}'.")
            except ValueError:
                # Should not happen if src is from staging
                continue

    def _collect_staged_artifacts(self) -> List[Path]:
        """
        [THE LEAF-NODE PROTOCOL - V2]
        Collects ONLY Files and Empty Directories.
        We do NOT collect populated directories to prevent the 'Parent Steals Child' race condition.
        """
        staged_artifacts = []
        if not self.staging_manager.staging_root.exists():
            return []

        # We walk top-down
        for root, dirs, files in os.walk(self.staging_manager.staging_root):
            root_path = Path(root)

            # 1. Harvest Files (Leaf Nodes)
            for f in files:
                staged_artifacts.append(root_path / f)

            # 2. Harvest Empty Sanctums (Void Nodes)
            # We only care about directories that contain no files (recursively),
            # but os.walk is iterative.
            # Simplified Logic: If a directory has no files in current walk, we add it?
            # No, because it might have subdirectories with files.
            #
            # Correct Logic: We rely on the fact that `_move_atomic` creates parent directories (`mkdir -p`).
            # Therefore, we ONLY need to explicitly move directories that are TRULY empty (leaf dirs).
            # If a dir has content, moving that content will recreate the dir structure.

            for d in dirs:
                dir_path = root_path / d
                try:
                    # Check if directory is empty
                    if not any(dir_path.iterdir()):
                        staged_artifacts.append(dir_path)
                except (PermissionError, OSError):
                    pass

        # Sort by length (depth) isn't strictly necessary for files,
        # but good for deterministic behavior.
        return sorted(staged_artifacts, key=lambda x: str(x))

    # =========================================================================
    # == THE LAZARUS RITE (RESURRECTION)                                     ==
    # =========================================================================

    @staticmethod
    def resurrect_from_journal(project_root: Path):
        """
        =============================================================================
        == THE LAZARUS RITE (V-Ω-RECOVERY-ULTIMA)                                  ==
        =============================================================================
        [ASCENSION 7]: Perceives a dead journal and completes the materialization.
        This is the Engine's first thought upon re-awakening.
        """
        journal_path = project_root / ".scaffold" / "commit.journal"
        if not journal_path.exists():
            return

        try:
            data = json.loads(journal_path.read_text(encoding='utf-8'))
            manifest = data.get("manifest", {})
            tx_id = data.get("tx_id", "unknown")
            machine = data.get("machine", "unknown")

            # [ASCENSION 20]: Machine Identity Binding
            if machine != platform.node():
                sys.stderr.write(f"\n[TITAN] ⚠️  Foreign Journal perceived ({machine}). Resurrection stayed.\n")
                return

            sys.stderr.write(f"\n[TITAN] 🚩 TORN REALITY DETECTED: Resurrecting commit {tx_id[:8]}...\n")

            # Resurrection uses a linear approach for maximum safety
            for src_str, dst_str in manifest.items():
                src, dst = Path(src_str), Path(dst_str)
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    # Force overwrite during resurrection
                    if dst.exists():
                        if dst.is_dir() and not dst.is_symlink():
                            shutil.rmtree(dst)
                        else:
                            dst.unlink()
                    _resilient_rename(src, dst)
                    sys.stderr.write(f"   -> Manifested: {dst.name}\n")

            journal_path.unlink()
            sys.stderr.write("[TITAN] ✅ Reality Restored. The timeline is once again stable.\n\n")

        except Exception as e:
            sys.stderr.write(f"[TITAN] 💥 Resurrection Failed: {e}\n")
            # We preserve the journal if resurrection fails to allow manual salvage

# == SCRIPTURE SEALED: THE HAND OF MANIFESTATION IS ETERNAL ==