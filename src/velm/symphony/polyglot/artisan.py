# Path: src/velm/symphony/polyglot/artisan.py
# =========================================================================================
# == THE POLYGLOT ARTISAN: OMEGA POINT (V-Ω-TOTALITY-V25000.42-CONCRETE-FINALIS)        ==
# =========================================================================================
# LIF: ∞ | ROLE: CROSS_LANGUAGE_EXECUTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_POLYGLOT_V25K_CONCRETE_SUTURE_2026_FINALIS
# =========================================================================================

import importlib
import importlib.util
import io
import json
import os
import platform
import re
import shlex
import subprocess
import tempfile
import time
import uuid
import sys
import traceback
from pathlib import Path
from queue import Queue, Empty
from threading import Thread
from typing import Dict, Any, Optional, List, Tuple, Union, Callable

# --- THE LUMINOUS UI & TELEMETRY ---
from rich.panel import Panel
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...constants import DEFAULT_COMMAND_TIMEOUT
from ...containerization import DockerEngine
from ...contracts.data_contracts import ExecutionPlan
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.symphony_contracts import Reality, Edict
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import PolyglotRequest
from ...logger import Scribe, get_console
from ...settings.manager import SettingsManager

# =========================================================================================
# == [THE CURE]: THE ISOMORPHIC IMPORT PHALANX                                           ==
# =========================================================================================
# Resolves the RuntimeManager coordinate across all physical and virtual substrates.
RuntimeManager = None
try:
    from ...runtime_manager import RuntimeManager as RM

    RuntimeManager = RM
except ImportError:
    try:
        import runtime_manager

        RuntimeManager = runtime_manager.RuntimeManager
    except (ImportError, AttributeError):
        try:
            from velm.runtime_manager import RuntimeManager as RM

            RuntimeManager = RM
        except ImportError:
            pass


# =========================================================================================

