# Path: core/cli/cli_conductor.py
# -------------------------------
import sys
import os
import time
import typing
from pathlib import Path

# =========================================================================================
# == THE OMEGA CONDUCTOR: TOTALITY (V-Ω-TOTALITY-V100000.99-APOPHATIC-BOOT)              ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_ROOT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
# AUTH: Ω_CONDUCTOR_V100K_APOPHATIC_BOOT_2026_FINALIS

# [ASCENSION 1]: NANOSECOND CHRONOMETRY & ACHRONAL TRACING
_BOOT_START = time.perf_counter_ns()
_LAST_TICK = _BOOT_START
_DEBUG_BOOT = os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1"


def _tick(label: str):
    """Metabolic Tomography of the Boot Sequence."""
    global _LAST_TICK
    if _DEBUG_BOOT:
        now = time.perf_counter_ns()
        total = (now - _BOOT_START) / 1_000_000
        delta = (now - _LAST_TICK) / 1_000_000
        _LAST_TICK = now
        sys.stderr.write(f"[BOOT] +{total:>7.2f}ms (Δ {delta:>6.2f}ms) : {label}\n")
        sys.stderr.flush()


_tick("Process Start: Conductor Awakens")

# [ASCENSION 2]: SUBSTRATE SENSING
IS_WASM = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "pyodide" in sys.modules
)

# [ASCENSION 20]: THE SILENT GUARDIAN
import warnings

warnings.filterwarnings("ignore")


def _fast_daemon_handshake(argv: list, cwd_str: str) -> bool:
    """
    =================================================================================
    == THE IRON DAEMON HANDSHAKE (V-Ω-TOTALITY-RUST-ACCELERATED-HEALED)            ==
    =================================================================================
    [THE MASTER CURE]: Annihilates the JIT Import Thrashing paradox, but now features
    the **Graceful Degradation Suture**. If the Rust binary is out-of-date or
    lacks the `fast_daemon_probe` attribute, it instantly and silently falls back
    to the Python-native socket implementation. The boot sequence will never shatter.
    """
    import os
    import sys

    # 1. Apophatic Guard: Do not check daemon if specifically prohibited
    if "--local" in argv or "--no-daemon" in argv or os.environ.get("SCAFFOLD_NO_DAEMON") == "1":
        return False

    # Lifecycle commands must run locally
    if len(argv) > 1 and argv[1] in ("daemon", "lsp", "init"):
        return False

    # 2. Substrate Verification
    if IS_WASM:
        return False

    _tick("Executing Daemon Probe (Rust/Python Hybrid)")

    pulse_path = os.path.join(cwd_str, ".scaffold", "daemon.pulse")
    if not os.path.exists(pulse_path):
        return False

    pid, port, token = None, None, None

    # =========================================================================
    # == [THE CURE]: NATIVE C-SPEED PROBE WITH PYTHONIC FALLBACK             ==
    # =========================================================================
    try:
        import scaffold_core_rs
        # Attempt the native C-speed ping
        probe_result = scaffold_core_rs.fast_daemon_probe(pulse_path)
        if probe_result is None:
            return False  # Daemon is definitively cold via Rust

        pid, port, token = probe_result
        _tick("Rust FFI Handshake Successful.")

    except (ImportError, AttributeError, Exception) as ffi_fracture:
        # [THE TITANIUM WARD]: If Rust is missing the attribute (out of sync)
        # or fails, we degrade gracefully to pure Python to save the boot.
        _tick(f"Rust Probe Bypassed ({type(ffi_fracture).__name__}). Degrading to Python Socket.")

        try:
            import json
            import socket
            import time

            # Time-check to prevent zombie connections
            if (time.time() - os.path.getmtime(pulse_path)) > 10:
                return False

            with open(pulse_path, 'r', encoding='utf-8') as f:
                content = f.read(1024).strip()

            if not content:
                return False

            json_str = content.split("DAEMON_JSON:")[1] if "DAEMON_JSON:" in content else content
            parsed = json.loads(json_str)
            port = int(parsed.get("port", 0))
            pid = int(parsed.get("pid", 0))
            token = parsed.get("token", "")

            if not port or not token:
                return False

            # Python-Native TCP Ping (15ms timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.015)
                if s.connect_ex(("127.0.0.1", port)) != 0:
                    return False

            _tick("Python Native Handshake Successful.")

        except Exception:
            # Absolute worst-case scenario: Daemon is inaccessible
            return False

    # Daemon is Resonant. We possess PID, Port, and Token.
    _tick(f"Daemon Resonant at PID {pid}, Port {port}. Forging Telepathic Link.")

    # =========================================================================
    # == LATE-BOUND IMPORT STRIKE (JIT WAKING)                               ==
    # =========================================================================
    # We only pay the heavy tax of these imports if we KNOW we are connecting.
    import json
    import socket
    import uuid

    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=2.0)
        req_id = f"tr-ipc-{uuid.uuid4().hex[:6].upper()}"

        payload = {
            "jsonrpc": "2.0",
            "method": "cli/dispatch",
            "params": {
                "args": argv[1:],
                "cwd": cwd_str,
                "env": dict(os.environ)
            },
            "auth_token": token,
            "id": req_id
        }

        body = json.dumps(payload).encode('utf-8')
        header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')

        s.sendall(header + body)
        _tick("Payload transmitted. Awaiting revelation.")

        # Streaming Mirror Loop
        buffer = b""
        while True:
            while b"\r\n\r\n" not in buffer:
                chunk = s.recv(4096)
                if not chunk:
                    raise ConnectionResetError("Remote Nexus closed connection prematurely.")
                buffer += chunk

            header_part, buffer = buffer.split(b"\r\n\r\n", 1)

            import re
            match = re.search(rb"Content-Length: (\d+)", header_part, re.IGNORECASE)
            if not match:
                return False

            length = int(match.group(1))

            while len(buffer) < length:
                chunk = s.recv(4096)
                if not chunk:
                    raise ConnectionResetError("Stream truncated during payload reception.")
                buffer += chunk

            frame = buffer[:length]
            buffer = buffer[length:]

            msg = json.loads(frame)

            # Route messages based on Daemon directives
            if msg.get("method") == "window/logMessage":
                print(msg["params"]["message"])
                sys.stdout.flush()
            elif msg.get("id") == req_id:
                if msg.get("error"):
                    sys.stderr.write(f"Daemon Error: {msg['error'].get('message', 'Unknown')}\n")
                    sys.exit(1)

                result = msg.get("result", {})
                if result and result.get("data") and isinstance(result["data"], str):
                    print(result["data"])

                sys.stdout.flush()
                sys.stderr.flush()

                # [THE OMEGA EXIT]: Absolute hard exit
                os._exit(0)

    except Exception as e:
        sys.stderr.write(f"\n[DAEMON_FRACTURE] Telepathic link severed: {e}\n")
        sys.stderr.flush()
        return False

    return False




