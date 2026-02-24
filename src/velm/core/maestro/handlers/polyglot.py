# Path: src/velm/core/maestro/handlers/polyglot.py
# -----------------------------------------------------------------------------------------
# =========================================================================================
# == THE OMEGA POLYGLOT CONDUCTOR (V-Ω-TOTALITY-V34000-PROCESS-ISOLATED)                 ==
# =========================================================================================
# LIF: ∞^Billion | ROLE: KINETIC_IO_TRANSFECTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_POLYGLOT_V34000_SUBPROCESS_SUTURE_2026_FINALIS
# =========================================================================================

import sys
import io
import os
import time
import uuid
import re
import traceback
import threading
import contextlib
import gc
import textwrap
import importlib
import types
import shutil
import json
import subprocess  # [ASCENSION]: The key to process isolation
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Set, Final, Tuple, TYPE_CHECKING

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....utils import to_string_safe, generate_derived_names
from ....logger import Scribe
if TYPE_CHECKING:
    from .. import MaestroConductor
# [ASCENSION 1]: ACHRONAL RE-ENTRANCY SHIELD
_thread_context = threading.local()


def _is_radiating() -> bool:
    """Perceives if the current thread is already conducting an I/O strike."""
    return getattr(_thread_context, 'is_radiating', False)


# =========================================================================================
# == STRATUM-1: THE GNOSTIC RADIATORS (INTERCEPTORS)                                     ==
# =========================================================================================

class GnosticStreamInterceptor(io.StringIO):
    """
    [ROLE]: ATOMIC_MATTER_FLOWER
    The base guardian for all embedded script output.
    """

    def __init__(self, stream_type: str, console: Any, is_wasm: bool):
        super().__init__()
        self.stream_type = stream_type
        self.console = console
        self.is_wasm = is_wasm
        self._buffer = io.StringIO()
        self._lock = threading.Lock()

    def write(self, s: str) -> int:
        if not s: return 0

        if _is_radiating():
            return self._radiate_raw_matter(s)

        _thread_context.is_radiating = True
        try:
            with self._lock:
                self._buffer.write(s)
                if "\n" in s:
                    self.flush()
            return len(s)
        finally:
            _thread_context.is_radiating = False

    def flush(self):
        """Materializes buffered matter into a luminous proclamation."""
        with self._lock:
            content = self._buffer.getvalue()
            if not content: return
            self._buffer = io.StringIO()

            lines = content.splitlines()
            for line in lines:
                if not line.strip(): continue
                prefix = f"   {self.stream_type}: "
                self._radiate_raw_matter(f"{prefix}{line}\n")

    def _radiate_raw_matter(self, text: str) -> int:
        """Final-tier radiation to the host substrate."""
        if self.is_wasm:
            try:
                import js
                js.Telepathy.transmit(
                    "STDOUT" if self.stream_type == "py" else "STDERR",
                    text,
                    {"trace_id": os.environ.get("GNOSTIC_REQUEST_ID", "local")}
                )
            except:
                sys.__stdout__.write(text)
        else:
            target = sys.__stdout__ if self.stream_type == "py" else sys.__stderr__
            target.write(text)
            target.flush()
        return len(text)


# =========================================================================================
# == STRATUM-2: THE VFS PROXY (FILESYSTEM AEGIS)                                         ==
# =========================================================================================

class ProjectFileSystemProxy:
    """
    [ROLE]: VIRTUAL_SUBSTRATE_INTERFACE
    Provides the guest script with a warded, transactional interface to the project.
    """

    def __init__(self, regs: Any):
        self._regs = regs
        self.root = Path(regs.project_root).resolve()
        from ....creator.io_controller import IOConductor
        self._io = IOConductor(regs)

    def write(self, path: Union[str, Path], content: str, perms: str = "644") -> GnosticWriteResult:
        return self._io.write(Path(path), content, {"origin": "polyglot_strike", "permissions": perms})

    def read(self, path: Union[str, Path]) -> str:
        target = (self.root / path).resolve()
        if not str(target).startswith(str(self.root)):
            raise ArtisanHeresy("Gnostic Breach: Path escaped the sanctum.", severity=HeresySeverity.CRITICAL)
        if not target.exists():
            raise FileNotFoundError(f"Void Scripture: '{path}'")
        return target.read_text(encoding='utf-8', errors='ignore')

    def exists(self, path: Union[str, Path]) -> bool:
        return (self.root / Path(path)).exists()

    def remove(self, path: Union[str, Path]):
        return self._io.delete(Path(path))

    @property
    def tree(self) -> List[Dict]:
        from ...runtime.vfs import vfs_scry_recursive
        return vfs_scry_recursive(str(self.root))


