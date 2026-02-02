# Path: studio/pads/refactor_pad.py
# ---------------------------------
import asyncio  # <--- THE DIVINE SUMMONS OF THE LOOP
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any, Set

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import var
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Tree, Label, Input, Button, Static, DataTable, Log, Markdown
from textual.widgets._tree import TreeNode

from ...artisans.transmute import TransmuteArtisan
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.blueprint_scribe import BlueprintScribe
from ...core.runtime import ScaffoldEngine
from ...interfaces.requests import TransmuteRequest
from ...logger import Scribe

Logger = Scribe("RefactorPad")


# --- GNOSTIC CONTRACTS ---

@dataclass
class RefactorNode:
    """The soul of a tree node."""
    path: Path
    is_dir: bool
    seed_origin: Optional[Path] = None

    @property
    def name(self) -> str:
        return self.path.name


@dataclass
class TreeState:
    """A snapshot of the universe for Time Travel."""
    chronicle: Dict[str, Path]
    structure: Dict[str, Any]


# --- UI COMPONENTS ---

class BaseModal(ModalScreen):
    def compose_content(self) -> ComposeResult:
        yield Label("Override me")

    def compose(self) -> ComposeResult:
        with Vertical(classes="modal-box"):
            yield from self.compose_content()


class InputModal(BaseModal):
    def __init__(self, prompt: str, initial_value: str = ""):
        self.prompt_text = prompt
        self.initial_value = initial_value
        super().__init__()

    def compose_content(self) -> ComposeResult:
        yield Label(self.prompt_text, classes="modal-title")
        yield Input(value=self.initial_value, id="modal-input")
        with Horizontal(classes="modal-buttons"):
            yield Button("Confirm", variant="primary", id="confirm")
            yield Button("Cancel", variant="error", id="cancel")

    def on_mount(self):
        self.query_one(Input).focus()

    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed):
        if event.button.id == "confirm":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted):
        self.dismiss(event.value)


class RegexModal(BaseModal):
    def compose_content(self) -> ComposeResult:
        yield Label("Mass Transmutation (Regex Rename)", classes="modal-title")
        yield Label("Find Pattern (Regex):")
        yield Input(placeholder=r"^src/(.*)\.js$", id="find-input")
        yield Label("Replace Pattern:")
        yield Input(placeholder=r"src/\1.ts", id="replace-input")
        with Horizontal(classes="modal-buttons"):
            yield Button("Transmute", variant="warning", id="confirm")
            yield Button("Cancel", id="cancel")

    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed):
        if event.button.id == "confirm":
            find = self.query_one("#find-input", Input).value
            replace = self.query_one("#replace-input", Input).value
            if find:
                self.dismiss((find, replace))
            else:
                self.dismiss(None)
        else:
            self.dismiss(None)


class WelcomeModal(BaseModal):
    """The Gnostic Guide for the initiate."""

    def compose_content(self) -> ComposeResult:
        yield Label("Welcome to the Quantum Forge", classes="modal-title")
        yield Markdown("""
        **Reshape Reality with Visual Gnosis.**

        • **Left Pane:** The Reality that Is (Read-Only).
        • **Right Pane:** The Prophecy that Shall Be (Editable).

        **Controls:**
        • `m`: **Move/Rename** selected item.
        • `d`: **Delete** the selected item.
        • `a`: **Add** a new child item.
        • `Enter`: **Execute** the refactor.

        The engine will automatically track your changes and heal all imports.
        """)
        with Horizontal(classes="modal-buttons"):
            yield Button("Enter the Forge", variant="primary", id="dismiss_welcome")

    def on_mount(self):
        # Capture focus to prevent key-leakage to the main app
        self.query_one("#dismiss_welcome").focus()

    @on(Button.Pressed, "#dismiss_welcome")
    def dismiss_modal(self):
        self.dismiss()