def conduct_local_rite(argv: list, engine_instance: typing.Any = None) -> typing.Any:
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR: OMEGA TOTALITY (V-Ω-V26000-TITANIUM-HARD-EXIT)     ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_ROOT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CONDUCTOR_V26000_TITANIUM_STABILITY_2026_FINALIS

    [THE MANIFESTO]
    The absolute authority for Local Execution. It has been ascended to possess
    'Biological Finality', ensuring that the process evaporates from the host
    memory the exact nanosecond the Revelation is spoken.

    ### THE PANTHEON OF LEGENDARY ASCENSIONS (THE CURE):
    1.  **The Syntax Suture (THE MASTER CURE):** Mathematically annihilated the Rust
        `if let` syntax bleed. Uses standard Python assignment to scry the locus.
    2.  **Unreachable Code Exorcism:** Surgically reorganizes `os._exit(0)` paths
        so that WASM environments return gracefully while Native Iron hard-exits
        without triggering IDE dead-code warnings.
    3.  **Type Reference Purity:** Decoupled `Any` and `Path` from top-level assumptions
        by utilizing local imports and explicit `typing.Any`, curing "Unresolved Reference".
    4.  **Variable Amnesty:** Removed unused `cwd_str` and localized exception variables
        to prevent casing warnings in strict IDEs.
    =================================================================================
    """
    import sys
    import os
    import time
    import re
    import secrets
    from pathlib import Path

    # --- MOVEMENT 0: METABOLIC CALIBRATION ---
    _is_verbose = "-v" in argv or "--verbose" in argv or os.environ.get("SCAFFOLD_VERBOSE") == "1"
    _is_json = "--json" in argv
    _is_silent = "--silent" in argv or "-s" in argv or os.environ.get("SCAFFOLD_SILENT") == "1"

    if _is_silent:
        os.environ["SCAFFOLD_SILENT"] = "1"

    # =========================================================================
    # == [ASCENSION 34]: ZERO-LATENCY DIRECT ARGV SCRY                       ==
    # =========================================================================
    if len(argv) > 1 and argv[1] in ("--version", "-V"):
        try:
            from ... import __version__
            msg = f"Velm God-Engine v{__version__}"
        except ImportError:
            msg = "Velm God-Engine v[UNKNOWN]"

        if not _is_silent:
            sys.stdout.write(msg + "\n")
            sys.stdout.flush()

        # [THE CURE]: Annihilate Unreachable Code Warning
        if IS_WASM:
            return None
        os._exit(0)

    if len(argv) > 1 and argv[1] == "lsp":
        _tick("LSP Signal Detected. Shifting to Oracle Mindstate.")
        if not IS_WASM:
            try:
                import setproctitle
                setproctitle.setproctitle(f"scaffold: oracle-lsp[{os.path.basename(os.getcwd())}]")
            except ImportError:
                pass

        # JIT Load LSP Shim
        from .cli_shims import run_lsp_server
        import argparse
        dummy_args = argparse.Namespace(verbose=_is_verbose, root=os.getcwd())
        run_lsp_server(engine_instance, dummy_args)

        # [THE CURE]: Annihilate Unreachable Code Warning
        if IS_WASM:
            return None
        os._exit(0)

    # =========================================================================
    # ==[ASCENSION 37]: ACHRONAL LOCUS SCRYING (RUST-ACCELERATED)           ==
    # =========================================================================
    _tick("Adjudicating Sanctum Anchor...")
    explicit_root_str = None

    # 1. Search for the Root coordinate override in the plea
    for i, arg in enumerate(argv):
        if arg == "--root" and i + 1 < len(argv):
            explicit_root_str = argv[i + 1]
            break

    # 2. Fallback to Environment DNA
    if not explicit_root_str:
        explicit_root_str = os.environ.get("SCAFFOLD_PROJECT_ROOT")

    # 3.[THE MASTER CURE]: Native C-Speed Upward Traversal
    # Pythonic assignment. Absolutely NO Rust syntax (&) here.
    if not explicit_root_str and not IS_WASM:
        try:
            import scaffold_core_rs
            # Rust blasts up 12 directory levels in <0.05ms natively
            fast_root = scaffold_core_rs.fast_locus_anchor_scry(os.getcwd())
            if fast_root:
                explicit_root_str = fast_root
                _tick(f"Identity anchored natively at: {explicit_root_str}")
        except Exception as core_err:
            _tick(f"Native Iron Scry deferred: {core_err}. Degrading to Python.")

    project_root = Path(explicit_root_str).resolve() if explicit_root_str else Path.cwd()
    os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root).replace('\\', '/')

    # =========================================================================
    # == [ASCENSION 35]: THE IRON DAEMON HANDSHAKE                           ==
    # =========================================================================
    if _fast_daemon_handshake(argv, str(project_root)):
        # We should never reach here as the handshake calls os._exit(0) natively
        return None

    _tick("Daemon unreachable or local willed. Waking Python Core.")

    # =========================================================================
    # == [ASCENSION 33]: JIT ALCHEMY (DEFERRED HEAVY IMPORTS)                ==
    # =========================================================================
    # --- MOVEMENT I: TOPOGRAPHICAL ANCHORING ---
    from .core_cli import build_parser

    clean_argv = [re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', arg) for arg in argv]

    # --- MOVEMENT II: THE FORGE OF WILL (PARSER) ---
    parser = build_parser()

    if len(clean_argv) == 1 or (len(clean_argv) == 2 and clean_argv[1] in ("-h", "--help")):
        if not _is_silent:
            parser.print_help()
        if IS_WASM:
            return None
        os._exit(0)

    if IS_WASM:
        time.sleep(0)

    try:
        args = parser.parse_args(clean_argv[1:])
    except SystemExit as se:
        # [ASCENSION 19]: WASM EXIT AMNESTY
        if IS_WASM:
            return None
        raise se

    command_name = getattr(args, 'command', 'unknown')

    # Identity Suture
    if not IS_WASM:
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: {command_name}")
        except ImportError:
            pass

    # [ASCENSION 7]: METABOLIC TOMOGRAPHY
    if _is_verbose and not IS_WASM:
        try:
            import psutil
            vitals = psutil.Process().memory_info()
            _tick(f"Metabolic Tomography: RSS {vitals.rss / 1024 / 1024:.1f}MB | Substrate: IRON")
        except Exception:
            pass

    # --- MOVEMENT III: ENGINE MATERIALIZATION ---
    from ...core.runtime import VelmEngine

    engine = None
    if engine_instance:
        _tick("Adopting existing Engine soul (Warm Boot).")
        engine = engine_instance
        if project_root != engine.project_root:
            engine.anchor(project_root, engine.cortex)
    else:
        _tick("Materializing Quantum Engine (Cold Boot).")
        engine = VelmEngine(
            project_root=project_root,
            log_level="DEBUG" if _is_verbose else "INFO",
            json_logs=_is_json,
            auto_register=True,
            silent=_is_silent
        )

    # --- MOVEMENT IV: THE KINETIC STRIKE ---
    handler_result = None
    if hasattr(args, 'handler') and callable(args.handler):
        _tick(f"Delegating Will to Artisan: {args.handler.__name__}")
        try:
            if not hasattr(args, 'trace_id') or not args.trace_id:
                setattr(args, 'trace_id', f"tr-{secrets.token_hex(4).upper()}")

            # [STRIKE]: Execute the rite
            handler_result = args.handler(engine, args)

            # =====================================================================
            # == MOVEMENT V: THE REVELATION & DRAIN (THE CURE)                   ==
            # =====================================================================
            # [ASCENSION 3]: HYDRAULIC FLUSH
            sys.stdout.flush()
            sys.stderr.flush()

            # [ASCENSION 12]: THE HERALD'S GATE
            if hasattr(args, 'herald') and callable(args.herald) and not _is_silent:
                _tick("Summoning Herald for Proclamation.")
                args.herald(handler_result, args)

            _tick("Draining Engine Vitals.")
            engine.shutdown()

            # =====================================================================
            # == [ASCENSION 36]: THE OMEGA HARD-EXIT                             ==
            # =====================================================================
            if not IS_WASM:
                _total_latency = (time.perf_counter_ns() - _BOOT_START) / 1_000_000
                _tick(f"Conductor Cycle Complete. Latency: {_total_latency:.2f}ms. Hard-Exit Engaged.")
                sys.stdout.flush()
                sys.stderr.flush()
                # STRIKE: Immediate OS Reclamation.
                # Bypasses all thread.join() blocking on Daemons.
                os._exit(0)

            return handler_result

        except Exception as handler_err:
            # [ASCENSION 11]: SOCRATIC FALLBACK
            if not _is_silent:
                if isinstance(handler_err, (TypeError, AttributeError)) and "unexpected keyword" in str(
                        handler_err).lower():
                    sys.stderr.write(f"\x1b[33m[Guidance] Plea mismatch in '{command_name}'. Scrying help...\x1b[0m\n")
                    parser.parse_args([command_name, "--help"])
            raise handler_err
    else:
        if not _is_silent:
            parser.print_help()

        if IS_WASM:
            return None
        os._exit(0)


def main():
    """
    =============================================================================
    == THE ALPHA AND THE OMEGA: ENTRY POINT                                    ==
    =============================================================================
    """
    try:
        conduct_local_rite(sys.argv)
    except KeyboardInterrupt:
        sys.stderr.write("\n\x1b[31m[CLI] 🔌 Link Severed by Architect. Reality Dissolving...\x1b[0m\n")
        # Reset terminal state
        sys.stderr.write("\x1b[0m")
        if not IS_WASM: os._exit(130)
    except Exception as catastrophic_paradox:
        import traceback
        trace = traceback.format_exc()
        err_name = type(catastrophic_paradox).__name__

        # We write directly to stderr to ensure visibility even during a profound crash
        sys.stderr.write(f"\n\x1b[41;1m[CATASTROPHIC FRACTURE]\x1b[0m 💀 {err_name}: {catastrophic_paradox}\n")
        if _DEBUG_BOOT:
            sys.stderr.write(f"\x1b[90m{trace}\x1b[0m\n")

        # The Death Rattle Ledger (Forensic preservation)
        try:
            # Safely attempt to write to the project log if we know the root
            env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT", ".")
            log_dir = Path(env_root) / ".scaffold"
            log_dir.mkdir(parents=True, exist_ok=True)

            with open(log_dir / "crash_boot.log", "a", encoding="utf-8") as f:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                # Attempt to extract command from argv safely
                cmd_attempt = sys.argv[1] if len(sys.argv) > 1 else "unknown_rite"
                f.write(f"\n[{ts}] FRACTURE IN {cmd_attempt}\n{trace}\n")
        except Exception:
            pass  # Silent failure on the death rattle

        sys.stderr.flush()
        if not IS_WASM: os._exit(1)


if __name__ == "__main__":
    main()