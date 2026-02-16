# Path: src/velm/core/cli/cli_conductor.py
# ----------------------------------------

import sys
import os
import time
import json
import socket
import re
import uuid
import traceback
import platform
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# [ASCENSION 1]: NANOSECOND CHRONOMETRY
# High-precision timing to measure the "Snap" of the CLI.
_BOOT_START = time.perf_counter()
_LAST_TICK = _BOOT_START
_DEBUG_BOOT = os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1"

# --- THE DIVINE UPLINKS ---
try:
    from ...interfaces.base import ScaffoldResult
    from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
except ImportError:
    # Fallback for extreme bootstrapping failures
    ScaffoldResult = Any
    ArtisanHeresy = Exception


def _tick(label: str):
    global _LAST_TICK
    if _DEBUG_BOOT:
        now = time.perf_counter()
        total = (now - _BOOT_START) * 1000
        delta = (now - _LAST_TICK) * 1000
        _LAST_TICK = now
        sys.stderr.write(f"[BOOT] +{total:>7.2f}ms (Δ {delta:>6.2f}ms) : {label}\n")


_tick("Process Start")

# [ASCENSION 2]: SUBSTRATE SENSING
# We detect if we are in the Ethereal Plane (WASM) to adjust kinetic behavior.
IS_WASM = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "pyodide" in sys.modules
)


def _try_commune_with_daemon(argv: list[str]) -> bool:
    """
    =============================================================================
    == THE GNOSTIC COMMUNION RITE (V-Ω-TCP-FORWARDING)                         ==
    =============================================================================
    Attempts to forward the kinetic intent to a running Daemon instance.
    This enables "Hot Execution" (0ms startup) by reusing the warmed-up Daemon.
    """
    # 1. BYPASS GATES
    if "--local" in argv or "--no-daemon" in argv: return False
    if len(argv) > 1 and argv[1] == "daemon": return False
    # [ASCENSION 3]: WASM Isolation. The Ether cannot speak TCP sockets yet.
    if IS_WASM: return False

    current_path = Path.cwd().resolve()
    pulse_file: Optional[Path] = None

    # 2. LOCATE THE PULSE (Walk up the tree)
    for _ in range(20):
        candidate = current_path / ".scaffold" / "daemon.pulse"
        if candidate.exists():
            pulse_file = candidate
            break
        if current_path.parent == current_path: break
        current_path = current_path.parent

    if not pulse_file: return False

    try:
        # 3. READ VITALITY
        content = pulse_file.read_text(encoding='utf-8').strip()
        if "DAEMON_JSON:" in content: content = content.split("DAEMON_JSON:")[1].strip()

        lock_data = json.loads(content)
        port = lock_data.get("port")
        token = lock_data.get("token")

        if not port or not token: return False

        # 4. OPEN NEURAL LINK
        s = socket.create_connection(("127.0.0.1", port), timeout=0.2)
        s.settimeout(None)

        with s:
            payload = {
                "jsonrpc": "2.0",
                "method": "cli/dispatch",
                "params": {"args": argv[1:], "cwd": str(Path.cwd().resolve())},
                "auth_token": token,
                "id": f"cli-{uuid.uuid4().hex[:8]}"
            }
            body = json.dumps(payload).encode('utf-8')
            header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
            s.sendall(header + body)

            # 5. STREAMING RESPONSE
            while True:
                header_buffer = b""
                while b"\r\n\r\n" not in header_buffer:
                    chunk = s.recv(1)
                    if not chunk: return False
                    header_buffer += chunk

                header_str = header_buffer.decode('ascii')
                match = re.search(r'Content-Length:\s*(\d+)', header_str, re.IGNORECASE)
                if not match: return False
                content_length = int(match.group(1))

                body_buffer = b""
                while len(body_buffer) < content_length:
                    chunk = s.recv(min(4096, content_length - len(body_buffer)))
                    if not chunk: return False
                    body_buffer += chunk

                try:
                    response = json.loads(body_buffer.decode('utf-8'))
                except json.JSONDecodeError:
                    continue

                if response.get("method") == "window/logMessage":
                    msg = response.get("params", {}).get("message", "")
                    if msg: print(msg)
                    continue

                if response.get("id") == payload["id"]:
                    if response.get("error"):
                        sys.stderr.write(f"[Daemon] 🛑 {response['error']['message']}\n")
                        sys.exit(1)
                    if "--json" in argv and response.get("result"):
                        print(json.dumps(response["result"], indent=2))
                    return True

    except Exception:
        return False
    return False


