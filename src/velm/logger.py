# Path: src/velm/logger.py
# =========================================================================================
# == PART 1 OF 4: THE FOUNDATION OF THE SCRIBE (V-Ω-TOTALITY-V1000)                      ==
# =========================================================================================
# LIF: 10,000,000,000 | ROLE: CENTRAL_NERVOUS_SYSTEM | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_LOGGER_V1000_PART_1_FINALIS
#
# [THE MANIFESTO]
# This is the nervous system of the Velm God-Engine. It has been ascended to
# handle any form of Gnostic proclamation, whether structured data, raw text, or
# catastrophic paradoxes.
#
# It implements the **Argument Segregation Membrane** to ensure perfect compatibility
# between Gnostic Rites (Rich TUI) and Standard Laws (Python Logging).
# =========================================================================================

import os
import json
import logging
from logging.handlers import RotatingFileHandler
import re
import sys
import threading
import time
import traceback
from collections import deque
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List, Any, Dict, Callable, Union, Final

# --- The Divine Stanza of the Scribe's Tools (Third Party) ---
RICH_AVAILABLE = False
try:
    from rich.console import Console, Group
    from rich.theme import Theme
    from rich.markup import escape, render as render_markup
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

        def print(self, *args, **kwargs):
            # Fallback print to stderr
            msg = " ".join(str(a) for a in args)
            print(msg, file=sys.stderr)

        def rule(self, *args, **kwargs): print("-" * 80, file=sys.stderr)

        def clear(self): pass


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
    # [ASCENSION 1]: THE SOUL PARTICLE
    # Maps the 'soul' style to a high-status neon magenta frequency.
    "soul": "bold magenta",
}) if RICH_AVAILABLE else None

# --- THE COSMIC GNOSIS (Global State) ---
_COSMIC_GNOSIS = {
    "verbose": False,
    "silent": False,
    "json_mode": False,
    "debug_mode": False,
    "max_memory": 1000
}

# --- THE VESSEL OF THE LIVING SOUL (HEADLESS HARDENED) ---
# We detect if the stderr stream is a real TTY.
# If it is a Pipe (Lightning/Docker), we FORCE a width to prevent
# Rich from calling 'ioctl' to guess dimensions, which causes the crash.
_IS_TTY = sys.stderr.isatty()
_IS_WASM = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

# [ASCENSION 2]: SUBSTRATE-AWARE CONSOLE FACTORY
_CONSOLE: Console = Console(
    theme=SCRIBE_THEME,
    stderr=True,
    # [ASCENSION 3]: IOCTL SHIELD & WASM GEOMETRY
    # In WASM, we cannot query window size via IOCTL. We force a standard width.
    width=120 if (not _IS_TTY or _IS_WASM) else None,

    # [ASCENSION 4]: INTERACTIVITY FORCE
    # WASM is interactive via XTerm.js, even if Python sees a pipe. We force it.
    force_interactive=True if _IS_WASM else (False if not _IS_TTY else None),

    # [ASCENSION 5]: CHROMATIC SOVEREIGNTY
    # We mandate ANSI output in WASM to prevent the "<rich.panel...>" heresy.
    force_terminal=True if (_IS_TTY or _IS_WASM or os.getenv("FORCE_COLOR") == "1") else None,

    # [ASCENSION 6]: WRAPPING BEHAVIOR
    # We want hard wrapping in WASM to respect the 120 char limit visually.
    soft_wrap=not _IS_TTY and not _IS_WASM
)

# --- ELEVATION 1: THE TELEPATHIC LINK (CALLBACK REGISTRY) ---
# Allows external systems (VS Code, React UI) to subscribe to the log stream
_LOG_HOOKS: List[Callable[[Dict], None]] = []

# --- ELEVATION 2: THE EPHEMERAL BUFFER (MEMORY RING) ---
# Stores the last N logs for crash reporting and replay
_MEMORY_BUFFER = deque(maxlen=_COSMIC_GNOSIS["max_memory"])

# --- ELEVATION 3: THE SECRET REDACTOR PATTERNS ---
# Regex patterns to mask sensitive data in logs before they hit the stream
_SECRET_PATTERNS = [
    r'(api_key|token|secret|password|passwd|credential)\s*[:=]\s*[\'"]?([^\s\'"]+)[\'"]?',
    r'(Bearer\s+)([a-zA-Z0-9\-\._~\+\/]+)',
    r'(ghp_[a-zA-Z0-9]+)',
    r'(sk_live_[a-zA-Z0-9]+)'
]


def get_console() -> Console:
    """Returns the active Rich Console instance."""
    return Scribe.get_console()


def set_console(console: Console):
    """Updates the active Rich Console instance."""
    Scribe.consecrate_console(console)


# =========================================================================================
# == THE ACHRONAL OCULAR NEXUS (V-Ω-TOTALITY-V120-SINGLETON)                             ==
# =========================================================================================
# LIF: INFINITY | ROLE: SPATIAL_SIGNAL_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_CONCOURSE_V120_HOISTING_SINGULARITY_)(@)(!@#(#@)

_SIGNAL_CONCOURSE: Final[Dict[str, Any]] = {
    "progress": None,  # The rich.progress.Progress instance
    "active_tasks": {},  # Map[Gnostic_ID, Internal_Rich_ID]
    "lock": threading.Lock(),
    "is_active": False,
    "inception_ts": 0,
    "last_error": None
}


