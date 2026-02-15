# Path: scaffold/artisans/shadow_clone/governor.py
# =========================================================================================
# == THE REALITY GOVERNOR: OMEGA TOTALITY (V-Ω-TOTALITY-V20000.16-ISOMORPHIC)            ==
# =========================================================================================
# LIF: ∞ | ROLE: KINETIC_LIFECYCLE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GOVERNOR_V20000_SENSORY_SUTURE_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import shutil
import subprocess
import threading
import signal
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Final

# [ASCENSION 1]: SURGICAL SENSORY GUARD
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("RealityGovernor")


class RealityGovernor:
    """
    =================================================================================
    == THE REALITY GOVERNOR (V-Ω-TOTALITY)                                         ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME

    Orchestrates the materialization and management of parallel process realities.
    Hardened for Isomorphic resonance across IRON (Native) and ETHER (WASM).
    """

    def __init__(self, sid: str, engine: Optional[Any] = None):
        """[THE RITE OF INCEPTION]"""
        self.sid = sid
        self.engine = engine
        self._process: Optional[subprocess.Popen] = None
        self._stop_event = threading.Event()
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or not PSUTIL_AVAILABLE

    def _resolve_binary(self, cmd: str) -> str:
        """
        [ASCENSION 2]: THE OMNI-BINARY RESOLVER.
        Annihilates WinError 2 by scrying the host substrate for the true executable locus.
        """
        # 1. Absolute Gaze
        if os.path.isabs(cmd) and os.path.exists(cmd):
            return cmd

        # 2. Python Environment Suture
        if cmd in ('python', 'python3', 'python.exe'):
            return sys.executable

        # 3. OS Path Scrying
        found = shutil.which(cmd)
        if found:
            return found

        # 4. Windows Extension Triage
        if os.name == 'nt':
            for ext in ['.cmd', '.exe', '.bat']:
                candidate = shutil.which(f"{cmd}{ext}")
                if candidate: return candidate

        return cmd

    def ignite(self, cwd: Path, cmd_list: List[str], dport: Optional[int], aura: str) -> Tuple[int, Path, Path]:
        """
        =============================================================================
        == THE RITE OF KINETIC IGNITION (V-Ω-STRIKE-RESONANT)                      ==
        =============================================================================
        Materializes a new reality within a warded sandbox.
        """
        # --- MOVEMENT I: BINARY PURIFICATION ---
        original_bin = cmd_list[0]
        cmd_list[0] = self._resolve_binary(original_bin)

        # [ASCENSION 11]: DEBUGGER INJECTION
        if dport:
            cmd_list = [sys.executable, "-m", "debugpy", "--listen", f"127.0.0.1:{dport}"] + cmd_list

        # --- MOVEMENT II: ATOMIC LOG MATERIALIZATION ---
        # [ASCENSION 5]: Atomic Inception of the Ocular Logs
        log_dir = cwd / ".logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        stdout_f, stderr_f = log_dir / "stdout.log", log_dir / "stderr.log"

        # Wipe previous souls if they exist
        for f in (stdout_f, stderr_f):
            f.write_text("", encoding='utf-8')

        # [ASCENSION 33]: Hydraulic Buffered IO
        out_h = open(stdout_f, "w", encoding='utf-8', buffering=1)
        err_h = open(stderr_f, "w", encoding='utf-8', buffering=1)

        # --- MOVEMENT III: DNA GRAFTING (ENVIRONMENT) ---
        # [ASCENSION 3 & 8]: Lattice Path Suture
        env = os.environ.copy()

        # Suture bin paths for major toolchains
        bin_paths = [
            str(cwd / "node_modules" / ".bin"),
            str(cwd / ".venv" / ("Scripts" if os.name == 'nt' else "bin")),
            env.get("PATH", "")
        ]
        env["PATH"] = os.pathsep.join(filter(None, bin_paths))

        # [ASCENSION 7]: Trace Identity Suture
        env.update({
            "PYTHONUNBUFFERED": "1",
            "SCAFFOLD_SHADOW_ID": self.sid,
            "SCAFFOLD_TRACE_ID": getattr(self, "trace_id", f"tr-cln-{self.sid[:4]}"),
            "FORCE_COLOR": "1"
        })

        # --- MOVEMENT IV: KINETIC SPAWN ---
        creation_flags = 0
        if os.name == 'nt' and not self.is_wasm:
            # [ASCENSION 4]: Windows Priority Inversion
            # CREATE_NEW_PROCESS_GROUP (0x0200) | BELOW_NORMAL_PRIORITY_CLASS (0x4000)
            creation_flags = 0x00000200 | 0x00004000

        Logger.info(f"[{self.sid}] Igniting {aura.upper()} Reality: {' '.join(cmd_list)}")

        try:
            self._process = subprocess.Popen(
                cmd_list,
                cwd=str(cwd),
                stdout=out_h,
                stderr=err_h,
                env=env,
                # [ASCENSION 2]: Sovereign Sessioning
                start_new_session=(os.name != 'nt' and not self.is_wasm),
                creationflags=creation_flags,
                shell=False  # Binary resolution makes shell=True an unnecessary risk
            )
        except OSError as e:
            out_h.close()
            err_h.close()
            raise ArtisanHeresy(
                f"Ignition Fracture: OS was unable to forge process soul.",
                severity=HeresySeverity.CRITICAL,
                details=f"Binary: {cmd_list[0]} | Error: {str(e)}",
                suggestion="Verify the executable path and filesystem permissions."
            )

        # --- MOVEMENT V: METABOLIC CONTAINMENT ---
        # [ASCENSION 4 & 15]: Substrate-Aware Nice-ness
        if PSUTIL_AVAILABLE and not self.is_wasm:
            try:
                p = psutil.Process(self._process.pid)
                if os.name != 'nt':
                    p.nice(10)  # Lower priority in the scheduler
                else:
                    # I/O priority lustration
                    p.ionice(psutil.IOPRIO_VERYLOW)
            except:
                pass

        # --- MOVEMENT VI: TELEMETRY HARVESTING ---
        # [ASCENSION 12]: Scribe Thread Awakening
        self._awaken_harvesters(stdout_f, stderr_f)

        # --- MOVEMENT VII: THE CRADLE VIGIL ---
        # [ASCENSION 6]: Poll for early-onset fracture
        for _ in range(10):  # 5 seconds of intensive scrying
            if self._process.poll() is not None: break
            time.sleep(0.5)

        if self._process.poll() is not None:
            out_h.close()
            err_h.close()
            # [ASCENSION 9]: Forensic Autopsy on stillborn process
            self._perform_autopsy(stderr_f, self._process.returncode)
            raise ArtisanHeresy(
                f"Reality Fractured: Shadow Clone {self.sid[:8]} died in the cradle.",
                severity=HeresySeverity.CRITICAL,
                details=f"Exit Code: {self._process.returncode} | Context: {aura}"
            )

        return self._process.pid, stdout_f, stderr_f

    def _awaken_harvesters(self, out: Path, err: Path):
        """[ASCENSION 10]: Neural Link Multiplexing. Radiates logs to HUD."""
        threading.Thread(target=self._tail, args=(out, "stdout"), name=f"Scribe-Out-{self.sid[:4]}",
                         daemon=True).start()
        threading.Thread(target=self._tail, args=(err, "stderr"), name=f"Scribe-Err-{self.sid[:4]}",
                         daemon=True).start()

    def _tail(self, path: Path, stream_type: str):
        """[ASCENSION 5]: The Persistent Scribe Loop."""
        while not path.exists() and (not self._process or self._process.poll() is None):
            time.sleep(0.2)

        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                # Move to the end to only capture new matter
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        clean_line = line.strip()
                        if not clean_line: continue

                        # [ASCENSION 10]: RADIATE TO AKASHIC HUD
                        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
                            try:
                                self.engine.akashic.broadcast({
                                    "method": "novalym/stream_log",
                                    "params": {
                                        "source": f"SHADOW:{self.sid[:8]}",
                                        "stream": stream_type,
                                        "content": clean_line,
                                        "timestamp": time.time()
                                    }
                                })
                            except:
                                pass

                        # Internal Chronicle
                        Logger.verbose(f"[{self.sid[:4]}:{stream_type}] {clean_line[:100]}")
                    else:
                        if self._process and self._process.poll() is not None:
                            break
                        time.sleep(0.2)
        except Exception:
            pass

    def scythe(self, pid: int):
        """
        =============================================================================
        == THE RECURSIVE SCYTHE (V-Ω-SOUL-REAPER)                                  ==
        =============================================================================
        [ASCENSION 8]: Deep-tissue reaping of orphaned process matter.
        """
        try:
            if PSUTIL_AVAILABLE:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)

                # Soft Banish (TERM)
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                parent.terminate()

                # Wait for dissolution (3s cooling)
                _, alive = psutil.wait_procs(children + [parent], timeout=3)

                # Hard Banish (KILL)
                for survivor in alive:
                    try:
                        survivor.kill()
                    except:
                        pass
            else:
                # [WASM/LEGACY]: Signal-based group annihilation
                if os.name != 'nt':
                    try:
                        os.killpg(os.getpgid(pid), signal.SIGKILL)
                    except:
                        pass
                else:
                    # Windows minimal fallback
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)],
                                   capture_output=True, check=False)

            Logger.success(f"[{self.sid[:8]}] Scythe concluded. Reality dissolved.")
        except Exception as e:
            Logger.debug(f"Scythe friction: {e}")

    def _perform_autopsy(self, err_path: Path, code: int):
        """[ASCENSION 9]: Forensic Tomography of Process Failure."""
        evidence = "VOID_LOG"
        try:
            if err_path.exists():
                with open(err_path, 'r', encoding='utf-8', errors='replace') as f:
                    evidence = f.read()[-4096:]  # Last 4KB of soul-fragments
        except:
            pass

        # Socratic Triage
        diagnosis = "GENERIC_FRACTURE"
        if code == 127:
            diagnosis = "ARTISAN_UNMANIFEST_HERESY"
        elif code == 126:
            diagnosis = "SANCTUM_PERMISSION_WARD"
        elif code in (-9, 137):
            diagnosis = "METABOLIC_OOM_RECLAMATION"

        Logger.error(f"[{self.sid[:8]}] Forensic Report ({diagnosis}):\n[dim]{evidence}[/]")