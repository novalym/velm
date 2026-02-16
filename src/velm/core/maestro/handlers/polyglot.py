# Path: src/velm/core/maestro/handlers/polyglot.py
# =========================================================================================
# == THE OMEGA POLYGLOT CONDUCTOR (V-Ω-TOTALITY-V32000-RECURSION-WARDED)                ==
# =========================================================================================
# LIF: ∞^Billion | ROLE: KINETIC_IO_TRANSFECTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_POLYGLOT_V32K_REENTRANCY_SHIELD_2026_FINALIS
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
import queue
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Set, Final, Tuple

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....utils import to_string_safe, generate_derived_names
from ....logger import Scribe

# [ASCENSION 1]: ACHRONAL RE-ENTRANCY SHIELD
# We use thread-local storage to track the "State of Speech".
# This is the primary weapon against the Ouroboros Recursion.
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
    Implements the RECURSION_WARD to prevent stack collapse.
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

        # --- MOVEMENT I: RE-ENTRANCY DETECTION ---
        if _is_radiating():
            # [ASCENSION 9]: BYPASS MODE
            # We are already inside a print cycle. We must NOT call self.console.print().
            # We shunt matter directly to the substrate to break the loop.
            return self._radiate_raw_matter(s)

        # --- MOVEMENT II: THE PROTECTED INSCRIPTION ---
        _thread_context.is_radiating = True
        try:
            with self._lock:
                # Buffer and radiate on newline to maintain HUD alignment
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

                # [ASCENSION 3]: LUMINOUS PREFIXING
                # We avoid Console.print if possible, or use it only when safe.
                color = "cyan" if self.stream_type == "py" else "bold red"
                prefix = f"\x1b[1;{'36' if self.stream_type == 'py' else '31'}m   {self.stream_type}: \x1b[0m"

                # Radiate the formatted line
                self._radiate_raw_matter(f"{prefix}{line}\n")

    def _radiate_raw_matter(self, text: str) -> int:
        """Final-tier radiation to the host substrate, bypassing all high-level logic."""
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
        """Inscribes matter with automatic transaction tracking."""
        return self._io.write(Path(path), content, {"origin": "polyglot_strike", "permissions": perms})

    def read(self, path: Union[str, Path]) -> str:
        """Recall scripture with spatial boundary protection."""
        target = (self.root / path).resolve()
        if not str(target).startswith(str(self.root)):
            raise ArtisanHeresy("Gnostic Breach: Path escaped the sanctum.", severity=HeresySeverity.CRITICAL)
        if not target.exists():
            raise FileNotFoundError(f"Void Scripture: '{path}'")
        return target.read_text(encoding='utf-8', errors='ignore')

    def exists(self, path: Union[str, Path]) -> bool:
        return (self.root / Path(path)).exists()

    def remove(self, path: Union[str, Path]):
        """Annihilates matter from the physical plane."""
        return self._io.delete(Path(path))

    @property
    def tree(self) -> List[Dict]:
        """Provides an O(1) topographic scry via the VFS oracle."""
        from ...vfs import vfs_scry_recursive
        return vfs_scry_recursive(str(self.root))


# =========================================================================================
# == STRATUM-3: THE SOVEREIGN HANDLER (THE MIND)                                         ==
# =========================================================================================

