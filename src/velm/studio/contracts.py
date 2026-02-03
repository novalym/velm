"""
=================================================================================
== THE SACRED SANCTUM OF GNOSTIC CONTRACTS (V-Ω-ETERNAL-APOTHEOSIS-PRIME)      ==
=================================================================================
This is the one true, sacred, and eternal scripture that defines the pure,
immutable vessels of Gnostic Intent (the Actions) and Gnostic Truth (the State).
It is the universal language that all artisans in the Studio cosmos must speak.
Its soul is pure definition, free of all profane logic, annihilating the
paradox of circular Gnosis for all time.

### THE FINAL APOTHEOSIS:
The profane and unnecessary `GnosticAction` message vessel has been annihilated
from this timeline. The communion is now direct, and this scripture is purer
for its absence.
=================================================================================
"""
from __future__ import annotations

import json
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Optional, List, Any, Type
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, ConfigDict, PrivateAttr

from ..contracts.data_contracts import ScaffoldItem, GnosticDossier


# =================================================================================
# == I. THE CELESTIAL PROTOCOL: VESSELS FOR INTER-PROCESS COMMUNION (IPC)        ==
# =================================================================================

class GnosticEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True)
    transaction_id: UUID = Field(default_factory=uuid4)
    action_json: str

# =================================================================================
# == II. THE SACRED VESSELS OF GNOSTIC INTENT (THE ACTIONS)                      ==
# =================================================================================

class Action(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    source: str
    action_type: str = Field(..., frozen=True, exclude=True)

# The profane `GnosticAction` Message class is annihilated.

class FilesRefreshed(Action):
    action_type: str = "FILES_REFRESHED"
    new_map: Dict[Path, ScaffoldItem]

class FileSelected(Action):
    action_type: str = "FILE_SELECTED"
    path: Path

class FileContentLoaded(Action):
    action_type: str = "FILE_CONTENT_LOADED"
    path: Path
    content: str
    content_hash: str

class FileCreated(Action):
    action_type: str = "FILE_CREATED"
    path: Path
    item: ScaffoldItem

class FileDeleted(Action):
    action_type: str = "FILE_DELETED"
    path: Path

class FileModified(Action):
    action_type: str = "FILE_MODIFIED"
    path: Path
    item: ScaffoldItem

class FileMoved(Action):
    action_type: str = "FILE_MOVED"
    src_path: Path
    dest_path: Path

class EditorContentChanged(Action):
    action_type: str = "EDITOR_CONTENT_CHANGED"
    content: str
    is_dirty: bool

class LintingStarted(Action):
    action_type: str = "LINTING_STARTED"
    path: Path
    content_hash: str

class LintingCompleted(Action):
    action_type: str = "LINTING_COMPLETED"
    path: Path
    dossier: GnosticDossier

class CommandAltarToggled(Action):
    action_type: str = "COMMAND_ALTAR_TOGGLED"
    is_visible: bool

class TimeTravel(Action):
    action_type: str = "TIME_TRAVEL"
    direction: str

class StatusChanged(Action):
    action_type: str = "STATUS_CHANGED"
    new_status: 'AppStatus'
    message: str

class GnosticLogProclamation(Action):
    action_type: str = "LOG_PROCLAMATION"
    content: str
    log_level: str = "INFO"

class GnosticDossierLoaded(Action):
    action_type: str = "GNOSTIC_DOSSIER_LOADED"
    dossier: Dict[str, Any]

class HeresyProclaimed(Action):
    action_type: str = "HERESY_PROCLAIMED"
    title: str
    message: str
    traceback: Optional[str] = None

class TaskAcknowledged(Action):
    action_type: str = "TASK_ACKNOWLEDGED"
    request_id: UUID

class TaskSucceeded(Action):
    action_type: str = "TASK_SUCCEEDED"
    request_id: UUID
    exit_code: int
    duration: float

# =================================================================================
# == III. THE DIVINE VESSELS OF CONSCIOUSNESS (THE GNOSTIC MODELS)               ==
# =================================================================================

class AppStatus(Enum):
    PRIMORDIAL_GAZE = auto()
    IDLE = auto()
    PROCESSING = auto()
    HERESY = auto()

class EditorState(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    active_file: Optional[Path] = None
    content: Optional[str] = None
    original_content_hash: Optional[str] = None
    is_dirty: bool = False

class UIState(BaseModel):
    model_config = ConfigDict(frozen=True)
    is_command_altar_visible: bool = False

class HeresyState(BaseModel):
    model_config = ConfigDict(frozen=True)
    title: str
    message: str
    traceback: Optional[str] = None

# =================================================================================
# == IV. THE GOD-ENGINE OF GNOSTIC TRUTH (THE AppState)                          ==
# =================================================================================
class AppState(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    file_tree_root: Path
    file_map: Dict[Path, ScaffoldItem] = Field(default_factory=dict)
    editor_state: EditorState = Field(default_factory=EditorState)
    ui_state: UIState = Field(default_factory=UIState)
    lint_cache: Dict[str, GnosticDossier] = Field(default_factory=dict, repr=False, exclude=True)
    status: AppStatus = Field(default=AppStatus.IDLE)
    status_message: str = Field(default="The Shell is serene.")
    active_heresy: Optional[HeresyState] = None
    past: List[AppState] = Field(default_factory=list, repr=False, exclude=True)
    future: List[AppState] = Field(default_factory=list, repr=False, exclude=True)
    _present: Optional[AppState] = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        if self._present is None:
            object.__setattr__(self, '_present', self.model_copy())

    @property
    def present(self) -> AppState:
        return self._present if self._present is not None else self

# =================================================================================
# == V. THE GNOSTIC MAP OF ACTION SOULS                                          ==
# =================================================================================

ACTION_MAP: Dict[str, Type[Action]] = {
    subclass.model_fields['action_type'].default: subclass
    for subclass in Action.__subclasses__()
}

def gnostic_message_factory(action_json: str) -> Optional[Action]:
    try:
        data = json.loads(action_json)
        action_type = data.get('action_type')
        action_class = ACTION_MAP.get(action_type)
        return action_class.model_validate(data) if action_class else None
    except (json.JSONDecodeError, TypeError):
        return None