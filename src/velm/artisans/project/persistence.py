# Path: src/velm/artisans/project/persistence.py
# ----------------------------------------------


import json
import os
import shutil
import time
import hashlib
import threading
import platform
from pathlib import Path
from typing import Optional, Dict, Any, Final, Tuple

# --- THE DIVINE UPLINKS ---
from .contracts import RegistrySchema
from .constants import REGISTRY_FILENAME, REGISTRY_VERSION
from ...utils import atomic_write, hash_file
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ProjectPersistence")


class RegistryPersistence:
    """
    =================================================================================
    == THE KEEPER OF THE BOOK OF NAMES (V-Ω-TOTALITY-V2001-WASM-AWARE)             ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: CHRONICLE_GOVERNOR | RANK: OMEGA_SUPREME

    The Sovereign Hand responsible for the physical manifestation of the Multiverse
    Registry. It manages the temporal persistence of project metadata with
    indestructible resilience.
    """

    # [PHYSICS CONSTANTS]
    BACKUP_COUNT: Final[int] = 5
    SYNC_THRESHOLD_MS: Final[float] = 100.0
    SHADOW_SUFFIX: Final[str] = ".shadow"

    def __init__(self, root_override: Optional[Path] = None):
        """
        [THE RITE OF INCEPTION]
        Calibrates the persistence engine to the active substrate and anchors the root.
        """
        self._io_lock = threading.RLock()
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        # [ASCENSION 1]: GEOMETRIC ANCHORING
        self.root = root_override or self._divine_root()
        self.registry_path = self.root / REGISTRY_FILENAME

        # [ASCENSION 4]: RECOVERY PATHS
        self.backup_path = self.registry_path.with_suffix(".bak")
        self.shadow_path = self.registry_path.with_suffix(self.SHADOW_SUFFIX)

        self._last_save_ts = 0.0
        self._ensure_sanctum()

        Logger.verbose(
            f"Registry Persistence Resonant at: [cyan]{self.root}[/cyan] ({'ETHER' if self.is_wasm else 'IRON'})")

    def _divine_root(self) -> Path:
        """
        Determines where the Book of Names resides based on the perceived reality.
        """
        # [ASCENSION 1]: WASM TRANSPARENCY
        if self.is_wasm:
            # In WASM, the registry lives in /vault/.scaffold
            # This separates it from the actual workspaces at /vault/workspaces
            return Path("/vault/.scaffold")

        # Iron Core (Native): Use the user's home sanctum
        return Path.home() / ".scaffold"

    def _ensure_sanctum(self):
        """Forges the physical directory tree if it is unmanifest."""
        try:
            if not self.root.exists():
                self.root.mkdir(parents=True, exist_ok=True)
                # [ASCENSION 11]: Windows Hide Rite
                if platform.system() == "Windows" and not self.is_wasm:
                    import ctypes
                    ctypes.windll.kernel32.SetFileAttributesW(str(self.root), 2)
        except Exception as e:
            Logger.debug(f"Sanctum Inception deferred: {e}")

    def load(self) -> RegistrySchema:
        """
        =============================================================================
        == THE RITE OF RESURRECTION (LOAD)                                         ==
        =============================================================================
        Resurrects the Multiverse Registry from the physical substrate.
        Implements a 3-tier Lazarus fallback if the primary soul is fractured.
        """
        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE PRIMARY GAZE ---
        if not self.registry_path.exists():
            Logger.verbose("Lobby is a void. Materializing Tabula Rasa Registry.")
            return RegistrySchema(version=REGISTRY_VERSION)

        # [ASCENSION 4]: THE LAZARUS LADDER
        candidates = [self.registry_path, self.backup_path, self.shadow_path]

        for locus in candidates:
            if not locus.exists():
                continue

            try:
                content = locus.read_text(encoding='utf-8')
                if not content.strip():
                    continue

                data = json.loads(content)

                # [ASCENSION 3]: SCHEMA VERIFICATION
                # We validate the version to prevent "Temporal Version Schisms"
                if data.get("version") != REGISTRY_VERSION:
                    Logger.warn(f"Version Drift: Registry {data.get('version')} -> {REGISTRY_VERSION}")

                registry = RegistrySchema(**data)

                # Forensic Tomography
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                Logger.debug(f"Registry Resurrected from [dim]{locus.name}[/dim] in {duration_ms:.2f}ms.")

                return registry

            except Exception as fracture:
                Logger.error(f"Registry Fracture in {locus.name}: {fracture}")
                # We move to the next candidate in the ladder...

        # --- MOVEMENT II: THE FINAL FALLBACK ---
        # [ASCENSION 9]: NoneType Sarcophagus
        Logger.critical("TOTAL PERSISTENCE FAILURE: All registry echoes are profane. Generating Tabula Rasa.")
        return RegistrySchema(version=REGISTRY_VERSION)

    def save(self, registry: RegistrySchema):
        """
        =============================================================================
        == THE RITE OF ATOMIC INSCRIPTION (SAVE)                                   ==
        =============================================================================
        Enshrines the current Gnostic Registry into the physical substrate.
        Uses a two-phase commit to guarantee zero-loss materialization.
        """
        with self._io_lock:
            start_ns = time.perf_counter_ns()

            # [ASCENSION 5]: METABOLIC THROTTLING
            # Prevent write-storms during rapid-fire project transmutations.
            now = time.monotonic()
            if (now - self._last_save_ts) * 1000 < self.SYNC_THRESHOLD_MS:
                time.sleep(self.SYNC_THRESHOLD_MS / 1000.0)

            try:
                # --- MOVEMENT I: THE SHADOW ECHO ---
                # Before we overwrite, we preserve the current state as a backup.
                if self.registry_path.exists():
                    shutil.copy2(self.registry_path, self.backup_path)

                # --- MOVEMENT II: THE TRANSMUTATION ---
                # Prepare the JSON matter
                registry_json = json.dumps(registry.model_dump(mode='json'), indent=2)

                # [ASCENSION 2 & 8]: THE ATOMIC COMMIT
                # atomic_write handles the temp file and the atomic os.replace/fsync
                write_result = atomic_write(
                    target_path=self.registry_path,
                    content=registry_json,
                    logger=Logger,
                    sanctum=self.root
                )

                if not write_result.success:
                    raise ArtisanHeresy(
                        "REGISTRY_INSCRIPTION_FRACTURE",
                        details=write_result.message,
                        severity=HeresySeverity.CRITICAL
                    )

                # --- MOVEMENT III: THE INTEGRITY SEAL ---
                # [ASCENSION 3]: Verify the newly written file
                self._verify_inscription(registry_json)

                # --- MOVEMENT IV: CHRONOLOGIAL ROTATION ---
                # [ASCENSION 6]: Periodically rotate shadows
                self._rotate_shadows()

                self._last_save_ts = time.monotonic()
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

                if not self.is_wasm:
                    Logger.verbose(
                        f"Registry sealed. Mass: {write_result.bytes_written} bytes. Latency: {duration_ms:.2f}ms.")

            except Exception as catastrophic_heresy:
                Logger.critical(f"META-HERESY: Registry Inscription failed: {catastrophic_heresy}")
                # [ASCENSION 12]: THE FINALITY VOW
                # We attempt to restore from backup immediately
                if self.backup_path.exists():
                    shutil.copy2(self.backup_path, self.registry_path)
                    Logger.warn("Reality Inversion: Registry restored from backup due to save failure.")
                raise catastrophic_heresy

    def _verify_inscription(self, original_matter: str):
        """
        [ASCENSION 3]: MERKLE INTEGRITY VERIFICATION.
        Verifies that the matter on disk exactly matches the willed intent.
        """
        if self.is_wasm: return  # VFS caching makes immediate read-back redundant in WASM

        actual_hash = hashlib.sha256(self.registry_path.read_bytes()).hexdigest()
        willed_hash = hashlib.sha256(original_matter.encode('utf-8')).hexdigest()

        if actual_hash != willed_hash:
            raise ArtisanHeresy(
                "INTEGRITY_SCHISM",
                details="Physical file hash mismatch after atomic write.",
                severity=HeresySeverity.CRITICAL
            )

    def _rotate_shadows(self):
        """
        [ASCENSION 6]: ACHRONAL BACKUP ROTATION.
        Maintains a rolling buffer of project registry snapshots.
        """
        if not self.registry_path.exists(): return

        # Only rotate once every hour to minimize I/O tax
        if time.time() % 3600 > 60: return

        shadow_dir = self.root / "shadows"
        shadow_dir.mkdir(parents=True, exist_ok=True)

        timestamp = int(time.time())
        shadow_file = shadow_dir / f"{REGISTRY_FILENAME}.{timestamp}.bak"

        try:
            shutil.copy2(self.registry_path, shadow_file)

            # Prune old souls
            backups = sorted(list(shadow_dir.glob("*.bak")), key=lambda x: x.stat().st_mtime)
            while len(backups) > self.BACKUP_COUNT:
                backups.pop(0).unlink()
        except Exception:
            pass  # Shadowing is a non-critical faculty

    def purge_multiverse(self, force: bool = False):
        """
        [THE RITE OF OBLIVION]
        Annihilates the registry and all backups.
        Requires the Vow of Absolute Will (force=True).
        """
        if not force:
            raise ArtisanHeresy("OBLIVION_STAYED: Purging the multiverse requires --force.")

        with self._io_lock:
            for locus in [self.registry_path, self.backup_path, self.shadow_path]:
                if locus.exists():
                    locus.unlink()

            shadow_dir = self.root / "shadows"
            if shadow_dir.exists():
                shutil.rmtree(shadow_dir)

            Logger.warn("Multiverse Registry Annihilated. All project memories returned to the void.")

    def __repr__(self) -> str:
        status = "RESONANT" if self.registry_path.exists() else "VOID"
        return f"<Ω_REGISTRY_PERSISTENCE root={self.root} status={status}>"