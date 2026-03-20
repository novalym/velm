# Path: core/runtime/engine/execution/guardian.py
# ----------------------------------------------

import os
import sys
import time
import hashlib
import threading
import unicodedata
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional, Final

# --- THE DIVINE UPLINKS ---
from .....contracts.data_contracts import ScaffoldItem, GnosticLineType
from .....logger import Scribe

Logger = Scribe("TopologicalGuardian")

class TopologicalGuardian:
    """
    =================================================================================
    == THE Ω_TOPOLOGICAL_GUARDIAN: TOTALITY (V-Ω-VMAX-INDESTRUCTIBLE-SUTURE)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_INTEGRITY_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_GUARDIAN_VMAX_WASM_SAFE_TEMPORAL_SUTURE_2026_FINALIS

    The supreme final authority for collision adjudication. It righteously
    distinguishes between Ancient Matter (Pre-existing Debt) and
    Internal Inception (Willed Matter) using Multimodal Temporal Biopsy.
    =================================================================================
    """

    __slots__ = (
        'engine', 'project_root', 'process_birth_ns', '_lock',
        '_is_wasm', '_is_windows', '_trace_id'
    )

    def __init__(self, engine: Any, project_root: Path, trace_id: str = "tr-guard"):
        self.engine = engine
        self.project_root = project_root.resolve()
        self._trace_id = trace_id
        self._lock = threading.RLock()

        # [ASCENSION 6]: SUBSTRATE DNA DETECTION
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_windows = os.name == 'nt'

        # =========================================================================
        # == MOVEMENT 0: ACHRONAL PROCESS ANCHORING (THE MASTER CURE)            ==
        # =========================================================================
        # We define the "Great Divide". Matter older than this is a collision.
        # Matter younger than this is our own creation.
        self.process_birth_ns = self._divine_process_birth()

    def _divine_process_birth(self) -> int:
        """
        Surgically extracts the process birth time in nanoseconds,
        shielded against WASM toxins.
        """
        # 1. ATTEMPT IRON PROBE (PSUTIL)
        if not self._is_wasm:
            try:
                import psutil
                # Convert seconds to nanoseconds
                return int(psutil.Process().create_time() * 1_000_000_000)
            except (ImportError, Exception):
                pass

        # 2. ETHEREAL FALLBACK (INTERNAL SNAPSHOT)
        # We look for the Engine's birth nanosecond captured in the global context
        if self.engine and hasattr(self.engine, '_start_ns'):
            return self.engine._start_ns

        # 3. PRIMORDIAL FALLBACK
        # If all else fails, assume we started 5 seconds ago
        return int((time.time() - 5.0) * 1_000_000_000)

    def survey(self, items: List[ScaffoldItem], variables: Dict[str, Any]) -> List[Path]:
        """
        =============================================================================
        == THE RITE OF THE OMNISCIENT SURVEY (CONDUCT)                            ==
        =============================================================================
        LIF: ∞ | ROLE: TOPOLOGICAL_PHYSICIST
        """
        start_ns = time.perf_counter_ns()
        collisions: List[Path] = []
        seen_inodes: Set[Tuple[int, int]] = set()

        # [ASCENSION 11]: Path Normalization Utility
        from .....core.alchemist import get_alchemist
        alchemist = get_alchemist()

        self._radiate_hud_pulse("COLLISION_SCRY_START", "#a855f7")

        for idx, item in enumerate(items):
            # [ASCENSION 10]: Metabolic Pacing
            if idx > 0 and idx % 500 == 0: time.sleep(0)

            if item.is_dir or not item.path:
                continue

            # --- MOVEMENT I: THE AMNESTY FILTERS ---
            # [ASCENSION 4]: Shards willed as 'ghosts' or by internal forgers are exempt.
            origin = str(item.metadata.get("origin", "")) if item.metadata else ""
            if item.metadata and (item.metadata.get("is_ghost") or "Forger" in origin):
                Logger.verbose(f"   -> Amnesty Granted: Metabolic artifact '{item.path}'")
                continue

            # --- MOVEMENT II: SPATIAL TRIANGULATION ---
            try:
                # [ASCENSION 7]: Isomorphic Normalization
                raw_path_str = str(item.path).replace('\\', '/')
                resolved_path_str = alchemist.transmute(raw_path_str, variables).strip().strip('"\'')

                abs_target = (self.project_root / resolved_path_str).resolve()
            except Exception:
                continue

            # =========================================================================
            # == MOVEMENT III: THE BICAMERAL TEMPORAL BIOPSY (THE MASTER CURE)       ==
            # =========================================================================
            if abs_target.exists() and abs_target.is_file():
                try:
                    # [ASCENSION 8]: Inode Tracking
                    if not self._is_wasm:
                        stats = abs_target.stat()
                        inode_key = (stats.st_dev, stats.st_ino)
                        if inode_key in seen_inodes: continue
                        seen_inodes.add(inode_key)

                        # [FACULTY 5]: SCRIER OF ANTIQUITY
                        # Capture birth: Windows=ctime, Posix=birthtime or ctime
                        file_birth_ns = int(stats.st_ctime * 1_000_000_000)
                        if hasattr(stats, 'st_birthtime'):
                            file_birth_ns = min(file_birth_ns, int(stats.st_birthtime * 1_000_000_000))
                    else:
                        # WASM Fallback: uses mtime as a proxy for age
                        file_birth_ns = int(os.path.getmtime(abs_target) * 1_000_000_000)

                    # --- THE ADJUDICATION ---
                    # Logic: If file was born BEFORE the engine, it is ANCIENT DEBT.
                    # 500ms buffer for FS clock drift.
                    if file_birth_ns < (self.process_birth_ns - 500_000_000):

                        # =============================================================
                        # == [ASCENSION 3]: THE GHOST-WRITE RESONANCE CHECK          ==
                        # =============================================================
                        # If content matches exactly, it's not a collision, it's a
                        # redundant inception. We grant amnesty to save I/O.
                        if item.content is not None:
                            try:
                                with open(abs_target, 'rb') as f:
                                    existing_hash = hashlib.sha256(f.read()).hexdigest()

                                willed_matter = str(item.content).encode('utf-8')
                                willed_hash = hashlib.sha256(willed_matter).hexdigest()

                                if existing_hash == willed_hash:
                                    Logger.verbose(f"   -> Ghost Match: '{abs_target.name}' is already resonant.")
                                    continue
                            except: pass

                        # --- TRUE COLLISION ---
                        collisions.append(abs_target)

                        # [ASCENSION 11]: Socratic Rationale
                        if Logger.is_verbose:
                            age_sec = (time.time() * 1e9 - file_birth_ns) / 1e9
                            Logger.debug(f"   !! [Ancient Debt] '{abs_target.name}' (Age: {age_sec:.1f}s)")

                    else:
                        # MATTER BORN DURING THIS PROCESS
                        if Logger.is_verbose:
                            Logger.verbose(f"   -> [Willed Inception] '{abs_target.name}' waked JIT. Amnesty Granted.")

                except (OSError, PermissionError) as e:
                    Logger.debug(f"Inquest Fracture for {abs_target.name}: {e}")
                    collisions.append(abs_target)

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        self._radiate_hud_pulse("COLLISION_SCRY_COMPLETE", "#64ffda" if not collisions else "#f59e0b")

        if collisions:
            Logger.info(f"The Guardian perceived {len(collisions)} ancient atoms in {duration_ms:.2f}ms.")
        else:
            Logger.success(f"Reality plane is pure. No ancient debt scried in {duration_ms:.2f}ms.")

        return list(set(collisions))

    def _radiate_hud_pulse(self, label: str, color: str):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TOPOLOGICAL_SURVEY",
                        "label": label,
                        "color": color,
                        "trace": self._trace_id
                    }
                })
            except: pass

    def __repr__(self) -> str:
        return f"<Ω_TOPOLOGICAL_GUARDIAN root={self.project_root.name} birth={self.process_birth_ns} status=RESONANT>"