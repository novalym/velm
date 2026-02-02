# Path: scaffold/symphony/polyglot/artisan.py
# -------------------------------------------


"""
=================================================================================
== THE POLYGLOT ARTISAN (V-Ω-LEGENDARY-ULTIMA. THE HIGH PROTECTOR)             ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000

This is the divine Hand of the Polyglot Conductor. It has ascended to become a
**High Protector**. It prefers the Celestial Ward (Docker) for its ultimate
security, but guides the Architect with wisdom and grace if they must walk the
Mortal Path (System/Local).

It now supports **Live Streaming** of the foreign rite's voice via the Gnostic Logger.
"""
import importlib
import json
import os
import re
import shlex
import subprocess
import tempfile
import time
from pathlib import Path
from queue import Queue, Empty
from threading import Thread
from typing import Dict, Any, Optional, List

# --- The Divine Stanza of the Scribe's Tools ---
from rich.panel import Panel
from rich.text import Text

from ...constants import DEFAULT_COMMAND_TIMEOUT
from ...containerization import DockerEngine
from ...contracts.data_contracts import ExecutionPlan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.symphony_contracts import Reality, Edict
from ...logger import Scribe, get_console
from ...runtime_manager import RuntimeManager
from ...settings.manager import SettingsManager

Logger = Scribe("PolyglotArtisan")


