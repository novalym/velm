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
        from scaffold.core.cli.cli_conductor import conduct_local_rite

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
    The Single Source of Truth.
    """
    _stabilize_environment()

    # [ASCENSION 14]: VERSION SHORT-CIRCUIT
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-V"):
        # We assume version is in __init__.py or similar lightweight place
        try:
            # Minimal import to get version
            from scaffold import __version__
            print(f"Scaffold God-Engine v{__version__}")
            sys.exit(0)
        except:
            pass

    # [ASCENSION 10]: PROFILER INJECTION
    if os.environ.get("SCAFFOLD_PROFILE") == "1":
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

    # 1. Attempt Telepathy (Daemon)
    # If this succeeds, the process exits inside the function.
    _try_commune_with_daemon()

    # 2. Fallback to Local Physics
    _ignite_local_engine()

    # [ASCENSION 10]: PROFILER DUMP
    if os.environ.get("SCAFFOLD_PROFILE") == "1":
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats(20)


if __name__ == "__main__":
    main()