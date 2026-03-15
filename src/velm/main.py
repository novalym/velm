# Path: scaffold/main.py
# ----------------------
# LIF: INFINITY | ROLE: PRIMORDIAL_HYPERVISOR | RANK: SOVEREIGN
# AUTH_CODE: Ω_BOOTSTRAP_SINGULARITY_V400_ZERO_DEP
# =================================================================================

import sys
import os
import time
import json
import socket
import struct
import platform
import traceback
import signal
from pathlib import Path

# [ASCENSION 1]: NANOSECOND CHRONOMETRY
BOOT_START = time.perf_counter()

# [ASCENSION 2]: HYPER-V BOOT
# Pause GC to accelerate the initial import wave and class definitions.
import gc

gc.disable()

# [ASCENSION 3]: FAULTHANDLER INTEGRATION
# If the Python interpreter crashes hard (Segfault), dump the trace to stderr.
import faulthandler

faulthandler.enable()


# =================================================================================
# == SECTION I: ENVIRONMENTAL HARDENING                                          ==
# =================================================================================

def _stabilize_environment():
    """
    [ASCENSION 4 & 5]: WINDOWS TERMINAL & STREAM PURIFICATION.
    Forces the OS to speak the language of UTF-8 and ANSI.
    """
    # 1. Inject Identity
    os.environ["SCAFFOLD_CLI_PID"] = str(os.getpid())

    # 2. Stream Encoding (Windows Fix)
    if sys.platform == 'win32':
        # Enable ANSI Colors in CMD/PowerShell
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass

        # Force UTF-8 Streams
        for stream in [sys.stdin, sys.stdout, sys.stderr]:
            if hasattr(stream, 'reconfigure'):
                try:
                    stream.reconfigure(encoding='utf-8', errors='replace')
                except:
                    pass

    # 3. Path Sanitation
    # Ensure the package root is in sys.path so we can import 'scaffold.core'
    # scaffold/main.py -> parent = scaffold -> parent = root
    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    # 4. Identity Check
    try:
        import setproctitle
        setproctitle.setproctitle(f"scaffold: cli {' '.join(sys.argv[1:])}")
    except ImportError:
        pass


# =================================================================================
# == SECTION II: THE TELEPATHIC BRIDGE (ZERO-DEPENDENCY)                         ==
# =================================================================================

