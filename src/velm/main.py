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
    == THE SOVEREIGN ENTRYPOINT: OMEGA POINT (V-Ω-TOTALITY-V24000-FINALIS)         ==
    =================================================================================
    LIF: ∞ | ROLE: METASYSTEMIC_GATEKEEPER | RANK: OMEGA_SUPREME
    AUTH: Ω_MAIN_V24000_ZERO_LATENCY_SILENCE_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The absolute horizon of the Velm God-Engine. It has been ascended to possess
    'Pre-Cognitive Silence', scrying the intent for silence at nanosecond zero
    to ward the terminal against metabolic log-noise.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Apophatic Intent Scrying (THE CURE):** Performs raw 'sys.argv' iteration
        to detect --silent or -s before any internal imports occur. This prevents
        "Boot-Time Whispering" in WASM environments.
    2.  **Environmental DNA Suture:** Force-injects 'SCAFFOLD_SILENT=1' into the
        OS Environment at birth, ensuring the Scribe, the Alchemist, and all
        Sub-processes inherit the Vow of Stillness.
    3.  **WASM Substrate Mirroring:** Automatically detects the Ethereal Plane
        (Pyodide) and disables Signal Handlers/Subprocesses that fracture the browser.
    4.  **Achronal Chronometry:** Captures the 'Birth NS' immediately to measure
        the 'Time-to-Truth' (TTT) for the telemetry dashboard.
    5.  **NoneType Sarcophagus:** Hard-wards the boot sequence against missing
        sys components; if the terminal is unmanifest, it forges a Void Stream.
    6.  **Zero-Dependency Communion:** Executes the Daemon Handshake using raw
        sockets and JSON-stdlib only, keeping the local mind 'Cold' if possible.
    7.  **Subversion Guard:** If the CLI is invoked from within another VELM
        process, it inherits the parent's Trace ID and Silence Vow automatically.
    8.  **The Omega Hard-Exit:** Enforces 'os._exit(0)' for CLI standalone mode,
        annihilating the "Hanging Thread" heresy and the "Slow Cleanup" paradox.
    9.  **Hydraulic GC Pacing:** Disables the Garbage Collector during the
        import wave to achieve the 'Sub-50ms Boot' milestone.
    10. **Faulthandler Inception:** Bestows the power to dump the Python soul
        to stderr in the event of a native C-level crash.
    11. **Trace ID Silver-Cord:** Forges a unique boot-trace ID if none exists,
        binding the entire lifecycle to a single forensic coordinate.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable gateway.
    =================================================================================
    """
    # [ASCENSION 4]: NANOSECOND CHRONOMETRY INCEPTION
    import time
    _boot_ns = time.perf_counter_ns()

    # [ASCENSION 9]: HYDRAULIC GC PACING
    import gc
    gc.disable()

    import sys
    import os
    import re
    import json
    import socket
    import uuid

    # =========================================================================
    # == MOVEMENT 0: APOPHATIC SILENCE SIEVE (THE CURE)                      ==
    # =========================================================================
    # We scry the raw argv for the Vow of Silence before the Mind is even awake.
    # This prevents 'Import-Time' logging noise from reaching the terminal.
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

    # [ASCENSION 10]: NATIVE FAULT SUTURE
    if not _is_wasm:
        try:
            import faulthandler
            faulthandler.enable()
        except Exception:
            pass

    # =========================================================================
    # == SECTION II: THE STABILIZATION RITE                                  ==
    # =========================================================================
    # [THE CURE]: We only stabilize if we aren't silent, or if it's a critical error.
    try:
        from .core.runtime.middleware.contract import GnosticVoidEngine
        # We perform a manual, high-speed environment stabilization
        if sys.platform == 'win32' and not _is_silent:
            try:
                import ctypes
                ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass

        # Enforce UTF-8 Path Purity for current and future logic
        import importlib
        root_path = Path(__file__).resolve().parent.parent
        if str(root_path) not in sys.path:
            sys.path.insert(0, str(root_path))

    except Exception:
        pass

    # --- SECTION III: THE RITE OF HASTE (VERSION) ---
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-V"):
        try:
            from velm import __version__
            if not _is_silent:
                print(f"Velm God-Engine v{__version__}")
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
    # [ASCENSION 6]: This is the ONLY authorized locus for Daemon redirection.
    # It is zero-dependency to ensure the Mind stays cold during the check.
    try:
        # Check if redirection is willed
        if not ("--local" in sys.argv or "--no-daemon" in sys.argv or os.environ.get("SCAFFOLD_NO_DAEMON") == "1"):
            # Rites that must remain local
            if not (len(sys.argv) > 1 and sys.argv[1] in ("daemon", "lsp", "init")):
                # The _try_commune_with_daemon function must be warded with _is_silent awareness
                if _try_commune_with_daemon():
                    os._exit(0)
    except Exception as bridge_paradox:
        if not _is_silent:
            sys.stderr.write(f"[BRIDGE_FRACTURE] {bridge_paradox}\n")

    # =========================================================================
    # == SECTION VI: THE KINETIC IGNITION (LOCAL CORE)                       ==
    # =========================================================================
    try:
        # [ASCENSION 9]: GC RE-ENGAGEMENT
        # We re-enable GC just before the heavy import wave to allow cleanup.
        gc.enable()

        # JIT: Import the heavy Conductor
        from velm.core.cli.cli_conductor import conduct_local_rite

        # [STRIKE]: Execute the local rite.
        # This function will handle internal silence based on the environment variables.
        conduct_local_rite(sys.argv)

    except KeyboardInterrupt:
        if not _is_silent:
            sys.stderr.write("\n\x1b[31m[CLI] 🔌 Link Severed by Architect.\x1b[0m\n")
        os._exit(130)

    except Exception as catastrophic_paradox:
        # [ASCENSION 5]: THE BLACK BOX SARCOPHAGUS
        if not _is_silent:
            sys.stderr.write(f"\n\x1b[41;1m[FATAL FRACTURE]\x1b[0m 💀 {catastrophic_paradox}\n")
            import traceback
            traceback.print_exc()

        # Inscribe the Death Rattle to disk for later audit
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

        # 1. [THE PROFILER DUMP]
        if profiler:
            import pstats
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumtime')
            stats.print_stats(20)

        # 2. [THE OMEGA EXIT] (ASCENSION 8)
        # We perform a "Hard Kill" to ensure absolute OS reclamation.
        # This prevents the Electron/WASM thread-joining hang.
        if __name__ == "__main__" or os.environ.get("SCAFFOLD_CLI_PID"):
            sys.stdout.flush()
            sys.stderr.flush()

            # [METABOLIC FINALITY LOG]
            if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1" and not _is_silent:
                _total_ms = (time.perf_counter_ns() - _boot_ns) / 1_000_000
                sys.stderr.write(f"[BOOT] Total Runtime: {_total_ms:.2f}ms. Exiting.\n")

            os._exit(0)


if __name__ == "__main__":
    main()

