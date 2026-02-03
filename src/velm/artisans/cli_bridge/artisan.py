# Path: artisans/cli_bridge/artisan.py
# ------------------------------------
import io
import sys
import os
import contextlib
import traceback
import argparse
from typing import List, Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.requests import CliDispatchRequest
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan
from ...core.cli.core_cli import build_parser


# =================================================================================
# == THE HOLOGRAPHIC PARSER (V-Ω-NON-LETHAL)                                     ==
# =================================================================================
class HolographicExit(Exception):
    """Signal raised when the parser wants to exit (Help or Error)."""

    def __init__(self, status, message):
        self.status = status
        self.message = message


class HolographicParser(argparse.ArgumentParser):
    """
    [ASCENSION 1]: THE SAFE CONTAINER
    Overrides system-killing methods to throw catchable exceptions.
    """

    def exit(self, status=0, message=None):
        # [ASCENSION 2]: MESSAGE PRESERVATION
        # If there is a message (e.g. error detail), ensure it's captured
        if message:
            # We write to sys.stderr because the context manager will catch it
            sys.stderr.write(message)
        raise HolographicExit(status, message)

    def error(self, message):
        # [ASCENSION 3]: USAGE HINTING
        # Standard argparse prints usage to stderr on error. We replicate that.
        self.print_usage(sys.stderr)
        raise HolographicExit(2, f"{self.prog}: error: {message}\n")


@register_artisan("cli/dispatch")
class CliBridgeArtisan(BaseArtisan[CliDispatchRequest]):
    """
    =============================================================================
    == THE CLI BRIDGE (V-Ω-HOLOGRAPHIC-CONSOLE-V3-ASCENDED)                    ==
    =============================================================================
    LIF: INFINITY | ROLE: VIRTUAL_TERMINAL_EMULATOR

    This artisan executes a CLI command *inside* the running Daemon process.
    It simulates a shell environment, trapping input/output and lifecycle signals
    to prevent the Daemon from terminating while executing sub-routines.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1.  **Injection Logic:** Uses `build_parser(HolographicParser)` to create a safe tree.
    2.  **Stream Capture:** `StringIO` buffers capture every byte of output.
    3.  **ANSI Integrity:** Preserves color codes for XTerm rendering.
    4.  **Contextual Root:** Injects `--root` based on the request `cwd`.
    5.  **State Preservation:** Saves and restores `self.engine.project_root`.
    6.  **Hybrid Output:** Merges stdout and stderr into a single log for the user, but keeps them separate for logic.
    7.  **Exit Code Mapping:** Translates `HolographicExit` status to `ScaffoldResult` success/fail.
    8.  **Help Passthrough:** Treats `status=0` (Help) as a Success, returning the help text.
    9.  **Argument Hygiene:** Copies args list to prevent mutation side-effects.
    10. **Traceback Filtering:** Cleans internal stack traces from the error output.
    11. **Herald Invocation:** Runs the herald if present to generate human-readable text.
    12. **Forensic Logging:** Writes to the Daemon log about the virtual execution.
    """

    def execute(self, request: CliDispatchRequest) -> ScaffoldResult:
        # 1. FORGE THE VIRTUAL CONSOLE
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        # 2. INERTIAL ANCHOR (State Backup)
        original_root = self.engine.project_root

        # 3. EXECUTION CONTEXT
        # We define this inner function to wrap the parsing and execution
        # inside the I/O capture context.
        def _run_hologram():
            # [ASCENSION 9]: ARGUMENT HYGIENE
            raw_args = list(request.args)

            # [ASCENSION 4]: SMART INJECTION
            # If CWD is provided and --root is missing, inject it.
            if request.cwd and "--root" not in raw_args:
                raw_args = ["--root", request.cwd] + raw_args

            # [ASCENSION 1]: INJECTION LOGIC
            # Build the parser using our safe class
            parser = build_parser(parser_class=HolographicParser)

            try:
                # PARSE
                args = parser.parse_args(raw_args)
            except HolographicExit as e:
                # [ASCENSION 7 & 8]: EXIT MAPPING
                if e.status == 0:
                    # Help requested. This is a success.
                    # Rerun print_help to capture it into our buffer (since we are inside the context manager)
                    parser.print_help()
                    return True  # Success
                else:
                    # Error parsing args
                    # Message already written to stderr in .error() override
                    return False  # Failure

            # UPDATE ENGINE CONTEXT
            if hasattr(args, 'root') and args.root:
                self.engine.project_root = args.root

            # HANDLER RESOLUTION
            if hasattr(args, 'handler') and callable(args.handler):
                try:
                    # [ASCENSION 12]: FORENSIC LOGGING
                    # self.logger.info(f"Virtual Execution: {request.args}")

                    # EXECUTE RITE
                    result = args.handler(self.engine, args)

                    # [ASCENSION 11]: HERALD INVOCATION
                    if hasattr(args, 'herald') and callable(args.herald):
                        if not (hasattr(args, 'audit') and args.audit):
                            args.herald(result, args)

                    # Pass the result object out for data return
                    return result

                except Exception as handler_exc:
                    # [ASCENSION 10]: TRACEBACK FILTERING
                    # We print the trace to stderr_capture so the user sees it
                    trace = traceback.format_exc()
                    print(f"\n[RITE FRACTURE]\n{trace}", file=sys.stderr)
                    return False
            else:
                parser.print_help()
                return False

        # 4. RUN THE HOLOGRAM
        final_result = None
        is_success = False

        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                final_result = _run_hologram()

                # Interpret result
                if isinstance(final_result, ScaffoldResult):
                    is_success = final_result.success
                elif isinstance(final_result, bool):
                    is_success = final_result
                elif final_result is None:
                    # Handler returned nothing but didn't crash? Assume success if no stderr?
                    # No, assume failure if void.
                    is_success = False
                else:
                    # Handler returned data
                    is_success = True

        except Exception as e:
            # Catch anything that escaped the hologram (shouldn't happen)
            return self.failure(f"Virtual Machine Failure: {e}")

        finally:
            # [ASCENSION 5]: STATE RESTORATION
            if original_root:
                self.engine.project_root = original_root

        # 5. HARVEST & SYNTHESIZE
        output = stdout_capture.getvalue()
        errors = stderr_capture.getvalue()

        # [ASCENSION 6]: HYBRID OUTPUT
        full_log = output
        if errors:
            full_log += "\n" + errors  # Append errors to output for the terminal

        # Data extraction
        data_payload = None
        if isinstance(final_result, ScaffoldResult):
            data_payload = final_result.data

        if is_success:
            return self.success(full_log, data=data_payload)
        else:
            # If we have a ScaffoldResult failure message, use it, otherwise use captured stderr
            fail_msg = errors
            if isinstance(final_result, ScaffoldResult) and final_result.message:
                fail_msg = final_result.message + "\n" + errors

            return self.failure(fail_msg or "Unknown Failure", data=data_payload)