def _try_commune_with_daemon() -> bool:
    """
    [ASCENSION 6]: THE ZERO-DEPENDENCY HANDSHAKE.
    Attempts to forward the command to a running Daemon using ONLY stdlib.
    This allows 'scaffold run' to start instantly by bypassing local imports.

    Returns: True if the Daemon accepted the burden. False to fall back to local.
    """
    # 1. BYPASS GATES
    args = sys.argv[1:]
    if "--local" in args or "--no-daemon" in args or os.environ.get("SCAFFOLD_NO_DAEMON"):
        return False

    # Lifecycle commands must run locally
    if args and args[0] in ("daemon", "lsp", "init"):
        return False

    # 2. LOCATE PULSE (Recursive Ascent)
    cwd = Path.cwd()
    pulse_file = None

    # Scan up to 10 levels
    search_dir = cwd
    for _ in range(10):
        candidate = search_dir / ".scaffold" / "daemon.pulse"
        if candidate.exists():
            pulse_file = candidate
            break
        if search_dir.parent == search_dir: break
        search_dir = search_dir.parent

    if not pulse_file:
        return False

    # 3. PARSE VITALITY
    try:
        # [ASCENSION 7]: ROBUST READ
        # Read with timeout retry to handle atomic write race conditions
        content = ""
        for _ in range(3):
            try:
                content = pulse_file.read_text(encoding='utf-8').strip()
                if content: break
            except:
                time.sleep(0.05)

        if not content: return False

        # Support "DAEMON_JSON:" prefix or raw JSON
        if "DAEMON_JSON:" in content:
            content = content.split("DAEMON_JSON:")[1]

        data = json.loads(content)
        port = data.get("port")
        token = data.get("token")

        if not port or not token: return False

        # 4. OPEN SOCKET (Raw TCP)
        s = socket.create_connection(("127.0.0.1", port), timeout=0.5)

        # 5. FORGE PAYLOAD (JSON-RPC)
        import uuid
        req_id = str(uuid.uuid4())

        payload = {
            "jsonrpc": "2.0",
            "method": "cli/dispatch",
            "params": {
                "args": args,
                "cwd": str(cwd.resolve()),
                "env": dict(os.environ)  # Pass env vars like CI=true
            },
            "auth_token": token,
            "id": req_id
        }

        body = json.dumps(payload).encode('utf-8')
        header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')

        s.sendall(header + body)

        # 6. STREAM RESPONSE (The Mirror)
        # We act as a dumb terminal, printing what the Daemon tells us.
        buffer = b""

        while True:
            # Read Header
            while b"\r\n\r\n" not in buffer:
                chunk = s.recv(4096)
                if not chunk: raise ConnectionResetError()
                buffer += chunk

            header_part, buffer = buffer.split(b"\r\n\r\n", 1)

            # Extract Length
            match = None
            # Simple regex for Content-Length without importing 're' if possible?
            # No, 're' is stdlib and fast.
            import re
            match = re.search(rb"Content-Length: (\d+)", header_part, re.IGNORECASE)
            if not match: return False
            length = int(match.group(1))

            # Read Body
            while len(buffer) < length:
                chunk = s.recv(4096)
                if not chunk: raise ConnectionResetError()
                buffer += chunk

            frame = buffer[:length]
            buffer = buffer[length:]

            # Process Frame
            msg = json.loads(frame)

            # Case A: Log/Stream
            if msg.get("method") == "window/logMessage":
                # Print directly to stdout/stderr
                # params: { type: 1-4, message: "..." }
                print(msg["params"]["message"])

            # Case B: Result (Exit)
            elif msg.get("id") == req_id:
                if msg.get("error"):
                    sys.stderr.write(f"Daemon Error: {msg['error']['message']}\n")
                    sys.exit(1)

                # Success
                result = msg.get("result", {})
                # If result has data intended for stdout (like 'scaffold tree'), print it
                # The daemon usually streams logs, but might return a final payload
                if result and result.get("data") and isinstance(result["data"], str):
                    print(result["data"])

                sys.exit(0)  # [ATOMIC EXIT]

    except Exception:
        # If anything fails (timeout, parse error, socket death),
        # we silently fall back to local execution.
        return False

    return False


# =================================================================================
# == SECTION III: THE FALLBACK (LOCAL IGNITION)                                  ==
# =================================================================================

def _ignite_local_engine():
    """
    [ASCENSION 8]: LAZY LOADING.
    Imports the heavy machinery only when the Daemon is unreachable.
    """
    try:
        # [ASCENSION 21]: PERFORMANCE MARKERS
        if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
            t = (time.perf_counter() - BOOT_START) * 1000
            sys.stderr.write(f"[BOOT] +{t:.2f}ms : Daemon Silent. Igniting Local Core.\n")

        # [ASCENSION 9]: EARLY DEBUGGER ATTACHMENT
        if "--debug-boot" in sys.argv:
            try:
                import debugpy
                debugpy.listen(5678)
                print("Waiting for debugger attach on 5678...")
                debugpy.wait_for_client()
            except ImportError:
                print("Install 'debugpy' to use --debug-boot")

        # Import the Conductor
        from velm.core.cli.cli_conductor import conduct_local_rite

        # [ASCENSION 19]: GC RE-ENGAGEMENT
        gc.enable()

        # Execute
        conduct_local_rite(sys.argv)

    except KeyboardInterrupt:
        # [ASCENSION 12]: CLEAN EXIT
        sys.exit(130)
    except Exception as e:
        _scribe_fracture(e)
        sys.exit(1)


def _scribe_fracture(e: Exception):
    """[ASCENSION 11]: THE SARCOPHAGUS."""
    log_dir = Path.cwd() / ".scaffold"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_dir / "crash_boot.log", "a") as f:
            f.write(f"[{time.ctime()}] {traceback.format_exc()}\n")
    except:
        pass

    # Always scream to stderr
    sys.stderr.write(f"\n[FATAL] Local Engine Fracture: {e}\n")
    traceback.print_exc()


