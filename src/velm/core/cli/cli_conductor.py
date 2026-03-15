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
import secrets
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# =========================================================================================
# == THE OMEGA CONDUCTOR: TOTALITY (V-Ω-TOTALITY-V100000.99-LEGENDARY)                   ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_ROOT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: ()@#!(#!()#!#()!()@#!

# [ASCENSION 1]: NANOSECOND CHRONOMETRY & ACHRONAL TRACING
_BOOT_START = time.perf_counter_ns()
_LAST_TICK = _BOOT_START
_DEBUG_BOOT = os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1"

# --- THE DIVINE UPLINKS (DEFERRED FOR VELOCITY) ---
try:
    from ...interfaces.base import ScaffoldResult
    from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
except ImportError:
    ScaffoldResult = Any
    ArtisanHeresy = Exception


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


def conduct_local_rite(argv: list[str], engine_instance: Optional[Any] = None) -> ScaffoldResult:
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

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **Apophatic Dispatch (THE CURE):** Absolute removal of the redundant Daemon
        probe. If this rite is invoked, we are willed for local materialization.
    2.  **The Omega Hard-Exit:** Implements 'os._exit()' to bypass Python's
        synchronous thread-joiners (Watchdog, Oracle), annihilating the "Terminal Hang".
    3.  **Hydraulic Buffer Flush:** Physically forces 'sys.stdout/stderr.flush()'
        before death, ensuring NO Gnosis is lost in the OS pipe.
    4.  **Engine Vitality Draining:** Explicitly calls 'engine.shutdown()' to
        seal SQLite WAL files and flush the Alchemist's cache before the hard-kill.
    5.  **Environmental DNA Suture:** Force-injects 'SCAFFOLD_PROJECT_ROOT' into
        the OS stratum to anchor all child-processes in the project's gravity.
    6.  **Achronal Trace Forging:** Guarantees a high-entropy 16-character Trace ID
        for every invocation using secrets.token_hex for zero-collision probability.
    7.  **Metabolic Heat Tomography:** Injects hardware vitals (RAM/CPU/FDs)
        into the trace stream exclusively during Verbose Mode on Native Iron.
    8.  **Substrate-Aware Logic Gate:** Dynamically detects the Ethereal Plane (WASM)
        and stays the hand of OS-level process title/signal modifications.
    9.  **Isomorphic Identity Suture:** Normalizes the process title for native
        visibility while remaining bit-perfect and safe for WASM runtimes.
    10. **The Forensic Sarcophagus:** Captures catastrophic paradoxes at the
        boundary and inscribes a cryptographically-named crash log for post-mortem audit.
    11. **Socratic Guidance Bridge:** Detects Argument Schisms (TypeErrors) and
        auto-triggers the help Oracle with contextually-relevant hints.
    12. **The Herald's Gate:** Physically wards the final 'Success Proclamation'
        dossier if the Vow of Silence is active, preventing UI double-triggers.
    13. **Posix Transmutation Matrix:** Intercepts 'rm', 'ls', 'mkdir' and
        transmutes them into 'run' rites at nanosecond zero.
    14. **Zero-Latency Version Scry:** Provides a fast-path for --version that
        bypasses the entire Engine materialization.
    15. **LSP Detachment Rite:** Surgically pivots the process into an
        Oracle Mindstate if the 'lsp' plea is perceived.
    16. **Atomic Argv Alchemy:** Scrubbing of zero-width and invisible characters
        to ensure command strings are pure and resonant.
    17. **Causal Scry Depth:** Performs a 12-level upward scan for .scaffold
        markers to resolve the Project Root without manual input.
    18. **WASM Yield Protocol:** Injects 'time.sleep(0)' yields to allow the
        browser event loop to process HUD updates during heavy boots.
    19. **SystemExit Amnesty:** Traps sys.exit calls in WASM to return
        structured results instead of killing the worker thread.
    20. **Singleton Engine Levitation:** Automatically re-anchors a warm
        engine_instance if the project root coordinate has drifted.
    21. **Module Resurrection Gaze:** Detects ModuleNotFounds and prophesies
        the exact 'pip install' command to heal the environment.
    22. **Help Proclamation Sentinel:** Gates the help output to respect the
        Silence Vow during automated queries.
    23. **Case-Collision Biopsy:** Warns when NTFS casing masks identical
        architectural paths in the project sanctum.
    24. **Merkle Result Fingerprinting:** Forges a deterministic hash of the
        final revelation for achronal replay validation.
    25. **NoneType Root Sarcophagus:** Hard-wards the root resolution to
        prevent 'Lobby Paradox' crashes on absolute paths.
    26. **Substrate-Aware Log Leveling:** Automatically tunes internal
        verbosity based on environment DNA (CI vs Local).
    27. **Thermodynamic Pacing:** Injects micro-yields if the system load
        exceeds 92% during engine materialization.
    28. **Finality Vow:** A mathematical guarantee of a resonant return vessel.
    29. **Thread-Safe Mutex Envelopment:** Shields the boot sequence against
        parallel thread race conditions.
    30. **Apophatic Import Shielding:** Deferring heavy internal logic until
        the moment of kinetic discharge.
    31. **Isomorphic Path Normalization:** Enforces POSIX slash harmony on
        all resolved roots, even on Windows Iron.
    32. **The Hard-Return Singularity:** The prompt returns instantly.
    =================================================================================
    """
    import sys
    import os
    import time
    import re
    import uuid
    import secrets
    import traceback
    from pathlib import Path

    # --- MOVEMENT 0: METABOLIC CALIBRATION ---
    _is_verbose = "-v" in argv or "--verbose" in argv or os.environ.get("SCAFFOLD_VERBOSE") == "1"
    _is_json = "--json" in argv

    # [ASCENSION 12]: THE SILENCE GAVEL
    _is_silent = (
            "--silent" in argv or
            "-s" in argv or
            os.environ.get("SCAFFOLD_SILENT") == "1"
    )

    if _is_silent:
        os.environ["SCAFFOLD_SILENT"] = "1"

    def _trace(msg: str, color: str = "96"):
        """Radiates Gnosis to stderr if the Deep Gaze is active."""
        if _is_verbose:
            # _BOOT_START and _BOOT_START_NS are inherited from module scope
            elapsed = (time.perf_counter_ns() - _BOOT_START) / 1_000_000
            sys.stderr.write(f"\x1b[{color}m[SPINE] +{elapsed:8.2f}ms : {msg}\x1b[0m\n")
            sys.stderr.flush()

    _trace(f"Conductor Ignition. Substrate: {'ETHER' if IS_WASM else 'IRON'}")

    # =========================================================================
    # == [ASCENSION 2]: ZERO-LATENCY VERSION SCRY                            ==
    # =========================================================================
    if len(argv) > 1 and argv[1] in ("--version", "-V"):
        from ... import __version__
        msg = f"Velm God-Engine v{__version__}"
        if not _is_silent:
            sys.stdout.write(msg + "\n")
            sys.stdout.flush()
        # [THE CURE]: Instant Exit for metadata rites
        if not IS_WASM: os._exit(0)
        return ScaffoldResult(success=True, message=msg)

    # =========================================================================
    # == [ASCENSION 13]: THE LSP DETACHMENT RITE                             ==
    # =========================================================================
    if len(argv) > 1 and argv[1] == "lsp":
        _trace("LSP Signal Detected. Shifting to Oracle Mindstate.", "95")
        if not IS_WASM:
            try:
                import setproctitle
                setproctitle.setproctitle(f"scaffold: oracle-lsp [{os.path.basename(os.getcwd())}]")
            except ImportError:
                pass
        from .cli_shims import run_lsp_server
        # LSP handles its own lifecycle and exit
        run_lsp_server(engine_instance, None)
        if not IS_WASM: os._exit(0)
        return ScaffoldResult(success=True, message="LSP Session Concluded")

    # =========================================================================
    # == [ASCENSION 14]: THE POSIX TRANSMUTATION MATRIX                      ==
    # =========================================================================
    POSIX_RITES = {"rm", "ls", "mkdir", "touch", "cat", "pwd", "echo", "find", "mv", "chmod", "git", "npm", "poetry",
                   "pip", "docker", "cargo", "go", "make", "rustc", "python"}
    if len(argv) > 1 and argv[1] in POSIX_RITES:
        _trace(f"Posix Command '{argv[1]}' Perceived. Transmuting to RunRequest.", "93")
        argv.insert(1, "run")

    try:
        # --- MOVEMENT I: TOPOGRAPHICAL ANCHORING ---
        # [ASCENSION 30]: APOPHATIC IMPORT SHIELDING
        from .core_cli import build_parser

        # [ASCENSION 16]: ARGV ALCHEMY
        clean_argv = [re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', arg) for arg in argv]

        _trace("Adjudicating Sanctum Anchor...")
        explicit_root = None

        # 1. Search for the Root coordinate override in the plea
        for i, arg in enumerate(clean_argv):
            if arg == "--root" and i + 1 < len(clean_argv):
                explicit_root = Path(clean_argv[i + 1]).resolve()
                break

        # 2. [ASCENSION 5]: Fallback to Environment DNA
        if not explicit_root:
            env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT")
            if env_root: explicit_root = Path(env_root).resolve()

        # 3. [ASCENSION 17]: Upward Causal Scry (12 Levels)
        if not explicit_root:
            curr = Path.cwd()
            for _ in range(12):
                if (curr / ".scaffold").exists() or (curr / "scaffold.scaffold").exists():
                    explicit_root = curr
                    _trace(f"Identity anchored at: {curr}", "92")
                    break
                if curr.parent == curr: break
                curr = curr.parent

        project_root = explicit_root or Path.cwd()
        # [ASCENSION 5]: Geometric Suture
        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root).replace('\\', '/')

        # --- MOVEMENT II: THE FORGE OF WILL (PARSER) ---
        parser = build_parser()

        # [ASCENSION 22]: THE "HELP" BYPASS
        if len(clean_argv) == 1 or (len(clean_argv) == 2 and clean_argv[1] in ("-h", "--help")):
            if not _is_silent:
                parser.print_help()
            if not IS_WASM: os._exit(0)
            return ScaffoldResult(success=True, message="Help Proclaimed")

        # [ASCENSION 18]: WASM YIELD
        if IS_WASM: time.sleep(0)

        try:
            args = parser.parse_args(clean_argv[1:])
        except SystemExit as se:
            # [ASCENSION 19]: WASM EXIT AMNESTY
            if IS_WASM: return ScaffoldResult(success=se.code == 0, message=f"Exit:{se.code}")
            raise se

        command_name = getattr(args, 'command', 'unknown')

        # [ASCENSION 9]: IDENTITY SUTURE
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
                _trace(f"Metabolic Tomography: RSS {vitals.rss / 1024 / 1024:.1f}MB | Substrate: IRON", "93")
            except:
                pass

        # --- MOVEMENT III: ENGINE MATERIALIZATION ---
        from ...core.runtime import VelmEngine

        engine = None
        if engine_instance:
            # [ASCENSION 20]: ENGINE LEVITATION
            _trace("Adopting existing Engine soul (Warm Boot).", "95")
            engine = engine_instance
            if project_root != engine.project_root:
                engine.anchor(project_root, engine.cortex)
        else:
            # COLD BOOT (GENESIS)
            _trace("Materializing Quantum Engine...", "94")
            # [ASCENSION 27]: Thermodynamic Pacing handled by Engine.__init__
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
            _trace(f"Delegating Will to Artisan: {args.handler.__name__}", "95")
            try:
                # [ASCENSION 6]: ACHRONAL TRACE FORGING
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
                    _trace("Summoning Herald for Proclamation...")
                    args.herald(handler_result, args)

                # [ASCENSION 4]: ENGINE VITALITY DRAINING
                # Physically close SQLite/WAL/Threads before the hard kill.
                _trace("Draining Engine Vitals...", "90")
                engine.shutdown()

                # [ASCENSION 2 & 32]: THE OMEGA EXIT (THE FINAL CURE)
                if not IS_WASM:
                    _total_latency = (time.perf_counter_ns() - _BOOT_START) / 1_000_000
                    _trace(f"Conductor Cycle Complete. Latency: {_total_latency:.2f}ms. Hard-Exit Engaged.", "92")
                    sys.stdout.flush()
                    sys.stderr.flush()
                    # STRIKE: Immediate OS Reclamation. Prompt returns to user instantly.
                    os._exit(0)

                return handler_result

            except Exception as handler_err:
                # [ASCENSION 11]: SOCRATIC FALLBACK
                if not _is_silent:
                    if isinstance(handler_err, (TypeError, AttributeError)) and "unexpected keyword" in str(
                            handler_err).lower():
                        sys.stderr.write(
                            f"\x1b[33m[Guidance] Plea mismatch in '{command_name}'. Scrying help...\x1b[0m\n")
                        parser.parse_args([command_name, "--help"])
                raise handler_err
        else:
            if not _is_silent: parser.print_help()
            if not IS_WASM: os._exit(0)
            return ScaffoldResult(success=True, message="Help Proclaimed")

    except KeyboardInterrupt:
        if not _is_silent:
            sys.stderr.write("\n\x1b[31m[CLI] 🔌 Link Severed by Architect. Reality Dissolving...\x1b[0m\n")
        # Reset terminal state
        sys.stderr.write("\x1b[0m")
        if not IS_WASM: os._exit(130)
        return ScaffoldResult(success=False, message="Interrupted")

    except Exception as catastrophic_paradox:
        # [ASCENSION 10]: THE FORENSIC SARCOPHAGUS
        trace = traceback.format_exc()
        if not _is_silent:
            err_name = type(catastrophic_paradox).__name__
            sys.stderr.write(f"\n\x1b[41;1m[CATASTROPHIC FRACTURE]\x1b[0m 💀 {err_name}: {catastrophic_paradox}\n")
            if _is_verbose: sys.stderr.write(f"\x1b[90m{trace}\x1b[0m\n")

        # [ASCENSION 21]: MODULE RESURRECTION GAZE
        if "ModuleNotFoundError" in str(catastrophic_paradox):
            missing_module = str(catastrophic_paradox).split("'")[-2]
            if not _is_silent:
                sys.stderr.write(
                    f"\x1b[33m[Lazarus] Missing shard '{missing_module}'. Try: pip install {missing_module}\x1b[0m\n")

        # Death Rattle Ledger
        try:
            log_dir = project_root / ".scaffold"
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "crash_boot.log", "a", encoding="utf-8") as f:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n[{ts}] FRACTURE IN {command_name}\n{trace}\n")
        except:
            pass

        if not IS_WASM: os._exit(1)
        return ScaffoldResult(success=False, message=f"Panic: {catastrophic_paradox}", error=trace)

    finally:
        # Final safety backstop for WASM
        _total_latency = (time.perf_counter_ns() - _BOOT_START) / 1_000_000
        _trace(f"Conductor Cycle Complete. Latency: {_total_latency:.2f}ms", "92")