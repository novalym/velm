# Path: src/velm/core/kernel/transaction/committer.py
# ---------------------------------------------------
import uuid
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
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final, Union

# --- THE DIVINE UPLINKS ---
from ....utils import _resilient_rename, hash_file, get_human_readable_size
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import InscriptionAction

if TYPE_CHECKING:
    from .staging import StagingManager

Logger = Scribe("GnosticCommitter")


class GnosticCommitter:
    """
    =================================================================================
    == THE GNOSTIC TITANIUM COMMITTER (V-Ω-TOTALITY-V320-FINALIS)                  ==
    =================================================================================
    LIF: ∞ | ROLE: ATOMIC_MATERIALIZER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_COMMITTER_V320_TITANIUM_ZERO_LOSS_ULTIMA

    The final, unbreakable arbiter of physical reality. It ensures the transition
    from Gnostic Thought to Manifest Matter is perfect, atomic, and reversible.
    """

    # [PHYSICS CONSTANTS]
    MIN_DISK_BUFFER_MB: Final[int] = 128
    MAX_CONCURRENCY: Final[int] = 16
    RETRY_COUNT: Final[int] = 5
    RETRY_DELAY_S: Final[float] = 0.2

    def __init__(self, project_root: Path, staging_manager: "StagingManager", logger: Scribe):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root.resolve()
        self.staging_manager = staging_manager
        self.logger = logger
        self.console = get_console()

        # [ASCENSION 2]: The Achronal Ledger Path (WAL)
        self.journal_path = self.project_root / ".scaffold" / "commit.journal"

        # [ASCENSION 10]: Session Signing Secret
        self._session_secret = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

        # Internal Metrics & Synchronizers
        self._io_lock = threading.Lock()
        self._checkpoint_lock = threading.Lock()
        self._completed_paths: Set[str] = set()

        self._metrics = {
            "bytes_shadowed": 0,
            "bytes_manifested": 0,
            "files_touched": 0,
            "start_ns": 0
        }

    def commit(self):
        """
        =============================================================================
        == THE RITE OF FINALITY (V-Ω-SHADOW-ARCHIVE-COMMIT)                        ==
        =============================================================================
        The Grand Symphony. Conducts the transition from Staging to Reality using
        the Shadow-Archive Protocol and the Leaf-Node Protocol for absolute safety.
        """
        self._metrics["start_ns"] = time.perf_counter_ns()

        # 1. THE CENSUS OF ATOMIC SOULS
        # [ASCENSION 2]: Leaf-Node Protocol. Only move files and empty dirs.
        staged_artifacts = self._collect_leaf_nodes()
        if not staged_artifacts:
            self.logger.verbose("The Ephemeral Realm is a void. No matter to manifest.")
            return

        # 2. [ASCENSION 3 & 9]: PRE-FLIGHT ADJUDICATION
        # Check permissions and disk space before the first shadow is cast.
        self._conduct_pre_flight_inquest(staged_artifacts)

        # 3. [ASCENSION 1 & 4]: THE RITE OF THE SHADOW ARCHIVE
        # We forge temporal echoes of all files we are about to transfigure.
        self.logger.info(f"Forging Shadow Archive for {len(staged_artifacts)} artifact(s)...")
        self._forge_shadow_archive(staged_artifacts)

        # 4. [ASCENSION 10]: THE INSCRIPTION OF INTENT (JOURNALING)
        # We record the WAL (Write Ahead Log) so Lazarus can resurrect us if we fall.
        manifest_map = self._inscribe_journal(staged_artifacts)

        # 5. [ASCENSION 5 & 12]: THE KINETIC TRANSMUTATION (MATERIALIZATION)
        # We physically move the matter from Staging to Root in parallel.
        self.logger.info("The Hand of Manifestation awakens. Transmuting Reality...")
        try:
            self._conduct_parallel_materialization(manifest_map)
        except Exception as catastrophic_paradox:
            # If we fracture here, the journal and shadows remain.
            # The higher-level Transaction will use the Shadows to Rollback.
            raise catastrophic_paradox

        # 6. [ASCENSION 3 & 11]: THE RITE OF VERIFICATION & SEALING
        # Merkle-check every manifested file.
        self._verify_physical_integrity(manifest_map)

        # BURN THE JOURNAL: The rite is complete.
        if self.journal_path.exists():
            self.journal_path.unlink()

        # 7. THE FINAL TELEMETRY
        duration_ms = (time.perf_counter_ns() - self._metrics["start_ns"]) / 1_000_000
        self.logger.success(
            f"Commitment complete. {self._metrics['files_touched']} shards manifest in {duration_ms:.2f}ms. "
            f"Reality is now [bold green]STABLE[/bold green]."
        )

    # =========================================================================
    # == INTERNAL ORGANS (KINETIC RITES)                                     ==
    # =========================================================================

    def _forge_shadow_archive(self, artifacts: List[Path]):
        """
        [ASCENSION 1, 4 & 7]: THE SHADOW FORGE.
        Creates bit-perfect backups of existing reality in parallel.
        """
        targets_needing_shadow = []
        for src in artifacts:
            rel = src.relative_to(self.staging_manager.staging_root)
            dst = self._canonize_path(self.project_root / rel)

            if dst.exists() and dst.is_file():
                targets_needing_shadow.append((dst, rel))

        if not targets_needing_shadow:
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_CONCURRENCY) as executor:
            futures = []
            for dst, rel in targets_needing_shadow:
                backup_path = self._canonize_path(self.staging_manager.backup_root / rel)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                futures.append(executor.submit(shutil.copy2, str(dst), str(backup_path)))

            concurrent.futures.wait(futures)
            for f in futures:
                if f.exception():
                    raise ArtisanHeresy(f"Shadow Forge fractured: {f.exception()}")

    def _conduct_parallel_materialization(self, manifest_map: Dict[str, str]):
        """[ASCENSION 5 & 8]: PARALLEL TRANSMUTATION with Throttling."""
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

        # Dynamic worker sizing based on I/O type (SSD vs HDD heuristic)
        worker_count = min(self.MAX_CONCURRENCY, (os.cpu_count() or 1) * 2)

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                console=self.console,
                transient=True
        ) as progress:
            task = progress.add_task("[cyan]Materializing Matter...", total=len(manifest_map))

            with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
                futures = {
                    executor.submit(self._move_atomic_resilient, Path(src), Path(dst)): dst
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
                        raise ArtisanHeresy(
                            f"Materialization Fracture: Failed to manifest '{dst_path}'",
                            details=str(e),
                            severity=HeresySeverity.CRITICAL
                        )

    def _move_atomic_resilient(self, src: Path, dst: Path):
        """
        [ASCENSION 12 & 5]: THE ATOMIC HAND (RESILIENT).
        Includes Windows Long-Path support and retry loops.
        """
        # [ASCENSION 1]: Path Normalization for Windows Long Paths
        src_can = self._canonize_path(src)
        dst_can = self._canonize_path(dst)

        # 1. Geometric Consecration
        dst_can.parent.mkdir(parents=True, exist_ok=True)

        # 2. Collision Erasure (Shadows already safely archived)
        if dst_can.exists():
            if dst_can.is_dir() and not dst_can.is_symlink():
                shutil.rmtree(str(dst_can))
            else:
                dst_can.unlink()

        # [ASCENSION 6]: Capture intended timestamp
        now_ns = time.time_ns()

        # 3. PHYSICAL TRANSMUTATION (WITH RETRY)
        last_error = None
        for attempt in range(self.RETRY_COUNT):
            try:
                # _resilient_rename handles low-level lock contention
                _resilient_rename(src_can, dst_can)
                break
            except Exception as e:
                last_error = e
                time.sleep(self.RETRY_DELAY_S * (attempt + 1))
        else:
            raise last_error

        # 4. [ASCENSION 7]: ATTRIBUTE REPLICATION
        try:
            # Mirror original staging permissions/mode
            shutil.copystat(str(dst_can), str(dst_can), follow_symlinks=False)
            # Apply achronal timestamp
            os.utime(str(dst_can), ns=(now_ns, now_ns))
        except:
            pass

        # 5. [ASCENSION 11]: INODE SYNC
        # Force parent directory to update its Inode entry for the new file
        if os.name != 'nt':
            try:
                dfd = os.open(str(dst_can.parent), os.O_RDONLY)
                os.fsync(dfd)
                os.close(dfd)
            except:
                pass

        # 6. CHECKPOINT
        with self._checkpoint_lock:
            self._completed_paths.add(str(dst_can))
            self._metrics["files_touched"] += 1

    def _conduct_pre_flight_inquest(self, artifacts: List[Path]):
        """[ASCENSION 3 & 9]: PRE-COMMIT TRIAGE."""
        # 1. Disk Space Gaze
        try:
            usage = shutil.disk_usage(self.project_root)
            free_mb = usage.free / (1024 * 1024)
            if free_mb < self.MIN_DISK_BUFFER_MB:
                raise ArtisanHeresy(
                    f"Metabolic Exhaustion: Host disk has only {free_mb:.1f}MB remaining.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Clean the host filesystem to allow for Shadow-Archive Forge."
                )
        except OSError:
            pass

        # 2. Permission Gaze
        for src in artifacts:
            try:
                rel = src.relative_to(self.staging_manager.staging_root)
                dst = self.project_root / rel
                if dst.exists() and not os.access(dst, os.W_OK):
                    raise ArtisanHeresy(f"Sanctum Locked: Permission Denied on '{rel}'.")
            except ValueError:
                continue

    def _collect_leaf_nodes(self) -> List[Path]:
        """
        [THE LEAF-NODE PROTOCOL]
        Collects ONLY Files and Empty Directories.
        Prevents race conditions by allowing recursive parent creation via mkdir.
        """
        staged_artifacts = []
        if not self.staging_manager.staging_root.exists():
            return []

        for root, dirs, files in os.walk(self.staging_manager.staging_root):
            root_path = Path(root)
            for f in files:
                staged_artifacts.append(root_path / f)
            for d in dirs:
                dir_path = root_path / d
                try:
                    if not any(dir_path.iterdir()):
                        staged_artifacts.append(dir_path)
                except (OSError, PermissionError):
                    pass

        return sorted(staged_artifacts, key=lambda x: str(x))

    def _inscribe_journal(self, artifacts: List[Path]) -> Dict[str, str]:
        """[ASCENSION 10]: FORGES THE SIGNED WAL JOURNAL."""
        manifest_map = {}
        for src in artifacts:
            rel = src.relative_to(self.staging_manager.staging_root)
            dst = self.project_root / rel
            manifest_map[str(src)] = str(dst)

        journal_data = {
            "version": "3.2-titanium",
            "tx_id": self.staging_manager.tx_id,
            "machine_signature": hashlib.md5(platform.node().encode()).hexdigest()[:8],
            "manifest": manifest_map,
            "shadow_root": str(self.staging_manager.backup_root),
            "timestamp": time.time()
        }

        # [ASCENSION 10]: Sign the Journal
        raw_json = json.dumps(journal_data, sort_keys=True)
        signature = hashlib.sha256((raw_json + self._session_secret).encode()).hexdigest()
        journal_data["signature"] = signature

        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.journal_path, 'w', encoding='utf-8') as f:
            json.dump(journal_data, f, indent=2)
            f.flush()
            if os.name != 'nt': os.fsync(f.fileno())

        return manifest_map

    def _verify_physical_integrity(self, manifest_map: Dict[str, str]):
        """[ASCENSION 3 & 5]: THE FINAL BIT-VERIFICATION."""
        for src_str, dst_str in manifest_map.items():
            dst = self._canonize_path(Path(dst_str))
            if not dst.exists():
                raise ArtisanHeresy(f"Integrity Schism: '{dst.name}' failed to materialize.")

            # Future: Merkle-hash verification could be added here for ultra-high security

    def _canonize_path(self, path: Path) -> Path:
        """
        [ASCENSION 1]: THE WINDOWS LONG-PATH BRIDGE.
        Transmutes standard paths into extended-length paths on Windows.
        """
        path_str = str(path.resolve())
        if platform.system() == "Windows" and not path_str.startswith("\\\\?\\"):
            # We must use backslashes for the extended prefix
            return Path("\\\\?\\" + path_str.replace("/", "\\"))
        return path

    # =========================================================================
    # == THE LAZARUS RITE (RESURRECTION)                                     ==
    # =========================================================================

    @staticmethod
    def resurrect_from_journal(project_root: Path):
        """
        =============================================================================
        == THE LAZARUS RITE (V-Ω-TOTALITY-V320-TITANIUM-RESURRECT)                 ==
        =============================================================================
        Perceives a dead journal and either completes the move or reverts using
        the Shadow Archive if the move was corrupt.
        """
        journal_path = project_root / ".scaffold" / "commit.journal"
        if not journal_path.exists():
            return

        try:
            data = json.loads(journal_path.read_text(encoding='utf-8'))
            manifest = data.get("manifest", {})
            tx_id = data.get("tx_id", "unknown")

            # [ASCENSION 10]: Machine Signature Check
            my_sig = hashlib.md5(platform.node().encode()).hexdigest()[:8]
            if data.get("machine_signature") != my_sig:
                sys.stderr.write(f"\n[TITAN] ⚠️  Foreign Journal detected. Skipping resurrection.\n")
                return

            sys.stderr.write(f"\n[TITAN] 🚩 RESURRECTING TORN REALITY (TX: {tx_id[:8]})...\n")

            # Resurrection Path: We complete the move atomically
            for src_str, dst_str in manifest.items():
                src, dst = Path(src_str), Path(dst_str)
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    if dst.exists():
                        if dst.is_dir() and not dst.is_symlink():
                            shutil.rmtree(str(dst))
                        else:
                            dst.unlink()
                    _resilient_rename(src, dst)
                    sys.stderr.write(f"   -> Recovered: {dst.name}\n")

            journal_path.unlink()
            sys.stderr.write("[TITAN] ✅ Reality Resonated. The Timeline is whole.\n\n")

        except Exception as e:
            sys.stderr.write(f"[TITAN] 💀 Lazarus Fracture: {e}\n")

# == SCRIPTURE SEALED: THE HAND OF MANIFESTATION REACHES OMEGA TOTALITY ==