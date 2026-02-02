# Path: scaffold/utils/invocation.py
# ----------------------------------
"""
=================================================================================
== THE SACRED SANCTUM OF INVOCATION (V-Ω-ETERNAL. THE PURE CONDUIT)            ==
=================================================================================
This scripture is the one true, universal home of the God-Engine of Gnostic
Invocation. By enshrining this rite in a pure, decoupled sanctum, we annihilate
the Ouroboros of circular dependency and make its power available to all
artisans in the cosmos.
=================================================================================
"""
import argparse
import os
import shlex
import sys
import threading
import time
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import List, Optional, Dict, Any, Generator, Union

from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from ..contracts.data_contracts import CoreCLIInvocationResult
from ..contracts.heresy_contracts import ArtisanHeresy, GuardianHeresy
from ..logger import get_console, set_console, SCRIBE_THEME, Scribe

Logger = Scribe("GodEngineInvoker")

# A sacred, global vessel for the Chronocache
_INVOCATION_CACHE: Dict[str, 'CoreCLIInvocationResult'] = {}


@contextmanager
def _capture_reality(stdin_content: Optional[str], raw_mode: bool) -> Generator[Dict[str, Any], None, None]:
    """
    [THE GNOSTIC SANCTUM] A divine context manager that forges an ephemeral reality
    for a child artisan to be conducted in, capturing its every word and thought.
    """
    original_stdout, original_stderr, original_stdin = sys.stdout, sys.stderr, sys.stdin
    original_console = get_console()
    original_raw_mode = os.getenv("SCAFFOLD_RAW_MODE")
    captured_output = StringIO()

    try:
        # --- The Rite of Soul Transfiguration ---
        from rich.console import Console
        humble_console = Console(file=captured_output, force_terminal=False, no_color=True, theme=SCRIBE_THEME)
        set_console(humble_console)
        sys.stdin = StringIO(stdin_content) if stdin_content is not None else StringIO()
        if raw_mode:
            os.environ["SCAFFOLD_RAW_MODE"] = "true"

        yield {"output_stream": captured_output}

    finally:
        # --- The Rite of Eternal Restoration ---
        set_console(original_console)
        sys.stdout, sys.stderr, sys.stdin = original_stdout, original_stderr, original_stdin
        if original_raw_mode is None:
            if "SCAFFOLD_RAW_MODE" in os.environ: del os.environ["SCAFFOLD_RAW_MODE"]
        else:
            os.environ["SCAFFOLD_RAW_MODE"] = original_raw_mode


@contextmanager
def _temporal_sanctum(cwd: Optional[Union[str, Path]]) -> Generator[None, None, None]:
    """
    [THE DIVINE ARTISAN OF EPHEMERAL REALITIES]
    Performs Gnostic Translocation and atomic restoration.
    """
    if not cwd:
        yield
        return

    original_cwd = Path.cwd()
    try:
        Logger.verbose(f"Gnostic Translocation: Entering ephemeral sanctum at '{cwd}'")
        os.chdir(cwd)
        yield
    finally:
        os.chdir(original_cwd)
        Logger.verbose(f"Rite of Return: Original sanctum '{original_cwd.name}' restored.")


def invoke_scaffold_command(
        command_args: List[str],
        stdin_content: Optional[str] = None,
        raw_mode: bool = False,
        timeout_seconds: int = 60,
        use_cache: bool = True,
        non_interactive: bool = False,
        cwd: Optional[Union[str, Path]] = None
) -> 'CoreCLIInvocationResult':
    """
    [THE GOD-ENGINE OF GNOSTIC INVOCATION]
    Executes a command in-process via the Parser.
    """
    start_time = time.monotonic()

    if not command_args:
        return CoreCLIInvocationResult(exit_code=1, output="Heresy of the Void Plea: No command arguments provided.",
                                       command_executed="scaffold")

    is_pure_rite = "--audit" in command_args or "--preview" in command_args
    cache_key = None
    if use_cache and is_pure_rite:
        from hashlib import sha256
        cache_key = sha256(f"{' '.join(command_args)}{stdin_content}{cwd}".encode()).hexdigest()
        if cache_key in _INVOCATION_CACHE:
            Logger.verbose("Chronocache HIT. Proclaiming remembered Gnosis instantly.")
            return _INVOCATION_CACHE[cache_key]

    result_container = {}
    heresy_container = {}
    worker_finished = threading.Event()

    def _rite_worker():
        try:
            with _temporal_sanctum(cwd):
                result_container['result'] = _perform_actual_invocation(
                    command_args,
                    stdin_content,
                    raw_mode,
                    non_interactive
                )
        except Exception as e:
            heresy_container['heresy'] = e
        finally:
            worker_finished.set()

    worker_thread = threading.Thread(target=_rite_worker)
    worker_thread.daemon = True
    worker_thread.start()

    worker_finished.wait(timeout=timeout_seconds)

    if worker_thread.is_alive():
        return CoreCLIInvocationResult(
            exit_code=1,
            output=f"DAEMON PARADOX: InvocationTimeoutHeresy: The rite exceeded the sacred {timeout_seconds}s time limit and was stayed.",
            command_executed=f"scaffold {' '.join(command_args)}"
        )

    if 'heresy' in heresy_container:
        e = heresy_container['heresy']
        return CoreCLIInvocationResult(
            exit_code=1,
            output=f"DAEMON PARADOX: {type(e).__name__}: {e}",
            command_executed=f"scaffold {' '.join(command_args)}"
        )

    result_vessel = result_container.get('result')
    if not result_vessel:
        return CoreCLIInvocationResult(exit_code=1, output="DAEMON PARADOX: The rite concluded without a proclamation.",
                                       command_executed=f"scaffold {' '.join(command_args)}")

    if use_cache and is_pure_rite and cache_key and result_vessel.exit_code == 0:
        _INVOCATION_CACHE[cache_key] = result_vessel
        Logger.verbose("Pure Gnosis inscribed into the Chronocache.")

    return result_vessel


