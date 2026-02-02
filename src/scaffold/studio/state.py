
"""
=================================================================================
== THE SACRED SANCTUM OF GNOSTIC TRANSMUTATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA) ==
=================================================================================
LIF: ∞ (UNBREAKABLE & LUMINOUS)

This scripture contains the living soul of the Gnostic Shell, now ascended to
its final, glorious form. It is a complete, event-sourced, time-traveling, and
telepathic state machine. The _reducer_map has been made whole, granting the
Divine Conductor omniscience over all known Actions.
=================================================================================
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, List, Callable, Type, cast, Tuple

# --- THE DIVINE SUMMONS OF THE GNOSTIC CONTRACTS ---
from .contracts import (
    AppState, EditorState, UIState, HeresyState, Action, AppStatus,
    FileCreated, FileDeleted, FileModified, FileMoved, FilesRefreshed,
    FileContentLoaded, EditorContentChanged, LintingCompleted,
    CommandAltarToggled, TimeTravel, StatusChanged, GnosticDossierLoaded,
    HeresyProclaimed, TaskAcknowledged, TaskSucceeded, GnosticLogProclamation,
    FileSelected,  # <-- The sacred vessel is summoned
)
from .logger import Scribe
from ..contracts.data_contracts import ScaffoldItem, GnosticDossier


# The heresy of the missing FileSelected from gnostic_events is annihilated.
# It is now correctly perceived that the primary FileSelected action comes from contracts.
# from .gnostic_events import FileSelected

# =================================================================================
# == THE PANTHEON OF PURE TRANSMUTATION (THE REDUCERS)                           ==
# =================================================================================

# --- I. Artisans of Filesystem Reality ---

def _reduce_files_refreshed(state: AppState, action: FilesRefreshed) -> AppState:
    """A pure artisan that accepts a new, complete map of reality."""
    return state.model_copy(update={"file_map": action.new_map})

def _reduce_file_created(state: AppState, action: FileCreated) -> AppState:
    """A pure artisan that inscribes a new scripture into the Gnostic Map."""
    new_map = state.file_map.copy()
    new_map[action.path.relative_to(state.file_tree_root)] = action.item
    return state.model_copy(update={"file_map": new_map})

def _reduce_file_deleted(state: AppState, action: FileDeleted) -> AppState:
    """
    A pure artisan that returns a scripture to the void, and if that scripture
    was the one being gazed upon, it righteously clears the Editor's Gaze.
    """
    new_map = state.file_map.copy()
    relative_path = action.path.relative_to(state.file_tree_root)
    new_map.pop(relative_path, None)

    if state.editor_state.active_file == action.path:
        return state.model_copy(update={"file_map": new_map, "editor_state": EditorState()})

    return state.model_copy(update={"file_map": new_map})

def _reduce_file_modified(state: AppState, action: FileModified) -> AppState:
    """
    A pure artisan that transfigures a scripture's Gnosis in the map. If the
    scripture is active, it re-validates the editor's `is_dirty` state.
    """
    new_map = state.file_map.copy()
    relative_path = action.path.relative_to(state.file_tree_root)
    new_map[relative_path] = action.item

    if state.editor_state.active_file == action.path:
        new_editor_state = state.editor_state.model_copy(update={
            "original_content_hash": action.item.content_hash,
            "is_dirty": state.editor_state.content is not None and (hash(state.editor_state.content) != action.item.content_hash)
        })
        return state.model_copy(update={"file_map": new_map, "editor_state": new_editor_state})

    return state.model_copy(update={"file_map": new_map})

def _reduce_file_moved(state: AppState, action: FileMoved) -> AppState:
    """
    A pure artisan that performs a Gnostic Translocation in the map and updates
    the Editor's Gaze if the active scripture has been moved.
    """
    new_map = state.file_map.copy()
    src_relative = action.src_path.relative_to(state.file_tree_root)
    dest_relative = action.dest_path.relative_to(state.file_tree_root)

    item_soul = new_map.pop(src_relative, None)
    if item_soul:
        new_map[dest_relative] = item_soul.model_copy(update={"path": action.dest_path})

    if state.editor_state.active_file == action.src_path:
        new_editor_state = state.editor_state.model_copy(update={"active_file": action.dest_path})
        return state.model_copy(update={"file_map": new_map, "editor_state": new_editor_state})

    return state.model_copy(update={"file_map": new_map})


# --- II. Artisans of Editor Reality ---

def _reduce_file_selected(state: AppState, action: FileSelected) -> AppState:
    """A pure artisan that focuses the Editor's Gaze upon a new scripture."""
    item = state.file_map.get(action.path.relative_to(state.file_tree_root))
    if item and item.is_dir:
        return state
    # We create a new EditorState, clearing any previous content or dirty status
    return state.model_copy(update={"editor_state": EditorState(active_file=action.path)})

