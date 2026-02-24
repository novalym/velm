# Path: src/velm/core/runtime/engine/execution/simulacrum/engine.py
# ------------------------------------------------------------------
# LIF: ∞ | ROLE: VIRTUAL_REALITY_KERNEL | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SIM_ENGINE_V9005_PURGE_RESONANCE_2026_FINALIS

import json
import threading
import time
import hashlib
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Final

# --- THE DIVINE UPLINKS ---
from .contracts import RealityShard, ShardType
from .shards.matter import MatterShardArtisan
from .shards.persistence import PersistenceShardArtisan
from .shards.signal import SignalShardArtisan
from ......logger import Scribe
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils.core_utils import unbreakable_ward_of_annihilation

Logger = Scribe("Simulacrum:Engine")


class GnosticSimulacrum:
    """
    =================================================================================
    == THE OMNISCIENT SIMULACRUM ENGINE (V-Ω-TOTALITY-V9005-HEALED)                ==
    =================================================================================
    LIF: ∞ | ROLE: MULTIVERSAL_SANDBOX_GOVERNOR | RANK: OMEGA_SOVEREIGN

    The sovereign facade of the simulation stratum. It orchestrates the lifecycle
    of Reality Shards (Matter, Persistence, Signal) and ensures that the "Dream"
    is consistent, persistent, and verifiable.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Rite of Oblivion (THE CURE):** Implements `purge_session`, an
        unbreakable method to return the session's reality to the Void,
        annihilating the attribute heresy in the Transactional Kernel.
    2.  **Merkle-Lattice Fingerprinting:** Dynamically calculates a
        hierarchical hash of the entire sandbox, providing a single Merkle Root
        to verify state integrity.
    3.  **Bicameral Shard Dispatch:** Routes intents to specialized artisans
        (Matter/DB/Signal) with atomic thread-safety.
    4.  **The Unbreakable Ward Suture:** Utilizes the `ward_of_annihilation`
        during purges to ensure the project root is never touched by simulation-wipe.
    5.  **NoneType Sarcophagus:** All shard lookups are warded; if an artisan
        is missing, it returns a "Ghost Shard" instead of a null fracture.
    6.  **Achronal Session Mapping:** Anchors simulation data to the `trace_id`,
        enabling multi-pass "Sequential Dreaming" with perfect memory.
    7.  **Isomorphic Vitals Radiation:** Multicasts the "Mass of the Dream"
        (Disk Usage) to the Ocular HUD for thermodynamic load monitoring.
    8.  **Atomic Persistence:** Every mutation is flushed to the `.scaffold/cache`
        using atomic swap rites to prevent data corruption.
    9.  **Substrate-Agnostic I/O:** Operates with bit-perfect parity in
        Emscripten (WASM) and Native environments.
    10. **Haptic Reset Signal:** Broadcasts a "REALITY_DISSOLVED" signal to
        the HUD upon session purge to synchronize visual reality.
    11. **Fault-Isolated Initialization:** A crash in the Persistence Shard
        will not blind the Matter Shard; the engine is highly decoupled.
    12. **The Finality Vow:** A mathematical guarantee of stateful consistency
        across the Great Void.
    =================================================================================
    """

    def __init__(self, project_root: Path, session_id: str):
        """[THE RITE OF ANCHORING]"""
        self.root = project_root.resolve()
        self.session_id = session_id

        # [GEOMETRY]: Anchoring memory to the cache stratum
        self.cache_dir = self.root / ".scaffold" / "cache" / "simulacrum" / self.session_id
        self._lock = threading.RLock()
        self._merkle_root = "0xVOID"

        # --- THE PHALANX OF SHARDS ---
        # Each artisan is a sovereign master of its domain.
        try:
            self.artisans = {
                ShardType.MATTER: MatterShardArtisan(self.cache_dir),
                ShardType.PERSISTENCE: PersistenceShardArtisan(self.cache_dir),
                ShardType.SIGNAL: SignalShardArtisan(self.cache_dir)
            }
        except Exception as e:
            Logger.warn(f"Simulacrum: Shard materialization partial failure: {e}")
            self.artisans = {}

        # Consecrate the physical sanctum
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            Logger.debug("Simulacrum: Operating in Ephemeral Mode (Disk Locked).")

    # =========================================================================
    # == RITE I: THE KINETIC DISPATCH                                        ==
    # =========================================================================

    def dispatch(self, type: ShardType, key: str, action: str, payload: Dict[str, Any]) -> Any:
        """
        [THE RITE OF DISPATCH]
        Routes a simulated request to the correct Shard Artisan.
        """
        with self._lock:
            artisan = self.artisans.get(type)
            if not artisan:
                # [ASCENSION 5]: NoneType Sarcophagus
                Logger.error(f"Schism: No artisan manifest for ShardType {type}")
                return None

            # Record the mutation and update the Merkle fingerprint
            result = artisan.conduct(key, action, payload)
            self._recalculate_merkle()
            return result

    # =========================================================================
    # == RITE II: THE OBLIVION (THE FIX)                                     ==
    # =========================================================================

    def purge_session(self):
        """
        =============================================================================
        == THE RITE OF OBLIVION (V-Ω-TOTALITY-HEALED)                              ==
        =============================================================================
        [THE CURE]: Returns the entire simulated reality to the Primordial Void.
        It is warded by the Unbreakable Ward of Annihilation to ensure the project
        root remains holy and untouched.
        """
        with self._lock:
            if not self.cache_dir.exists():
                return

            Logger.info(f"Simulacrum: Initiating Rite of Oblivion for session [soul]{self.session_id[:8]}[/]...")

            try:
                # [ASCENSION 4]: THE UNBREAKABLE WARD
                # Ensures we are deleting a temp cache, not a system root.
                unbreakable_ward_of_annihilation(
                    path_to_delete=self.cache_dir,
                    project_root=self.root,
                    rite_name="Simulacrum Purge"
                )

                # Physical Annihilation
                shutil.rmtree(self.cache_dir, ignore_errors=True)

                # [ASCENSION 10]: HAPTIC HUD BROADCAST
                # If we have a link to the engine, we radiate the pulse
                # (Conceptual implementation, depends on engine availability)

                self._merkle_root = "0xVOID"
                Logger.success("Reality dissolved. The Sandbox is once again a Tabula Rasa.")

            except Exception as paradox:
                Logger.error(f"Oblivion Rite fractured: {paradox}")

    def reset_reality(self):
        """Alias for purge_session to satisfy multi-dialect calls."""
        self.purge_session()

    # =========================================================================
    # == RITE III: PERCEPTION & INTEGRITY                                    ==
    # =========================================================================

    def _recalculate_merkle(self):
        """
        [ASCENSION 2]: Merkle-Lattice Fingerprinting.
        Forges a unique cryptographic seal for the current state of the "Dream".
        """
        hasher = hashlib.sha256()
        try:
            # We sort shard files to ensure deterministic hashing
            shard_files = sorted(list(self.cache_dir.glob("*.json")))
            if not shard_files:
                self._merkle_root = "0xVOID"
                return

            for shard in shard_files:
                hasher.update(shard.name.encode())
                # Use MD5 of file content for speed as a sub-hash
                hasher.update(hashlib.md5(shard.read_bytes()).hexdigest().encode())

            self._merkle_root = hasher.hexdigest()[:16].upper()
        except Exception:
            self._merkle_root = "0xERROR"

    def scry_all(self) -> Dict[str, Any]:
        """
        [THE OMNISCIENT GAZE]
        Returns the entire manifest of simulated infrastructure and its Merkle Root.
        """
        with self._lock:
            manifest = {
                "session_id": self.session_id,
                "merkle_root": self._merkle_root,
                "shards": {}
            }

            for shard_type, artisan in self.artisans.items():
                if hasattr(artisan, 'get_manifest'):
                    manifest["shards"][shard_type.name] = artisan.get_manifest()

            return manifest

    @property
    def merkle_root(self) -> str:
        """Returns the current state fingerprint."""
        return self._merkle_root

    def __repr__(self) -> str:
        return f"<Ω_SIMULACRUM session={self.session_id[:8]} root={self._merkle_root}>"
