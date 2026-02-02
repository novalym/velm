# Path: scaffold/symphony/execution/kinetic_titan/titan/state.py
# --------------------------------------------------------------

import time
import re
from typing import Deque, List, Optional, Dict, Any, Tuple, Union
from collections import deque
from queue import Queue  # <--- THE DIVINE SUMMONS
from dataclasses import dataclass, field
from rich.text import Text

# The Regex of Purity (Strips ANSI codes)
ANSI_ESCAPE_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


@dataclass
class TitanState:
    """
    =================================================================================
    == THE VESSEL OF KINETIC STATE (V-Ω-LIVING-CONDUIT-RESTORED)                   ==
    =================================================================================
    @gnosis:title The Vessel of Kinetic State
    @gnosis:summary A divine, sentient, and forensically-aware vessel for the Titan's
                     mutable memory. It holds both the HISTORY and the LIVE WIRE.
    @gnosis:LIF 10,000,000,000

    This class is the living memory of a subprocess. It holds the logs, the telemetry,
    the temporal markers, and the active connection to the process output.
    """

    # --- I. The Temporal Anchors ---
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    # --- II. The Identity of the Process ---
    pid: Optional[int] = None
    command: str = "Unknown Rite"

    # --- III. The Outcome (The Truth) ---
    _return_code: Optional[int] = None

    # --- IV. The Living Conduit (THE FIX) ---
    # We exclude this from repr to keep logs clean, but it exists for the Conductor.
    output_queue: Optional[Queue] = field(default=None, repr=False, compare=False)

    # --- V. The Scroll of History (Logs) ---
    # We use a deque with a maxlen to prevent memory exhaustion (The Sentinel of Memory)
    _history: Deque[Text] = field(default_factory=lambda: deque(maxlen=2000))

    # --- VI. The Telemetry Vectors (Performance) ---
    # List of (timestamp, cpu_percent, memory_mb)
    _telemetry: List[Tuple[float, float, float]] = field(default_factory=list)

    # =========================================================================
    # == THE RITES OF MUTATION (WRITING TRUTH)                               ==
    # =========================================================================

    def add_line(self, text: Union[str, Text]):
        """
        Inscribes a new line into the scroll of history.
        Accepts raw strings or Luminous Text objects.
        """
        if isinstance(text, str):
            # If raw string, we trust it is already decoded
            rich_text = Text(text)
        else:
            rich_text = text

        self._history.append(rich_text)

    def add_telemetry(self, cpu: float, mem_mb: float):
        """
        Records the pulse of the machine.
        """
        self._telemetry.append((time.time(), cpu, mem_mb))

    def finish(self, return_code: int):
        """
        [THE ATOMIC SEAL]
        Marks the rite as complete. Freezes time and judgment.
        """
        self.end_time = time.time()
        self._return_code = return_code

    def set_pid(self, pid: int):
        """Consecrates the PID."""
        self.pid = pid

    def attach_queue(self, queue: Queue):
        """
        [THE RITE OF ATTACHMENT]
        Connects the state to the live output stream.
        """
        self.output_queue = queue

    # =========================================================================
    # == THE RITES OF PERCEPTION (READING TRUTH)                             ==
    # =========================================================================

    def is_running(self) -> bool:
        """Adjudicates if the rite is still active."""
        return self._return_code is None

    def is_success(self) -> bool:
        """
        [THE DYNAMIC ADJUDICATOR]
        Returns True if the rite has concluded successfully (Exit 0).
        """
        return self._return_code == 0

    def is_finished(self) -> bool:
        """Adjudicates if the rite has concluded (Success or Failure)."""
        return self._return_code is not None

    def return_code(self) -> Optional[int]:
        """Returns the raw exit code."""
        return self._return_code

    def duration(self) -> float:
        """
        [THE CHRONOMETRIC MIND]
        Calculates the duration. If running, returns elapsed time.
        If finished, returns the fixed duration of the event.
        """
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def get_history_snapshot(self, lines: int = 15) -> List[Text]:
        """
        [THE SNAPSHOT ORACLE]
        Returns the last N lines of history for the UI.
        """
        return list(self._history)[-lines:]

    def get_full_text(self) -> str:
        """
        [THE ANSI PURIFIER]
        Returns the complete history as a clean string for file logging.
        """
        return "\n".join(t.plain for t in self._history)

    def get_status_badge(self) -> str:
        """
        [THE LUMINOUS BADGE]
        Returns a rich-markup string representing the current state.
        """
        if self.is_running():
            return "[bold blue]RUNNING[/bold blue]"
        if self.is_success():
            return "[bold green]SUCCESS[/bold green]"
        return f"[bold red]FAILED ({self._return_code})[/bold red]"

    # =========================================================================
    # == THE RITES OF SERIALIZATION (FORENSICS)                              ==
    # =========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        [THE FORENSIC DOSSIER]
        Serializes the state for the Gnostic Historian.
        The `output_queue` is purposefully excluded to ensure JSON purity.
        """
        return {
            "pid": self.pid,
            "command": self.command,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration(),
            "return_code": self._return_code,
            "status": "SUCCESS" if self.is_success() else ("RUNNING" if self.is_running() else "FAILED"),
            "log_line_count": len(self._history),
            "telemetry_points": len(self._telemetry)
        }

    def __repr__(self) -> str:
        """The Developer's Gaze."""
        status = "RUNNING"
        if self._return_code is not None:
            status = "SUCCESS" if self._return_code == 0 else f"FAILED({self._return_code})"

        return (
            f"<TitanState pid={self.pid} status={status} "
            f"duration={self.duration():.2f}s lines={len(self._history)}>"
        )