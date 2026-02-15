# Path: artisans/neural_link/dashboard.py
# =========================================================================================
# == THE NEURAL DASHBOARD: OMEGA TOTALITY (V-Ω-TOTALITY-V20000.1-ISOMORPHIC)             ==
# =========================================================================================
# LIF: ∞ | ROLE: SOVEREIGN_OCULAR_MEMBRANE | RANK: OMEGA_SUPREME
# AUTH: Ω_DASHBOARD_V20000_SUBSTRATE_AWARE_2026_FINALIS
# =========================================================================================

import time
import random
import threading
import os
from collections import deque
from pathlib import Path
from typing import Optional, List, Tuple

# [ASCENSION 1]: SURGICAL SENSORY GUARD
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Sparkline, Label, DataTable
from textual.containers import Grid, Vertical, Horizontal
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from textual.binding import Binding


class SystemMonitor(Static):
    """The Heartbeat Sensor. Warded for substrate independence."""
    cpu_history: reactive[deque] = reactive(deque([0.0] * 60, maxlen=60))
    ram_history: reactive[deque] = reactive(deque([0.0] * 60, maxlen=60))

    # [ASCENSION 2]: Reactive state for dynamic updates
    current_cpu = reactive(0.0)
    current_mem = reactive(0.0)

    def compose(self) -> ComposeResult:
        with Vertical(classes="monitor-box"):
            yield Label(f"CPU Vitality ({self.current_cpu:.1f}%)")
            yield Sparkline(self.cpu_history, summary_function=max, color="green")
        with Vertical(classes="monitor-box"):
            yield Label(f"Memory Pressure ({self.current_mem:.1f}MB)")
            yield Sparkline(self.ram_history, summary_function=max, color="blue")

    def watch_current_cpu(self, value: float):
        self.query_one(Label).update(f"CPU Vitality ({value:.1f}%)")

    def watch_current_mem(self, value: float):
        # Find the correct label to update
        for label in self.query(Label):
            if "Memory" in str(label.renderable):
                label.update(f"Memory Pressure ({value:.1f}MB)")

    def update_stats(self, pid: Optional[int], is_demo: bool):
        cpu, mem = 0.0, 0.0
        if PSUTIL_AVAILABLE and pid and psutil.pid_exists(pid):
            try:
                proc = psutil.Process(pid)
                cpu = proc.cpu_percent(interval=None)
                mem = proc.memory_info().rss / (1024 * 1024)  # MB
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process has dissolved, flatline the vitals
                cpu, mem = 0.0, 0.0
        elif is_demo:
            # Heuristic simulation for demo mode
            cpu = random.uniform(5.0, 25.0) + (random.sin(time.time() * 0.5) * 5)
            mem = 150 + (random.sin(time.time() * 0.2) * 50)

        # Update reactive properties to trigger UI re-render
        self.current_cpu = cpu
        self.current_mem = mem

        new_cpu_deque = self.cpu_history
        new_cpu_deque.append(cpu)
        self.cpu_history = new_cpu_deque

        new_ram_deque = self.ram_history
        new_ram_deque.append(mem)
        self.ram_history = new_ram_deque


class TrafficVisualizer(Static):
    """The Flow of Data."""

    def compose(self) -> ComposeResult:
        yield DataTable(zebra_stripes=True)

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Time", "Method", "Path", "Status", "Latency")

    def add_request(self, method: str, path: str, status: int, latency: str):
        table = self.query_one(DataTable)
        status_color = "green" if status < 400 else "red" if status >= 500 else "yellow"
        fmt_status = Text(str(status), style=f"bold {status_color}")
        table.add_row(time.strftime("%H:%M:%S"), method, path, fmt_status, latency, key=str(time.time()))
        if len(table.rows) > 100: table.remove_row(table.rows[0][0])
        table.scroll_end(animate=False)


