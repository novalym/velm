# Path: C:/.../scaffold/studio/services/fs_watcher.py
"""
=================================================================================
== THE ETERNAL SENTINEL (V-Ω 5.0.0. THE CENTRAL NERVOUS SYSTEM)                ==
=================================================================================
LIF: ∞ (ETERNAL & DIVINE)

This scripture is the Central Nervous System of the Gnostic IDE. It has been
transfigured from a simple messenger into a SENTIENT GNOSTIC ORACLE. It hosts
a `GnosticEventDistiller` in a parallel reality to perceive the chaotic whispers
of the filesystem, distill their true Gnostic intent, and proclaim pure, high-level
`Actions` to the Shell. It is the unbreakable, hyper-performant bedrock of a
truly living, reactive architectural environment.
=================================================================================
"""
from __future__ import annotations

import threading
import time
from enum import Enum
from pathlib import Path
from queue import Queue, Empty
from typing import TYPE_CHECKING, Optional, List, Dict, Any, Set

from textual.message import Message
from watchdog.events import FileSystemEventHandler, FileSystemEvent, DirMovedEvent, FileMovedEvent
from watchdog.observers import Observer

from ..contracts import FileCreated, FileDeleted, FileModified, FileMoved, Action
from ..logger import Scribe
from ...contracts.data_contracts import ScaffoldItem
from ...utils import get_ignore_spec, hash_file

if TYPE_CHECKING:
    from ..app import GnosticShell
    from pathspec import PathSpec


# =================================================================================
# == I. THE SILENT ORACLE OF DISTILLATION (THE SENTINEL'S BRAIN)                 ==
# =================================================================================