class PreviewModal(BaseModal):
    def __init__(self, plan: List[Dict[str, Any]]):
        self.plan = plan
        super().__init__()

    def compose_content(self) -> ComposeResult:
        yield Label("Prophecy of Transmutation", classes="modal-title")

        table = DataTable(id="preview-table")
        table.add_columns("Action", "Path", "Gnostic Origin")

        for action in self.plan:
            kind = action['kind']
            path = str(action['path'])
            details = action.get('details', '')

            if kind == 'MOVE':
                kind_styled = Text("MOVE", style="bold yellow")
            elif kind == 'CREATE':
                kind_styled = Text("CREATE", style="bold green")
            elif kind == 'DELETE':
                kind_styled = Text("DELETE", style="bold red")
            else:
                kind_styled = Text(kind)

            table.add_row(kind_styled, path, details)

        yield table

        with Horizontal(classes="modal-buttons"):
            yield Button("Make Manifest", variant="success", id="execute")
            yield Button("Refine Plan", variant="primary", id="edit")

    @on(Button.Pressed)
    def handle_buttons(self, event: Button.Pressed):
        self.dismiss(event.button.id == "execute")


class ExecutionModal(BaseModal):
    def compose_content(self) -> ComposeResult:
        yield Label("Executing Transmutation...", classes="modal-title")
        yield Log(id="execution-log", highlight=True)
        with Horizontal(classes="modal-buttons"):
            yield Button("Close", variant="primary", id="close", disabled=True)

    def add_log(self, message: str):
        self.query_one(Log).write(message)

    def execution_finished(self, success: bool):
        btn = self.query_one("#close", Button)
        btn.disabled = False
        btn.variant = "success" if success else "error"
        btn.label = "Return to Shell"

    @on(Button.Pressed)
    def close(self):
        self.dismiss()


# --- THE APP ---

