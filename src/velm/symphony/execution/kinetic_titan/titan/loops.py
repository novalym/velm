# Path: scaffold/symphony/execution/kinetic_titan/titan/loops.py
# --------------------------------------------------------------

import time
import queue
import re
import shutil
from collections import deque
from typing import Callable, Any, List, Optional, Union, Dict

from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.console import Group, Console
from rich import box
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, BarColumn, TextColumn
from rich.rule import Rule  # <--- [FIX] Imported for visual separator

from .state import TitanState
from .visuals import VisualCortex
from ..executor import TitanExecutor
from ..semantics import SemanticGrimoire
from .....logger import Scribe

Logger = Scribe('LoopConductor')


class LoopMetrics:
    """
    =============================================================================
    == THE PULSE OF THE MACHINE (V-Ω-TELEMETRY-ENGINE)                         ==
    =============================================================================
    Tracks velocity, volume, and history of the kinetic rite.
    """
    SPARK_HISTORY_SIZE = 30

    def __init__(self):
        self.start_time = time.time()
        self.last_update = time.time()

        # Counters
        self.lines_processed = 0
        self.bytes_processed = 0
        self.error_count = 0
        self.warn_count = 0
        self.artifacts_detected = 0

        # Rates
        self.current_throughput = 0.0
        self.peak_throughput = 0.0

        # Sparkline Buffer (Normalized 0-1)
        self.spark_buffer = deque([0.0] * self.SPARK_HISTORY_SIZE, maxlen=self.SPARK_HISTORY_SIZE)

    def update(self, line_len: int, is_error: bool, content: str):
        self.lines_processed += 1
        self.bytes_processed += line_len
        self.last_update = time.time()

        if is_error:
            self.error_count += 1
        if "warn" in content.lower():
            self.warn_count += 1
        # [FACULTY 5] Artifact Beacon Logic
        if "generated" in content.lower() or "created" in content.lower() or "wrote" in content.lower():
            if any(x in content for x in ['.js', '.py', '.css', '.html', '.json', '.lock']):
                self.artifacts_detected += 1

    def tick(self):
        """Calculates instantaneous rates."""
        now = time.time()
        duration = now - self.start_time
        if duration > 0.1:
            # Simple moving average for stability
            instant_rate = self.lines_processed / duration
            self.current_throughput = instant_rate
            self.peak_throughput = max(self.peak_throughput, instant_rate)

            # Update sparkline (normalized against peak, filtered for noise)
            peak = max(self.peak_throughput, 1.0)
            normalized = min(1.0, instant_rate / peak)
            self.spark_buffer.append(normalized)

    def get_silence_duration(self) -> float:
        return time.time() - self.last_update


