# Path: scaffold/settings/tui.py

"""
=================================================================================
== THE ALTAR OF CONFIGURATION (V-Ω-SINGULARITY. THE COCKPIT OF WILL)           ==
=================================================================================
LIF: 10,000,000,000,000

This is the interactive sanctuary where the Architect tunes the soul of the
machine. It features Omniscient Search, Live Diffs, and the Rite of Ejection.
"""
import json
import time
from typing import Any, List

from rich.box import ROUNDED
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.text import Text

from .manager import SettingsManager
from .schema import DEFAULT_SETTINGS_SCHEMA, SettingDef, get_schema_map
from ..runtime_manager import RuntimeManager

# --- THE ICONS OF POWER ---
ICONS = {
    "Core": "🦁", "Runtimes": "⚡", "Docker": "🐳", "Hermetic": "📦",
    "Analysis": "🔮", "AI": "🧠", "Forge": "⚒️", "Network": "🌐",
    "Telemetry": "📡", "Profiles": "🎭"
}

# --- GNOSTIC PROFILES ---
PROFILES = {
    "default": {
        "desc": "The Balanced Path. Auto runtimes, standard linting.",
        "settings": {"runtimes.strategy": "auto", "analysis.level": "standard"}
    },
    "celestial": {
        "desc": "The Docker Absolutist. Everything runs in containers.",
        "settings": {"runtimes.strategy": "docker", "docker.pull_policy": "missing"}
    },
    "hermetic": {
        "desc": "The Reproducible Purist. No system tools, only managed binaries.",
        "settings": {"runtimes.strategy": "hermetic", "analysis.strict_mode": True}
    },
    "speed": {
        "desc": "The Sprinter. System runtimes, lenient checks. Fast & dangerous.",
        "settings": {"runtimes.strategy": "system", "analysis.level": "lenient"}
    }
}


