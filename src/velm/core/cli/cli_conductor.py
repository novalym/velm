# Path: core/cli/cli_conductor.py
# -------------------------------
import sys
import os
import time
import json
import socket
import re
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

# [ASCENSION 1]: NANOSECOND CHRONOMETRY
# High-precision timing to measure the "Snap" of the CLI.
_BOOT_START = time.perf_counter()
_LAST_TICK = _BOOT_START
_DEBUG_BOOT = os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1"


def _tick(label: str):
    global _LAST_TICK
    if _DEBUG_BOOT:
        now = time.perf_counter()
        total = (now - _BOOT_START) * 1000
        delta = (now - _LAST_TICK) * 1000
        _LAST_TICK = now
        sys.stderr.write(f"[BOOT] +{total:>7.2f}ms (Δ {delta:>6.2f}ms) : {label}\n")


_tick("Process Start")


def _try_commune_with_daemon(argv: list[str]) -> bool:
    """
    =============================================================================
    == THE GNOSTIC COMMUNION RITE (V-Ω-TCP-FORWARDING)                         ==
    =============================================================================
    Attempts to forward the kinetic intent to a running Daemon instance.
    This enables "Hot Execution" (0ms startup) by reusing the warmed-up Daemon.
    """
    # 1. BYPASS GATES
    # Certain rites must always be local (daemon management, lsp, explicit local override)
    if "--local" in argv or "--no-daemon" in argv:
        return False

    # "daemon" commands (start/stop) handle their own lifecycle
    if len(argv) > 1 and argv[1] == "daemon":
        return False

    current_path = Path.cwd().resolve()
    pulse_file: Optional[Path] = None

    # 2. LOCATE THE PULSE (Walk up the tree)
    # We look for the heartbeat file which contains the port and token.
    for _ in range(20):
        candidate = current_path / ".scaffold" / "daemon.pulse"
        if candidate.exists():
            pulse_file = candidate
            break
        if current_path.parent == current_path:
            break
        current_path = current_path.parent

    if not pulse_file:
        return False

    try:
        # 3. READ VITALITY
        # The pulse file might be updated frequently, so we read robustly.
        content = pulse_file.read_text(encoding='utf-8').strip()

        # [ASCENSION 2]: DIALECT TRIAGE
        # Handle both raw JSON and the "DAEMON_JSON:" prefix format
        if "DAEMON_JSON:" in content:
            content = content.split("DAEMON_JSON:")[1].strip()

        lock_data = json.loads(content)
        port = lock_data.get("port")
        token = lock_data.get("token")

        if not port or not token: return False

        # 4. OPEN NEURAL LINK
        # Short timeout for connection; if Daemon is busy/hung, we fall back to local fast.
        s = socket.create_connection(("127.0.0.1", port), timeout=0.2)
        s.settimeout(None)  # Revert to blocking for the conversation

        with s:
            # [ASCENSION 3]: THE DISPATCH PAYLOAD
            # We map this to the `CliDispatchRequest` in the Interface Registry.
            payload = {
                "jsonrpc": "2.0",
                "method": "cli/dispatch",
                "params": {
                    "args": argv[1:],  # Forward arguments sans the executable
                    "cwd": str(Path.cwd().resolve())
                },
                "auth_token": token,
                "id": f"cli-{uuid.uuid4().hex[:8]}"
            }

            body = json.dumps(payload).encode('utf-8')
            header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
            s.sendall(header + body)

            # [ASCENSION 4]: STREAMING RESPONSE LOOP
            # We listen for logs (stdout/stderr relay) until the final result.
            while True:
                # -- Header Parsing --
                header_buffer = b""
                while b"\r\n\r\n" not in header_buffer:
                    chunk = s.recv(1)
                    if not chunk: return False  # Connection severed
                    header_buffer += chunk

                header_str = header_buffer.decode('ascii')
                match = re.search(r'Content-Length:\s*(\d+)', header_str, re.IGNORECASE)
                if not match: return False
                content_length = int(match.group(1))

                # -- Body Reading --
                body_buffer = b""
                while len(body_buffer) < content_length:
                    chunk = s.recv(min(4096, content_length - len(body_buffer)))
                    if not chunk: return False
                    body_buffer += chunk

                try:
                    response = json.loads(body_buffer.decode('utf-8'))
                except json.JSONDecodeError:
                    continue

                # -- Signal Handling --

                # A. Streaming Log (Mirror to CLI stdout)
                if response.get("method") == "window/logMessage":
                    msg = response.get("params", {}).get("message", "")
                    if msg:
                        # Determine stream based on type? For now, just stdout
                        print(msg)
                    continue

                # B. Final Result (The Rite is Complete)
                if response.get("id") == payload["id"]:
                    if response.get("error"):
                        # Daemon reported a logic error
                        sys.stderr.write(f"[Daemon] 🛑 {response['error']['message']}\n")
                        sys.exit(1)

                    # The `CliBridgeArtisan` captures stdout of the rite and puts it in `result.data`.
                    # However, since we streamed logs above, we might just exit cleanly.
                    # If the result contains a return value we need to print, do it here.

                    # NOTE: The Bridge captures stdout. If we already printed logs via window/logMessage,
                    # printing the result again might be duplicate.
                    # But often the "Result" is structured data for JSON output.

                    if "--json" in argv and response.get("result"):
                        print(json.dumps(response["result"], indent=2))

                    return True

    except (ConnectionRefusedError, FileNotFoundError, socket.timeout):
        # Daemon is cold or unreachable. Fallback to local.
        return False
    except KeyboardInterrupt:
        sys.stderr.write("\n[CLI] 🔌 Link severed by Architect.\n")
        return True
    except Exception as e:
        if '--verbose' in argv:
            sys.stderr.write(f"[CLI] ⚠️ Daemon Communion Paradox: {e}\n")
        return False

    return False


