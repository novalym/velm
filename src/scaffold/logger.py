# scaffold/logger.py - PART 1 of 2

"""
=================================================================================
== THE SACRED SANCTUM OF THE UNIVERSAL SCRIBE (V-Ω-APOTHEOSIS-FINALIS)         ==
=================================================================================
LIF: 10,000,000,000
STATUS: SENTIENT EVENT BUS, HYPER-LOGGER & TELEMETRY ENGINE

This is the nervous system of the Scaffold God-Engine. It has been ascended to
handle any form of Gnostic proclamation, whether structured data, raw text, or
catastrophic paradoxes.

It implements the **Argument Segregation Membrane** to ensure perfect compatibility
between Gnostic Rites (Rich TUI) and Standard Laws (Python Logging).
=================================================================================
"""
import os
import json
import logging
import re
import sys
import threading
import time
import traceback
from collections import deque
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List, Any, Dict, Callable, Union

# --- The Divine Stanza of the Scribe's Tools (Third Party) ---
RICH_AVAILABLE = False
try:
    from rich.console import Console, Group
    from rich.theme import Theme
    from rich.markup import escape
    from rich.panel import Panel
    from rich.text import Text
    from rich.padding import Padding
    from rich.traceback import Traceback
    from rich.json import JSON
    from rich.markdown import Markdown
    from rich.pretty import Pretty

    RICH_AVAILABLE = True
except ImportError:
    # Gnostic Ward for environments without Rich
    # Allows the Scribe to function in a diminished but stable capacity
    class Console:
        def __init__(self, *args, **kwargs): pass

        def print(self, *args, **kwargs): print(*args, file=sys.stderr)

        def rule(self, *args, **kwargs): print("-" * 80, file=sys.stderr)


    class Theme:
        def __init__(self, *args, **kwargs): pass


    def Padding(renderable, pad):
        return renderable


    def JSON(data):
        return str(data)


    def Markdown(data):
        return str(data)


    def Pretty(data):
        return str(data)

# --- THE DIVINE GRIMOIRE OF THE SCRIBE'S VOICE ---
SCRIBE_THEME = Theme({
    "info": "cyan",
    "success": "bold green",
    "warning": "yellow",
    "error": "bold red",
    "danger": "bold red reverse",
    "verbose": "dim white",
    "audit": "bold magenta",
    "context": "dim italic",
    "timestamp": "dim white",
    "tag": "bold magenta reverse",
})

# --- THE COSMIC GNOSIS (Global State) ---
_COSMIC_GNOSIS = {
    "verbose": False,
    "silent": False,
    "json_mode": False,
    "debug_mode": False,
    "max_memory": 1000
}

# --- THE VESSEL OF THE LIVING SOUL ---
# We output to stderr by default to keep stdout clean for piped commands (Unix Philosophy)
_CONSOLE: Console = Console(theme=SCRIBE_THEME, stderr=True)

# --- ELEVATION 6: THE TELEPATHIC LINK (CALLBACK REGISTRY) ---
# Allows external systems (VS Code) to subscribe to the log stream
_LOG_HOOKS: List[Callable[[Dict], None]] = []

# --- ELEVATION 5: THE EPHEMERAL BUFFER (MEMORY RING) ---
# Stores the last N logs for crash reporting
_MEMORY_BUFFER = deque(maxlen=_COSMIC_GNOSIS["max_memory"])

# --- ELEVATION 2: THE SECRET REDACTOR PATTERNS ---
# Regex patterns to mask sensitive data in logs
_SECRET_PATTERNS = [
    r'(api_key|token|secret|password|passwd|credential)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?',
    r'(Bearer\s+)([a-zA-Z0-9\-\._~\+\/]+)',
    r'(ghp_[a-zA-Z0-9]+)'
]


def get_console() -> Console:
    """Returns the active Rich Console instance."""
    return Scribe.get_console()


