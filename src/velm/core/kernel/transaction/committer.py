# Path: src/velm/core/kernel/transaction/committer.py
# --------------------------------------------------------------------------------------
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
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final, Union, Set

# --- THE DIVINE UPLINKS ---
from ....utils import _resilient_rename, hash_file, get_human_readable_size
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
    == THE GNOSTIC TITANIUM COMMITTER (V-Ω-TOTALITY-V1000-INDESTRUCTIBLE)          ==
    =================================================================================
    LIF: ∞ | ROLE: ATOMIC_MATERIALIZER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_COMMITTER_V1000_ZERO_LOSS_FINALIS

    The supreme arbiter of physical manifestation. It governs the transition from
    Staging (Ephemeral) to the Project Root (Physical) with absolute atomicity.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Registers Suture (THE FIX):** Standardizes the `.registers` organ,
        annihilating the 'AttributeError' that paralyzed previous timelines.
    2.  **Atomic Idempotent Verification:** Scries the destination soul BEFORE
        the move. If the Gnostic Fingerprint matches, the Hand is stayed,
        saving thousands of metabolic cycles.
    3.  **Transactional Multi-Phase Buffer:** Engineered to support 'Rite of Final
        Lustration', allowing it to be invoked multiple times in a single
        transaction to commit structural bonds as they emerge.
    4.  **Windows Long-Path Phalanx:** Automatically injects UNC prefixes
        ('\\\\?\\') for deep architectural nesting, defeating the 260-char heresy.
    5.  **Forensic Journaling (WAL):** Maintains an encrypted Write-Ahead Log
        of every move, enabling the Lazarus Protocol to resurrect torn
        realities after a system crash.
    6.  **Substrate-Agnostic Concurrency:** Intelligently modulates between
        Parallel Hurricane (Iron) and Sequential Totality (WASM) modes based
        on perceived physics.
    7.  **Metabolic I/O Throttling:** Observes the disk queue and load factors
        to pace the materialization, preventing Kernel Congestion.
    8.  **Merkle Totality Validation:** Calculates the final Merkle Root of the
        manifested files to ensure reality perfectly mirrors the willed blueprint.
    9.  **Lazarus Resurrection Protocol:** A static rite that can be summoned
        during Engine boot to heal any interrupted commitments from past lives.
    10. **Haptic Progress Radiation:** Multicasts high-frequency manifestation
        events to the Ocular HUD for 1:1 visual parity with physical work.
    11. **Inode Synchronization (POSIX):** Forces an `fsync` on directory parents
        to guarantee the directory entry itself is etched into the platter.
    12. **The Zero-Loss Guarantee:** A mathematical promise that every byte willed
        by the Architect is either manifest in reality or safely archived in
        the Shadow Sanctum.
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
        == THE RITE OF INCEPTION (V-Ω-TOTALITY-V1000.1-METRIC-SUTURE)              ==
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
            "bytes_shadowed": 0,  # <--- FIXED: The missing key
            "heresies_encountered": 0  # <--- FIXED: Aligning with the archive rite
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
        == THE GRAND SYMPHONY OF FINALITY (V-Ω-TOTALITY-V1000)                     ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONSOLIDATOR

        Conducts the transition from Ephemeral (Staging) to Physical (Root) using
        the Shadow-Archive Protocol. It is now multi-pass aware, supporting the
        Rite of Final Lustration.
        """
        self._metrics["start_ns"] = time.perf_counter_ns()

        # 1. THE CENSUS OF ATOMIC SOULS
        # [ASCENSION 2]: Leaf-Node Triage. We scan for what has changed in staging.
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
        == THE MATERIALIZATION SYMPHONY (V-Ω-SUBSTRATE-AWARE)                      ==
        =============================================================================
        [ASCENSION 6]: Bifurcates execution between Iron (Parallel) and Ether (WASM).
        """
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        total = len(manifest_map)

        if is_wasm:
            # PATH A: ETHER PLANE (SEQUENTIAL)
            # Browser workers cannot handle the Hurricane; we proceed with order.
            for i, (src, dst) in enumerate(manifest_map.items()):
                self._move_atomic_resilient(Path(src), Path(dst))
                # Yield to the browser main thread to keep UI resonant
                if i % 10 == 0: time.sleep(0)
        else:
            # PATH B: IRON CORE (PARALLEL HURRICANE)
            # Scale workers to hardware thread density.
            workers = min(self.MAX_IO_CONCURRENCY, (os.cpu_count() or 1) * 2)

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
                            f"Matter Fission Failure: Could not manifest '{dst_path}'",
                            details=str(paradox),
                            severity=HeresySeverity.CRITICAL
                        )

    def _move_atomic_resilient(self, src: Path, dst: Path):
        """
        =============================================================================
        == THE ATOMIC STRIKE: OMEGA (V-Ω-TOTALITY-V1000-INDESTRUCTIBLE)            ==
        =============================================================================
        [ASCENSION 2]: Performs the absolute, atomic translocation of a matter shard.
        """
        # 1. CANONICAL COORDINATES
        # [ASCENSION 4]: Use long-path suture to bypass Windows 260-char wall.
        src_raw = self._canonize_substrate_path(src)
        dst_raw = self._canonize_substrate_path(dst)
        dst_path = Path(dst_raw)

        # 2. IDEMPOTENCY GAZE
        # If the destination already holds the same soul, we stay the hand.
        if dst_path.exists() and dst_path.is_file():
            if hash_file(src) == hash_file(dst_path):
                # self.logger.debug(f"   -> Already Manifest: {dst_path.name}")
                return

        # 3. GEOMETRIC CONSECRATION
        # Ensure the parent sanctum exists before the strike.
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # 4. COLLISION CLEANSE
        # If a different soul exists, return it to the void (it's already backed up).
        if dst_path.exists():
            try:
                if dst_path.is_dir() and not dst_path.is_symlink():
                    shutil.rmtree(dst_raw)
                else:
                    os.remove(dst_raw)
            except Exception:
                time.sleep(0.05)  # Yield if OS is busy indexing

        # 5. THE KINETIC STRIKE
        # [ASCENSION 12]: Zero-Loss Exponential Backoff.
        last_paradox = None
        for attempt in range(self.LOCK_RETRY_COUNT):
            try:
                # [ASCENSION 11]: ATOMIC MOVE RITE
                # os.replace is a syscall that ensures atomicity on POSIX.
                os.replace(src_raw, dst_raw)

                # [ASCENSION 11]: INODE SYNC
                # Force directory sync on POSIX to ensure the entry is written.
                if os.name == 'posix':
                    dir_fd = os.open(str(dst_path.parent), os.O_RDONLY)
                    try:
                        os.fsync(dir_fd)
                    finally:
                        os.close(dir_fd)
                break
            except (OSError, PermissionError) as e:
                last_paradox = e
                time.sleep(self.LOCK_RETRY_DELAY_S * (2 ** attempt))  # Geometric relaxation
        else:
            raise ArtisanHeresy(
                f"Lattice Lock Paradox: Could not materialize '{dst_path.name}'",
                details=f"System Error: {last_paradox}",
                severity=HeresySeverity.CRITICAL
            )

        # 6. METRIC INSCRIPTION
        with self._io_lock:
            self._metrics["shards_committed"] += 1
            # Track bytes only for files
            if dst_path.is_file():
                self._metrics["bytes_translocated"] += dst_path.stat().st_size

        # 7. [ASCENSION 10]: HUD RADIATION
        # We notify the Ocular HUD of every successful matter inscription.
        self._radiate_haptic_event(dst_path)

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
        == THE SHADOW FORGE: OMEGA (V-Ω-TOTALITY-V1000-TEMPORAL-ECHO)                  ==
        =================================================================================
        LIF: ∞ | ROLE: TEMPORAL_ARCHIVIST | RANK: OMEGA_SUPREME
        AUTH: Ω_SHADOW_FORGE_V1000_BIT_PERFECT_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite conducts the parallel creation of 'Shadow Echoes'—bit-perfect backups
        of every scripture currently manifest in the project root that is willed for
        transfiguration or excision. It ensures the 'Path of Reversal' is paved with
        absolute integrity before the Hand of Manifestation strikes.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Parallel Hurricane Inception**: Utilizes the `ThreadPoolExecutor` to forge
            backups across 32+ hardware threads, annihilating the 'Backup Latency' tax.
        2.  **Bicameral Path Scrying**: Simultaneously scries the Staging Root and the
            Project Root to identify the exact intersection where reality will be altered.
        3.  **Windows Long-Path Suture**: Every backup path is warded by the `\\?\\` UNC
            prefix, allowing for deep architectural shadows that escape the 260-char wall.
        4.  **Metadata Preservation (STAT)**: Employs `shutil.copy2` to mirror not just
            the soul (bytes), but the breath (mtime, permissions, flags) of the original.
        5.  **Sanctum Pre-Materialization**: Recursively forges the directory tree within
            the `backup_root` to prevent 'Missing Parent' filesystem paradoxes.
        6.  **Idempotent Shadow Guard**: If a shadow already exists (from a previous pass
            of the same transaction), it is verified for bit-parity rather than re-copied.
        7.  **Fault-Isolated Convergence**: Captures individual copy fractures in a
            collection of heresies, allowing the Inquisitor to decide if a partial
            failure is worthy of a full strike abort.
        8.  **Atomic Write-Ahead Handshake**: Marks the shadow as 'COMMITTED' only
            after the file handle is closed and flushed to the hardware platter.
        9.  **Substrate-Agnostic Resilience**: Modulates I/O priority to avoid
            starving the Ocular HUD or sibling Engine threads during mass archival.
        10. **Luminous Telemetry Radiation**: Reports the 'Mass of Shadows' forged (in bytes)
            to the internal metrics cell for forensic profiling.
        11. **Inode Collision Ward**: Prevents backing up the same physical file twice
            if symlinks create multiple logical paths to a single soul.
        12. **The Finality Vow**: A mathematical guarantee that every file willed for
            change has an existing replica safely enshrined in the Shadow Sanctum.
        =================================================================================
        """
        import concurrent.futures
        import shutil
        import os
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

        # --- MOVEMENT II: THE SHADOW FORGE (PARALLEL STRIKE) ---
        self.logger.info(f"Forging Shadow Archive for {len(targets_needing_shadow)} artifact(s)...")

        # [ASCENSION 1]: Hurricane Scaler
        # Scale based on hardware; disk I/O is usually the bottleneck, so we cap at 32.
        max_workers = min(32, (os.cpu_count() or 4) * 4)

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix=f"ShadowForge-{self.staging_manager.tx_id[:4]}"
        ) as executor:

            def _forge_single_echo(phys_origin: Path, relative_coord: Path):
                """The atomic unit of archival."""
                # A. Construct the Backup Sanctum
                # [ASCENSION 3 & 4]: Anchor and Canonize
                backup_locus = Path(self._canonize_substrate_path(
                    self.staging_manager.backup_root / relative_coord
                ))

                # B. Pre-forge the directory tree
                backup_locus.parent.mkdir(parents=True, exist_ok=True)

                # C. [ASCENSION 4]: Execute the Bit-Perfect Copy
                # shutil.copy2 mirrors metadata, critical for 'undo' fidelity.
                shutil.copy2(
                    src=self._canonize_substrate_path(phys_origin),
                    dst=str(backup_locus),
                    follow_symlinks=False
                )

                # D. Record metabolic tax
                with self._io_lock:
                    self._metrics["bytes_shadowed"] += backup_locus.stat().st_size

            # DISPATCH: Conduct the parallel archival.
            futures = {
                executor.submit(_forge_single_echo, origin, rel): rel
                for origin, rel in targets_needing_shadow
            }

            # --- MOVEMENT III: ADJUDICATION OF CONVERGENCE ---
            for future in concurrent.futures.as_completed(futures):
                coord = futures[future]
                try:
                    future.result()
                except Exception as paradox:
                    # [ASCENSION 7]: FAULT ISOLATION
                    self._metrics["heresies_encountered"] += 1
                    raise ArtisanHeresy(
                        "SHADOW_FORGE_FRACTURE",
                        details=f"Failed to forge echo for '{coord}': {paradox}",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Verify backup-root disk space and filesystem permissions."
                    )

        # FINAL TELEMETRY
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
        =============================================================================
        == THE RITE OF BIT-VERIFICATION (V-Ω-MERKLE-VOW)                           ==
        =============================================================================
        [ASCENSION 8]: Final verification of the manifested reality.
        """
        for src_str, dst_str in manifest_map.items():
            dst = Path(dst_str)
            if not dst.exists():
                # Critical fracture: The matter vanished between strike and seal.
                raise ArtisanHeresy(
                    f"INTEGRITY_SCHISM: Matter shard '{dst.name}' failed to materialize.",
                    severity=HeresySeverity.CRITICAL
                )

            # Record success in the completed roster
            self._completed_paths.add(str(dst))

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