def _perform_actual_invocation(
        command_args: List[str],
        stdin_content: Optional[str] = None,
        raw_mode: bool = False,
        non_interactive: bool = False
) -> 'CoreCLIInvocationResult':
    """
    [THE GOD-ENGINE OF GNOSTIC INVOCATION]
    The one true mind.
    """
    # ★★★ THE DEFERRED SUMMONS: BREAKING THE OUROBOROS ★★★
    from ..core.cli.core_cli import build_parser
    # ★★★ THE CIRCLE IS BROKEN ★★★

    start_time = time.monotonic()
    exit_code: int = 0
    parsed_args: Optional[argparse.Namespace] = None
    handler_name: str = "N/A"
    exception_obj: Optional[BaseException] = None
    output_str: str = ""
    proclamations: Dict[str, Any] = {}

    with _capture_reality(stdin_content, raw_mode) as reality:
        try:
            final_command_args = list(command_args)
            if non_interactive and '--non-interactive' not in final_command_args:
                final_command_args.append('--non-interactive')

            parser = build_parser()
            parsed_args, unknown_args = parser.parse_known_args(final_command_args)

            if unknown_args:
                handler_name_for_gaze = getattr(parsed_args, 'command', 'genesis')
                artisans_accepting_paths = {'genesis', 'beautify', 'symphony'}

                if handler_name_for_gaze in artisans_accepting_paths:
                    path_gnosis = unknown_args[0]
                    if handler_name_for_gaze == 'symphony' and hasattr(parsed_args, 'symphony_path'):
                        parsed_args.symphony_path = path_gnosis
                    elif hasattr(parsed_args, 'blueprint_path'):
                        parsed_args.blueprint_path = path_gnosis
                else:
                    parser.parse_args(final_command_args)

            handler_name = getattr(parsed_args, 'command', 'genesis')

            if hasattr(parsed_args, 'handler') and callable(parsed_args.handler):
                handler_result = parsed_args.handler(parsed_args)
                if isinstance(handler_result, dict):
                    proclamations = handler_result
            else:
                raise ArtisanHeresy(
                    f"Heresy of the Unknown Tongue: The plea '{handler_name}' is not a recognized rite.", exit_code=2)

        except (ArtisanHeresy, GuardianHeresy) as e:
            exception_obj, exit_code = e, getattr(e, 'exit_code', 1)
            reality["output_stream"].write(e.get_proclamation())
        except SystemExit as e:
            exception_obj, exit_code = e, e.code if e.code is not None else 0
        except Exception as e:
            exception_obj, exit_code = e, 1
            from rich.traceback import Traceback
            console = get_console()
            dossier_table = Table(box=None, show_header=False)
            dossier_table.add_row("[dim]Raw Plea:[/dim]", f"[yellow]`scaffold {' '.join(command_args)}`[/yellow]")
            dossier_table.add_row("[dim]Perceived Handler:[/dim]", f"[yellow]{handler_name}[/yellow]")
            trace = Traceback.from_exception(type(e), e, e.__traceback__, show_locals=True, word_wrap=True)
            console.print(Panel(Group(dossier_table, trace),
                                title="[bold red]Dossier of the Catastrophic, Unhandled Paradox[/bold red]"))

        output_str = reality["output_stream"].getvalue()

    duration = time.monotonic() - start_time
    full_command_str = f"scaffold {' '.join(shlex.quote(arg) for arg in command_args)}"
    final_args_dict = vars(parsed_args) if parsed_args else {}
    if 'handler' in final_args_dict: del final_args_dict['handler']

    exception_str = str(exception_obj) if exception_obj and not isinstance(exception_obj, SystemExit) else ""

    return CoreCLIInvocationResult(
        exit_code=exit_code, output=output_str, duration=duration, command_executed=full_command_str,
        handler_name=handler_name, final_arguments=final_args_dict,
        exception_object=exception_str, new_sanctum=proclamations.get("new_sanctum")
    )