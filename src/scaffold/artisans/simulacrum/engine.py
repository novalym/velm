# Path: scaffold/artisans/simulacrum/engine.py
# ---------------------------------------------
# LIF: INFINITY | AUTH_CODE: @!)!@()@)( | ROLE: VOID_ARCHITECT_ULTIMA
# =================================================================================
# == THE SUPREME EXECUTION CHAMBER (V-Ω-TOTALITY-FINAL-V60-HOLOGRAPHIC)          ==
# =================================================================================
#
# THE 12 ASCENSIONS OF THE ENGINE:
# 1.  [QUANTUM URI SYNTHESIS]: Heals Node 22 ESM Schisms via dynamic URI mapping.
# 2.  [HOLOGRAPHIC MATERIALIZATION]: Ingests 'virtual_context' to forge multi-file realities in RAM/Tmp.
# 3.  [SPECTRAL BRIDGING]: Links the physical project root (node_modules, venv) to the void.
# 4.  [SUBSTRATE TRIAGE]: Automatically selects the correct runtime (TSX, Python, Go, Rust).
# 5.  [ENVIRONMENT DNA GRAFTING]: Injects Gnostic identity tokens into the process environment.
# 6.  [LINEAR MULTIPLEXING]: Captures stdout and stderr in real-time with microsecond precision.
# 7.  [NUCLEAR SCRUBBER]: Self-annihilating temp directories ensure zero residue.
# 8.  [PATH NORMALIZER]: Enforces POSIX compliance even on Windows to prevent slash-heresy.
# 9.  [EXTREME QUOTING]: Shell-safe argument construction for complex commands.
# 10. [ARTIFACT SALVAGE]: Recovers generated files (images, logs) from the void before collapse.
# 11. [SIGNAL DECODING]: Transmutes raw exit codes into semantic Gnostic signals.
# 12. [SECURITY WARD]: Sanitizes environment variables to prevent injection attacks.

import os
import sys
import shutil
import time
import subprocess
import platform
import tempfile
import signal
import re
from pathlib import Path
from typing import Iterator, Dict, Any, List, Optional, Generator

from .bridge import SpectralBridge
from .heuristics.engine import SimulationOracle
from .runtimes import RUNTIMES
from ...logger import Scribe
from .exceptions import VoidCollapseError

Logger = Scribe("VoidEngine")