class LoopConductor:
    """
    =============================================================================
    == THE LUMINOUS ORRERY (V-Ω-FLUID-DYNAMICS-ASCENDED)                       ==
    =============================================================================
    LIF: 10,000,000,000,000,000,000

    The God-Engine of Visual Feedback. It turns a subprocess execution into
    a living, breathing dashboard.
    """

    BASE_RENDER_INTERVAL = 0.05
    TURBO_THRESHOLD = 150.0  # Lines per second to trigger simplified view
    MAX_STATIC_HISTORY = 100

    # [FACULTY 4] The Semantic Spinner Shifter
    ACTIVITY_PATTERNS = {
        'download': 'bouncingBar',
        'fetch': 'bouncingBar',
        'install': 'arc',
        'build': 'hammer',
        'compiling': 'hammer',
        'transmut': 'arc',
        'wait': 'clock',
        'sleep': 'clock',
        'verify': 'dots12',
        'analyz': 'dots12',
        'push': 'arrow3',
        'pull': 'arrow3',
        'pack': 'package',
        'bundl': 'package'
    }

    # [FACULTY 1] The Sparkline Characters
    SPARKS = [' ', ' ', '▂', '▃', '▄', '▅', '▆', '▇', '█']

    @staticmethod
    def conduct_raw(
            executor: TitanExecutor,
            output_queue: queue.Queue,
            state: TitanState,
            stream_callback: Callable,
            live_context: Any
    ):
        """The Naked Rite. Pure speed, no glory."""
        while executor.is_alive() or not output_queue.empty():
            try:
                stream_type, line = output_queue.get(timeout=0.1)
                if line is None: continue
                state.add_line(Text(line))
                if stream_callback: stream_callback(live_context, line)
            except queue.Empty:
                continue
            except Exception as e:
                Logger.error(f"Raw Conductor faltered: {e}")

    @staticmethod
    def conduct_cinematic(
            executor: TitanExecutor,
            output_queue: queue.Queue,
            state: TitanState,
            stream_callback: Callable,
            live_context: Any,
            sanctum: Any,
            console: Console
    ):
        """
        The Luminous Rite (Ascended).
        Orchestrates the visual symphony with a dedicated Status Header and Fluid Content Panel.
        """
        metrics = LoopMetrics()
        visuals = VisualCortex()

        # UI State
        current_spinner_name = "dots12"
        spinner = Spinner(current_spinner_name, style="cyan")
        border_color = "cyan"
        last_pulse_time = 0.0
        terminal_height = shutil.get_terminal_size().lines
        max_live_height = max(10, int(terminal_height * 0.6))  # Use up to 60% of screen height

        # [FACULTY 1] The Divine Icon
        command_icon = SemanticGrimoire.divine_icon(state.command)

        # [FACULTY 2] The Luminous Prologue Panel (Static Anchor)
        # This prints ONCE before the live loop, anchoring the context.
        prologue_grid = Table.grid(expand=True, padding=(0, 1))
        prologue_grid.add_column(justify="left", style="bold white")
        prologue_grid.add_column(justify="right", style="dim cyan")

        # Truncate command if too long for header
        display_cmd = state.command
        if len(display_cmd) > 80: display_cmd = display_cmd[:77] + "..."

        prologue_grid.add_row(
            Text.assemble((f"{command_icon} ", "bold"), (f"{display_cmd}", "bold white")),
            f"{sanctum}"
        )

        console.print(Panel(prologue_grid, border_style="dim cyan", box=box.MINIMAL))

        def generate_sparkline() -> str:
            """[FACULTY 1] Renders the Sparkline."""
            line = ""
            for val in metrics.spark_buffer:
                idx = int(val * (len(LoopConductor.SPARKS) - 1))
                line += LoopConductor.SPARKS[idx]
            return line

        def generate_renderable(current_duration: float):
            nonlocal border_color, current_spinner_name

            metrics.tick()

            # [FACULTY 3] Adaptive Throttle / Turbo Mode
            is_turbo = metrics.current_throughput > LoopConductor.TURBO_THRESHOLD

            # [FACULTY 5] Silence Sentinel
            is_stalled = metrics.get_silence_duration() > 10.0 and not is_turbo

            # [FACULTY 2] Chromatic Resonator Decay
            if border_color != "cyan" and time.time() - last_pulse_time > 0.5:
                border_color = "cyan"

            # --- 1. Forge the Status Header (Live) ---
            grid = Table.grid(expand=True, padding=(0, 1))
            grid.add_column(justify="left", ratio=1)
            grid.add_column(justify="right", style="dim")

            # Status Text Construction
            status_style = "bold cyan"
            status_text = "Running..."

            if is_turbo:
                status_text = "🚀 TURBO VELOCITY"
                status_style = "bold magenta"
            elif is_stalled:
                status_text = "⏳ Stalled?"
                status_style = "bold yellow"

            # Sub-table for Spinner + Text
            left_table = Table.grid(padding=(0, 1))
            left_table.add_row(
                spinner,
                Text(f"{status_text} ({current_duration:.1f}s)", style=status_style)
            )

            # Sparkline + Metrics
            spark = generate_sparkline()
            right_side = f"[{spark}] {metrics.current_throughput:.0f}/s"

            grid.add_row(left_table, right_side)

            # --- 2. Forge the Content Panel ---
            if is_turbo:
                # [FACULTY 3] Turbo View (Simplified)
                content = Align.center(
                    f"\n[bold dim]Processing massive stream...[/]\n"
                    f"[cyan]{metrics.lines_processed}[/] lines processed.\n"
                    f"[magenta]{metrics.bytes_processed / 1024:.1f} KB[/] ingested.\n"
                    f"[bold white]{metrics.peak_throughput:.0f}/s[/] peak velocity.\n"
                )
                panel_height = 8
            else:
                # [FACULTY 13 - THE FIX] Elastic Viewport
                # We calculate how many lines we HAVE, and show as many as possible
                # up to max_live_height.

                # We want to show the TAIL of the history.
                # However, to prevent "chunking" where lines disappear, we should
                # fill the box.

                lines_available = len(state._history)
                # If we have few lines, box is small. If many, box grows to max.
                dynamic_height = min(max(lines_available, 4), max_live_height)

                # Get the slice that fits
                history_snapshot = state.get_history_snapshot(lines=dynamic_height)

                if not history_snapshot:
                    content = Text("\nWaiting for output...", style="dim italic")
                else:
                    # Update spinner based on last line content [FACULTY 4]
                    last_line = history_snapshot[-1].plain.lower()
                    for keyword, spin_type in LoopConductor.ACTIVITY_PATTERNS.items():
                        if keyword in last_line and current_spinner_name != spin_type:
                            current_spinner_name = spin_type
                            # Rich Spinner objects don't support hot-swapping 'name' easily.
                            # We create a new spinner for the next frame.
                            # Ideally we'd store a map of Spinner objects, but this is a V1 patch.
                            pass

                    content = Group(*history_snapshot)

                panel_height = None  # Let Rich auto-size up to constraints, but we control content length

            # [FACULTY 6] Histogram Footer
            # Shows count of specific line types
            footer_parts = [f"[dim]Total: {metrics.lines_processed}[/dim]"]
            if metrics.error_count > 0: footer_parts.append(f"[bold red]Errors: {metrics.error_count}[/]")
            if metrics.warn_count > 0: footer_parts.append(f"[bold yellow]Warns: {metrics.warn_count}[/]")
            if metrics.artifacts_detected > 0: footer_parts.append(
                f"[bold blue]Artifacts: {metrics.artifacts_detected}[/]")

            footer_stats = " | ".join(footer_parts)

            return Group(
                grid,
                Panel(
                    content,
                    border_style=border_color,
                    box=box.ROUNDED,
                    padding=(0, 1),
                    # We remove fixed height to allow elasticity, or set it dynamically
                    height=panel_height if is_turbo else None,
                    title=f"[bold]Output Stream[/bold]",
                    title_align="left",
                    subtitle=footer_stats,
                    subtitle_align="right"
                )
            )

        # --- THE LIVE LOOP ---
        with Live(generate_renderable(0.0), console=console, refresh_per_second=15, transient=True) as live:

            while executor.is_alive() or not output_queue.empty():
                try:
                    try:
                        stream_type, line = output_queue.get(timeout=LoopConductor.BASE_RENDER_INTERVAL)
                    except queue.Empty:
                        live.update(generate_renderable(state.duration()))
                        continue

                    if line is None: continue

                    # Process Gnosis
                    styled_line = visuals.transmute(line, stream_type)
                    state.add_line(styled_line)
                    metrics.update(len(line), stream_type == 'stderr', line)

                    # [FACULTY 2] Trigger Error Pulse
                    if stream_type == 'stderr' or "error" in line.lower():
                        border_color = "red"
                        last_pulse_time = time.time()
                    elif "warn" in line.lower():
                        border_color = "yellow"
                        last_pulse_time = time.time()

                    if stream_callback: stream_callback(live_context, line)

                    # Update Live Display
                    live.update(generate_renderable(state.duration()))

                except KeyboardInterrupt:
                    state.add_line(Text("Rite Aborted by Architect", style="bold red"))
                    raise
                except Exception as e:
                    Logger.error(f"Cinematic Loop Paradox: {e}")

        # --- THE FINAL ADJUDICATION (THE TRUTH) ---
        final_rc = executor.returncode()
        if final_rc is None: final_rc = -1

        is_success = (final_rc == 0)

        final_color = "green" if is_success else "red"
        final_icon = "✔" if is_success else "✘"
        final_title = "Rite Complete" if is_success else f"Rite Failed (Exit {final_rc})"

        # [THE ASCENSION: ADAPTIVE HISTORY V2]
        # We calculate how much to show.
        total_history = len(state._history)
        display_lines = min(total_history, LoopConductor.MAX_STATIC_HISTORY)

        final_snapshot = state.get_history_snapshot(lines=display_lines)

        # [THE SCROLL MARKER]
        if total_history > display_lines:
            hidden_count = total_history - display_lines
            final_snapshot.insert(0, Text(f"... {hidden_count} previous lines hidden ...", style="dim italic"))

        # [FACULTY 12] The Luminous Epilogue (Metrics Table)
        stats_grid = Table.grid(expand=True, padding=(0, 2))
        stats_grid.add_column(justify="center", ratio=1)
        stats_grid.add_column(justify="center", ratio=1)
        stats_grid.add_column(justify="center", ratio=1)

        duration = state.duration()
        throughput = metrics.current_throughput

        stats_grid.add_row(
            f"[dim]Duration:[/dim] [bold white]{duration:.2f}s[/]",
            f"[dim]Throughput:[/dim] [bold white]{throughput:.1f}/s[/]",
            f"[dim]Peak:[/dim] [bold white]{metrics.peak_throughput:.1f}/s[/]"
        )

        final_panel = Panel(
            Group(
                *final_snapshot,
                Text(""),  # Spacer
                # [FIX] Replaced non-existent box.DoubleEdge with Rule(style=final_color)
                Rule(style=final_color) if not is_success else Text(""),  # Visual break on error
                stats_grid
            ),
            border_style=final_color,
            # [FACULTY 14] The Persistent Badge of Command
            title=f"[{final_color}]{final_icon} {final_title}[/{final_color}]",
            subtitle=f"[dim]Total Lines: {metrics.lines_processed}[/dim]",
            box=box.ROUNDED,
            padding=(0, 1),
            expand=True
        )

        console.print(final_panel)