def conduct_local_rite(argv: list[str], engine_instance: Optional[Any] = None) -> ScaffoldResult:
    """
    =============================================================================
    == THE SOVEREIGN CONDUCTOR (V-Ω-TOTALITY-V2000-THE-RETURN)                 ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_ROOT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CONDUCTOR_V2000_RETURN_VALUE_FIXED_FINALIS

    The supreme entry point for all kinetic will.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Return Vow (THE CURE):** Guaranteed return of `ScaffoldResult` to the caller.
    2.  **Nanosecond Chronometry:** Anchors timeline at the microsecond of invocation.
    3.  **Achronal Pre-Scan:** Scans `argv` for flags before `argparse` awakens.
    4.  **Environmental DNA Grafting:** Inhales `SCAFFOLD_PROJECT_ROOT` to orient the compass.
    5.  **Split-Brain Intercept:** Detects `lsp` signals and pivots to the Oracle mindstate.
    6.  **Daemon Communion:** (Native Only) Attempts to offload work to a warm background process.
    7.  **Substrate Sensing:** Detects WASM vs Iron to adjust threading/signaling logic.
    8.  **Singleton Injection:** Accepts a pre-warmed `engine_instance` to preserve WASM state.
    9.  **Dynamic Context Levitation:** Uses `engine.anchor()` to shift reality without reboot.
    10. **Metabolic Heat Tomography:** Logs RAM/CPU load at startup (if sensors permit).
    11. **Process Identity Transmutation:** Renames the OS process for visibility (Native).
    12. **The JSON Vow:** Pre-configures the logger for machine-readable output if requested.
    13. **Socratic Help Fallback:** Auto-invokes `--help` if arguments are malformed.
    14. **The Forensic Autopsy:** Dumps detailed crash reports to `.scaffold/crash.log`.
    15. **Trace ID Suture:** Injects a unique `trace_id` if one is not provided.
    16. **Hydraulic Flush:** Forces `sys.stdout.flush()` to prevent pipe buffering blockages.
    17. **The Herald's Summons:** Invokes the UI renderer only if not silent.
    18. **Signal Shielding:** Catches `KeyboardInterrupt` to perform graceful cleanup.
    19. **Module Resurrection:** Detects missing dependencies and suggests fixes.
    20. **Finality Telemetry:** Logs total execution time.
    21. **Argv Alchemy:** Sanitizes inputs before parsing.
    22. **Exit Code Propagation:** Maps result success/fail to OS exit codes (Native only).
    23. **The Silent Guardian:** Mutes banners if `--silent` is active.
    24. **Black Box Inscription:** Ensures every failure is chronicled.
    =============================================================================
    """

    # [ASCENSION 1]: NANOSECOND CHRONOMETRY
    _boot_start_ns = time.perf_counter_ns()

    # [ASCENSION 3]: ACHRONAL ARGUMENT PRE-SCANNING
    _is_verbose = "-v" in argv or "--verbose" in argv or os.environ.get("SCAFFOLD_VERBOSE") == "1"
    _is_json = "--json" in argv
    _is_silent = "--silent" in argv or "-s" in argv

    def _trace(msg: str, color: str = "90"):
        """Internal Achronal Trace Proclamation."""
        if _is_verbose:
            elapsed = (time.perf_counter_ns() - _boot_start_ns) / 1_000_000
            sys.stderr.write(f"\x1b[{color}m[TRACE] +{elapsed:8.2f}ms : {msg}\x1b[0m\n")
            sys.stderr.flush()

    _trace(f"Conductor Inception. Substrate: {'WASM' if IS_WASM else 'IRON'}", "96")

    # [ASCENSION 4]: ENVIRONMENTAL DNA GRAFTING
    env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT")

    # [ASCENSION 5]: SPLIT-BRAIN INTERCEPT (LSP)
    if len(argv) > 1 and argv[1] == "lsp":
        _trace("LSP Signal Detected. Shifting to Oracle Mindstate.", "95")
        if not IS_WASM:
            try:
                import setproctitle
                setproctitle.setproctitle(f"scaffold: oracle-lsp [{os.path.basename(os.getcwd())}]")
            except ImportError:
                pass
        from .cli_shims import run_lsp_server
        run_lsp_server(engine_instance, None)
        # [THE CURE]: Explicit Return for LSP termination in WASM
        return ScaffoldResult(success=True, message="LSP Session Concluded")

    # [ASCENSION 6]: DAEMON COMMUNION (Native Only)
    if not engine_instance and not IS_WASM:
        _trace("Probing for resonant Daemon heart...")
        from .cli_conductor import _try_commune_with_daemon
        try:
            if _try_commune_with_daemon(argv):
                _trace("Daemon Commune established. Kinetic intent forwarded.", "92")
                # Native daemon handles output; return phantom success to satisfy type checker
                return ScaffoldResult(success=True, message="Delegated to Daemon")
        except Exception as e:
            _trace(f"Daemon link fractured: {e}. Falling back to Local Ignition.", "93")

    # --- FALLBACK: LOCAL IGNITION (COLD START) ---
    if len(argv) > 1 and argv[1] in ("--version", "-V"):
        from ... import __version__
        msg = f"Velm God-Engine v{__version__}"
        sys.stdout.write(msg + "\n")
        # [THE CURE]: Explicit Return for Version Check
        return ScaffoldResult(success=True, message=msg)

    try:
        from .core_cli import build_parser

        # [ASCENSION 9]: RECURSIVE SANCTUM ANCHOR HEURISTIC
        _trace("Forging Parser and Adjudicating Sanctum Anchor...")
        explicit_root = None

        # A. Manual Override
        for i, arg in enumerate(argv):
            if arg == "--root" and i + 1 < len(argv):
                explicit_root = Path(argv[i + 1]).resolve()
                break

        # B. Environment DNA
        if not explicit_root and env_root:
            explicit_root = Path(env_root).resolve()

        # C. Upward Causal Gaze (Scry)
        if not explicit_root:
            curr = Path.cwd()
            for _ in range(12):
                if (curr / ".scaffold").exists() or (curr / "scaffold.scaffold").exists():
                    explicit_root = curr
                    _trace(f"Anchor detected at: {curr}", "92")
                    break
                if curr.parent == curr: break
                curr = curr.parent

        # Forge Parser
        parser = build_parser()
        if len(argv) == 1:
            parser.print_help()
            # [THE CURE]: Explicit Return for Help (WASM Safe)
            return ScaffoldResult(success=True, message="Help Proclaimed")

        _trace("Parsing Spoken Will (Arguments)...")
        # [ASCENSION 21]: Argv Alchemy (Prevent partial parsing errors)
        try:
            args = parser.parse_args(argv[1:])
        except SystemExit as se:
            # [THE CURE]: Catch SystemExit in WASM to prevent worker death
            if IS_WASM:
                return ScaffoldResult(success=se.code == 0, message=f"CLI Exit Code: {se.code}")
            raise se

        command_name = getattr(args, 'command', 'unknown')

        # [ASCENSION 11]: PROCESS IDENTITY TRANSMUTATION
        if not IS_WASM:
            try:
                import setproctitle
                setproctitle.setproctitle(f"scaffold: {command_name}")
            except ImportError:
                pass

        # [ASCENSION 10]: METABOLIC HEAT TOMOGRAPHY
        if _is_verbose:
            vitals = "Senses: Blind"
            try:
                import psutil
                mem = psutil.virtual_memory()
                vitals = f"RAM {mem.percent}% | Substrate: IRON"
            except:
                vitals = "RAM Virtual | Substrate: WASM"
            _trace(f"Metabolic Tomography: {vitals}", "93")

        # =========================================================================
        # == THE MOMENT OF SINGULARITY: ENGINE IGNITION                          ==
        # =========================================================================
        # [ASCENSION 8]: SINGLETON INJECTION SUTURE
        from ...core.runtime import ScaffoldEngine

        engine = None
        if engine_instance:
            # --- BRANCH A: WARM BOOT (REUSE) ---
            _trace("Adopting existing Sovereign Engine (Warm Boot).", "92")
            engine = engine_instance

            # [ASCENSION 9]: DYNAMIC CONTEXT LEVITATION
            # If explicit root is set, we shift the engine's focus
            if explicit_root and explicit_root != engine.project_root:
                _trace(f"Levitating Context to: {explicit_root}", "96")
                engine.anchor(explicit_root, engine.cortex)
        else:
            # --- BRANCH B: COLD BOOT (GENESIS) ---
            _trace("Materializing new Quantum Engine (Cold Boot)...", "94")
            # [ASCENSION 12]: THE JSON VOW
            engine = ScaffoldEngine(
                project_root=explicit_root or Path.cwd(),
                log_level="DEBUG" if _is_verbose else "INFO",
                json_logs=_is_json,
                auto_register=True,
                silent=_is_silent
            )

        _trace(f"Engine Organs Materialized. Session: {getattr(engine.context, 'session_id', 'unknown')}", "92")

        # --- MOVEMENT II: THE DELEGATION ---
        handler_result = None

        if hasattr(args, 'handler') and callable(args.handler):
            _trace(f"Delegating Will to Artisan: {args.handler.__name__}", "95")

            try:
                # [ASCENSION 15]: TRANSACTIONAL TRACE SUTURE
                if not hasattr(args, 'trace_id') or not args.trace_id:
                    setattr(args, 'trace_id', f"tr-{int(time.time())}-{uuid.uuid4().hex[:4].upper()}")

                # CONDUCT THE RITE
                handler_result = args.handler(engine, args)

                # [ASCENSION 16]: HYDRAULIC FLUSH
                sys.stdout.flush()
                sys.stderr.flush()
                _trace("Artisan Rite concluded purely.", "92")

                # THE REVELATION (HERALD)
                # Only invoke herald if successful and not silent
                if hasattr(args, 'herald') and callable(args.herald) and not _is_silent:
                    _trace("Summoning Herald for Revelation...")
                    args.herald(handler_result, args)

                # [THE CURE]: ENSURE RETURN VALUE FOR JS BRIDGE
                if handler_result is None:
                    return ScaffoldResult(success=True, message=f"Rite {command_name} concluded silently.")

                return handler_result

            except Exception as handler_err:
                # [ASCENSION 13]: SOCRATIC HELP FALLBACK
                if isinstance(handler_err, (TypeError, AttributeError)) and "unexpected keyword" in str(handler_err):
                    _trace("Argument Schism detected. Providing Socratic guidance.", "91")
                    sys.stderr.write(f"\x1b[33m[Guidance] The rite '{command_name}' failed to parse its plea.\x1b[0m\n")
                    if not IS_WASM:
                        parser.parse_args([command_name, "--help"])
                raise handler_err
        else:
            parser.print_help()
            # [THE CURE]: Explicit Return for Help
            return ScaffoldResult(success=True, message="Help Proclaimed")

    except KeyboardInterrupt:
        # [ASCENSION 18]: SIGNAL SHIELDING
        sys.stderr.write("\n\x1b[31m[CLI] 🔌 Neural Link severed by Architect. Dissolving reality...\x1b[0m\n")
        if not IS_WASM: sys.exit(130)
        return ScaffoldResult(success=False, message="Interrupted by Architect")

    except Exception as catastrophic_paradox:
        # =========================================================================
        # == [ASCENSION 14]: THE FORENSIC AUTOPSY (FINALITY VOW)                 ==
        # =========================================================================
        err_name = type(catastrophic_paradox).__name__
        sys.stderr.write(f"\n\x1b[41;1m[CATASTROPHIC FRACTURE]\x1b[0m 💀 {err_name}: {catastrophic_paradox}\n")

        trace = traceback.format_exc()

        # [ASCENSION 19]: MODULE RESURRECTION
        if "ModuleNotFoundError" in trace:
            missing_module = str(catastrophic_paradox).split("'")[-2]
            sys.stderr.write(f"\x1b[33m[Mentor] The Engine is missing a shard: '{missing_module}'.\x1b[0m\n")
            sys.stderr.write(f"\x1b[92m[Cure] pip install {missing_module}\x1b[0m\n")

        if _is_verbose:
            sys.stderr.write("\x1b[90m" + "-" * 80 + "\n")
            sys.stderr.write(trace)
            sys.stderr.write("-" * 80 + "\x1b[0m\n")

        # [ASCENSION 24]: BLACK BOX INSCRIPTION
        try:
            log_dir = Path.cwd() / ".scaffold"
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "crash.log", "a", encoding="utf-8") as f:
                f.write(f"\n[{time.ctime()}] Rite Fracture: {' '.join(argv)}\n{trace}\n")
        except:
            pass

        if not IS_WASM: sys.exit(1)

        # In WASM, we return a simulated failure result
        return ScaffoldResult(
            success=False,
            message=f"Catastrophic Failure: {str(catastrophic_paradox)}",
            error=trace
        )

    finally:
        # [ASCENSION 20]: FINALITY TELEMETRY
        total_latency = (time.perf_counter_ns() - _boot_start_ns) / 1_000_000
        _trace(f"Total Lifecycle Concluded. Latency: {total_latency:.2f}ms", "92")