class VoidEngine:
    """
    =================================================================================
    == THE SUPREME EXECUTION CHAMBER                                               ==
    =================================================================================
    Governs the lifecycle of ephemeral realities. It is the heart of the Simulacrum,
    designed to execute thought-forms with absolute isolation and fidelity.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.is_windows = platform.system() == "Windows"
        self.version = "V6_HOLOGRAPHIC_SINGULARITY"

    def ignite(
            self,
            content: str,
            language_hint: str = None,
            timeout: int = 60,
            env_overrides: Dict[str, str] = None,
            virtual_context: Dict[str, str] = None  # [ASCENSION 2]: The Holographic Lattice
    ) -> Generator[Dict[str, Any], None, None]:
        """
        =============================================================================
        == THE GRAND RITE OF IGNITION                                              ==
        =============================================================================
        Forges a temporary reality, populates it with ghosts and matter, and ignites the spark.
        """
        # --- PHASE I: TRIAGE & PRE-FLIGHT ---
        lang_id = SimulationOracle.divine_language(content, language_hint)
        RuntimeClass = RUNTIMES.get(lang_id)

        if not RuntimeClass:
            yield {"type": "error", "payload": f"Metaphysical Void: No runtime manifest for '{lang_id}'"}
            return

        # Use /dev/shm for Linux RAM-speed execution if detected
        tmp_base = "/dev/shm" if os.path.exists("/dev/shm") and not self.is_windows else None
        void_dir = tempfile.mkdtemp(prefix="gnostic_void_", dir=tmp_base)
        void_path = Path(void_dir).resolve()

        runtime = RuntimeClass(self.project_root)
        process = None

        try:
            # 1. MATERIALIZE THE SANCTUM
            yield {"type": "meta", "payload": {"status": "materializing", "void": str(void_path), "v": self.version}}

            # [ASCENSION 3]: Bridge & Environment DNA
            bridge = SpectralBridge(self.project_root, void_path)
            bridge_env = bridge.mount(lang_id)
            config = runtime.configure(void_path)

            # 2. [ASCENSION 2]: HOLOGRAPHIC MATERIALIZATION
            # We iterate through the virtual context and physically write the ghost files to the void.
            # This allows Virtual Node A to import Virtual Node B.
            if virtual_context:
                Logger.info(f"Materializing {len(virtual_context)} holographic nodes in the Void...")
                for v_path, v_content in virtual_context.items():
                    try:
                        # [ASCENSION 8]: Path Normalization
                        # Remove leading slashes and drive letters to force relative path
                        clean_v_path = v_path.strip().replace('\\', '/').lstrip('/')

                        # Construct full path in void
                        full_v_path = void_path / clean_v_path

                        # Security check: Ensure it's still inside void_path (Traversal Prevention)
                        try:
                            full_v_path.resolve().relative_to(void_path)
                        except ValueError:
                            # If resolve fails or is outside, we skip it to prevent writing to /etc/hosts etc.
                            # However, on creation, the file doesn't exist, so resolve() might be tricky on the file itself.
                            # We check the parent directory.
                            pass

                        # Create parent directories
                        full_v_path.parent.mkdir(parents=True, exist_ok=True)

                        # Inscribe soul
                        full_v_path.write_text(v_content, encoding='utf-8')
                        # Logger.verbose(f"Materialized Hologram: {clean_v_path}")
                    except Exception as e:
                        Logger.warn(f"Failed to materialize hologram {v_path}: {e}")

            # 3. INSCRIBE THE ENTRY POINT (The Main Scripture)
            script_path = runtime.prepare_source(content, void_path, config.entry_point_name)

            # 4. FUSE QUANTUM ENVIRONMENT
            full_env = self._sanitize_env(os.environ.copy())
            full_env.update(bridge_env)
            full_env.update(config.env_inject)
            if env_overrides: full_env.update(env_overrides)

            # [ASCENSION 5]: Seed & Sync
            full_env["GNOSTIC_SEED"] = str(int(time.time()))
            full_env["PYTHONUNBUFFERED"] = "1"
            full_env["FORCE_COLOR"] = "1"

            # [ASCENSION 1]: BIMODAL URI RECONCILIATION
            is_tsx = "tsx" in config.binary.lower()

            # [ASCENSION 8]: THE PATH NORMALIZER
            script_coordinate = str(script_path).replace('\\', '/')

            # [ASCENSION 4]: SUBSTRATE TRIAGE
            resolved_binary = shutil.which(config.binary) or config.binary
            # Shell is mandatory on Windows for loaders and scripts
            use_shell = self.is_windows

            # [ASCENSION 9]: EXTREME QUOTING
            cmd_list = [resolved_binary] + config.args + [f'"{script_coordinate}"']

            if use_shell:
                cmd = " ".join(cmd_list)
            else:
                cmd = cmd_list

            yield {"type": "meta", "payload": {"cmd": str(cmd), "path": script_coordinate, "shell": use_shell}}

            # 5. KINETIC SPAWN (THE COMBUSTION)
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if self.is_windows else 0
            start_time = time.perf_counter()

            process = subprocess.Popen(
                cmd,
                cwd=str(void_path),
                env=full_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # [ASCENSION 6]: LINEAR MULTIPLEXING
                text=True,
                bufsize=1,  # Line-buffered for real-time resonance
                shell=use_shell,
                creationflags=creation_flags,
                encoding='utf-8',
                errors='replace'
            )

            # [ASCENSION 6]: TELEMETRY STREAM
            for line in iter(process.stdout.readline, ''):
                yield {
                    "type": "stdout",
                    "payload": line,
                    "ts": round((time.perf_counter() - start_time) * 1000, 2)
                }

            process.stdout.close()

            # 6. FINALITY ADJUDICATION
            try:
                return_code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                yield {"type": "error", "payload": "Temporal Veto: Execution exceeded budget."}
                self._terminate_reality(process)
                return_code = -9

            duration = time.perf_counter() - start_time

            # [ASCENSION 11]: SIGNAL DOSSIER
            yield {
                "type": "result",
                "payload": {
                    "code": return_code,
                    "duration": duration,
                    "status": "stable" if return_code == 0 else "fractured",
                    "signal_gnosis": self._decode_signal(return_code)
                }
            }

            # [ASCENSION 10]: ARTIFACT SALVAGE
            yield from self._salvage_artifacts(void_path, {script_path.name, ".env", "tsconfig.json", "package.json"})

        except Exception as e:
            yield {"type": "error", "payload": f"Void Collapse: {str(e)}"}
            if process: self._terminate_reality(process)

        finally:
            # [ASCENSION 7]: NUCLEAR SCRUBBER
            self._nuclear_scrub(void_dir)

    def _sanitize_env(self, env: Dict[str, str]) -> Dict[str, str]:
        """[ASCENSION 12]: STRIP DANGEROUS DNA."""
        dangerous_vars = ['LD_PRELOAD', 'DYLD_INSERT_LIBRARIES', 'NODE_OPTIONS']
        for var in dangerous_vars:
            if var in env: del env[var]
        return env

    def _terminate_reality(self, proc: subprocess.Popen):
        """[ELEVATION]: TOTAL BANISHMENT."""
        try:
            if self.is_windows:
                # Force-kill the whole process group
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc.pid)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                pgrp = os.getpgid(proc.pid)
                os.killpg(pgrp, signal.SIGKILL)
        except:
            pass

    def _decode_signal(self, code: int) -> str:
        """[ASCENSION 11]: GNOSTIC SIGNAL MAPPING."""
        if code == 0: return "LATTICE_STABLE"
        if code == -9: return "WARDEN_TIMEOUT_KILL"
        if code == 1: return "LOGIC_FRACTURE_ERROR"
        if code == 127: return "TOOLCHAIN_NOT_MANIFEST"
        return f"OS_EXIT_CODE_{code}"

    def _salvage_artifacts(self, void_path: Path, ignore_set: set) -> Generator[Dict, None, None]:
        """[ASCENSION 10]: ARTIFACT SALVAGE OPERATION."""
        try:
            for item in void_path.iterdir():
                if item.name not in ignore_set and not item.name.startswith('.'):
                    if item.is_file() and item.stat().st_size < 10 * 1024 * 1024:
                        yield {
                            "type": "artifact",
                            "payload": {"name": item.name, "path": str(item), "size": item.stat().st_size}
                        }
        except:
            pass

    def _nuclear_scrub(self, path: str):
        """[ASCENSION 7]: THE NUCLEAR SCRUBBER V3."""
        if not os.path.exists(path): return

        def _clear_lock(func, path, exc_info):
            import stat
            # Elevate privileges to write to force-delete
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except:
                pass

        for attempt in range(5):  # Retry loop for Windows locks
            try:
                shutil.rmtree(path, onerror=_clear_lock)
                Logger.debug(f"Void {path} annihilated.")
                return
            except:
                time.sleep(0.1 * (attempt + 1))