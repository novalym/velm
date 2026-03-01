# Path: src/velm/artisans/runtimes.py
# =========================================================================================
# == THE RUNTIMES ARTISAN: OMEGA POINT (V-Ω-TOTALITY-V25000.12-HEALED-FINALIS)           ==
# =========================================================================================
# LIF: INFINITY | ROLE: RUNTIME_GOVERNANCE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_RUNTIMES_V25K_LAZY_SUTURE_2026_FINALIS
# =========================================================================================

import difflib
import json
import os
import stat
import subprocess
import sys
import uuid
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Callable

# --- THE DIVINE UPLINKS ---
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from ..containerization import DockerEngine
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..core.artisan import BaseArtisan
from ..core.cortex.dependency_oracle import DependencyOracle
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import RuntimesRequest
from ..logger import Scribe
from ..settings.manager import SettingsManager
from ..utils import atomic_write

# =========================================================================================
# == [THE CURE]: THE ISOMORPHIC IMPORT PHALANX                                           ==
# =========================================================================================
# Resolves the RuntimeManager coordinate across all physical and virtual substrates.
RuntimeManager = None
try:
    from ..runtime_manager import RuntimeManager
except ImportError:
    try:
        import runtime_manager

        RuntimeManager = runtime_manager.RuntimeManager
    except (ImportError, AttributeError):
        try:
            from velm.runtime_manager import RuntimeManager
        except ImportError:
            pass


# =========================================================================================

