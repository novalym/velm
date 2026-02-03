# Path: scaffold/artisans/shadow_clone/governor.py
# ------------------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@REALITY_GOVERNOR_V16.0_ASCENDED
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ------------------------------------------------

import os
import sys
import time
import shutil
import subprocess
import threading
import psutil
import signal
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

from ...logger import Scribe

Logger = Scribe("RealityGovernor")


class RealityGovernor:
    """
    =============================================================================
    == THE REALITY GOVERNOR (V-Ω-KINETIC-SOVEREIGNTY-V16.0-ASCENDED)           ==
    =============================================================================
    Orchestrates the raw physics of process inception, telemetry, and execution.
    Annihilates "WinError 2" via the Omni-Binary Resolver and optimizes child
    kinetics through Priority Governance.
    =============================================================================
    """

    def __init__(self, sid: str):
        self.sid = sid
        self._process: Optional[subprocess.Popen] = None
        self._stop_event = threading.Event()

    def _resolve_binary(self, cmd: str) -> str:
        """
        [ASCENSION 1]: THE OMNI-BINARY RESOLVER.
        Hunts for the true executable path. Crucial for Windows where 'npm' 
        must be resolved to 'npm.cmd' or 'npm.exe'.
        """
        # 1. Direct path check
        if os.path.isabs(cmd) and os.path.exists(cmd):
            return cmd

        # 2. OS scry via shutil
        path = shutil.which(cmd)
        if path:
            return path

        # 3. Windows Fallback: Scry common extensions
        if os.name == 'nt':
            for ext in ['.cmd', '.exe', '.bat']:
                candidate = shutil.which(cmd + ext)
                if candidate:
                    return candidate

        return cmd

    def ignite(self, cwd: Path, cmd_list: List[str], dport: Optional[int], aura: str) -> Tuple[int, Path, Path]:
        """
        [ASCENSION 2 & 3]: AURA-AWARE IGNITION & ENVIRONMENT GRAFTING.
        Materializes the process within a warded sandbox.
        """
        # [THE FIX]: Resolve the primary binary before spawning
        original_binary = cmd_list[0]
        if original_binary not in (sys.executable, 'python', 'python3'):
            cmd_list[0] = self._resolve_binary(original_binary)

        # [ASCENSION 9]: Binary Shimming 2.0
        if cmd_list[0] in ('python', 'python3', 'python.exe'):
            cmd_list[0] = sys.executable

        # [ASCENSION 7]: Constitutional Debugging
        if dport:
            cmd_list = [sys.executable, "-m", "debugpy", "--listen", f"127.0.0.1:{dport}"] + cmd_list

        # --- [ASCENSION 5]: ATOMIC LOG INCEPTION ---
        log_dir = cwd / ".logs"
        log_dir.mkdir(exist_ok=True)
        stdout_f, stderr_f = log_dir / "stdout.log", log_dir / "stderr.log"

        # Faculty 3: Atomic Truncation
        stdout_f.write_text("", encoding='utf-8')
        stderr_f.write_text("", encoding='utf-8')

        # [ASCENSION 33]: Buffered IO for High-Throughput Telemetry
        out_h = open(stdout_f, "w", encoding='utf-8', buffering=1)
        err_h = open(stderr_f, "w", encoding='utf-8', buffering=1)

        # --- [ASCENSION 4]: KINETIC PRIORITY & SPAWN ---
        creation_flags = 0
        if os.name == 'nt':
            # Faculty 5: Signal Propagation Group
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | 0x00004000  # BELOW_NORMAL_PRIORITY_CLASS

        # [ASCENSION 2]: Lattice Path Injection
        env = os.environ.copy()
        paths = [
            str(cwd / "node_modules" / ".bin"),
            str(cwd / ".venv" / ("Scripts" if os.name == 'nt' else "bin")),
            env.get("PATH", "")
        ]
        env["PATH"] = os.pathsep.join(filter(None, paths))
        env.update({
            "PORT": os.environ.get("PORT", "5173"),
            "PYTHONUNBUFFERED": "1",
            "SCAFFOLD_SHADOW_ID": self.sid,
            "FORCE_COLOR": "1"
        })

        Logger.info(f"[{self.sid}] Igniting {aura.upper()} Matter: {' '.join(cmd_list)}")
        Logger.verbose(f"[{self.sid}] Binary Scry Result: {original_binary} -> {cmd_list[0]}")

        try:
            self._process = subprocess.Popen(
                cmd_list,
                cwd=cwd,
                stdout=out_h,
                stderr=err_h,
                env=env,
                start_new_session=(os.name != 'nt'),  # Faculty 11: Sovereignty
                creationflags=creation_flags,
                shell=False  # [THE CURE]: Resolved binary removes need for shell=True
            )
        except OSError as e:
            out_h.close()
            err_h.close()
            # Faculty 10: Forensic Autopsy
            raise RuntimeError(f"Ignition Fracture (OS Error): {e} - Target: {cmd_list[0]}")

        # [ASCENSION 15]: RESOURCE CONTAINMENT FIELD
        try:
            p = psutil.Process(self._process.pid)
            if os.name != 'nt':
                p.nice(10)  # Nice level
            else:
                p.ionice(psutil.IOPRIO_VERYLOW)  # I/O Priority
        except:
            pass

        # --- [ASCENSION 5 & 12]: TELEMETRY LINK INCEPTION ---
        self._awaken_harvesters(stdout_f, stderr_f)

        # --- [ASCENSION 6 & 21]: THE CRADLE VIGIL ---
        for i in range(10):  # 5 seconds of vigilance
            if self._process.poll() is not None:
                break
            time.sleep(0.5)

        if self._process.poll() is not None:
            out_h.close()
            err_h.close()
            # Faculty 10: Exit Code Prophet
            self._perform_autopsy(stderr_f, self._process.returncode)
            raise RuntimeError(f"Ignition Fracture in {self.sid} (Exited with code {self._process.returncode})")

        return self._process.pid, stdout_f, stderr_f

    def _awaken_harvesters(self, out: Path, err: Path):
        """[ASCENSION 16]: Neural Link Stream Multiplexing."""
        threading.Thread(target=self._tail, args=(out, "stdout"), daemon=True).start()
        threading.Thread(target=self._tail, args=(err, "stderr"), daemon=True).start()

    def _tail(self, path: Path, stream_type: str):
        """[ASCENSION 9]: Adaptive Buffer Tuning."""
        while not path.exists() and (not self._process or self._process.poll() is None):
            time.sleep(0.2)
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        # Faculty 7: Adaptive length cap (1024 chars)
                        safe_line = line.strip()[:1024]
                        # Faculty 12: Merkle Traceback Bridge
                        Logger.info(safe_line, extra={"tags": ["NEURAL_LINK"], "data": {
                            "type": "shadow:log",
                            "shadow_id": self.sid,
                            "stream": stream_type,
                            "message": safe_line,
                            "timestamp": time.time()
                        }})
                    else:
                        if self._process and self._process.poll() is not None:
                            break
                        time.sleep(0.2)
        except:
            pass

    def _perform_autopsy(self, err_path: Path, code: int):
        """[ASCENSION 10]: Forensic Autopsy Engine."""
        evidence = "VOID_LOG"
        try:
            # Capture last 8KB of error data
            with open(err_path, 'r', encoding='utf-8', errors='replace') as f:
                evidence = f.read()[-8192:]
        except:
            pass

        # Exit Code Translation
        translation = "GENERIC_FRACTURE"
        if code == 127:
            translation = "FILE_NOT_FOUND_HERESY"
        elif code == 126:
            translation = "PERMISSION_DENIED_WARD"
        elif code == -9 or code == 137:
            translation = "OOM_KILL_RECLAMATION"

        Logger.error(f"[{self.sid}] Fracture Detected ({translation}):\n{evidence}")

    def scythe(self, pid: int):
        """
        [ASCENSION 8]: RECURSIVE SCYTHE ENGINE.
        Annihilates process trees to prevent orphaned matter.
        """
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            parent.terminate()

            # Wait for dissolution (Max 3s)
            gone, alive = psutil.wait_procs(children + [parent], timeout=3)
            for survivor in alive:
                try:
                    survivor.kill()  # Ultimate force
                except:
                    pass
            Logger.success(f"[{self.sid}] Scythe concluded. Matter dissolved.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