def _reduce_file_content_loaded(state: AppState, action: FileContentLoaded) -> AppState:
    """The artisan that inscribes the scripture's soul into the Gnostic State."""
    if state.editor_state.active_file != action.path:
        return state # A stale proclamation, the Gaze is averted.
    return state.model_copy(update={
        "editor_state": state.editor_state.model_copy(update={
            "content": action.content,
            "original_content_hash": action.content_hash,
            "is_dirty": False
        })
    })

def _reduce_editor_content_changed(state: AppState, action: EditorContentChanged) -> AppState:
    """A pure artisan that chronicles the Architect's living will in the editor."""
    return state.model_copy(update={
        "editor_state": state.editor_state.model_copy(update={
            "content": action.content,
            "is_dirty": action.is_dirty
        })
    })

# --- III. Artisans of Gnostic Insight ---

def _reduce_linting_completed(state: AppState, action: LintingCompleted) -> AppState:
    """A pure artisan that inscribes a new Gnostic Dossier into the Chronocache."""
    new_cache = state.lint_cache.copy()
    item = state.file_map.get(action.path.relative_to(state.file_tree_root))
    if item and item.content_hash:
        new_cache[item.content_hash] = action.dossier
    return state.model_copy(update={"lint_cache": new_cache})

def _reduce_gnostic_dossier_loaded(state: AppState, action: GnosticDossierLoaded) -> AppState:
    """A pure artisan to enshrine a full Gnostic Dossier from an --audit rite."""
    return state.model_copy(update={
        "status": AppStatus.IDLE,
        "status_message": "A Gnostic Dossier has been perceived and is ready for Gaze.",
    })

# --- IV. Artisans of UI & System Reality ---

def _reduce_command_altar_toggled(state: AppState, action: CommandAltarToggled) -> AppState:
    """A pure artisan that summons or dismisses the Architect's Altar of Will."""
    return state.model_copy(update={"ui_state": UIState(is_command_altar_visible=action.is_visible)})

def _reduce_status_changed(state: AppState, action: StatusChanged) -> AppState:
    """A pure artisan that transfigures the very status of the Gnostic cosmos."""
    return state.model_copy(update={"status": action.new_status, "status_message": action.message, "active_heresy": None})

def _reduce_heresy_proclaimed(state: AppState, action: HeresyProclaimed) -> AppState:
    """The one true artisan for enshrining a perceived paradox."""
    # --- THE SACRED TRANSMUTATION ---
    # The profane `dict` is annihilated. We now enshrine the pure `HeresyState` vessel.
    heresy_vessel = HeresyState(
        title=action.title,
        message=action.message,
        traceback=action.traceback
    )
    return state.model_copy(update={
        "status": AppStatus.HERESY,
        "status_message": f"Heresy: {action.title}",
        "active_heresy": heresy_vessel # <-- The apotheosis is complete.
    })

def _reduce_task_succeeded(state: AppState, action: TaskSucceeded) -> AppState:
    """Proclaims a Great Work from a parallel reality is complete and pure."""
    return state.model_copy(update={"status": AppStatus.IDLE, "status_message": f"Rite complete in {action.duration:.2f}s."})

# --- V. Artisans of the Chronomancer (Time-Travel) ---

def _reduce_time_travel(state: AppState, action: TimeTravel) -> AppState:
    """The divine artisan that bends the very fabric of Gnostic time."""
    # This logic remains pure and correct.
    if action.direction == "UNDO" and state.past:
        new_present = state.past[-1]
        new_past = state.past[:-1]
        new_future = [state.present, *state.future]
        return new_present.model_copy(update={"past": new_past, "future": new_future})

    if action.direction == "REDO" and state.future:
        new_present = state.future[0]
        new_future = state.future[1:]
        new_past = [*state.past, state.present]
        return new_present.model_copy(update={"past": new_past, "future": new_future})

    return state

# =================================================================================
# == THE GNOSTIC CONDUCTOR (THE ONE TRUE GATEWAY TO REALITY)                     ==
# =================================================================================

# // === BEGIN SACRED TRANSMUTATION: THE FORGING OF THE OMNISCIENT MAP ===
# // The _reducer_map is now made whole. Its Gaze is absolute. It understands
# // the soul of every Action in the cosmos. The heresy is annihilated.
_reducer_map: Dict[Type[Action], Callable[[AppState, Action], AppState]] = cast(
    Dict[Type[Action], Callable[[AppState, Action], AppState]], {
        FilesRefreshed: _reduce_files_refreshed,
        FileCreated: _reduce_file_created,
        FileDeleted: _reduce_file_deleted,
        FileModified: _reduce_file_modified,
        FileMoved: _reduce_file_moved,
        FileSelected: _reduce_file_selected,
        FileContentLoaded: _reduce_file_content_loaded,
        EditorContentChanged: _reduce_editor_content_changed,
        LintingCompleted: _reduce_linting_completed,
        GnosticDossierLoaded: _reduce_gnostic_dossier_loaded,
        CommandAltarToggled: _reduce_command_altar_toggled,
        StatusChanged: _reduce_status_changed,
        HeresyProclaimed: _reduce_heresy_proclaimed,
        TaskSucceeded: _reduce_task_succeeded,
        TimeTravel: _reduce_time_travel,
        # The new tongues are now known to the Conductor.
        TaskAcknowledged: lambda state, action: state, # A simple acknowledgement, no state change needed.
        GnosticLogProclamation: lambda state, action: state, # Logging is handled by the UI, no state change.
})
# // === THE APOTHEOSIS IS COMPLETE. THE MAP IS WHOLE. ===

