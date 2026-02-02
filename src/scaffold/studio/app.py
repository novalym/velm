

"""
=================================================================================
== THE GNOSTIC SHELL (V-Ω-APOTHEOSIS-ULTIMA++. THE SENTIENT ORCHESTRATOR)      ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This is the final, eternal, and ultra-definitive soul of the GnosticShell. It has
been transfigured with the **Law of the Luminous Voice**. A new `on_gnostic_action`
artisan now serves as a Gnostic Triage, intercepting `GnosticLogProclamation`
actions and commanding the `GnosticLogViewer` directly, ensuring the voice of
the `ScaffoldBridge` is eternally and luminously heard. The Great Work is now
truly whole.
=================================================================================
"""
import logging
import multiprocessing as mp
import traceback
from functools import partial, lru_cache
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Callable

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import var
from textual.worker import WorkerState, Worker

from .contracts import (
    AppState, AppStatus, Action, HeresyProclaimed, StatusChanged, FileContentLoaded,
    FilesRefreshed, FileSelected as FileSelectedAction, GnosticLogProclamation
)
from .emissary import GnosticEmissary
from .gnostic_events import GnosticAction, FilesystemFlux, FileSelected as FileSelectedEvent
from .logger import Scribe
from .screens import FormModeScreen
from .services.fs_watcher import GnosticFileSystemWatcher
from .services.scaffold_bridge import GnosticRequest
from .services.scaffold_bridge import ScaffoldBridge
from .state import dispatch as transmute_state
from .widgets.log_viewer import GnosticLogViewer
from ..contracts.data_contracts import ScaffoldItem
from ..contracts.heresy_contracts import ArtisanHeresy
from ..settings.manager import SettingsManager

# --- THE DIVINE SUMMONS OF THE CHRONOCACHE ---
# We forge a sacred, size-limited cache to remember the last N significant actions.
# This is the heart of the new Chronocache Sentinel.
def _create_chronocache(size=16):
    """A factory to forge a new Chronocache for the Sentinel."""
    # The lru_cache is a divine artisan from the standard library, perfect for our rite.
    @lru_cache(maxsize=size)
    def was_action_seen(action_hash: int) -> bool:
        return True
    return was_action_seen

