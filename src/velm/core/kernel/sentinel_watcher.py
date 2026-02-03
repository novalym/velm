# Path: scaffold/core/kernel/sentinel_watcher.py
# ----------------------------------------------


"""
=================================================================================
== THE ETERNAL SENTINEL (V-Ω-GIT-AWARE-AUTONOMOUS)                             ==
=================================================================================
LIF: 10,000,000,000,000

The Sentient Nervous System of the Scaffold God-Engine.
It watches. It remembers. It heals.

It unifies:
1.  **Watchdog:** Raw filesystem events.
2.  **Git Oracle:** Truth verification for moves/renames.
3.  **Gnostic Healer:** Surgical import correction.
4.  **Safety Capacitor:** Infinite loop prevention.
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import threading
import time
from collections import deque
from enum import Enum, auto
from pathlib import Path
from queue import Queue, Empty
from typing import List, Dict, Optional, Any, Set, TYPE_CHECKING, Tuple

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe
from ...utils import get_ignore_spec, atomic_write, hash_file
from .sentinel_gardener import SentinelGardener # <--- THE ASCENSION
from ...interfaces.requests import LintRequest
if TYPE_CHECKING:
    from ..cortex.engine import GnosticCortex
    from pathspec import PathSpec

try:
    from watchdog.events import (
        FileSystemEventHandler, FileSystemEvent, DirMovedEvent, FileMovedEvent,
        FileCreatedEvent, FileDeletedEvent, DirCreatedEvent, DirDeletedEvent
    )
    from watchdog.observers import Observer

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Dummy classes for type hinting
    FileSystemEventHandler = object
    FileSystemEvent = object
    DirMovedEvent = object
    FileMovedEvent = object
    FileCreatedEvent = object
    FileDeletedEvent = object
    DirCreatedEvent = object
    DirDeletedEvent = object
    Observer = object


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
    [FACULTY 3] The Governor of Flux.
    Prevents infinite feedback loops (Watcher -> Healer -> Watcher).
    """

    def __init__(self, max_ops_per_minute: int = 50):
        self.max_ops = max_ops_per_minute
        self.history = deque()
        self._lock = threading.Lock()

    def can_act(self) -> bool:
        with self._lock:
            now = time.time()
            # Prune old events
            while self.history and self.history[0] < now - 60:
                self.history.popleft()

            if len(self.history) >= self.max_ops:
                return False

            self.history.append(now)
            return True


