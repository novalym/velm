# Path: artisans/neural_link/dashboard.py
# ---------------------------------------

import psutil
import time
import random
from collections import deque
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Sparkline, Label, DataTable
from textual.containers import Grid, Vertical, Horizontal
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel


class SystemMonitor(Static):
    """The Heartbeat Sensor."""
    cpu_history = reactive(deque([0.0] * 60, maxlen=60))
    ram_history = reactive(deque([0.0] * 60, maxlen=60))

    def compose(self) -> ComposeResult:
        with Vertical(classes="monitor-box"):
            yield Label("CPU Vitality")
            yield Sparkline(self.cpu_history, summary_function=max, color="green")
        with Vertical(classes="monitor-box"):
            yield Label("Memory Pressure")
            yield Sparkline(self.ram_history, summary_function=max, color="blue")

    def update_stats(self, pid: Optional[int]):
        # Mock or Real Data
        if pid:
            try:
                proc = psutil.Process(pid)
                cpu = proc.cpu_percent()
                mem = proc.memory_info().rss / (1024 * 1024)  # MB
            except:
                cpu, mem = 0, 0
        else:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent

        self.cpu_history.append(cpu)
        self.ram_history.append(mem)
        self.cpu_history = self.cpu_history  # Trigger reactivity
        self.ram_history = self.ram_history


class TrafficVisualizer(Static):
    """The Flow of Data."""

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Time", "Method", "Path", "Status", "Latency")

    def add_request(self, method: str, path: str, status: int, latency: str):
        table = self.query_one(DataTable)

        # Colorize status
        status_color = "green" if status < 400 else "red" if status >= 500 else "yellow"
        fmt_status = Text(str(status), style=f"bold {status_color}")

        table.add_row(
            time.strftime("%H:%M:%S"),
            method,
            path,
            fmt_status,
            latency
        )
        # Scroll to bottom
        table.scroll_end(animate=False)


class NeuralDashboardApp(App):
    CSS = """
    Screen { layout: grid; grid-size: 2; grid-rows: 1fr 2fr; }
    .monitor-box { border: solid $accent; padding: 1; height: 100%; }
    #log-panel { grid-column: span 2; border-top: solid $primary; }
    #traffic-panel { grid-column: 2; border-left: solid $primary; }
    Sparkline { height: 1fr; }
    Label { text-align: center; width: 100%; }
    """

    def __init__(self, target_pid: Optional[int], log_file: Optional[str], demo_mode: bool):
        super().__init__()
        self.target_pid = target_pid
        self.log_file = Path(log_file) if log_file else None
        self.demo_mode = demo_mode

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield SystemMonitor(id="sys-mon")
        yield TrafficVisualizer(id="traffic-panel")
        yield Log(id="log-panel", classes="box")
        yield Footer()

    def on_mount(self):
        self.set_interval(1.0, self.tick)
        self.query_one("#log-panel").write(Text("Neural Link Established.", style="bold green"))

        if self.target_pid:
            self.query_one("#log-panel").write(f"Attached to PID: {self.target_pid}")
        elif self.log_file:
            self.query_one("#log-panel").write(f"Tailing: {self.log_file}")
            # In real impl, launch a thread to tail -f

    def tick(self):
        # 1. Update Vitals
        self.query_one(SystemMonitor).update_stats(self.target_pid)

        # 2. Simulate Traffic (Demo Mode)
        if self.demo_mode:
            methods = ["GET", "POST", "PUT", "DELETE"]
            paths = ["/api/v1/users", "/auth/login", "/metrics", "/health"]
            status_codes = [200, 200, 200, 201, 400, 401, 500]

            if random.random() > 0.6:
                self.query_one(TrafficVisualizer).add_request(
                    random.choice(methods),
                    random.choice(paths),
                    random.choice(status_codes),
                    f"{random.randint(10, 500)}ms"
                )
                self.query_one("#log-panel").write(f"[INFO] Simulated request processed.")