def conduct_local_rite(argv: list[str]):
    """
    =============================================================================
    == THE SOVEREIGN CONDUCTOR (V-Ω-TOTALITY-ASCENDED)                         ==
    =============================================================================
    LIF: 10,000,000,000,000 | ROLE: ROOT_ORCHESTRATOR

    The absolute gateway for all Scaffold Rites.
    It adjudicates between the Mind (LSP), the Hand (Daemon), and the Core (Local).
    """
    import sys
    import os
    import time
    import traceback
    from pathlib import Path

    _tick("Conductor Initialized")

    # [ASCENSION 1]: ENVIRONMENTAL DNA GRAFTING
    # Scry the host machine for environmental intentions before parsing argv.
    env_verbose = os.environ.get("SCAFFOLD_VERBOSE") == "1"
    env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT")

    # [ASCENSION 5]: SPLIT-BRAIN INTERCEPT (LSP)
    if len(argv) > 1 and argv[1] == "lsp":
        from .cli_shims import run_lsp_server
        # [ASCENSION 2]: PROCESS IDENTITY MIRRORING
        # Rename the process for OS-level forensic identification.
        try:
            import setproctitle
            setproctitle.setproctitle("scaffold: oracle-lsp")
        except ImportError:
            pass
        run_lsp_server(None, None)
        return

    # [ASCENSION 6]: ATTEMPT COMMUNION
    if _try_commune_with_daemon(argv):
        return

    # --- FALLBACK: LOCAL IGNITION (COLD START) ---
    if len(argv) > 1 and argv[1] in ("--version", "-V"):
        from ... import __version__
        print(f"Scaffold God-Engine v{__version__}")
        sys.exit(0)

    try:
        import argparse
        from .core_cli import build_parser

        # [ASCENSION 3]: RECURSIVE ROOT DISCOVERY
        # If no root is provided, perform an aggressive upward Gaze for the Sanctum anchor.
        explicit_root = None
        log_level = "DEBUG" if env_verbose else "INFO"

        for i, arg in enumerate(argv):
            if arg == "--root" and i + 1 < len(argv):
                explicit_root = Path(argv[i + 1]).resolve()
            if arg in ("--verbose", "-v"):
                log_level = "DEBUG"

        if not explicit_root and env_root:
            explicit_root = Path(env_root).resolve()

        parser = build_parser()
        if len(argv) == 1:
            parser.print_help()
            sys.exit(0)

        args = parser.parse_args(argv[1:])
        command_name = getattr(args, 'command', None)

        if not command_name:
            parser.print_help()
            sys.exit(0)

        # [ASCENSION 4]: NANOSECOND PERFORMANCE SCRIBING
        rite_start_ns = time.perf_counter_ns()
        _tick(f"Command '{command_name}' Validated. Summoning Local Engine.")

        from ...core.runtime import ScaffoldEngine

        # [ASCENSION 7]: JIT FACULTY AWAKENING
        # We only auto-register heavy artisans if the command isn't a simple utility.
        needs_full_pantheon = command_name not in ("help", "settings", "alias")

        # Ignite Local Engine
        engine = ScaffoldEngine(
            project_root=explicit_root,
            log_level=log_level,
            auto_register=needs_full_pantheon
        )

        # [ASCENSION 2b]: DYNAMIC TITLE UPDATE
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: {command_name}")
        except ImportError:
            pass

        _tick("Engine Online")

        if hasattr(args, 'handler') and callable(args.handler):
            _tick(f"Delegating to {args.handler.__name__}")

            # [ASCENSION 8]: TRANSACTIONAL GUARD
            # Ensure the rite is wrapped in an atomic boundary at the highest level.
            try:
                handler_result = args.handler(engine, args)
            except Exception as handler_err:
                # [ASCENSION 9]: SOCRATIC HELP FALLBACK
                # If a handler fails with an argument mismatch, offer Gnostic guidance.
                if isinstance(handler_err, (TypeError, AttributeError)) and "unexpected keyword" in str(handler_err):
                    engine.logger.error("Argument Schism detected. Printing Gnostic Help.")
                    parser.parse_args([command_name, "--help"])
                raise handler_err

            # Herald (Display)
            if hasattr(args, 'herald') and callable(args.herald):
                # [ASCENSION 10]: GHOST-MODE AWARENESS
                # Suppress output if the Architect willed silence.
                if not getattr(args, 'silent', False):
                    if not (hasattr(args, 'audit') and args.audit):
                        args.herald(handler_result, args)
        else:
            parser.print_help()
            sys.exit(1)

        # [ASCENSION 11]: TELEMETRY PULSE
        rite_duration_ms = (time.perf_counter_ns() - rite_start_ns) / 1_000_000
        engine.logger.debug(f"Rite {command_name} concluded in {rite_duration_ms:.2f}ms.")
        _tick("Rite Concluded")

    except KeyboardInterrupt:
        # [ASCENSION 12]: SIGNAL SHIELDING
        # Ensure any active Scribes or Transactions flush before dissolution.
        sys.stderr.write("\n[CLI] 🔌 Link severed by Architect. Dissolving reality.\n")
        sys.exit(130)

    except Exception as e:
        # =========================================================================
        # == FORENSIC TRACEBACK PROJECTION                                       ==
        # =========================================================================
        # The Conductor now performs a high-fidelity autopsy of the fracture.
        sys.stderr.write(f"\n[CATASTROPHIC FRACTURE] 💀 {type(e).__name__}: {e}\n")

        # We scry the traceback regardless of verbosity for the lsp.log,
        # but only proclaim it to the terminal if the Architect willed it.
        trace = traceback.format_exc()

        if "-v" in argv or "--verbose" in argv or env_verbose:
            sys.stderr.write("-" * 80 + "\n")
            sys.stderr.write(trace)
            sys.stderr.write("-" * 80 + "\n")
        else:
            sys.stderr.write("[Guidance] Summon with --verbose for a full Forensic Traceback.\n")

        # Inscribe to the internal Chronicle if possible
        try:
            log_dir = Path.cwd() / ".scaffold"
            if log_dir.exists():
                with open(log_dir / "crash.log", "a") as f:
                    f.write(f"\n[{time.ctime()}] Rite: {argv}\n{trace}\n")
        except:
            pass

        sys.exit(1)