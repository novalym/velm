# Path: artisans/inspect/artisan.py
# -------------------------

import difflib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
# --- The Divine Summons of the Luminous Scribe ---
from rich.text import Text

# --- The Divine Summons of the Interactive Soul ---
try:
    from textual.app import App, ComposeResult
    from textual.widgets import (
        Header, Footer, Tree, Static, DataTable, Button, Label,
        TabbedContent, TabPane, Input, ContentSwitcher
    )
    from textual.containers import Horizontal, Vertical, Container
    from textual.screen import Screen, ModalScreen
    from textual.binding import Binding
    from textual.reactive import reactive
    from textual.message import Message
    from textual import on, work

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False

from ...core.artisan import BaseArtisan
from ...interfaces.requests import InspectRequest
from ...interfaces.base import ScaffoldResult
from ...parser_core.parser import parse_structure
from ...contracts.data_contracts import ScaffoldItem
from ...utils import is_binary
from ...logger import get_console, Scribe
# === THE DIVINE HEALING: THE UNIVERSAL IMPORT ===
from ...rendering import LogicFlowGraphScribe
# ============================================
Logger = Scribe("GnosticInspector")


# --- GNOSTIC EVENTS ---
class ProphecyUpdated(Message):
    """Proclaimed when the timeline has changed (Variable Edit / Hot Reload)."""
    pass


class InspectorError(Message):
    """Proclaimed when the Oracle is blinded by a paradox."""

    def __init__(self, error_panel: Panel):
        self.error_panel = error_panel
        super().__init__()


class EditVariableScreen(ModalScreen[str]):
    """A divine modal to transmute a variable's value."""

    def __init__(self, key: str, current_value: str):
        self.key = key
        self.current_value = current_value
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="edit-dialog"):
            yield Label(f"Transmute Value: [cyan]{self.key}[/cyan]")
            yield Input(value=self.current_value, id="var-input")
            with Horizontal(id="edit-buttons"):
                yield Button("Confirm", variant="primary", id="confirm")
                yield Button("Cancel", id="cancel")

    def on_mount(self):
        self.query_one(Input).focus()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "confirm":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)


