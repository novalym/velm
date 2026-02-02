# Path: scaffold/symphony/execution/kinetic_titan/renderer.py
# -----------------------------------------------------------

import time
import sys
import threading
from collections import deque
from typing import List, Optional, Deque

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text
from rich.table import Table
from rich.ansi import AnsiDecoder
from rich.style import Style

from .semantics import SemanticGrimoire
from ....logger import get_console

# Lazy load psutil for Vitals
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class KineticRenderer:
    """
    =============================================================================
    == THE KINETIC RENDERER (V-Ω-LUMINOUS-HUD)                                 ==
    =============================================================================
    LIF: 10,000,000,000

    A stateful UI engine that renders a high-fidelity, interactive dashboard
    for the executing process.
    """

    BAR_CHARS = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    def __init__(self, command: str, sanctum: str):
        self.console = get_console()
        self.command = command
        self.sanctum = sanctum

        # State
        self.history: Deque[Text] = deque(maxlen=500)  # Deep buffer
        self.view_buffer: Deque[Text] = deque(maxlen=20)  # Visible buffer
        self.decoder = AnsiDecoder()

        # Aesthetics
        self.icon = SemanticGrimoire.divine_icon(command)
        self.spinner_name = SemanticGrimoire.divine_spinner(command)
        self.command_color = SemanticGrimoire.divine_color(command.split()[0])

        # Vitals
        self.cpu_history: Deque[float] = deque(maxlen=20)
        self.mem_current = 0.0
        self._monitor_thread = None
        self._stop_monitor = threading.Event()
        self.start_time = time.time()

        # Deduplication
        self.last_line_text = ""
        self.dup_count = 0

        # Live Context
        self.live: Optional[Live] = None

        # Error State
        self.has_error = False

    def start_monitoring(self, pid: int):
        """[FACULTY 2] The Vitals Monitor."""
        if PSUTIL_AVAILABLE:
            self._monitor_thread = threading.Thread(target=self._monitor_vitals, args=(pid,), daemon=True)
            self._monitor_thread.start()

    def stop_monitoring(self):
        self._stop_monitor.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=0.5)

    def _monitor_vitals(self, pid: int):
        try:
            proc = psutil.Process(pid)
            while not self._stop_monitor.is_set():
                try:
                    cpu = proc.cpu_percent(interval=None)
                    mem = proc.memory_info().rss / 1024 / 1024  # MB
                    self.cpu_history.append(cpu)
                    self.mem_current = mem
                except:
                    break
                time.sleep(0.5)
        except:
            pass

    def add_line(self, line: str, stream: str):
        """
        [FACULTY 4] Log Ingestion & Deduplication.
        """
        # 1. Decode & Style
        rich_text = self.decoder.decode_line(line)
        SemanticGrimoire.enhance(rich_text)

        if stream == 'stderr':
            rich_text.stylize("red")
            self.has_error = True

        # 2. Artifact Detection
        if "Created" in line or "Generated" in line:
            rich_text.stylize("bold green")

        # 3. Deduplication
        # If line matches previous, increment counter instead of appending
        plain = rich_text.plain.strip()
        if plain and plain == self.last_line_text:
            self.dup_count += 1
            # Update the last line in the view buffer to show count
            if self.view_buffer:
                last = self.view_buffer[-1]
                # We modify the text in place (risky but performant) or replace
                count_text = Text(f" [x{self.dup_count + 1}]", style="dim cyan")
                # Create composite
                new_text = Text(plain)
                new_text.stylize(last.style)  # Inherit style
                SemanticGrimoire.enhance(new_text)
                new_text.append(count_text)
                self.view_buffer[-1] = new_text
        else:
            self.dup_count = 0
            self.last_line_text = plain
            self.view_buffer.append(rich_text)
            self.history.append(rich_text)

    def _generate_sparkline(self) -> str:
        """[FACULTY 3] The Sparkline Prophet."""
        if not self.cpu_history: return ""
        chars = []
        max_cpu = 100.0
        for val in self.cpu_history:
            idx = int((val / max_cpu) * (len(self.BAR_CHARS) - 1))
            idx = max(0, min(len(self.BAR_CHARS) - 1, idx))
            chars.append(self.BAR_CHARS[idx])
        return "".join(chars)

    def renderable(self) -> Panel:
        """[FACULTY 10] Forges the HUD."""
        elapsed = time.time() - self.start_time

        # --- HEADER ---
        header_grid = Table.grid(expand=True)
        header_grid.add_column()
        header_grid.add_column(justify="right")

        title = Text.assemble(
            (self.icon, "default"),
            (" "),
            (self.command, f"bold {self.command_color}")
        )
        meta = Text(f"in {self.sanctum}", style="dim white")
        header_grid.add_row(title, meta)

        # --- BODY (LOGS) ---
        log_group = Group(*self.view_buffer)

        # --- FOOTER ---
        footer_grid = Table.grid(expand=True)
        footer_grid.add_column(ratio=1)
        footer_grid.add_column(justify="right")

        # Left: Vitals
        vitals = Text(f"⏱️ {elapsed:.1f}s", style="bold cyan")
        if PSUTIL_AVAILABLE:
            spark = self._generate_sparkline()
            vitals.append(f" | CPU {spark}", style="magenta")
            vitals.append(f" | MEM {self.mem_current:.0f}MB", style="blue")

        # Right: Spinner
        spinner = Spinner(self.spinner_name, style=self.command_color)

        footer_grid.add_row(vitals, spinner)

        # Frame Color (Red if error, else Blue)
        border = "red" if self.has_error else "blue"

        return Panel(
            Group(
                header_grid,
                Text("─" * 40, style="dim"),  # Divider
                log_content_spacer := Text(""),  # Vertical spacer if needed
                log_group,
                Text(""),
                footer_grid
            ),
            border_style=border,
            box=None,  # Use None for inner structure if nested, but here we want a panel
            padding=(0, 1)
        )

    # Context Manager for Live
    def __enter__(self):
        # We manually control the Live loop in Titan, so we just return self.
        # But if we wanted to encapsulate Live here:
        self.live = Live(
            self.renderable(),
            console=self.console,
            refresh_per_second=12,  # [FACULTY 12] Frame Regulator
            transient=True,
            auto_refresh=False
        )
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.live:
            self.live.stop()

    def update(self):
        """Triggers a redraw."""
        if self.live:
            self.live.update(self.renderable(), refresh=True)

    def render_final_snapshot(self, success: bool):
        """
        [FACULTY 11] The Static Chronicle.
        Prints a permanent record after the HUD vanishes.
        """
        style = "green" if success else "red"
        status_text = "SUCCESS" if success else "FAILURE"
        border = "green" if success else "red"

        # Re-render full history (or reasonable tail)
        # We unroll the history deque
        content = Group(*self.history)

        header = Text.assemble(
            (self.icon, "default"), (" "),
            (self.command, f"bold {self.command_color}"),
            (" "),
            (f"[{status_text}]", f"bold white on {style}")
        )

        panel = Panel(
            content,
            title=header,
            border_style=border,
            padding=(0, 1),
            expand=True
        )
        self.console.print(panel)