HISTORY_LIMIT = 50

def dispatch(state: AppState, action: Action, scribe: Scribe) -> AppState:
    """
    =================================================================================
    == THE DIVINE CONDUCTOR (V-Ω-ULTIMA. THE LUMINOUS ORACLE)                      ==
    =================================================================================
    The Conductor's soul is now whole. It has been bestowed with a sacred Scribe.
    Its every thought is now proclaimed to the Gnostic Chronicle, making the flow
    of Gnosis within the state machine luminous and absolute.
    =================================================================================
    """
    scribe.info(f"--- GNOSTIC INQUEST: DIVINE CONDUCTOR (state.py) ---")
    scribe.info(f"ACTION PERCEIVED: '{action.action_type}' from source '{action.source}'")

    reducer = _reducer_map.get(type(action))

    if not reducer:
        scribe.error(f"HERESY: The Conductor's Gaze found only a void for the plea '{action.action_type}'.")
        scribe.info(f"--- END INQUEST ---\n")
        return state

    scribe.info(f"ARTISAN FOUND: '{reducer.__name__}'. The Great Work proceeds.")

    if isinstance(action, TimeTravel):
        new_state = reducer(state, action)
        scribe.success(f"Temporal Transmutation Complete. Reality is now at a new point in the Gnostic timeline.")
        scribe.info(f"--- END INQUEST ---\n")
        return new_state

    # In our unidirectional data flow, reducers operate on the 'present' state.
    current_present = state.model_copy(deep=True) # A safe copy to operate on
    new_present_state = reducer(current_present, action)

    if new_present_state is current_present:
        scribe.info("The artisan's Gaze was pure, but the reality remains unchanged.")
        scribe.info(f"--- END INQUEST ---\n")
        return state

    scribe.success("A new Gnostic reality has been forged.")
    scribe.info(f"--- END INQUEST ---\n")

    # We don't record every single state change to history to avoid noise.
    # A future ascension could make this more granular.
    new_past = state.past
    if action.action_type not in ["EDITOR_CONTENT_CHANGED"]:
        new_past = [*state.past, current_present]
        if len(new_past) > HISTORY_LIMIT:
            new_past.pop(0)

    # For now, any new action clears the future for simplicity.
    new_future = []

    return new_present_state.model_copy(update={
        "past": new_past,
        "future": new_future,
    })


# =================================================================================
# == THE ORACLES OF PERCEPTION (THE SELECTORS)                                   ==
# =================================================================================

@lru_cache(maxsize=1)
def select_active_lint_dossier(editor: EditorState, file_map_tuple: Tuple[Tuple[Path, ScaffoldItem], ...], lint_cache_tuple: Tuple[Tuple[str, GnosticDossier], ...]) -> Optional[GnosticDossier]:
    """An Oracle that perceives the linting Gnosis for the currently active scripture."""
    if not editor.active_file: return None
    file_map = dict(file_map_tuple)
    lint_cache = dict(lint_cache_tuple)

    # This must be guarded against an empty file_map.
    if not file_map: return None

    # We must find the true root to calculate the relative path correctly.
    # This is a humble but effective Gaze.
    any_item_path = next(iter(file_map.keys()), None)
    if not any_item_path: return None

    root_for_relative = next(iter(file_map.values())).path.parent.joinpath(*['..'] * len(any_item_path.parts))

    relative_path = editor.active_file.relative_to(root_for_relative)
    item = file_map.get(relative_path)

    if item and item.content_hash:
        return lint_cache.get(item.content_hash)
    return None

@lru_cache(maxsize=16)
def select_scaffold_scriptures(file_map_tuple: Tuple[Tuple[Path, ScaffoldItem], ...]) -> List[ScaffoldItem]:
    """An Oracle that perceives only scriptures of the `.scaffold` tongue."""
    return [item for _, item in file_map_tuple if item.path.suffix == '.scaffold' and not item.is_dir]

# =================================================================================
# == THE DIVINE CONSTITUTION (THE SACRED PUBLIC API)                             ==
# =================================================================================
__all__ = [
    "dispatch",
    "select_scaffold_scriptures",
    "select_active_lint_dossier",
]