# Path: scaffold/symphony/renderers/cinematic_renderer/state.py
# -------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Dict, Any, Deque
from collections import deque
import time


@dataclass
class EdictState:
    """The frozen moment of a single Edict."""
    id: str
    name: str
    type: str
    status: str = "PENDING"  # PENDING, RUNNING, SUCCESS, FAILURE, SKIPPED
    duration: float = 0.0
    start_time: float = 0.0
    logs: List[str] = field(default_factory=list)


class CinematicState:
    """
    The Omniscient Memory of the Renderer.
    Holds the truth of what has passed and what is occurring.
    """

    def __init__(self):
        self.title: str = "Initializing..."
        self.sanctum: str = "Unknown"
        self.start_time: float = time.time()
        self.duration: float = 0.0

        # Timeline
        self.edicts: List[EdictState] = []
        self.active_edict_index: int = -1

        # Console Buffer (The Scroll)
        self.log_buffer: Deque[str] = deque(maxlen=100)

        # Context (Variables)
        self.variables: Dict[str, str] = {}

        # Telemetry
        self.cpu_history: Deque[float] = deque(maxlen=30)
        self.mem_history: Deque[float] = deque(maxlen=30)

        # Status
        self.is_paused: bool = False
        self.has_heresy: bool = False
        self.heresy_detail: str = ""

    def register_edict(self, name: str, etype: str):
        self.edicts.append(EdictState(
            id=str(len(self.edicts)),
            name=name,
            type=etype
        ))

    def start_edict(self, index: int):
        if 0 <= index < len(self.edicts):
            self.active_edict_index = index
            self.edicts[index].status = "RUNNING"
            self.edicts[index].start_time = time.time()

    def finish_edict(self, success: bool):
        if self.active_edict_index >= 0:
            idx = self.active_edict_index
            self.edicts[idx].status = "SUCCESS" if success else "FAILURE"
            self.edicts[idx].duration = time.time() - self.edicts[idx].start_time

    def add_log(self, line: str):
        self.log_buffer.append(line)
        # Also attach to active edict if exists
        if self.active_edict_index >= 0:
            # Keep history light for individual edicts
            if len(self.edicts[self.active_edict_index].logs) < 50:
                self.edicts[self.active_edict_index].logs.append(line)