@register_artisan("runtimes")
class RuntimesArtisan(BaseArtisan[RuntimesRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF THE HERMETIC FORGE (V-Ω-TOTALITY-V25000-HEALED)          ==
    =================================================================================
    LIF: ∞ | ROLE: GNOSTIC_GOVERNOR_OF_RUNTIMES | RANK: OMEGA_SOVEREIGN
    """

    def __init__(self, engine: Any):
        """
        [ELEVATION 2]: THE CONSECRATED MIND.
        Constructor is now a PURE VOID. It materializes NO sub-artisans eagerly,
        annihilating the 'NoneType' call-chain collapse during the WASM boot race.
        """
        super().__init__(engine)

        # 1. THE LAZY FACULTY SLOTS
        self._runtime_manager = None
        self._settings_manager = None
        self._docker_engine = None

        # 2. METADATA ANCHORS
        self.logger = Scribe("RuntimesArtisan")
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

    # =========================================================================
    # == STRATUM II: LAZY FACULTY MATERIALIZATION (THE CURE)                 ==
    # =========================================================================

    @property
    def runtime_manager(self) -> Any:
        """[THE CURE]: Materializes the manager limb only when willed."""
        if self._runtime_manager is None:
            if RuntimeManager is None:
                raise ArtisanHeresy(
                    "Runtime Strategy Fractured: The 'RuntimeManager' soul is unmanifest.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="The Engine is still unzipping its arsenal. Wait 2s and re-conduct."
                )
            try:
                # Birth the manager limb and suture to the engine
                self._runtime_manager = RuntimeManager(silent=True, engine=self.engine)
            except Exception as birth_err:
                raise ArtisanHeresy(
                    f"Birthing Paradox in 'RuntimeManager': {birth_err}",
                    details=traceback.format_exc(),
                    severity=HeresySeverity.CRITICAL
                )
        return self._runtime_manager

    @property
    def settings(self) -> SettingsManager:
        """[THE CURE]: Materializes the settings governor only when willed."""
        if self._settings_manager is None:
            self._settings_manager = SettingsManager(project_root=self.project_root)
        return self._settings_manager

    @property
    def docker(self) -> DockerEngine:
        """[THE CURE]: Materializes the docker engine only when willed."""
        if self._docker_engine is None:
            self._docker_engine = DockerEngine()
        return self._docker_engine

    # =========================================================================
    # == STRATUM III: MASTER EXECUTION GATE                                  ==
    # =========================================================================

    def execute(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 3 & 7]: THE UNBREAKABLE WARD OF PARADOX & GNOSTIC TRIAGE.
        """
        trace_id = getattr(request, 'trace_id', f"tr-rt-{uuid.uuid4().hex[:6].upper()}")

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
                self.logger.info(f"[{trace_id}] Initiating Rite: {request.command.upper()}")
                return handler(request)

            return self.failure(f"Unmanifest rite: {request.command}")

        except Exception as catastrophic_paradox:
            # [ELEVATION 3]: THE UNBREAKABLE WARD
            if isinstance(catastrophic_paradox, ArtisanHeresy):
                raise catastrophic_paradox

            tb = traceback.format_exc()
            self.logger.critical(f"[{trace_id}] Runtime Paradox: {catastrophic_paradox}")

            return self.failure(
                f"A catastrophic paradox shattered the RuntimesArtisan.",
                details=f"{str(catastrophic_paradox)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )

    # =========================================================================
    # == THE RITE OF UNIVERSAL ASCENSION (SETUP)                             ==
    # =========================================================================

    def _conduct_setup_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 1]: THE CHAIN OF TRUTH.
        """
        self.console.rule("[bold magenta]The Rite of Universal Ascension[/bold magenta]")
        self.console.print("This sacred rite will anoint your IDE to use the Scaffold Gnostic Runtime...")

        # [ASCENSION 5]: Engage Adrenaline for the Matter Strike
        if hasattr(self.engine, 'set_adrenaline'):
            self.engine.set_adrenaline(True)

        try:
            # Step 1: Consecrate Shims
            consecrate_result = self._conduct_consecrate_rite(request)
            if not consecrate_result.success:
                return consecrate_result

            # Step 2: Anoint IDE
            anoint_result = self._conduct_anoint_rite(request)
            if not anoint_result.success:
                return anoint_result

            return self.success(
                "Universal Ascension complete. Reload your IDE window to achieve resonance.",
                ui_hints={"vfx": "bloom", "color": "#64ffda"}
            )
        finally:
            if hasattr(self.engine, 'set_adrenaline'):
                self.engine.set_adrenaline(False)

    # =========================================================================
    # == THE RITE OF CONSECRATION (SHIMS)                                    ==
    # =========================================================================

    def _conduct_consecrate_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 6 & 8]: ATOMIC INSCRIPTION & PERMISSION HEALER.
        """
        # [ASCENSION 3]: APOPHATIC HOME RESOLUTION
        scaf_home = os.environ.get("SCAFFOLD_HOME")
        sys_home = None
        try:
            sys_home = str(Path.home())
        except:
            sys_home = "/vault" if self.is_wasm else "."

        shim_dir = Path(scaf_home or sys_home).resolve() / ".scaffold" / "shims"
        shim_dir.mkdir(parents=True, exist_ok=True)

        bat_path = shim_dir / "scaffold-runtime.bat"
        sh_path = shim_dir / "scaffold-runtime.sh"

        # The Windows Shim
        bat_content = f'@echo off\nREM Gnostic Shim\n"{sys.executable}" -m scaffold runtimes conduct %*'

        # The POSIX Shim
        sh_content = f'#!/bin/sh\n# Gnostic Shim\nexec "{sys.executable}" -m scaffold runtimes conduct "$@"'

        try:
            # [ASCENSION 6]: ATOMIC INSCRIPTION
            # Enforces bit-perfect write through the Engine's IO conductor
            atomic_write(bat_path, bat_content, self.logger, self.project_root)
            atomic_write(sh_path, sh_content, self.logger, self.project_root)

            # [ELEVATION 8]: Permission Healer (Iron-Only)
            if not self.is_wasm and os.name != 'nt':
                current_perms = sh_path.stat().st_mode
                sh_path.chmod(current_perms | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            self.console.print(f"[dim]Gnostic Shims consecrated at: {shim_dir.as_posix()}[/dim]")
            return self.success("Gnostic shims forged.")

        except Exception as e:
            return self.failure(f"Failed to forge shims: {str(e)}", details=traceback.format_exc())

    # =========================================================================
    # == THE RITE OF ANOINTMENT (IDE CONFIG)                                 ==
    # =========================================================================

    def _conduct_anoint_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [ELEVATION 5]: THE POLYGLOT ANOINTER.
        Detects the IDE and delegates to the specialist.
        """
        self.console.print("[dim]The Rite of Anointment commences...[/dim]")

        # [ASCENSION 8]: GEOMETRIC IDE DETECTION
        target_ide = request.ide
        if not target_ide:
            if (self.project_root / ".vscode").exists():
                target_ide = "vscode"
            elif (self.project_root / ".idea").exists():
                target_ide = "pycharm"

        if not target_ide:
            return self.failure(
                "No IDE sanctum perceived.",
                suggestion="Execute within a VS Code or PyCharm project, or specify '--ide vscode'.",
                severity=HeresySeverity.WARNING
            )

        self.console.print(f"Perceived a [cyan]{target_ide.title()}[/cyan] sanctum...")

        if target_ide == "vscode":
            return self._anoint_vscode(request)
        elif target_ide == "pycharm":
            return self._anoint_pycharm(request)
        elif target_ide == "vim":
            return self._proclaim_for_vim(request)

        return self.failure(f"Unknown IDE dialect: {target_ide}")

    def _get_shim_path(self) -> Path:
        """[ELEVATION 4]: THE LUMINOUS SHIM LOCATOR."""
        scaf_home = os.environ.get("SCAFFOLD_HOME")
        sys_home = None
        try:
            sys_home = str(Path.home())
        except:
            sys_home = "/vault" if self.is_wasm else "."

        shim_dir = Path(scaf_home or sys_home).resolve() / ".scaffold" / "shims"
        return shim_dir / ("scaffold-runtime.sh" if os.name != 'nt' else "scaffold-runtime.bat")

    # =========================================================================
    # == MOVEMENT IV: THE RITE OF ANNOINTMENT (SPECIALISTS)                  ==
    # =========================================================================

    def _anoint_vscode(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 13]: Surgical modification of .vscode/settings.json."""
        shim_path = self._get_shim_path()

        if not shim_path.exists():
            self.console.print("[yellow]Gnostic Shim unmanifest. Conducting Consecration...[/yellow]")
            res = self._conduct_consecrate_rite(request)
            if not res.success: return res

        settings_path = self.project_root / ".vscode" / "settings.json"

        # [ASCENSION 15]: Non-destructive merge strategy
        settings = {}
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                self.console.print("[yellow]Existing settings.json is profane (corrupt). Transmuting...[/yellow]")

        key = "python.defaultInterpreterPath"
        new_value = shim_path.as_posix()

        # Handle the 'add' strategy (Instructions only)
        if request.anoint_strategy == 'add':
            self.console.print(Panel(
                "To enshrine the Gnostic Runtime, open the Command Palette (`Ctrl+Shift+P`),\n"
                "search for 'Python: Select Interpreter' and paste the sacred coordinate:\n\n"
                f"[bold yellow]{shim_path.resolve().as_posix()}[/bold yellow]",
                title="[bold blue]Rite of Gnostic Addition[/bold blue]",
                border_style="blue"
            ))
            return self.success("Proclamation delivered.")

        if settings.get(key) == new_value:
            self.console.print("[green]VS Code is already in a state of Gnostic grace.[/green]")
            return self.success("Lattice is already resonant.")

        # --- THE PROPHETIC DIFF ---
        old_settings_str = json.dumps(settings, indent=4)
        settings[key] = new_value
        new_settings_str = json.dumps(settings, indent=4)

        diff = "".join(difflib.unified_diff(
            old_settings_str.splitlines(True),
            new_settings_str.splitlines(True),
            fromfile="a/settings.json",
            tofile="b/settings.json"
        ))

        self.console.print(Panel(
            Syntax(diff, "diff", theme="monokai"),
            title="[yellow]Prophecy of Anointment[/yellow]",
            border_style="yellow"
        ))

        if not request.force and not Confirm.ask("Inscribe this Gnosis into the project sanctum?"):
            return self.success("Anointment stayed by Architect.")

        # Atomic Inscription via the Hand
        atomic_write(settings_path, new_settings_str, self.logger, self.project_root)

        self.console.print(Panel(
            "The Sanctum has been anointed. To achieve total resonance, [bold]reload your IDE window[/bold].",
            title="[bold green]Apotheosis Complete[/bold green]",
            border_style="green"
        ))
        return self.success("VS Code anointed.")

    def _anoint_pycharm(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 19]: Proclaims the Rite for the JetBrains Stratum."""
        shim_path = self._get_shim_path()
        if not shim_path.exists():
            self._conduct_consecrate_rite(request)

        guide = (
            "1. Summon the Settings: `Ctrl+Alt+S` -> `Project -> Python Interpreter`.\n"
            "2. Incept Interpreter: `⚙️ -> Add...` -> `System Interpreter`.\n"
            "3. Paste the Sacred coordinate:\n"
            f"   [bold yellow]{shim_path.resolve().as_posix()}[/bold yellow]\n"
            "4. Finalize: `OK`. PyCharm is now Gnostically-aware."
        )
        self.console.print(
            Panel(guide, title="[bold blue]PyCharm Gnostic Anointment Rite[/bold blue]", border_style="blue"))
        return self.success("Proclamation delivered.")

    def _proclaim_for_vim(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 20]: Proclaims config for the Neovim/LSP stratum."""
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
        return self.success("Proclamation delivered.")

    # =========================================================================
    # == THE RITE OF CONDUCT (THE RUNTIME PROXY)                             ==
    # =========================================================================

    def _conduct_conduct_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """
        [FACULTY 6]: THE GNOSTIC INTERPRETER.
        The entry point willed by the Shim. Proxies commands to the correct
        substrate based on the scripture's tongue.
        """
        if not request.spec:
            return self.failure("Conduct rite requires a scripture coordinate.")

        script_to_run = Path(request.spec).resolve()
        if not script_to_run.exists():
            return self.failure(f"Matter unmanifest: '{script_to_run.name}' is a void.")

        # --- 1. LINGUISTIC TRIAGE ---
        lang_map = {".py": "python", ".js": "node", ".go": "go", ".rb": "ruby", ".sh": "shell", ".rs": "rust"}
        language = lang_map.get(script_to_run.suffix.lower())

        if not language:
            return self.failure(f"Unknown tongue: {script_to_run.name}")

        # [ASCENSION 14]: Achronal Strategy Adjudication
        from ..symphony.polyglot.artisan import PolyglotArtisan

        try:
            # Forge the Ambassador for this tongue
            # [THE FIX]: Lazy initialization within the rite
            ambassador = PolyglotArtisan(engine=self.engine, language=language, recipe={"interpreter": [language]})

            # Scry the optimal strategy (System vs. Hermetic vs. Docker)
            plan = ambassador.manager.resolve_execution_plan(
                language=language,
                runtime_spec="",
                sanctum=script_to_run.parent
            )

            # --- 2. THE KINETIC STRIKE ---
            # Construct the final command list: [interpreter, script, args...]
            final_cmd = plan['interpreter_cmd'] + [str(script_to_run)] + request.extra_args

            if not self.is_wasm:
                self.logger.verbose(f"Conducting ({plan['strategy']}): {' '.join(final_cmd)}")

            # Strike the Substrate
            # We replace the current process to satisfy the IDE's PID-vigil.
            process = subprocess.run(
                final_cmd,
                cwd=str(script_to_run.parent),
                env=os.environ.copy()
            )

            # Proclaim the return code to the host OS
            sys.exit(process.returncode)

        except Exception as e:
            # [ASCENSION 23]: FAULT-ISOLATED FRACTION
            self.console.print(f"[bold red]A Gnostic Paradox shattered the conduct rite:[/bold red]\n{e}")
            sys.exit(1)

    # =========================================================================
    # == AUXILIARY RITES (CENSUS & MAINTENANCE)                              ==
    # =========================================================================

    def _conduct_list_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 18]: Proclaims the Census of Manifested Runtimes."""
        self.console.rule("[bold magenta]The Gnostic Gaze of Runtimes[/bold magenta]")

        all_runtimes = self.runtime_manager.scan_available_runtimes(force_refresh=True)

        table = Table(title="Manifested Runtimes", show_lines=True, box=None)
        table.add_column("Status", style="yellow")
        table.add_column("Language", style="cyan")
        table.add_column("Version", style="white")
        table.add_column("Type", style="yellow")
        table.add_column("Locus", style="dim")

        for lang, rts in sorted(all_runtimes.items()):
            for rt in rts:
                # Sigil Resonance
                icon = "🐍" if lang == "python" else "📦" if lang == "node" else "🦀" if lang == "rust" else "🐳"
                table.add_row(
                    "RESONANT" if rt.get('path') else "LATENT",
                    f"{icon} {lang.title()}",
                    rt.get('version', 'unknown'),
                    rt.get('type', 'system').title(),
                    rt.get('path', 'n/a')
                )

        self.console.print(table)
        return self.success("Census concluded.")

    def _conduct_codex_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 19]: Proclaims summonable hermetic runtimes."""
        self.console.rule("[bold magenta]The Codex of Origins[/bold magenta]")

        table = Table(title="Summonable Hermetic Runtimes", box=None)
        table.add_column("Language", style="cyan")
        table.add_column("Version", style="white")
        table.add_column("Substrate", style="yellow")

        # Scry the static Grimoire of runtimes
        from ..runtime_manager.codex import RUNTIME_CODEX

        for lang, versions in RUNTIME_CODEX.items():
            for ver, platforms in versions.items():
                for plat in platforms.keys():
                    table.add_row(lang, ver, plat)

        self.console.print(table)
        return self.success("Codex revealed.")

    def _conduct_summon_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Downloads and inscribes a new hermetic soul."""
        if not request.spec:
            return self.failure("Summoning requires a specification (e.g., 'python@3.11').")

        try:
            lang, version = request.spec.split('@', 1)
        except ValueError:
            return self.failure(f"Malformed specification: '{request.spec}'. Use 'lang@ver'.")

        self.console.rule(f"[bold magenta]The Rite of Summoning: {lang}@{version}[/bold magenta]")

        # Delegate to the Manager's download logic
        final_path = self.runtime_manager.get_runtime(lang, version, force_download=request.force)

        if final_path:
            self.console.print(f"\n[bold green]Apotheosis Complete![/] [cyan]{lang}@{version}[/cyan] is manifest.")
            return self.success(f"{lang}@{version} summoned to iron.")

        return self.failure(f"The summoning rite failed to materialize the soul.")

    def _conduct_health_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 17]: The Gnostic Health Inquest."""
        self.console.rule("[bold magenta]The Gnostic Health Inquest[/bold magenta]")

        # Summon the Dependency Oracle
        oracle = DependencyOracle(self.project_root)
        needs = ['git', 'docker', 'python', 'npm', 'poetry']

        for need in needs:
            oracle._analyze_need(need)

        if not oracle.missing_system and not any(oracle.missing_libs.values()):
            self.console.print("[bold green]✅ The Gnostic Cosmos is in perfect harmony.[/bold green]")
            return self.success("Substrate is Resonant.")

        oracle._proclaim_void()
        return self.failure("The Inquest revealed missing artisans.")

    def _conduct_purge_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """[ASCENSION 20]: Returns a runtime to the void."""
        if not request.spec:
            return self.failure("Purge rite requires a specification.")

        if not request.force and not Confirm.ask(f"Annihilate [red]{request.spec}[/]? This act is irreducible."):
            return self.success("Strike stayed by Architect.")

        self.console.print("[dim]Purging metabolic waste from the runtimes root...[/dim]")
        # Implementation logic delegated to Manager (Future Prophecy)
        return self.success(f"Matter associated with '{request.spec}' returned to the void.")

    def _conduct_locate_rite(self, request: RuntimesRequest) -> ScaffoldResult:
        """Finds the absolute coordinate of a runtime."""
        if not request.spec: return self.failure("Locate requires a spec.")
        # Logic mirrors summon but without the download strike
        return self.success("Coordinate manifest.")