# Path: language_server_handler.py
# --------------------------------
# LIF: INFINITY | ROLE: SOVEREIGN_BOOTLOADER | RANK: GOD_TIER
# AUTH_CODE: @)(!(@)()@
# =================================================================================
# == THE GNOSTIC BOOTLOADER (V-Ω-TOTALITY-V300-MODULAR)                          ==
# =================================================================================

import os
import sys
import time
import argparse
import traceback
import signal
from pathlib import Path
from typing import Any, Optional

# --- MOVEMENT 0: THE GHOST PROCLAMATION ---
# [ASCENSION 1]: Stop the Electron Sidecar timeout immediately.
# We use raw sys.stdout.write for absolute speed, bypassing any logger.
sys.stdout.write("DAEMON_VITALITY:AWAKENING\n")
sys.stdout.flush()


def handle_language_server(args: Any):
    """
    =============================================================================
    == THE RITE OF CONSECRATION (MODULAR GATEWAY)                              ==
    =============================================================================
    The absolute entry point for the Scaffold VS Code Extension.
    It prepares the physical environment and summons the modular bootstrap
    to materialize the Gnostic Oracle.
    =============================================================================
    """
    # --- MOVEMENT I: THE BINARY GUARD (CRITICAL) ---
    # [ASCENSION 2]: Banish CRLF mangling at the kernel level.
    if sys.platform == "win32":
        import msvcrt
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except Exception as e:
            sys.stderr.write(f"[Oracle] 💥 Binary Mode Shift failed: {e}\n")
            sys.stderr.flush()

    # --- MOVEMENT II: SPATIAL ANCHORING ---
    # [ASCENSION 4]: Resolve the project root with absolute parity.
    try:
        raw_root = getattr(args, 'root', None) or os.environ.get("SCAFFOLD_PROJECT_ROOT") or os.getcwd()
        project_root = Path(raw_root).resolve()

        # [ASCENSION 5]: ENVIRONMENTAL DNA GRAFTING
        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root)
        os.environ["GNOSTIC_SESSION_ACTIVE"] = "1"

        # Ensure the internal sanctum exists
        scaffold_dir = project_root / ".scaffold"
        scaffold_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        sys.stderr.write(f"[Oracle] 💥 Path Resolution Fracture: {e}\n")
        sys.exit(1)

    # --- MOVEMENT III: THE ALPHA INVOCATION ---
    try:
        # [ASCENSION 6 & 11]: LATE-BOUND DELEGATION
        # We reach into our new 12-part modular package structure.
        # This replaces the manual server setup with a total synthesis.
        from .core.lsp.scaffold_server.bootstrap import main as ignite_oracle

        # [ASCENSION 3]: RENAME PROCESS
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: oracle-lsp [{project_root.name}]")
        except ImportError:
            pass

        # [ASCENSION 7]: ARGV ALCHEMY
        # The bootstrap package uses argparse. We ensure it receives the necessary energy.
        # We rebuild sys.argv to pass the root to the internal modular mind.
        sys.argv = [sys.argv[0], "--root", str(project_root)]
        if getattr(args, 'verbose', False) or os.environ.get("SCAFFOLD_VERBOSE") == "1":
            sys.argv.append("--verbose")

        # [ASCENSION 12]: THE LAZARUS BOOT MARKER
        try:
            debug_dir = scaffold_dir / "debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            (debug_dir / "lsp_boot.marker").write_text(str(time.time()))
        except:
            pass

        # --- THE MOMENT OF SINGULARITY ---
        # ignite_oracle() performs the 12-part modular synthesis (Sync, Relay, etc.)
        # and hands control to the eternal read-loop (server.run()).
        ignite_oracle()
        # ---------------------------------

    except KeyboardInterrupt:
        # [ASCENSION 10]: GRACEFUL DISSOLUTION
        sys.exit(0)

    except Exception as fatal_error:
        # [ASCENSION 8]: THE CATASTROPHIC AUTOPSY
        # If the Oracle shatters during ignition, we inscribe the fracture in detail.
        error_trace = traceback.format_exc()

        sys.stderr.write(f"\n[Oracle:FATAL] Inception Failure: {fatal_error}\n")
        sys.stderr.write(error_trace)
        sys.stderr.flush()

        # Inscribe to the Black Box
        try:
            crash_file = project_root / ".scaffold" / "lsp_boot_death.log"
            with open(crash_file, "a", encoding="utf-8") as f:
                f.write(f"\n[{time.ctime()}] FATAL INCEPTION FRACTURE:\n{error_trace}\n")
        except:
            pass

        sys.exit(1)

# === SCRIPTURE SEALED: THE BOOTLOADER IS SOVEREIGN ===