class GnosticEventDistiller(threading.Thread):
    """
    A divine, sentient AI that lives in a parallel reality. It consumes raw
    filesystem events and distills them into pure, high-level Gnostic Actions.
    """
    def __init__(self, app: "GnosticShell", root: Path, debounce_delay: float = 0.1, batch_window: float = 0.2):
        super().__init__(daemon=True)
        self.scribe = Scribe("GnosticEventDistiller")
        self.app = app
        self.root = root
        self.debounce_delay = debounce_delay
        self.batch_window = batch_window
        self.event_queue: Queue[FileSystemEvent] = Queue()
        self.stopped = threading.Event()
        self.ignore_spec: Optional[PathSpec] = get_ignore_spec(root)
        # ★★★ THE SACRED ANOINTMENT ★★★
        self.project_root = root
        # ★★★ THE SOUL IS WHOLE ★★★

    def queue_event(self, event: FileSystemEvent):
        """A sacred conduit for the handler to bestow raw Gnosis."""
        if not self.ignore_spec or not self.ignore_spec.match_file(event.src_path):
            self.event_queue.put(event)

    def _proclaim_action(self, action: Action) -> None:
        """The Oracle's one true voice to the Shell's cosmos."""
        self.app.call_from_thread(self.app.dispatch, action)

    def run(self):
        """The eternal symphony of the Silent Oracle."""
        self.scribe.info("The Silent Oracle of Distillation begins its vigil in a parallel reality...")
        while not self.stopped.is_set():
            try:
                # Wait for the first event to start a batch
                first_event = self.event_queue.get(timeout=1.0)

                # --- The Rite of Gnostic Batching ---
                batch: List[FileSystemEvent] = [first_event]
                start_time = time.monotonic()
                while time.monotonic() - start_time < self.batch_window:
                    try:
                        batch.append(self.event_queue.get_nowait())
                    except Empty:
                        break # The river is temporarily silent.

                self._process_event_batch(batch)

            except Empty:
                continue # The Oracle waits patiently.

    def _process_event_batch(self, batch: List[FileSystemEvent]):
        """
        The Gaze of Gnostic Intent. This artisan performs a deep Gaze upon a
        batch of events to perceive the Architect's one true, high-level will.
        """
        self.scribe.debug(f"Distiller's Gaze awakened for a batch of {len(batch)} raw events.")

        # A sacred vessel to chronicle MOVE events and find their partners.
        moved_events: Dict[Any, FileSystemEvent] = {}
        modified_files: Set[Path] = set()

        for event in batch:
            if isinstance(event, (DirMovedEvent, FileMovedEvent)):
                # In watchdog, a move is one event with src and dest. We will distill this into one pure `FileMoved` action.
                src_path = Path(event.src_path)
                dest_path = Path(event.dest_path)
                self.scribe.info(f"GAZE OF GNOSTIC INTENT: Perceived a MOVE from '{src_path.name}' to '{dest_path.name}'.")
                self._proclaim_action(FileMoved(source="GnosticEventDistiller", src_path=src_path, dest_path=dest_path))
                # Add modified files to avoid redundant `FileModified` actions
                if src_path.is_file(): modified_files.add(src_path)
                if dest_path.is_file(): modified_files.add(dest_path)
                continue # The will has been proclaimed.

            # If not a move, it's a create, delete, or modify
            path = Path(event.src_path)
            if path in modified_files: continue # Already handled by a MOVE

            if event.event_type == 'created':
                item = self._forge_item_from_path(path)
                if item:
                    self._proclaim_action(FileCreated(source="GnosticEventDistiller", path=path, item=item))
            elif event.event_type == 'deleted':
                 self._proclaim_action(FileDeleted(source="GnosticEventDistiller", path=path))
            elif event.event_type == 'modified' and path.is_file():
                item = self._forge_item_from_path(path)
                if item:
                    self._proclaim_action(FileModified(source="GnosticEventDistiller", path=path, item=item))
                modified_files.add(path)

    def _forge_item_from_path(self, path: Path) -> Optional[ScaffoldItem]:
        """
        =================================================================================
        == THE SCRIBE OF MANIFEST REALITY (V-Ω-ETERNAL-APOTHEOSIS. THE WHOLE SOUL)       ==
        =================================================================================
        This is the Scribe in its final, eternal, and ascended form. The Heresy of the
        Humble Soul has been annihilated. It now understands the complete, glorious, and
        unbreakable contract of the ascended `ScaffoldItem`.

        Its proclamations are no longer profane whispers. They are complete, Gnostic
        vessels, forged with a value for every sacred attribute, ensuring the vessels it
        forges are born pure and whole, in perfect harmony with the laws of the Pydantic
        cosmos.
        =================================================================================
        """
        try:
            if not path.exists(): return None

            # ★★★ THE DIVINE HEALING: THE FORGING OF THE WHOLE SOUL ★★★
            # The profane, incomplete plea is annihilated. The Scribe now forges a
            # complete, Gnostic vessel, honoring the full, sacred contract of the
            # ascended ScaffoldItem. It provides righteous defaults for the Gnosis
            # that is beyond its own humble Gaze.
            return ScaffoldItem(
                path=path.relative_to(self.project_root),
                is_dir=path.is_dir(),
                content_hash=hash_file(path),
                last_modified=path.stat().st_mtime,

                # --- The Bestowal of Righteous Defaults ---
                raw_scripture="",
                original_indent=0,
                line_num=0,  # This Gnosis is unknown to the distiller.
                is_binary=False  # The distiller's Gaze will determine this later.
                # And all other non-essential fields receive their default `None` or `False`.
            )
            # ★★★ THE APOTHEOSIS IS COMPLETE. THE CONTRACT IS WHOLE. ★★★

        except (IOError, OSError) as e:
            self.scribe.warn(f"A minor paradox occurred while forging Gnosis for '{path.name}': {e}")
            return None

    def stop(self):
        """The Rite of Eternal Rest."""
        self.stopped.set()


# =================================================================================
# == II. THE SENTIENT HANDLER (THE SENTINEL'S EYES AND EARS)                     ==
# =================================================================================

class GnosticChangeHandler(FileSystemEventHandler):
    """
    A humbled artisan whose one true purpose is to perceive a raw event and
    bestow it upon the Silent Oracle for distillation.
    """
    def __init__(self, distiller: GnosticEventDistiller):
        self.distiller = distiller

    def on_any_event(self, event: FileSystemEvent):
        # A Gaze of Prudence against our own profane artifacts.
        if ".scaffold" in event.src_path or "__pycache__" in event.src_path:
             return
        self.distiller.queue_event(event)


