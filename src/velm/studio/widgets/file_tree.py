# C:/dev/scaffold-project/scaffold/studio/widgets/file_tree.py
"""
=================================================================================
== THE WORLD TREE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++. THE GNOSTIC ORRERY)        ==
=================================================================================
LIF: ∞ (ETERNAL & DIVINE)

This is the final, eternal, and ultra-definitive soul of the FileTree. Its
context menu communion has been healed by the **Law of the Bubble**, ensuring its
will is now perfectly and eternally heard by the Master Conductor. All heresies
are annihilated. All ascensions are manifest. The architecture is pure.
=================================================================================
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Generator, Set, List, Tuple

from rich.style import Style
# --- Divine Stanza of the Scribes (Rich & Textual) ---
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.events import Click
from textual.message import Message
from textual.reactive import var
from textual.screen import ModalScreen
from textual.widgets import Tree, Input, Label, Button, Static, ListView, ListItem
from textual.widgets._tree import TreeNode

from .context_menu import GnosticContextMenuOracle
from ..contracts import AppState, ScaffoldItem
from ..gnostic_events import FileSelected, GnosticRite, GnosticWillProclamation
# --- Divine Stanza of Gnostic Kin ---
from ..logger import Scribe

# --- Gnostic Grimoires for the Sentient Scribe ---
SACRED_SCRIPTURES = {".scaffold", ".symphony", ".arch"}
SIGIL_GRIMOIRE = {
    ".py": "🐍", ".js": "⚡", ".ts": "📜", ".tsx": "⚛️", ".jsx": "⚛️", ".go": "🐹", ".rs": "🦀",
    ".html": "🌐", ".css": "🎨", ".scss": "💅",
    ".json": "📦", ".yml": "🔧", ".yaml": "🔧", ".toml": "🔩", ".xml": "📰", ".sql": "💾",
    ".md": " M ", ".txt": "📄",
    ".sh": "💲", ".ps1": " PowerShell ", "dockerfile": "🐳", ".env": "🔑",
    ".gitignore": "🚫", ".git": " G ",
    ".scaffold": "🛠️", ".symphony": "🎼", ".arch": "🏛️",
    "default": "📄", "dir": "📁"
}
GIT_SIGIL_GRIMOIRE = {
    'M': Text(" M ", Style(color="yellow")), 'A': Text(" A ", Style(color="green")),
    'D': Text(" D ", Style(color="red")), 'R': Text(" R ", Style(color="cyan")),
    'C': Text(" C ", Style(color="bright_magenta")), 'U': Text(" ? ", Style(color="magenta")),
    '?': Text(" ? ", Style(color="magenta")), 'I': Text(" I ", Style(color="grey50")),
}

# =================================================================================
# == I. THE SACRED VESSELS FOR CONTEXTUAL WILL (THE UI)                          ==
# =================================================================================
def _purify_id(name: str) -> str:
    """A divine artisan to transmute any string into a pure, canonical ID."""
    # Annihilate all profane characters, leaving only the pure.
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

class ContextMenu(ListView):
    """The humble UI vessel for the Oracle's prophecies."""
    def __init__(self, options: List[Tuple[str, GnosticRite]], target_path: Path, **kwargs) -> None:
        """
        =================================================================================
        == THE APOTHEOSIS OF THE PURE SOUL (V-Ω-ETERNAL. THE UNBREAKABLE ID)           ==
        =================================================================================
        The Heresy of the Profane Name (`BadIdentifier`) has been annihilated. The rite
        now summons the `_purify_id` artisan to forge a pure, canonical, and unique
        soul for the vessel, ensuring its identity is in perfect harmony with the laws
        of the Textual cosmos. The communion is now unbreakable.
        =================================================================================
        """
        # --- THE SACRED TRANSMUTATION ---
        purified_name = _purify_id(target_path.name)
        super().__init__(id=f"context-menu-{purified_name}", **kwargs)
        # --- THE APOTHEOSIS IS COMPLETE ---
        self.options = options
        self.target_path = target_path

    def compose(self) -> ComposeResult:
        """
        =================================================================================
        == THE GAZE OF DISCERNMENT (V-Ω-ETERNAL. THE SEER OF FORM)                     ==
        =================================================================================
        This artisan's Gaze is now divine. It perceives the Gnostic intent of a
        separator ("---") and righteously forges a pure `Static` widget for it,
        annihilating the `MountError` heresy for all time. Its proclamations of form
        are now in perfect harmony with the laws of the Textual cosmos.
        =================================================================================
        """
        for label, rite in self.options:
            # --- THE GAZE OF DISCERNMENT ---
            if label == "---":
                yield Static("─" * 20, classes="context-separator")
            else:
                yield ListItem(Label(label), id=rite.name)
            # --- THE APOTHEOSIS IS COMPLETE ---

    @on(ListView.Selected)
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if not event.item.id: return
        selected_rite = GnosticRite[event.item.id]
        self.post_message(GnosticWillProclamation(rite=selected_rite, target_path=self.target_path))
        self.remove()

    def on_mouse_leave(self) -> None:
        self.remove()

