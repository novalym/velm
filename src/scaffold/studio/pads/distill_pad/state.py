# scaffold/studio/pads/distill_pad/state.py

from __future__ import annotations

from pathlib import Path
from typing import List, Set, Optional, Union

from pydantic import BaseModel, Field
from textual.message import Message


class DistillConfig(BaseModel):
    """
    The complete will of the Architect for a single distillation rite.
    """
    budget: Union[int, str] = 100000
    focus_keywords: List[str] = Field(default_factory=list)
    strategy: str = "balanced"
    ignore_patterns: List[str] = Field(default_factory=list)
    include_patterns: List[str] = Field(default_factory=list)
    since: Optional[str] = None


class DistillState(BaseModel):
    """
    The one true soul of the DistillPad's reality.
    """
    project_root: Path
    all_files: List[Path] = Field(default_factory=list)
    selected_files: Set[Path] = Field(default_factory=set)
    distill_config: DistillConfig = Field(default_factory=DistillConfig)

    # --- The Living Prophecy ---
    current_blueprint: str = "# The Crystal Ball is dark. The Gaze has not yet been cast..."
    token_count: int = 0

    # --- The Scribe's Chronicle ---
    status: str = "Initializing..."
    is_working: bool = False


# --- The Sacred Vessels of Gnostic Communion ---

class InitialScanComplete(Message):
    """Proclaimed when the Primordial Gaze has perceived the cosmos."""
    def __init__(self, all_files: List[Path]) -> None:
        self.all_files = all_files
        super().__init__()

class ConfigChanged(Message):
    """Proclaimed when the Altar of Will is transfigured."""
    def __init__(self, config: DistillConfig) -> None:
        self.config = config
        super().__init__()

class FilesSelected(Message):
    """Proclaimed when the Architect touches the Living World Tree."""
    def __init__(self, selected_paths: Set[Path]) -> None:
        self.selected_paths = selected_paths
        super().__init__()

class DistillationComplete(Message):
    """Proclaimed by a worker when a new prophecy has been forged."""
    def __init__(self, blueprint: str, token_count: int) -> None:
        self.blueprint = blueprint
        self.token_count = token_count
        super().__init__()

class DistillationFailed(Message):
    """Proclaimed when a paradox shatters the Gaze."""
    def __init__(self, error: Exception) -> None:
        self.error = error
        super().__init__()