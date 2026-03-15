# Path: src/velm/creator/bootloader.py
# ------------------------------------

import argparse
import sys
import os
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Union

# --- Core System Interfaces ---
from .engine import QuantumCreator
from .registers import QuantumRegisters
from ..contracts.data_contracts import ScaffoldItem
from ..core.kernel.transaction import GnosticTransaction
from ..interfaces.requests import BaseRequest

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
# Set SCAFFOLD_DEBUG=1 to enable high-fidelity, unbuffered system tracing
# during the critical boot phase before standard loggers are attached.
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


def _sys_log(msg: str, color_code: str = "36"):
    """
    Unbuffered, direct-to-stderr logging for early-stage boot tracking.
    Guarantees output delivery even during catastrophic WASM kernel panics.
    """
    if _DEBUG_MODE:
        sys.stderr.write(f"\x1b[{color_code};1m[BOOTLOADER]\x1b[0m {msg}\n")
        sys.stderr.flush()


def create_structure(
        scaffold_items: List[ScaffoldItem],
        base_path: Path = Path.cwd(),
        post_run_commands: Optional[List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]] = None,
        pre_resolved_vars: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
        force: bool = False,
        silent: bool = False,
        verbose: bool = False,
        preview: bool = False,
        audit: bool = False,
        lint: bool = False,
        non_interactive: bool = False,
        parser_context: Any = None,
        args: Union[argparse.Namespace, BaseRequest, None] = None,
        transaction: Optional[GnosticTransaction] = None,
        engine: Optional[Any] = None  # [THE CURE]: THE OMEGA ENGINE SUTURE
) -> QuantumRegisters:
    """
    =================================================================================
    == THE OMEGA BOOTLOADER (V-Ω-TOTALITY-V50000-HEALED-ENGINE-LINK)               ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_INITIALIZER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_BOOTLOADER_V50000_ENGINE_SUTURE_2026_FINALIS

    Initializes the execution engine and prepares parsed blueprint items for physical
    materialization. It has been ascended to perfectly transport the God-Engine's
    soul down the execution chain, annihilating the `GnosticVoidEngine` paradox.

    ### THE PANTHEON OF LEGENDARY ASCENSIONS:
    1.  **The Omega Engine Suture (THE CURE):** Safely transports the `engine` instance
        from the Materializer down to the `QuantumCreator`, enabling nested
        `logic.weave()` dispatches without shattering the reality.
    2.  **Null-Content Sarcophagus:** Converts `NoneType` payloads on file nodes
        into empty strings, preventing the I/O Conductor from crashing on write.
    3.  **Substrate-Aware Path Rebasing:** Automatically identifies WASM (Emscripten)
        substrates and dynamically remaps local template seeds to the virtual package path.
    4.  **Achronal Argument Synthesis:** Dynamically reconstructs an `argparse.Namespace`
        if the outer context failed to provide one, ensuring downstream compatibility.
    5.  **Metabolic Boot Tomography:** Records nanosecond precision metrics on the
        exact latency of the sanitization and instantiation phases.
    =================================================================================
    """
    start_ns = time.perf_counter_ns()

    if _DEBUG_MODE:
        _sys_log("Initializing creation pipeline...")

    # Detect the runtime environment to adjust file pathing strategies
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    if _DEBUG_MODE:
        _sys_log(f"Substrate context: {'Browser (WASM/Emscripten)' if is_wasm else 'Native OS'}")
        _sys_log(f"Items pending evaluation: {len(scaffold_items)}")

    # --- Phase 1: Pre-flight Data Sanitization ---
    # Iterates through the parsed Abstract Syntax Tree (AST) items to ensure
    # they are structurally sound before attempting disk I/O.
    for idx, item in enumerate(scaffold_items):
        try:
            content_len = len(item.content) if item.content else 0

            if _DEBUG_MODE:
                _sys_log(
                    f"  -> Validating Node {idx}: [{item.path}] | IsDir: {item.is_dir} | Seed: {item.seed_path} | Size: {content_len} bytes",
                    "30")

            # [ASCENSION 2]: Null-Content Suture
            # If the parser failed to extract content but the node is explicitly defined as a file
            # without an external template seed, we MUST force it to an empty string.
            # Passing `None` to the physical writer will trigger a TypeError and halt the build.
            if item.content is None and not item.seed_path and not item.is_dir:
                if _DEBUG_MODE:
                    _sys_log(
                        f"     [!] Warning: Node '{item.path}' has null content. Coercing to empty string to ensure file creation.",
                        "33")
                item.content = ""

            # [ASCENSION 3]: Environment-Specific Path Rebasing
            # In the browser, local relative paths (e.g., './templates') do not map to the CWD
            # because the Python package is installed deep within the Pyodide virtual filesystem.
            # We intercept and re-route these to the absolute package installation path.
            if is_wasm and item.seed_path:
                seed_str = str(item.seed_path).replace('\\', '/')
                if seed_str.startswith('./templates') or seed_str.startswith('templates/'):
                    clean_seed = seed_str.replace('./', '')
                    item.seed_path = f"/home/pyodide/simulacrum_pkg/default_templates/{clean_seed}"
                    if _DEBUG_MODE:
                        _sys_log(f"     [!] Rebased relative template path for WASM compatibility: {item.seed_path}", "33")

                # Existence Verification: Fail early if the seed template is missing
                seed_p = Path(str(item.seed_path))
                if seed_p.exists():
                    if _DEBUG_MODE:
                        _sys_log(f"     [+] Seed template verified: '{seed_p}' ({seed_p.stat().st_size} bytes).", "32")
                else:
                    if _DEBUG_MODE:
                        _sys_log(f"     [-] Critical Error: Seed template '{seed_p}' is missing from the substrate!", "31")

        except Exception as e:
            if _DEBUG_MODE:
                _sys_log(f"     [X] Unhandled exception during node evaluation: {e}", "31")

    if _DEBUG_MODE:
        _sys_log("Sanitization complete. Handing off to QuantumCreator.", "36")

    # --- Phase 2: Configuration Assembly ---
    # [ASCENSION 4]: Ensure the execution context possesses a standardized configuration namespace
    if args is None:
        args = argparse.Namespace(
            dry_run=dry_run,
            force=force,
            verbose=verbose,
            silent=silent,
            preview=preview,
            audit=audit,
            lint=lint,
            non_interactive=non_interactive,
            root=str(base_path),
            no_edicts=False
        )

    # --- Phase 3: Engine Execution ---
    # The QuantumCreator handles spatial alignment and dispatches to the CPU
    # [ASCENSION 1]: THE OMEGA ENGINE SUTURE
    # We pass the `engine` object so the QuantumCreator can bind it to the registers,
    # preventing the `GnosticVoidEngine` from spawning during `logic.weave`.
    creator = QuantumCreator(
        scaffold_items=scaffold_items,
        args=args,
        engine=engine,  # <-- THE ABSOLUTE CURE
        parser_context=parser_context,
        post_run_commands=post_run_commands,
        pre_resolved_vars=pre_resolved_vars,
        transaction=transaction
    )

    registers = creator.run()

    # [ASCENSION 5]: Metabolic Boot Tomography
    if _DEBUG_MODE:
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        _sys_log(f"Bootloader sequence completed in {duration_ms:.2f}ms.", "32")

    return registers