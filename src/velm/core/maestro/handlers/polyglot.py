# Path: src/velm/core/maestro/handlers/polyglot.py
# ------------------------------------------------
# LIF: ∞ | ROLE: NOETIC_TRANSMUTATION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_POLYGLOT_V800_WASM_SUTURE_2026_FINALIS

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
import queue
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Set, Final

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....utils import to_string_safe, generate_derived_names
from ....logger import Scribe

Logger = Scribe("PolyglotConcourse")


# =========================================================================================
# == STRATUM-1: THE QUEUED RADIATOR (DECOUPLED I/O - NATIVE)                             ==
# =========================================================================================

class QueuedStreamInterceptor(io.StringIO):
    """
    [ROLE]: ASYNCHRONOUS_MATTER_FLOWER (NATIVE)
    Pushes lines into an atomic queue for the main thread to handle.
    """

    def __init__(self, stream_type: str, output_queue: queue.Queue):
        super().__init__()
        self.stream_type = stream_type
        self.output_queue = output_queue

    def write(self, s: str):
        if not s: return 0
        clean_s = s.rstrip('\r\n')
        if clean_s:
            for line in clean_s.splitlines():
                if line.strip():
                    self.output_queue.put((self.stream_type, line))
        return super().write(s)


# =========================================================================================
# == STRATUM-1.5: THE DIRECT RADIATOR (SYNCHRONOUS I/O - WASM)                           ==
# =========================================================================================

class DirectStreamInterceptor(io.StringIO):
    """
    [ROLE]: SYNCHRONOUS_MATTER_FLOWER (WASM)
    Directly radiates lines to the Console, bypassing the thread queue.
    """

    def __init__(self, stream_type: str, console: Any):
        super().__init__()
        self.stream_type = stream_type
        self.console = console

    def write(self, s: str):
        if not s: return 0
        clean_s = s.rstrip('\r\n')
        if clean_s:
            for line in clean_s.splitlines():
                if line.strip():
                    color = "cyan" if self.stream_type == "py" else "bold red"
                    # Direct strike to the console
                    self.console.print(f"[{color}]   {self.stream_type}: [/]{line}")
        return super().write(s)


# =========================================================================================
# == STRATUM-2: THE VFS PROXY (FILESYSTEM AEGIS)                                         ==
# =========================================================================================