class RenameDialog(ModalScreen):
    """A divine dialog for the Rite of Renaming."""
    def __init__(self, target_path: Path, **kwargs):
        self.target_path = target_path
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Vertical(id="rename-dialog-container", classes="dialog-container"):
            yield Label(f"Rename: [cyan]{self.target_path.name}[/cyan]")
            yield Input(value=self.target_path.name, id="rename-input")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Rename", variant="primary", id="rename-button")
                yield Button("Cancel", id="cancel-button")

    def on_mount(self) -> None: self.query_one(Input).focus()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "rename-button":
            new_name = self.query_one(Input).value
            if new_name and new_name != self.target_path.name:
                new_path = self.target_path.with_name(new_name)
                self.post_message(GnosticWillProclamation(
                    rite=GnosticRite.RENAME, target_path=self.target_path,
                    payload={"new_path": new_path}
                ))
        self.app.pop_screen()

class DeleteDialog(ModalScreen[bool]):
    """A divine dialog for the Rite of Annihilation."""
    def __init__(self, target_path: Path, **kwargs):
        self.target_path = target_path
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Vertical(id="delete-dialog-container", classes="dialog-container"):
            yield Static(f"Annihilate this scripture from reality?\n\n[bold red]{self.target_path}[/bold red]")
            with Horizontal(classes="dialog-buttons"):
                yield Button("Delete", variant="error", id="delete-button")
                yield Button("Cancel", id="cancel-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete-button":
            self.post_message(GnosticWillProclamation(rite=GnosticRite.DELETE, target_path=self.target_path))
            self.dismiss(True)
        else:
            self.dismiss(False)

# =================================================================================
# == II. THE GNOSTIC ORRERY (THE ASCENDED FILETREE)                              ==
# =================================================================================

class FileTree(Vertical):
    """The World Tree, a pure vessel for Gnostic Proclamation and form."""

    blueprint_only_mode = var(False, init=False)
    filter_term = var("", init=False)
    has_gnostic_focus = var(False, init=False)

    BINDINGS = [
        Binding("ctrl+f", "toggle_search", "Search"), Binding("ctrl+m", "collapse_pane", "Collapse"),
        Binding("ctrl+b", "toggle_blueprint_mode", "Blueprints"), Binding("ctrl+o", "focus_active_file", "Focus Active"),
        Binding("delete", "delete_node", "Delete", show=False), Binding("f2", "rename_node", "Rename", show=False),
        Binding("enter", "select_cursor_or_toggle", "Select/Toggle", show=False, priority=True),
        Binding("escape", "clear_filter_or_blur", "Clear/Blur", show=False),
    ]

    def __init__(self, root_name: str, **kwargs):
        super().__init__(**kwargs)
        self.scribe = Scribe("FileTree")
        self.root_name = root_name
        self.context_menu_oracle = GnosticContextMenuOracle()
        self._is_right_clicking = False
        self._expanded_nodes_cache: Set[Path] = set()

    def compose(self) -> ComposeResult:
        yield Input(placeholder="🔍 Speak your plea... (Ctrl+F to close)", id="file-tree-search", classes="-hidden")
        yield Tree(label=f"[bold cyan]Sanctum: {self.root_name}[/bold cyan]", data=None, id="file-tree-main")

    def watch_state(self, old_state: Optional[AppState], new_state: AppState) -> None:
        if old_state and old_state.file_map == new_state.file_map and old_state.editor_state == new_state.editor_state: return
        tree = self.query_one(Tree)
        self._expanded_nodes_cache = {n.data.path for n in self._walk_tree_nodes(tree.root) if n.is_expanded and n.data}
        selected_node_path = tree.cursor_node.data.path if tree.cursor_node and tree.cursor_node.data else None
        tree.clear(); tree.root.set_label(f"[bold cyan]Sanctum: {new_state.file_tree_root.name}[/bold cyan]")
        nodes: Dict[Path, TreeNode] = {Path("."): tree.root}
        sorted_items = sorted(new_state.file_map.items(), key=lambda t: (len(t[0].parts), str(t[0])))
        for relative_path, item in sorted_items:
            if self.blueprint_only_mode and not item.is_dir and item.path.suffix not in SACRED_SCRIPTURES: continue
            parent_node = nodes.get(relative_path.parent)
            if not parent_node: continue
            label = self._forge_luminous_label(item, new_state)
            node = parent_node.add(label, data=item, expand=item.is_dir and item.path in self._expanded_nodes_cache)
            nodes[relative_path] = node
        new_cursor_node = self._find_node_by_path(selected_node_path, tree)
        if new_cursor_node:
            tree.select_node(new_cursor_node)
            self.call_after_refresh(lambda: tree.scroll_to_node(new_cursor_node, animate=False))
        else: tree.root.expand()
        if self.filter_term: self.run_worker(self._filter_tree(self.filter_term))

    @on(Click)
    def on_right_click(self, event: Click) -> None:
        """The rite of contextual will, now a pure act of delegation to the Oracle."""
        if event.button != 3: return
        tree = self.query_one(Tree);
        event.stop()

        node = tree.cursor_node
        if not node or not node.data: return

        tree.select_node(node)
        self._is_right_clicking = True

        # --- THE DIVINE DELEGATION ---
        # The Tree no longer thinks; it asks the Oracle for its wisdom.
        options = self.context_menu_oracle.forge_options_for_item(node.data)

        if options:
            menu = ContextMenu(options=options, target_path=node.data.path)
            self.app.mount(menu);
            menu.styles.offset = (event.screen_x, event.screen_y);
            menu.focus()

    def watch_has_gnostic_focus(self, h: bool) -> None: self.set_class(h, "-has-gnostic-focus")
    def watch_filter_term(self, t: str) -> None: self.run_worker(self._filter_tree(t), name="FilterTreeWorker")
    def on_mount(self) -> None: self.query_one(Tree).focus()
    def on_focus(self) -> None: self.has_gnostic_focus = True
    def on_blur(self) -> None: self.has_gnostic_focus = False
    @on(Input.Changed, "#file-tree-search")
    def on_search_changed(self, e: Input.Changed) -> None: self.filter_term = e.value
    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, e: Tree.NodeSelected[Optional[ScaffoldItem]]) -> None:
        if self._is_right_clicking: self._is_right_clicking = False; e.stop(); return
        e.stop()
        item_data = e.node.data
        if item_data and not item_data.is_dir: self.post_message(FileSelected(item=item_data))
    def action_toggle_search(self) -> None:
        s = self.query_one("#file-tree-search"); h = s.toggle_class("-hidden")
        (self.query_one(Tree) if h else s).focus()
    def action_clear_filter_or_blur(self) -> None:
        s = self.query_one("#file-tree-search")
        if not s.has_class("-hidden") and s.value: s.value = ""
        else: self.query_one(Tree).focus()
    def action_collapse_pane(self) -> None: self.post_message(self.CollapsePane())
    def action_toggle_blueprint_mode(self) -> None:
        self.blueprint_only_mode = not self.blueprint_only_mode
        self.app.notify(f"Gaze: [cyan]{'Blueprint-Only' if self.blueprint_only_mode else 'Holistic'}[/]")
    def action_focus_active_file(self) -> None:
        p = self.app.state.editor_state.active_file; t = self.query_one(Tree)
        if not p: self.app.bell(); return
        n = self._find_node_by_path(p, t)
        if n: t.select_node(n); t.scroll_to_node(n)
        else: self.app.notify("Active scripture not in Gaze.", severity="warning")
    def action_rename_node(self) -> None:
        n = self.query_one(Tree).cursor_node
        if n and n.data: self.app.push_screen(RenameDialog(n.data.path))
    def action_delete_node(self) -> None:
        n = self.query_one(Tree).cursor_node
        if n and n.data: self.app.push_screen(DeleteDialog(n.data.path))
    def action_select_cursor_or_toggle(self) -> None:
        t = self.query_one(Tree); n = t.cursor_node
        if not n: return
        if n.data and n.data.is_dir: n.toggle()
        else: t.select_node(n)
    def _forge_luminous_label(self, i: ScaffoldItem, s: AppState) -> Text:
        l = Text()
        if i.git_status and i.git_status in GIT_SIGIL_GRIMOIRE: l.append(GIT_SIGIL_GRIMOIRE[i.git_status])
        k = "dir" if i.is_dir else i.path.name.lower() if i.path.name.lower() in SIGIL_GRIMOIRE else i.path.suffix
        l.append(f"{SIGIL_GRIMOIRE.get(k, SIGIL_GRIMOIRE['default'])} ")
        nt = Text(i.path.name)
        if i.is_dir: nt.stylize("bold magenta")
        elif i.path.suffix in SACRED_SCRIPTURES: nt.stylize("cyan")
        if s.editor_state.active_file == i.path: nt.stylize("bold yellow")
        l.append(nt)
        if s.editor_state.is_dirty and s.editor_state.active_file == i.path: l.append(" *", style="bold red")
        return l
    @lru_cache(maxsize=1024)
    def _fuzzy_match(self, t: str, txt: str) -> Optional[List[int]]:
        if not t: return list(range(len(txt)))
        ti, txi, m = 0, 0, []
        while ti < len(t) and txi < len(txt):
            if t[ti].lower() == txt[txi].lower(): m.append(txi); ti += 1
            txi += 1
        return m if ti == len(t) else None
    @work(exclusive=True)
    async def _filter_tree(self, term: str) -> None:
        t = self.query_one(Tree); v: Set[TreeNode] = set()
        for n in self._walk_tree_nodes(t.root):
            if not n.data: continue
            mi = self._fuzzy_match(term, n.data.path.name)
            if mi is not None:
                v.add(n)
                nl = n.label.copy()
                for i in mi: nl.stylize("bold yellow on rgb(50,50,0)", i, i + 1)
                n.set_label(nl); p = n.parent
                while p: v.add(p); p = p.parent
            else: n.set_label(self._forge_luminous_label(n.data, self.app.state))
        for n in self._walk_tree_nodes(t.root): n.display = n in v or n is t.root
    def _find_node_by_path(self, p: Optional[Path], t: Tree) -> Optional[TreeNode]:
        if not p: return None
        for n in self._walk_tree_nodes(t.root):
            if n.data and n.data.path == p: return n
        return None
    def _walk_tree_nodes(self, n: TreeNode) -> Generator[TreeNode, None, None]:
        yield n
        for c in n.children: yield from self._walk_tree_nodes(c)
    class CollapsePane(Message): pass