class PolyglotHandler(BaseRiteHandler):
    """
    [ROLE]: NOETIC_TRANSMUTATION_ENGINE
    LIF: ∞ | ROLE: INTENT_MATERIALIZER | RANK: OMEGA_SUPREME

    The supreme conductor of embedded Python logic. It has been ascended to
    possess absolute substrate awareness and recursive re-entrancy wards.
    """

    # [ASCENSION 11]: THE BANNED SOULS
    # Wards against dangerous built-ins that could fracture the WASM loop.
    BANNED_SOULS: Final[Set[str]] = {
        "eval", "exec", "compile", "input", "help",
        "globals", "locals", "setattr", "delattr"
    }

    def __init__(self, registers: Any, alchemist: Any, context: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(registers, alchemist, context)
        self.engine = getattr(registers, 'engine', None)
        self.regs = registers

        if not self.engine:
            from ...runtime.middleware.contract import GnosticVoidEngine
            self.engine = GnosticVoidEngine()

        # [ASCENSION 1]: SUBSTRATE DIVINATION
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def conduct(self, script_body: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF NOETIC INCEPTION (CONDUCT)                                  ==
        =============================================================================
        LIF: 10,000,000,000 | ROLE: LOGIC_STRIKE | RANK: OMEGA
        """
        start_ns = time.perf_counter_ns()
        trace_id = (env or {}).get("SCAFFOLD_TRACE_ID", "tr-poly-void")

        # --- MOVEMENT I: THE ALCHEMICAL DEDENT ---
        # Normalize the scripture to remove leading whitespace tax.
        pure_script = textwrap.dedent(script_body.strip("\n\r"))

        # --- MOVEMENT II: THE ALCHEMICAL FORGE ---
        # Assemble the Gnostic Globals—the arsenal provided to the guest script.
        safe_builtins = {k: v for k, v in __builtins__.items() if k not in self.BANNED_SOULS} if isinstance(
            __builtins__, dict) else {k: getattr(__builtins__, k) for k in dir(__builtins__) if
                                      k not in self.BANNED_SOULS}

        gnostic_globals = {
            "__builtins__": safe_builtins,
            "__name__": "__symphony__",
            "os": os,
            "sys": sys,
            "shutil": shutil,
            "Path": Path,
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

        # --- MOVEMENT III: THE SUBSTRATE BIFURCATION ---
        self._project_hud_signal(trace_id, "POLYGLOT_STRIKE", "#64ffda")

        if self.is_wasm:
            # =========================================================================
            # == PATH A: ETHER PLANE (SYNCHRONOUS RECURSION-WARDED)                  ==
            # =========================================================================
            # [ASCENSION 1]: WASM cannot spawn threads. We execute in the main loop.
            # We use the GnosticStreamInterceptor to annihilate the Ouroboros loop.
            self.logger.verbose("PolyglotHandler: WASM Substrate detected. Initiating Synchronous Strike.")

            out_interceptor = GnosticStreamInterceptor("py", self.console, is_wasm=True)
            err_interceptor = GnosticStreamInterceptor("py_err", self.console, is_wasm=True)

            try:
                # [THE CURE]: Atomic Redirection
                with contextlib.redirect_stdout(out_interceptor), \
                        contextlib.redirect_stderr(err_interceptor):
                    # THE MOMENT OF TRANSMUTATION
                    exec(pure_script, gnostic_globals)
                    strike_state["success"] = True
            except Exception as e:
                strike_state["error"] = e
                strike_state["traceback"] = traceback.format_exc()

        else:
            # =========================================================================
            # == PATH B: IRON CORE (THREADED RADIATION)                              ==
            # =========================================================================
            # Native iron core supports threading for non-blocking I/O.
            self.logger.verbose("PolyglotHandler: Iron Core detected. Initiating Parallel Strike.")

            # We still use the GnosticStreamInterceptor to prevent recursion in threads
            out_interceptor = GnosticStreamInterceptor("py", self.console, is_wasm=False)
            err_interceptor = GnosticStreamInterceptor("py_err", self.console, is_wasm=False)

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

            # Wait for conclusion with temporal ward
            timeout = float(os.getenv("SCAFFOLD_POLYGLOT_TIMEOUT", 60.0))
            strike_thread.join(timeout=timeout)

            if strike_thread.is_alive():
                self._project_hud_signal(trace_id, "TEMPORAL_EXHAUSTION", "#ef4444")
                # We do not attempt to kill the thread (unsafe), we simply abandon it.
                raise ArtisanHeresy("POLYGLOT_TIMEOUT: The scripture exceeded its 60s temporal budget.")

        # --- MOVEMENT IV: ADJUDICATION ---
        if not strike_state["success"]:
            error = strike_state["error"]
            tb = strike_state["traceback"] or traceback.format_exc()

            # [ASCENSION 12]: THE FINALITY VOW
            # If the script fails, we perform a forensic dump.
            raise ArtisanHeresy(
                "POLYGLOT_INCEPTION_FRACTURE",
                details=f"Paradox: {type(error).__name__}: {str(error)}\n\nTraceback:\n{tb}",
                severity=HeresySeverity.CRITICAL,
                line_num=self.context.line_num,
                suggestion="Gaze upon the internal traceback and ensure your 'py:' logic is pure."
            )

        total_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.logger.success(f"Polyglot Rite concluded purely in {total_ms:.2f}ms.")

        # [METABOLIC LUSTRATION]
        gc.collect()

    def _forge_haptic_bridge(self, trace_id: str):
        """
        =============================================================================
        == THE HAPTIC BRIDGE (V-Ω-UI-TELEPATHY)                                    ==
        =============================================================================
        Bestows the ability to signal the Ocular HUD upon the guest script.
        """

        class HudBridge:
            def __init__(self, engine, trace):
                self.engine = engine
                self.trace = trace

            def bloom(self, color="#64ffda"): self._send("bloom", color)

            def shake(self, color="#ef4444"): self._send("shake", color)

            def pulse(self, color="#3b82f6"): self._send("pulse", color)

            def _send(self, vfx, color):
                akashic = getattr(self.engine, 'akashic', None)
                if akashic:
                    akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": vfx, "color": color, "trace": self.trace}
                    })

        return HudBridge(self.engine, trace_id)

    def _project_hud_signal(self, trace: str, label: str, color: str):
        """Internal telemetry multicast."""
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            try:
                akashic.broadcast({
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

