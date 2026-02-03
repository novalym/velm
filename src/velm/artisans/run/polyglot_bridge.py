# Path: artisans/run/polyglot_bridge.py
# -------------------------------------
import json
import os
import time
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.text import Text

from ...contracts.data_contracts import ExecutionPlan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.symphony_contracts import Edict, EdictType, Reality
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import RunRequest
from ...logger import Scribe
from ...symphony.polyglot.artisan import PolyglotArtisan
from ...symphony.polyglot.grimoire import POLYGLOT_GRIMOIRE


class PolyglotBridge:
    """
    =================================================================================
    == THE GNOSTIC AMBASSADOR (V-Ω-ETERNAL-ELEVATED. THE INTELLIGENT BRIDGE)       ==
    =================================================================================
    LIF: 100,000,000,000,000

    The Diplomat between the Scaffold God-Engine and the Foreign Tongues.
    It translates a high-level RunRequest into a concrete, environmentally-enriched,
    and output-aware Polyglot Edict.
    """

    def __init__(self, engine: Any, logger: Scribe):
        self.engine = engine
        self.logger = logger
        self.console = Console()

    def delegate(self, language: str, scripture_path: Path, parent_request: RunRequest,
                 execution_plan: ExecutionPlan) -> ScaffoldResult:
        """
        [THE ULTRA-DEFINITIVE DELEGATION]
        Conducts the foreign rite by summoning the one true Polyglot Conductor.
        """
        self.logger.verbose(f"Polyglot Bridge awakened for a '{language}' rite.")

        # [FACULTY 8] The Recipe Guardian
        recipe = POLYGLOT_GRIMOIRE.get(language)
        if not recipe:
            raise ArtisanHeresy(
                f"No Gnostic recipe found for the '{language}' tongue.",
                suggestion=f"Supported tongues: {', '.join(POLYGLOT_GRIMOIRE.keys())}"
            )

        exec_style = recipe.get("execution_style", "temp_file")

        # [FACULTY 6] The Path Anchor
        # We resolve the path to absolute truth to prevent drift.
        abs_scripture_path = scripture_path.resolve()
        edict_command = str(abs_scripture_path)

        # [FACULTY 1] The Debug Injection
        is_debug = getattr(parent_request, 'debug', False)

        raw_scripture = f"{language}: >> {scripture_path.name}"
        script_block = ""
        mode_label = "FILE"

        # [FACULTY 9] The Mode Sentinel & [FACULTY 11] Interactive TTY Guard
        # Handle Ephemeral Content (Pipes/Eval) vs File
        if parent_request.eval_content:
            mode_label = "EVAL"
            script_block = parent_request.eval_content
            raw_scripture = f"{language}(eval): >> [Inline Gnosis]"

        elif parent_request.pipe_content:
            mode_label = "PIPE"
            script_block = parent_request.pipe_content
            raw_scripture = f"{language}(pipe): >> [Stream Gnosis]"
            # If pipe content is empty but we expected it, warn?
            # BaseRequest validator handles reading stdin, so we trust it.

        # Handle File Content (Only if needed for temp_file/stdin execution)
        elif exec_style in ["temp_file", "stdin_pipe"]:
            if abs_scripture_path.is_file():
                try:
                    script_block = abs_scripture_path.read_text(encoding='utf-8')
                except Exception:
                    self.logger.warn(
                        f"Could not read soul of '{abs_scripture_path.name}'. Assuming binary or direct execution.")
                    script_block = ""

        # Forge the Edict Vessel
        edict = Edict(
            type=EdictType.POLYGLOT_ACTION,
            raw_scripture=raw_scripture,
            line_num=0,
            language=language,
            command=edict_command,
            script_block=script_block
        )

        # --- MOVEMENT II: FORGING THE GNOSTIC CONTEXT ---
        context = os.environ.copy()

        # Inject Architect's Variables
        for key, value in parent_request.variables.items():
            context[f"SC_VAR_{key.upper()}"] = str(value)

        # [FACULTY 1 & 5] The Debug Beacon
        if is_debug:
            context["SCAFFOLD_DEBUG_MODE"] = "true"
            context["DEBUG"] = "1"  # Standard convention
            self.logger.info("Gnostic Debug Beacon lit.")

        # [FACULTY 1] The Gnostic Context Injector
        context["SC_PROJECT_ROOT"] = str(parent_request.project_root or Path.cwd())
        context["SC_TIMESTAMP"] = str(int(time.time()))
        context["SC_RITE_MODE"] = mode_label
        context["SC_SCRIPT_PATH"] = str(abs_scripture_path)

        # [FACULTY 2] The Virtual Environment Sentinel
        # Automatically detect and activate venv if present in project root
        project_root = parent_request.project_root or Path.cwd()
        venv_path = None
        for venv_name in [".venv", "venv", "env"]:
            candidate = project_root / venv_name
            if candidate.is_dir():
                venv_path = candidate
                break

        if venv_path:
            bin_dir = venv_path / ("Scripts" if os.name == 'nt' else "bin")
            if bin_dir.exists():
                self.logger.verbose(f"Virtual Environment Sentinel detected '{venv_name}'. Injecting into PATH.")
                current_path = context.get("PATH", "")
                context["PATH"] = str(bin_dir.resolve()) + os.pathsep + current_path

        try:
            # [FACULTY 10] The Luminous Prologue
            if not parent_request.silent:
                self.console.print(f"[dim]Conducting {language.upper()} rite ({mode_label})...[/dim]")

            # --- MOVEMENT III: THE SACRED COMMUNION ---
            artisan = PolyglotArtisan(language, recipe)

            # The PolyglotArtisan is now directly commanded with the execution plan.
            reality = artisan.conduct_with_plan(
                script_code=script_block,
                context=context,
                sanctum=abs_scripture_path.parent,
                edict=edict,
                execution_plan=execution_plan
            )

            # --- MOVEMENT IV: THE FINAL ADJUDICATION & PROCLAMATION ---
            self._proclaim_result(reality, language)

            if reality.returncode == 0:
                return self.engine.success(f"The foreign rite of '{language}' was conducted successfully.")
            else:
                return self.engine.failure(
                    f"The foreign rite of '{language}' was tainted by a heresy (Exit Code: {reality.returncode}).")

        except Exception as e:
            # [FACULTY 12] The Unbreakable Ward of Delegation
            raise ArtisanHeresy("A catastrophic paradox occurred in the Polyglot Bridge.", child_heresy=e) from e

    def _proclaim_result(self, reality: Reality, language: str):
        """
        [THE LUMINOUS HERALD - SILENCED ECHO]
        Intelligently renders the output of the rite.
        Now honors the Vow of Silence for successful, plain-text rites that were already streamed.
        """
        output = reality.output.strip()

        if not output:
            return

        # [FACULTY 3] The JSON Diviner
        # If the output is JSON, we ALWAYS print it again because the stream
        # printed raw lines, but we want to show the beautified structure.
        try:
            if (output.startswith('{') and output.endswith('}')) or \
                    (output.startswith('[') and output.endswith(']')):
                json_obj = json.loads(output)
                self.console.print(Panel(
                    JSON.from_data(json_obj),
                    title=f"[bold green]{language.upper()} Gnosis (JSON)[/bold green]",
                    border_style="green"
                ))
                return
        except (json.JSONDecodeError, Exception):
            pass

        # [FACULTY 4] The Error Analyst
        # If the rite failed, we print the output in a Red Panel to ensure the
        # Architect sees the cause of death clearly.
        if reality.returncode != 0:
            self.console.print(Panel(
                Text(output, style="red"),
                title=f"[bold red]Heresy in {language.upper()} Rite (Exit {reality.returncode})[/bold red]",
                border_style="red"
            ))
            return

        # [THE FIX] The Silenced Echo
        # If we are here, the rite was successful (Exit 0) and the output was text.
        # Since the PolyglotArtisan already streamed this to the console via Logger,
        # repeating it here is profane. We do nothing.
        pass