class SettingsAltar:
    """
    The High Priest of Configuration.
    """

    def __init__(self, manager: SettingsManager):
        self.manager = manager
        self.console = Console()
        self.runtime_manager = RuntimeManager()
        self.schema_map = get_schema_map()
        self.active_profile = "Custom"
        self.message_log: List[str] = []

    def open(self):
        """The Rite of Entrance. Starts the main event loop."""
        while True:
            self.console.clear()
            self._render_dashboard()

            # The Luminous Prompt
            prompt_text = Text.assemble(
                ("[bold]Command[/bold]", "cyan"),
                (" (", "dim"),
                ("1-8", "white"), (", ", "dim"),
                ("/", "bold yellow"), (" search, ", "dim"),
                (":", "bold green"), (" edict, ", "dim"),
                ("p", "bold magenta"), ("rofiles, ", "dim"),
                ("e", "bold blue"), ("ject, ", "dim"),
                ("q", "white"), ("uit", "dim"),
                (")", "dim")
            )

            choice = Prompt.ask(prompt_text, default="q").strip()

            if choice == "q":
                self.console.print("[dim]The Altar closes. The Gnosis is preserved.[/dim]")
                break

            # Global Hotkeys
            if choice == "/":
                self._omniscient_search()
            elif choice.startswith(":"):
                self._direct_edict(choice[1:])
            elif choice == "p":
                self._manage_profiles()
            elif choice == "e":
                self._rite_of_ejection()

            # Navigation
            elif choice == "1":
                self._manage_category("Core")
            elif choice == "2":
                self._manage_runtimes_hub()
            elif choice == "3":
                self._manage_category("Docker")
            elif choice == "4":
                self._manage_category("Hermetic")
            elif choice == "5":
                self._manage_category("Analysis")
            elif choice == "6":
                self._manage_ai_nexus()
            elif choice == "7":
                self._manage_category("Forge")
            elif choice == "8":
                self._manage_category("Network")
            else:
                self._flash_message(f"[red]Unknown Command: {choice}[/red]")

    def _render_dashboard(self):
        """Renders the main HUD with Telemetry."""
        # 1. Header & Telemetry
        active_strategy = self.manager.get("runtimes.strategy")
        strategy_color = "green" if active_strategy == "docker" else "yellow" if active_strategy == "hermetic" else "white"
        docker_avail = self.manager.docker_engine.is_available
        docker_status = "[bold green]Online[/bold green]" if docker_avail else "[bold red]Dormant[/bold red]"
        project_name = self.manager.project_config_path.parent.parent.name if self.manager.project_config_path else "Global Scope"

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)

        grid.add_row(
            f"📍 Scope: [bold cyan]{project_name}[/]",
            f"⚡ Strategy: [{strategy_color}]{active_strategy.upper()}[/]",
            f"🐳 Docker: {docker_status}"
        )

        self.console.print(Panel(
            grid,
            title="[bold magenta]SCAFFOLD COMMAND ALTAR[/bold magenta]",
            border_style="magenta",
            subtitle="[dim]v0.1.0 • Gnostic Engine Online[/dim]"
        ))

        # 2. The Menu Grid
        menu = Table(box=ROUNDED, show_header=False, expand=True, border_style="dim", padding=(0, 2))
        menu.add_column("Key", style="bold cyan", width=3, justify="right")
        menu.add_column("Category", style="bold white")
        menu.add_column("Description", style="dim")

        rows = [
            ("1", "Core", "Identity, Editor, Shell"),
            ("2", "Runtimes", "Execution Strategy & Binaries"),
            ("3", "Docker", "Celestial Vessel Config"),
            ("4", "Hermetic", "Managed Versions (Py/Node/Go)"),
            ("5", "Analysis", "The Gnostic Inquisitor"),
            ("6", "AI Nexus", "OpenAI, Anthropic, Local AI"),
            ("7", "Forge", "Template Sources & Gists"),
            ("8", "Network", "Timeouts & Proxies")
        ]

        for key, cat, desc in rows:
            icon = ICONS.get(cat.split()[0], "🔧")
            menu.add_row(f"[{key}]", f"{icon} {cat}", desc)

        self.console.print(menu)

        # 3. The Luminous Message Log
        if self.message_log:
            self.console.print(Padding(Text(self.message_log[-1]), (1, 0)))
            # Clear log after rendering one frame? Or keep history?
            # For TUI feel, we keep only the last message.
            # self.message_log.clear()

    # =========================================================================
    # == 1. OMNISCIENT SEARCH (THE GNOSTIC QUERY)                            ==
    # =========================================================================
    def _omniscient_search(self):
        """Allows the Architect to search across all settings."""
        search_term = Prompt.ask("[bold yellow]Gnostic Query[/bold yellow] (search settings)").lower()
        if not search_term: return

        hits = []
        for s in DEFAULT_SETTINGS_SCHEMA:
            if search_term in s.key.lower() or search_term in s.description.lower():
                hits.append(s)

        if not hits:
            self._flash_message(f"[red]No Gnosis found matching '{search_term}'[/red]")
            return

        self._present_search_results(hits)

    def _present_search_results(self, hits: List[SettingDef]):
        """Interactive list of search results."""
        while True:
            self.console.clear()
            self.console.rule(f"[bold yellow]Search Results ({len(hits)})[/bold yellow]")

            table = Table(box=ROUNDED, show_lines=True, expand=True)
            table.add_column("#", style="yellow", width=4)
            table.add_column("Key", style="bold white")
            table.add_column("Value", style="green")
            table.add_column("Description", style="dim")

            for i, s in enumerate(hits):
                val = self.manager.get(s.key)
                display_val = "********" if s.secret and val else str(val)
                table.add_row(str(i + 1), s.key, display_val, s.description)

            self.console.print(table)
            choice = Prompt.ask("\n[bold]Edit #[/bold] (or 'b'ack)", default="b")

            if choice == 'b': return
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(hits):
                    self._edit_setting(hits[idx])
            except ValueError:
                pass

    # =========================================================================
    # == 2. THE RITE OF EJECTION (BOOTSTRAP)                                 ==
    # =========================================================================
    def _rite_of_ejection(self):
        """Dumps current config to local file."""
        if Confirm.ask(
                "[bold red]Perform the Rite of Ejection?[/bold red]\nThis will create/overwrite `.scaffold/config.json` with current defaults.",
                default=False):
            self.manager.bootstrap_project_config()
            self._flash_message("[bold green]Configuration Ejected to Project Sanctum.[/bold green]")
            time.sleep(1.5)

    # =========================================================================
    # == 3. DIRECT EDICT (VIM MODE)                                          ==
    # =========================================================================
    def _direct_edict(self, command: str):
        """Parses :key value."""
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            self._flash_message("[red]Malformed Edict. Use :key value[/red]")
            return

        key, val = parts
        # Find the schema definition
        setting = self.schema_map.get(key)
        if not setting:
            self._flash_message(f"[red]Unknown Key: {key}[/red]")
            return

        # Auto-detect type
        final_val = val
        if setting.value_type == "bool":
            final_val = val.lower() in ('true', '1', 'yes', 'y')
        elif setting.value_type == "int":
            try:
                final_val = int(val)
            except:
                pass

        try:
            # Default to global for speed, or project if exists
            if self.manager.project_config_path:
                self.manager.set_project(key, final_val)
                scope = "Project"
            else:
                self.manager.set_global(key, final_val)
                scope = "Global"
            self._flash_message(f"[green]Edict Enacted:[/green] {key} = {final_val} ({scope})")
            time.sleep(0.5)
        except Exception as e:
            self._flash_message(f"[red]Heresy:[/red] {e}")

    # =========================================================================
    # == UTILITIES                                                           ==
    # =========================================================================
    def _flash_message(self, msg: str):
        self.message_log.append(msg)

    def _manage_category(self, category: str):
        # ... (Standard category management, updated to use _edit_setting) ...
        # Reusing logic from previous iteration but ensuring it calls the enhanced edit
        while True:
            self.console.clear()
            icon = ICONS.get(category, "🔧")
            self.console.rule(f"[bold {self._get_cat_color(category)}]{icon} {category} Settings[/]")

            settings = [s for s in DEFAULT_SETTINGS_SCHEMA if s.category == category]

            table = Table(box=ROUNDED, show_lines=True, expand=True)
            table.add_column("#", style="yellow", width=4, justify="right")
            table.add_column("Key", style="bold white")
            table.add_column("Value", style="green")
            table.add_column("Source", style="dim", width=10)

            for i, s in enumerate(settings):
                val = self.manager.get(s.key)
                source_label, source_style = self._determine_source_style(s.key, val)

                display_val = "********" if s.secret and val else str(val)
                if len(display_val) > 40: display_val = display_val[:37] + "..."

                table.add_row(str(i + 1), s.key, display_val, f"[{source_style}]{source_label}[/]")

            self.console.print(table)
            choice = Prompt.ask("\n[bold]Edit #[/bold] (or 'b'ack)", default="b").lower()

            if choice == 'b': return
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(settings):
                    self._edit_setting(settings[idx])
            except ValueError:
                pass

    def _edit_setting(self, setting: SettingDef):
        """
        [THE RITE OF TRANSFIGURATION (ENHANCED)]
        Now with Live Diff and Reset capabilities.
        """
        while True:
            self.console.clear()
            self.console.rule(f"[bold yellow]Transfiguring: {setting.key}[/bold yellow]")

            current_val = self.manager.get(setting.key)
            source_label, source_style = self._determine_source_style(setting.key, current_val)

            # Context Panel
            self.console.print(Panel(
                Text.assemble(
                    (f"{setting.description}\n\n", "italic white"),
                    ("Current Soul: ", "dim"), (f"{current_val}", "green"),
                    (f" ({source_label})", source_style),
                    ("\nDefault Soul: ", "dim"), (f"{setting.default}", "dim white")
                ),
                title="Gnostic Context", border_style="cyan"
            ))

            self.console.print("[dim]Actions: (e)dit, (r)eset to default, (b)ack[/dim]")
            action = Prompt.ask("Action", choices=['e', 'r', 'b'], default='e')

            if action == 'b': return

            new_val = None
            if action == 'r':
                new_val = setting.default
            else:
                # Input Acquisition
                if setting.value_type == "bool":
                    new_val = Confirm.ask("Enable?", default=bool(current_val))
                elif setting.options:
                    self.console.print(f"Options: [cyan]{', '.join(str(o) for o in setting.options)}[/cyan]")
                    new_val = Prompt.ask("Value", choices=[str(o) for o in setting.options], default=str(current_val))
                elif setting.value_type == "int":
                    new_val = IntPrompt.ask("Value", default=int(current_val) if current_val else 0)
                else:
                    new_val = Prompt.ask("Value", default=str(current_val))

            # The Crystal Ball (Diff View)
            if str(new_val) != str(current_val):
                self.console.print(Panel(
                    Text.assemble(
                        ("Old: ", "red"), (str(current_val), "red strike"),
                        ("\nNew: ", "green"), (str(new_val), "bold green")
                    ),
                    title="Prophecy of Change", border_style="yellow"
                ))
                if not Confirm.ask("Confirm Transfiguration?", default=True):
                    continue

            # Scope Selection
            can_set_project = bool(self.manager.project_config_path)
            scope = "global"
            if can_set_project:
                scope = Prompt.ask("Scope?", choices=["project", "global"], default="project")

            # Inscription
            try:
                if scope == "project":
                    self.manager.set_project(setting.key, new_val)
                else:
                    self.manager.set_global(setting.key, new_val)
                self._flash_message(f"[green]Updated {setting.key} -> {new_val}[/green]")
                return
            except Exception as e:
                self._flash_message(f"[red]Heresy: {e}[/red]")
                return

    def _determine_source_style(self, key: str, value: Any) -> tuple[str, str]:
        """
        [THE GAZE OF TRUTH]
        Determines where a setting comes from to color-code it.
        Returns: (Source Label, Rich Style)
        """
        # Gaze 1: The Project Sanctum
        if self.manager.project_config_path and self.manager.project_config_path.exists():
            try:
                proj_data = json.loads(self.manager.project_config_path.read_text())
                if key in proj_data:
                    return "Project", "bold gold3"
            except:
                pass

        # Gaze 2: The Global Canon
        if self.manager.global_config_path.exists():
            try:
                glob_data = json.loads(self.manager.global_config_path.read_text())
                if key in glob_data:
                    return "Global", "cyan"
            except:
                pass

        # Gaze 3: The Primal Void
        return "Default", "dim white"

    def _manage_profiles(self):
        """
        [THE MASK OF THE GODS]
        Allows the Architect to instantly apply presets (Local vs Celestial vs Hermetic).
        """
        while True:
            self.console.clear()
            self.console.rule("[bold yellow]Architectural Profiles[/bold yellow]")
            self.console.print("[dim]Select a profile to instantly transfigure multiple settings.[/dim]\n")

            table = Table(box=ROUNDED, show_lines=True, expand=True)
            table.add_column("Profile", style="bold cyan")
            table.add_column("Description", style="white")
            table.add_column("Key Changes", style="dim")

            for key, data in PROFILES.items():
                changes = ", ".join([f"{k}={v}" for k, v in data['settings'].items()])
                table.add_row(key.title(), data['desc'], changes)

            self.console.print(table)

            choice = Prompt.ask("\n[bold]Apply Profile[/bold] (name or 'b'ack)", default="b").lower()
            if choice == 'b': return

            if choice in PROFILES:
                if Confirm.ask(f"[bold]Activate '{choice.title()}' profile?[/bold] This will overwrite settings.",
                               default=True):
                    # Apply Settings
                    for k, v in PROFILES[choice]['settings'].items():
                        # Default to global unless project active
                        if self.manager.project_config_path:
                            self.manager.set_project(k, v)
                        else:
                            self.manager.set_global(k, v)

                    self.console.print(f"\n[bold green]Profile '{choice.title()}' Activated.[/bold green]")
                    import time;
                    time.sleep(1)
                    return
            else:
                self._flash_message(f"[red]Unknown Profile: {choice}[/red]")

    def _manage_ai_nexus(self):
        """
        [THE CEREBRO CONNECTION]
        Configures LLM backends, including Local AI (LM Studio/Ollama) and Cloud Gods.
        """
        while True:
            self.console.clear()
            self.console.rule("[bold purple]The AI Nexus[/bold purple]")

            current_model = self.manager.get("ai.model")
            current_base = self.manager.get("ai.api_base")
            has_key = bool(self.manager.get("ai.api_key"))

            # Status Panel
            status_color = "green" if (has_key or "localhost" in str(current_base)) else "yellow"
            self.console.print(Panel(
                Text.assemble(
                    ("Active Mind: ", "dim"), (f"{current_model}\n", "bold white"),
                    ("Connection:  ", "dim"), (f"{current_base}\n", "cyan"),
                    ("Credentials: ", "dim"), ("Set" if has_key else "Unset (Required for Cloud)", status_color)
                ),
                title="[bold purple]Cerebro Status[/bold purple]",
                border_style="purple"
            ))

            self.console.print("\n[bold]Quick Configs:[/bold]")
            self.console.print("  [1] [green]Local AI[/green] (LM Studio / Ollama - localhost:1234)")
            self.console.print("  [2] [cyan]OpenAI[/cyan] (GPT-4o)")
            self.console.print("  [3] [yellow]Anthropic[/yellow] (Claude 3.5 Sonnet)")
            self.console.print("  [4] [blue]Manual Configuration[/blue] (Advanced)")

            choice = Prompt.ask("\n[bold]Select[/bold] (b to back)", default="b")

            if choice == 'b': return

            if choice == '1':  # Local
                self.manager.set_global("ai.api_base", "http://localhost:1234/v1")
                self.manager.set_global("ai.model", "local-model")  # User usually loads model in UI
                self.manager.set_global("ai.api_key", "lm-studio")  # Dummy key usually required
                self.console.print("[green]Configured for Local AI. Ensure LM Studio server is running.[/green]")

            elif choice == '2':  # OpenAI
                self.manager.set_global("ai.api_base", "https://api.openai.com/v1")
                self.manager.set_global("ai.model", "gpt-4o")
                key = Prompt.ask("Enter OpenAI API Key", password=True)
                if key: self.manager.set_global("ai.api_key", key)

            elif choice == '3':  # Anthropic
                self.console.print("[dim]Note: Direct Anthropic support requires the 'anthropic' library update.[/dim]")
                # For now, we assume a proxy or standard setup

            elif choice == '4':
                self._manage_category("AI")  # Fallback to standard list editor
                return

            if choice in ['1', '2', '3']:
                import time;
                time.sleep(1)

    def _manage_runtimes_hub(self):
        """
        [THE CROSSROADS OF EXECUTION]
        A split view: Manage Strategy OR Manage Binaries.
        """
        while True:
            self.console.clear()
            self.console.rule("[bold green]The Runtime Cosmos[/bold green]")

            strategy = self.manager.get("runtimes.strategy")

            self.console.print(f"Current Strategy: [bold green]{strategy.upper()}[/bold green]")
            self.console.print("[dim]How Scaffold executes your polyglot code.[/dim]\n")

            self.console.print("  [1] Change Strategy (System / Hermetic / Docker)")
            self.console.print("  [2] Manage Hermetic Binaries (Download/Install)")
            self.console.print("  [3] View Detailed Settings")

            choice = Prompt.ask("\n[bold]Select[/bold] (b to back)", default="b")

            if choice == 'b': return
            if choice == '1':
                # Quick Toggle
                new_strat = Prompt.ask("Strategy", choices=["auto", "system", "hermetic", "docker"], default=strategy)
                self.manager.set_global("runtimes.strategy", new_strat)
            if choice == '2':
                self._manage_installed_runtimes()
            if choice == '3':
                self._manage_category("Runtimes")

    def _manage_installed_runtimes(self):
        """
        [THE HALL OF SOULS]
        Visualizes installed runtimes and allows summoning new ones via the RuntimeManager.
        """
        while True:
            self.console.clear()
            self.console.rule("[bold green]The Cosmos of Runtimes[/bold green]")

            runtimes = self.manager.scan_available_runtimes(force_refresh=True)

            grid = Table.grid(padding=(0, 2), expand=True)
            grid.add_column(style="bold white", width=10)
            grid.add_column(style="dim")

            for lang in ["python", "node", "go", "docker"]:
                icon = "🐍" if lang == "python" else "📦" if lang == "node" else "🐹" if lang == "go" else "🐳"

                # Special handling for Docker presence
                if lang == "docker":
                    available = [
                        {"version": "Active", "type": "system"}] if self.manager.docker_engine.is_available else []
                else:
                    available = runtimes.get(lang, [])

                if not available:
                    grid.add_row(f"{icon} {lang.title()}", "[red]Not Manifest[/red]")
                else:
                    versions = []
                    for r in available:
                        style = "green" if r['type'] == 'managed' else "blue"
                        tag = "[Managed]" if r['type'] == 'managed' else "[System]"
                        versions.append(f"[{style}]{r['version']} {tag}[/{style}]")
                    grid.add_row(f"{icon} {lang.title()}", ", ".join(versions))

            self.console.print(Panel(grid, title="Manifested Souls", border_style="green"))

            self.console.print("\n[dim]Commands: (i)nstall <lang> <ver>, (b)ack[/dim]")
            cmd = Prompt.ask("Edict").strip()

            if cmd == 'b': return

            parts = cmd.split()
            if len(parts) >= 3 and parts[0] == 'i':
                lang, ver = parts[1], parts[2]
                try:
                    with self.console.status(f"[bold cyan]Summoning {lang}@{ver}...[/bold cyan]"):
                        path = self.runtime_manager.get_runtime(lang, ver)
                    if path:
                        self.console.print(f"[bold green]Success! Summoned to {path}[/bold green]")
                        import time;
                        time.sleep(1.5)
                except Exception as e:
                    self.console.print(f"[bold red]Summoning Failed:[/bold red] {e}")
                    Prompt.ask("Press Enter")

    def _get_cat_color(self, cat: str) -> str:
        colors = {
            "Core": "cyan", "Runtimes": "green", "Docker": "blue",
            "Hermetic": "magenta", "Analysis": "yellow", "AI": "purple",
            "Forge": "red", "Network": "white"
        }
        return colors.get(cat, "white")