class GnosticEventDistiller(threading.Thread):
    """
    =============================================================================
    == THE MIND OF THE SENTINEL (V-Ω-GIT-BRIDGE-INTEGRATED)                    ==
    =============================================================================
    Distills raw noise into Gnostic Truth.
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
        self.internal_paths = {self.root / ".scaffold", self.root / ".git", self.root / "__pycache__"}
        # ASCENSION: The Gardener is born with the Sentinel
        self.gardener = SentinelGardener(self.root, self.cortex)
        # [ASCENSION 13]: Initializing the Internal Mentor
        # We forge a dedicated engine instance for background jurisprudence.
        from ..runtime.engine import ScaffoldEngine
        from ...artisans.lint.artisan import LintArtisan

        self.internal_engine = ScaffoldEngine(project_root=self.root, silent=True)
        self.mentor = LintArtisan(self.internal_engine)

        # Track paths affected in the current batch
        self._batch_affected_paths: Set[Path] = set()

    def queue_event(self, event: FileSystemEvent):
        self.event_queue.put(event)

    def run(self):
        """The Eternal Loop of Distillation."""
        self.scribe.info(f"Sentinel Mind online. Mode: [cyan]{self.mode.name}[/cyan]")

        while not self.stopped.is_set():
            try:
                # [FACULTY 6] The Debounce Buffer
                first_event = self.event_queue.get(timeout=1.0)

                # We have an event. Wait briefly to collect the full burst (e.g. "Save All").
                time.sleep(self.debounce_delay)

                batch: List[FileSystemEvent] = [first_event]
                while not self.event_queue.empty():
                    batch.append(self.event_queue.get_nowait())

                self._process_batch(batch)

            except Empty:
                continue
            except Exception as e:
                self.scribe.error(f"Distiller's Gaze shattered: {e}", exc_info=True)

    def _process_batch(self, batch: List[FileSystemEvent]):
        """
        =================================================================================
        == THE ALCHEMY OF INTENT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                     ==
        =================================================================================
        LIF: ∞ (ETERNAL & ABSOLUTE)

        This is the divine artisan in its final, eternal form. It is the sentient mind
        of the Sentinel, transmuting the raw, chaotic noise of filesystem events into
        the pure, Gnostic truth of the Architect's will. Its Gaze is absolute. Its
        judgment is truth.

        [HEXAGRAM INTEGRATION]:
        Movement I-V: Triage, Git Oracle, Cortex Sync, Gardener Vigil, Healing Symphony.
        Movement VI: The Rite of Sanctity (Real-time Heresy Adjudication).
        =================================================================================
        """
        if not batch:
            return

        self.scribe.verbose(f"Distilling a batch of {len(batch)} raw temporal events...")

        # --- MOVEMENT I: THE GNOSTIC TRIAGE (The Purification of Chaos) ---
        raw_moves: Dict[Path, Path] = {}
        raw_creates: Set[Path] = set()
        raw_deletes: Set[Path] = set()
        raw_modifies: Set[Path] = set()

        for event in batch:
            # The Polyglot Path Purifier: Canonicalizing coordinates across OS boundaries
            src_path = Path(event.src_path).resolve()

            if isinstance(event, (DirMovedEvent, FileMovedEvent)):
                dest_path = Path(event.dest_path).resolve()
                # The Idempotency Ward: Consolidate chained moves (A->B, B->C becomes A->C)
                src_to_update = next((k for k, v in raw_moves.items() if v == src_path), src_path)
                raw_moves[src_to_update] = dest_path
            elif isinstance(event, (FileCreatedEvent, DirCreatedEvent)):
                raw_creates.add(src_path)
            elif isinstance(event, (FileDeletedEvent, DirDeletedEvent)):
                raw_deletes.add(src_path)
            elif event.event_type == 'modified':
                raw_modifies.add(src_path)

        self.scribe.verbose(
            f"  -> Triage: {len(raw_creates)} Creates, {len(raw_deletes)} Deletes, {len(raw_moves)} Moves, {len(raw_modifies)} Mods"
        )

        # --- MOVEMENT II: THE COMMUNION WITH THE GIT ORACLE (The Gaze of Truth) ---
        # We consult the Git timeline to distinguish between 'Delete+Create' and a 'Move'.
        final_moves = raw_moves.copy()
        if raw_deletes and raw_creates:
            git_renames = self._consult_git_oracle()
            if git_renames:
                self.scribe.verbose(f"  -> Git Oracle revealed {len(git_renames)} hidden translocation(s).")
                final_moves.update(git_renames)
                # Purify the raw sets by removing events now understood as moves
                for src, dst in git_renames.items():
                    raw_deletes.discard(src)
                    raw_creates.discard(dst)

        # --- MOVEMENT III: THE CORTEX'S FIRST WORD (The Synchronization of Mind) ---
        # The Cortex MUST be updated before any healing is attempted, as the healers
        # rely on its Gaze to form their prophecies.
        all_affected_paths: Set[Path] = set()

        if final_moves:
            for src, dst in final_moves.items():
                self.cortex.forget_file(src)
                self.cortex.ingest_file(dst)
                all_affected_paths.add(dst)

        if raw_deletes:
            for p in raw_deletes:
                self.cortex.forget_file(p)

        if raw_creates or raw_modifies:
            paths_to_ingest = raw_creates | raw_modifies
            for p in paths_to_ingest:
                self.cortex.ingest_file(p)
                all_affected_paths.add(p)

        self.scribe.success(f"Cortex has perceived the new reality. {len(all_affected_paths)} souls transfigured.")

        # --- MOVEMENT IV: THE GARDENER'S VIGIL (The Healing of the Chronicle) ---
        # Synchronizing the living documentation with the transfigured code.
        if hasattr(self, 'gardener'):
            for path in all_affected_paths:
                self.gardener.on_file_modified(path)

        # --- MOVEMENT V: THE HEALING SYMPHONY (The Orchestration of Purity) ---
        # If the Sentinel is not merely a passive observer, repair broken imports.
        if self.mode != SentinelMode.PASSIVE:
            if final_moves:
                # The Selective Healing: We only attempt to heal what matters (Code Scriptures).
                relevant_moves = {
                    s: d for s, d in final_moves.items()
                    if self._is_architecturally_significant(s) or self._is_architecturally_significant(d)
                }
                if relevant_moves:
                    self._orchestrate_healing(relevant_moves)
                else:
                    self.scribe.verbose("No architecturally significant translocations perceived. The Healer rests.")

        # --- MOVEMENT VI: THE RITE OF SANCTITY (HERESY DETECTION) ---
        # [ASCENSION 13]: The Final Adjudication.
        # We audit the modified reality for structural heresies and broadcast to the Cockpit.
        if all_affected_paths:
            # Short pause to let the OS finalize the IO operations before the Inquest.
            time.sleep(0.1)

            # Filter targets: We only inquest files that exist and are significant.
            inquest_targets = [
                p for p in all_affected_paths
                if p.exists() and p.is_file() and self._is_architecturally_significant(p)
            ]

            if inquest_targets:
                self._conduct_sanctity_inquest(inquest_targets)

    def _conduct_sanctity_inquest(self, targets: List[Path]):
        """
        [FACULTY 13]: THE RITE OF SANCTITY.
        Performs a background audit of the transfigured files and broadcasts
        the state of sin to the Cockpit.
        """
        try:
            from ...interfaces.requests import LintRequest

            # 1. Execute Linting Logic surgerically
            # We only gaze upon the files that actually changed in this batch.
            request = LintRequest(
                project_root=self.root,
                target_paths=[str(p.relative_to(self.root)) for p in targets],
                json_mode=True,
                silent=True
            )

            # The Mentor adjudicates the flux
            result = self.mentor.execute(request)

            # 2. Forge the Neural Broadcast Payload
            # result.data is expected to be a List of Heresy dictionaries (from LintArtisan)
            heresies = result.data if isinstance(result.data, list) else []

            # Dynamic Purity Calculation
            # We deduct points from the Lattice based on the weight of the sins.
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
                "type": "daemon-heresy-report",
                "score": integrity_score,
                "heresies": heresies,
                "timestamp": time.time(),
                "batch_size": len(targets)
            }

            # 3. TELEPATHIC BROADCAST
            # Tagged with NEURAL_LINK to ensure the Electron Bridge intercepts
            # and forwards the signal to the Cockpit UI.
            self.scribe.info(
                f"Sanctity Inquest Concluded: Score {integrity_score}%",
                tags=["NEURAL_LINK"],
                extra_payload=payload
            )

        except Exception as e:
            self.scribe.error(f"Sanctity Inquest faltered: {e}")

    def _is_architecturally_significant(self, path: Path) -> bool:
        """A humble Gaze to filter out noise before the healing rite."""
        # A prophecy for a deeper Gaze. For now, we focus on code.
        return path.suffix in {'.py', '.ts', '.js', '.go', '.rs', '.rb', '.java', '.cpp'}

    def _consult_git_oracle(self) -> Dict[Path, Path]:
        """
        Asks Git if any files have been renamed recently.
        Returns a map of OldPath -> NewPath.
        """
        if not (self.root / ".git").exists():
            return {}

        try:
            # 'git status --porcelain' shows 'R  old -> new'
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=1.0
            )
            renames = {}
            for line in res.stdout.splitlines():
                if line.startswith("R "):
                    # Format: R  old_path -> new_path
                    parts = line[3:].split(" -> ")
                    if len(parts) == 2:
                        old = (self.root / parts[0]).resolve()
                        new = (self.root / parts[1]).resolve()
                        renames[old] = new
            return renames
        except Exception:
            return {}

    def _orchestrate_healing(self, moves: Dict[Path, Path]):
        """
        Determines if healing is needed and executes based on Mode.
        """
        # Filter for relevant files (e.g. Python)
        relevant_moves = {s: d for s, d in moves.items() if s.suffix == '.py' or d.suffix == '.py'}
        if not relevant_moves:
            return

        # Prophesy the Healing Plan
        self.scribe.info(f"Analyzing impact of {len(relevant_moves)} translocation(s)...")
        healing_plan = self.cortex.prophesy_healing_plan(relevant_moves)

        if not healing_plan:
            self.scribe.verbose("Cosmos is stable. No broken bonds perceived.")
            return

        self.scribe.warn(f"Perceived {len(healing_plan)} broken Gnostic Bond(s).")

        # [FACULTY 9] The Neural Broadcast (Advisory)
        self._broadcast_prophecy(relevant_moves, healing_plan)

        # [FACULTY 2] Autonomous Action
        if self.mode == SentinelMode.AUTONOMOUS:
            if self.capacitor.can_act():
                self._perform_surgical_healing(healing_plan)
            else:
                self.scribe.error("Safety Capacitor Triggered! Healing suspended to prevent infinite loop.")

    def _broadcast_prophecy(self, moves: Dict[Path, Path], plan: Dict[Path, List[Dict]]):
        """Sends a telepathic signal to the IDE/Daemon."""
        # Convert paths to relative strings for JSON serialization
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
            "plan": serializable_plan,
            "auto_applied": self.mode == SentinelMode.AUTONOMOUS
        }
        # The Scribe's 'extra_payload' is picked up by the Daemon's TelemetryMiddleware
        # and forwarded to connected clients (like VS Code).
        self.scribe.info("Healing Prophecy Broadcast", tags=["NEURAL_LINK"], extra_payload=payload)

    def _perform_surgical_healing(self, plan: Dict[Path, List[Dict]]):
        """
        [FACULTY 5] The Atomic Healer.
        Executes the plan on disk with safety backups.
        """
        from ...artisans.translocate_core.resolvers import PythonImportResolver

        # [FACULTY 4] The Shadow Backup
        backup_dir = self.root / ".scaffold" / "backups" / "auto_heal" / str(int(time.time()))
        backup_dir.mkdir(parents=True, exist_ok=True)

        self.scribe.info(f"Initiating Autonomous Healing on {len(plan)} files...")

        # We need a resolver instance. We can reuse the one from Cortex or forge a new one.
        # Since we have the plan, we just need the 'conduct_healing_rite' method.
        # We'll instantiate a fresh one for purity, passing empty maps as we already have the plan.
        resolver = PythonImportResolver(self.root, {}, {})

        success_count = 0

        for file_path, edicts in plan.items():
            if not file_path.exists():
                continue

            try:
                # 1. Backup
                rel_path = file_path.relative_to(self.root)
                backup_file = backup_dir / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file)

                # 2. Heal
                if resolver.conduct_healing_rite(file_path, edicts):
                    success_count += 1
                    self.scribe.verbose(f"   -> Healed: {rel_path}")

            except Exception as e:
                self.scribe.error(f"Healing failed for {file_path.name}: {e}")

        self.scribe.success(f"Autonomous Healing Complete. {success_count} files restored.")

    def stop(self):
        self.stopped.set()


class GnosticChangeHandler(FileSystemEventHandler):
    """The Gaze of Aversion. Filters noise before it reaches the Mind."""

    def __init__(self, distiller: GnosticEventDistiller, ignore_spec: Optional[Any], root: Path):
        self.distiller = distiller
        self.ignore_spec = ignore_spec
        self.root = root

    def on_any_event(self, event: FileSystemEvent):
        # [FACULTY 7] The Ignorance Field
        paths_to_check = [event.src_path]
        if hasattr(event, 'dest_path'):
            paths_to_check.append(event.dest_path)

        for path_str in paths_to_check:
            # Fast String Check
            if ".scaffold" in path_str or "__pycache__" in path_str or ".git" in path_str:
                return

            # Gitignore Check
            if self.ignore_spec:
                try:
                    rel = str(Path(path_str).relative_to(self.root))
                    if self.ignore_spec.match_file(rel):
                        return
                except (ValueError, Exception):
                    return

        self.distiller.queue_event(event)


class SentinelWatcher(threading.Thread):
    """The Sovereign Process."""

    def __init__(self, root: Path, command_queue: Queue, cortex: "GnosticCortex"):
        super().__init__(daemon=True, name="SentinelWatcher")

        if not WATCHDOG_AVAILABLE:
            raise ArtisanHeresy("The Sentinel requires 'watchdog'.", suggestion="pip install watchdog")

        self.root = root.resolve()
        self.command_queue = command_queue
        self.scribe = Scribe("SentinelWatcher")

        # Determine Mode from Env
        mode_str = os.getenv("SCAFFOLD_SENTINEL_MODE", "AUTONOMOUS").upper()
        mode = getattr(SentinelMode, mode_str, SentinelMode.AUTONOMOUS)

        self.distiller = GnosticEventDistiller(self.root, cortex=cortex, mode=mode)
        self.observer = Observer()

    def run(self):
        self.scribe.info(f"The Eternal Sentinel fixes its Gaze upon: [cyan]{self.root}[/cyan]")

        ignore_spec = get_ignore_spec(self.root)
        event_handler = GnosticChangeHandler(self.distiller, ignore_spec, self.root)

        self.observer.schedule(event_handler, str(self.root), recursive=True)
        self.observer.start()
        self.distiller.start()

        try:
            while True:
                try:
                    cmd = self.command_queue.get(timeout=3600)
                    if cmd == "STOP":
                        self.scribe.info("Rest command received.")
                        break
                except Empty:
                    continue
        finally:
            self._stop_components()

    def _stop_components(self):
        self.observer.stop()
        self.distiller.stop()
        self.observer.join(timeout=2)
        self.distiller.join(timeout=2)
        self.scribe.success("The Sentinel is at rest.")