class RefactorPad(App[Optional[str]]):
    """
    The Quantum Forge.
    """
    CSS_PATH = "refactor.css"

    BINDINGS = [
        Binding("q", "quit_no_save", "Quit"),
        Binding("enter", "preview_refactor", "Execute"),
        Binding("m", "move_node", "Move"),
        Binding("r", "move_node", "Rename"),
        Binding("d", "delete_node", "Delete"),
        Binding("a", "add_node", "Add"),
        Binding("e", "expand_all", "Expand All"),
        Binding("c", "collapse_all", "Collapse All"),

        # --- 12 ELEVATIONS ---
        Binding("ctrl+z", "undo", "Undo"),
        Binding("ctrl+y", "redo", "Redo"),
        Binding("ctrl+r", "regex_rename", "Regex Rename"),
        Binding("ctrl+f", "flatten_dir", "Flatten Dir"),
        Binding("ctrl+e", "encapsulate", "Encapsulate"),
        Binding("ctrl+l", "toggle_layout", "Layout"),
        Binding("ctrl+h", "toggle_hidden", "Toggle Unchanged"),
        Binding("tab", "next_change", "Next Change"),
        # Vim Navigation
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]

    # Reactive State
    filter_text = var("")
    show_unchanged = var(True)
    layout_mode = var("horizontal")

    def __init__(
            self,
            before_items: List[ScaffoldItem],
            after_items: List[ScaffoldItem],
            meta_gnosis: Dict[str, Any],
            project_root: Path,
            engine: Optional[ScaffoldEngine] = None
    ):
        self.before_items = before_items
        self.initial_after_items = after_items
        self.meta_gnosis = meta_gnosis
        self.project_root = project_root
        self.engine = engine or ScaffoldEngine(project_root=project_root)

        self.gnostic_chronicle: Dict[str, Path] = {}
        self.original_paths: Set[str] = set()

        # Time Travel Stacks
        self.history_stack: List[TreeState] = []
        self.redo_stack: List[TreeState] = []
        self.is_time_traveling = False

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(id="main-container", classes="horizontal"):
            # Reality Pane
            with Vertical(id="left-pane", classes="pane"):
                yield Label("Reality (Before)", classes="pane-title")
                yield Tree("Project Root", id="tree-before")

            # Prophecy Pane (THE COCKPIT)
            with Vertical(id="right-pane", classes="pane"):
                yield Label("Prophecy (After)", classes="pane-title")

                # The Omniscient Eye
                with Horizontal(id="search-container"):
                    yield Input(placeholder="Filter Prophecy... (Start typing)", id="search-input")

                # The Tree
                yield Tree("Project Root", id="tree-after")

                # --- THE GNOSTIC CONTROL BAR (NEW) ---
                with Horizontal(id="control-bar"):
                    yield Button("👁️ Preview & Execute", variant="success", id="btn_execute")
                    yield Button("💾 Save Plan Only", variant="primary", id="btn_save_plan")

        yield Static(id="hud", content="Gnostic Telemetry: Initializing...")
        yield Footer()

    def on_mount(self):
        self.title = f"Quantum Forge: {self.project_root.name}"
        self._populate_tree("tree-before", self.before_items, read_only=True)
        self._populate_tree("tree-after", self.initial_after_items, read_only=False)

        self._update_hud()
        self.query_one("#tree-after").focus()
        self._snapshot_state()
        self.push_screen(WelcomeModal())

    # --- CONTROL BAR HANDLERS (NEW) ---

    @on(Button.Pressed, "#btn_execute")
    def on_execute_btn(self):
        """The user clicks 'Preview & Execute'."""
        self.action_preview_refactor()

    @on(Button.Pressed, "#btn_save_plan")
    def on_save_plan_btn(self):
        """The user clicks 'Save Plan Only'."""
        self.action_finalize_refactor()

    # --- CHRONOMANCER'S DIAL ---

    def _snapshot_state(self):
        if self.is_time_traveling: return
        tree_data = self._serialize_tree(self.query_one("#tree-after", Tree).root)
        snapshot = TreeState(
            chronicle=self.gnostic_chronicle.copy(),
            structure=tree_data
        )
        self.history_stack.append(snapshot)
        self.redo_stack.clear()
        if len(self.history_stack) > 50: self.history_stack.pop(0)
        self._update_hud()

    def action_undo(self):
        if len(self.history_stack) <= 1:
            self.notify("Genesis reached.", severity="warning")
            return
        current_snapshot = self.history_stack.pop()
        self.redo_stack.append(current_snapshot)
        target = self.history_stack[-1]
        self._restore_state(target)
        self.notify("Time Reversed.")

    def action_redo(self):
        if not self.redo_stack:
            self.notify("No future timelines.", severity="warning")
            return
        target = self.redo_stack.pop()
        self.history_stack.append(target)
        self._restore_state(target)
        self.notify("Time Restored.")

    def _restore_state(self, state: TreeState):
        self.is_time_traveling = True
        try:
            self.gnostic_chronicle = state.chronicle.copy()
            tree = self.query_one("#tree-after", Tree)
            tree.clear()
            tree.root.expand()
            self._deserialize_tree(tree.root, state.structure)
            self._update_hud()
        finally:
            self.is_time_traveling = False

    def _serialize_tree(self, node: TreeNode) -> Dict[str, Any]:
        data = node.data
        payload = None
        if data:
            payload = {'path': str(data.path), 'is_dir': data.is_dir,
                       'seed': str(data.seed_origin) if data.seed_origin else None}
        children = [self._serialize_tree(c) for c in node.children]
        return {'data': payload, 'children': children, 'expanded': node.is_expanded}

    def _deserialize_tree(self, node: TreeNode, state: Dict[str, Any]):
        if state['data']:
            d = state['data']
            seed = Path(d['seed']) if d['seed'] else None
            r_node = RefactorNode(path=Path(d['path']), is_dir=d['is_dir'], seed_origin=seed)
            node.data = r_node
            self._style_node(node)

        if state['expanded']:
            node.expand()
        else:
            node.collapse()

        for child_state in state['children']:
            if child_state['data']:
                label = Path(child_state['data']['path']).name
                new_node = node.add(label)
                self._deserialize_tree(new_node, child_state)

    # --- QUANTUM FACULTIES ---

    def action_toggle_layout(self):
        cont = self.query_one("#main-container")
        if "horizontal" in cont.classes:
            cont.remove_class("horizontal")
            cont.add_class("vertical")
            self.notify("Layout: Vertical")
        else:
            cont.remove_class("vertical")
            cont.add_class("horizontal")
            self.notify("Layout: Side-by-Side")

    def action_toggle_hidden(self):
        self.show_unchanged = not self.show_unchanged
        self._apply_filters()
        self.notify(f"Unchanged Files: {'Visible' if self.show_unchanged else 'Hidden'}")

    def action_next_change(self):
        tree = self.query_one("#tree-after", Tree)
        nodes = self._collect_all_nodes(tree.root)
        start_idx = -1
        if tree.cursor_node:
            try:
                start_idx = nodes.index(tree.cursor_node)
            except ValueError:
                pass

        for i in range(1, len(nodes)):
            idx = (start_idx + i) % len(nodes)
            node = nodes[idx]
            if self._is_modified(node):
                tree.select_node(node)
                tree.scroll_to_node(node)
                return
        self.notify("No more changes found.")

    def action_cursor_down(self):
        self.query_one("#tree-after", Tree).action_cursor_down()

    def action_cursor_up(self):
        self.query_one("#tree-after", Tree).action_cursor_up()

    @on(Input.Changed, "#search-input")
    def on_search(self, event: Input.Changed):
        self.filter_text = event.value
        self._apply_filters()

    def _apply_filters(self):
        tree = self.query_one("#tree-after", Tree)
        term = self.filter_text.lower()

        def _visit(n):
            data = n.data
            if not data:
                n.display = True
                return
            matches_search = term in data.name.lower()
            is_mod = self._is_modified(n)
            matches_change = self.show_unchanged or is_mod
            should_show = matches_search and matches_change

            if not data.is_dir:
                n.display = should_show
            else:
                n.display = should_show

            for c in n.children: _visit(c)

        _visit(tree.root)

    # --- COMPLEX TRANSFORMATIONS ---

    def action_regex_rename(self):
        def _on_transmute(result):
            if not result: return
            pattern, repl = result
            self._snapshot_state()
            count = self._apply_regex_rename(pattern, repl)
            self.notify(f"Transmuted {count} souls.")
            self._update_hud()

        self.push_screen(RegexModal(), _on_transmute)

    def _apply_regex_rename(self, pattern: str, replacement: str) -> int:
        count = 0
        regex = re.compile(pattern)
        tree = self.query_one("#tree-after", Tree)
        nodes = [n for n in self._collect_all_nodes(tree.root) if n.data and not n.data.is_dir]

        for node in nodes:
            rel_path = str(node.data.path)
            if regex.search(rel_path):
                new_path_str = regex.sub(replacement, rel_path)
                try:
                    self._perform_transform(node, new_path_str)
                    count += 1
                except Exception:
                    pass
        return count

    def action_flatten_dir(self):
        tree = self.query_one("#tree-after", Tree)
        node = tree.cursor_node
        if not node or not node.data.is_dir:
            self.notify("Select a directory.", severity="warning")
            return

        self._snapshot_state()
        parent_node = node.parent
        children = list(node.children)
        for child in children:
            self._move_tree_node(child, parent_node)
            self._recalculate_child_paths(child)

        self._prune_chronicle(node)
        node.remove()
        self.notify(f"Flattened '{node.data.name}'.")
        self._update_hud()

    def action_encapsulate(self):
        tree = self.query_one("#tree-after", Tree)
        node = tree.cursor_node
        if not node: return

        def _on_input(folder_name):
            if not folder_name: return
            self._snapshot_state()
            parent = node.parent
            self._perform_add(parent, folder_name + "/")
            new_folder_node = parent.children[-1]
            self._move_tree_node(node, new_folder_node)
            self._recalculate_child_paths(node)
            self.notify(f"Encapsulated in '{folder_name}'.")
            self._update_hud()

        self.push_screen(InputModal(f"Encapsulate '{node.data.name}' in new folder:"), _on_input)

    # --- CORE LOGIC ---

    def _populate_tree(self, tree_id: str, items: List[ScaffoldItem], read_only: bool):
        tree = self.query_one(f"#{tree_id}", Tree)
        tree.root.expand()
        tree.root.data = RefactorNode(Path("."), is_dir=True, seed_origin=Path("."))

        nodes: Dict[Path, TreeNode] = {Path("."): tree.root}
        sorted_items = sorted(items, key=lambda x: len(x.path.parts) if x.path else 0)

        for item in sorted_items:
            if not item.path or str(item.path).startswith("$$"): continue
            if read_only: self.original_paths.add(str(item.path))

            parent_path = item.path.parent
            if parent_path not in nodes: self._forge_missing_parents(parent_path, nodes, tree.root)

            parent_node = nodes[parent_path]
            seed = item.seed_path if item.seed_path else item.path
            node_data = RefactorNode(path=item.path, is_dir=item.is_dir, seed_origin=seed)

            if not read_only: self.gnostic_chronicle[str(item.path)] = seed

            new_node = parent_node.add("", data=node_data, expand=item.is_dir)
            self._style_node(new_node)
            nodes[item.path] = new_node

    def _forge_missing_parents(self, target_path: Path, node_map: Dict[Path, TreeNode], root_node: TreeNode):
        if str(target_path) == ".": return
        if target_path in node_map: return
        parent = target_path.parent
        if parent not in node_map: self._forge_missing_parents(parent, node_map, root_node)
        parent_node = node_map.get(parent, root_node)

        data = RefactorNode(path=target_path, is_dir=True, seed_origin=target_path)
        new_node = parent_node.add("", data=data, expand=True)
        self._style_node(new_node)
        node_map[target_path] = new_node

    def _style_node(self, node: TreeNode):
        data: RefactorNode = node.data
        if not data: return
        icon = "📁 " if data.is_dir else "📄 "
        label = Text(f"{icon}{data.name}")

        if data.seed_origin is None:
            label.stylize("bold green")  # Created
        elif data.seed_origin != data.path:
            label.stylize("bold yellow italic")  # Moved
        elif str(data.path) not in self.original_paths:
            label.stylize("green")  # Implicit
        else:
            label.stylize("bold cyan" if data.is_dir else "white")  # Pure

        node.set_label(label)

    def _is_modified(self, node: TreeNode) -> bool:
        d = node.data
        if not d: return False
        if d.seed_origin is None: return True
        if d.seed_origin != d.path: return True
        return False

    def _update_hud(self):
        moves = 0;
        creates = 0;
        deletes = 0
        tree = self.query_one("#tree-after", Tree)
        all_nodes = self._collect_all_nodes(tree.root)
        current_paths = set()

        for n in all_nodes:
            d = n.data
            if not d or str(d.path) == ".": continue
            current_paths.add(str(d.path))
            if d.seed_origin is None:
                creates += 1
            elif d.seed_origin != d.path:
                moves += 1

        for orig in self.original_paths:
            if orig not in current_paths: deletes += 1

        status = f"Moves: {moves} | Creates: {creates} | Deletes: {deletes} | Undo Stack: {len(self.history_stack)}"
        self.query_one("#hud", Static).update(status)

    def _collect_all_nodes(self, root: TreeNode) -> List[TreeNode]:
        nodes = []

        def _visit(n):
            nodes.append(n)
            for c in n.children: _visit(c)

        _visit(root)
        return nodes

    def action_move_node(self):
        self._snapshot_state()
        tree = self.query_one("#tree-after", Tree)
        node = tree.cursor_node
        if not node or node == tree.root: return

        def _on_input(new_path_str):
            if new_path_str:
                self._perform_transform(node, new_path_str)
                self._update_hud()

        self.push_screen(InputModal(f"Enter new path for '{node.data.name}':", str(node.data.path)), _on_input)

    def action_add_node(self):
        self._snapshot_state()
        tree = self.query_one("#tree-after", Tree)
        parent = tree.cursor_node or tree.root
        if parent.data and not parent.data.is_dir: parent = parent.parent

        def _on_input(name):
            if name:
                self._perform_add(parent, name)
                self._update_hud()

        self.push_screen(InputModal(f"Add child to '{parent.label}':"), _on_input)

    def action_delete_node(self):
        self._snapshot_state()
        tree = self.query_one("#tree-after", Tree)
        node = tree.cursor_node
        if not node or node == tree.root: return
        self._prune_chronicle(node)
        node.remove()
        self._update_hud()

    def action_quit_no_save(self):
        self.exit(result=None)

    def action_expand_all(self):
        self.query_one("#tree-after", Tree).root.expand_all()

    def action_collapse_all(self):
        self.query_one("#tree-after", Tree).root.collapse_all()

    def action_preview_refactor(self):
        plan = self._calculate_plan()
        if not plan:
            self.notify("Reality is unchanged.", severity="warning")
            return

        def _on_decision(execute: bool):
            if execute: self._run_execution_rite()

        self.push_screen(PreviewModal(plan), _on_decision)

    def action_finalize_refactor(self):
        """Writes the plan and exits (Save Plan Only)."""
        blueprint = self._forge_blueprint()
        self.exit(result=blueprint)

    # --- LOGIC HELPERS ---

    def _perform_transform(self, node: TreeNode, new_path_str: str):
        data: RefactorNode = node.data
        new_path = Path(new_path_str)
        current_parent_node = node.parent
        expected_parent_path = new_path.parent
        current_parent_path = current_parent_node.data.path if current_parent_node.data else Path(".")

        if expected_parent_path != current_parent_path:
            new_parent_node = self._resolve_or_create_tree_path(expected_parent_path)
            self._move_tree_node(node, new_parent_node)

        self._remap_chronicle_recursive(node, data.path, new_path)
        data.path = new_path
        self._style_node(node)

    def _perform_add(self, parent: TreeNode, name: str):
        parent_path = parent.data.path if parent.data else Path(".")
        new_path = parent_path / name
        is_dir = name.endswith("/")
        clean = name.rstrip("/")
        data = RefactorNode(path=new_path, is_dir=is_dir, seed_origin=None)
        self.gnostic_chronicle[str(new_path)] = None
        node = parent.add("", data=data, expand=True)
        self._style_node(node)

    def _resolve_or_create_tree_path(self, target_path: Path) -> TreeNode:
        tree = self.query_one("#tree-after", Tree)
        if str(target_path) == ".": return tree.root
        current = tree.root
        for part in target_path.parts:
            found = next((c for c in current.children if c.data.path.name == part and c.data.is_dir), None)
            if found:
                current = found
            else:
                p = current.data.path / part if str(current.data.path) != "." else Path(part)
                d = RefactorNode(path=p, is_dir=True, seed_origin=None)
                self.gnostic_chronicle[str(p)] = None
                current = current.add("", data=d, expand=True)
                self._style_node(current)
        return current

    def _move_tree_node(self, node: TreeNode, new_parent: TreeNode):
        def _clone(n, p):
            new = p.add(n.label, data=n.data, expand=n.is_expanded)
            self._style_node(new)
            for c in n.children: _clone(c, new)

        _clone(node, new_parent)
        node.remove()

    def _recalculate_child_paths(self, node: TreeNode):
        base_path = node.data.path
        for child in node.children:
            new_child_path = base_path / child.data.path.name
            child.data.path = new_child_path
            self._recalculate_child_paths(child)

    def _remap_chronicle_recursive(self, node: TreeNode, old_base: Path, new_base: Path):
        data: RefactorNode = node.data
        try:
            rel = data.path.relative_to(old_base)
            new_full = new_base / rel
        except ValueError:
            new_full = new_base
        old_key = str(data.path)
        new_key = str(new_full)
        if old_key in self.gnostic_chronicle:
            seed = self.gnostic_chronicle.pop(old_key)
            self.gnostic_chronicle[new_key] = seed
        data.path = new_full
        for c in node.children: self._remap_chronicle_recursive(c, old_base, new_base)
        self._style_node(node)

    def _prune_chronicle(self, node: TreeNode):
        if node.data: self.gnostic_chronicle.pop(str(node.data.path), None)
        for c in node.children: self._prune_chronicle(c)

    # --- EXECUTION & BLUEPRINT ---

    def _calculate_plan(self) -> List[Dict]:
        plan = []
        after_nodes = []

        def _collect(n):
            if n.data: after_nodes.append(n.data)
            for c in n.children: _collect(c)

        _collect(self.query_one("#tree-after").root)

        current_paths = set()
        for node_data in after_nodes:
            if str(node_data.path) == ".": continue
            current_paths.add(str(node_data.path))
            seed = node_data.seed_origin
            if seed is None:
                plan.append({'kind': 'CREATE', 'path': node_data.path, 'details': 'New Entity'})
            elif seed != node_data.path:
                plan.append({'kind': 'MOVE', 'path': node_data.path, 'details': str(seed)})

        for orig in self.original_paths:
            if orig not in current_paths: plan.append({'kind': 'DELETE', 'path': Path(orig), 'details': 'Removed'})
        return plan

    def _run_execution_rite(self):
        modal = ExecutionModal()
        self.push_screen(modal)
        self.run_worker(self._execution_worker(modal), exclusive=True)

    async def _execution_worker(self, modal: ExecutionModal):
        """
        The Background Worker for the Rite.
        Uses the Asyncio Loop to run the synchronous God-Engine without freezing the UI.
        [HERESY UNIFIER ASCENSION]: Now correctly catches and renders `ArtisanHeresy`.
        """
        try:
            modal.add_log("[bold cyan]Step 1: Forging Prophecy...[/bold cyan]\n")

            blueprint_content = self._forge_blueprint()

            target_path = self.project_root / "refactor.scaffold"
            modal.add_log(f"Inscribing blueprint to: {target_path.name}\n")
            target_path.write_text(blueprint_content, encoding="utf-8")

            modal.add_log("[bold cyan]Step 2: Summoning the Transmuter...[/bold cyan]\n")

            req = TransmuteRequest(
                path_to_scripture=str(target_path),
                project_root=self.project_root,
                force=True,
                no_edicts=False
            )

            artisan = TransmuteArtisan(self.engine)
            modal.add_log("Transmuting reality... (The God-Engine is working)\n")

            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, artisan.execute, req)

            if result.success:
                modal.add_log("\n[bold green]SUCCESS: The Rite is Complete.[/bold green]\n")
                for artifact in result.artifacts:
                    modal.add_log(f"  - {artifact.action}: {artifact.path.name}\n")

                modal.execution_finished(True)
            else:
                modal.add_log(f"\n[bold red]FAILURE: {result.message}[/bold red]\n")
                # Proclaim the structured heresies
                for h in result.heresies:
                    # If the heresy has a pre-rendered panel, we can try to use it.
                    # For a Log widget, plain text is safer and clearer.
                    modal.add_log(f"  [red]Heresy:[/red] {h.message}")
                    if h.details:
                        modal.add_log(f"    [dim]{h.details}[/dim]")
                    if h.suggestion:
                        modal.add_log(f"    [green]Suggestion:[/green] {h.suggestion}")

                modal.execution_finished(False)

        # [THE FIX] We catch the specific Gnostic Heresy first
        except ArtisanHeresy as heresy:
            modal.add_log(f"\n[bold red]GNOSTIC HERESY: {heresy.message}[/bold red]\n")
            # The `get_proclamation` method gives a nice, indented string of the full causal chain.
            modal.add_log(heresy.get_proclamation())
            modal.execution_finished(False)

        except Exception as e:
            # The final, unbreakable ward for all other paradoxes.
            modal.add_log(f"\n[bold red]CATASTROPHIC PARADOX: {e}[/bold red]\n")
            import traceback
            modal.add_log(traceback.format_exc())
            modal.execution_finished(False)

    def _forge_blueprint(self) -> str:
        final_items: List[ScaffoldItem] = []
        # [TYPE SAFETY FIX]
        tree = self.query_one("#tree-after", Tree)

        def _collect_nodes(node: TreeNode):
            if node.data and str(node.data.path) != ".":
                path_str = str(node.data.path)
                seed = self.gnostic_chronicle.get(path_str)
                # Safety: Self-Seed unmoved files
                final_seed = seed
                if not node.data.is_dir:
                    final_content = None if final_seed else ""
                    item = ScaffoldItem(
                        path=node.data.path, is_dir=False, seed_path=final_seed,
                        content=final_content, line_num=0
                    )
                    final_items.append(item)
                elif node.data.is_dir:
                    item = ScaffoldItem(path=node.data.path, is_dir=True, line_num=0)
                    final_items.append(item)
            for child in node.children: _collect_nodes(child)

        _collect_nodes(tree.root)
        scribe = BlueprintScribe(self.project_root)
        var_items = []
        for k, v in self.meta_gnosis.get("variables", {}).items():
            var_items.append(ScaffoldItem(
                path=Path(f"$$ {k}"), is_dir=False, content=v,
                line_type=GnosticLineType.VARIABLE, line_num=0
            ))
        commands = [cmd for cmd, _ in self.meta_gnosis.get("commands", [])]
        return scribe.transcribe(items=var_items + final_items, commands=commands, gnosis={}, rite_type="refactor")