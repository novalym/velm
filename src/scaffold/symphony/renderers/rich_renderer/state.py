# Path: scaffold/symphony/renderers/rich_renderer/state.py
# --------------------------------------------------------

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, List, Deque
from ....contracts.symphony_contracts import Edict
from .theme import GnosticTheme


@dataclass
class StepState:
    name: str
    style: str
    spinner_name: str
    start_time: float = field(default_factory=time.time)
    edict: Optional[Edict] = None


@dataclass
class HistoricStep:
    name: str
    duration: float
    success: bool
    timestamp: float


class RendererState:
    """The Mutable Soul of the Renderer."""

    # How many past events to show in the HUD Echo Scroll
    SCROLL_SIZE = 3

    def __init__(self):
        self.is_simulation: bool = False
        self.start_time: float = time.time()
        self.current_sanctum: str = "."

        self.active_step: Optional[StepState] = None

        # Stats
        self.completed_steps: int = 0
        self.success_count: int = 0
        self.fail_count: int = 0

        # Histories
        self.completed_history: List[HistoricStep] = []
        self.recent_history: Deque[HistoricStep] = deque(maxlen=self.SCROLL_SIZE)

    def start_step(self, edict: Edict, icon: str, style: str, name: str):
        spinner_name = GnosticTheme.get_spinner(name)
        self.active_step = StepState(
            name=name,
            style=style,
            spinner_name=spinner_name,
            edict=edict
        )

    def finish_step(self, success: bool, duration: float):
        if self.active_step:
            record = HistoricStep(
                name=self.active_step.name,
                duration=duration,
                success=success,
                timestamp=time.time()
            )
            self.completed_history.append(record)
            # Add to the left of the deque for easy chronological rendering (newest first)
            self.recent_history.appendleft(record)

            if success:
                self.success_count += 1
            else:
                self.fail_count += 1

        self.active_step = None
        self.completed_steps += 1

    def update_context(self, sanctum: str):
        self.current_sanctum = sanctum

    def elapsed_time(self) -> float:
        return time.time() - self.start_time