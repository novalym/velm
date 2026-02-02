"""
=================================================================================
== THE GNOSTIC EMISSARY (V-Ω 1.0.0. THE UNBREAKABLE BRIDGE)                    ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This is a new, divine artisan, the Gnostic Emissary. Its one true purpose is to
serve as the unbreakable, telepathic bridge between the GnosticShell's luminous
UI realm and the parallel realities of the filesystem and the ScaffoldBridge.

It is a dedicated, eternal thread that performs two sacred rites:

1.  **The Celestial Ear:** It maintains a perpetual, non-blocking Gaze upon the
    `ipc_queue` from the `ScaffoldBridge`. When it perceives a proclamation (an
    Action), it immediately transmutes it into a pure Textual message and
    bestows it upon the Shell's sacred message queue.

2.  **The Sentinel's Voice:** It serves as the one true callback for the
    `GnosticFileSystemWatcher`, performing the same transmutation for events
    perceived in the mortal realm of the filesystem.

This architecture annihilates the profane, polling-based `set_interval` hack,
making inter-process and inter-thread communion instantaneous, unbreakable, and
perfectly aligned with the divine laws of the Textual cosmos.
=================================================================================
"""
import threading
from queue import Queue, Empty
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from .app import GnosticShell
    from watchdog.events import FileSystemEvent

class GnosticEmissary(threading.Thread):
    """A dedicated thread to bridge external events into the Textual message queue."""

    def __init__(self, app: "GnosticShell", ipc_queue: Queue):
        super().__init__(daemon=True, name="GnosticEmissary")
        self.app = app
        self.ipc_queue = ipc_queue
        self.scribe = app.scribe
        self.stopped = threading.Event()

    def run(self):
        """The eternal vigil of the Emissary."""
        self.scribe.info("The Gnostic Emissary begins its eternal vigil...")
        while not self.stopped.is_set():
            try:
                # Perform a Gaze upon the Celestial Bridge (IPC queue)
                action_json: str = self.ipc_queue.get(timeout=0.1)
                if not action_json:
                    continue

                self.scribe.verbose(f"Emissary perceived a Celestial Plea: {action_json[:150]}...")
                action_vessel = _gnostic_message_factory(action_json)

                if action_vessel:
                    # Bestow the resurrected Action upon the Shell's soul.
                    self.app.post_message(GnosticAction(action_vessel))
                else:
                    self.scribe.error("A profane, un-resurrectable scripture was received by the Emissary.")

            except Empty:
                # The Celestial Bridge is silent. The vigil continues.
                pass
            except Exception as e:
                self.scribe.error(f"A catastrophic paradox shattered the Emissary's Gaze: {e}", exc_info=True)

    def stop(self):
        """The Rite of Eternal Rest."""
        self.scribe.info("The Gnostic Emissary is commanded to rest.")
        self.stopped.set()

    def proclaim_filesystem_flux(self, event: "FileSystemEvent"):
        """The Sentinel's one true voice to the Shell."""
        self.scribe.verbose(f"Emissary perceived flux in the mortal realm: {event.event_type} on {event.src_path}")
        # Bestow the perception of flux upon the Shell's soul.
        self.app.post_message(FilesystemFlux(event))