def set_console(console: Console):
    """Updates the active Rich Console instance."""
    Scribe.consecrate_console(console)


class Scribe:
    """
    =================================================================================
    == THE HYPER-SENTIENT GOD-ENGINE OF GNOSTIC PROCLAMATION                       ==
    =================================================================================
    The Scribe is not merely a logger; it is a Context-Aware Event Bus.
    """
    _console_instance: Optional[Console] = None
    _cache_lock = threading.Lock()

    # Context Stacks for Visual Indentation
    _context: threading.local = threading.local()

    # Performance Tracking
    _last_log_time: threading.local = threading.local()

    def __init__(self, module_name: str, **kwargs):
        self.module_name = module_name.upper()
        self.logger = logging.getLogger(self.module_name)
        # Ensure propagation if root logger is configured by the host
        self.logger.propagate = True

    @property
    def is_verbose(self) -> bool:
        """
        [THE FIX]
        Proclaims whether the verbose/debug mode is active.
        Used by Conductors to decide whether to log deep Gnosis.
        """
        return _COSMIC_GNOSIS["verbose"]

    @classmethod
    def get_console(cls) -> Console:
        with cls._cache_lock:
            return cls._console_instance or _CONSOLE

    @classmethod
    def consecrate_console(cls, console: Console):
        with cls._cache_lock:
            cls._console_instance = console

    @classmethod
    def register_hook(cls, callback: Callable[[Dict], None]):
        """Registers a callback to receive structured log events."""
        _LOG_HOOKS.append(callback)

    @classmethod
    def get_history(cls) -> List[Dict]:
        """Retrieves the memories of the Scribe."""
        return list(_MEMORY_BUFFER)

    @classmethod
    def configure_cosmic_gnosis(cls, verbose: bool, silent: bool = False, log_file: Optional[Path] = None,
                                json_mode: bool = False):
        """
        Configures the global state of the logging system.
        Should be called once at the start of the application lifecycle.
        """
        _COSMIC_GNOSIS["verbose"] = verbose
        _COSMIC_GNOSIS["silent"] = silent
        _COSMIC_GNOSIS["json_mode"] = json_mode

        # Configure Standard Python Logging
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        # Remove existing handlers to prevent echo chambers
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)

        if log_file:
            try:
                # Elevation 7: Self-Healing File Handler
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(formatter)
                root_logger.addHandler(file_handler)
            except Exception as e:
                # Degrade gracefully to stderr if file access fails
                sys.stderr.write(f"Failed to initialize log file: {e}\n")

        # Note: We do NOT add a StreamHandler to root_logger because
        # Scribe handles console output manually via Rich.

    def _redact(self, message: str) -> str:
        """
        [ELEVATION 2] The Secret Redactor.
        Masks sensitive information based on regex patterns.
        """
        redacted_msg = message
        for pattern in _SECRET_PATTERNS:
            redacted_msg = re.sub(pattern, r'\1: [REDACTED]', redacted_msg)
        return redacted_msg

    def progress(self, task: str, current: int, total: int, message: str = "", **kwargs):
        """
        [THE KINETIC PULSE]
        Proclaims the status of a long-running Rite (TELEMETRY).

        This method bridges the gap between the Terminal and the Cockpit:
        1. Console: Renders a textual progress bar.
        2. Daemon: Emits a structured 'scaffold/progress' event to the UI.
        """
        # 1. The Calculus of Completion
        # We guard against the Void (Zero Division) and clamp to 0-100.
        safe_total = max(1, total)
        percent = min(100, max(0, int((current / safe_total) * 100)))

        # 2. The Gnostic Payload
        # This structure aligns with the UI's expectation for progress events.
        # We allow an optional 'id' in kwargs to track parallel tasks.
        payload = {
            "id": kwargs.pop("id", "global-progress"),
            "task": task,
            "title": task,  # UI often expects 'title'
            "current": current,
            "total": safe_total,
            "message": message,
            "percentage": percent,
            "done": current >= safe_total
        }

        # 3. Tag Alchemy
        # We extract user tags and inject the sacred 'PROGRESS' and 'KINETIC' sigils.
        # 'KINETIC' allows the Gatekeeper/Akashic engine to apply specific rate limits if needed.
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]
        final_tags = ["PROGRESS", "KINETIC"] + user_tags

        # 4. The Visual Manifestation (Console)
        # We forge a humble ASCII bar for the terminal observer.
        # Example: Task: [▓▓▓▓▓░░░░░] 50% | Details...
        bar_width = 15
        filled = int((percent / 100) * bar_width)
        bar = f"{'▓' * filled}{'░' * (bar_width - filled)}"

        display_msg = f"{task}: [{bar}] {percent}%"
        if message:
            display_msg += f" | {message}"

        # 5. The Proclamation
        # We use style="blue" to denote kinetic, non-permanent activity.
        self._proclaim(
            "INFO",
            display_msg,
            style="blue",
            tags=final_tags,
            extra_payload=payload,
            **kwargs
        )

    def _proclaim(self, level_name: str, *objects: Any, style: str = "white",
                  tags: List[str] = None, extra_payload: Dict = None,
                  bare: bool = False, **kwargs):
        """
        =============================================================================
        == THE RITE OF PROCLAMATION (V-Ω-THREAD-SAFE-FIXED)                        ==
        =============================================================================
        The internal engine of output. It orchestrates the simultaneous writing to:
        1. The Console (The Architect's Eye) - Mutable Form (Bare vs Luminous).
        2. The File (The Forensic Log) - Immutable Form (Always Detailed + TraceID).
        3. The Neural Link (The Daemon's Mind) - Structured Form (JSON Events + TraceID).

        [FIX]: Now performs Atomic Thread Hydration to prevent AttributeError on new threads.
        """
        # 0. Silence Check (The Ward of Quietude)
        if _COSMIC_GNOSIS["silent"] and level_name not in ['ERROR', 'AUDIT', 'CRITICAL']:
            return

        # 1. The Membrane of Argument Segregation
        std_log_kwargs = {
            k: v for k, v in kwargs.items()
            if k in ['exc_info', 'stack_info', 'stacklevel', 'extra']
        }

        # 2. The Retrieval of the Silver Cord (Distributed Tracing)
        trace_id: Optional[str] = None
        try:
            if 'scaffold.core.runtime.middleware.tracing' in sys.modules:
                from .core.runtime.middleware.tracing import get_current_trace_id
                trace_id = get_current_trace_id()
        except ImportError:
            pass

        # 3. Chronometry & Context (The Pulse of Time - THREAD SAFE FIX)
        # Ensure the thread-local storage container exists on the class
        if not hasattr(Scribe, '_thread_local'):
            Scribe._thread_local = threading.local()

        # [THE FIX]: Hydrate the specific thread's timeline if it is a new soul
        if not hasattr(Scribe._thread_local, 'last_log_time'):
            Scribe._thread_local.last_log_time = time.time()

        if not hasattr(Scribe._thread_local, 'context_stack'):
            Scribe._thread_local.context_stack = []

        # Calculate Delta
        now = time.time()
        delta = now - Scribe._thread_local.last_log_time
        Scribe._thread_local.last_log_time = now

        # Calculate Indentation
        indent_depth = len(Scribe._thread_local.context_stack)
        indent_str = "  " * indent_depth

        # 4. The Rite of Stringification
        message_parts = []
        for obj in objects:
            if isinstance(obj, (dict, list)) and not _COSMIC_GNOSIS["json_mode"]:
                try:
                    message_parts.append(json.dumps(obj, default=str))
                except:
                    message_parts.append(str(obj))
            else:
                message_parts.append(str(obj))
        raw_message = " ".join(message_parts)

        # 5. The Veil (Secret Redaction)
        clean_message = self._redact(raw_message)

        # 6. The Rite of File Persistence (Immutable History)
        if hasattr(self, 'logger'):
            log_method = getattr(self.logger, level_name.lower(), self.logger.info)

            file_msg = f"{indent_str}{clean_message}"
            if trace_id:
                file_msg = f"[T:{trace_id}] {file_msg}"
            if tags:
                file_msg += f" [{', '.join(tags)}]"

            log_method(file_msg, **std_log_kwargs)

        # 7. The Rite of Console Revelation (The Visual Interface)
        console = self.get_console()

        # [PATH A: THE MACHINE GAZE]
        if _COSMIC_GNOSIS["json_mode"]:
            json_record = {
                "timestamp": now,
                "level": level_name,
                "module": self.module_name,
                "trace_id": trace_id,
                "message": clean_message,
                "context": Scribe._thread_local.context_stack,
                "tags": tags or [],
                "delta": delta,
                "data": extra_payload
            }
            print(json.dumps(json_record))
            if hasattr(sys.stdout, 'flush'): sys.stdout.flush()
            _MEMORY_BUFFER.append(json_record)
            return

        # [PATH B: THE HUMAN GAZE]
        if bare:
            # --- THE NAKED VOICE ---
            text_obj = Text.from_markup(clean_message)
            console.print(text_obj)
        else:
            # --- THE LUMINOUS VOICE ---
            timestamp = time.strftime("%H:%M:%S")

            # Performance Heatmap
            delta_str = ""
            if delta > 1.0:
                delta_str = f"[bold red](+{delta:.2f}s)[/bold red] "
            elif delta > 0.1:
                delta_str = f"[dim](+{delta:.2f}s)[/dim] "

            # Trace Visualization
            trace_str = ""
            if trace_id:
                short_trace = trace_id.split('-')[-1][:6]
                trace_str = f"[dim blue]T:{short_trace}[/dim blue] "

            # Prefix
            prefix = f"[dim]{timestamp}[/dim] {delta_str}{trace_str}[[{style}]{self.module_name}[/{style}]] "

            # Message Construction
            text_obj = Text.from_markup(f"{prefix}{clean_message}")
            if tags:
                for tag in tags:
                    tag_style = "dim magenta"
                    if tag == "HERESY":
                        tag_style = "bold red"
                    elif tag == "SUCCESS":
                        tag_style = "bold green"
                    elif tag == "SYSTEM":
                        tag_style = "bold cyan"

                    text_obj.append(f" #{tag}", style=tag_style)

            # Render
            console.print(Padding(text_obj, (0, 0, 0, indent_depth * 2)))

        # 8. The Rite of Visual Paradox (Exception Rendering)
        if kwargs.get('exc_info') or kwargs.get('ex'):
            exc = kwargs.get('ex')
            if exc:
                console.print(Traceback.from_exception(
                    type(exc), exc, exc.__traceback__,
                    show_locals=False, width=100
                ))

        # 9. The Telepathic Link (Neural Pulse)
        # [NARCISSUS GUARD]
        if tags and "INTERNAL_BRIDGE" in tags:
            return

        payload = {
            "timestamp": now,
            "level": level_name,
            "module": self.module_name,
            "trace_id": trace_id,
            "message": clean_message,
            "tags": tags or [],
            "data": extra_payload
        }

        _MEMORY_BUFFER.append(payload)

        for hook in _LOG_HOOKS:
            try:
                hook(payload)
            except Exception:
                pass

    def system(self, *objects, bare=False, **kwargs):
        """
        [THE SYSTEM CHANNEL] (V-Ω-INFRASTRUCTURE-VOICE)
        LIF: INFINITY | Logs high-level lifecycle events (Startup, Shutdown, Signals).

        This method maps to the INFO level but injects specific semantic tags
        that allow the Akashic Record to route these logs to the 'System'
        telemetry stream in the UI, distinct from standard application logs.
        """
        # 1. Extract User Tags (The Merge)
        # We POP the tags from kwargs to prevent the 'multiple values' TypeError
        # when passing them explicitly to _proclaim.
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Forge the Semantic Tags
        # We ensure 'SYSTEM' is present for UI filtering.
        final_tags = ["SYSTEM"] + user_tags

        # 3. The Narcissus Guard (Echo Filter)
        # 'INTERNAL_BRIDGE' prevents the Akashic Record from echo-looping this log
        # if it originated from the broadcasting logic itself.
        # We allow a manual override via 'recursive=True' in rare debugging cases.
        if "INTERNAL_BRIDGE" not in final_tags and not kwargs.pop("recursive", False):
            final_tags.append("INTERNAL_BRIDGE")

        # 4. The Proclamation
        # We map "SYSTEM" to a distinct visual style (Bold Cyan) to stand out
        # against standard INFO logs in the console.
        self._proclaim(
            "SYSTEM",
            *objects,
            style="bold cyan",
            tags=final_tags,
            bare=bare,
            **kwargs
        )

    def _trigger_hooks(self, level: str, message: str, extra: dict):
        """
        Executes any registered callbacks (e.g. Akashic Broadcast).
        """
        if hasattr(self.__class__, '_hooks'):
            packet = {
                "level": level,
                "message": message,
                "module": self.name if hasattr(self, 'name') else "Scribe",
                "timestamp": __import__('time').time(),
                "tags": extra.get('tags', []),
                "data": extra.get('data', None)
            }
            for hook in self.__class__._hooks:
                try:
                    hook(packet)
                except Exception:
                    pass


    def _render_visual_paradox(self, exc_info_arg: Any, explicit_ex: Any):
        """Helper to render rich tracebacks if an exception occurred."""
        if not RICH_AVAILABLE: return

        # Determine if there is an exception to render
        exception_obj = explicit_ex
        if exc_info_arg is True and exception_obj is None:
            exception_obj = sys.exc_info()[1]
        elif isinstance(exc_info_arg, tuple):
            # We have a tuple info, Rich can handle this via from_exception args
            pass

            # If no exception context, we exit
        if not exception_obj and not isinstance(exc_info_arg, tuple):
            return

        console = self.get_console()
        try:
            show_locals = self.is_verbose

            if exception_obj:
                trace_renderable = Traceback.from_exception(
                    type(exception_obj), exception_obj, exception_obj.__traceback__,
                    show_locals=show_locals, width=100
                )
            elif isinstance(exc_info_arg, tuple):
                trace_renderable = Traceback.from_exception(
                    exc_info_arg[0], exc_info_arg[1], exc_info_arg[2],
                    show_locals=show_locals, width=100
                )
            else:
                return

            panel = Panel(
                trace_renderable,
                title=f"[bold red]Paradox in {self.module_name}[/bold red]",
                border_style="red"
            )
            console.print(Padding(panel, (0, 0, 0, 2)))
        except Exception:
            # Fallback if Rich fails
            if exception_obj: traceback.print_exc()

    # --- THE PUBLIC API (UNIVERSAL SIGNATURES) ---
    def info(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE STANDARD CHANNEL]
        Proclaims standard Gnosis (INFO).
        The baseline reality of the application.
        """
        # 1. Extraction (Prevent Collision)
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Proclamation
        self._proclaim("INFO", *objects, tags=user_tags, bare=bare, **kwargs)

    def success(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE VICTORY CHANNEL]
        Proclaims a triumph (INFO + SUCCESS tag).
        Used when a Rite is completed or a Reality is anchored.
        """
        # 1. Extraction
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Enrichment
        final_tags = ["SUCCESS"] + user_tags

        # 3. Proclamation (Green Aura)
        self._proclaim(
            "INFO",
            *objects,
            style="success",
            tags=final_tags,
            bare=bare,
            **kwargs
        )

    def warn(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE CAUTIONARY CHANNEL]
        Proclaims a non-fatal paradox (WARNING).
        Used for deprecations, retries, or near-misses.
        """
        # 1. Extraction
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Enrichment
        final_tags = ["WARNING"] + user_tags

        # 3. Proclamation (Amber Aura)
        self._proclaim(
            "WARNING",
            *objects,
            style="warning",
            tags=final_tags,
            bare=bare,
            **kwargs
        )

    def verbose(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE DEEP GAZE CHANNEL]
        Proclaims high-frequency detail (DEBUG).
        Only manifests if the 'verbose' flag is hoisted.
        """
        # 0. The Gate of Silence (Optimization)
        if not self.is_verbose:
            return

        # 1. Extraction
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Proclamation (Cyan Aura)
        self._proclaim(
            "DEBUG",
            *objects,
            style="verbose",
            tags=user_tags,
            bare=bare,
            **kwargs
        )

    def debug(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE HIDDEN WISDOM CHANNEL]
        Proclaims structural secrets (DEBUG).
        Used for internal state dumps and variable inspection.
        """
        # 1. Extraction
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Proclamation (Dim Aura)
        # Note: Debug logs are always written to the File, even if not printed to Console
        self._proclaim(
            "DEBUG",
            *objects,
            style="dim",
            tags=user_tags,
            bare=bare,
            **kwargs
        )

    def error(self, *objects: Any, ex: Optional[BaseException] = None, tags: List[str] = None, bare: bool = False,
              **kwargs):
        """
        =============================================================================
        == THE PROCLAMATION OF HERESY (V-Ω-RESILIENT-BARE-AWARE)                   ==
        =============================================================================
        Proclaims an error to the cosmos.

        Faculties:
        1.  **The Tag Alchemist:** Merges explicit tags, kwargs tags, and the sacred 'HERESY' tag without collision.
        2.  **The Unified Exception Handler:** Intelligently extracts exception info from arguments, `sys.exc_info`, or the explicit `ex` parameter.
        3.  **The Visual Paradox Renderer:** If Rich is available, it renders a beautiful, syntax-highlighted traceback panel.
        4.  **The Recursion Guard:** Wraps rendering in a safety block to prevent logging errors from masking the original heresy.
        """
        # 1. The Tag Alchemist (The Fix)
        # We pop tags from kwargs to prevent the 'multiple values' collision
        # and merge them with the explicit argument and the sacred mark.
        kwarg_tags = kwargs.pop('tags', [])
        if not isinstance(kwarg_tags, list): kwarg_tags = [str(kwarg_tags)]

        explicit_tags = tags or []
        if not isinstance(explicit_tags, list): explicit_tags = [str(explicit_tags)]

        final_tags = ["HERESY"] + explicit_tags + kwarg_tags

        # 2. The Unified Exception Handler
        # Determine if we have an exception context
        exc_info = kwargs.get('exc_info', False)
        exception_obj = ex

        # If exc_info=True but no object passed, get it from sys (The Invisible Catch)
        if exc_info is True and exception_obj is None:
            exception_obj = sys.exc_info()[1]

        # If ex passed, ensure the underlying logger receives it for file persistence
        if exception_obj and 'exc_info' not in kwargs:
            kwargs['exc_info'] = exception_obj

        # 3. The Proclamation
        # We delegate the actual writing to the inner engine.
        self._proclaim("ERROR", *objects, style="error", tags=final_tags, bare=bare, **kwargs)

        # 4. The Visual Paradox Renderer (Rich)
        # We render the traceback explicitly here to allow for the custom Title and Border style.
        # This runs ONLY if we are not silent and Rich is available.
        if RICH_AVAILABLE and not _COSMIC_GNOSIS["silent"] and not bare:
            # Check if we have something to render
            has_trace = exception_obj or (isinstance(exc_info, tuple) and len(exc_info) == 3)

            if has_trace:
                console = self.get_console()
                try:
                    # [RECURSION GUARD]: If verbose is off, hide locals to prevent infinite depth crashes
                    show_locals = self.is_verbose

                    if exception_obj:
                        trace_renderable = Traceback.from_exception(
                            type(exception_obj), exception_obj, exception_obj.__traceback__,
                            show_locals=show_locals, width=100
                        )
                    elif isinstance(exc_info, tuple):
                        trace_renderable = Traceback.from_exception(
                            exc_info[0], exc_info[1], exc_info[2],
                            show_locals=show_locals, width=100
                        )
                    else:
                        # Fallback for implicit contexts
                        trace_renderable = Traceback(show_locals=show_locals, width=100)

                    panel = Panel(
                        trace_renderable,
                        title=f"[bold red]Paradox in {self.module_name}[/bold red]",
                        border_style="red"
                    )
                    console.print(Padding(panel, (0, 0, 0, 2)))

                except Exception as render_error:
                    # [FALLBACK]: The Safe Mode
                    # If the fancy renderer fails, we must still proclaim the truth to stderr.
                    sys.stderr.write(f"\n[CRITICAL LOGGER FAILURE] Visual Paradox engine fractured: {render_error}\n")
                    sys.stderr.write(f"Original Error Context: {objects}\n")
                    if exception_obj:
                        traceback.print_exc()

    def critical(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE RED ALERT]
        Proclaims a catastrophic state (CRITICAL).
        Bypasses all silence filters. Used for panic states, corruption, and crash dumps.
        """
        # 1. Extraction (Prevent Collision)
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Enrichment
        final_tags = ["CRITICAL"] + user_tags

        # 3. Proclamation (Red Background / High Contrast)
        self._proclaim(
            "CRITICAL",
            *objects,
            style="danger",
            tags=final_tags,
            bare=bare,
            **kwargs
        )

    def audit(self, *objects: Any, bare: bool = False, **kwargs):
        """
        [THE FORENSIC LEDGER]
        Secure Log for Security Events (CRITICAL Level).
        Always logs, regardless of silence settings.
        Used for auth tokens, permission changes, and Gnostic boundary crossings.
        """
        # 1. Extraction
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list): user_tags = [str(user_tags)]

        # 2. Enrichment (Enforce Security Context)
        # We implicitly add 'SECURITY' to all audits for easy grep/filtering later.
        final_tags = ["AUDIT", "SECURITY"] + user_tags

        # 3. Proclamation (Gold / Inverse Style)
        self._proclaim(
            "CRITICAL",
            *objects,
            style="audit",
            tags=final_tags,
            bare=bare,
            **kwargs
        )

    @contextmanager
    def indent(self, title: str = None):
        """
        Visual Hierarchy Context Manager.

        Usage:
            with scribe.indent("Processing..."):
                scribe.info("Step 1")

        Result:
            ┌── Processing...
              ℹ️ Step 1
            └──
        """
        if not hasattr(Scribe._context, 'stack') or Scribe._context.stack is None:
            Scribe._context.stack = []

        Scribe._context.stack.append(title or "Block")

        # Calculate indent for the brackets
        depth = len(Scribe._context.stack) - 1
        indent_str = "  " * depth

        if title and not _COSMIC_GNOSIS["silent"]:
            self.get_console().print(f"[dim]{indent_str}┌── {title}[/dim]")

        try:
            yield
        finally:
            if title and not _COSMIC_GNOSIS["silent"]:
                self.get_console().print(f"[dim]{indent_str}└──[/dim]")

            if Scribe._context.stack:
                Scribe._context.stack.pop()