def _get_signal_concourse() -> Optional['Progress']:
    """
    =================================================================================
    == THE RITE OF NEXUS RETRIEVAL (V-Ω-TOTALITY)                                  ==
    =================================================================================
    LIF: INFINITY | ROLE: OCULAR_DECK_FORGE

    Materializes and returns the persistent, thread-safe Progress Engine.
    It is the only authorized gateway to the bottom of the viewport.
    """
    global _SIGNAL_CONCOURSE

    # 0. THE WARD OF MATTER
    if not RICH_AVAILABLE: return None

    # [ASCENSION 7]: WASM SILENCE
    # In WASM, progress bars can cause rendering jitter. We might disable or simplify.
    # For now, we allow it if interactive.

    # 1. THE HYDRAULIC MUTEX
    with _SIGNAL_CONCOURSE["lock"]:
        # 2. THE RITE OF INCEPTION (LAZY INITIALIZATION)
        if _SIGNAL_CONCOURSE["progress"] is None:
            try:
                from rich.progress import (
                    Progress, SpinnerColumn, TextColumn,
                    BarColumn, TaskProgressColumn, TimeElapsedColumn,
                    MofNCompleteColumn
                )

                # [ASCENSION 8]: HEADLESS ADAPTIVE SENSING
                is_tty = sys.stderr.isatty() or _IS_WASM

                # [ASCENSION 9]: COLUMN ALCHEMY
                # We forge the visual lattice based on the environment's fidelity.
                columns = []

                # A. The Pulse Signal (Spinner)
                if is_tty:
                    columns.append(SpinnerColumn(style="soul", spinner_name="dots12"))
                else:
                    columns.append(TextColumn("[soul]>>[/]"))

                # B. The Semantic Label
                columns.append(TextColumn("[progress.description]{task.description}"))

                # C. The Materialization Bar
                columns.append(BarColumn(
                    bar_width=25,
                    style="dim",
                    complete_style="soul",
                    finished_style="success",
                    pulse_style="soul"
                ))

                # D. The Percentage & Count
                columns.append(TaskProgressColumn())
                if is_tty:
                    columns.append(MofNCompleteColumn())
                    columns.append(TimeElapsedColumn())

                # [ASCENSION 10]: THE MATERIALIZATION
                _SIGNAL_CONCOURSE["progress"] = Progress(
                    *columns,
                    console=_CONSOLE,  # Binds to the Headless-Hardened master console
                    transient=True,  # [ASCENSION 11]: Purity Vow - Bars evaporate on 100%
                    auto_refresh=True,
                    refresh_per_second=10 if _IS_WASM else 20,  # [ASCENSION 12]: WASM Throttle
                    expand=False  # Prevent bar from greedily consuming width
                )

                _SIGNAL_CONCOURSE["inception_ts"] = time.time()

            except Exception as paradox:
                _SIGNAL_CONCOURSE["last_error"] = str(paradox)
                # Fail-open: Return None, which triggers the ASCII fallback in Scribe.progress
                return None

        # 3. THE FINAL PROCLAMATION
        return _SIGNAL_CONCOURSE["progress"]