class ProjectFileSystemProxy:
    """
    [ROLE]: VIRTUAL_SUBSTRATE_INTERFACE
    """

    def __init__(self, regs: Any):
        self._regs = regs
        self.root = Path(regs.project_root).resolve()
        from ....creator.io_controller import IOConductor
        self._io = IOConductor(regs)

    def write(self, path: Union[str, Path], content: str, perms: str = "644"):
        return self._io.write(Path(path), content, {"origin": "polyglot_script", "permissions": perms})

    def read(self, path: Union[str, Path]) -> str:
        target = (self.root / path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError(f"Gnostic Breach: Path '{path}' is outside the sanctum.")
        if not target.exists():
            raise FileNotFoundError(f"Void Scripture: '{path}'")
        return target.read_text(encoding='utf-8', errors='ignore')

    def exists(self, path: Union[str, Path]) -> bool:
        return (self.root / path).exists()

    def remove(self, path: Union[str, Path]):
        return self._io.delete(Path(path))


# =========================================================================================
# == STRATUM-3: THE SOVEREIGN HANDLER (THE MIND)                                         ==
# =========================================================================================

class PolyglotHandler(BaseRiteHandler):
    """
    [ROLE]: NOETIC_TRANSMUTATION_ENGINE
    Executes embedded Python logic within the Blueprint.
    """

    BANNED_SOULS: Final[Set[str]] = {
        "eval", "exec", "compile", "input", "help",
        "globals", "locals", "setattr", "delattr"
    }

    def __init__(self, registers: Any, alchemist: Any, context: Any):
        super().__init__(registers, alchemist, context)
        self.engine = getattr(registers, 'engine', None)
        self.regs = registers

        if not self.engine:
            from ...runtime.middleware.contract import GnosticVoidEngine
            self.engine = GnosticVoidEngine()

        # [ASCENSION 1]: DETECT SUBSTRATE
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def conduct(self, script_body: str, env: Optional[Dict[str, str]] = None):
        """
        [RITE]: NOETIC INCEPTION
        Executes the script. Branches logic based on substrate (Iron vs Ether).
        """
        start_ns = time.perf_counter_ns()
        trace_id = (env or {}).get("SCAFFOLD_TRACE_ID", "tr-poly-void")

        # --- MOVEMENT I: THE ALCHEMICAL DEDENT ---
        pure_script = textwrap.dedent(script_body.strip("\n\r"))

        # --- MOVEMENT II: PRE-EMPTIVE HYDRATION ---
        import os as _os
        import sys as _sys
        import shutil as _shutil
        from pathlib import Path as _Path

        # --- MOVEMENT III: THE ALCHEMICAL FORGE ---
        # Safe globals for the guest script
        safe_builtins = {k: v for k, v in __builtins__.items() if k not in self.BANNED_SOULS} if isinstance(
            __builtins__, dict) else {k: getattr(__builtins__, k) for k in dir(__builtins__) if
                                      k not in self.BANNED_SOULS}

        gnostic_globals = {
            "__builtins__": safe_builtins,
            "__name__": "__symphony__",
            "os": _os,
            "sys": _sys,
            "shutil": _shutil,
            "Path": _Path,
            "engine": self.engine,
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

        strike_state = {"success": False, "error": None, "traceback": None}

        # --- MOVEMENT IV: THE SUBSTRATE BIFURCATION ---
        self._project_hud_signal(trace_id, "POLYGLOT_STRIKE", "#64ffda")

        if self.is_wasm:
            # === PATH A: ETHER PLANE (SYNCHRONOUS) ===
            # In WASM, we cannot spawn threads. We execute directly in the main loop.
            # We use DirectStreamInterceptor to print immediately to the console.
            self.logger.verbose("PolyglotHandler: WASM Substrate detected. Executing Synchronously.")

            out_interceptor = DirectStreamInterceptor("py", self.console)
            err_interceptor = DirectStreamInterceptor("py_err", self.console)

            try:
                with contextlib.redirect_stdout(out_interceptor), \
                        contextlib.redirect_stderr(err_interceptor):
                    exec(pure_script, gnostic_globals)
                    strike_state["success"] = True
            except Exception as e:
                strike_state["error"] = e
                strike_state["traceback"] = traceback.format_exc()

        else:
            # === PATH B: IRON CORE (THREADED) ===
            # Native environment supports threading to prevent blocking the UI/CLI.
            radiation_queue = queue.Queue()
            out_interceptor = QueuedStreamInterceptor("py", radiation_queue)
            err_interceptor = QueuedStreamInterceptor("py_err", radiation_queue)

            def _conduct_noetic_strike():
                try:
                    with contextlib.redirect_stdout(out_interceptor), \
                            contextlib.redirect_stderr(err_interceptor):
                        exec(pure_script, gnostic_globals)
                        strike_state["success"] = True
                except Exception as e:
                    strike_state["error"] = e
                    strike_state["traceback"] = traceback.format_exc()

            strike_thread = threading.Thread(
                target=_conduct_noetic_strike,
                name=f"PolyglotCell-{trace_id[:8]}",
                daemon=True
            )
            strike_thread.start()

            # Main-Thread Radiator Loop
            timeout = float(os.getenv("SCAFFOLD_POLYGLOT_TIMEOUT", 60.0))
            strike_deadline = time.monotonic() + timeout

            while strike_thread.is_alive():
                # Drain Queue
                try:
                    while True:
                        stream_type, line = radiation_queue.get_nowait()
                        color = "cyan" if stream_type == "py" else "bold red"
                        self.console.print(f"[{color}]   {stream_type}: [/]{line}")
                except queue.Empty:
                    pass

                if time.monotonic() > strike_deadline:
                    self._project_hud_signal(trace_id, "TEMPORAL_EXHAUSTION", "#ef4444")
                    raise ArtisanHeresy("POLYGLOT_TIMEOUT", severity=HeresySeverity.CRITICAL)

                time.sleep(0.05)

            # Final Drain
            try:
                while not radiation_queue.empty():
                    stream_type, line = radiation_queue.get_nowait()
                    color = "cyan" if stream_type == "py" else "bold red"
                    self.console.print(f"[{color}]   {stream_type}: [/]{line}")
            except queue.Empty:
                pass

        # --- MOVEMENT V: ADJUDICATION ---
        if not strike_state["success"]:
            error = strike_state["error"]
            tb = strike_state["traceback"] or traceback.format_exc()
            raise ArtisanHeresy(
                "POLYGLOT_INCEPTION_FRACTURE",
                details=f"Paradox: {type(error).__name__}: {str(error)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                line_num=self.context.line_num,
                suggestion="Gaze upon the internal traceback and verify your 'py:' logic."
            )

        total_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.logger.success(f"Polyglot Rite concluded purely in {total_ms:.2f}ms.")
        gc.collect()

    def _forge_haptic_bridge(self, trace_id: str):
        """Bestows the Hud sigil-generator upon the guest script."""

        class HudBridge:
            def __init__(self, engine, trace):
                self.engine = engine
                self.trace = trace

            def bloom(self, color="#64ffda"): self._send("bloom", color)

            def shake(self, color="#ef4444"): self._send("shake", color)

            def pulse(self, color="#3b82f6"): self._send("pulse", color)

            def _send(self, vfx, color):
                if hasattr(self.engine, 'akashic') and self.engine.akashic:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": vfx, "color": color, "trace": self.trace}
                    })

        return HudBridge(self.engine, trace_id)

    def _project_hud_signal(self, trace: str, label: str, color: str):
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "POLYGLOT_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_POLYGLOT_CONCOURSE substrate={'WASM' if self.is_wasm else 'IRON'} status=RESONANT>"