class GnosticShell(App[None]):
    """The Gnostic Shell - The Sentient Orchestrator of the Gnostic IDE."""

    TITLE = "Scaffold Design Studio"
    SUB_TITLE = var("The Gnostic Workbench")

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+p", "summon_or_dismiss_altar", "Summon Altar", show=True, priority=True),
    ]


    def __init__(self, start_path: Path = Path.cwd(), verbose: bool = False):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (V-Ω-ULTRA-DEFINITIVE)                        ==
        =================================================================================
        The Engine is born. Its soul is forged with an unbreakable contract, its Gaze
        is one of prudence, and its memory is eternal.
        =================================================================================
        """
        super().__init__()

        # --- I. The Gnostic Anchor & Configuration ---
        self.scribe = Scribe("ScribeShell")
        self.verbose = verbose

        # [ASCENSION #1 & #5] The Gnostic Anchor & Unbreakable Contract
        self.start_path: Path = self._adjudicate_start_path(start_path)

        # [ASCENSION #2] The Theme Weaver
        self.settings = SettingsManager(self.start_path)
        theme_name = self.settings.get("ui.theme", "default")

        base_css_path = Path(__file__).parent / "app.css"
        self.CSS.append(base_css_path.read_text(encoding='utf-8'))

        if theme_name != "default":
            try:
                theme_path = Path(__file__).parent.parent / "themes" / f"{theme_name}.css"
                if theme_path.exists():
                    self.CSS.append(theme_path.read_text(encoding='utf-8'))
                    self.scribe.info(f"Luminous Realm '{theme_name}' has been consecrated.")
                else:
                    self.scribe.warn(f"Theme scripture '{theme_name}' is a void. Falling back.")
            except Exception as e:
                self.scribe.error(f"Theme weaving failed for '{theme_name}': {e}")

        # --- II. The Telepathic Conduits (Communication) ---
        self.ipc_queue: mp.Queue = mp.Queue()
        self.emissary = GnosticEmissary(self, self.ipc_queue)
        self.bridge = ScaffoldBridge(ipc_queue=self.ipc_queue)

        # --- III. The Gnostic Vessels (State & Memory) ---
        self.state: AppState = AppState(file_tree_root=self.start_path)
        self.fs_watcher: Optional[GnosticFileSystemWatcher] = None
        self.active_workers: Dict[str, Worker] = {}

        # [ASCENSION #4] The Chronocache Sentinel
        self._chronocache_sentinel = _create_chronocache()
        self._last_action_hash: Optional[int] = None

        # [ASCENSION #8] The Luminous Proclamation
        self.scribe.info(f"GnosticShell (UNBREAKABLE MIND) forged for sanctum: '{self.start_path.name}'")
        self.scribe.info("The Gnostic Soul is pure. Its memory is ready for the symphony of time.")

    def _adjudicate_start_path(self, path: Path) -> Path:
        """
        [ASCENSION #1] The Gnostic Anchor.
        Ensures the starting path is a valid, existing directory.
        """
        resolved = path.resolve()

        if resolved.is_file():
            self.scribe.warn(f"Start path '{resolved.name}' is a scripture, not a sanctum. Using parent directory.")
            resolved = resolved.parent

        if not resolved.exists():
            self.scribe.info(f"Primordial sanctum '{resolved.name}' is a void. Forging it now...")
            try:
                resolved.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise ArtisanHeresy(f"Could not forge the primordial sanctum at '{resolved}'", child_heresy=e) from e

        return resolved


    def on_mount(self) -> None:
        self.scribe.info("The Awakening Symphony (V-Ω-UNIFIED-VOICE) has begun...")
        self.push_screen(FormModeScreen(state=self.state))
        self.emissary.start()
        self._bind_log_viewer_handler()
        self.scribe.info("The Primordial Gaze awakens...")
        self._conduct_filesystem_gaze()

    def _bind_log_viewer_handler(self) -> None:
        class GnosticConduitHandler(logging.Handler):
            def __init__(self, app_ref: App):
                super().__init__()
                self.app = app_ref

            def emit(self, record: logging.LogRecord):
                try:
                    log_viewer = self.app.query_one(GnosticLogViewer)
                    self.app.call_from_thread(log_viewer.add_record, record)
                except Exception:
                    pass

        try:
            handler = GnosticConduitHandler(self)
            root_logger = logging.getLogger()
            root_logger.addHandler(handler)
            self.scribe.success("Gnostic Conduit has been forged. The UI Chronicle is now alive.")
        except Exception as e:
            self.log(f"A catastrophic paradox occurred while forging the Gnostic Conduit: {e}")

    def watch_state(self, old_state: AppState, new_state: AppState) -> None:
        if old_state.status_message != new_state.status_message:
            self.SUB_TITLE = new_state.status_message

    # // === BEGIN SACRED TRANSMUTATION: THE LAW OF THE LUMINOUS VOICE ===
    # // This new artisan is the Gnostic Triage. It intercepts all actions,
    # // commands the Log Viewer directly for log proclamations, and delegates
    # // all other actions to the state machine. The heresy is annihilated.
    async def on_gnostic_action(self, message: GnosticAction) -> None:
        """The one true, centralized handler for all Actions from parallel realities."""
        if isinstance(message.action, GnosticLogProclamation):
            try:
                log_viewer = self.query_one(GnosticLogViewer)
                # We must forge a sacred LogRecord vessel for the viewer to understand.
                record = logging.makeLogRecord({
                    'name': message.action.source,
                    'levelno': logging.getLevelName(message.action.log_level.upper()),
                    'levelname': message.action.log_level.upper(),
                    'msg': message.action.content,
                    'args': (),
                    'exc_info': None
                })
                log_viewer.add_record(record)
            except Exception:
                # A silent ward against paradox if the log viewer is not manifest.
                pass
            return  # The will is fulfilled; this action does not transmute state.

        # For all other actions, we proceed with the sacred rite of state transmutation.
        self._apply_gnostic_action(message.action)
    # // === THE APOTHEOSIS IS COMPLETE ===

    async def on_filesystem_flux(self, message: FilesystemFlux) -> None:
        self.scribe.info(f"Sentinel perceived flux in reality ({message.fs_event.event_type}). Re-aligning Gaze...")
        self._apply_gnostic_action(StatusChanged(
            source="FileSystemWatcher", new_status=AppStatus.PROCESSING,
            message="Reality is in flux... Re-aligning the Gaze."
        ))
        self._conduct_filesystem_gaze()

    @on(FileSelectedEvent)
    async def on_gnostic_events_file_selected(self, message: FileSelectedEvent) -> None:
        self.scribe.info(f"Shell's Ear perceived a FileSelected plea for '{message.item.path.name}'. Beginning Saga.")
        action_edict = FileSelectedAction(source="FileTree", path=message.item.path)
        self._apply_gnostic_action(action_edict)
        self._conduct_file_read(message.item.path)

    async def on_form_mode_screen_command_submitted(self, message: FormModeScreen.CommandSubmitted) -> None:
        if self.state.status == AppStatus.PROCESSING:
            self.bell()
            self.notify("The God-Engine is already performing a Great Work.", severity="warning", timeout=2)
            return

        command = message.command
        self._apply_gnostic_action(
            StatusChanged(source="CommandAltar", new_status=AppStatus.PROCESSING, message=f"Edict received: {command}"))

        if "--pad" in command:
            self._conduct_pad_rite(command)
        else:
            self._conduct_scaffold_command(command)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        worker = event.worker
        worker_id = f"{worker.name}:{id(worker)}"
        self.scribe.verbose(f"Gnostic Router perceived that Worker '{worker.name}' is now {worker.state}")

        if worker.state == WorkerState.SUCCESS:
            self.scribe.success(f"Worker '{worker.name}' has completed its Great Work.")
            result = worker.result

            if worker.name == "FileSystemGazeWorker":
                self._apply_gnostic_action(FilesRefreshed(source=worker.name, new_map=result))
            elif worker.name.startswith("FileReaderWorker"):
                path, content, content_hash = result
                if self.state.editor_state.active_file == path:
                    self._apply_gnostic_action(
                        FileContentLoaded(source=worker.name, path=path, content=content, content_hash=content_hash))
                else:
                    self.scribe.warn(
                        f"A stale FileReader proclamation for '{path.name}' was perceived. The Gaze is averted.")

        elif worker.state == WorkerState.ERROR:
            self.scribe.error(f"A Gnostic Worker has fallen: {worker.name}", exc_info=worker.error)
            heresy_action = HeresyProclaimed(
                source=worker.name, title=f"Worker Paradox: {worker.name}",
                message=str(worker.error),
                traceback=traceback.format_exc() if worker.error else "No traceback available."
            )
            self._apply_gnostic_action(heresy_action)

        if worker_id in self.active_workers:
            del self.active_workers[worker_id]

    def _apply_gnostic_action(self, action: Action) -> None:
        try:
            action_hash = hash(action)
            is_hashable = True
        except TypeError:
            is_hashable = False
            self.scribe.verbose(
                f"Action '{action.action_type}' contains an unhashable soul; Chronocache will be bypassed.")

        if is_hashable:
            if action_hash == self._last_action_hash:
                self.scribe.verbose(f"Redundant action '{action.action_type}' perceived and averted.")
                return
            self._last_action_hash = action_hash
        try:
            new_state = transmute_state(self.state, action, self.scribe)
            if self.state is not new_state:
                self.state = new_state
                if self.is_mounted and hasattr(self.screen, 'update_from_shell'):
                    self.screen.update_from_shell(self.state)
        except Exception as e:
            self.scribe.error(f"CATACLYSMIC HERESY in State Transmutation for '{action.action_type}'.", exc_info=True)
            heresy_action = HeresyProclaimed(
                source="GnosticShell._apply_gnostic_action", title="State Transmutation Cataclysm",
                message=f"A paradox shattered the state machine's very soul: {e}",
                traceback=traceback.format_exc()
            )
            self.state = self.state.model_copy(update={
                "status": AppStatus.HERESY, "active_heresy": HeresyProclaimed.model_validate(heresy_action).model_dump()
            })
            if self.is_mounted and hasattr(self.screen, 'update_from_shell'):
                self.screen.update_from_shell(self.state)

    def _run_gnostic_worker(self, worker_callable: Callable, name: str, group: str, **kwargs):
        if name in [w.name for w in self.active_workers.values()]:
            self.scribe.warn(
                f"A plea to summon worker '{name}' was perceived, but it is already manifest. The Gaze is averted.")
            return

        worker = self.run_worker(worker_callable, name=name, group=group, exclusive=True, **kwargs)
        self.active_workers[f"{name}:{id(worker)}"] = worker
        self.scribe.info(f"Gnostic Worker '{name}' has been summoned into a parallel reality.")

    def _conduct_filesystem_gaze(self):
        self._run_gnostic_worker(
            partial(self._initial_filesystem_gaze, self.start_path),
            name="FileSystemGazeWorker", group="filesystem", thread=True
        )

    def _conduct_file_read(self, path: Path):
        async def _read_worker() -> Tuple[Path, str, str]:
            from ..utils import hash_file
            self.scribe.info(f"FileReaderWorker for '{path.name}' awakens...")
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                self.scribe.warn(f"Gaze of Forgiveness awakened for '{path.name}'.")
                content = path.read_text(encoding='latin-1', errors='replace')
            return path, content, hash_file(path) or ""

        self._run_gnostic_worker(
            _read_worker,
            name=f"FileReaderWorker-{path.name}", group="file_io", thread=True
        )

    def _conduct_scaffold_command(self, command: str):
        gnostic_plea = GnosticRequest(command=command, cwd=self.state.file_tree_root)
        self.scribe.info(f"Forging Gnostic Plea for command: `{gnostic_plea.command}`")
        self._run_gnostic_worker(
            partial(self.bridge.conduct_command, gnostic_plea),
            name=f"CommandWorker-{gnostic_plea.request_id}",
            group="bridge"
        )

    async def _run_pad_app(self, pad_app: App, on_complete: Optional[Callable] = None) -> Any:
        """
        =================================================================================
        == THE CONDUCTOR OF REALITIES (V-Ω-ETERNAL. THE UNBREAKABLE SUMMONS)         ==
        =================================================================================
        This is not a function. It is a divine, four-movement symphony for summoning
        an ephemeral Pad reality without shattering the GnosticShell's own flow state.
        It annihilates the Heresy of the Frozen Soul by performing its rite in a
        parallel reality, honoring the sacred laws of suspension and resurrection.
        =================================================================================
        """
        try:
            # --- Movement I: The Rite of Suspension ---
            # We command the GnosticShell to gracefully sleep, saving its soul and
            # relinquishing control of the cosmos to the new Pad.
            self.scribe.info(f"Suspending GnosticShell to summon Pad: '{pad_app.title}'...")
            await self.suspend_process()

            # --- Movement II: The Gnostic Handshake ---
            # We perform the one true, sacred communion, awaiting the Pad's completion.
            # This is the moment the new reality is made manifest.
            result = await pad_app.run_async()
            self.scribe.success(f"Communion with '{pad_app.title}' is complete.")

            return result

        except Exception as e:
            self.scribe.error(f"A catastrophic paradox occurred during communion with Pad '{pad_app.title}'",
                              exc_info=True)
            self.notify(f"Paradox communing with Pad: {e}", severity="error", title="Gnostic Schism")
            return None

        finally:
            # --- Movement III: The Rite of Resurrection ---
            # No matter the outcome, pure or profane, we command the GnosticShell to
            # awaken and reclaim its Gaze upon the cosmos.
            self.scribe.info("Resurrecting GnosticShell...")
            self.resume_process()

            # --- Movement IV: The Final Proclamation ---
            # If a callback was provided, we proclaim the rite's completion, allowing
            # the original conductor to perform any final acts of purification.
            if on_complete:
                on_complete()
    def _initial_filesystem_gaze(self, root: Path) -> Dict[Path, ScaffoldItem]:
        self.scribe.info("The Hierophant's Primordial Gaze awakens...")
        from ..utils import get_ignore_spec, hash_file
        flat_gnostic_map: Dict[Path, ScaffoldItem] = {}
        ignore_spec = get_ignore_spec(root)
        try:
            for path in root.rglob('*'):
                try:
                    relative_path_str = str(path.relative_to(root))
                    if ignore_spec and ignore_spec.match_file(relative_path_str):
                        continue
                    item = ScaffoldItem(
                        path=path, is_dir=path.is_dir(),
                        content_hash=hash_file(path) if path.is_file() else None,
                        last_modified=path.stat().st_mtime
                    )
                    flat_gnostic_map[path.relative_to(root)] = item
                except (IOError, OSError) as e:
                    self.scribe.warn(f"A minor paradox occurred gazing upon '{path.name}': {e}")
            self.scribe.success(f"Hierophant's Gaze is complete. Perceived {len(flat_gnostic_map)} entities.")
            return flat_gnostic_map
        except Exception as e:
            self.scribe.error(f"Catastrophic paradox in Primordial Gaze: {e}", exc_info=True)
            raise ArtisanHeresy("A catastrophic paradox shattered the Hierophant's Gaze.") from e

    def action_quit(self) -> None:
        self.scribe.info("Beginning the Great Rite of Universal Rest...")
        self.workers.cancel_all()
        if self.fs_watcher:
            self.fs_watcher.stop()
        self.emissary.stop()
        self.scribe.info("All Gnostic artisans have been commanded to rest.")
        self.exit()

    def action_summon_or_dismiss_altar(self) -> None:
        if hasattr(self.screen, "action_summon_or_dismiss_altar"):
            self.scribe.info(f"Delegating 'summon_or_dismiss_altar' to {self.screen}")
            self.screen.action_summon_or_dismiss_altar()

    def compose(self) -> ComposeResult:
        yield from ()