# --- THE DIVINE RESTORATION: THE MODULE-LEVEL GATEWAY ---

# --- THE GLOBAL LOCK ---
_config_lock = threading.Lock()


def configure_logging(
        verbose: bool = False,
        silent_console: bool = False,
        log_file: Optional[Union[str, Path]] = None,
        json_mode: bool = False
):
    """
    [THE RITE OF STREAM GOVERNANCE]
    Configures the Gnostic Scribe and the global logging nervous system.

    Ensures that for LSP and Daemon sessions, the stdout conduit remains
    pure and unprofaned by human-readable text.
    """
    global _config_lock

    with _config_lock:
        # --- MOVEMENT I: ENVIRONMENT SCRYING ---
        # Allow environment variables to force a state of silence or verbosity
        if os.environ.get("SCAFFOLD_SILENT") == "1":
            silent_console = True
        if os.environ.get("SCAFFOLD_VERBOSE") == "1":
            verbose = True

        # --- MOVEMENT II: ROOT PURIFICATION ---
        # Clear all existing handlers to prevent duplicate messages or
        # unwanted noise from 3rd party libraries.
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Set the threshold of perception
        level = logging.DEBUG if verbose else logging.INFO
        root_logger.setLevel(level)

        # --- MOVEMENT III: FORMAT FORGING ---
        # [ASCENSION 11]: Luminous metadata strings
        if json_mode:
            # Atomic JSON format for machine parsing
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "name": "%(name)s", '
                '"level": "%(levelname)s", "pid": %(process)d, '
                '"thread": "%(threadName)s", "message": "%(message)s"}'
            )
        else:
            # Human-readable Luminous format
            formatter = logging.Formatter(
                '%(asctime)s [PID:%(process)d] [%(threadName)s] '
                '%(levelname)-8s %(name)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        # --- MOVEMENT IV: CONDUIT ASSEMBLY ---

        # 1. THE CONSOLE (Only if not silenced)
        # [ASCENSION 1]: The Stdout Quarantine
        if not silent_console:
            # We use stderr for human-readable console logs to keep
            # stdout reserved for potential JSON-RPC or piped data.
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            root_logger.addHandler(console_handler)

        # 2. THE SCROLL (File Logging)
        # [ASCENSION 5 & 7]: Rotation and UTF-8 enforcement
        if log_file:
            log_path = Path(log_file).resolve()
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # Rotate at 10MB, keep 5 backups
            file_handler = RotatingFileHandler(
                filename=str(log_path),
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'  # [ASCENSION 7]
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            root_logger.addHandler(file_handler)

        # --- MOVEMENT V: THE GLOBAL INTERCEPTOR ---
        # [ASCENSION 10 & 12]: Hardened Exception Hook
        _original_hook = sys.excepthook

        def _gnostic_excepthook(type_, value, traceback_):
            # Guard against recursive failure if logging itself is broken
            try:
                crash_scribe = logging.getLogger("SystemKernel")
                # Capture the full traceback soul
                crash_scribe.critical(
                    f"Unhandled Process Crash: {value}",
                    exc_info=(type_, value, traceback_)
                )
            except Exception:
                # Absolute last resort fallback to raw stderr
                sys.stderr.write(f"CRITICAL: Logging failed during crash: {value}\n")

            # Preserve standard Python behavior
            if _original_hook:
                _original_hook(type_, value, traceback_)

        sys.excepthook = _gnostic_excepthook

        # --- MOVEMENT VI: SCRIBE SYNCHRONIZATION ---
        # Update the Scribe's internal Gnosis so future instances are born configured
        try:
            from .logger import Scribe
            # [ASCENSION 12]: Class-level state mutation
            Scribe.configure_cosmic_gnosis(verbose, silent_console, log_file, json_mode)
        except (ImportError, AttributeError):
            # Fallback if Scribe is not yet manifest in the namespace
            pass

        # Proclaim success to the internal log (now safe in stderr or file)
        root_logger.debug("Gnostic Logging System Manifested. Stream Purity Verified.")



__all__ = ["Scribe", "get_console", "set_console", "configure_logging", "SCRIBE_THEME"]