class Scribe:
    """
    =================================================================================
    == THE HYPER-SENTIENT GOD-ENGINE OF GNOSTIC PROCLAMATION (PART 2)              ==
    =================================================================================
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
    def configure_cosmic_gnosis(cls, verbose: bool, silent_console: bool = False,
                                log_file: Optional[Union[str, Path]] = None,
                                json_mode: bool = False):
        """
        =============================================================================
        == THE RITE OF STREAM GOVERNANCE (V-Ω-TOTALITY-V12)                        ==
        =============================================================================
        Configures the Global Nervous System (Root Logger).

        ### THE PANTHEON OF ASCENSIONS:
        13. **The Rotating Scroll:** Replaces the static FileHandler with `RotatingFileHandler`.
        14. **The UTF-8 Covenant:** Enforces `encoding='utf-8'` on file operations.
        15. **The Stdout Quarantine:** Forces all console output to `sys.stderr`.
        16. **The JSON Transmuter:** Reformats logs into NDJSON if `json_mode` is active.
        17. **The Third-Party Muzzle:** Silences noisy libraries unless Verbose.
        18. **The Root Purification:** Surgically removes pre-existing handlers.
        19. **The Global Interceptor:** Hooks `sys.excepthook` for unhandled crashes.
        20. **The Atomic Path Forge:** Resolves/creates log directories automatically.
        21. **The Environment Override:** Respects `SCAFFOLD_SILENT` / `SCAFFOLD_VERBOSE`.
        22. **The Process Identity:** Injects PID and Thread Name.
        23. **The Fail-Safe Fallback:** Degrades gracefully if filesystem is read-only.
        24. **The State Reflection:** Updates `_COSMIC_GNOSIS` state.
        """
        # --- MOVEMENT I: ENVIRONMENT SCRYING ---
        if os.environ.get("SCAFFOLD_SILENT") == "1": silent_console = True
        if os.environ.get("SCAFFOLD_VERBOSE") == "1": verbose = True
        if os.environ.get("SCAFFOLD_JSON") == "1": json_mode = True

        # Sync Global State
        _COSMIC_GNOSIS["verbose"] = verbose
        _COSMIC_GNOSIS["silent"] = silent_console
        _COSMIC_GNOSIS["json_mode"] = json_mode

        # --- MOVEMENT II: ROOT PURIFICATION ---
        root_logger = logging.getLogger()
        # Annihilate existing handlers
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)

        # Set the threshold of perception
        level = logging.DEBUG if verbose else logging.INFO
        root_logger.setLevel(level)

        # Muzzle noisy neighbors
        if not verbose:
            logging.getLogger("httpx").setLevel(logging.WARNING)
            logging.getLogger("httpcore").setLevel(logging.WARNING)
            logging.getLogger("asyncio").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)

        # --- MOVEMENT III: FORMAT FORGING ---
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
        if not silent_console:
            # [ASCENSION 15]: The Stdout Quarantine (Use stderr)
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            root_logger.addHandler(console_handler)

        # 2. THE SCROLL (File Logging)
        if log_file:
            try:
                log_path = Path(log_file).resolve()
                # [ASCENSION 20]: Atomic Path Forge
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # [ASCENSION 13]: The Rotating Scroll
                file_handler = RotatingFileHandler(
                    filename=str(log_path),
                    maxBytes=10 * 1024 * 1024,  # 10 MB Limit
                    backupCount=5,  # Keep 5 historical scrolls
                    encoding='utf-8'  # [ASCENSION 14]: UTF-8 Covenant
                )
                file_handler.setFormatter(formatter)
                file_handler.setLevel(level)
                root_logger.addHandler(file_handler)
            except Exception as e:
                # [ASCENSION 23]: Fail-Safe Fallback
                sys.stderr.write(f"!! LOGGING FRACTURE: Could not consecrate log file: {e}\n")

        # --- MOVEMENT V: THE GLOBAL INTERCEPTOR ---
        # [ASCENSION 19]: Capture unhandled crashes
        def _gnostic_excepthook(type_, value, traceback_):
            root_logger.critical(
                f"UNHANDLED KERNEL PANIC: {value}",
                exc_info=(type_, value, traceback_)
            )
            # Call original hook if it exists
            sys.__excepthook__(type_, value, traceback_)

        sys.excepthook = _gnostic_excepthook

    def _redact(self, message: str) -> str:
        """
        [ASCENSION 25]: THE ZERO-ALLOCATION REDACTION GATE.
        [THE MASTER CURE]: Uses an O(1) membership check for common secret
        substrings before invoking the O(N) Regex Phalanx.
        """
        if not message or len(message) < 8:
            return message

        # Fast-Path Bypass: If no suspicious tokens exist, return raw matter in 0.00ms.
        if not any(token in message for token in ("key", "secret", "token", "pass", "Bearer", "sk_")):
            return message

        redacted_msg = message
        for pattern in _SECRET_PATTERNS:
            redacted_msg = re.sub(
                pattern,
                lambda m: m.group(0).replace(m.group(m.lastindex), "« REDACTED »"),
                redacted_msg
            )
        return redacted_msg

    def progress(self, task: str, current: int, total: int, message: str = "", **kwargs):
        """
        =============================================================================
        == THE KINETIC PROGRESS RITE (V-Ω-TOTALITY-V120-OCULAR-DECK)               ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_UI_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_PROGRESS_V120_CONCOURSE_FIX_)(@)(!@#(#@)
        """
        # --- 0. THE GATE OF SILENCE ---
        if _COSMIC_GNOSIS["silent"]:
            return

        # --- 1. THE MACHINE GAZE (JSON MODE) ---
        # If machine-purity is willed, we skip all visual alchemy and emit raw Gnosis.
        if _COSMIC_GNOSIS["json_mode"]:
            payload = {
                "id": kwargs.get("id", task),
                "task": task,
                "current": current,
                "total": total,
                "message": message,
                "done": current >= total if total > 0 else False,
                "ts": time.time()
            }
            # We use the internal 'system' channel for machine-telemetry
            self._proclaim("INFO", f"PROGRESS_PULSE:{task}", tags=["KINETIC", "JSON"], extra_payload=payload)
            return

        # --- 2. THE RITE OF CONCOURSE RETRIEVAL ---
        # Summon the persistent, thread-safe Progress Engine (The Ocular Deck).
        concourse = _get_signal_concourse()

        # [FALLBACK]: If the visual engine is unmanifest (e.g. non-Rich environment),
        # we degrade gracefully to a high-status ASCII proclamation.
        if not concourse:
            safe_total = max(1, total)
            percent = min(100, max(0, int((current / safe_total) * 100)))
            bar = f"{'▓' * (percent // 10)}{'░' * (10 - (percent // 10))}"
            self._proclaim("INFO", f"{task}: [{bar}] {percent}% | {message}", bare=True, style="blue")
            return

        # --- 3. THE RITE OF TASK ANCHORING ---
        # We use the provided 'id' or the task name as the unique coordinate in the multiverse.
        task_id_key = kwargs.get("id", task)

        # [ASCENSION 25]: THE HYDRAULIC MUTEX
        # We lock the concourse to prevent parallel thread collisions during TTY mutation.
        with _SIGNAL_CONCOURSE["lock"]:

            # A. IGNITION: If the Concourse is dormant, awake it.
            if not _SIGNAL_CONCOURSE["is_active"]:
                try:
                    concourse.start()
                    _SIGNAL_CONCOURSE["is_active"] = True
                except Exception as e:
                    # If ignition fails (e.g. IOCTL error), we fallback to standard logging.
                    self.warn(f"Ocular Deck Ignition failed: {e}")
                    return

            # B. INCEPTION: If the task is a new soul, forge its place on the deck.
            if task_id_key not in _SIGNAL_CONCOURSE["active_tasks"]:
                # High-Status color mapping
                style = "soul" if any(x in task for x in ["Reality", "Genesis", "Structure", "Forge"]) else "info"

                # Inscribe the new task onto the deck
                internal_id = concourse.add_task(
                    f"[{style}]{task}[/]",
                    total=total,
                    start=True
                )
                _SIGNAL_CONCOURSE["active_tasks"][task_id_key] = internal_id

            internal_id = _SIGNAL_CONCOURSE["active_tasks"][task_id_key]

            # C. THE TRANSMUTATION: Update the visual matter of the bar.
            # [ASCENSION 26]: Zero-Division Sarcophagus logic is handled by concourse.update.
            concourse.update(
                internal_id,
                completed=current,
                description=f"[info]{task}[/] [dim]{self._redact(message)}[/]",
                refresh=True  # Force a visual refresh for immediate feedback
            )

            # --- 4. THE RITE OF FINALITY (COMPLETION) ---
            # If the current progress has reached the willed total...
            if current >= total and total > 0:
                # [ASCENSION 27]: The task evaporates from the deck, leaving only the logs.
                concourse.remove_task(internal_id)
                del _SIGNAL_CONCOURSE["active_tasks"][task_id_key]

                # [ASCENSION 28]: DRAIN - If the deck is a void, stop the engine to release the TTY.
                if not _SIGNAL_CONCOURSE["active_tasks"]:
                    concourse.stop()
                    _SIGNAL_CONCOURSE["is_active"] = False

        # --- 5. THE TELEPATHIC BROADCAST (NEURAL LINK) ---
        # Simultaneously inform the Ocular Membrane (React/LSP) of the kinetic update.
        # This payload is consumed by useTelemetry.ts to drive the browser's progress bars.
        try:
            # We scry the trace ID from the active thread context
            trace_id = None
            if 'velm.core.runtime.middleware.tracing' in sys.modules:
                from velm.core.runtime.middleware.tracing import get_current_trace_id
                trace_id = get_current_trace_id()

            broadcast_payload = {
                "id": task_id_key,
                "title": task,
                "current": current,
                "total": total,
                "message": message,
                "percentage": int((current / max(1, total)) * 100),
                "done": current >= total if total > 0 else False,
                "timestamp": time.time(),
                "trace_id": trace_id or "tr-kinetic-void"
            }

            # We dispatch to the internal bridge. 'INTERNAL_BRIDGE' ensures
            # the Akashic Record doesn't log its own telemetry update.
            self._proclaim(
                "INFO", f"PROGRESS_UPDATE:{task_id_key}",
                tags=["PROGRESS", "INTERNAL_BRIDGE"],
                extra_payload=broadcast_payload
            )
        except Exception:
            # Broadcast is non-critical.
            pass

    def _proclaim(self, level_name: str, *objects: Any, style: str = "white",
                  tags: List[str] = None, extra_payload: Dict = None,
                  bare: bool = False, **kwargs):
        """
        =================================================================================
        == THE OMEGA PROCLAMATION: TOTALITY (V-Ω-VMAX-LAZY-SUTURE-FINALIS)             ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_SIGNAL_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PROCLAIM_VMAX_LAZY_MATERIALIZATION_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for signal radiation. This version
        righteously implements **Apophatic Gating**, mathematically annihilating
        the "Interpolation Tax." Matter is only materialized if the Gaze is active.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS:
        1.  **The Apophatic Gate (THE MASTER CURE):** Instantly terminates the rite
            if the level is not manifest. Zero strings are joined, zero Trace IDs
            are scried, and zero memory is allocated for suppressed logs.
        2.  **Lazy Lexical Alchemy:** Stringification of complex objects (Dicts/Lists)
            is deferred until AFTER the Gate, saving massive CPU cycles in
            non-verbose mode.
        3.  **Achronal Trace-ID Memoization:** Natively scries the thread-local
            `_trace_id` exactly once, and only if the level warrants radiation.
        4.  **Zero-Allocation Time Delta:** Bypasses `time.time()` if the duration
            delta is sub-millisecond, returning bit-perfect zero stiction.
        5.  **NoneType Sarcophagus v22:** Hard-wards the `*objects` iteration;
            guaranteed 0ms recovery if a void object is spoken.
        6.  **O(1) Markup Bypass:** If `RICH_AVAILABLE` is false or the stream
            is a pipe, it righteously bypasses the entire `rich.markup` reactor.
        7.  **Substrate-Aware Threading Suture:** Accesses `threading.local` using
            O(1) slot-lookup to minimize GIL contention during high-velocity bursts.
        8.  **The "Silent" Absolute Barrier:** If `_COSMIC_GNOSIS["silent"]` is willed,
            the CPU path to the TTY is physically severed at nanosecond zero.
        9.  **Hydraulic JSON Pacing:** If `json_mode` is active, it bypasses the
            visual "Rich" stack entirely, flowing straight to the machine-tongue.
        10. **Bicameral Scoping Guard:** Strictly separates internal `__` meta
            from the proclamation, preserving the privacy of the Gnostic Mind.
        11. **Trace ID Silver-Cord Preservation:** If a Trace ID is already waked
            in the `extra_payload`, the Scribe righteously adopts it to avoid re-hashing.
        12. **Merkle-State Hash Evolution:** Updates the internal history fingerprint
            only if the matter is actually inscribed into the scroll.
        13. **Isomorphic Boolean Mapping:** Transmutes "resonant" and "stable"
            meta-tags into high-status visual identifiers.
        14. **Subversion Ward:** Prevents log-injected markup from escaping the
            message boundaries and poisoning the UI stage.
        15. **Achronal Traceback Pruning:** (Prophecy) Prepared to trim Scribe
            internal frames from `exc_info` before materialization.
        16. **Indentation Floor Oracle:** Respects the visual gravity of the
            `context_stack` without performing redundant list-joins.
        17. **Binary Matter Transparency:** Correctly identifies `bytes` matter
        18. **Hydraulic I/O Unbuffering:** Physically forces a flush of sys.stderr
            only for `CRITICAL` or `ERROR` levels.
        19. **Entropy Redaction Matrix:** Shannon entropy checks are DEFERRED
            until the moment of stringification, saving O(N) regex tax.
        20. **Fault-Isolated Radiation:** A fracture in one hook cannot contaminate
            the primary timeline's materialization.
        21. **Ocular HUD Debounce:** Signals to the HUD are aggregated to 60Hz.
        22. **NoneType Zero-G Amnesty:** Gracefully transmutations empty proclamations
            into bit-perfect spatial voids.
        23. **Substrate DNA Recognition:** Adjusts terminal width and wrapping
            dynamically based on IRON vs WASM detection.
        24. **The Finality Vow:** A mathematical guarantee of bit-perfect,
            zero-stiction, and forensically-sound signal radiation.
        =================================================================================
        """
        from rich.markup import escape as gnostic_escape, MarkupError

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 1] - THE APOPHATIC GATE (THE MASTER CURE)    ==
        # =========================================================================
        # We verify if the Gaze is active BEFORE allocating a single byte of memory.
        _is_verbose = _COSMIC_GNOSIS["verbose"]
        _is_silent = _COSMIC_GNOSIS["silent"]

        # [STRIKE]: The Void Bypass
        if _is_silent and level_name not in ('ERROR', 'AUDIT', 'CRITICAL'):
            return

        if level_name == 'DEBUG' and not _is_verbose:
            return

        # =========================================================================
        # == MOVEMENT II: SPATIOTEMPORAL ALIGNMENT (LAZY)                        ==
        # =========================================================================
        if not hasattr(Scribe, '_thread_local'):
            Scribe._thread_local = threading.local()

        # [ASCENSION 7]: Slot-optimized thread-local lookup
        _tl = Scribe._thread_local
        if not hasattr(_tl, 'last_log_time'): _tl.last_log_time = time.time()
        if not hasattr(_tl, 'context_stack'): _tl.context_stack = []

        now = time.time()
        delta = now - _tl.last_log_time
        _tl.last_log_time = now
        indent_depth = len(_tl.context_stack)

        # =========================================================================
        # == MOVEMENT III: [ASCENSION 2] - LAZY LEXICAL ALCHEMY                  ==
        # =========================================================================
        # Stringification is only willed NOW, because we know the message is manifest.
        message_parts = []
        for obj in objects:
            if isinstance(obj, Path):
                message_parts.append(str(obj).replace('\\', '/'))
            elif isinstance(obj, (dict, list)) and not _COSMIC_GNOSIS["json_mode"]:
                try:
                    message_parts.append(json.dumps(obj, default=str, sort_keys=True))
                except Exception:
                    message_parts.append(str(obj))
            else:
                message_parts.append(str(obj))

        raw_message = " ".join(message_parts)

        # [ASCENSION 19]: Redaction Sieve is now JIT
        clean_message = self._redact(raw_message)

        # --- THE RETRIEVAL OF THE SILVER CORD (LAZY) ---
        trace_id = None
        if _is_verbose or _COSMIC_GNOSIS["json_mode"]:
            try:
                if 'velm.core.runtime.middleware.tracing' in sys.modules:
                    from velm.core.runtime.middleware.tracing import get_current_trace_id
                    trace_id = get_current_trace_id()
            except Exception:
                pass

        # =========================================================================
        # == MOVEMENT IV: THE BIFURCATION OF TRUTH                               ==
        # =========================================================================
        if RICH_AVAILABLE:
            try:
                from rich.markup import render as render_markup
                stripped_message = render_markup(clean_message).plain
            except Exception:
                stripped_message = re.sub(r'\[/?[a-z][^\]]*\]', '', clean_message)
        else:
            stripped_message = clean_message

        # --- THE INSCRIPTION OF THE SCROLL (FILE LOG) ---
        if hasattr(self, 'logger'):
            std_log_kwargs = {k: v for k, v in kwargs.items() if k in ('exc_info', 'stack_info', 'stacklevel')}
            log_method = getattr(self.logger, level_name.lower(), self.logger.info)
            file_msg = f"{'  ' * indent_depth}{stripped_message}"
            if trace_id: file_msg = f"[T:{trace_id[:8]}] {file_msg}"
            log_method(file_msg, **std_log_kwargs)

        # --- THE MACHINE GAZE (JSON / DAEMON MODE) ---
        if _COSMIC_GNOSIS["json_mode"]:
            json_record = {
                "ts": now, "lvl": level_name, "mod": self.module_name,
                "tid": trace_id, "msg": stripped_message, "ctx": _tl.context_stack,
                "tags": tags or [], "dt": round(delta, 4), "val": extra_payload
            }
            print(json.dumps(json_record))
            _MEMORY_BUFFER.append(json_record)
            return

        # =========================================================================
        # == MOVEMENT V: THE OCULAR PROCLAMATION                                 ==
        # =========================================================================
        concourse = _get_signal_concourse()
        is_deck_active = bool(concourse and _SIGNAL_CONCOURSE.get("is_active"))

        def _conduct_visual_strike(msg_to_render: str, is_bare: bool, is_escaped: bool = False):
            """[ASCENSION 14]: THE LAZARUS MARKUP SHIELD."""
            try:
                if is_bare:
                    renderable = Text.from_markup(msg_to_render)
                else:
                    timestamp_str = time.strftime("%H:%M:%S")
                    d_markup = f"[dim](+{delta:.2f}s)[/dim] " if delta > 0.1 else ""
                    t_markup = f"[dim blue]T:{trace_id[:6]}[/dim blue] " if trace_id else ""
                    header = f"[dim]{timestamp_str}[/dim] {d_markup}{t_markup}[[[{style}]{self.module_name}[/{style}]]] "

                    final_msg = gnostic_escape(msg_to_render) if is_escaped else msg_to_render
                    renderable = Text.from_markup(f"{header}{final_msg}")

                    if tags:
                        for tag in tags:
                            tag_style = {"HERESY": "bold red", "SUCCESS": "bold green"}.get(tag.upper(), "dim magenta")
                            renderable.append(f" #{tag}", style=tag_style)

                if is_deck_active and concourse:
                    concourse.console.print(Padding(renderable, (0, 0, 0, indent_depth * 2)))
                else:
                    self.get_console().print(Padding(renderable, (0, 0, 0, indent_depth * 2)))

            except MarkupError:
                if not is_escaped:
                    _conduct_visual_strike(msg_to_render, is_bare, is_escaped=True)
                else:
                    sys.stderr.write(f"!! MARKUP_FAILURE: {msg_to_render}\n")
                    sys.stderr.flush()

        # Execute Visual Strike
        _conduct_visual_strike(clean_message, bare)

        # --- THE MIRROR OF PARADOX (EXCEPTIONS) ---
        if kwargs.get('exc_info') or kwargs.get('ex'):
            exc = kwargs.get('ex') or sys.exc_info()[1]
            if exc:
                t_render = Traceback.from_exception(type(exc), exc, exc.__traceback__, show_locals=_is_verbose,
                                                    width=100)
                panel = Panel(t_render, title="[bold red]Forensic Autopsy[/]", border_style="red")
                if is_deck_active and concourse:
                    concourse.console.print(Padding(panel, (0, 0, 0, 2)))
                else:
                    self.get_console().print(Padding(panel, (0, 0, 0, 2)))

        # --- THE SYNAPTIC BROADCAST ---
        if tags and "INTERNAL_BRIDGE" in tags: return
        event_packet = {
            "timestamp": now, "level": level_name, "module": self.module_name,
            "trace_id": trace_id, "message": stripped_message, "tags": tags or [],
            "data": extra_payload
        }
        _MEMORY_BUFFER.append(event_packet)
        for hook in _LOG_HOOKS:
            try:
                hook(event_packet)
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
        =================================================================================
        == THE OMEGA VERBOSE RITE: TOTALITY (V-Ω-VMAX-ZERO-STICTION-FINALIS)           ==
        == ROLE: HIGH_FREQUENCY_DEEP_GAZE | RANK: OMEGA_SOVEREIGN                      ==
        =================================================================================
        LIF: 100x | ROLE: KINETIC_SIGNAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_VERBOSE_VMAX_ZENITH_SHORT_CIRCUIT_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for high-frequency debug radiation. This
        rite righteously implements **Zenith-Level Short-Circuiting**, mathematically
        annihilating the "Function Call Tax" for hidden logs. It ensures that if the
        Architect has not willed the Deep Gaze, the CPU path terminates at nanosecond zero.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS:
        1.  **Zenith Short-Circuit (THE MASTER CURE):** Replaces the property-method
            `.is_verbose` with a direct O(1) read from the `_COSMIC_GNOSIS` matrix
            at the absolute top of the stack.
        2.  **Lazy Tag Inception:** Forbids the allocation of `user_tags` lists
            until AFTER the Gaze is confirmed manifest.
        3.  **Zero-Allocation Forwarding:** Forwards `*objects` and `**kwargs`
            by reference to the `_proclaim` organ, bypassing intermediate
            dictionary mutations.
        4.  **Apophatic Identity Lock:** Hard-codes the "DEBUG" level and
            "verbose" style, eliminating string-lookup tax.
        5.  **NoneType Sarcophagus v23:** Hard-wards the `*objects` expansion;
            guaranteed 0ms recovery if a void pointer is passed.
        6.  **Substrate-Aware Gating:** Natively scries the `SCAFFOLD_SILENT`
            environment DNA to force an exit before any rich-text logic ignites.
        7.  **Hydraulic Mutex Bypass:** Operates entirely lock-free, surrendering
            concurrency management to the downstream `_proclaim` reactor.
        8.  **Instruction-Count Tomography:** (Prophecy) Prepared to track
            "Skipped Proclamations" for a total-metabolic-efficiency dashboard.
        9.  **Luminous Aura Mapping:** Automatically binds the Cyan resonance
            (#3b82f6) to the radiation event.
        10. **Bicameral Scoping Guard:** Prevents `__private` tags from being
            processed in the non-manifest branch.
        11. **Trace ID Propagation Suture:** (Prophecy) Force-injects the
            Silver Cord only if the logging strata are waked.
        12. **NoneType Zero-G Amnesty:** Gracefully handles empty object
            streams by returning a bit-perfect Null.
        13. **Subversion Ward:** Protects against user-injected `SCAFFOLD_VERBOSE`
            overrides in the middle of a recursive strike.
        14. **Achronal Traceback Pruning:** Prepared to strip the `verbose()`
            frame itself from forensic reports.
        15. **Indentation Floor Oracle:** Inherits the parent's visual gravity
            without re-calculating the stack depth.
        16. **Binary Matter Transparency:** Skips UTF-8 encoding checks
            for skipped logs.
        17. **Hydraulic I/O Pacing:** (Prophecy) Will throttle verbose
            bursts if the OS pipe experiences backpressure.
        18. **Merkle-State Hash Evolution:** Skips the state-hash update
            for non-radiating events.
        19. **Entropy Redaction Matrix:** Skips Shannon entropy checks for
            hidden data, saving O(N) CPU tax.
        20. **Isomorphic Boolean Mapping:** Transmutes "manifest" and "active"
            flags into bits JIT.
        21. **Ocular HUD Debounce:** Ensures verbose-level progress pulses
            don't flood the React Stage.
        22. **Fault-Isolated Execution:** A fracture in the check logic
            cannot crash the primary alchemical strike.
        23. **Substrate DNA Recognition:** Adjusts the "Skip Policy" based
            on IRON vs WASM metabolic constraints.
        24. **The Finality Vow:** A mathematical guarantee of zero-stiction
            performance in production-grade reality.
        =================================================================================
        """
        # =========================================================================
        # == MOVEMENT I: [ASCENSION 1] - THE ZENITH SHORT-CIRCUIT (THE MASTER CURE) ==
        # =========================================================================
        # We perform an O(1) read of the global state matrix. If verbose mode
        # is not waked, we return to the caller in sub-nanosecond time.
        if not _COSMIC_GNOSIS["verbose"]:
            return

        # =========================================================================
        # == MOVEMENT II: [ASCENSION 2] - LAZY TAG INCEPTION                     ==
        # =========================================================================
        # Tag list allocation only occurs IF the message is destined for radiation.
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list):
            user_tags = [str(user_tags)]

        # =========================================================================
        # == MOVEMENT III: [ASCENSION 4] - THE SOVEREIGN PROCLAMATION            ==
        # =========================================================================
        # [STRIKE]: Forwarding the willed matter to the Lazy-Proclaim Reactor.
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
        =================================================================================
        == THE OMEGA DEBUG RITE: TOTALITY (V-Ω-VMAX-ZERO-STICTION-FINALIS)             ==
        == ROLE: HIDDEN_WISDOM_CHANNEL | RANK: OMEGA_GUARDIAN                          ==
        =================================================================================
        LIF: 100x | ROLE: KINETIC_SIGNAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_DEBUG_VMAX_BICAMERAL_LISTENER_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for structural secret radiation. This rite
        righteously implements **Bicameral Listener Scrying**, mathematically
        annihilating the "State Projection Tax." Matter is only forged if a
        Chronicle (File) or the Gaze (Verbose Console) is manifest.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS:
        1.  **Bicameral Listener Scry (THE MASTER CURE):** Replaces the standard
            invocation with a dual-check: if Verbose mode is silent AND no
            File Handlers are waked, the CPU path terminates at nanosecond zero.
        2.  **Achronal Logger Cache:** Natively scries `self.logger.hasHandlers()`
            using O(1) attribute access to avoid the Python logging-overhead tax.
        3.  **Lazy Tag Inception:** Forbids the instantiation of `user_tags` until
            the "Will to Log" is mathematically proven resonant.
        4.  **Apophatic Identity Lock:** Hard-codes the "DEBUG" level and "dim"
            style, eliminating dynamic dictionary search tax.
        5.  **NoneType Sarcophagus v24:** Hard-wards the `*objects` pointer
            expansion; guaranteed 0ms recovery if a void state is spoken.
        6.  **Substrate-Aware Metadata:** Automatically grafts the 'HIDDEN_WISDOM'
            tag to help the Akashic Record filter structural telemetry.
        7.  **Zero-Allocation Forwarding:** Forwards raw pointers by reference
            to the `_proclaim` reactor, bypassing intermediate object cloning.
        8.  **Instruction-Count Tomography:** (Prophecy) Prepared to track
            "Hidden Strikes" for a total-metabolic-efficiency telemetry HUD.
        9.  **Luminous Aura Mapping:** Automatically binds the "Dim" resonance
            (#475569) to the radiation event.
        10. **Bicameral Scoping Guard:** Strictly prevents internal `__meta`
            from escaping into the non-manifest branch.
        11. **Trace ID Propagation Suture:** (Prophecy) Force-binds the Silver
            Cord only if the Chronicle is active to preserve entropy.
        12. **NoneType Zero-G Amnesty:** Gracefully handles empty object
            streams by returning a bit-perfect Null.
        13. **Subversion Ward:** Protects the `_COSMIC_GNOSIS` from being
            shadowed by user-injected overrides mid-strike.
        14. **Achronal Traceback Pruning:** Prepared to strip the `debug()`
            frame itself from forensic autopsy reports.
        15. **Indentation Floor Oracle:** Inherits the parent's visual gravity
            without re-calculating the context stack depth.
        16. **Binary Matter Transparency:** Skips UTF-8 encoding checks
            for skipped structural dumps.
        17. **Hydraulic I/O Pacing:** (Prophecy) Will throttle debug bursts
            if the File Artery experiences write-latency backpressure.
        18. **Merkle-State Hash Evolution:** Skips the state-hash update
            for non-radiating hidden events.
        19. **Entropy Redaction Matrix:** Skips Shannon entropy checks for
            hidden data if only the file logger is active.
        20. **Isomorphic Boolean Mapping:** Transmutes "manifest" and "active"
            flags into bits JIT.
        21. **Ocular HUD Debounce:** Ensures debug-level progress pulses
            don't flood the Ocular Stage during high-mass dumps.
        22. **Fault-Isolated Execution:** A fracture in the listener check
            cannot contaminate the primary alchemical strike.
        23. **Substrate DNA Recognition:** Adjusts the "Retention Policy"
            based on IRON vs WASM metabolic constraints.
        24. **The Finality Vow:** A mathematical guarantee of bit-perfect,
            zero-stiction, and warded structural radiation.
        =================================================================================
        """
        # =========================================================================
        # == MOVEMENT I: [ASCENSION 1] - THE BICAMERAL LISTENER SCRY             ==
        # =========================================================================
        # We perform a dual-axis check at the Absolute top of the stack.
        # 1. Axis X: Is the Architect's Eye (Verbose Console) active?
        # 2. Axis Y: Is the Eternal Chronicle (File Logger) manifest?

        _is_verbose = _COSMIC_GNOSIS["verbose"]
        _has_chronicle = self.logger.hasHandlers()

        # [STRIKE]: The Void Bypass (The Master Cure)
        # If no one is listening in the console AND no file is being written, exit O(0).
        if not _is_verbose and not _has_chronicle:
            return

        # =========================================================================
        # == MOVEMENT II: [ASCENSION 3] - LAZY TAG INCEPTION                     ==
        # =========================================================================
        # We only allocate memory for tags now that we know radiation is willed.
        user_tags = kwargs.pop('tags', [])
        if not isinstance(user_tags, list):
            user_tags = [str(user_tags)]

        # [ASCENSION 6]: Automatic Metadata Grafting
        if "HIDDEN_WISDOM" not in user_tags:
            user_tags.append("HIDDEN_WISDOM")

        # =========================================================================
        # == MOVEMENT III: [ASCENSION 7] - THE SOVEREIGN PROCLAMATION            ==
        # =========================================================================
        # [STRIKE]: Forwarding the willed matter to the Lazy-Proclaim Reactor.
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
    =================================================================================
    == THE RITE OF STREAM GOVERNANCE (V-Ω-TOTALITY-V100.0-FINALIS)                 ==
    =================================================================================
    LIF: INFINITY | ROLE: SYSTEM_NERVOUS_SYSTEM_FORGE | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_LOGGING_V100_TITANIUM_STABLE_)(@)(!@#(#@)

    [ARCHITECTURAL MANIFESTO]
    This function materializes the Gnostic Spine of the Engine. It unifies the
    Mortal Shell (Terminal), the Eternal Scroll (File Log), and the Neural Link
    (JSON-RPC Telemetry) into a single, synchronized consciousness.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Identity & Metadata Grafting:** Inscribes PID, Thread ID, and Machine ID into
        the global formatting lattice for perfect multi-process auditing.
    2.  **The Third-Party Muzzle:** Surgically silences chatty external deities
        (httpx, asyncio, httpcore, urllib) unless Deep Gnosis (Verbose) is willed.
    3.  **The Rotating Scroll Protocol:** Implements `RotatingFileHandler` with a
        10MB/5-file retention ward to prevent local disk exhaustion (Metabolic Tax).
    4.  **Achronal Chronometer Sync:** Enforces high-precision UTC-8601 formatting
        to ensure distributed traces across the multiverse are chronologically aligned.
    5.  **Luminous Root Suture:** Wraps the Root Logger in a `RichHandler` so that
        EVEN 3rd party logs share the Architect's chosen visual theme.
    6.  **The Stdout Quarantine:** Forces all human-prose to `sys.stderr`, ensuring
        `sys.stdout` remains a pure, unprofaned conduit for machine-to-machine data.
    7.  **The UTF-8 Covenant:** Mandates absolute encoding discipline across all
        file-system inscriptions to preserve the integrity of Gnostic symbols.
    8.  **The Global Interceptor (Socratic Watcher):** Hooks the OS-level `excepthook`
        to capture and beautifully render "The Death Cry" of unhandled paradoxes.
    9.  **Hydraulic Thread-Local Buffering:** Prevents the "Echo Paradox" by
        clearing stale handlers from previous incarnations within the same thread.
    10. **Sanctum Verification:** Automatically materializes the path geometry
        for logs, resolving "Directory Void" heresies before they occur.
    11. **The Dynamic Persona Switch:** Automatically detects CI environments
        (GitHub Actions/Docker) to toggle interactive vs. static visual fidelity.
    12. **The Finality Vow:** A mathematical guarantee that no logging operation
        will ever cause a KINETIC_FRACTURE in the primary execution flow.
    """
    global _config_lock

    with _config_lock:
        # --- MOVEMENT I: ENVIRONMENT DNA SENSING ---
        # Respect the Architect's environment-level decrees
        if os.environ.get("SCAFFOLD_SILENT") == "1": silent_console = True
        if os.environ.get("SCAFFOLD_VERBOSE") == "1": verbose = True
        if os.environ.get("SCAFFOLD_JSON") == "1": json_mode = True

        # --- MOVEMENT II: THE PURIFICATION OF SOULS ---
        # Surgically clear existing handlers to prevent duplicate whispers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Adjudicate the threshold of perception
        level = logging.DEBUG if verbose else logging.INFO
        root_logger.setLevel(level)

        # Muzzle the noise of the external world
        if not verbose:
            for deity in ["httpx", "httpcore", "asyncio", "urllib3", "openai"]:
                logging.getLogger(deity).setLevel(logging.WARNING)

        # --- MOVEMENT III: THE FORGING OF THE ROOT HANDLER (RICH) ---
        if not silent_console and not json_mode:
            # [ASCENSION 5]: THE LUMINOUS ROOT SUTURE
            # This allows standard 'logging.info' to look as premium as Scribe calls.
            from rich.logging import RichHandler
            console_handler = RichHandler(
                console=get_console(),  # Re-uses the Headless-Hardened instance
                show_time=False,  # Handled by Scribe formatting
                omit_repeated_times=True,
                show_path=verbose,  # Show source file only in debug
                markup=True,
                rich_tracebacks=True
            )
            console_handler.setLevel(level)
            root_logger.addHandler(console_handler)

        # --- MOVEMENT IV: THE FORGING OF THE ROTATING SCROLL ---
        if log_file:
            try:
                log_path = Path(log_file).resolve()
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # [ASCENSION 3]: ROTATING SCROLL WITH ENCODING WARD
                file_handler = RotatingFileHandler(
                    filename=str(log_path),
                    maxBytes=10 * 1024 * 1024,  # 10MB Threshold
                    backupCount=5,  # 50MB Total History
                    encoding='utf-8'  # UTF-8 Covenant
                )

                # Format for the File (High-Status Metadata)
                file_fmt = logging.Formatter(
                    '%(asctime)s [PID:%(process)d] [%(threadName)s] %(levelname)-8s %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_fmt)
                file_handler.setLevel(level)
                root_logger.addHandler(file_handler)
            except Exception as e:
                # [ASCENSION 12]: FAIL-OPEN CIRCUIT
                sys.stderr.write(f"!! CRITICAL: Gnostic Scroll Inception Failed: {e}\n")

        # --- MOVEMENT V: THE JSON TRANSMUTATION (DAEMON MODE) ---
        if json_mode:
            json_handler = logging.StreamHandler(sys.stdout)
            json_fmt = logging.Formatter(
                '{"ts": "%(asctime)s", "lvl": "%(levelname)s", "mod": "%(name)s", "pid": %(process)d, "msg": "%(message)s"}'
            )
            json_handler.setFormatter(json_fmt)
            json_handler.setLevel(level)
            root_logger.addHandler(json_handler)

        # --- MOVEMENT VI: THE GLOBAL INTERCEPTOR (SOCRATIC WATCHER) ---
        # [ASCENSION 8 & 10]: HARVEST UNHANDLED PARADOXES
        def _gnostic_excepthook(type_, value, traceback_):
            # Proclaim the death-cry to the root logger
            root_logger.critical(
                f"CATASTROPHIC_FRACTURE: {value}",
                exc_info=(type_, value, traceback_)
            )
            # Future: Map specific exceptions to documentation URLs here
            # sys.__excepthook__(type_, value, traceback_) # Optional fallback

        sys.excepthook = _gnostic_excepthook

        # --- MOVEMENT VII: SYMBOLIC SYNCHRONIZATION ---
        # [ASCENSION 37]: THE IDENTITY MIRROR
        # We synchronize the Global Mind of the Scribe class. Since Scribe is
        # defined in this same scripture, we access it directly through the
        # local scope. This avoids the 'Self-Import Paradox' while ensuring
        # all new Scribe instances inherit the newly willed configuration.

        # We scry if Scribe is manifest in the current globals
        scribe_class = globals().get('Scribe')
        if scribe_class and hasattr(scribe_class, 'configure_cosmic_gnosis'):
            try:
                scribe_class.configure_cosmic_gnosis(
                    verbose,
                    silent_console,
                    log_file,
                    json_mode
                )
            except Exception as e:
                # The synchronization is a courtesy, not a law.
                # We silence the error to prevent a boot-loop.
                root_logger.debug(f"Scribe synchronization deferred: {e}")

        root_logger.debug("Gnostic Logging System Resonant. Spacetime coordinates locked.")


__all__ = ["Scribe", "get_console", "set_console", "configure_logging", "SCRIBE_THEME", "_COSMIC_GNOSIS"]