class NeuralDashboardApp(App):
    CSS_PATH = "dashboard.css"
    BINDINGS = [Binding("q", "quit", "Quit"), Binding("ctrl+c", "quit", "Quit")]

    # [ASCENSION 4]: HAPTIC STATUS AURA
    status_aura = reactive("green")

    def __init__(self, target_pid: Optional[int], log_file: Optional[str], demo_mode: bool):
        super().__init__()
        self.target_pid = target_pid
        self.log_file = Path(log_file) if log_file else None
        self.demo_mode = demo_mode
        self._stop_threads = threading.Event()
        self._log_thread: Optional[threading.Thread] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield SystemMonitor(id="sys-mon")
        yield TrafficVisualizer(id="traffic-panel")
        yield Log(id="log-panel", classes="box", max_lines=2000)
        yield Footer()

    def on_mount(self):
        # [ASCENSION 10]: SOCRATIC STARTUP GUIDANCE
        log_panel = self.query_one("#log-panel", Log)
        log_panel.write(Text("Neural Link Established. Awaiting Gnostic Telemetry...", style="bold green"))

        if self.target_pid:
            log_panel.write(f"Vigil anchored to Process ID: [bold cyan]{self.target_pid}[/bold cyan]")
        elif self.log_file:
            log_panel.write(f"Tailing scripture: [bold yellow]{self.log_file}[/bold yellow]")
            self._start_log_tail()
        elif self.demo_mode:
            log_panel.write("[bold purple]Engaging DEMO MODE. Simulating kinetic activity.[/bold purple]")

        self.set_interval(1.0, self.tick)

    def action_quit(self) -> None:
        self._stop_threads.set()
        if self._log_thread:
            self._log_thread.join(timeout=0.5)
        self.exit()

    def tick(self):
        # 1. Update Vitals
        self.query_one(SystemMonitor).update_stats(self.target_pid, self.demo_mode)

        # 2. Check for Process Death (Forensic Autopsy)
        if self.target_pid and PSUTIL_AVAILABLE and not psutil.pid_exists(self.target_pid):
            log_panel = self.query_one("#log-panel", Log)
            log_panel.write(Text(f"FATAL_FRACTURE: Process {self.target_pid} has dissolved.", style="bold red"))
            self.target_pid = None  # Stop monitoring

        # 3. Simulate Traffic
        if self.demo_mode and random.random() > 0.5:
            methods, paths = ["GET", "POST"], ["/api/v1/users", "/auth/login"]
            status_codes = [200, 201, 400, 500]
            self.query_one(TrafficVisualizer).add_request(
                random.choice(methods), random.choice(paths),
                random.choice(status_codes), f"{random.randint(10, 500)}ms"
            )
            self.query_one("#log-panel", Log).write(f"[DIM] Simulated request processed.")

        # 4. Update Aura
        cpu = self.query_one(SystemMonitor).current_cpu
        if cpu > 85:
            self.status_aura = "red"
        elif cpu > 60:
            self.status_aura = "yellow"
        else:
            self.status_aura = "green"
        self.screen.styles.border = ("heavy", self.status_aura)

    def _start_log_tail(self):
        """[ASCENSION 2]: ACHRONAL LOG SIPHONING"""
        if not self.log_file: return
        self._log_thread = threading.Thread(target=self._tail_worker, daemon=True)
        self._log_thread.start()

    def _tail_worker(self):
        """Non-blocking file tailing rite."""
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as f:
                # [ASCENSION 7]: THE "LIVE TAIL" SENTINEL
                f.seek(0, 2)  # Go to the end of the file
                while not self._stop_threads.is_set():
                    line = f.readline()
                    if line:
                        # Schedule write on the main event loop
                        self.call_from_thread(self.query_one("#log-panel", Log).write, line)
                    else:
                        time.sleep(0.1)  # Yield
        except FileNotFoundError:
            self.call_from_thread(self.query_one("#log-panel", Log).write,
                                  Text(f"HERESY: Log scripture '{self.log_file}' is a void.", style="bold red"))
        except Exception as e:
            self.call_from_thread(self.query_one("#log-panel", Log).write,
                                  Text(f"Log Siphon Fracture: {e}", style="bold red"))