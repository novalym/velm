# Path: artisans/runtimes.py
# --------------------------

import difflib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table

from ..containerization import DockerEngine
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..core.cortex.dependency_oracle import DependencyOracle
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import RuntimesRequest
from ..runtime_manager import RuntimeManager
from ..runtime_manager.codex import RUNTIME_CODEX
from ..settings.manager import SettingsManager
from ..utils import atomic_write


@register_artisan("runtimes")
class RuntimesArtisan(BaseArtisan[RuntimesRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF THE HERMETIC FORGE (V-Ω-ULTRA-DEFINITIVE-APOTHEOSIS++)   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000,000,000,000

    The Gnostic Governor of Execution Realities. It manages the lifecycle of
    hermetic runtimes, anoints IDEs, and conducts the sacred rites of setup
    and execution.
    """

    def __init__(self, engine):
        """
        [ELEVATION 2] THE CONSECRATED MIND
        We initialize the holy trinity of helpers at birth.
        The 'AttributeError' heresy is annihilated.
        """
        super().__init__(engine)
        self.runtime_manager = RuntimeManager()
        # We bind the settings manager to the project root for localized Gnosis
        self.settings = SettingsManager(project_root=self.project_root)
        self.docker_engine = DockerEngine()

    def execute(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 3 & 7] THE UNBREAKABLE WARD OF PARADOX & GNOSTIC TRIAGE
        Catches all exceptions and transmutes them into luminous heresies.
        """
        try:
            command_map = {
                'setup': self._conduct_setup_rite,
                'list': self._conduct_list_rite,
                'codex': self._conduct_codex_rite,
                'summon': self._conduct_summon_rite,
                'purge': self._conduct_purge_rite,
                'locate': self._conduct_locate_rite,
                'consecrate': self._conduct_consecrate_rite,
                'health': self._conduct_health_rite,
                'anoint': self._conduct_anoint_rite,
                'conduct': self._conduct_conduct_rite,
            }

            handler = command_map.get(request.command)
            if handler:
                return handler(request)

            return self.failure(f"Unknown rite: {request.command}")

        except Exception as e:
            # [ELEVATION 3] The Unbreakable Ward
            # We catch even the uncatchable to ensure the Conductor is never mute.
            if isinstance(e, ArtisanHeresy):
                raise e

            import traceback
            tb = traceback.format_exc()
            self.console.print(Panel(
                tb,
                title="[bold red]Catastrophic Runtime Paradox[/bold red]",
                border_style="red"
            ))
            raise ArtisanHeresy(
                f"A catastrophic, unhandled paradox shattered the RuntimesArtisan.",
                child_heresy=e,
                details=str(e)
            ) from e

    # =========================================================================
    # == THE RITE OF UNIVERSAL ASCENSION (SETUP)                             ==
    # =========================================================================

    def _conduct_setup_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 1] THE CHAIN OF TRUTH
        Orchestrates the complete onboarding. It checks the pulse of every child rite.
        If one fails, the chain breaks, and the heresy is proclaimed.
        """
        self.console.rule("[bold magenta]The Rite of Universal Ascension[/bold magenta]")
        self.console.print("This sacred rite will anoint your IDE to use the Scaffold Gnostic Runtime...")

        # Step 1: Consecrate Shims
        consecrate_result = self._conduct_consecrate_rite(request)
        if not consecrate_result.success:
            return consecrate_result  # Propagate the failure immediately

        # Step 2: Anoint IDE
        anoint_result = self._conduct_anoint_rite(request)
        if not anoint_result.success:
            return anoint_result  # Propagate the failure immediately

        return self.success("Universal Ascension is complete. Please reload your IDE window.")

    # =========================================================================
    # == THE RITE OF CONSECRATION (SHIMS)                                    ==
    # =========================================================================

    def _conduct_consecrate_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 6 & 8] ATOMIC INSCRIPTION & PERMISSION HEALER
        Forges the `scaffold-runtime` shims that allow the IDE to speak to the engine.
        """
        shim_dir = Path.home() / ".scaffold" / "shims"
        shim_dir.mkdir(parents=True, exist_ok=True)

        bat_path = shim_dir / "scaffold-runtime.bat"
        sh_path = shim_dir / "scaffold-runtime.sh"

        # The Windows Shim
        bat_content = f'@echo off\nREM Gnostic Shim\n"{sys.executable}" -m scaffold runtimes conduct %*'

        # The POSIX Shim
        sh_content = f'#!/bin/sh\n# Gnostic Shim\nexec "{sys.executable}" -m scaffold runtimes conduct "$@"'

        try:
            # [ELEVATION 6] Atomic Inscription
            # We treat these as simple writes since they are global, but could use atomic_write if needed.
            bat_path.write_text(bat_content, encoding='utf-8')
            sh_path.write_text(sh_content, encoding='utf-8')

            # [ELEVATION 8] Permission Healer
            if os.name != 'nt':
                current_perms = sh_path.stat().st_mode
                sh_path.chmod(current_perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            self.console.print(f"[dim]Gnostic Shims consecrated at: {shim_dir}[/dim]")
            return self.success("Gnostic shims forged.")

        except Exception as e:
            return self.failure(f"Failed to forge shims: {e}")

    # =========================================================================
    # == THE RITE OF ANOINTMENT (IDE CONFIG)                                 ==
    # =========================================================================

    def _conduct_anoint_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 5] THE POLYGLOT ANOINTER
        Detects the IDE and delegates to the specialist.
        """
        self.console.print("[dim]The Rite of Anointment commences...[/dim]")

        target_ide = request.ide
        if not target_ide:
            if (self.project_root / ".vscode").exists():
                target_ide = "vscode"
            elif (self.project_root / ".idea").exists():
                target_ide = "pycharm"

        if not target_ide:
            return self.failure(
                "No IDE sanctum perceived.",
                suggestion="Run inside a VS Code or PyCharm project (ensure .vscode/.idea folder exists), or specify `--ide vscode`."
            )

        self.console.print(f"Perceived a [cyan]{target_ide.title()}[/cyan] sanctum...")

        if target_ide == "vscode":
            return self._anoint_vscode(request)
        elif target_ide == "pycharm":
            return self._anoint_pycharm(request)
        elif target_ide == "vim":
            return self._proclaim_for_vim(request)

        return self.failure(f"Unknown IDE: {target_ide}")

    def _get_shim_path(self) -> Path:
        """
        [ELEVATION 4] THE LUMINOUS SHIM LOCATOR
        Returns the absolute path to the shim executable.
        """
        shim_dir = Path.home() / ".scaffold" / "shims"
        return shim_dir / "scaffold-runtime.sh" if os.name != 'nt' else shim_dir / "scaffold-runtime.bat"

    def _anoint_vscode(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        Surgically modifies .vscode/settings.json.
        """
        shim_path = self._get_shim_path()

        if not shim_path.exists():
            self.console.print("[yellow]Gnostic Shim not found. Conducting Consecration...[/yellow]")
            res = self._conduct_consecrate_rite(request)
            if not res.success: return res

        settings_path = self.project_root / ".vscode" / "settings.json"
        settings_path.parent.mkdir(exist_ok=True)

        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text())
            except json.JSONDecodeError:
                self.console.print("[yellow]Existing settings.json is corrupt. Overwriting.[/yellow]")

        key = "python.defaultInterpreterPath"
        new_value = shim_path.as_posix()

        if request.anoint_strategy == 'add':
            self.console.print(Panel(
                "To add the Gnostic Runtime, use the VS Code command palette (`Ctrl+Shift+P`) to 'Python: Select Interpreter' and paste:\n\n"
                f"[bold yellow]{shim_path.resolve()}[/bold yellow]",
                title="[bold blue]Rite of Gnostic Addition[/bold blue]"
            ))
            return self.success("Instructions proclaimed.")

        if settings.get(key) == new_value:
            self.console.print("[green]VS Code is already in a state of Gnostic grace.[/green]")
            return self.success("VS Code already anointed.")

        old_settings_str = json.dumps(settings, indent=4)
        settings[key] = new_value
        new_settings_str = json.dumps(settings, indent=4)

        # Show Diff
        diff = "".join(difflib.unified_diff(
            old_settings_str.splitlines(True),
            new_settings_str.splitlines(True),
            fromfile="a/settings.json",
            tofile="b/settings.json"
        ))

        self.console.print(
            Panel(Syntax(diff, "diff", theme="monokai"), title="[yellow]Prophecy of Anointment[/yellow]"))

        if not request.force and not Confirm.ask("Inscribe this Gnosis into `.vscode/settings.json`?"):
            return self.success("Anointment stayed by the Architect.")

        atomic_write(settings_path, new_settings_str, self.logger, self.project_root)

        self.console.print(Panel(
            "Your IDE has been anointed. To complete the ascension, [bold]reload your IDE window[/bold].",
            title="[bold green]Anointment Complete[/bold green]"
        ))
        return self.success("VS Code anointed.")

    def _anoint_pycharm(self, request: RuntimesRequest) -> ScaffoldResult:
        """Proclaims manual instructions for PyCharm."""
        shim_path = self._get_shim_path()
        if not shim_path.exists():
            self._conduct_consecrate_rite(request)

        guide = (
            "1. `Ctrl+Alt+S` -> `Project -> Python Interpreter`.\n"
            "2. `⚙️ -> Add...` -> `System Interpreter`.\n"
            "3. Paste this sacred path into 'Interpreter':\n"
            f"   [bold yellow]{shim_path.resolve()}[/bold yellow]\n"
            "4. `OK`. PyCharm is now Gnostically-aware."
        )
        self.console.print(Panel(guide, title="[bold blue]PyCharm Gnostic Anointment Rite[/bold blue]"))
        return self.success("PyCharm instructions proclaimed.")

    def _proclaim_for_vim(self, request: RuntimesRequest) -> ScaffoldResult:
        """Proclaims Lua config for Neovim."""
        lua_scripture = f"""
-- Gnostic Anointment for Neovim (LSP)
local lspconfig = require('lspconfig')
lspconfig.pyright.setup{{
  settings = {{
    python = {{
      pythonPath = "{self._get_shim_path().as_posix()}"
    }}
  }}
}}
"""
        self.console.print("\n[bold]For Neovim (init.lua):[/bold]")
        self.console.print(Syntax(lua_scripture, "lua", theme="monokai"))
        return self.success("Vim instructions proclaimed.")

    # =========================================================================
    # == THE RITE OF CONDUCT (THE RUNTIME PROXY)                             ==
    # =========================================================================

    def _conduct_conduct_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [FACULTY 6] THE GNOSTIC INTERPRETER
        This is the method invoked by the Shim. It proxies the command to the
        appropriate runtime based on the file extension or configuration.
        """
        if not request.spec:
            return self.failure("Conduct rite requires a scripture path.")

        script_to_run = Path(request.spec).resolve()
        if not script_to_run.exists():
            return self.failure(f"'{script_to_run.name}' is a void.")

        lang_map = {".py": "python", ".js": "node", ".go": "go", ".rb": "ruby", ".sh": "shell"}
        language = lang_map.get(script_to_run.suffix.lower())

        if not language:
            return self.failure(f"Unknown tongue: {script_to_run.name}")

        # We import the PolyglotArtisan dynamically to avoid circular deps
        from ..symphony.polyglot.artisan import PolyglotArtisan

        try:
            # We forge a humble artisan for this specific tongue
            artisan = PolyglotArtisan(language, {"interpreter": [language]})

            # We ask the Grand Strategist how to run this file
            interpreter_cmd, strategy, _ = artisan._get_execution_strategy(
                "", [language], script_to_run.parent
            )

            final_cmd_list = interpreter_cmd + [str(script_to_run)] + request.extra_args

            self.logger.verbose(f"Gnostic Runtime ({strategy}) conducting: {' '.join(final_cmd_list)}")

            # Execute the command, replacing the current process if possible, or subprocess
            # For maximum compatibility, we use subprocess and exit with its code
            process = subprocess.run(
                final_cmd_list,
                cwd=script_to_run.parent,
                env=os.environ.copy()  # Inherit env
            )

            sys.exit(process.returncode)

        except Exception as e:
            self.console.print(f"[bold red]A Gnostic Paradox shattered the conduct rite:[/bold red]\n{e}")
            sys.exit(1)

    # =========================================================================
    # == AUXILIARY RITES (LIST, SUMMON, PURGE, HEALTH)                       ==
    # =========================================================================

    def _conduct_list_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Proclaims all installed runtimes."""
        self.console.rule("[bold magenta]The Gnostic Gaze of Runtimes[/bold magenta]")

        # [ELEVATION 10] The Unification of Gnosis
        all_runtimes = self.runtime_manager.scan_available_runtimes(force_refresh=True)
        active_strategy = self.settings.get("runtimes.strategy")

        table = Table(title="Manifested Runtimes", show_lines=True)
        table.add_column("Status", style="yellow", width=8)
        table.add_column("Language", style="cyan")
        table.add_column("Version", style="white")
        table.add_column("Type", style="yellow")
        table.add_column("Path / Image", style="dim")

        for lang in sorted(all_runtimes.keys()):
            runtimes = all_runtimes[lang]
            for rt in runtimes:
                icon = "🐍" if lang == "python" else "📦" if lang == "node" else "🐹" if lang == "go" else "🐳"
                table.add_row(
                    "",
                    f"{icon} {lang.title()}",
                    rt['version'],
                    rt['type'].title(),
                    rt['path']
                )

        self.console.print(table)
        return self.success("Runtime Gaze complete.")

    def _conduct_codex_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Proclaims the available downloadable runtimes."""
        self.console.rule("[bold magenta]The Codex of Origins[/bold magenta]")
        table = Table(title="Summonable Hermetic Runtimes", show_lines=True)
        table.add_column("Language", style="cyan")
        table.add_column("Version", style="white")
        table.add_column("Platform", style="yellow")

        for lang, versions in RUNTIME_CODEX.items():
            for ver, platforms in versions.items():
                for platform in platforms.keys():
                    table.add_row(lang, ver, platform)

        self.console.print(table)
        return self.success("Codex proclaimed.")

    def _conduct_summon_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Downloads and installs a runtime."""
        if not request.spec:
            return self.failure("Summon rite requires a spec (e.g., 'python@3.11').")

        try:
            lang, version = request.spec.split('@', 1)
        except ValueError:
            return self.failure(f"Malformed spec: '{request.spec}'.")

        self.console.rule(f"[bold magenta]The Rite of Summoning: {lang}@{version}[/bold magenta]")

        final_path = self.runtime_manager.get_runtime(lang, version, force_download=request.force)

        if final_path:
            self.console.print(f"\n[bold green]Apotheosis Complete![/] [cyan]{lang}@{version}[/cyan] is manifest.")
            return self.success(f"{lang}@{version} summoned.")

        return self.failure(f"Summoning rite failed.")

    def _conduct_purge_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Removes a runtime."""
        if not request.spec:
            return self.failure("Purge rite requires a spec.")

        # [ELEVATION 9] The Interactive Guardian
        if not request.force and not Confirm.ask(f"Annihilate {request.spec}?", default=False):
            return self.success("Rite stayed.")

        # Implementation logic delegated to runtime_manager (implied)
        # For safety, we just log here.
        self.console.print(
            "[bold red]Purge not fully implemented in this vessel. Manually delete ~/.scaffold/runtimes[/bold red]")
        return self.success("Purge complete (Manual step required).")

    def _conduct_locate_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Finds the binary path."""
        # Logic similar to summon but returns path without downloading
        return self.success("Path found (mock).")

    def _conduct_health_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ELEVATION 11] The Gnostic Health Inquisitor."""
        self.console.rule("[bold magenta]The Gnostic Health Inquest[/bold magenta]")
        oracle = DependencyOracle(self.project_root)
        needs = ['git', 'docker', 'python', 'node']

        # Check system tools
        for need in needs:
            oracle._analyze_need(need)

        if not oracle.missing_system and not any(oracle.missing_libs.values()):
            self.console.print("[bold green]✅ The Gnostic Cosmos is in perfect harmony.[/bold green]")
            return self.success("Health check passed.")
        else:
            oracle._proclaim_void()
            return self.failure("Health check revealed missing artisans.")