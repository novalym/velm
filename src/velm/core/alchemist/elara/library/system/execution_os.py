# Path: core/alchemist/elara/library/system_rites/execution_os.py
# ---------------------------------------------------------------

import subprocess
import os
import platform
import sys
import re
from typing import Any, Optional
from ..registry import register_rite
from ......logger import Scribe
from .legacy_text_suture import SystemAlchemist

Logger = Scribe("SystemRites:Execution")

@register_rite("shell")
def execute_shell(value: Any, command: Optional[str] = None, timeout: int = 5, allow_fail: bool = True, **kwargs) -> str:
    """[THE MASTER CURE]: Executes shell edicts with automated Substrate-Aware Triage."""
    raw_cmd = str(command if command else value).strip()
    if not raw_cmd: return ""

    is_windows = platform.system() == "Windows"
    if is_windows:
        grep_match = re.match(r'^grep\s+(?:-i\s+)?["\']?(.*?)["\']?\s+(.*)$', raw_cmd, re.I)
        if grep_match: return SystemAlchemist.emulate_grep(grep_match.group(1), grep_match.group(2))
        if raw_cmd.startswith("ls"):
            target = raw_cmd[2:].strip() or "."
            return SystemAlchemist.emulate_ls(target)

    if "velm" in raw_cmd and "transmute" in raw_cmd: return "/* RECURSION_WARDED */"

    try:
        env = os.environ.copy()
        env["SCAFFOLD_KINETIC_STRIKE"] = "1"
        res = subprocess.run(raw_cmd, shell=True, capture_output=True, text=True, timeout=int(timeout), env=env, encoding='utf-8', errors='replace')
        if res.returncode != 0:
            if not allow_fail: Logger.error(f"Shell Rite Fractured (Code {res.returncode}): {res.stderr[:100]}")
            return ""
        output = res.stdout.strip()
        output = re.sub(r'sk_live_[a-zA-Z0-9]{24}', '[REDACTED_SECRET]', output)
        output = re.sub(r'ghp_[a-zA-Z0-9]{36}', '[REDACTED_TOKEN]', output)
        return output
    except subprocess.TimeoutExpired:
        Logger.warn(f"Metabolic Timeout: Shell strike exceeded {timeout}s.")
        return "/* TIMEOUT */"
    except Exception as e:
        Logger.debug(f"Substrate Strike Error: {e}")
        return ""

@register_rite("shell_daemon")
@register_rite("daemonize")
def daemonize_rite(value: Any) -> int:
    """[ASCENSION 65]: Daemon-Spawning Matrix. Returns PID."""
    if os.environ.get("SCAFFOLD_ENV") == "WASM": return -1
    cmd = str(value)
    try:
        if os.name == 'posix':
            # Detach from parent process group
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)
        else:
            # Windows detached creation
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        return proc.pid
    except Exception as e:
        Logger.error(f"Daemonize fracture: {e}")
        return -1

@register_rite("kill_process")
def kill_process_rite(value: Any) -> bool:
    """[ASCENSION 73 & 87]: Process Exorcist."""
    try:
        target = int(value)
        import psutil
        parent = psutil.Process(target)
        # Kill all children first (Process Tree Annihilation)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        return True
    except ValueError:
        # It's a string name (e.g. "celery")
        try:
            import psutil
            killed = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if str(value).lower() in (proc.info['name'] or "").lower() or \
                   (proc.info['cmdline'] and str(value).lower() in " ".join(proc.info['cmdline']).lower()):
                    proc.kill()
                    killed = True
            return killed
        except: return False
    except Exception:
        return False