# Path: scaffold/shell/app.py

import os
import subprocess
import json
from pathlib import Path
from typing import List, Optional

from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Key
from textual.reactive import var, reactive
from textual.widgets import Footer, Header, Label, Static

# --- GNOSTIC IMPORTS ---
from .contracts import ExecutionMode, ShellIntent
from .interpreter import ShellInterpreter
from .widgets.dossier import LuminousDossier
from .widgets.orrery import Orrery
from .widgets.prompter import GnosticPrompter
from .widgets.history_screen import HistorySearchScreen
from .widgets.suggestion_menu import SuggestionMenu

# --- CONSTANTS OF PERSISTENCE ---
HISTORY_FILE = Path.home() / ".scaffold" / "shell_history.json"
MAX_HISTORY = 1000


class GnosticStatusBar(Static):
    """The heartbeat of the shell."""
    DEFAULT_CSS = """
    GnosticStatusBar {
        dock: bottom;
        height: 1;
        background: #1a1b26;
        color: #565f89;
        border-top: solid #565f89;
        layout: horizontal;
        padding: 0 1;
    }
    .status-item { margin-right: 2; color: #7aa2f7; }
    .status-label { color: #565f89; }
    .hint-label { color: #e0af68; text-style: italic; margin-left: 2; }
    """
    cwd_display: reactive[str] = reactive("~")
    context_hint: reactive[str] = reactive("Ready.")

    def compose(self) -> ComposeResult:
        yield Label("Sanctum: ", classes="status-label")
        yield Label(self.cwd_display, id="stat-cwd", classes="status-item")
        yield Label(" | ", classes="status-label")
        yield Label(self.context_hint, id="stat-hint", classes="hint-label")

    def watch_cwd_display(self, val: str):
        if self.is_mounted: self.query_one("#stat-cwd", Label).update(val)

    def watch_context_hint(self, val: str):
        if self.is_mounted: self.query_one("#stat-hint", Label).update(val)


