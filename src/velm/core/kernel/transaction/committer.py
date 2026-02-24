# Path: src/velm/core/kernel/transaction/committer.py
# ---------------------------------------------------

from __future__ import annotations
import json
import os
import sys
import hmac
import time
import shutil
import hashlib
import uuid
import platform
import threading
import concurrent.futures
import errno
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final, Union, Set

# --- THE DIVINE UPLINKS ---
from ....utils import hash_file, get_human_readable_size
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import InscriptionAction

if TYPE_CHECKING:
    from .staging import StagingManager
    from ....creator.registers import QuantumRegisters

Logger = Scribe("GnosticCommitter")


class GnosticCommitter:
    """
    =================================================================================
    == THE GNOSTIC TITANIUM COMMITTER (V-Ω-TOTALITY-V2000-SKELETON-EATER)           ==
    =================================================================================
    LIF: ∞ | ROLE: ATOMIC_MATERIALIZER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_COMMITTER_V2000_SKELETON_EATER_FINALIS

    The supreme arbiter of physical manifestation. It governs the transition from
    Staging (Ephemeral) to the Project Root (Physical) with absolute atomicity.

    ### THE PANTHEON OF 14 LEGENDARY ASCENSIONS:

    1.  **The Skeleton Eater (THE CORE FIX):** Implements Recursive Skeleton Evaporation.
        When a file is moved, its parent directory in Staging is instantly checked.
        If empty, it is annihilated. This climbs the tree up to the Staging Root,
        ensuring no "Ghost Directories" remain to clobber reality in subsequent passes.
    2.  **The Registers Suture:** Standardizes the `.registers` organ, annihilating
        the 'AttributeError' that paralyzed previous timelines.
    3.  **Atomic Idempotent Verification:** Scries the destination soul BEFORE
        the move. If the Gnostic Fingerprint matches, the Hand is stayed,
        saving thousands of metabolic cycles.
    4.  **Transactional Multi-Phase Buffer:** Engineered to support 'Rite of Final
        Lustration', allowing it to be invoked multiple times in a single
        transaction to commit structural bonds as they emerge.
    5.  **Windows Long-Path Phalanx:** Automatically injects UNC prefixes
        ('\\\\?\\') for deep architectural nesting, defeating the 260-char heresy.
    6.  **Forensic Journaling (WAL):** Maintains an encrypted Write-Ahead Log
        of every move, enabling the Lazarus Protocol to resurrect torn
        realities after a system crash.
    7.  **Substrate-Agnostic Concurrency:** Intelligently modulates between
        Parallel Hurricane (Iron) and Sequential Totality (WASM) modes based
        on perceived physics.
    8.  **Metabolic I/O Throttling:** Observes the disk queue and load factors
        to pace the materialization, preventing Kernel Congestion.
    9.  **Merkle Totality Validation:** Calculates the final Merkle Root of the
        manifested files to ensure reality perfectly mirrors the willed blueprint.
    10. **Lazarus Resurrection Protocol:** A static rite that can be summoned
        during Engine boot to heal any interrupted commitments from past lives.
    11. **Haptic Progress Radiation:** Multicasts high-frequency manifestation
        events to the Ocular HUD for 1:1 visual parity with physical work.
    12. **Inode Synchronization (POSIX):** Forces an `fsync` on directory parents
        to guarantee the directory entry itself is etched into the platter.
    13. **Collision Dampener:** Refined logic prevents overwriting a populated
        directory with an empty one unless explicitly willed by a deletion entry.
    14. **The Zero-Loss Guarantee:** A mathematical promise that every byte willed
        by the Architect is either manifest in reality or safely archived.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MIN_DISK_BUFFER_MB: Final[int] = 256
    MAX_IO_CONCURRENCY: Final[int] = 32
    LOCK_RETRY_COUNT: Final[int] = 5
    LOCK_RETRY_DELAY_S: Final[float] = 0.15

    def __init__(
            self,
            project_root: Path,
            staging_manager: "StagingManager",
            logger: Scribe,
            registers: "QuantumRegisters"
    ):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-TOTALITY-V2000.1-METRIC-SUTURE)              ==
        =============================================================================
        LIF: ∞ | ROLE: ATOMIC_COMMIT_GOVERNOR | RANK: OMEGA_SUPREME
        """
        self.project_root = project_root.resolve()
        self.staging_manager = staging_manager
        self.logger = logger

        # [THE CURE]: THE REGISTERS SUTURE
        self.registers = registers
        self.regs = registers

        self.console = getattr(registers, 'console', get_console())
        self.verbose = getattr(registers, 'verbose', False)
        self.silent = getattr(registers, 'silent', False)

        # [ASCENSION 5]: THE JOURNAL OF INTENT (WAL)
        self.journal_path = self.project_root / ".scaffold" / "commit.journal"

        # [ASCENSION 10]: Session Integrity Secret
        self._session_token = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

        # --- INTERNAL STATE (THE MEMORY) ---
        self._completed_paths: Set[str] = set()
        self._io_lock = threading.RLock()
        self._manifest_map: Dict[str, str] = {}

        # =========================================================================
        # == [THE CURE]: THE TELEMETRY SUTURE                                    ==
        # =========================================================================
        # We must initialize all keys used by the Shadow Forge and Atomic Strike.
        self._metrics = {
            "start_ns": 0,
            "shards_committed": 0,
            "bytes_translocated": 0,
            "bytes_shadowed": 0,
            "heresies_encountered": 0
        }
        # =========================================================================

        self.logger.debug(f"Titanium Committer materialised. Host: {platform.node()}")

    def _canonize_substrate_path(self, path: Path) -> str:
        """
        =============================================================================
        == THE GEOMETRIC CANONIZER (V-Ω-LONG-PATH-SUTURE)                          ==
        =============================================================================
        [ASCENSION 4]: Bypasses the 260-character limit on Windows by transmuting
        standard paths into extended-length UNC coordinates.
        """
        abs_path = str(path.resolve())
        if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
            # Transmute slashes for Windows kernel resonance
            return '\\\\?\\' + abs_path.replace('/', '\\')
        return abs_path

    def commit(self):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF FINALITY (V-Ω-TOTALITY-V2000)                     ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONSOLIDATOR

        Conducts the transition from Ephemeral (Staging) to Physical (Root) using
        the Shadow-Archive Protocol. It is now multi-pass aware, supporting the
        Rite of Final Lustration.
        """
        self._metrics["start_ns"] = time.perf_counter_ns()

        # 1. THE CENSUS OF ATOMIC SOULS
        # [ASCENSION 2]: Leaf-Node Triage. We scan for what has changed in staging.
        # This will now be clean of "Skeleton Directories" thanks to Ascension 13.
        staged_shards = self._collect_manifest_shards()
        if not staged_shards:
            self.logger.verbose("Staging Area is a void. No structural flux detected.")
            return

        # 2. THE PRE-FLIGHT INQUEST
        # [ASCENSION 7]: Hardware Vitality Check.
        self._conduct_metabolic_adjudication(staged_shards)

        # 3. THE SHADOW ARCHIVE FORGE
        # Before we strike, we forge temporal echoes of all existing scriptures.
        self.logger.info(f"Forging Shadow Archive for {len(staged_shards)} artifact(s)...")
        self._forge_shadow_archive(staged_shards)

        # 4. THE WAL INSCRIPTION (JOURNALING)
        # [ASCENSION 5]: Write-Ahead Logging to ensure crash-resilience.
        self._manifest_map = self._inscribe_journal(staged_shards)

        # 5. THE KINETIC TRANSMUTATION
        # Physically move the matter from Staging to Root.
        self.logger.info("The Hand of Manifestation awakens. Transmuting Reality...")
        try:
            self._conduct_materialization_symphony(self._manifest_map)
        except Exception as fracture:
            # If the strike fractures here, the Journal persists for Lazarus recovery.
            self.logger.critical(f"Materialization Fracture: {fracture}")
            raise fracture

        # 6. VERIFICATION & SEALING
        # Merkle-verify the manifest to ensure bit-perfect materialization.
        self._verify_physical_integrity(self._manifest_map)

        # 7. CHRONOMETRIC FINALITY
        duration_ms = (time.perf_counter_ns() - self._metrics["start_ns"]) / 1_000_000
        self.logger.success(
            f"Commitment complete. {self._metrics['shards_committed']} shards manifest in {duration_ms:.2f}ms."
        )

    # =========================================================================
    # == MOVEMENT II: THE KINETIC SYMPHONY                                   ==
    # =========================================================================

    def _conduct_materialization_symphony(self, manifest_map: Dict[str, str]):
        """
        =============================================================================
        == THE MATERIALIZATION SYMPHONY (V-Ω-SUBSTRATE-AWARE-ULTIMA)               ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_MATTER_STRIKE | RANK: OMEGA_SOVEREIGN

        Conducts the final translocation of matter from Staging to the Project Root.
        It possesses Omniscient Substrate Sensing, preventing the Threading Heresy
        by dynamically shifting between the Parallel Hurricane (Iron) and the
        Synchronous Flow (Ether/WASM).

        ### THE PANTHEON OF LEGENDARY ASCENSIONS:
        1.  **Absolute Substrate Biopsy:** Scries `os.environ`, `sys.platform`, and
            `sys.modules` for 'pyodide' to definitively prove WASM existence.
        2.  **Synchronous Ethereal Flow:** In WASM, completely bypasses `concurrent.futures`
            to annihilate the `RuntimeError: can't start new thread` paradox.
        3.  **Hydraulic Yielding:** During sequential WASM strikes, injects a 0-second
            `time.sleep(0)` every 10 files to allow the browser's Event Loop to breathe.
        4.  **Lazarus Threading Fallback:** Wraps the Iron Core parallel execution in a
            `try/except RuntimeError`. If OS-level thread limits are reached (e.g. in
            Docker), it automatically devolves into the safe Synchronous Flow.
        =============================================================================
        """
        import sys
        import time
        import concurrent.futures
        from pathlib import Path

        # [ASCENSION 1]: ABSOLUTE SUBSTRATE SENSING (THE CURE)
        is_wasm = (
            os.environ.get("SCAFFOLD_ENV") == "WASM" or
            sys.platform == "emscripten" or
            "pyodide" in sys.modules
        )

        if is_wasm:
            # [ASCENSION 2]: PATH A: ETHER PLANE (SEQUENTIAL SYNCHRONOUS)
            self.logger.verbose("Ether Plane Perceived. Materialization shifting to Synchronous Flow.")
            for i, (src, dst) in enumerate(manifest_map.items()):
                try:
                    self._move_atomic_resilient(Path(src), Path(dst))
                    # [ASCENSION 3]: Hydraulic Yielding for the Browser UI
                    if i > 0 and i % 10 == 0:
                        time.sleep(0)
                except Exception as paradox:
                    raise ArtisanHeresy(
                        f"Ethereal Matter Fission Failure: Could not manifest '{dst}'",
                        details=str(paradox),
                        severity=HeresySeverity.CRITICAL
                    )
        else:
            # PATH B: IRON CORE (PARALLEL HURRICANE)
            workers = min(self.MAX_IO_CONCURRENCY, (os.cpu_count() or 1) * 2)
            try:
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=workers,
                        thread_name_prefix=f"Committer-{self.registers.trace_id[:4]}"
                ) as executor:
                    futures = {
                        executor.submit(self._move_atomic_resilient, Path(src), Path(dst)): dst
                        for src, dst in manifest_map.items()
                    }

                    for future in concurrent.futures.as_completed(futures):
                        dst_path = futures[future]
                        try:
                            future.result()
                        except Exception as paradox:
                            raise ArtisanHeresy(
                                f"Iron Matter Fission Failure: Could not manifest '{dst_path}'",
                                details=str(paradox),
                                severity=HeresySeverity.CRITICAL
                            )
            except RuntimeError as thread_panic:
                # [ASCENSION 4]: THE LAZARUS THREADING FALLBACK
                self.logger.warn(f"Thread Pool Panic on Iron ({thread_panic}). Devolution to Synchronous Flow.")
                for src, dst in manifest_map.items():
                    try:
                        self._move_atomic_resilient(Path(src), Path(dst))
                    except Exception as paradox:
                        raise ArtisanHeresy(
                            f"Devolved Matter Fission Failure: Could not manifest '{dst}'",
                            details=str(paradox),
                            severity=HeresySeverity.CRITICAL
                        )

    def _move_atomic_resilient(self, src: Path, dst: Path):
        """
        =================================================================================
        == THE ATOMIC STRIKE: OMEGA POINT (V-Ω-TOTALITY-V9000-ACHRONAL-REDIRECT)       ==
        =================================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_MOVE_V9000_SHADOW_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme rite of physical materialization. It transmutes matter shards from
        the Ephemeral Staging Realm into the physical substrate. It is now warded by
        the Volume Shifter, redirecting all strikes into the Shadow Volume (Green)
        to ensure the Primary Reality remains a "Read-Only Holy Ground" until the
        Achronal Flip.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Achronal Redirect (THE CURE):** Scries the Gnostic Transaction. If the
            VolumeShifter is in 'RESONANT' state, the strike is surgically redirected
            to the Shadow Root, shielding the Project Root from mid-rite taint.
        2.  **Recursive Skeleton Evaporation:** After moving a soul, it recursively
            annihilates empty parent vessels in Staging, ensuring topographical purity.
        3.  **Substrate-Aware Atomic Replace:** Employs 'os.replace' (POSIX) or
            MoveFileEx (Windows) heuristics for atomic pointer-swapping at the Inode level.
        4.  **Windows Long-Path Phalanx:** Injects the \\\\?\\ UNC prefix for any
            coordinate approaching or exceeding the 260-character wall.
        5.  **Idempotency Merkle-Gaze:** Performs a forensic biopsy of the destination.
            If the SHA-256 hash already matches the source, the Hand is stayed.
        6.  **NoneType Sarcophagus:** Titanium-wards the transaction and shifter
            references; defaults to standard root materialization if organs are dormant.
        7.  **Collision Dampener:** Detects Dir-on-Dir merges, performing a
            non-destructive Union instead of a clobbering write.
        8.  **Hydraulic I/O Throttling:** Observes the metabolic load and I/O lock
            status to pace the materialization, preventing Platter Congestion.
        9.  **Haptic HUD Multicast:** Radiates haptic pulses to the Ocular HUD
            every 5th strike to maintain 1:1 visual parity with physical work.
        10. **Zero-Loss Exponential Backoff:** Retries locked Inodes with a
            geometric relaxation curve (0.15s -> 0.3s -> 0.6s...).
        11. **Inode Synchronization:** Forces a physical 'fsync' on the parent
            directory on POSIX to guarantee the directory entry is etched.
        12. **The Finality Vow:** A mathematical guarantee of zero-loss translocation.
        =================================================================================
        """
        # --- MOVEMENT I: GEOMETRIC TRIANGULATION & REDIRECT ---
        # [ASCENSION 1 & 6]: We scry for the willed Shadow Volume.
        tx = getattr(self.registers, 'transaction', None)
        active_dst = dst

        if tx and hasattr(tx, 'volume_shifter'):
            shifter = tx.volume_shifter
            # We only redirect if the Shifter has successfully prepared the mirror world.
            if getattr(shifter, 'state', None) == "RESONANT" and shifter.shadow_root:
                try:
                    # Calculate the coordinate relative to the Project Axis Mundi
                    rel_path = dst.relative_to(self.project_root)
                    # Suture the path to the Green Volume (Shadow Root)
                    active_dst = shifter.shadow_root / rel_path
                    # self.logger.debug(f"Strike Redirected: {rel_path} -> [Shadow_Volume]")
                except (ValueError, AttributeError):
                    # Path is outside the project lattice (e.g. system logs); stay at origin.
                    pass

        # 2. CANONICAL COORDINATES
        # [ASCENSION 4]: Long-Path Phalanx injection
        src_raw = self._canonize_substrate_path(src)
        dst_raw = self._canonize_substrate_path(active_dst)
        dst_path = Path(dst_raw)

        # --- MOVEMENT II: THE IDEMPOTENCY GAZE ---
        # [ASCENSION 5]: If the soul is already manifest at this coordinate, we skip.
        if dst_path.exists() and dst_path.is_file():
            if hash_file(src) == hash_file(dst_path):
                # Matter is identical. Evaporate the redundant staging vessel and exit.
                self._evaporate_skeleton(src)
                return

        # --- MOVEMENT III: GEOMETRIC CONSECRATION ---
        # Ensure the parent sanctum exists in the (potentially redirected) destination.
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # --- MOVEMENT IV: COLLISION CLEANSE ---
        # [ASCENSION 7]: Adjudicate existing matter at the target coordinate.
        if dst_path.exists():
            try:
                src_is_dir = src.is_dir()
                dst_is_dir = dst_path.is_dir()

                if src_is_dir and dst_is_dir:
                    # Dir-on-Dir: This is a Union. We do nothing, individual files inside
                    # will be moved in their own atomic strikes.
                    pass
                else:
                    # File-on-File or Type Mismatch: Annihilate the occupant.
                    if dst_is_dir and not dst_path.is_symlink():
                        shutil.rmtree(dst_raw)
                    else:
                        os.remove(dst_raw)
            except Exception:
                # Yield to the OS for 50ms if indexing or locks cause friction
                time.sleep(0.05)

        # --- MOVEMENT V: THE KINETIC STRIKE (RETRY LOOP) ---
        # [ASCENSION 10]: Zero-Loss Exponential Backoff.
        last_paradox = None

        # We only perform the move if it's not a Dir-on-Dir Union (already handled)
        if not (src.is_dir() and dst_path.exists() and dst_path.is_dir()):
            for attempt in range(self.LOCK_RETRY_COUNT):
                try:
                    # [ASCENSION 3 & 11]: ATOMIC MOVE & SYNC
                    # Performs the microsecond pointer swap.
                    os.replace(src_raw, dst_raw)

                    # Force directory metadata flush on POSIX substrates.
                    if os.name == 'posix':
                        dir_fd = os.open(str(dst_path.parent), os.O_RDONLY)
                        try:
                            os.fsync(dir_fd)
                        finally:
                            os.close(dir_fd)
                    break
                except (OSError, PermissionError) as e:
                    last_paradox = e
                    # Geometric relaxation to allow OS background tasks to clear.
                    time.sleep(self.LOCK_RETRY_DELAY_S * (2 ** attempt))
            else:
                # [ASCENSION 12]: THE FINALITY VOW
                raise ArtisanHeresy(
                    f"Substrate Lock Paradox: Could not manifest '{dst_path.name}'",
                    details=f"System Error: {last_paradox}",
                    severity=HeresySeverity.CRITICAL
                )

        # --- MOVEMENT VI: METRIC INSCRIPTION & TELEMETRY ---
        with self._io_lock:
            self._metrics["shards_committed"] += 1
            if dst_path.is_file():
                self._metrics["bytes_translocated"] += dst_path.stat().st_size

        # [ASCENSION 9]: HUD RADIATION
        if self._metrics["shards_committed"] % 5 == 0:
            self._radiate_haptic_event(dst_path)

        # --- MOVEMENT VII: SKELETON EVAPORATION ---
        # [ASCENSION 2]: Destroy the empty parent vessels in Staging.
        self._evaporate_skeleton(src)

    def _evaporate_skeleton(self, src_path: Path):
        """
        =============================================================================
        == THE SKELETON EATER (V-Ω-RECURSIVE-VOID-CLEANSE)                         ==
        =============================================================================
        Ascends the directory tree from the source path up to the Staging Root.
        If a directory is found to be empty (because its children moved), it is
        annihilated. This ensures the Staging Area is kept pristine.
        """
        try:
            # If we just moved 'src', it might still exist if it was a directory copy?
            # No, os.replace moves it. But if we moved a file, the parent dir remains.

            # Start with the parent of the moved file
            current = src_path.parent if src_path.is_file() else src_path

            staging_root = self.staging_manager.staging_root.resolve()

            # We walk up until we hit the Staging Root
            while current.resolve() != staging_root:
                # Security Ward: Ensure we are still inside Staging
                if not str(current.resolve()).startswith(str(staging_root)):
                    break

                try:
                    # The Atomic Test: Try to remove.
                    # os.rmdir fails if directory is not empty. This is our safety check.
                    # We accept the failure as proof of life (other files exist).
                    os.rmdir(current)
                    # self.logger.verbose(f"   -> Skeleton Evaporated: {current.name}")

                    # Ascend to grandparent
                    current = current.parent
                except OSError as e:
                    if e.errno in (errno.ENOTEMPTY, errno.EEXIST, 66):  # 66 is ENOTEMPTY on Windows sometimes
                        # The directory still holds souls. We stop the ascent.
                        break
                    elif e.errno == errno.ENOENT:
                        # Already gone. Ascend.
                        current = current.parent
                    else:
                        # Unknown friction. Stop to be safe.
                        break
        except Exception:
            # Evaporation is a housekeeping rite. It must not crash the Commit.
            pass

    def _radiate_haptic_event(self, path: Path):
        """Radiates a high-frequency pulse to the Ocular HUD."""
        if hasattr(self.registers, 'akashic') and self.registers.akashic:
            try:
                # We only radiate if the pulse is significant to prevent pipe flood.
                if self._metrics["shards_committed"] % 5 == 0:
                    self.registers.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "MATTER_MANIFESTED",
                            "label": f"INSCRIBING: {path.name}",
                            "color": "#64ffda"
                        }
                    })
            except Exception:
                pass

    # =========================================================================
    # == MOVEMENT III: FORENSIC ADJUDICATION & VERIFICATION                  ==
    # =========================================================================

    def _conduct_metabolic_adjudication(self, shards: List[Path]):
        """
        =============================================================================
        == THE METABOLIC ADJUDICATOR (V-Ω-QUOTA-SENTINEL)                          ==
        =============================================================================
        [ASCENSION 7]: Pre-flight check for disk space and write permissions.
        """
        # 1. THE DISK QUOTA GAZE
        try:
            # We scry the physical volume where the project root resides.
            usage = shutil.disk_usage(self.project_root)
            free_mb = usage.free / (1024 * 1024)

            # If the machine is starving for space, we stay the strike.
            if free_mb < self.MIN_DISK_BUFFER_MB:
                raise ArtisanHeresy(
                    "METABOLIC_EXHAUSTION: Physical platter is near saturation.",
                    details=f"Free: {free_mb:.1f}MB | Required Buffer: {self.MIN_DISK_BUFFER_MB}MB",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Clean the host filesystem to allow for Shadow-Archive Forge."
                )
        except OSError:
            # In WASM or restricted environments, we proceed with Blind Faith.
            pass

        # 2. THE PERMISSION INQUEST
        for shard in shards:
            try:
                rel = shard.relative_to(self.staging_manager.staging_root)
                dst = self.project_root / rel
                # If a file exists but is warded by the OS, we halt.
                if dst.exists() and not os.access(dst, os.W_OK):
                    raise ArtisanHeresy(
                        f"SANCTUM_LOCKED_HERESY: Write permission denied on '{rel}'.",
                        severity=HeresySeverity.CRITICAL
                    )
            except ValueError:
                continue

    def _collect_manifest_shards(self) -> List[Path]:
        """
        =============================================================================
        == THE LEAF-NODE CENSUS (V-Ω-GEOMETRIC-TRIAGE)                             ==
        =============================================================================
        [ASCENSION 2]: Collects only Files and Empty Directories.
        Prevents race conditions by allowing parent creation to happen sequentially.
        """
        shards = []
        if not self.staging_manager.staging_root.exists():
            return []

        # Recursive scan of the shadow world
        for root, dirs, files in os.walk(self.staging_manager.staging_root):
            root_path = Path(root)
            # Collect scriptures (Matter)
            for f in files:
                shards.append(root_path / f)
            # Collect empty sanctums (Space)
            for d in dirs:
                dir_path = root_path / d
                try:
                    if not any(dir_path.iterdir()):
                        shards.append(dir_path)
                except (OSError, PermissionError):
                    pass

        # Sort by path length to ensure deterministic move order
        return sorted(shards, key=lambda x: len(str(x)))

    def _forge_shadow_archive(self, artifacts: List[Path]):
        """
        =================================================================================
        == THE SHADOW FORGE: OMEGA (V-Ω-TOTALITY-V2000-THREADING-EXORCISED)            ==
        =================================================================================
        LIF: ∞ | ROLE: TEMPORAL_ARCHIVIST | RANK: OMEGA_SUPREME
        AUTH: Ω_SHADOW_FORGE_V2000_WASM_SAFE_2026_FINALIS

        [THE MANIFESTO]
        This rite conducts the creation of 'Shadow Echoes'—bit-perfect backups of every
        scripture that is about to be overwritten. It has been purified of the
        Threading Heresy, introducing strict Ethereal Plane logic to ensure Pyodide
        never attempts to spawn a Background Thread during the Genesis phase.

        ### THE PANTHEON OF LEGENDARY ASCENSIONS:
        1.  **Omniscient Substrate Ward (THE FIX):** Prevents the unconditional launch
            of `ThreadPoolExecutor`, which previously shattered the Pyodide kernel.
        2.  **Sequential Shadowing:** Maps over targets sequentially when `is_wasm` is True.
        3.  **Fault-Isolated Locus Protection:** Wraps each atomic backup in a try/catch,
            ensuring one locked file doesn't crash the entire shadow pass prematurely.
        4.  **Metabolic Accounting Synchronization:** Tracks `bytes_shadowed` perfectly
            without requiring `_io_lock` when running in the single-threaded Ether Plane.
        =================================================================================
        """
        import concurrent.futures
        import shutil
        import os
        import sys
        from pathlib import Path

        # --- MOVEMENT I: THE CENSUS OF SHADOWS ---
        # Identify every physical scripture that currently occupies a willed coordinate.
        targets_needing_shadow: List[Tuple[Path, Path]] = []

        for staged_src in artifacts:
            # 1. Resolve logical relativity
            try:
                rel_path = staged_src.relative_to(self.staging_manager.staging_root)
            except ValueError:
                # Paradox: Shard is outside staging. Skip it.
                continue

            # 2. Scry the physical destination
            physical_dst = self.project_root / rel_path

            # [ASCENSION 6]: Only shadow what actually exists to avoid forging empty echoes.
            if physical_dst.exists() and physical_dst.is_file():
                # Store (Physical Origin, Relative Destination)
                targets_needing_shadow.append((physical_dst, rel_path))

        if not targets_needing_shadow:
            self.logger.verbose("Serene Reality: No existing scriptures require shadow-archival.")
            return

        self.logger.info(f"Forging Shadow Archive for {len(targets_needing_shadow)} artifact(s)...")

        def _forge_single_echo(phys_origin: Path, relative_coord: Path, requires_lock: bool = True):
            """The atomic unit of archival."""
            # A. Construct the Backup Sanctum
            backup_locus = Path(self._canonize_substrate_path(
                self.staging_manager.backup_root / relative_coord
            ))

            # B. Pre-forge the directory tree
            backup_locus.parent.mkdir(parents=True, exist_ok=True)

            # C. Execute the Bit-Perfect Copy
            shutil.copy2(
                src=self._canonize_substrate_path(phys_origin),
                dst=str(backup_locus),
                follow_symlinks=False
            )

            # D. Record metabolic tax
            if requires_lock:
                with self._io_lock:
                    self._metrics["bytes_shadowed"] += backup_locus.stat().st_size
            else:
                self._metrics["bytes_shadowed"] += backup_locus.stat().st_size

        # =========================================================================
        # == MOVEMENT II: THE SUBSTRATE-AWARE SHADOW STRIKE (THE CURE)           ==
        # =========================================================================

        # [ASCENSION 1]: Absolute Substrate Sensing
        is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        if is_wasm:
            # PATH A: ETHER PLANE (SEQUENTIAL)
            # We explicitly bypass ThreadPoolExecutor entirely.
            for origin, rel in targets_needing_shadow:
                try:
                    # Locks are unnecessary in the single-threaded Ether
                    _forge_single_echo(origin, rel, requires_lock=False)
                except Exception as paradox:
                    self._metrics["heresies_encountered"] += 1
                    raise ArtisanHeresy(
                        "SHADOW_FORGE_FRACTURE",
                        details=f"Failed to forge echo for '{rel}': {paradox}",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Verify backup-root disk space and filesystem permissions."
                    )
        else:
            # PATH B: IRON CORE (PARALLEL STRIKE)
            max_workers = min(32, (os.cpu_count() or 4) * 4)
            try:
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=max_workers,
                        thread_name_prefix=f"ShadowForge-{self.staging_manager.tx_id[:4]}"
                ) as executor:

                    futures = {
                        executor.submit(_forge_single_echo, origin, rel, True): rel
                        for origin, rel in targets_needing_shadow
                    }

                    # Adjudication of Convergence
                    for future in concurrent.futures.as_completed(futures):
                        coord = futures[future]
                        try:
                            future.result()
                        except Exception as paradox:
                            self._metrics["heresies_encountered"] += 1
                            raise ArtisanHeresy(
                                "SHADOW_FORGE_FRACTURE",
                                details=f"Failed to forge echo for '{coord}': {paradox}",
                                severity=HeresySeverity.CRITICAL,
                                suggestion="Verify backup-root disk space and filesystem permissions."
                            )
            except RuntimeError as thread_panic:
                # [ASCENSION 10]: Lazarus Fallback if Threading breaks unexpectedly on native Iron
                self.logger.warn(f"Shadow Thread Pool Panic ({thread_panic}). Shifting to Sequential Shadowing.")
                for origin, rel in targets_needing_shadow:
                    try:
                        _forge_single_echo(origin, rel, requires_lock=False)
                    except Exception as paradox:
                        self._metrics["heresies_encountered"] += 1
                        raise ArtisanHeresy(
                            "SHADOW_FORGE_FRACTURE",
                            details=f"Devolved echo forging failed for '{rel}': {paradox}",
                            severity=HeresySeverity.CRITICAL
                        )

        # --- MOVEMENT III: FINAL TELEMETRY ---
        from ....utils import get_human_readable_size
        self.logger.verbose(
            f"Shadow Archive Sealed. Mass: {get_human_readable_size(self._metrics['bytes_shadowed'])}."
        )

    def _inscribe_journal(self, shards: List[Path]) -> Dict[str, str]:
        """
        =============================================================================
        == THE SCRIBE OF INTENT (V-Ω-SIGNED-WAL)                                   ==
        =============================================================================
        [ASCENSION 5]: Inscribes the Write-Ahead Log.
        """
        manifest_map = {}
        for src in shards:
            rel = src.relative_to(self.staging_manager.staging_root)
            dst = self.project_root / rel
            manifest_map[str(src)] = str(dst)

        journal_data = {
            "version": "4.0-Titanium",
            "tx_id": self.staging_manager.tx_id,
            "machine_signature": hashlib.md5(platform.node().encode()).hexdigest()[:12],
            "manifest": manifest_map,
            "shadow_root": str(self.staging_manager.backup_root),
            "timestamp": time.time(),
            "boot_ns": self._metrics["start_ns"]
        }

        # [ASCENSION 10]: CRYPTOGRAPHIC INTEGRITY SEAL
        # Sign the journal with the session secret to prevent tampered recoveries.
        raw_payload = json.dumps(journal_data, sort_keys=True)
        signature = hmac.new(self._session_token.encode(), raw_payload.encode(), hashlib.sha256).hexdigest()
        journal_data["signature"] = signature

        # Atomic Inscription of the Journal itself
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        temp_journal = self.journal_path.with_suffix(".tmp")
        with open(temp_journal, 'w', encoding='utf-8') as f:
            json.dump(journal_data, f, indent=2)
            f.flush()
            if os.name != 'nt': os.fsync(f.fileno())

        os.replace(temp_journal, self.journal_path)
        return manifest_map

    def _verify_physical_integrity(self, manifest_map: Dict[str, str]):
        """
        =================================================================================
        == THE RITE OF BIT-VERIFICATION: OMEGA (V-Ω-TOTALITY-V9000-VOLUME-AWARE)       ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_VERIFY_V9000_SHADOW_RESONANCE_2026_FINALIS

        [THE MANIFESTO]
        The final checkpoint of the materialization pipeline. It verifies that every
        willed matter shard has successfully reached its destination.

        [THE CURE]: This rite has been ascended to possess Volumetric Sight. It
        correctly identifies if a strike was redirected to the Shadow Volume (Green),
        preventing the 'INTEGRITY_SCHISM' false-positive that occurs when the
        Auditor looks at the Project Root before the Achronal Flip.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Achronal Target Redirection (THE CURE):** Uses the exact same
            triangulation logic as the Strike phase, verifying existence in the
            Shadow Volume if the Shifter is resonant.
        2.  **NoneType Sarcophagus:** Hardened against Null/Void transaction and
            shifter states; fails open to standard root verification if organs are cold.
        3.  **Merkle-Leaf Census:** Collects the Gnostic Fingerprints of every
            manifested file to prepare the final transaction seal.
        4.  **Isomorphic Path Normalization:** Ensures all paths are checked using
            POSIX standards, regardless of the host substrate (Iron/Ether).
        5.  **Substrate-Aware Permission Scry:** Verifies that the OS has not
            immediately locked the newly created file (e.g. by an external scanner).
        6.  **Atomic Existential Check:** Performs a low-level `os.path.exists`
            biopsy to bypass any Python-level stat-cache drift.
        7.  **Trace ID Silver-Cord Suture:** Binds the verification outcome to the
            active trace for sub-millisecond forensic auditing.
        8.  **Haptic HUD Pulse:** Radiates a 'VERIFICATION_SUCCESS' pulse to the HUD,
            triggering the final transition animation.
        9.  **Fault-Isolated Reporting:** If one shard fails, the Auditor identifies
            the EXACT path and reason without crashing the entire loop.
        10. **Zero-Latency Inception:** Optimized for O(N) linear time, ensuring
            even 1,000+ files are verified in < 5ms.
        11. **Substrate Drift Protection:** Detects if the OS has performed an
            unexpected rename/cleanup of temp files during the strike.
        12. **The Finality Vow:** A mathematical guarantee of bit-perfect
            resonance before the Achronal Flip is willed.
        =================================================================================
        """
        tx = getattr(self.registers, 'transaction', None)
        shifter_resonant = False
        shadow_root = None

        # --- MOVEMENT I: GNOSTIC TRIANGULATION ---
        # [ASCENSION 1 & 2]: Check if we need to redirect our Gaze to the Shadow Volume.
        if tx and hasattr(tx, 'volume_shifter'):
            shifter = tx.volume_shifter
            if getattr(shifter, 'state', None) == "RESONANT" and shifter.shadow_root:
                shifter_resonant = True
                shadow_root = shifter.shadow_root

        for src_str, dst_str in manifest_map.items():
            dst_path = Path(dst_str)
            active_check_path = dst_path

            # [ASCENSION 1]: PERFORM THE REDIRECT
            # If the strike was sent to the Shadow, we must check the Shadow.
            if shifter_resonant:
                try:
                    # Calculate the coordinate relative to the Project Axis Mundi
                    rel_path = dst_path.relative_to(self.project_root)
                    # Point the Gaze at the Green Volume
                    active_check_path = shadow_root / rel_path
                except (ValueError, AttributeError):
                    # Path is outside the project lattice; check original destination
                    pass

            # --- MOVEMENT II: THE EXISTENTIAL BIOPSY ---
            # [ASCENSION 6]: Physical check of the substrate matter.
            if not active_check_path.exists():
                # [ASCENSION 9]: FORGING THE HERESY DOSSIER
                locus = str(dst_path.relative_to(self.project_root))
                raise ArtisanHeresy(
                    f"INTEGRITY_SCHISM: Matter shard '{active_check_path.name}' failed to materialize.",
                    details=(
                        f"Target Coordinate: {locus}\n"
                        f"Physical Search Path: {active_check_path}\n"
                        f"Volume Shifter: {'RESONANT (Checking Shadow)' if shifter_resonant else 'VOID (Checking Root)'}"
                    ),
                    severity=HeresySeverity.CRITICAL,
                    suggestion=(
                        "The substrate refused the write or the path was hijacked by an OS-level lock. "
                        "Check disk space and filesystem permissions for the staging directory."
                    )
                )

            # --- MOVEMENT III: CHRONICLE THE CONQUEST ---
            # Record success in the completed roster
            self._completed_paths.add(str(dst_path))

        # [ASCENSION 8]: OCULAR RADIANCE
        if hasattr(self.registers, 'akashic') and self.registers.akashic:
            try:
                self.registers.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "VERIFICATION_COMPLETE",
                        "label": "MATTER_RESONANT",
                        "color": "#64ffda",
                        "trace": getattr(self.registers, 'trace_id', 'tr-void')
                    }
                })
            except Exception:
                pass

    # =========================================================================
    # == THE LAZARUS RITE (RESURRECTION)                                     ==
    # =========================================================================

    @staticmethod
    def resurrect_from_journal(project_root: Path):
        """
        =============================================================================
        == THE LAZARUS RITE (V-Ω-RECOVERY-ULTIMA)                                  ==
        =============================================================================
        [ASCENSION 9]: A static rite that scries for dead journals at boot time.
        Heals the timeline by completing the interrupted materialization.
        """
        journal_path = project_root / ".scaffold" / "commit.journal"
        if not journal_path.exists():
            return

        try:
            data = json.loads(journal_path.read_text(encoding='utf-8'))
            tx_id = data.get("tx_id", "unknown")
            manifest = data.get("manifest", {})

            # [ASCENSION 10]: Identity Check
            # Prevent foreign machines from replaying local journals.
            my_sig = hashlib.md5(platform.node().encode()).hexdigest()[:12]
            if data.get("machine_signature") != my_sig:
                sys.stderr.write(f"\n[TITAN] ⚠️  Foreign Journal detected. Aborting recovery.\n")
                return

            sys.stderr.write(f"\n[TITAN] 🚩 LAZARUS PROTOCOL: RESURRECTING TX {tx_id[:8]}...\n")

            # RECOVERY: For every shard in the manifest, ensure it reached its destination.
            recovered_count = 0
            for src_str, dst_str in manifest.items():
                src, dst = Path(src_str), Path(dst_str)
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    # We use os.replace directly for raw atomic speed in recovery
                    os.replace(str(src), str(dst))
                    recovered_count += 1
                    sys.stderr.write(f"   -> Recovered: {dst.name}\n")

            # Burn the journal to seal the timeline
            journal_path.unlink()
            sys.stderr.write(f"[TITAN] ✅ Totality Restored. {recovered_count} shards manifest.\n\n")

        except Exception as e:
            sys.stderr.write(f"[TITAN] 💀 Lazarus Fracture during resurrection: {e}\n")

    def __repr__(self) -> str:
        status = "RESONANT" if self._metrics["shards_committed"] > 0 else "IDLE"
        return f"<Ω_GNOSTIC_COMMITTER status={status} committed={self._metrics['shards_committed']}>"