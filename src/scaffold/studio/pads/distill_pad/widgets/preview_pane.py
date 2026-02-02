# scaffold/studio/pads/distill_pad/widgets/preview_pane.py

from __future__ import annotations

from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.traceback import Traceback as RichTraceback

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, ProgressBar, Label, Button, Input, DataTable

from ..state import DistillState


class PreviewPane(Vertical):
    """
    The Crystal Ball.
    Displays the distilled blueprint, telemetry, and progress.
    """

    DEFAULT_CSS = """
    PreviewPane {
        height: 100%;
        width: 100%;
        layout: vertical;
    }

    #preview-command-bar {
        height: 3;
        dock: top;
        padding: 0 1;
        align: center middle;
        background: $surface-darken-1;
        border-bottom: solid $primary;
    }

    #copy-blueprint-btn {
        width: auto;
        min-width: 8;
        margin-right: 1;
    }

    #search-blueprint-input {
        width: 1fr;
        height: 1;
        border: none;
        background: $surface-darken-2;
    }

    #preview-scroll-container {
        height: 1fr;
        scrollbar-gutter: stable;
        background: $surface;
    }

    #preview-display {
        height: auto;
        min-height: 100%;
        padding: 1 2;
    }

    #telemetry-container {
        dock: bottom;
        height: auto;
        max-height: 15;
        border-top: solid $primary;
        background: $surface-darken-1;
    }

    #telemetry-table {
        height: auto;
        width: 100%;
    }

    #token-scribe-container {
        height: 3;
        padding: 0 1;
        border-top: solid $primary;
        align: center middle;
        background: $surface-darken-2;
    }

    #token-progress {
        width: 1fr;
        margin-right: 2;
        height: 1;
    }

    #token-label {
        width: auto;
        min-width: 20;
        content-align: right middle;
    }
    """

    def compose(self) -> ComposeResult:
        """Forge the sacred vessels."""

        # 1. Command Bar
        with Horizontal(id="preview-command-bar"):
            yield Button("📋 Copy", id="copy-blueprint-btn", variant="primary")
            yield Input(placeholder="🔍 Search prophecy...", id="search-blueprint-input")

        # 2. The Scrollable Prophecy
        with VerticalScroll(id="preview-scroll-container"):
            yield Static(id="preview-display", expand=True)

        # 3. Telemetry & Budget
        with Vertical(id="telemetry-container"):
            yield DataTable(id="telemetry-table", show_header=False, cursor_type="none")
            with Horizontal(id="token-scribe-container"):
                yield ProgressBar(id="token-progress", total=100000, show_eta=False)
                yield Label("0 / 100,000 Tokens", id="token-label")

    def on_mount(self) -> None:
        """The Rite of First Light."""
        self.display_gazing_state("Awaiting the Primordial Gaze...")
        table = self.query_one(DataTable)
        table.add_columns("Key", "Value")

    def display_gazing_state(self, message: str = "The Oracle is Gazing...") -> None:
        """Transfigures the display into a waiting state."""
        preview_static = self.query_one("#preview-display", Static)
        gazing_markdown = Markdown(f"# {message}\n\n*The Gnostic symphony is being conducted in a parallel reality...*")
        preview_static.update(gazing_markdown)

        # Hide telemetry during gaze to prevent stale data
        self.query_one("#telemetry-container").display = False

    def update_view(self, state: DistillState) -> None:
        """
        [THE SCRIBE OF LIVING PROPHECY]
        Updates all visual elements with the new Gnostic Truth.
        """
        # 1. Show containers
        self.query_one("#telemetry-container").display = True

        # 2. Update Syntax Highlighting
        # We use 'yaml' as the default lexer for blueprints, or 'markdown' if it's a summary.
        # If content starts with '#', likely YAML-ish or Scaffold DSL.
        syntax = Syntax(
            state.current_blueprint,
            "yaml",
            theme="monokai",
            line_numbers=True,
            word_wrap=False
        )
        self.query_one("#preview-display", Static).update(syntax)

        # 3. Update Telemetry Table
        table = self.query_one(DataTable)
        table.clear()

        # Calculate Stats
        total_scanned = len(state.all_files)
        total_selected = len(state.selected_files)
        blueprint_size_kb = len(state.current_blueprint.encode('utf-8')) / 1024

        table.add_rows([
            ("Files Scanned", f"{total_scanned:,}"),
            ("Files Selected", f"[bold green]{total_selected:,}[/bold green]"),
            ("Blueprint Size", f"{blueprint_size_kb:.1f} KB"),
            ("Strategy", f"[cyan]{state.distill_config.strategy}[/cyan]"),
        ])

        # 4. Update Token Scribe
        prog = self.query_one(ProgressBar)
        label = self.query_one("#token-label", Label)

        max_tokens = self.app._resolve_budget(state.distill_config.budget)
        current_tokens = state.token_count

        prog.total = float(max_tokens)
        prog.progress = float(current_tokens)

        # Colorize based on budget pressure
        ratio = current_tokens / max(1, max_tokens)
        if ratio > 1.0:
            prog.bar_style = "bold red"
            label.update(f"[bold red]{current_tokens:,} / {max_tokens:,} (OVERFLOW)[/]")
        elif ratio > 0.9:
            prog.bar_style = "orange3"
            label.update(f"[orange3]{current_tokens:,} / {max_tokens:,}[/]")
        elif ratio > 0.75:
            prog.bar_style = "yellow"
            label.update(f"[yellow]{current_tokens:,} / {max_tokens:,}[/]")
        else:
            prog.bar_style = "green"
            label.update(f"[green]{current_tokens:,} / {max_tokens:,}[/]")

    def display_heresy(self, error: Exception) -> None:
        """
        [THE HERALD OF PARADOX]
        Displays a traceback when the Gaze is shattered.
        """
        self.query_one("#telemetry-container").display = False

        preview_static = self.query_one("#preview-display", Static)

        tb = RichTraceback.from_exception(type(error), error, error.__traceback__, show_locals=True)
        preview_static.update(tb)

    @on(Button.Pressed, "#copy-blueprint-btn")
    def on_copy_pressed(self) -> None:
        self.app.action_copy_to_clipboard()

    @on(Input.Changed, "#search-blueprint-input")
    def on_search_changed(self, event: Input.Changed) -> None:
        """Highlights search terms in the preview (Basic implementation)."""
        search_term = event.value
        if not search_term:
            # Reset view
            self.update_view(self.app.state)
            return

        # In a real implementation, we would use a custom highlighter.
        # For V1, we rely on Textual's native find or just reload (expensive).
        # A simple approach: Re-render with a different theme or style?
        # For now, we just re-render to ensure cleanliness, future ascension will highlight.
        # Implementing regex highlighting on top of Syntax in Rich is complex dynamically.
        pass