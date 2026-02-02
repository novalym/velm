# Path: studio/pads/distill_pad/distill_pad_app.py
# ------------------------------------------------

import asyncio
from pathlib import Path
from typing import Optional

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Button, Label

from .widgets import ConfigPane, FileSelector, PreviewPane
from .widgets.file_picker import FilePickerModal
from .state import (
    DistillState, ConfigChanged,
    DistillationComplete, DistillationFailed, InitialScanComplete
)
from ....core.cortex.engine import GnosticCortex
# --- THE DIVINE SUMMONS OF THE IRON CORE ---
# We import the official Pathfinder to ensure we use Rust acceleration and standard ignore logic.
from ....core.cortex.file_discoverer import FileDiscoverer
from ....logger import Scribe
from ....artisans.distill.core import DistillationOracle
from ....core.cortex.contracts import DistillationProfile
from ....core.cortex.tokenomics import TokenEconomist


class ConfigScreen(ModalScreen):
    """The Modal Altar of Will."""

    def compose(self) -> ComposeResult:
        with Vertical(id="config-dialog", classes="modal-box"):
            yield Label("Configure Distillation Strategy", classes="modal-title")
            with VerticalScroll(classes="modal-content"):
                yield ConfigPane(id="inner-config-pane")
            with Horizontal(classes="modal-footer"):
                yield Button("Close & Apply", variant="primary", id="close_config", classes="modal-btn")

    @on(Button.Pressed, "#close_config")
    def close_dialog(self):
        self.dismiss()