class InspectArtisan(BaseArtisan[InspectRequest]):
    """
    =================================================================================
    == THE GNOSTIC LENS (V-Ω-OMNISCIENT-LIVE-ASCENDED)                             ==
    =================================================================================
    LIF: 10,000,000,000,000 (THE LIVING SIMULATION)

    The Inspector General. It allows the Architect to gaze into the potential future
    without collapsing the quantum wave function.
    """

    def execute(self, request: InspectRequest) -> ScaffoldResult:

        # [FACULTY 13] THE REMOTE GAZE (Celestial Handling)
        blueprint_path_str = request.blueprint_path
        is_ephemeral = False
        temp_file_path: Optional[Path] = None

        if blueprint_path_str.startswith(('http://', 'https://')):
            try:
                import requests
                import tempfile

                if not request.non_interactive:
                    self.console.print(
                        f"[bold cyan]🔭 Communing with the Celestial Void ({blueprint_path_str})...[/bold cyan]")

                response = requests.get(blueprint_path_str, timeout=30)
                response.raise_for_status()

                # Forge Ephemeral Scripture
                # We try to infer extension, default to .scaffold
                suffix = Path(blueprint_path_str).suffix
                if not suffix or len(suffix) > 5: suffix = ".scaffold"

                tf = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=suffix, encoding='utf-8')
                tf.write(response.text)
                tf.close()

                blueprint = Path(tf.name)
                temp_file_path = blueprint
                is_ephemeral = True

            except Exception as e:
                return self.failure(f"Celestial Gaze failed: {e}")
        else:
            blueprint = Path(blueprint_path_str).resolve()

        if not blueprint.exists():
            return self.failure(f"Blueprint not found at: {blueprint}")

        try:
            # --- MOVEMENT I: THE PARSING RITE ---
            parser, items, commands, edicts, variables, dossier = parse_structure(
                blueprint,
                pre_resolved_vars=request.variables
            )

            if not parser:
                return self.failure("The blueprint is a void. Parsing failed.")

            # --- MOVEMENT II: THE TRIAGE OF FORMATS ---
            if request.lfg:
                if not dossier.logic_graph:
                    return self.success(
                        "The Scribe of Will is silent. No logic gates or loops were perceived in the scripture.")

                self.logger.info("The Scribe of Will awakens to chart the flow of causality...")

                scribe = LogicFlowGraphScribe(dossier.logic_graph)
                mermaid_scripture = scribe.render()

                self.console.print(Panel(
                    Syntax(mermaid_scripture, "mermaid", theme="monokai", background_color="default"),
                    title=f"[bold magenta]Logic Flow Graph: {blueprint.name}[/bold magenta]",
                    border_style="magenta"
                ))

                return self.success("The Graph of Will has been proclaimed.")
            # 1. Machine Apotheosis (JSON) - Static
            if request.format == 'json' or request.json_output:
                return self._render_json_apotheosis(items, variables, commands, dossier)

            # 2. Cartographer's Map (Mermaid) - Static
            if request.format == 'mermaid':
                return self._render_mermaid_cartography(items, blueprint.stem)

            # 3. The Luminous Experience (Interactive)
            if TEXTUAL_AVAILABLE and not request.non_interactive and sys.stdout.isatty():
                return self._launch_interactive_inspector(blueprint, request.variables, is_ephemeral)
            else:
                # Fallback to static report
                return self._render_static_luminous_report(items, variables, commands, blueprint)

        finally:
            # Clean up the ephemeral vessel if it was forged
            if temp_file_path and temp_file_path.exists():
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    pass

    def _launch_interactive_inspector(self, blueprint_path: Path, initial_vars: Dict[str, Any], is_ephemeral: bool):
        """Summons the Living App."""
        app = InspectorApp(blueprint_path, initial_vars, is_ephemeral)
        app.run()
        return self.success("Inspection concluded.")

    # =========================================================================
    # == MODE C: THE MACHINE APOTHEOSIS (JSON)                               ==
    # =========================================================================

    def _render_json_apotheosis(self, items: List[ScaffoldItem], variables: Dict[str, Any], commands: List[str],
                                dossier: Any) -> ScaffoldResult:
        """Machine readable output."""
        payload = {
            "meta": {"timestamp": datetime.now().isoformat()},
            "variables": variables,
            "structure": [
                {"path": str(i.path), "type": "dir" if i.is_dir else "file"}
                for i in items if not str(i.path).startswith("$$")
            ]
        }
        print(json.dumps(payload, indent=2))
        return self.success("JSON Proclaimed")

    def _render_mermaid_cartography(self, items, title):
        """Generates Mermaid diagram."""
        print(f"graph TD\n    root[{title}]")
        return self.success("Mermaid Proclaimed")

    def _render_static_luminous_report(self, items, variables, commands, blueprint):
        console = get_console()
        console.rule(f"[bold magenta]Gnostic Lens: {blueprint.name}[/bold magenta]")

        # 1. Context Table
        var_table = Table(title="Gnostic Context", box=None, show_header=True)
        var_table.add_column("Key", style="cyan")
        var_table.add_column("Value", style="green")

        for k, v in variables.items():
            val_str = str(v)
            if any(s in k.lower() for s in ['key', 'token', 'pass', 'secret']):
                val_str = "[red]**********[/red]"
            var_table.add_row(f"$$ {k}", val_str)

        console.print(var_table)
        console.print("")

        # 2. Prophetic Tree
        console.print(f"[bold]Architectural Prophecy ({blueprint.name})[/bold]")
        changes = {"new": 0, "mod": 0, "pure": 0}

        for item in items:
            if str(item.path).startswith("$$"): continue

            status_icon = "🛡️"
            style = "dim"
            target = Path.cwd() / item.path
            reason = "Unknown"

            if not target.exists():
                status_icon = "✨"
                style = "bold green"
                reason = "New Scripture"
                changes["new"] += 1
            elif not item.is_dir:
                try:
                    if target.read_text(encoding='utf-8').strip() != (item.content or "").strip():
                        status_icon = "⚡"
                        style = "bold yellow"
                        reason = "Content Drift"
                        changes["mod"] += 1
                    else:
                        reason = "Content Harmony"
                        changes["pure"] += 1
                except:
                    pass
            elif item.is_dir:
                changes["pure"] += 1

            prefix = "  " * (len(item.path.parts) - 1)
            name = item.path.name + ("/" if item.is_dir else "")
            console.print(f"{prefix}{status_icon} [bold {style}]{name}[/bold {style}] [dim]({reason})[/dim]")

        console.rule(
            f"[bold]Prophecy: {changes['new']} New, {changes['mod']} Modified, {changes['pure']} Unchanged.[/bold]")
        return self.success("Static Inspection Complete.")