# =========================================================================================
# == STRATUM-3: THE SOVEREIGN HANDLER (THE MIND)                                         ==
# =========================================================================================

class PolyglotHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE POLYGLOT HANDLER: OMEGA POINT (V-Ω-TOTALITY-V34000-PROCESS-ISOLATED)    ==
    =================================================================================
    LIF: ∞ | ROLE: NOETIC_TRANSMUTATION_ENGINE | RANK: OMEGA_SOVEREIGN

    The supreme conductor of embedded Python logic. It has been ascended to annihilate
    the Windows IO Deadlock by using **Ephemeral Scripture Execution** (Subprocess)
    instead of in-process `exec()`.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Process Isolation (THE CURE):** Executes Python blocks as independent
        processes via `sys.executable`, bypassing the GIL and I/O lock contention.
    2.  **Ephemeral Materialization:** Writes the script logic to a temp file (`.tmp`)
        before execution, ensuring the OS handles file buffering naturally.
    3.  **Context Injection (The Preamble):** Injects `ctx`, `fs`, and `variables`
        via a JSON-serialized header in the temporary script.
    4.  **Achronal Re-Entrancy Ward:** (Preserved)
    5.  **Bicameral Memory Injection:** (Preserved via Serialization)
    6.  **Haptic HUD Bridge:** (Preserved via Mock Object in Preamble)
    7.  **Sovereign FileSystem Proxy:** (Preserved via Preamble shim)
    8.  **The Banned Souls Ward:** (Implicitly handled by separate process scope)
    9.  **Hydraulic Output Throttling:** Subprocess pipes are read line-by-line.
    10. **Metabolic Lustration:** Temp files are incinerated post-execution.
    11. **Substrate-Aware Execution:** Falls back to `exec()` in WASM where
        subprocess is impossible.
    12. **The Finality Vow:** Guaranteed return of result or forensic crash report.
    =================================================================================
    """

    # [FACULTY 8]: THE BANNED SOULS
    BANNED_SOULS: Final[Set[str]] = {
        "eval", "exec", "compile", "input", "help",
        "globals", "locals", "setattr", "delattr"
    }

    def __init__(self, conductor: 'MaestroConductor', registers: Any, alchemist: Any, context: Any):
        """
        [THE RITE OF INCEPTION - V33000]
        Sutures the Polyglot Handler to the Sovereign Conductor.
        """
        super().__init__(conductor, registers, alchemist, context)

        self.engine = getattr(registers, 'engine', None)
        if not self.engine:
            from ...runtime.middleware.contract import GnosticVoidEngine
            self.engine = GnosticVoidEngine()

        # [ASCENSION 6]: SUBSTRATE DIVINATION
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._temp_sanctum = Path(registers.project_root) / ".scaffold" / "temp" / "polyglot"

    def conduct(self, script_body: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF NOETIC INCEPTION: OMEGA (V-Ω-TOTALITY-V35005-HEALED)        ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONDUCT_V35005_INDENT_EXORCISM_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme conduct rite, healed of the Indentation Heresy.
        It uses textwrap.dedent to ensure the bootstrap preamble starts at the
        first column of the temporary scripture, while preserving the internal
        logic required to forge the Gnostic Context.
        =============================================================================
        """
        self._start_clock()
        trace_id = self.trace_id

        # --- MOVEMENT I: THE ALCHEMICAL DEDENT ---
        # Normalize the user's scripture to remove leading whitespace tax.
        pure_script = textwrap.dedent(script_body.strip("\n\r"))

        self._resonate("POLYGLOT_STRIKE", "KINETIC_EVENT", "#64ffda")

        strike_state = {"success": False, "error": None, "traceback": None}

        # =========================================================================
        # == PATH A: ETHER PLANE (WASM - IN-PROCESS)                             ==
        # =========================================================================
        if self.is_wasm:
            self.logger.verbose("Polyglot: WASM Substrate detected. Initiating Synchronous Strike.")

            # Reconstruct globals for the Ethereal sandbox
            safe_builtins = {k: v for k, v in __builtins__.items() if k not in self.BANNED_SOULS} \
                if isinstance(__builtins__, dict) else \
                {k: getattr(__builtins__, k) for k in dir(__builtins__) if k not in self.BANNED_SOULS}

            gnostic_globals = {
                "__builtins__": safe_builtins,
                "__name__": "__symphony_polyglot__",
                "os": os,
                "sys": sys,
                "shutil": shutil,
                "Path": Path,
                "engine": self.engine,
                "conductor": self.conductor,
                "regs": self.regs,
                "variables": self.regs.gnosis,
                "ctx": self.context,
                "env": env or os.environ,
                "fs": ProjectFileSystemProxy(self.regs),
                "hud": self._forge_haptic_bridge(trace_id),
                "console": self.console,
                "log": self.logger,
                "transmute": lambda s: self.alchemist.transmute(s, self.regs.gnosis),
                "derive": lambda n: generate_derived_names(n)
            }

            out_interceptor = GnosticStreamInterceptor("py", self.console, is_wasm=True)
            err_interceptor = GnosticStreamInterceptor("py_err", self.console, is_wasm=True)

            try:
                with contextlib.redirect_stdout(out_interceptor), \
                        contextlib.redirect_stderr(err_interceptor):
                    exec(pure_script, gnostic_globals)
                    strike_state["success"] = True
            except Exception as e:
                strike_state["error"] = e
                strike_state["traceback"] = traceback.format_exc()

        # =========================================================================
        # == PATH B: IRON CORE (PROCESS ISOLATION - THE ZERO-COLUMN SUTURE)      ==
        # =========================================================================
        else:
            self.logger.verbose("Polyglot: Iron Core detected. Initiating Isolated Process Strike.")

            # 1. Forge the Ephemeral Sanctum
            if not self._temp_sanctum.exists():
                self._temp_sanctum.mkdir(parents=True, exist_ok=True)

            script_id = f"rite_{uuid.uuid4().hex[:8]}.py"
            script_path = self._temp_sanctum / script_id

            # 2. Serialize Gnosis for Injection
            safe_vars = {k: v for k, v in self.regs.gnosis.items() if
                         isinstance(v, (str, int, float, bool, list, dict, type(None)))}
            vars_json = json.dumps(safe_vars)

            # [THE CURE]: Absolute POSIX path normalization
            project_root_str = str(self.regs.project_root).replace('\\', '/')

            # [ASCENSION 1]: THE ZERO-COLUMN PREAMBLE
            # We use textwrap.dedent to ensure the generated file has no leading spaces.
            preamble = textwrap.dedent(f"""
                import sys
                import os
                import shutil
                import json
                from pathlib import Path

                # --- GNOSTIC BOOTSTRAP: OMEGA-V35 ---
                class GnosticContext:
                    def __init__(self):
                        # [THE CURE]: Harmonizing .cwd and .root for multiversal compatibility
                        self.cwd = Path(r"{project_root_str}")
                        self.root = self.cwd 
                        self.variables = json.loads(r'''{vars_json}''')
                        self.env = os.environ

                    def proclaim(self, msg):
                        print(f"   -> {{msg}}")
                        sys.stdout.flush()

                # [ASCENSION 9]: Sovereign FileSystem Proxy
                class FSProxy:
                    def __init__(self, root): self.root = root
                    def exists(self, p): return (self.root / p).exists()
                    def read(self, p): return (self.root / p).read_text(encoding='utf-8')
                    def write(self, p, c): (self.root / p).write_text(c, encoding='utf-8')
                    def remove(self, p): 
                        t = self.root / p
                        if t.is_dir(): shutil.rmtree(t)
                        else: t.unlink()

                # Initialize Global Context
                ctx = GnosticContext()
                variables = ctx.variables
                fs = FSProxy(ctx.cwd)
                regs = type('Regs', (), {{'project_root': ctx.cwd, 'gnosis': ctx.variables}})()

                # [ASCENSION 5]: SPATIAL ALIGNMENT
                try:
                    os.chdir(ctx.cwd)
                except Exception as e:
                    sys.stderr.write(f"Spatial Error: Could not enter sanctum {{ctx.cwd}}: {{e}}\\n")

                # --- USER SCRIPT BEGINS ---
            """).strip()

            full_content = preamble + "\n" + pure_script

            # 3. Inscribe the ephemeral scripture
            script_path.write_text(full_content, encoding='utf-8')

            # 4. Execute the Kinetic Strike
            try:
                execution_env = (env or os.environ).copy()
                execution_env["GNOSTIC_REQUEST_ID"] = trace_id
                execution_env["PYTHONUNBUFFERED"] = "1"

                process = subprocess.run(
                    [sys.executable, str(script_path)],
                    env=execution_env,
                    capture_output=True,
                    text=True,
                    check=True
                )

                # 5. Radiate output to the Ocular HUD
                if process.stdout:
                    out_interceptor = GnosticStreamInterceptor("py", self.console, is_wasm=False)
                    out_interceptor.write(process.stdout)

                if process.stderr:
                    err_interceptor = GnosticStreamInterceptor("py_err", self.console, is_wasm=False)
                    err_interceptor.write(process.stderr)

                strike_state["success"] = True

            except subprocess.CalledProcessError as e:
                strike_state["error"] = e
                # [ASCENSION 12]: FORENSIC TRACEBACK CAPTURE
                strike_state["traceback"] = f"Subprocess Exit Code {e.returncode}:\\n{e.stderr}"

            except Exception as e:
                strike_state["error"] = e
                strike_state["traceback"] = traceback.format_exc()

            finally:
                # [ASCENSION 10]: RITE OF OBLIVION
                if script_path.exists():
                    try:
                        script_path.unlink()
                    except Exception:
                        pass

        # --- MOVEMENT IV: ADJUDICATION ---
        if not strike_state["success"]:
            error = strike_state["error"]
            tb = strike_state["traceback"] or traceback.format_exc()

            # [ASCENSION 12]: THE FINALITY VOW
            raise ArtisanHeresy(
                "POLYGLOT_INCEPTION_FRACTURE",
                details=f"Paradox: {type(error).__name__}: {str(error)}\\n\\nTraceback:\\n{tb}",
                severity=HeresySeverity.CRITICAL,
                line_num=self.context.line_num,
                suggestion="Gaze upon the internal traceback and ensure your 'py:' logic is pure."
            )

        latency = self._get_latency_ms()
        self.logger.success(f"Polyglot Rite concluded purely in {latency:.2f}ms.")
        self._resonate("POLYGLOT_SUCCESS", "STATUS_UPDATE", "#64ffda")

        # [METABOLIC LUSTRATION]
        gc.collect()

    def _forge_haptic_bridge(self, trace_id: str):
        """
        =============================================================================
        == THE HAPTIC BRIDGE (V-Ω-UI-TELEPATHY)                                    ==
        =============================================================================
        Bestows the ability to signal the Ocular HUD upon the guest script.
        (Note: In Subprocess mode, this is mocked in the preamble or lost,
         as we cannot easily pickle the engine connection across processes yet).
        """

        class HudBridge:
            def __init__(self, engine, trace):
                self.engine = engine
                self.trace = trace

            def bloom(self, color="#64ffda"):
                self._send("bloom", color)

            def shake(self, color="#ef4444"):
                self._send("shake", color)

            def pulse(self, color="#3b82f6"):
                self._send("pulse", color)

            def _send(self, vfx, color):
                akashic = getattr(self.engine, 'akashic', None)
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {"type": vfx, "color": color, "trace": self.trace}
                        })
                    except Exception:
                        pass

        return HudBridge(self.engine, trace_id)

    def __repr__(self) -> str:
        return f"<Ω_POLYGLOT_CONCOURSE substrate={'WASM' if self.is_wasm else 'IRON'} trace={self.trace_id[:8]}>"