class PolyglotArtisan:
    """The Gnostic Ambassador, Governor of Runtimes, and High Protector."""

    def __init__(self, language: str, recipe: Dict[str, Any]):
        """
        The Rite of Inception. The artisan is born with the knowledge of its tongue
        and the sacred recipe for its invocation. It immediately forges its divine
        instruments for communing with all possible realities.
        """
        self.logger = Logger
        self.language = language
        self.recipe = recipe
        self.runtime_manager = RuntimeManager(silent=True)
        self.docker_engine = DockerEngine()
        self.settings = SettingsManager()
        self.console = get_console()

        # [FACULTY 25] The Identity Projector (Cache user info for Docker)
        self._uid = os.getuid() if hasattr(os, 'getuid') else 1000
        self._gid = os.getgid() if hasattr(os, 'getgid') else 1000

    # --- GNOSTIC UTILITIES (THE ARTISAN'S INTERNAL GRIMOIRE) ---
    def _forge_gnostic_ward_harness(self, language: str, sanctum: Path) -> str:
        try:
            ward_module_name = f"scaffold.symphony.polyglot.wards.{language}_ward"
            ward_module = importlib.import_module(ward_module_name)
            sanctum_abs_path = str(sanctum.resolve())
            return ward_module.get_harness(sanctum_abs_path)
        except (ImportError, Exception):
            return ""

    def _forge_network_ward_harness(self, language: str) -> str:
        try:
            ward_module_name = f"scaffold.symphony.polyglot.wards.{language}_network_ward"
            ward_module = importlib.import_module(ward_module_name)
            return ward_module.get_harness()
        except (ImportError, Exception):
            return ""

    def _forge_gnostic_environment(self, context: Dict[str, Any]) -> Dict[str, str]:
        env = os.environ.copy()
        for poison in ['PYTHONPATH', 'NODE_PATH', 'GEM_HOME', 'GOPATH']:
            if poison in env: del env[poison]
        for key, value in context.items():
            safe_key = re.sub(r'[^A-Z0-9_]', '_', key.upper())
            env_key = f"SC_VAR_{safe_key}"
            if isinstance(value, (dict, list, bool)):
                env[env_key] = json.dumps(value)
            elif value is None:
                env[env_key] = ""
            else:
                env[env_key] = str(value)
        env['PYTHONIOENCODING'] = 'utf-8'
        env['SCAFFOLD_LOGGING_MODE'] = 'basic'
        return env

    def _resolve_command_template(self, template: List[str], script_path: Path) -> List[str]:
        resolved = []
        for part in template:
            part = part.replace("{{script_path}}", str(script_path.resolve()))
            part = part.replace("{{script_path.stem}}", script_path.stem)
            part = part.replace("{{script_path.name}}", script_path.name)
            part = part.replace("{{script_path.parent}}", str(script_path.parent.resolve()))
            resolved.append(part)
        return resolved

    def _sanitize_output(self, output: str) -> str:
        if not output: return ""
        clean = output.replace('\0', '')
        clean = clean.replace('\r\n', '\n')
        return clean

    def _conduct_sub_rite(self, cmd: List[str], cwd: Path, env: Dict, timeout: int):
        try:
            subprocess.run(cmd, cwd=cwd, env=env, timeout=timeout, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('utf-8', 'replace') if e.stderr else str(e)
            raise ArtisanHeresy(f"A pre-flight sub-rite (`{' '.join(cmd)}`) was tainted by a heresy.", details=err_msg)

    def _proclaim_security_guidance(self, strategy: str):
        if strategy != 'docker' and not os.getenv("SCAFFOLD_MUTE_SECURITY_HINTS"):
            if getattr(self, '_warned', False): return
            self._warned = True
            hint = Text.assemble(("running in ", "dim"), (f"{strategy.upper()} mode", "bold yellow"), (". ", "dim"),
                                 ("For ultimate isolation, install Docker and set ", "dim"),
                                 ("runtimes.strategy", "bold cyan"), (" to docker via ", "dim"),
                                 ("scaffold settings", "bold white"), (".", "dim"))
            self.console.print(Panel(hint, title="[dim]🛡️ Gnostic Security Guidance[/dim]", border_style="dim"))

    def conduct(self, script_code: str, context: Dict[str, Any], sanctum: Path, edict: 'Edict') -> Reality:
        # ... (Delegate to conduct_with_plan) ...
        runtime_match = re.search(r'runtime=["\']([^"\']+)["\']', edict.command)
        runtime_spec = runtime_match.group(1) if runtime_match else ""
        execution_plan = self.runtime_manager.resolve_execution_plan(
            language=self.language, runtime_spec=runtime_spec, sanctum=sanctum
        )
        return self.conduct_with_plan(script_code, context, sanctum, edict, execution_plan)

    def _stream_output(self, pipe, queue: Queue):
        """[THE LIVING STREAM] Reads from a pipe and puts lines into a queue."""
        try:
            with pipe:
                for line in iter(pipe.readline, b''):
                    queue.put(line)
        finally:
            queue.put(None)

    def conduct_with_plan(
            self,
            script_code: str,
            context: Dict[str, Any],
            sanctum: Path,
            edict: 'Edict',
            execution_plan: ExecutionPlan
    ) -> Reality:
        """
        =================================================================================
        == THE RITE OF ALCHEMICAL EXECUTION (V-Ω-STREAMING-ASCENDED-ULTIMA)            ==
        =================================================================================
        LIF: 10,000,000,000,000

        Executes a foreign scripture with streaming output, timeout protection, and
        gnostic cleanup. It honors the "Naked Voice" to ensure the terminal output
        looks native, while capturing the full soul for the chronicle.
        """
        start_time = time.monotonic()
        final_output_list: List[str] = []
        final_returncode: int = 1
        was_terminated: bool = False
        final_command_str: str = f"{self.language}>> [initializing]"
        ephemeral_path: Optional[Path] = None

        # Unpack The Plan
        strategy = execution_plan['strategy']
        interpreter_cmd = execution_plan['interpreter_cmd']
        docker_image = execution_plan['docker_image']

        # [FACULTY 1] The Security Proclamation
        self._proclaim_security_guidance(strategy)

        # [FACULTY 2] The Timeout Sentinel Configuration
        timeout_match = re.search(r'timeout=(\d+)', edict.command)
        total_timeout = int(timeout_match.group(1)) if timeout_match else DEFAULT_COMMAND_TIMEOUT

        # [FACULTY 3] The Debug Beacon Setup
        is_debug = context.get("SCAFFOLD_DEBUG_MODE") == "true"
        if is_debug and "debug_interpreter" in self.recipe:
            interpreter_cmd = self.recipe["debug_interpreter"]
            self.logger.verbose(f"Debug Interpreter Engaged: {interpreter_cmd}")

        # [FACULTY 4] The Gnostic Environment Forge
        env = self._forge_gnostic_environment(context)
        # Force unbuffered output for common languages to ensure live streaming
        env["PYTHONUNBUFFERED"] = "1"
        env["NSUnbufferedIO"] = "YES"  # Ruby/ObjC
        env["NODE_NO_WARNINGS"] = "1"  # Optional cleaner output

        abs_sanctum = sanctum.resolve()

        # Recipe Environment Injection
        recipe_env = self.recipe.get("env", {})
        for k, v in recipe_env.items():
            target_path_ref = Path(edict.command) if edict.command and Path(edict.command).exists() else abs_sanctum
            env[k] = v.replace("{{script_path.name}}", target_path_ref.name)

        process = None
        stream_thread = None

        try:
            # --- MOVEMENT I: THE FORGING OF THE SCRIPTURE ---
            final_script_block = script_code
            # Inject Gnostic Wards (Filesystem/Network checks) if running locally
            if strategy != 'docker' and script_code.strip():
                ward_harness_fs = self._forge_gnostic_ward_harness(self.language, abs_sanctum)
                ward_harness_net = self._forge_network_ward_harness(self.language)
                final_script_block = f"{ward_harness_fs}\n{ward_harness_net}\n{script_code}"

            execution_style = self.recipe.get("execution_style", "temp_file")
            final_cmd_list = []

            # --- MOVEMENT II: THE MATERIALIZATION ---
            if execution_style == "temp_file":
                suffix = self.recipe.get("file_extension", "")
                # Create the temp file inside the sanctum to allow relative imports
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=suffix, dir=str(abs_sanctum),
                                                 encoding='utf-8') as tf:
                    ephemeral_path = Path(tf.name)
                    tf.write(final_script_block)

                # Resolve path for Docker (mapped volume) vs Local
                script_ref = Path(f"/app/{ephemeral_path.name}") if strategy == 'docker' else ephemeral_path

                # Template resolution
                final_cmd_list = self._resolve_command_template(interpreter_cmd, script_ref)

                # [FACULTY 5] The Atomic Setup (Compilation)
                if "setup_commands" in self.recipe and strategy != 'docker':
                    for setup_tmpl in self.recipe["setup_commands"]:
                        setup_cmd = self._resolve_command_template(setup_tmpl, ephemeral_path)
                        self.logger.verbose(f"Conducting Setup Rite: {' '.join(setup_cmd)}")
                        self._conduct_sub_rite(setup_cmd, abs_sanctum, env, 60)

            elif execution_style == "direct":
                target_file = Path(edict.command) if edict.command else abs_sanctum
                script_ref = target_file
                if strategy == 'docker':
                    try:
                        rel_path = target_file.resolve().relative_to(abs_sanctum)
                        script_ref = Path(f"/app/{rel_path}")
                    except ValueError:
                        # Fallback if file is outside sanctum (should be rare)
                        script_ref = Path(f"/app/{target_file.name}")
                final_cmd_list = self._resolve_command_template(interpreter_cmd, script_ref)

            elif execution_style == "project_context":
                final_cmd_list = interpreter_cmd

            elif execution_style == "stdin_pipe":
                final_cmd_list = interpreter_cmd

            else:
                raise ArtisanHeresy(f"Unknown execution style: {execution_style}")

            # --- MOVEMENT III: THE DOCKER ENCAPSULATION ---
            if strategy == 'docker':
                mount_dir = abs_sanctum
                final_cmd_list = self.docker_engine.forge_run_command(
                    image=docker_image, command=final_cmd_list, volumes={mount_dir: "/app"},
                    env_vars=env, workdir="/app", interactive=True,
                    network="host" if is_debug or self.language == "html" else "bridge"
                )
                process_env = os.environ.copy()  # Docker client needs local env
            else:
                process_env = env

            # Logging the intent
            final_command_str = " ".join(shlex.quote(p) for p in final_cmd_list)
            self.logger.verbose(f"Igniting Process: {final_command_str}")

            stdin_val = None
            if execution_style == "stdin_pipe":
                stdin_val = final_script_block.encode('utf-8')

            # --- MOVEMENT IV: THE LIVING STREAM (POPEN) ---
            process = subprocess.Popen(
                final_cmd_list,
                cwd=str(abs_sanctum),
                env=process_env,
                stdin=subprocess.PIPE if stdin_val else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # [FACULTY 6] Dual-Stream Fusion
                text=False,  # [FACULTY 7] Binary Mode for Encoding Safety
                bufsize=0  # Unbuffered
            )

            if stdin_val:
                process.stdin.write(stdin_val)
                process.stdin.close()

            # [FACULTY 8] The Threaded Siphon
            q = Queue()
            stream_thread = Thread(target=self._stream_output, args=(process.stdout, q))
            stream_thread.daemon = True
            stream_thread.start()

            while True:
                try:
                    # Non-blocking check to keep the loop responsive
                    line = q.get(timeout=0.1)
                    if line is None: break  # End of stream signal

                    # [FACULTY 12] Encoding Healer
                    decoded_line = line.decode('utf-8', errors='replace').rstrip()
                    final_output_list.append(decoded_line)

                    # [FACULTY 9] THE NAKED VOICE (Log without timestamps for UX)
                    # This sends the log to the Daemon/Console immediately.
                    self.logger.info(decoded_line, bare=True)

                except Empty:
                    # Check if process is dead
                    if process.poll() is not None:
                        # Drain remaining queue
                        while not q.empty():
                            l = q.get_nowait()
                            if l:
                                d = l.decode('utf-8', errors='replace').rstrip()
                                final_output_list.append(d)
                                self.logger.info(d, bare=True)
                        break

                    # [FACULTY 5] The Timeout Sentinel
                    if time.monotonic() - start_time > total_timeout:
                        process.kill()
                        was_terminated = True
                        msg = f"\n[TIMEOUT] Rite exceeded {total_timeout}s. The Guardian has severed the link."
                        final_output_list.append(msg)
                        self.logger.error(msg)
                        break

            stream_thread.join(timeout=1.0)
            final_returncode = process.wait()

            # --- MOVEMENT V: THE BROWSER HOOK (LOCAL) ---
            if self.language == "html" and "metadata" in self.recipe and strategy != 'docker':
                url_tmpl = self.recipe["metadata"].get("open_browser", "")
                target_name = Path(edict.command).name if edict.command else "index.html"
                url = url_tmpl.replace("{{script_path.name}}", target_name)
                if url:
                    import webbrowser
                    self.logger.info(f"Opening luminous portal: {url}")
                    webbrowser.open(url)

        except Exception as e:
            raise ArtisanHeresy(f"A catastrophic paradox in the Polyglot Artisan: {e}", line_num=edict.line_num)

        finally:
            # [FACULTY 10] The Zombie Reaper & Cleanup
            if process and process.poll() is None:
                try:
                    process.kill()
                except:
                    pass

            if ephemeral_path and ephemeral_path.exists():
                if "cleanup_commands" in self.recipe and strategy != 'docker':
                    try:
                        for clean_tmpl in self.recipe.get("cleanup_commands", []):
                            clean_cmd = self._resolve_command_template(clean_tmpl, ephemeral_path)
                            subprocess.run(clean_cmd, cwd=str(abs_sanctum), env=env, capture_output=True, timeout=10,
                                           check=False)
                    except:
                        pass
                try:
                    ephemeral_path.unlink()
                except:
                    pass

        duration = time.monotonic() - start_time
        final_output_str = "\n".join(final_output_list)
        # Sanitize null bytes for database storage compatibility
        sanitized_output = self._sanitize_output(final_output_str)

        return Reality(
            output=sanitized_output,
            returncode=final_returncode,
            duration=duration,
            command=final_command_str,
            was_terminated=was_terminated
        )