class GnosticShell(App):
    """
    =================================================================================
    == THE GNOSTIC COCKPIT (V-Ω-OMNISCIENT-EDITION)                                ==
    =================================================================================
    """

    CSS_PATH = "shell.css"
    TITLE = "Scaffold Gnostic Shell"

    BINDINGS = [
        Binding("ctrl+b", "toggle_orrery", "Sidebar", show=True),
        Binding("ctrl+l", "clear_screen", "Purify", show=True),
        Binding("ctrl+r", "search_history", "Resurrect", show=True),
        Binding("ctrl+q", "quit", "Disconnect", show=True),
    ]

    current_cwd: var[str] = var(str(Path.cwd()))

    def __init__(self, project_root: Path = None):
        super().__init__()
        self.project_root = (project_root or Path.cwd()).resolve()
        self.interpreter = ShellInterpreter(self.project_root)
        # Load the Ancient Scrolls
        self.history = self._load_history()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="⚡")

        with Horizontal(id="workspace"):
            yield Orrery(self.project_root, id="orrery")
            with Vertical(id="main-stage"):
                yield LuminousDossier(id="dossier", markup=True, wrap=True)

                # The Holographic Projection (Menu)
                yield SuggestionMenu(id="suggestion-menu")

                # The Prompt
                with Horizontal(id="prompter-container"):
                    yield Label("❯", id="prompt-sigil")
                    yield GnosticPrompter(id="prompter")

        yield GnosticStatusBar(id="status-bar")
        yield Footer()

    def on_mount(self):
        """The Rite of Awakening."""
        self.action_focus_prompter()
        self._update_context_telemetry()

        # Inject history into prompter
        self.query_one(GnosticPrompter).history = self.history

        welcome = Panel(
            Text.assemble(
                ("Welcome to the ", "dim"), ("Gnostic Shell", "bold magenta"), ("\n"),
                ("Sanctum: ", "dim"), (f"{self.project_root}\n", "cyan"),
                ("Commands: ", "bold white"), ("help", "cyan"), (", ", "dim"), ("cd", "cyan"), (", ", "dim"),
                ("scaffold", "cyan")
            ),
            title="System Online", border_style="magenta"
        )
        self.query_one(LuminousDossier).proclaim(welcome)

    # --- PERSISTENCE OF MEMORY ---

    def _load_history(self) -> List[str]:
        try:
            if HISTORY_FILE.exists():
                data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
                return data[-MAX_HISTORY:]  # Keep it bounded
        except Exception:
            pass
        return []

    def _persist_history(self):
        try:
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            HISTORY_FILE.write_text(json.dumps(self.history), encoding="utf-8")
        except Exception:
            pass

    def action_quit(self):
        self._persist_history()
        self.exit()

    # --- THE OMNI-FOCUS PROTOCOL ---

    def on_key(self, event: Key):
        """Typing anywhere targets the prompter."""
        if event.is_printable and len(event.character) == 1:
            prompter = self.query_one(GnosticPrompter)
            if not prompter.has_focus: prompter.focus()

    # --- AUTOCOMPLETE LOGIC ---

    @on(GnosticPrompter.ProphecyRequest)
    def handle_prophecy_request(self, message: GnosticPrompter.ProphecyRequest):
        val = message.value
        menu = self.query_one(SuggestionMenu)
        prompter = self.query_one(GnosticPrompter)

        # 1. Update Magic Enter Hint if empty
        if not val.strip():
            magic = self._detect_magic_run()
            hint = f"Magic Enter: {magic}" if magic else "Ready."
            self.query_one(GnosticStatusBar).context_hint = hint
            menu.display = False
            prompter.is_menu_visible = False
            return

        # 2. Get Suggestions
        suggestions = self.interpreter.get_suggestions(val, self.current_cwd)

        if suggestions:
            menu.update_suggestions(suggestions)
            prompter.is_menu_visible = True
            self.query_one(
                GnosticStatusBar).context_hint = f"{len(suggestions)} prophecies found. (Tab/Enter to select)"
        else:
            menu.display = False
            prompter.is_menu_visible = False
            self.query_one(GnosticStatusBar).context_hint = "Typing..."

    @on(GnosticPrompter.MenuNavigation)
    def handle_menu_nav(self, message: GnosticPrompter.MenuNavigation):
        menu = self.query_one(SuggestionMenu)
        prompter = self.query_one(GnosticPrompter)

        if message.direction == "up":
            menu.action_cursor_up()
        elif message.direction == "down":
            menu.action_cursor_down()
        elif message.direction == "close":
            menu.display = False
            prompter.is_menu_visible = False
        elif message.direction == "select":
            # The User Chose a Prophecy
            if menu.highlighted is not None:
                # Re-fetch suggestion text (simplest robust way)
                # In a perfect world, the menu option stores the value.
                # Here we reconstruct from the interpreter based on current input state logic,
                # OR we just accept what the interpreter gave us earlier.
                # For V1, we grab the raw text from the option label.
                # NOTE: The option label is a Text object.

                # Faster/Cleaner: Re-query interpreter for the EXACT list and pick index
                suggs = self.interpreter.get_suggestions(prompter.value, self.current_cwd)
                if suggs and menu.highlighted < len(suggs):
                    selected_cmd = suggs[menu.highlighted][0]
                    prompter.value = selected_cmd
                    prompter.action_end()

            menu.display = False
            prompter.is_menu_visible = False

    # --- EXECUTION LOOP ---

    @on(GnosticPrompter.Submitted)
    async def handle_submit(self, message: GnosticPrompter.Submitted):
        # Hide menu
        self.query_one(SuggestionMenu).display = False
        self.query_one(GnosticPrompter).is_menu_visible = False

        raw_cmd = message.value.strip()
        dossier = self.query_one(LuminousDossier)

        # [FACULTY 3] The Magic Enter
        if not raw_cmd:
            magic = self._detect_magic_run()
            if magic:
                dossier.proclaim(f"[dim italic]Invoking Magic: {magic}[/dim italic]")
                raw_cmd = magic
            else:
                return  # Do nothing on empty enter if no magic available

        # Update History
        if not self.history or self.history[-1] != raw_cmd:
            self.history.append(raw_cmd)
        self.query_one(GnosticPrompter).history = self.history  # Sync widget

        # Chronicle
        dossier.proclaim_command(raw_cmd, self._get_rel_cwd())

        # Interpret
        intent = self.interpreter.divine_intent(raw_cmd, self.current_cwd)

        # Dispatch
        if intent.mode == ExecutionMode.INTERNAL:
            self._conduct_internal(intent, dossier)
        else:
            self._conduct_system(intent)

    def _detect_magic_run(self) -> Optional[str]:
        """
        [THE MAGIC RUN]
        Context-aware default action.
        """
        cwd = Path(self.current_cwd)
        if (cwd / "scaffold.scaffold").exists(): return "scaffold genesis"
        if (cwd / ".git").exists(): return "git status"
        if (cwd / "package.json").exists(): return "npm start"
        if (cwd / "Makefile").exists(): return "make"
        if (cwd / "pyproject.toml").exists(): return "poetry run python src/main.py"  # Heuristic
        if any(cwd.glob("*.py")): return "ls -la"  # Fallback
        return "ls"

    def _conduct_internal(self, intent: ShellIntent, dossier: LuminousDossier):
        if intent.verb == "cd":
            target = intent.args[0] if intent.args else "~"
            try:
                new_path = Path(os.path.expanduser(target)).resolve()
                if not new_path.exists(): raise FileNotFoundError(f"Void path: {target}")
                os.chdir(new_path)
                self.current_cwd = str(new_path)
            except Exception as e:
                dossier.proclaim_error(str(e))

        elif intent.verb == "help":
            self._proclaim_universal_codex(dossier)

        elif intent.verb == "clear":
            dossier.clear_dossier()

        elif intent.verb in ["exit", "quit"]:
            self.action_quit()

    def _proclaim_universal_codex(self, dossier: LuminousDossier):
        """Renders the Universal Codex of Rites."""
        codex = self.interpreter.get_universal_codex()
        table = Table(title="The Gnostic Codex", box=None, expand=True)
        table.add_column("Rite", style="bold cyan")
        table.add_column("Description", style="white")

        for cmd, info in codex.items():
            desc = info.get("help", "").split('\n')[0]
            table.add_row(cmd, desc)

        dossier.proclaim_artifact(table, label="Scaffold Capabilities")

    # --- WORKERS & WATCHERS ---

    @work(thread=True)
    def _conduct_system(self, intent: ShellIntent):
        dossier = self.query_one(LuminousDossier)
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["FORCE_COLOR"] = "1"  # Try to force color output from tools

        try:
            process = subprocess.Popen(
                intent.raw_command, shell=True, cwd=intent.context_cwd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
                text=True, encoding='utf-8', errors='replace', bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                if line: self.call_from_thread(dossier.proclaim_stream, line)

            if process.wait() == 0:
                self.call_from_thread(self._refresh_orrery)
            else:
                self.call_from_thread(dossier.proclaim_error, f"Rite Failed (Exit {process.returncode})")

        except Exception as e:
            self.call_from_thread(dossier.proclaim_error, f"Paradox: {e}")

    # --- ACTIONS ---

    def action_focus_prompter(self):
        self.query_one(GnosticPrompter).focus()

    def action_clear_screen(self):
        self.query_one(LuminousDossier).clear_dossier()
        self.action_focus_prompter()

    def action_toggle_orrery(self):
        orrery = self.query_one("#orrery")
        if orrery.has_class("-hidden"):
            orrery.remove_class("-hidden")
        else:
            orrery.add_class("-hidden")
        self.action_focus_prompter()

    def action_search_history(self):
        prompter = self.query_one(GnosticPrompter)

        def on_select(res):
            if res:
                prompter.value = res
                prompter.focus()

        self.push_screen(HistorySearchScreen(self.history), on_select)

    # --- TELEMETRY & SYNC ---

    def watch_current_cwd(self, new_cwd: str):
        self._update_prompt_sigil()
        self._update_context_telemetry()
        try:
            self.query_one(Orrery).update_root(Path(new_cwd))
        except:
            pass

    def _update_prompt_sigil(self):
        p = Path(self.current_cwd)
        name = p.name or str(p)
        self.query_one("#prompt-sigil", Label).update(f"[bold blue]{name} ❯[/bold blue]")

    def _get_rel_cwd(self) -> str:
        try:
            return f"~/{Path(self.current_cwd).relative_to(Path.home())}"
        except:
            return self.current_cwd

    def _refresh_orrery(self):
        try:
            self.query_one(Orrery).update_root(Path(self.current_cwd))
        except:
            pass

    @work(thread=True)
    def _update_context_telemetry(self):
        # Git Branch
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.current_cwd,
                                             stderr=subprocess.DEVNULL, text=True).strip()
            hint = f"Git: {branch}"
        except:
            hint = "Git: void"

        def _upd():
            try:
                self.query_one(GnosticStatusBar).cwd_display = f"{self._get_rel_cwd()}  |  {hint}"
            except:
                pass

        self.call_from_thread(_upd)

    @on(Orrery.DirectorySelected)
    def on_dir_sel(self, e):
        self.query_one(GnosticPrompter).value = f"cd {e.path}"
        self.query_one(GnosticPrompter).action_submit_will()