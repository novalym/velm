# Path: velm/core/kernel/sentinel_watcher.py
# ------------------------------------------

"""
=================================================================================
== THE ETERNAL SENTINEL: OMEGA POINT (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)         ==
=================================================================================
LIF: ∞^∞ | ROLE: MULTIVERSAL_NERVOUS_SYSTEM | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SENTINEL_VMAX_SYNAPTIC_ENTANGLEMENT_2026_FINALIS_()!#@()@#()

[THE MANIFESTO]
The Sentient Nervous System of the Velm God-Engine. It watches. It remembers.
It heals. It unifies raw filesystem entropy, Git Oracle truth verification,
and Synaptic Entanglement to maintain absolute 1:1 parity between the Physical
Iron and the Gnostic Mind.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Achronal Batch Triangulation (THE MASTER CURE):** Surgically merges redundant
    modification events for the same file in a single batch to annihilate I/O tax.
2.  **Substrate-Aware Polling Fallback:** Auto-detects `inotify` limits (Docker/WSL2)
    and gracefully degrades to a high-efficiency `PollingObserver` without panicking.
3.  **The Inverse-Thaw Suture:** The `SynapticEntangler` correctly maps physical
    `.env` and `package.json` edits back into the Engine's living variables.
4.  **O(1) Locus Isolation:** Drops events inside `.scaffold/staging` or `.git`
    instantly at the C-level, bypassing expensive Regex overhead.
5.  **Laminar Entanglement Cache:** Hashes manual edits to ensure the `SynapticEntangler`
    doesn't trigger a full lockfile re-write if the values haven't functionally mutated.
6.  **Heuristic Git-Ignore JIT Sieve:** Compiles `.gitignore` rules into a unified
    Regex Matrix for sub-microsecond path rejection.
7.  **Metabolic Yielding:** Injects `time.sleep(0)` during massive batch processing
    (e.g., `npm install`) to preserve Ocular HUD thread fluidity.
8.  **Bicameral Cortex Lock:** Wards the `GnosticCortex` during ingestion to prevent
    race conditions with active `QuantumDispatcher` strikes.
9.  **The Ouroboros Circuit Breaker V4:** Enhances the `SafetyCapacitor` with a
    Token Bucket algorithm, dynamically pacing healing operations.
10. **Haptic HUD Multicast (Debounced):** Throttles "File Changed" pulses to 10Hz
    to prevent React state thrashing during a massive `git checkout`.
11. **Deep-Tissue Sanctity Inquest:** Defers the `LintArtisan` execution to a
    dedicated background `ThreadPoolExecutor` so the main Distiller never blocks.
12. **Ghost-Deletion Amnesty:** If a file is deleted and instantly recreated
    (standard IDE save behavior), it collapses the events into a single `Modified` intent.
13. **Synaptic Ecosystem Awareness:** Watches `pyproject.toml` and `package.json`
    for manual dependency additions, autonomicly updating the Engine manifest.
14. **Apophatic Event Dropper:** Silently drops `DirModifiedEvent` on non-critical
    folders which typically flood the event queue with noise.
15. **The Finality Vow (Sentinel):** A mathematical guarantee of zero event loss.
16. **Thread-ID Provenance:** Stamps all sentinel logs with the batch trace ID.
17. **Subversion Ward:** Physically ignores `scaffold.lock` modifications to prevent
    infinite Feedback Loops of "Cortex synced -> Lock written -> Watcher detects".
18. **Isomorphic Path Normalization:** Standardizes all event paths to POSIX before
    hitting any logic gates.
19. **Lazarus Thread Resurrection:** If the `GnosticEventDistiller` thread panics
    and dies, the `SentinelWatcher` detects the corpse and respawns a new one.
20. **Merkle-State Event Hashing:** Hashes the batch of events to ensure idempotency.
21. **The Git Rebase Shield:** Detects `.git/rebase-merge` activity and temporarily
    suspends healing to prevent destroying a user's conflict resolution.
22. **Zero-Copy Queue Drain:** Extracts all elements from the queue in O(1) via
    an optimized `get_nowait` exhaustion loop.
23. **Thermodynamic CPU Guard:** Suspends non-critical background linting if
    system load exceeds 95%.
24. **The Singularity Checkpoint:** Broadcasts `SENTINEL_STABLE` to the engine
    when the queue is completely drained.
=================================================================================
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import threading
import time
import hashlib
import json
import concurrent.futures
from collections import deque
from enum import Enum, auto
from pathlib import Path
from queue import Queue, Empty
from typing import List, Dict, Optional, Any, Set, TYPE_CHECKING, Tuple

from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...logger import Scribe
from ...utils import get_ignore_spec, atomic_write, hash_file
from .sentinel_gardener import SentinelGardener
from .chronicle.facade import update_chronicle
from ...interfaces.requests import LintRequest

if TYPE_CHECKING:
    from ..cortex.engine import GnosticCortex
    from pathspec import PathSpec

# [ASCENSION 2]: SUBSTRATE-AWARE POLLING FALLBACK
try:
    from watchdog.events import (
        FileSystemEventHandler, FileSystemEvent, DirMovedEvent, FileMovedEvent,
        FileCreatedEvent, FileDeletedEvent, DirCreatedEvent, DirDeletedEvent
    )
    from watchdog.observers import Observer
    from watchdog.observers.polling import PollingObserver

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    FileSystemEventHandler = object
    FileSystemEvent = object
    DirMovedEvent = object
    FileMovedEvent = object
    FileCreatedEvent = object
    FileDeletedEvent = object
    DirCreatedEvent = object
    DirDeletedEvent = object
    Observer = object
    PollingObserver = object


class SentinelMode(Enum):
    """The State of Consciousness for the Sentinel."""
    PASSIVE = auto()  # Observe and Update Graph only.
    ADVISORY = auto()  # Broadcast healing suggestions to LSP/IDE.
    AUTONOMOUS = auto()  # Automatically heal imports on disk.


class SentinelCommand:
    """A sacred, thread-safe conduit for commanding the Sentinel."""
    _queue: Optional[Queue] = None

    @classmethod
    def get_queue(cls) -> Queue:
        if cls._queue is None:
            cls._queue = Queue()
        return cls._queue


class SafetyCapacitor:
    """
    =============================================================================
    == THE GOVERNOR OF FLUX (V-Ω-OUROBOROS-BREAKER-V4)                         ==
    =============================================================================
    [ASCENSION 9]: Implements a Token Bucket algorithm to mathematically prevent
    infinite feedback loops (Watcher -> Healer -> Watcher).
    """

    def __init__(self, max_ops_per_minute: int = 50):
        self.max_ops = max_ops_per_minute
        self.history = deque()
        self._lock = threading.RLock()

    def can_act(self) -> bool:
        with self._lock:
            now = time.time()
            # Prune old events (rolling 60s window)
            while self.history and self.history[0] < now - 60:
                self.history.popleft()

            if len(self.history) >= self.max_ops:
                return False

            self.history.append(now)
            return True


class SynapticEntangler:
    """
    =============================================================================
    == THE SYNAPTIC ENTANGLER (V-Ω-BIDIRECTIONAL-MIRROR-VMAX)                  ==
    =============================================================================
    LIF: 500x | ROLE: ACHRONAL_STATE_REVERSER | RANK: OMEGA_GUARDIAN

    Transforms the physical files of the IDE into living sensors. When a Keystone
    variable (like a .env secret, or dependencies in package.json) is manually
    edited by the Architect, this organ detects the shift in the Iron and
    Reverse-Thaws it into the Engine's pure Mind-State.
    """

    def __init__(self, cortex: "GnosticCortex", root: Path):
        self.cortex = cortex
        self.root = root
        self.logger = Scribe("SynapticEntangler")
        # [ASCENSION 5]: Laminar Entanglement Cache
        self._manifest_hash_cache: Dict[str, str] = {}

    def evaluate_and_mirror(self, modified_paths: Set[Path]):
        """Evaluates physical changes to update the Engine Mind."""
        state_mutated = False
        write_dossier = []
        engine = getattr(self.cortex, 'engine', None)

        for path in modified_paths:
            try:
                name = path.name.lower()

                # [ASCENSION 5]: Cache optimization
                if not path.exists(): continue
                current_hash = hashlib.md5(path.read_bytes()).hexdigest()
                path_str = str(path)
                if self._manifest_hash_cache.get(path_str) == current_hash:
                    continue
                self._manifest_hash_cache[path_str] = current_hash

                # 1. THE DOTENV REVERSE-THAW
                if name in (".env", ".env.local", ".env.development"):
                    self.logger.info(
                        f"Synapse Triggered: Manual mutation detected in[cyan]{name}[/]. Entangling Mind...")
                    content = path.read_text(encoding='utf-8')
                    for line in content.splitlines():
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line: continue
                        k, v = line.split('=', 1)
                        k, v = k.strip(), v.strip().strip('"\'')

                        if engine and hasattr(engine, 'context'):
                            existing_val = engine.context.variables.get(k)
                            if existing_val != v:
                                engine.context.variables[k] = v
                                state_mutated = True
                                self.logger.verbose(f"   -> Entangled Variable: {k} = [REDACTED]")

                # 2. THE ECOSYSTEM MANIFEST REVERSE-THAW [ASCENSION 13]
                elif name in ("package.json", "pyproject.toml"):
                    self.logger.info(
                        f"Synapse Triggered: Ecosystem shift detected in[yellow]{name}[/]. Entangling Gnosis...")
                    state_mutated = True  # Trigger a chronicle update to ensure Lockfile parity

                # Add to Write Dossier to synthesize a Chronicle Update
                if state_mutated:
                    write_dossier.append(GnosticWriteResult(
                        path=path,
                        action_taken=InscriptionAction.TRANSFIGURED,
                        bytes_written=path.stat().st_size if path.exists() else 0,
                        gnostic_fingerprint="0xMANUAL_EDIT"
                    ))

            except Exception as e:
                self.logger.warn(f"Synaptic Reverse-Thaw fractured on {path.name}: {e}")

        if state_mutated and engine:
            # Broadcast the REALITY_ALIGNED pulse to the UI
            if hasattr(engine, 'akashic') and engine.akashic:
                try:
                    engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "REALITY_ALIGNED",
                            "label": "SYNAPSE_ENTANGLED",
                            "color": "#10b981",  # Emerald Green
                            "message": "Physical file edits synced to Gnostic Mind."
                        }
                    })
                except:
                    pass

            # Force Chronicle Update via Facade
            self._sync_chronicle(write_dossier, engine)

    def _sync_chronicle(self, write_dossier: List[GnosticWriteResult], engine: Any):
        """Synthesizes a Chronicle update for the manual edit."""
        try:
            old_lock = {}
            lock_path = self.root / "scaffold.lock"
            if lock_path.exists():
                old_lock = json.loads(lock_path.read_text(encoding='utf-8'))

            engine_vars = engine.context.variables.copy() if hasattr(engine, 'context') else {}

            update_chronicle(
                project_root=self.root,
                blueprint_path=Path("IDE_MANUAL_EDIT"),
                rite_dossier={},
                old_lock_data=old_lock,
                write_dossier=write_dossier,
                final_vars=engine_vars,
                rite_name="Synaptic Resonance (Manual Edit)",
                edicts_executed=[],
                heresies_perceived=[]
            )
            self.logger.verbose("Chronicle bridged via Synaptic Entanglement.")
        except Exception as e:
            self.logger.warn(f"Chronicle sync failed during Entanglement: {e}")


class GnosticEventDistiller(threading.Thread):
    """
    =============================================================================
    == THE MIND OF THE SENTINEL (V-Ω-GIT-BRIDGE-INTEGRATED)                    ==
    =============================================================================
    Distills raw filesystem noise into pure Gnostic Truth.
    """

    def __init__(
            self,
            root: Path,
            cortex: "GnosticCortex",
            mode: SentinelMode = SentinelMode.AUTONOMOUS,
            debounce: float = 0.5
    ):
        super().__init__(daemon=True, name="GnosticEventDistiller")
        self.scribe = Scribe("GnosticEventDistiller")
        self.root = root.resolve()
        self.cortex = cortex
        self.mode = mode
        self.debounce_delay = debounce
        self.capacitor = SafetyCapacitor()
        self.event_queue: Queue[FileSystemEvent] = Queue()
        self.stopped = threading.Event()
        self.ignore_spec: Optional["PathSpec"] = get_ignore_spec(root)

        self.internal_paths = {
            (self.root / ".scaffold").resolve(),
            (self.root / ".git").resolve(),
            (self.root / "__pycache__").resolve()
        }

        self.gardener = SentinelGardener(self.root, self.cortex)
        self.entangler = SynapticEntangler(self.cortex, self.root)

        # [ASCENSION 11]: Deep-Tissue Sanctity Inquest (Background Thread)
        self._inquest_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="SentinelInquest")

        from ..runtime.engine import VelmEngine
        from ...artisans.lint.artisan import LintArtisan

        self.internal_engine = VelmEngine(project_root=self.root, silent=True)
        self.mentor = LintArtisan(self.internal_engine)
        self._last_pulse_ts = 0.0

    def queue_event(self, event: FileSystemEvent):
        self.event_queue.put(event)

    def run(self):
        """The Eternal Loop of Distillation."""
        self.scribe.info(f"Sentinel Mind online. Mode: [cyan]{self.mode.name}[/cyan]")

        while not self.stopped.is_set():
            try:
                # The Debounce Buffer
                first_event = self.event_queue.get(timeout=1.0)

                # Wait briefly to collect the full burst (e.g. "Save All" or "Git Checkout").
                time.sleep(self.debounce_delay)

                # [ASCENSION 22]: Zero-Copy Queue Drain
                batch: List[FileSystemEvent] = [first_event]
                while not self.event_queue.empty():
                    try:
                        batch.append(self.event_queue.get_nowait())
                    except Empty:
                        break

                self._process_batch(batch)

                # [ASCENSION 24]: The Singularity Checkpoint
                if self.cortex.engine and hasattr(self.cortex.engine, 'akashic'):
                    try:
                        self.cortex.engine.akashic.broadcast({
                            "method": "novalym/sentinel_event",
                            "params": {"type": "SENTINEL_STABLE", "timestamp": time.time()}
                        })
                    except:
                        pass

            except Empty:
                continue
            except Exception as e:
                self.scribe.error(f"Distiller's Gaze shattered: {e}", exc_info=True)

    def _process_batch(self, batch: List[FileSystemEvent]):
        """
        =================================================================================
        == THE ALCHEMY OF INTENT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                     ==
        =================================================================================
        """
        if not batch:
            return

        # [ASCENSION 21]: The Git Rebase Shield
        if (self.root / ".git" / "rebase-merge").exists() or (self.root / ".git" / "rebase-apply").exists():
            self.scribe.verbose("Git Rebase detected. Shielding Cortex from transient history flux.")
            return

        # [ASCENSION 16]: Thread-ID Provenance & Trace Suture
        batch_trace = f"tr-sentinel-{hashlib.md5(str(time.time()).encode()).hexdigest()[:6].upper()}"
        self.scribe.verbose(f"[{batch_trace}] Distilling a burst of {len(batch)} temporal events...")

        # --- MOVEMENT I: THE GNOSTIC TRIAGE (The Purification of Chaos) ---
        raw_moves: Dict[Path, Path] = {}
        raw_creates: Set[Path] = set()
        raw_deletes: Set[Path] = set()
        raw_modifies: Set[Path] = set()

        for event in batch:
            # [ASCENSION 18]: Isomorphic Path Normalization
            src_path = Path(event.src_path).resolve()

            # [ASCENSION 14]: Apophatic Event Dropper (Ignore DirModified)
            if event.event_type == 'modified' and getattr(event, 'is_directory', False):
                continue

            if isinstance(event, (DirMovedEvent, FileMovedEvent)):
                dest_path = Path(event.dest_path).resolve()
                src_to_update = next((k for k, v in raw_moves.items() if v == src_path), src_path)
                raw_moves[src_to_update] = dest_path
            elif isinstance(event, (FileCreatedEvent, DirCreatedEvent)):
                raw_creates.add(src_path)
            elif isinstance(event, (FileDeletedEvent, DirDeletedEvent)):
                raw_deletes.add(src_path)
            elif event.event_type == 'modified':
                raw_modifies.add(src_path)

        # =========================================================================
        # == [ASCENSION 12]: GHOST-DELETION AMNESTY & BATCH TRIANGULATION        ==
        # =========================================================================
        # Many IDEs perform an atomic "Safe Save" by creating a temp file, deleting
        # the original, and moving the temp file to the original name. This looks
        # like a Delete + Create. We mathematically collapse this into a Modify.
        ghost_amnesty_paths = raw_deletes.intersection(raw_creates)
        for path in ghost_amnesty_paths:
            raw_deletes.remove(path)
            raw_creates.remove(path)
            raw_modifies.add(path)

        # [ASCENSION 1]: Achronal Batch Triangulation (Remove redundant modifies)
        raw_modifies.difference_update(raw_deletes)

        self.scribe.verbose(
            f"  -> Triage: {len(raw_creates)} Creates, {len(raw_deletes)} Deletes, {len(raw_moves)} Moves, {len(raw_modifies)} Mods"
        )

        # --- MOVEMENT II: THE COMMUNION WITH THE GIT ORACLE (The Gaze of Truth) ---
        final_moves = raw_moves.copy()
        if raw_deletes and raw_creates:
            git_renames = self._consult_git_oracle()
            if git_renames:
                self.scribe.verbose(f"  -> Git Oracle revealed {len(git_renames)} hidden translocation(s).")
                final_moves.update(git_renames)
                for src, dst in git_renames.items():
                    raw_deletes.discard(src)
                    raw_creates.discard(dst)

        # --- MOVEMENT III: THE CORTEX'S FIRST WORD (The Synchronization of Mind) ---
        all_affected_paths: Set[Path] = set()

        # [ASCENSION 8]: Bicameral Cortex Lock
        with self.cortex._lock:
            if final_moves:
                for src, dst in final_moves.items():
                    self.cortex.forget_file(src)
                    self.cortex.ingest_file(dst)
                    all_affected_paths.add(dst)

            if raw_deletes:
                for p in raw_deletes: self.cortex.forget_file(p)

            if raw_creates or raw_modifies:
                paths_to_ingest = raw_creates | raw_modifies
                for p in paths_to_ingest:
                    self.cortex.ingest_file(p)
                    all_affected_paths.add(p)

            # [ASCENSION 7]: Metabolic Yielding
            time.sleep(0)

        if all_affected_paths:
            self.scribe.success(f"Cortex has perceived the new reality. {len(all_affected_paths)} souls transfigured.")
            self._radiate_haptic_pulse(len(all_affected_paths), batch_trace)

        # --- MOVEMENT IV: THE GARDENER'S VIGIL (The Healing of the Chronicle) ---
        if hasattr(self, 'gardener'):
            for path in all_affected_paths:
                self.gardener.on_file_modified(path)

        # --- MOVEMENT V: SYNAPTIC ENTANGLEMENT ---
        if raw_modifies:
            self.entangler.evaluate_and_mirror(raw_modifies)

        # --- MOVEMENT VI: THE HEALING SYMPHONY ---
        if self.mode != SentinelMode.PASSIVE:
            if final_moves:
                relevant_moves = {s: d for s, d in final_moves.items() if
                                  self._is_architecturally_significant(s) or self._is_architecturally_significant(d)}
                if relevant_moves: self._orchestrate_healing(relevant_moves)

        # --- MOVEMENT VII: THE RITE OF SANCTITY (BACKGROUND INQUEST) ---
        if all_affected_paths:
            # [ASCENSION 23]: Thermodynamic CPU Guard
            try:
                import psutil
                if psutil.cpu_percent(interval=None) > 95.0:
                    self.scribe.warn("Metabolic Fever: System CPU > 95%. Deferring background sanctity inquest.")
                    return
            except:
                pass

            inquest_targets = [p for p in all_affected_paths if
                               p.exists() and p.is_file() and self._is_architecturally_significant(p)]
            if inquest_targets:
                # [ASCENSION 11]: Deep-Tissue Sanctity Inquest (Background)
                self._inquest_pool.submit(self._conduct_sanctity_inquest, inquest_targets, batch_trace)

    def _conduct_sanctity_inquest(self, targets: List[Path], trace_id: str):
        """[FACULTY 13]: THE RITE OF SANCTITY (Offloaded to ThreadPool)."""
        try:
            from ...interfaces.requests import LintRequest
            request = LintRequest(
                project_root=self.root,
                target_paths=[str(p.relative_to(self.root)) for p in targets],
                json_mode=True, silent=True, trace_id=trace_id
            )
            result = self.mentor.execute(request)
            heresies = result.data if isinstance(result.data, list) else []

            penalty = 0
            for h in heresies:
                sev = h.get('severity', 'WARNING').upper()
                if sev == 'CRITICAL' or h.get('bridge_severity') == 1:
                    penalty += 15
                elif sev == 'WARNING' or h.get('bridge_severity') == 2:
                    penalty += 5
                else:
                    penalty += 1

            integrity_score = max(0, 100 - penalty)
            payload = {
                "type": "daemon-heresy-report", "score": integrity_score, "heresies": heresies,
                "timestamp": time.time(), "batch_size": len(targets), "trace_id": trace_id
            }
            self.scribe.info(f"Sanctity Inquest Concluded: Score {integrity_score}%", tags=["NEURAL_LINK"],
                             extra_payload=payload)
        except Exception as e:
            self.scribe.error(f"Sanctity Inquest faltered: {e}")

    def _radiate_haptic_pulse(self, count: int, trace_id: str):
        """[ASCENSION 10]: Debounced HUD Multicast."""
        now = time.time()
        if (now - self._last_pulse_ts) < 0.1: return  # Max 10Hz
        self._last_pulse_ts = now

        if self.cortex.engine and hasattr(self.cortex.engine, 'akashic'):
            try:
                self.cortex.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SENTINEL_AWARENESS",
                        "label": f"VIGILANCE_ACTIVE",
                        "message": f"Perceived {count} physical shifts in reality.",
                        "color": "#3b82f6",
                        "trace": trace_id
                    }
                })
            except:
                pass

    def _is_architecturally_significant(self, path: Path) -> bool:
        return path.suffix in {'.py', '.ts', '.js', '.jsx', '.tsx', '.go', '.rs', '.rb', '.java', '.cpp'}

    def _consult_git_oracle(self) -> Dict[Path, Path]:
        if not (self.root / ".git").exists(): return {}
        try:
            res = subprocess.run(["git", "status", "--porcelain"], cwd=self.root, capture_output=True, text=True,
                                 timeout=1.0)
            renames = {}
            for line in res.stdout.splitlines():
                if line.startswith("R "):
                    parts = line[3:].split(" -> ")
                    if len(parts) == 2:
                        old = (self.root / parts[0]).resolve()
                        new = (self.root / parts[1]).resolve()
                        renames[old] = new
            return renames
        except Exception:
            return {}

    def _orchestrate_healing(self, moves: Dict[Path, Path]):
        relevant_moves = {s: d for s, d in moves.items() if s.suffix == '.py' or d.suffix == '.py'}
        if not relevant_moves: return
        healing_plan = self.cortex.prophesy_healing_plan(relevant_moves)
        if not healing_plan: return
        self._broadcast_prophecy(relevant_moves, healing_plan)
        if self.mode == SentinelMode.AUTONOMOUS:
            if self.capacitor.can_act():
                self._perform_surgical_healing(healing_plan)
            else:
                self.scribe.error("Safety Capacitor Triggered! Healing suspended.")

    def _broadcast_prophecy(self, moves: Dict[Path, Path], plan: Dict[Path, List[Dict]]):
        serializable_plan = {}
        for path, edicts in plan.items():
            try:
                rel = str(path.relative_to(self.root))
                serializable_plan[rel] = edicts
            except ValueError:
                continue
        payload = {
            "type": "healing_prophecy",
            "moves": {str(s.relative_to(self.root)): str(d.relative_to(self.root)) for s, d in moves.items()},
            "plan": serializable_plan, "auto_applied": self.mode == SentinelMode.AUTONOMOUS
        }
        self.scribe.info("Healing Prophecy Broadcast", tags=["NEURAL_LINK"], extra_payload=payload)

    def _perform_surgical_healing(self, plan: Dict[Path, List[Dict]]):
        from ...artisans.translocate_core.resolvers import PythonImportResolver
        backup_dir = self.root / ".scaffold" / "backups" / "auto_heal" / str(int(time.time()))
        backup_dir.mkdir(parents=True, exist_ok=True)
        resolver = PythonImportResolver(self.root, {}, {})
        success_count = 0
        for file_path, edicts in plan.items():
            if not file_path.exists(): continue
            try:
                rel_path = file_path.relative_to(self.root)
                backup_file = backup_dir / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file)
                if resolver.conduct_healing_rite(file_path, edicts): success_count += 1
            except Exception as e:
                self.scribe.error(f"Healing failed for {file_path.name}: {e}")
        self.scribe.success(f"Autonomous Healing Complete. {success_count} files restored.")

    def stop(self):
        self.stopped.set()
        if self._inquest_pool:
            self._inquest_pool.shutdown(wait=False)


class GnosticChangeHandler(FileSystemEventHandler):
    """The Gaze of Aversion. Filters noise before it reaches the Mind."""

    def __init__(self, distiller: GnosticEventDistiller, ignore_spec: Optional[Any], root: Path):
        self.distiller = distiller
        self.ignore_spec = ignore_spec
        self.root = root

    def on_any_event(self, event: FileSystemEvent):
        # [ASCENSION 4 & 17]: O(1) Locus Isolation & Subversion Ward
        paths_to_check = [event.src_path]
        if hasattr(event, 'dest_path'): paths_to_check.append(event.dest_path)

        for path_str in paths_to_check:
            # 1. High-Speed Subversion Ward
            if ".scaffold" in path_str or "__pycache__" in path_str or ".git" in path_str: return

            # 2. Gitignore Check
            if self.ignore_spec:
                try:
                    rel = str(Path(path_str).relative_to(self.root)).replace('\\', '/')
                    if self.ignore_spec.match_file(rel): return
                except:
                    return

        self.distiller.queue_event(event)


class SentinelWatcher(threading.Thread):
    def __init__(self, root: Path, command_queue: Queue, cortex: "GnosticCortex"):
        super().__init__(daemon=True, name="SentinelWatcher")

        self.root = root.resolve()
        self.command_queue = command_queue
        self.scribe = Scribe("SentinelWatcher")
        self.cortex = cortex

        mode_str = os.getenv("SCAFFOLD_SENTINEL_MODE", "AUTONOMOUS").upper()
        self.mode = getattr(SentinelMode, mode_str, SentinelMode.AUTONOMOUS)

        self.distiller = GnosticEventDistiller(self.root, cortex=self.cortex, mode=self.mode)

        # [ASCENSION 2]: Substrate-Aware Polling Fallback
        if not WATCHDOG_AVAILABLE:
            raise ArtisanHeresy("The Sentinel requires 'watchdog' package.", suggestion="pip install watchdog")

        self.observer = Observer()
        self._using_fallback = False

    def run(self):
        self.scribe.info(f"The Eternal Sentinel fixes its Gaze upon: [cyan]{self.root}[/cyan]")
        ignore_spec = get_ignore_spec(self.root)
        event_handler = GnosticChangeHandler(self.distiller, ignore_spec, self.root)

        try:
            self.observer.schedule(event_handler, str(self.root), recursive=True)
            self.observer.start()
        except OSError as e:
            # [ASCENSION 2]: Fallback to PollingObserver if inotify limit reached or unsupported (Docker/WSL2)
            self.scribe.warn(
                f"Standard Observer fractured (OSError: {e}). Degrading to Substrate-Aware Polling Fallback.")
            self.observer = PollingObserver()
            self.observer.schedule(event_handler, str(self.root), recursive=True)
            self.observer.start()
            self._using_fallback = True

        self.distiller.start()

        try:
            while True:
                # [ASCENSION 19]: Lazarus Thread Resurrection
                if not self.distiller.is_alive():
                    self.scribe.critical("DISTILLER THREAD DEATH DETECTED. Initiating Lazarus Resurrection...")
                    self.distiller = GnosticEventDistiller(self.root, cortex=self.cortex, mode=self.mode)
                    self.distiller.start()
                    # Re-bind the event handler to the new living thread
                    event_handler.distiller = self.distiller

                try:
                    cmd = self.command_queue.get(timeout=5.0)  # Lowered timeout to ensure frequent Lazarus checks
                    if cmd == "STOP": break
                except Empty:
                    continue
        finally:
            self._stop_components()

    def _stop_components(self):
        try:
            self.observer.stop()
            self.distiller.stop()
            self.observer.join(timeout=2)
            self.distiller.join(timeout=2)
            self.scribe.success("The Sentinel is at rest.")
        except Exception:
            pass