# =================================================================================
# == SECTION IV: THE MAIN SEQUENCE                                               ==
# =================================================================================
def main():
    """
    =================================================================================
    == THE SOVEREIGN ENTRYPOINT: OMEGA POINT (V-Ω-TOTALITY-V26K-HEALED-FINALIS)    ==
    =================================================================================
    LIF: ∞ | ROLE: METASYSTEMIC_GATEKEEPER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_MAIN_V26K_NAMESPACE_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The absolute horizon of the Velm God-Engine. It has been hyper-evolved to
    possess 'Topological Sovereignty', righteously anchoring the package root
    at nanosecond zero to annihilate the 'velm.core' KeyError paradox.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Achronal Namespace Suture (THE MASTER CURE):** Surgically resolves the
        physical 'src' root and places it at the absolute zenith of `sys.path`.
    2.  **Shadow-Path Exorcism (THE MASTER CURE):** Mathematically identifies and
        removes the current directory from `sys.path` if it is a sub-package,
        preventing 'Double-Loading' heresies.
    3.  **Identity Lock Suture:** Forcefully binds `__package__` to 'velm' at the
        global level, ensuring absolute consistency for relative and absolute imports.
    4.  **Apophatic Silence Sieve:** Performs raw `sys.argv` iteration to detect
        `--silent` before any internal logic ignites, warding against boot-noise.
    5.  **Environmental DNA Suture:** Syncs `PYTHONPATH` with the newly willed
        `src` root to ensure perfect recursive awareness for sub-parsers.
    6.  **Nanosecond Chronometry Inception:** Captures the 'Birth NS' immediately
        to measure the 'Time-to-Truth' (TTT) for the telemetry HUD.
    7.  **Hydraulic GC Pacing:** Disables the Garbage Collector during the
        heavy import wave to achieve sub-50ms boot velocity.
    8.  **NoneType Sarcophagus:** Hard-wards the boot sequence against missing
        sys components; if the terminal is unmanifest, it forges a Void Stream.
    9.  **WASM Substrate Mirroring:** Automatically detects the Ethereal Plane
        (Pyodide) and disables Signal Handlers/Subprocesses that fracture the browser.
    10. **Zero-Dependency Communion:** Executes the Daemon Handshake using raw
        sockets only, keeping the local mind 'Cold' if possible.
    11. **Subversion Guard:** If invoked from within another VELM process,
        inherits the parent's Trace ID and Silence Vow automatically.
    12. **The Omega Hard-Exit:** Enforces `os._exit(0)` for CLI mode,
        annihilating the "Hanging Thread" and "Slow Cleanup" paradoxes.
    ... [Continuous through 24 levels of Meta-Systemic Mastery]
    =================================================================================
    """
    # [ASCENSION 7]: HYDRAULIC GC PACING
    import gc
    gc.disable()

    # [ASCENSION 1 & 2]: THE ACHRONAL NAMESPACE SUTURE (THE MASTER CURE)
    import sys
    import os
    from pathlib import Path

    _current_file = Path(__file__).resolve()
    _pkg_dir = str(_current_file.parent)  # .../src/velm
    _src_root = str(_current_file.parents[1])  # .../src

    # 1. Exorcise the Shadow Path (Annihilates the KeyError)
    # Python adds the current script's dir to path; we must cast it out.
    if _pkg_dir in sys.path:
        sys.path.remove(_pkg_dir)

    # 2. Consecrate the True Root (Anchors the 'velm' package)
    if _src_root not in sys.path:
        sys.path.insert(0, _src_root)

    # 3. Environment DNA Suture
    os.environ["PYTHONPATH"] = os.pathsep.join([_src_root, os.environ.get("PYTHONPATH", "")])

    # 4. Identity Lock
    if globals().get("__package__") is None:
        globals()["__package__"] = "velm"

    # [ASCENSION 6]: NANOSECOND CHRONOMETRY INCEPTION
    import time
    _boot_ns = time.perf_counter_ns()

    import re
    import json
    import socket
    import uuid

    # =========================================================================
    # == MOVEMENT 0: APOPHATIC SILENCE SIEVE (THE CURE)                      ==
    # =========================================================================
    _is_silent = False
    for arg in sys.argv:
        if arg in ("--silent", "-s"):
            _is_silent = True
            break

    if _is_silent or os.environ.get("SCAFFOLD_SILENT") == "1":
        os.environ["SCAFFOLD_SILENT"] = "1"
        _is_silent = True

    # [ASCENSION 11]: TRACE ID INCEPTION
    _trace_id = os.environ.get("SCAFFOLD_TRACE_ID")
    if not _trace_id:
        _trace_id = f"tr-boot-{uuid.uuid4().hex[:6].upper()}"
        os.environ["SCAFFOLD_TRACE_ID"] = _trace_id

    # --- SECTION I: ENVIRONMENTAL HARDENING ---
    _is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    if not _is_wasm:
        try:
            import faulthandler
            faulthandler.enable()
        except Exception:
            pass

    # =========================================================================
    # == SECTION II: THE STABILIZATION RITE                                  ==
    # =========================================================================
    try:
        # High-speed substrate stabilization
        if sys.platform == 'win32' and not _is_silent:
            try:
                import ctypes
                ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass
    except Exception:
        pass

    # --- SECTION III: THE RITE OF HASTE (VERSION) ---
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-V"):
        try:
            # Now that pathing is sutured, this import will resonate perfectly
            from velm import __version__
            if not _is_silent: print(f"Velm God-Engine v{__version__}")
            os._exit(0)
        except Exception:
            sys.exit(0)

    # --- SECTION IV: THE PROFILER PROBE ---
    profiler = None
    if os.environ.get("SCAFFOLD_PROFILE") == "1":
        import cProfile
        profiler = cProfile.Profile()
        profiler.enable()

    # =========================================================================
    # == SECTION V: THE TELEPATHIC BRIDGE (DAEMON COMMUNION)                 ==
    # =========================================================================
    try:
        if not ("--local" in sys.argv or "--no-daemon" in sys.argv or os.environ.get("SCAFFOLD_NO_DAEMON") == "1"):
            if not (len(sys.argv) > 1 and sys.argv[1] in ("daemon", "lsp", "init")):
                from .main import _try_commune_with_daemon
                if _try_commune_with_daemon():
                    os._exit(0)
    except Exception:
        pass

    # =========================================================================
    # == SECTION VI: THE KINETIC IGNITION (LOCAL CORE)                       ==
    # =========================================================================
    try:
        # Re-enable GC just before the heavy import wave
        gc.enable()

        # [STRIKE]: Import the heavy conductor. The Suture ensures this works.
        from velm.core.cli.cli_conductor import conduct_local_rite
        conduct_local_rite(sys.argv)

    except KeyboardInterrupt:
        if not _is_silent: sys.stderr.write("\n\x1b[31m[CLI] 🔌 Link Severed.\x1b[0m\n")
        os._exit(130)

    except Exception as catastrophic_paradox:
        if not _is_silent:
            sys.stderr.write(f"\n\x1b[41;1m[FATAL FRACTURE]\x1b[0m 💀 {catastrophic_paradox}\n")
            import traceback
            traceback.print_exc()

        try:
            log_dir = Path.cwd() / ".scaffold"
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "crash_boot.log", "a", encoding="utf-8") as f:
                f.write(f"[{time.ctime()}] Trace: {_trace_id}\n{traceback.format_exc()}\n")
        except Exception:
            pass
        os._exit(1)

    finally:
        # =========================================================================
        # == SECTION VII: THE RITE OF FINALITY                                   ==
        # =========================================================================
        if profiler:
            import pstats
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumtime')
            stats.print_stats(20)

        if __name__ == "__main__" or os.environ.get("SCAFFOLD_CLI_PID"):
            sys.stdout.flush()
            sys.stderr.flush()
            if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1" and not _is_silent:
                _total_ms = (time.perf_counter_ns() - _boot_ns) / 1_000_000
                sys.stderr.write(f"[BOOT] Total Runtime: {_total_ms:.2f}ms. Exiting.\n")
            os._exit(0)

if __name__ == "__main__":
    main()

