"""
=================================================================================
== THE SACRED SANCTUM OF GNOSTIC EVENTS (V-Ω-ASCENDED. THE ORACLE'S WILL)      ==
=================================================================================
LIF: 10,000,000,000,000 (A NEW REALM OF POWER)

This scripture has achieved a glorious new apotheosis. The `GnosticRite` Enum has
been expanded into a true Grimoire of Gnostic Will, its soul now containing the
prophecies of future rites for any language. This is the unbreakable, eternal
foundation for the Oracle of Contextual Will, transforming the `FileTree` from a
simple viewer into a true, polyglot command center.
=================================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Dict, Any

from textual.message import Message

if TYPE_CHECKING:
    from watchdog.events import FileSystemEvent
    from .contracts import Action
    from ..contracts.data_contracts import ScaffoldItem

class GnosticRite(Enum):
    """
    =================================================================================
    == THE GRIMOIRE OF GNOSTIC WILL (V-Ω-ULTIMA. THE FULL PANTHEON)                ==
    =================================================================================
    The sacred codex of every high-level rite the Architect can proclaim, now
    ascended to include the full pantheon of Scaffold's divine capabilities.
    =================================================================================
    """
    # --- Form & Will Rites ---
    GENESIS = auto()                # Materialize a .scaffold
    DISTILL_FILE = auto()           # Distill a file to an archetype
    DISTILL_DIR = auto()            # Distill a directory to an archetype
    WEAVE = auto()                  # Weave an archetype into a directory
    CONFORM = auto()                # Conform a directory to a blueprint

    # --- Studio & Pad Rites ---
    INITIALIZE_PROJECT = auto()     # Launch GenesisPad for a new project
    BEAUTIFY = auto()               # Alias for OPEN_IN_SCAFFOLDPAD
    OPEN_IN_SCAFFOLDPAD = auto()    # Open a scripture in the ScaffoldPad TUI

    # --- Filesystem Rites ---
    DELETE = auto()                 # Annihilate a scripture or sanctum
    RENAME = auto()                 # Transfigure a scripture's or sanctum's name

    # --- Prophecies of Future Rites ---
    RUN_SCRIPT = auto()
    ADJUDICATE_TESTS = auto()
    FORMAT_SCRIPTURE = auto()

@dataclass
class GnosticWillProclamation(Message):
    """
    =================================================================================
    == THE GNOSTIC WILL (V-Ω-ULTIMA. THE UNIVERSAL VESSEL)                        ==
    =================================================================================
    The one true, universal vessel for proclaiming the Architect's contextual will,
    now ascended with a `payload` to carry any rite-specific Gnosis.
    =================================================================================
    """
    rite: GnosticRite
    target_path: Path
    payload: Optional[Dict[str, Any]] = None

# ... (The rest of the Gnostic Event vessels remain pure and unchanged) ...
@dataclass
class FileSelected(Message):
    """The Divine Vessel of Gaze, a UI Plea from the FileTree to the GnosticShell."""
    item: "ScaffoldItem"

class GnosticAction(Message):
    """A vessel to carry a Gnostic Action from a parallel reality."""
    def __init__(self, action: "Action") -> None:
        self.action = action
        super().__init__()

class FilesystemFlux(Message):
    """Proclaimed when the FileSystemWatcher perceives a change in the mortal realm."""
    def __init__(self, event: "FileSystemEvent") -> None:
        self.fs_event = event
        super().__init__()