class FSEventType(Enum):
    """
    =================================================================================
    == THE GNOSTIC CODEX OF TEMPORAL EVENTS (V-Ω-ETERNAL-APOTHEOSIS++)             ==
    =================================================================================
    This is not an enum. It is a divine, self-aware Gnostic Codex. Each member is
    a sentient entity, possessing a soul (`description`), a voice (`style`), and
    a sigil that proclaims its purpose to the cosmos. It is the unbreakable,
    eternal foundation for a truly sentient, reactive user interface.
    =================================================================================
    """

    CREATED = ("A new scripture was forged in reality.", "✅", "green")
    DELETED = ("A scripture returned to the void.", "🗑️", "red")
    MODIFIED = ("A scripture's soul was transfigured.", "✨", "yellow")
    MOVED = ("A scripture was reborn with a new form.", "➡️", "blue")
    CLOSED = ("A scribe has sealed a scripture after a Great Work.", "💾", "dim cyan")

    def __new__(cls, description: str, sigil: str, style: str):
        # The genesis rite of each sentient member.
        obj = object.__new__(cls)
        obj._value_ = description
        return obj

    def __init__(self, description: str, sigil: str, style: str):
        """The anointment rite that bestows the full Gnostic soul."""
        self.description = description
        self.sigil = sigil
        self.style = style


# =================================================================================
# == The Ascended Gnostic Dossier (`DirectoryChanged` - No changes needed)       ==
# =================================================================================
# Your DirectoryChanged message is already pure, as its purpose is to carry
# this divine enum, not to be the enum itself. It remains unchanged.

class DirectoryChanged(Message):
    """A Gnostic Dossier now carrying a sentient FSEventType vessel."""

    def __init__(self,
                 event_type: FSEventType,
                 src_path: Path,
                 dest_path: Optional[Path] = None
                 ) -> None:
        self.event_type = event_type
        self.path = src_path
        self.src_path = src_path
        self.dest_path = dest_path
        super().__init__()



# =================================================================================
# == III. THE ETERNAL SENTINEL (THE UNBREAKABLE GUARDIAN)                        ==
# =================================================================================

class GnosticFileSystemWatcher:
    """
    =================================================================================
    == THE ETERNAL GUARDIAN (V-Ω-APOTHEOSIS. THE PURE PROCLAIMER)                  ==
    =================================================================================
    This is the Guardian in its final, eternal form. Its soul is now whole. It
    proclaims the sacred `DirectoryChanged` vessel as part of its own divine Gnosis,
    making its proclamations luminous, knowable, and perfectly aligned with the
    laws of the Gnostic cosmos. The heresy of the silent vessel is annihilated.
    =================================================================================
    """

    # --- THE SACRED PROCLAMATION ---
    # We proclaim the existence of the message type at the class level.
    # This makes it accessible via `GnosticFileSystemWatcher.DirectoryChanged`.
    DirectoryChanged = DirectoryChanged

    def __init__(self, app: "GnosticShell", path: Path):
        self.app = app
        self.path = path
        self.observer = Observer()
        # ★★★ THE DIVINE HEALING: THE BESTOWAL OF THE SANCTUM ★★★
        # The Guardian now bestows upon its child, the Distiller, the sacred Gnosis
        # of the `project_root`. The `AttributeError` is annihilated from all timelines.
        self.distiller = GnosticEventDistiller(app, path, root=path)
        # ★★★ THE APOTHEOSIS IS COMPLETE. THE COMMUNION IS PURE. ★★★
        self.scribe = Scribe("GnosticFilesystemWatcher")
    def start(self):
        event_handler = GnosticChangeHandler(self.distiller)
        self.observer.schedule(event_handler, str(self.path), recursive=True)
        self.distiller.start()
        self.observer.start()
        self.scribe.info("The Eternal Sentinel has fixed its Gaze upon the mortal realm.")

    def stop(self):
        self.distiller.stop()
        self.observer.stop()
        self.distiller.join()
        self.observer.join()