class CommandAltar(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical(classes="modal-box"):
            yield Label("Rite of Proclamation", classes="modal-title")
            yield Button("📋 Copy to Clipboard", variant="primary", id="cmd_copy", classes="modal-btn")
            yield Button("❌ Cancel", id="cmd_cancel", variant="error", classes="modal-btn")

    def on_button_pressed(self, event: Button.Pressed):
        self.dismiss(event.button.id)


class DistillPadApp(App[None]):
    """The Gnostic Workbench."""



    BINDINGS = [
        Binding("ctrl+p", "toggle_command_altar", "Proclaim", show=True),
        Binding("ctrl+comma", "toggle_config", "Settings", show=True),
        Binding("ctrl+o", "add_external_source", "Add Source", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+q", "request_quit", "Quit", show=True)
    ]

    def __init__(self, initial_file_path: Optional[Path] = None, project_root: Optional[Path] = None, **kwargs):
        super().__init__(**kwargs)
        root = project_root or Path.cwd()
        self.state = DistillState(project_root=root)
        self.scribe = Scribe("DistillPadApp")
        self.cortex = GnosticCortex(root)
        self._is_distilling = False
        self._distill_timer: Optional[asyncio.TimerHandle] = None

        # Intelligent Startup Selection
        if initial_file_path:
            resolved = initial_file_path.resolve()
            # Only select if it's a specific file/folder, not the root itself
            if resolved != root:
                self.state.selected_files.add(resolved)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            # The Sidebar Container allows for the 'Folding Space' (Collapse) animation
            with Vertical(id="file-selector-pane"):
                yield FileSelector(project_root=self.state.project_root, id="file-selector")
            yield PreviewPane(id="preview-pane")
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = f"Gazing upon: {self.state.project_root.name}"
        self._conduct_primordial_gaze()

    @work(exclusive=True, group="gaze", thread=True)
    def _conduct_primordial_gaze(self) -> None:
        """
        Scans the project root using the Gnostic Cortex.
        The Cortex internally uses FileDiscoverer, ensuring Iron Core acceleration.
        """
        try:
            self.call_from_thread(setattr, self.state, 'status', "Perceiving reality...")

            # The Cortex respects .gitignore automatically via its internal FileDiscoverer
            memory = self.cortex.perceive(force_refresh=True)

            all_file_paths = [
                self.state.project_root / gnosis.path
                for gnosis in memory.inventory
                if not (self.state.project_root / gnosis.path).is_dir()
            ]

            self.call_from_thread(self.post_message, InitialScanComplete(all_files=all_file_paths))
        except Exception as e:
            self.call_from_thread(self.post_message, DistillationFailed(error=e))

    @on(InitialScanComplete)
    def on_initial_scan_complete(self, message: InitialScanComplete) -> None:
        self.state.all_files = message.all_files

        # Default Selection Logic: If nothing selected, select ALL valid files.
        if not self.state.selected_files:
            self.state.selected_files = set(message.all_files)

        self.query_one(FileSelector).update_files(self.state.all_files, self.state.selected_files)
        self._trigger_distillation()

    def add_ignore_pattern(self, pattern: str):
        self.state.distill_config.ignore_patterns.append(pattern)
        self.notify(f"Added ignore pattern: {pattern}")
        self._trigger_distillation()

    @work(exclusive=True, group="distill", thread=True)
    def _conduct_distillation_rite(self) -> None:
        if self._is_distilling: return
        self._is_distilling = True
        try:
            self.call_from_thread(setattr, self.state, 'status', 'Distilling...')
            self.call_from_thread(self.query_one(PreviewPane).display_gazing_state, "Re-forging Prophecy...")

            config = self.state.distill_config
            final_budget = self._resolve_budget(config.budget)

            # We create the inclusion list.
            # The Oracle prioritizes 'include' over 'ignore'.
            includes = []
            for p in self.state.selected_files:
                try:
                    rel = p.relative_to(self.state.project_root)
                    includes.append(str(rel).replace('\\', '/'))
                except ValueError:
                    # External file: Pass absolute path
                    includes.append(str(p))

            distillation_profile = DistillationProfile(
                token_budget=final_budget,
                strategy=config.strategy,
                since=config.since,
                focus_keywords=config.focus_keywords,
                ignore=config.ignore_patterns,
                include=includes,
                strip_comments=(config.strategy == 'aggressive'),
                redact_secrets=True,
                redaction_level="mask",
                prioritize_tests=False
            )

            oracle = DistillationOracle(
                distill_path=self.state.project_root,
                profile=distillation_profile,
                silent=True
            )

            blueprint = oracle.distill()
            token_count = TokenEconomist().estimate_cost(blueprint)

            self.call_from_thread(self.post_message, DistillationComplete(blueprint=blueprint, token_count=token_count))

        except Exception as e:
            self.call_from_thread(self.post_message, DistillationFailed(error=e))
        finally:
            self._is_distilling = False

    def _trigger_distillation(self):
        if self._distill_timer is not None:
            self._distill_timer.stop()
        self._distill_timer = self.set_timer(0.5, self._conduct_distillation_rite)

    @on(FileSelector.SelectionChanged)
    def on_files_selected_msg(self, message: FileSelector.SelectionChanged) -> None:
        if self.state.selected_files == message.selected_paths: return
        self.state.selected_files = message.selected_paths
        self._trigger_distillation()

    @on(ConfigChanged)
    def on_config_changed(self, message: ConfigChanged) -> None:
        self.state.distill_config = message.config
        self.notify("Configuration updated. Re-calculating...")
        self._trigger_distillation()

    @on(DistillationComplete)
    def on_distillation_complete(self, message: DistillationComplete) -> None:
        self.state.current_blueprint = message.blueprint
        self.state.token_count = message.token_count
        self.query_one(PreviewPane).update_view(self.state)

    @on(DistillationFailed)
    def on_distillation_failed(self, message: DistillationFailed) -> None:
        self.query_one(PreviewPane).display_heresy(message.error)

    def action_toggle_config(self) -> None:
        self.push_screen(ConfigScreen())

    def action_toggle_sidebar(self) -> None:
        """The Rite of Folding Space."""
        sidebar = self.query_one("#file-selector-pane")
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            sidebar.add_class("-hidden")

    def action_add_external_source(self) -> None:
        """
        THE RITE OF INTELLIGENT EXPANSION.
        """

        def _on_path_selected(selected_path: Optional[Path]):
            if not selected_path: return
            path = selected_path.resolve()

            if not path.exists():
                self.notify(f"Path does not exist: {path}", severity="error")
                return

            self.notify(f"Gazing upon {path.name}...", title="Scanning")

            # Use the patched FileDiscoverer to filter node_modules/etc.
            # We explicitly pass the current ignore patterns from config.
            current_ignores = self.state.distill_config.ignore_patterns

            # We scan relative to the external root, but FileDiscoverer returns ABSOLUTE paths.
            discoverer = FileDiscoverer(
                root=path,
                ignore_patterns=current_ignores
            )
            new_files = discoverer.discover()

            if not new_files:
                self.notify(f"No valid scriptures found in {path.name} (checked ignores).", severity="warning")
                return

            # Update State
            self.state.all_files.extend(new_files)
            # Auto-select new files for convenience
            self.state.selected_files.update(new_files)

            # Force UI Rebuild
            self.query_one(FileSelector).update_files(self.state.all_files, self.state.selected_files)

            # Trigger Distillation
            self._trigger_distillation()

            self.notify(f"Added {len(new_files)} scriptures from {path.name}.")

        # Open picker at current project root
        self.push_screen(FilePickerModal(initial_path=self.state.project_root), _on_path_selected)

    def action_toggle_command_altar(self) -> None:
        def _handle(cmd):
            if cmd == "cmd_copy": self.action_copy_to_clipboard()

        self.push_screen(CommandAltar(), _handle)

    def action_copy_to_clipboard(self):
        try:
            import pyperclip
            pyperclip.copy(self.state.current_blueprint)
            self.notify("Gnosis copied to clipboard!")
        except:
            self.notify("Clipboard error: Install pyperclip", severity="error")

    def action_request_quit(self):
        self.exit()

    def _resolve_budget(self, budget):
        if isinstance(budget, int): return budget
        if isinstance(budget, str) and budget.isdigit(): return int(budget)
        if str(budget).lower() == 'infinite': return 10_000_000
        return 100000