if TEXTUAL_AVAILABLE:
    class InspectorApp(App):
        """The Interactive Altar of Inspection (V-Ω-MUTABLE-FIX)."""

        CSS = """
        Screen { layout: horizontal; background: $surface; }
        #left-pane { width: 35%; border-right: solid $primary; height: 100%; }
        #right-pane { width: 65%; height: 100%; }
        #tree-container { height: 1fr; }
        #details-view { height: 1fr; padding: 1; }
        .header { background: $accent; color: $text; dock: top; height: 1; padding-left: 1; text-style: bold; }
        .footer-stat { color: $text-muted; margin-right: 2; }
        #edit-dialog { padding: 2; border: thick $accent; background: $surface; width: 60; height: auto; }
        #edit-buttons { align: center middle; margin-top: 1; }
        Button { margin: 0 1; }
        #save-vars-btn { margin: 1; dock: bottom; }
        """

        BINDINGS = [
            Binding("q", "quit", "Quit"),
            Binding("r", "reload_prophecy", "Reload"),
            Binding("n", "next_diff", "Next Diff"),
            Binding("p", "prev_diff", "Prev Diff"),
            Binding("e", "export_report", "Export JSON"),
        ]

        # Reactive State
        prophecy_items: reactive[List[ScaffoldItem]] = reactive([])
        current_vars: reactive[Dict[str, Any]] = reactive({})
        maestro_commands: reactive[List[str]] = reactive([])
        active_item: reactive[Optional[ScaffoldItem]] = reactive(None)

        def __init__(self, blueprint_path: Path, initial_vars: Dict[str, Any], is_ephemeral: bool = False):
            super().__init__()
            self.blueprint_path = blueprint_path

            # [FIX 1] The Sovereign State of Overrides
            # We maintain a separate dictionary for user edits. This is the Source of Truth.
            self.overrides = initial_vars.copy()

            # current_vars is the display state
            self.current_vars = initial_vars.copy()

            self.is_ephemeral = is_ephemeral
            self.last_mtime = 0.0
            self.watcher_active = True

        def compose(self) -> ComposeResult:
            title_prefix = "🔭 [Remote] " if self.is_ephemeral else "🔭 "
            with Container(id="left-pane"):
                yield Label(f"{title_prefix}{self.blueprint_path.name}", classes="header")
                yield Input(placeholder="Filter Tree...", id="tree-filter")
                with Vertical(id="tree-container"):
                    yield Tree("Project Root", id="file-tree")
                yield Static(id="stats-bar", classes="header")

            with Container(id="right-pane"):
                yield Label("📝 Gnostic Detail", classes="header")
                with TabbedContent(initial="tab-diff"):
                    with TabPane("Diff", id="tab-diff"):
                        yield Static("Select a scripture.", id="diff-view")
                    with TabPane("Preview", id="tab-preview"):
                        yield Static("Select a scripture.", id="content-view")
                    with TabPane("Context (Vars)", id="tab-context"):
                        with Vertical():
                            yield DataTable(id="var-table")
                            yield Button("Save Variables to Scripture", variant="warning", id="save-vars-btn")
                    with TabPane("Maestro", id="tab-maestro"):
                        yield Static(id="maestro-view")
                    with TabPane("Heresies", id="tab-heresy"):
                        yield Static("No heresies detected.", id="heresy-view")

            yield Footer()

        def on_mount(self):
            self.action_reload_prophecy()
            self.set_interval(1.0, self._check_file_changes)

        def _check_file_changes(self):
            if not self.blueprint_path.exists(): return
            mtime = self.blueprint_path.stat().st_mtime
            if self.last_mtime > 0 and mtime > self.last_mtime:
                self.notify("Blueprint changed on disk. Reloading...", title="Phoenix Protocol")
                self.action_reload_prophecy()
            self.last_mtime = mtime

        @work(exclusive=True, thread=True)
        def action_reload_prophecy(self):
            """
            [THE RITE OF RE-PROPHECY]
            Re-parses the blueprint, strictly enforcing User Overrides.
            """
            try:
                # [FIX 2] Pass overrides explicitly to the parser
                parser, items, commands, _, final_vars, dossier = parse_structure(
                    self.blueprint_path,
                    pre_resolved_vars=self.overrides,
                    overrides=self.overrides  # Force these values to win
                )

                if parser:
                    self.prophecy_items = items

                    # [FIX 3] The Law of Retention
                    # We ensure final_vars reflects our overrides, even if the file disagreed.
                    # The parser *should* handle this via `overrides`, but we double-seal the pact.
                    final_vars.update(self.overrides)

                    self.current_vars = final_vars
                    self.maestro_commands = commands
                    self.post_message(ProphecyUpdated())
                else:
                    self.notify("Parsing returned void.", severity="error")

            except Exception as e:
                self.notify(f"Prophecy Failed: {e}", severity="error")

        @on(ProphecyUpdated)
        def refresh_ui(self):
            self._rebuild_tree()
            self._rebuild_var_table()
            self._rebuild_maestro()
            self._update_stats()

            if self.active_item:
                new_item = next((i for i in self.prophecy_items if i.path == self.active_item.path), None)
                if new_item:
                    self.active_item = new_item
                    self._render_detail_view(new_item)

        def _rebuild_tree(self):
            tree = self.query_one(Tree)
            tree.clear()
            tree.root.expand()

            filter_text = self.query_one("#tree-filter", Input).value.lower()

            for item in self.prophecy_items:
                if str(item.path).startswith("$$"): continue
                if filter_text and filter_text not in str(item.path).lower(): continue

                target = Path.cwd() / item.path

                if not target.exists():
                    icon = "✨"
                    style = "bold green"
                elif item.is_dir:
                    icon = "🛡️"
                    style = "blue"
                else:
                    is_diff = self._has_diff(target, item.content)
                    icon = "⚡" if is_diff else "🛡️"
                    style = "bold yellow" if is_diff else "dim"

                if item.is_dir: icon = "📁"

                label = Text(f"{icon} {item.path.name}", style=style)
                tree.root.add(label, data=item)

        def _rebuild_var_table(self):
            table = self.query_one(DataTable)
            table.clear(columns=True)
            table.add_columns("Variable", "Value (Double-click to Edit)")
            for k, v in self.current_vars.items():
                # Highlight overrides visually
                style = "bold cyan" if k in self.overrides else "green"
                table.add_row(f"$$ {k}", Text(str(v), style=style), key=k)

        def _rebuild_maestro(self):
            view = self.query_one("#maestro-view", Static)
            if not self.maestro_commands:
                view.update("[dim]The Maestro is silent.[/dim]")
                return
            text = "\n".join([f"$ {cmd}" for cmd in self.maestro_commands])
            view.update(Syntax(text, "bash", theme="monokai"))

        def _update_stats(self):
            count = len([i for i in self.prophecy_items if not str(i.path).startswith("$$")])
            new_count = len([i for i in self.prophecy_items if
                             not (Path.cwd() / i.path).exists() and not str(i.path).startswith("$$")])
            bar = self.query_one("#stats-bar", Static)
            bar.update(f"Files: {count} | New: {new_count} | Vars: {len(self.current_vars)}")

        def _has_diff(self, target: Path, planned: Optional[str]) -> bool:
            if not planned: return False
            if is_binary(target): return False
            try:
                current = target.read_text(encoding='utf-8').replace('\r\n', '\n').strip()
                new = planned.replace('\r\n', '\n').strip()
                return current != new
            except:
                return True

        def on_tree_node_selected(self, event: Tree.NodeSelected):
            item = event.node.data
            if item:
                self.active_item = item
                self._render_detail_view(item)

        def _render_detail_view(self, item: ScaffoldItem):
            content_view = self.query_one("#content-view", Static)
            if item.content:
                ext = item.path.suffix.lstrip('.') or "yaml"
                syntax = Syntax(item.content, ext, theme="monokai", line_numbers=True)
                content_view.update(syntax)
            else:
                content_view.update("[dim]Content is dynamic or binary.[/dim]")

            diff_view = self.query_one("#diff-view", Static)
            target = Path.cwd() / item.path

            if target.exists() and target.is_file() and item.content:
                try:
                    current = target.read_text(encoding='utf-8').splitlines()
                    planned = item.content.splitlines()
                    diff = list(
                        difflib.unified_diff(current, planned, fromfile="Reality", tofile="Prophecy", lineterm=""))
                    if diff:
                        diff_text = "\n".join(diff)
                        diff_view.update(Syntax(diff_text, "diff", theme="monokai"))
                    else:
                        diff_view.update("[green]Perfect Harmony.[/green]")
                except:
                    diff_view.update("[red]Cannot diff (Binary or Access Error)[/red]")
            elif not target.exists():
                diff_view.update("[green]✨ New File (Entire content is an addition)[/green]")
            else:
                diff_view.update("[dim]No diff available.[/dim]")

        @on(DataTable.CellSelected)
        def on_var_edit(self, event: DataTable.CellSelected):
            key = event.cell_key.row_key.value
            current_val = str(self.current_vars.get(key, ""))

            def _on_edit(new_val: str):
                if new_val is not None:
                    # [FIX 4] Update the Sovereign State
                    self.overrides[key] = new_val
                    self.current_vars[key] = new_val  # Optimistic update
                    self.notify(f"Transmuted {key} -> {new_val}")
                    self.action_reload_prophecy()

            self.push_screen(EditVariableScreen(key, current_val), _on_edit)

        @on(Input.Changed, "#tree-filter")
        def on_filter_changed(self, event: Input.Changed):
            self._rebuild_tree()

        def action_next_diff(self) -> None:
            if not self.prophecy_items:
                self.notify("The prophecy is empty.", severity="warning")
                return

            start_index = -1
            if self.active_item:
                try:
                    start_index = self.prophecy_items.index(self.active_item)
                except ValueError:
                    start_index = -1

            search_indices = (
                    list(range(start_index + 1, len(self.prophecy_items))) +
                    list(range(0, start_index + 1))
            )

            target_item: Optional[ScaffoldItem] = None
            wrapped = False

            for idx in search_indices:
                item = self.prophecy_items[idx]
                if str(item.path).startswith("$$"): continue
                if item.is_dir: continue

                target_path = Path.cwd() / item.path
                is_new = not target_path.exists()
                is_modified = False
                if not is_new and item.content:
                    is_modified = self._has_diff(target_path, item.content)

                if is_new or is_modified:
                    target_item = item
                    if idx <= start_index:
                        wrapped = True
                    break

            if target_item:
                tree = self.query_one(Tree)
                target_node = None
                nodes_to_check = [tree.root]
                while nodes_to_check:
                    node = nodes_to_check.pop()
                    if node.data and node.data.path == target_item.path:
                        target_node = node
                        break
                    nodes_to_check.extend(node.children)

                if target_node:
                    parent = target_node.parent
                    while parent:
                        parent.expand()
                        parent = parent.parent

                    tree.select_node(target_node)
                    tree.scroll_to_node(target_node, animate=True)
                    msg = f"Jumped to {'mod' if is_modified else 'new'}: {target_item.path.name}"
                    if wrapped: msg += " (Wrapped to start)"
                    self.notify(msg, title="Diff Navigator")
            else:
                self.notify("Perfect Harmony. Reality matches Prophecy.", title="Gnostic Peace", severity="information")

        def action_export_report(self):
            path = Path.cwd() / "inspection_report.json"
            data = {
                "timestamp": datetime.now().isoformat(),
                "variables": self.current_vars,
                "items": [str(i.path) for i in self.prophecy_items]
            }
            path.write_text(json.dumps(data, indent=2))
            self.notify(f"Report exported to {path}")

        @on(Button.Pressed, "#save-vars-btn")
        def on_save_vars(self):
            """Patches the .scaffold file with the current variables."""
            try:
                content = self.blueprint_path.read_text(encoding='utf-8')
                patched_content = content

                count = 0
                # [FIX 5] Use self.overrides, not self.current_vars
                # This ensures we only write what the user explicitly changed or passed via CLI.
                # Writing all current_vars might bloat the file with defaults.
                vars_to_write = self.overrides

                for key, val in vars_to_write.items():
                    if isinstance(val, bool):
                        val_str = str(val).lower()
                    elif isinstance(val, (int, float)):
                        val_str = str(val)
                    else:
                        val_str = f'"{val}"'

                    # Regex to find definition: $$ key = ... OR key = ...
                    # We prioritize the explicit $$ form but handle bare assignments too.
                    pattern = re.compile(rf'^(\s*(?:\$\$)?\s*{re.escape(key)}\s*(?::[^=]+)?\s*=\s*)(.*)$', re.MULTILINE)

                    if pattern.search(patched_content):
                        # Only replace if different to avoid noise (though regex replace is idempotentish)
                        patched_content = pattern.sub(rf'\1{val_str}', patched_content)
                        count += 1

                self.blueprint_path.write_text(patched_content, encoding='utf-8')

                if self.is_ephemeral:
                    self.notify(f"Updated Ephemeral Scripture. Note: Changes will vanish on exit.", severity="warning")
                else:
                    self.notify(f"Inscribed {count} variable updates to '{self.blueprint_path.name}'.",
                                title="Rite of Inscription")

                self.action_reload_prophecy()

            except Exception as e:
                self.notify(f"Inscription Failed: {e}", severity="error")