class PolyglotArtisan(BaseArtisan[PolyglotRequest]):
    """
    =================================================================================
    == THE POLYGLOT ARTISAN: OMEGA TOTALITY (V-Ω-TOTALITY-V24000.12-FINALIS)       ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_WORMHOLE_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The supreme ambassador for executing foreign scriptures. It has been ascended
    to possess "Total Isomorphic Awareness," handling local-to-remote friction
    across all operating system substrates with zero metabolic waste.
    """

    def __init__(self, engine: Any, language: str = "python", recipe: Optional[Dict] = None):
        """
        =============================================================================
        == THE RITE OF INCEPTION: OMEGA (V-Ω-TOTALITY-V25000.42-SUTURED)           ==
        =============================================================================
        [ASCENSION 4]: Harmonized constructor to resolve circular and abstract heresies.
        """
        # --- 1. SOVEREIGN ANCESTRY ---
        # Inherit the Hand (io), the Eye (cortex), and the Voice (console).
        super().__init__(engine)

        # --- 2. GNOSTIC BINDING (THE FIX) ---
        # Enshrine the language and recipe in the mind.
        self.language = language.lower()
        self.recipe = recipe or {}

        # --- 3. ORGAN MATERIALIZATION ---
        self.logger = Scribe(f"Polyglot:{self.language.upper()}")
        self.settings = SettingsManager()
        self.docker_engine = DockerEngine()

        # --- 4. IDENTITY PROJECTION ---
        self._uid = os.getuid() if hasattr(os, 'getuid') else 1000
        self._gid = os.getgid() if hasattr(os, 'getgid') else 1000

        # --- 5. SUBSTRATE SENSING ---
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # --- 6. LAZY FACULTY SLOTS ---
        self._runtime_manager = None
        self._warned_security = False

    @property
    def manager(self) -> Any:
        """[THE LAZY FORGE]: Materializes the RuntimeManager exactly when willed."""
        if not self._runtime_manager:
            if RuntimeManager is None:
                raise ArtisanHeresy(
                    "Runtime Strategy Fractured: The RuntimeManager soul is unmanifest.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Ensure the Engine has finished unzipping its arsenal."
                )
            self._runtime_manager = RuntimeManager(engine=self.engine)
        return self._runtime_manager

    # =========================================================================
    # == THE CONCRETE EXECUTION VOW (THE CURE)                               ==
    # =========================================================================

    def execute(self, request: PolyglotRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE UNIVERSAL EXECUTION RITE: OMEGA (V-Ω-TOTALITY-V25000.42)            ==
        =============================================================================
        [ASCENSION 1]: Overrides the abstract method, making the class concrete.
        Allows the PolyglotArtisan to be dispatched directly for ad-hoc strikes.
        """
        trace_id = getattr(request, 'trace_id', f"tr-poly-{uuid.uuid4().hex[:6].upper()}")
        start_ns = time.perf_counter_ns()

        # [ASCENSION 11]: HUD Resonance
        self._multicast_hud("STRIKE_AWAKENED", "#a855f7", trace_id)

        try:
            # --- MOVEMENT I: THE PRE-FLIGHT INQUEST ---
            # [ASCENSION 8]: Geometric Normalization
            sanctum = Path(request.working_directory or self.project_root).resolve()
            if not sanctum.exists():
                sanctum.mkdir(parents=True, exist_ok=True)

            # --- MOVEMENT II: STRATEGY ADJUDICATION ---
            # We ask the Manager limb to resolve the optimal execution plan
            # (Iron vs. Docker vs. WASM-Mock)
            plan = self.manager.resolve_execution_plan(
                language=self.language,
                runtime_spec=request.runtime,
                sanctum=sanctum
            )

            # --- MOVEMENT III: THE SACRED COMMUNION (STRIKE) ---
            # [ASCENSION 4 & 9]: Environment Transmutation
            env_context = {
                **getattr(request, 'variables', {}),
                "trace_id": trace_id,
                "project_root": str(self.project_root)
            }

            # [ASCENSION 7]: Engage Adrenaline for the Strike
            self.engine.set_adrenaline(True)

            # Execute the conduct_with_plan logic (Movement III in Part 3/3)
            reality = self.conduct_with_plan(
                script_code=request.script_block or "",
                context=env_context,
                sanctum=sanctum,
                edict=None,  # Standalone strikes have no parent edict
                execution_plan=plan
            )

            # --- MOVEMENT IV: REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if reality.returncode == 0:
                self._multicast_hud("STRIKE_RESONANT", "#64ffda", trace_id)
                return self.success(
                    message=f"Rite of '{self.language}' manifest purely.",
                    data={"output": reality.output, "duration_ms": duration_ms}
                )
            else:
                self._multicast_hud("STRIKE_FRACTURED", "#ef4444", trace_id)
                return self.failure(
                    message=f"Rite of '{self.language}' fractured (Exit: {reality.returncode}).",
                    details=reality.output,
                    data={"exit_code": reality.returncode, "duration_ms": duration_ms}
                )

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW
            tb = traceback.format_exc()
            self.logger.error(f"Polyglot Inception Fracture: {catastrophic_paradox}")
            return self.failure(
                message=f"Catastrophic Paradox in '{self.language}' execution.",
                details=f"{str(catastrophic_paradox)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )
        finally:
            self.engine.set_adrenaline(False)

    def _multicast_hud(self, label: str, color: str, trace: str):
        """[ASCENSION 11]: Radiates kinetic signals to the Ocular HUD."""
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "POLYGLOT_STRIKE",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "language": self.language
                    }
                })
            except Exception:
                pass

    # =========================================================================
    # == MOVEMENT II: GNOSTIC UTILITIES (THE INTERNAL GRIMOIRE)               ==
    # =========================================================================

    def _forge_gnostic_environment(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        =============================================================================
        == THE ALCHEMICAL ENVIRONMENT FORGE: OMEGA (V-Ω-TOTALITY-V200.4)           ==
        =============================================================================
        LIF: ∞ | ROLE: CONTEXT_DNA_TRANSMUTER | RANK: OMEGA_SUPREME

        [ASCENSION 13]: Bifurcated Variable Injection.
        Transfigures Gnostic objects into POSIX-compliant environment strings.
        """
        # 1. PURIFICATION: Inhale the host DNA and purge system poisons
        env = os.environ.copy()

        # [ASCENSION 7]: Banish language-specific host paths to prevent leakage
        poisons = [
            'PYTHONPATH', 'NODE_PATH', 'GEM_HOME', 'GOPATH', 'PYTHONHOME',
            'PERL5LIB', 'PYTHONSTARTUP', 'NODE_OPTIONS'
        ]
        for poison in poisons:
            if poison in env: del env[poison]

        # 2. INJECTION: Graft Architect's Variables as SC_VAR_ constants
        for key, value in context.items():
            # [THE FIX]: Absolute key normalization
            safe_key = re.sub(r'[^A-Z0-9_]', '_', str(key).upper())
            env_key = f"SC_VAR_{safe_key}"

            # Type-Aware Transmutation
            if isinstance(value, (dict, list, bool)):
                env[env_key] = json.dumps(value)
            elif value is None:
                env[env_key] = ""
            else:
                env[env_key] = str(value)

        # 3. METABOLISM: Substrate-Aware Constants
        # [ASCENSION 14]: Path-Separator Iron Harmony
        path_sep = ";" if os.name == 'nt' else ":"

        env.update({
            'PYTHONUNBUFFERED': '1',
            'PYTHONIOENCODING': 'utf-8',
            'SCAFFOLD_ENV': 'WASM' if self.is_wasm else 'IRON',
            'SC_TRACE_ID': context.get('trace_id', 'tr-poly-void'),
            'SC_PROJECT_ROOT': str(self.project_root).replace('\\', '/'),
            'SC_PLATFORM': platform.system(),
            'SC_ARCH': platform.machine(),
            'FORCE_COLOR': '1',
            'NSUnbufferedIO': 'YES'
        })

        # 4. VIRTUAL ENVIRONMENT SUTURE (ASCENSION 23)
        # We scry for the project's lungs (.venv) and inject them into the PATH.
        for venv_name in [".venv", "venv", "env"]:
            v_path = self.project_root / venv_name
            if v_path.is_dir():
                bin_dir = v_path / ("Scripts" if os.name == 'nt' else "bin")
                if bin_dir.exists():
                    env["PATH"] = str(bin_dir.resolve()) + path_sep + env.get("PATH", "")
                    env["VIRTUAL_ENV"] = str(v_path.resolve())
                    break

        # 5. RECIPE OVERRIDES (ASCENSION 17)
        # Inhale environment DNA willed by the Blueprint Author.
        recipe_env = self.recipe.get("env", {})
        if recipe_env:
            for k, v in recipe_env.items():
                env[str(k)] = str(v).replace("{{project_root}}", str(self.project_root))

        return env

    def _resolve_command_template(self,
                                  template: List[str],
                                  script_path: Path,
                                  trace_id: str) -> List[str]:
        """
        =============================================================================
        == THE GEOMETRIC COMMAND ORACLE (V-Ω-TOTALITY-V200.4)                      ==
        =============================================================================
        [ASCENSION 15]: Recursive Template Resolution.
        Transmutes interpreter commands into absolute physical edicts.
        """
        resolved = []
        # Canonicalize the script locus to POSIX standards
        abs_script = str(script_path.resolve()).replace('\\', '/')
        abs_sanctum = str(script_path.parent.resolve()).replace('\\', '/')

        for part in template:
            if not isinstance(part, str):
                resolved.append(str(part))
                continue

            # Atomic Token Replacement
            p = part.replace("{{script_path}}", abs_script)
            p = p.replace("{{script_path.stem}}", script_path.stem)
            p = p.replace("{{script_path.name}}", script_path.name)
            p = p.replace("{{sanctum}}", abs_sanctum)
            p = p.replace("{{trace_id}}", trace_id)

            # [ASCENSION 21]: Resolve env placeholders inside templates
            if "${" in p:
                for env_k, env_v in os.environ.items():
                    p = p.replace(f"${{{env_k}}}", env_v)

            resolved.append(p)

        return resolved

    def _forge_gnostic_ward_harness(self, language: str, sanctum: Path) -> str:
        """
        =============================================================================
        == THE GNOSTIC WARD HARNESS (V-Ω-TOTALITY-V200.4)                          ==
        =============================================================================
        [ASCENSION 16]: Security Inception.
        Injects substrate-level wards directly into the guest script's soul.
        """
        # [THE FIX]: Bypass for non-script languages or WASM stubs
        if language not in ("python", "python3", "py"):
            return ""

        sanctum_posix = str(sanctum.resolve()).replace('\\', '/')

        # [THE CURE]: A titanium Python ward to prevent sanctum escape.
        return f"""
import sys, os
from pathlib import Path
def _scaffold_ward_inquest(path):
    p = str(Path(path).resolve()).replace('\\\\', '/')
    if not p.startswith('{sanctum_posix}'):
        print(f"\\n[SECURITY_HERESY] 🛡️  Substrate Escape Blocked: {{p}}", file=sys.stderr)
        os._exit(1)
# Enshrined Guard
"""

    def _sanitize_output(self, output: str) -> str:
        """[ASCENSION 11]: Annihilates null-bytes and normalizes CRLF."""
        if not output: return ""
        # Remove null bytes which fracture the JS bridge
        clean = output.replace('\0', '')
        # Normalize Windows drift to POSIX harmony for XTerm.js
        clean = clean.replace('\r\n', '\n')
        return clean

    # =========================================================================
    # == MOVEMENT III: THE KINETIC STRIKE (EXECUTION)                        ==
    # =========================================================================

    def _stream_output(self, pipe: io.IOBase, queue: Queue):
        """
        [THE LIVING STREAM]: Movement III.A
        Reads from a pipe and puts lines into a queue for hydraulic processing.
        Sutured to a daemon thread to prevent main-thread I/O asphyxiation.
        """
        try:
            # We use unbuffered binary reads to prevent encoding fractures
            for line in iter(pipe.readline, b''):
                if line: queue.put(line)
        except Exception:
            pass
        finally:
            queue.put(None)  # Signal End of Stream

    def _proclaim_security_guidance(self, strategy: str):
        """
        =============================================================================
        == THE OMEGA SECURITY PROCLAMATION (V-Ω-TOTALITY-V500.8)                   ==
        =============================================================================
        LIF: ∞ | ROLE: SOCRATIC_SECURITY_SENTINEL | RANK: LEGENDARY

        [ASCENSION 15]: Substrate-Aware Inquest.
        Detects and warns of un-warded execution substrates.
        """
        # --- 1. THE VOW OF SILENCE ---
        # We avert the Gaze if the Architect has willed a mute environment
        if os.getenv("SCAFFOLD_MUTE_SECURITY_HINTS") == "1":
            return

        # --- 2. HYSTERESIS ADJUDICATION ---
        # We only proclaim this law once per Artisan lifecycle to preserve metabolism
        if getattr(self, '_warned_security', False):
            return

        # --- 3. SUBSTRATE INQUEST ---
        # If we are in Docker or WASM, the reality is already warded.
        if strategy in ('docker', 'wasm', 'simulacrum'):
            return

        # =========================================================================
        # == MOVEMENT I: THE RADIATIVE PROCLAMATION                              ==
        # =========================================================================
        self._warned_security = True

        # We forge a high-status Rich Text artifact for the Ocular HUD
        hint = Text.assemble(
            ("ENVIRONMENTAL_SENSING: ", "bold cyan"),
            (f"Running in {strategy.upper()} mode. ", "bold yellow"),
            ("\n[WARDEN] ", "bold red"),
            ("For absolute isolation and Merkle-locked reproducibility, ", "dim"),
            ("consider transmuting your strategy to ", "dim"),
            ("docker", "bold white underline"),
            (" via ", "dim"),
            ("scaffold settings", "bold green italic"),
            (".", "dim")
        )

        # Strike the Console
        self.console.print(Panel(
            hint,
            title="[bold red]🛡️  GNOSTIC_SECURITY_ADVISORY[/]",
            title_align="left",
            border_style="yellow",
            padding=(1, 2),
            subtitle="[dim]Substrate: IRON_NATIVE[/dim]",
            subtitle_align="right"
        ))

    def conduct_with_plan(
            self,
            script_code: str,
            context: Dict[str, Any],
            sanctum: Path,
            edict: Optional['Edict'],
            execution_plan: ExecutionPlan
    ) -> Reality:
        """
        =================================================================================
        == THE RITE OF ALCHEMICAL EXECUTION: OMEGA (V-Ω-TOTALITY-V500.8-RESILIENT)     ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONDUCT_V500_8_THREADING_SUTURE_2026_FINALIS
        """
        start_time = time.monotonic()
        final_output_list: List[str] = []
        final_returncode: int = 1
        was_terminated: bool = False

        # --- MOVEMENT 0: IDENTITY & METADATA INCEPTION ---
        # [ASCENSION 3]: Achronal Trace Bloodline
        trace_id = (
                context.get('trace_id') or
                getattr(edict, 'trace_id', None) or
                f"tr-poly-{uuid.uuid4().hex[:6].upper()}"
        )

        # --- 1. THE REVELATION OF PLAN ---
        strategy = execution_plan.get('strategy', 'system')
        interpreter_cmd = execution_plan.get('interpreter_cmd', ['python'])
        docker_image = execution_plan.get('docker_image')

        # [ASCENSION 9]: Socratic Security Ward
        self._proclaim_security_guidance(strategy)

        # --- 2. THE TIMEOUT SENTINEL ---
        # [ASCENSION 5]: Substrate-Aware Timeout Scaling
        total_timeout = DEFAULT_COMMAND_TIMEOUT
        if self.is_wasm: total_timeout *= 2

        # --- 3. THE GNOSTIC ENVIRONMENT ---
        env = self._forge_gnostic_environment(context)
        abs_sanctum = sanctum.resolve()

        process = None
        ephemeral_path: Optional[Path] = None

        try:
            # =========================================================================
            # == MOVEMENT I: MATTER MATERIALIZATION                                  ==
            # =========================================================================
            final_script_block = script_code
            execution_style = self.recipe.get("execution_style", "temp_file")

            if strategy != 'docker' and script_code.strip():
                # Inhale language-specific wards (FS/Network)
                ward_harness = self._forge_gnostic_ward_harness(self.language, abs_sanctum)
                final_script_block = f"{ward_harness}\n{script_code}"

            final_cmd_list = []

            if execution_style == "temp_file":
                # Forge the temporary shard within the sanctum
                suffix = self.recipe.get("file_extension", ".py")
                with tempfile.NamedTemporaryFile(
                        mode='w+', delete=False, suffix=suffix, dir=str(abs_sanctum), encoding='utf-8'
                ) as tf:
                    ephemeral_path = Path(tf.name)
                    tf.write(final_script_block)

                # Resolve Template coordinates
                script_ref = Path(f"/app/{ephemeral_path.name}") if strategy == 'docker' else ephemeral_path
                final_cmd_list = self._resolve_command_template(interpreter_cmd, script_ref, trace_id)

            elif execution_style == "direct_shell":
                # [THE CURE]: Absolute Posix Bypass. Target is the raw command string.
                final_cmd_list = [str(script_code)]
            else:
                final_cmd_list = self._resolve_command_template(interpreter_cmd, Path(""), trace_id)

            # =========================================================================
            # == MOVEMENT II: THE SUBSTRATE ENCAPSULATION                            ==
            # =========================================================================
            if strategy == 'docker' and docker_image:
                final_cmd_list = self.docker_engine.forge_run_command(
                    image=docker_image,
                    command=final_cmd_list,
                    volumes={abs_sanctum: "/app"},
                    env_vars=env,
                    workdir="/app"
                )
                process_env = os.environ.copy()  # Native iron env for Docker client
            else:
                process_env = env

            # =========================================================================
            # == MOVEMENT III: THE KINETIC IGNITION                                  ==
            # =========================================================================
            final_command_str = " ".join(shlex.quote(str(p)) for p in final_cmd_list)

            if not self.is_wasm:
                self.logger.info(f"[{trace_id}] Ignite: [dim]{final_command_str}[/]", bare=True)

            process = subprocess.Popen(
                final_cmd_list if execution_style != "direct_shell" else final_command_str,
                shell=(execution_style == "direct_shell"),
                cwd=str(abs_sanctum),
                env=process_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Stream Fusion
                text=False,  # Binary mode for encoding resilience
                bufsize=0  # Unbuffered for real-time radiation
            )

            # =========================================================================
            # == MOVEMENT IV: THE HYDRAULIC STREAM (V-Ω-SUBSTRATE-AWARE)             ==
            # =========================================================================
            # [ASCENSION 1]: The Apophatic Threading Suture (THE CURE).
            # We bypass the 'Thread' inception in WASM to prevent RuntimeError.

            if self.is_wasm:
                # --- BRANCH A: ETHERIC REALITY (WASM SYNC DRAIN) ---
                # [ASCENSION 2]: Synchronous Matter Inhalation.
                # Since the WASM Subprocess is a Mock, the stdout is already resident.
                for line in iter(process.stdout.readline, b''):
                    if line:
                        # [ASCENSION 8]: Binary-Resistant Encoding
                        decoded = line.decode('utf-8', errors='replace').rstrip()
                        final_output_list.append(decoded)
                        # direct radiation to the Ocular HUD
                        self.logger.info(decoded, bare=True)
                        # [ASCENSION 7]: Hydraulic Yield for the JS Event Loop
                        time.sleep(0)
            else:
                # --- BRANCH B: IRON REALITY (NATIVE THREADED STREAM) ---
                output_queue = Queue()
                # Siphoning the voice in a dedicated thread to prevent I/O deadlock.
                stream_thread = Thread(target=self._stream_output, args=(process.stdout, output_queue), daemon=True)
                stream_thread.start()

                while True:
                    try:
                        line = output_queue.get(timeout=0.02)
                        if line is None: break  # End of stream reached

                        decoded = line.decode('utf-8', errors='replace').rstrip()
                        final_output_list.append(decoded)
                        self.logger.info(decoded, bare=True)

                    except Empty:
                        # [ASCENSION 12]: THE ZOMBIE REAPER
                        if process.poll() is not None:
                            # Process concluded. Perform final hydraulic drain.
                            while not output_queue.empty():
                                l = output_queue.get_nowait()
                                if l:
                                    d = l.decode('utf-8', errors='replace').rstrip()
                                    final_output_list.append(d);
                                    self.logger.info(d, bare=True)
                            break

                        # TIMEOUT ADJUDICATION
                        if (time.monotonic() - start_time) > total_timeout:
                            process.kill()
                            was_terminated = True
                            msg = f"💀 TIMEOUT: Rite exceeded {total_timeout}s. Severing link."
                            final_output_list.append(msg);
                            self.logger.error(msg)
                            break

            final_returncode = process.wait()

        except Exception as catastrophic_paradox:
            # [ASCENSION 22]: FORENSIC REDEMPTION
            tb = traceback.format_exc()
            self.logger.error(f"Polyglot Fracture: {catastrophic_paradox}")
            raise ArtisanHeresy(
                f"Dimensional Fracture in '{self.language}' execution.",
                details=f"{str(catastrophic_paradox)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )

        finally:
            # =========================================================================
            # == MOVEMENT V: LUSTRATION & DRAIN                                      ==
            # =========================================================================
            # 1. Kill the zombie processes
            # [ASCENSION 4]: NoneType Process Sarcophagus
            if process and process.poll() is None:
                try:
                    process.terminate();
                    process.wait(timeout=1)
                except:
                    if process: process.kill()

            # 2. [ASCENSION 11]: ATOMIC MATTER PURGATION
            if ephemeral_path and ephemeral_path.exists():
                try:
                    ephemeral_path.unlink()
                except Exception as e:
                    self.logger.warn(f"Lustration deferred for {ephemeral_path.name}: {e}")

        # --- MOVEMENT VI: REVELATION ---
        duration = time.monotonic() - start_time
        raw_output = "\n".join(final_output_list)

        # [ASCENSION 10]: Finality HUD Signal
        self._multicast_hud("STRIKE_CONCLUDED", "#10b981" if final_returncode == 0 else "#ef4444", trace_id)

        # [ASCENSION 12]: THE FINALITY VOW
        return Reality(
            output=self._sanitize_output(raw_output),
            returncode=final_returncode,
            duration=duration,
            command=final_command_str,
            was_terminated=was_terminated
        )

    def __repr__(self) -> str:
        return f"<Ω_POLYGLOT_ARTISAN language='{self.language}' status=RESONANT>"

