# Path: src/velm/artisans/run/polyglot_bridge.py
# =========================================================================================
# == THE OMEGA AMBASSADOR: TOTALITY (V-Ω-TOTALITY-V25000.99-CONCRETE-FIXED)             ==
# =========================================================================================
# LIF: ∞ | ROLE: KINETIC_TRANSMUTATION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BRIDGE_V25K_99_CONSTRUCTOR_SUTURE_2026_FINALIS
# =========================================================================================

import json
import os
import sys
import time
import uuid
import platform
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, Union, Tuple

# --- THE LUMINOUS UI ---
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.text import Text

# --- CORE SCAFFOLD UPLINKS ---
from ...contracts.data_contracts import ExecutionPlan
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.symphony_contracts import Edict, EdictType, Reality
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import RunRequest
from ...logger import Scribe, get_console
from ...symphony.polyglot.artisan import PolyglotArtisan
from ...symphony.polyglot.grimoire import POLYGLOT_GRIMOIRE


class PolyglotBridge:
    """
    =================================================================================
    == THE GNOSTIC AMBASSADOR (V-Ω-TOTALITY-V100T)                                 ==
    =================================================================================
    LIF: ∞ | ROLE: DIPLOMATIC_SUBSTRATE_MEDIATOR | RANK: OMEGA_SOVEREIGN

    The supreme diplomat between the Engine's Will and the Substrate's Matter.
    It transfigures abstract RunRequests into concrete, warded Polyglot Edicts.
    =================================================================================
    """

    def __init__(self, engine: Any, logger: Scribe):
        """[THE RITE OF BINDING]"""
        self.engine = engine
        self.logger = logger
        self.console = get_console()
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                "pyodide" in sys.modules
        )

    def delegate(self,
                 language: str,
                 scripture_path: Path,
                 parent_request: RunRequest,
                 execution_plan: ExecutionPlan) -> ScaffoldResult:
        """
        =============================================================================
        == THE ULTRA-DEFINITIVE DELEGATION (V-Ω-TOTALITY)                         ==
        =============================================================================
        Conducts the foreign rite by summoning the one true Polyglot Conductor.

        [THE CURE]: Corrects the constructor call to PolyglotArtisan and implements
        the Absolute Substrate Bypass for POSIX commands.
        """
        # --- MOVEMENT 0: IDENTITY INCEPTION ---
        trace_id = (
                getattr(parent_request, 'trace_id', None) or
                getattr(getattr(parent_request, 'metadata', {}), 'trace_id', None) or
                f"tr-bridge-{uuid.uuid4().hex[:6].upper()}"
        )

        self.logger.verbose(f"[{trace_id}] Polyglot Ambassador awakened for a '{language}' rite.")

        # =========================================================================
        # == MOVEMENT I: THE RECIPE ADJUDICATION (THE CURE)                      ==
        # =========================================================================
        # [ASCENSION 2]: ACHRONAL LOGIC SCRYING
        # If the Architect willed a "shell" rite, we synthesize a Virtual Recipe.
        # This prevents the 'No Gnostic recipe found' heresy.

        recipe = None
        if language == "shell":
            recipe = {
                "name": "Shell_Substrate",
                "execution_style": "direct_shell",
                "interpreter": [],  # Shell commands are their own interpreter
                "extensions": [],
                "platform": "universal"
            }
        else:
            recipe = POLYGLOT_GRIMOIRE.get(language)

        if not recipe:
            raise ArtisanHeresy(
                f"No Gnostic recipe manifest for the '{language}' tongue.",
                suggestion=f"Supported tongues: {', '.join(POLYGLOT_GRIMOIRE.keys())}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )

        exec_style = recipe.get("execution_style", "temp_file")

        # --- MOVEMENT II: GEOMETRIC ANCHORING ---
        # [ASCENSION 5]: Achronal Path Normalization
        try:
            abs_scripture_path = scripture_path.resolve()
        except Exception:
            abs_scripture_path = scripture_path

        edict_command = str(abs_scripture_path)
        raw_scripture = f"{language}: >> {scripture_path.name}"
        script_block = ""
        mode_label = "FILE"

        # --- MOVEMENT III: MATTER BIOPSY (EVAL / PIPE / FILE) ---
        if getattr(parent_request, 'eval_content', None):
            mode_label = "EVAL"
            script_block = parent_request.eval_content
            raw_scripture = f"{language}(eval): >> [Inline_Gnosis]"

        elif getattr(parent_request, 'pipe_content', None):
            mode_label = "PIPE"
            script_block = parent_request.pipe_content
            raw_scripture = f"{language}(pipe): >> [Stream_Gnosis]"

        elif exec_style in ["temp_file", "stdin_pipe"]:
            if abs_scripture_path.is_file():
                try:
                    script_block = abs_scripture_path.read_text(encoding='utf-8', errors='replace')
                except Exception as e:
                    self.logger.warn(
                        f"[{trace_id}] Matter Scry Interrupted: Could not read '{scripture_path.name}'. {e}")
                    script_block = ""

        # [ASCENSION 10]: BINARY ENTROPY WARD
        if "\x00" in script_block:
            self.logger.warn(f"[{trace_id}] Binary Entropy detected in script block. Redacting.")
            script_block = "[BINARY_MATTER_REDACTED]"

        # FORGE THE EDICT VESSEL
        edict = Edict(
            type=EdictType.POLYGLOT_ACTION,
            raw_scripture=raw_scripture,
            line_num=getattr(parent_request, 'line_num', 0),
            language=language,
            command=edict_command,
            script_block=script_block,
            source_blueprint=scripture_path
        )

        # =========================================================================
        # == MOVEMENT IV: FORGING THE GNOSTIC CONTEXT (ENV DNA)                  ==
        # =========================================================================
        context = os.environ.copy()

        # [ASCENSION 4]: NONETYPE SARCOPHAGUS FOR VARIABLES
        request_vars = getattr(parent_request, 'variables', {}) or {}
        for key, value in request_vars.items():
            context[f"SC_VAR_{str(key).upper()}"] = str(value)

        # [ASCENSION 3]: ISOMORPHIC TRACE BLOODLINE
        context["SC_TRACE_ID"] = trace_id
        context["SC_PROJECT_ROOT"] = str(parent_request.project_root or self.engine.project_root or os.getcwd())
        context["SC_TIMESTAMP"] = str(int(time.time()))
        context["SC_RITE_MODE"] = mode_label
        context["SC_SCRIPT_PATH"] = str(abs_scripture_path)
        context["SC_PLATFORM"] = platform.system()
        context["PYTHONUNBUFFERED"] = "1"
        context["FORCE_COLOR"] = "1"

        # [ASCENSION 9]: VIRTUAL ENVIRONMENT SENTINEL
        venv_path = self._scry_virtual_environment(parent_request.project_root)
        if venv_path:
            bin_dir = venv_path / ("Scripts" if os.name == 'nt' else "bin")
            if bin_dir.exists():
                self.logger.verbose(f"[{trace_id}] Venv Sentinel: Injecting '{bin_dir.as_posix()}' into PATH.")
                context["PATH"] = str(bin_dir.resolve()) + os.pathsep + context.get("PATH", "")
                context["VIRTUAL_ENV"] = str(venv_path.resolve())

        # =========================================================================
        # == MOVEMENT V: THE SACRED COMMUNION (EXECUTION)                       ==
        # =========================================================================
        try:
            if not getattr(parent_request, 'silent', False):
                self.console.print(
                    f"[dim]Conducting {language.upper()} rite ({mode_label}) [Trace: {trace_id[:8]}]...[/dim]")

            # [STRIKE]: Summon the Polyglot Artisan
            # =========================================================================
            # == [THE FIX]: TRIPLE-SUTURE CONSTRUCTOR CALL                           ==
            # =========================================================================
            # [ASCENSION 1]: We pass 'self.engine' as the first positional anchor,
            # annihilating the "Expected type 'str', got 'dict'" heresy.
            artisan = PolyglotArtisan(self.engine, language, recipe)

            # [ASCENSION 11]: ADRENALINE SYNCHRONIZATION
            if getattr(parent_request, 'is_adrenaline', False):
                self.engine.set_adrenaline(True)

            # CONDUCT THE RITE
            reality = artisan.conduct_with_plan(
                script_code=script_block,
                context=context,
                sanctum=abs_scripture_path.parent,
                edict=edict,
                execution_plan=execution_plan
            )

            # =========================================================================
            # == MOVEMENT VI: THE FINAL ADJUDICATION & PROCLAMATION                 ==
            # =========================================================================
            # [ASCENSION 5]: HYDRAULIC BUFFER DEBOUNCING
            self._proclaim_result(reality, language, trace_id)

            if reality.returncode == 0:
                return self.engine.success(
                    message=f"The foreign rite of '{language}' was conducted purely.",
                    data={"output": reality.output, "exit_code": 0, "trace_id": trace_id},
                    ui_hints={"vfx": "bloom", "color": "#64ffda"}
                )
            else:
                # [ASCENSION 6]: SOCRATIC ERROR TRIAGE
                error_msg = f"The foreign rite of '{language}' was tainted by a heresy (Exit: {reality.returncode})."
                suggestion = "Scry the forensic logs in the terminal for the cause of death."

                if reality.returncode == 127:
                    suggestion = f"The binary for '{language}' was not manifest. Check 'velm runtimes health'."
                elif reality.returncode == 130:
                    error_msg = f"Rite of '{language}' was stayed by the Architect (SIGINT)."
                    suggestion = "Timeline preserved."

                return self.engine.failure(
                    message=error_msg,
                    suggestion=suggestion,
                    details=reality.output,
                    severity=HeresySeverity.WARNING if reality.returncode == 130 else HeresySeverity.CRITICAL,
                    data={"exit_code": reality.returncode, "trace_id": trace_id},
                    ui_hints={"vfx": "shake", "color": "#ef4444"}
                )

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE UNBREAKABLE WARD
            tb = traceback.format_exc()
            self.logger.critical(f"[{trace_id}] Bridge Fracture: {catastrophic_paradox}")

            raise ArtisanHeresy(
                f"A catastrophic paradox shattered the Polyglot Bridge during the '{language}' rite.",
                details=f"{str(catastrophic_paradox)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )
        finally:
            self.engine.set_adrenaline(False)

    # =========================================================================
    # == INTERNAL FACULTIES (SENSORS & HERALDS)                              ==
    # =========================================================================

    def _scry_virtual_environment(self, project_root: Optional[Path]) -> Optional[Path]:
        """[ASCENSION 9]: Detects local venv for automatic PATH injection."""
        root = project_root or self.engine.project_root or Path.cwd()
        for venv_name in [".venv", "venv", "env"]:
            candidate = root / venv_name
            if candidate.is_dir():
                return candidate
        return None

    def _proclaim_result(self, reality: Reality, language: str, trace_id: str):
        """
        [ASCENSION 7]: THE GNOSTIC JSON ALCHEMIST
        Intelligently materializes the output of the rite into the Ocular HUD.
        """
        output = str(reality.output or "").strip()
        if not output: return

        # --- MOVEMENT I: THE JSON ALCHEMIST ---
        try:
            if (output.startswith('{') and output.endswith('}')) or \
                    (output.startswith('[') and output.endswith(']')):

                # Buffer Protection
                if len(output) > 100000: return

                json_obj = json.loads(output)
                self.console.print(Panel(
                    JSON.from_data(json_obj, indent=4),
                    title=f"[bold green]✨ {language.upper()} REVELATION (JSON)[/bold green]",
                    subtitle=f"[dim]Trace: {trace_id[:8]}[/dim]",
                    border_style="green",
                    padding=(1, 2)
                ))
                return
        except (json.JSONDecodeError, Exception):
            pass

        # --- MOVEMENT II: THE FRACTURE PANEL ---
        if reality.returncode != 0 and reality.returncode != 130:
            self.console.print(Panel(
                Text(output, style="red"),
                title=f"[bold red]💀 HERESY DETECTED: {language.upper()} (Exit {reality.returncode})[/bold red]",
                subtitle=f"[dim]Locus: {trace_id}[/dim]",
                border_style="red",
                padding=(1, 2)
            ))

    def __repr__(self) -> str:
        return f"<Ω_POLYGLOT_AMBASSADOR status=RESONANT substrate={'WASM' if self.is_wasm else 'IRON'}>"